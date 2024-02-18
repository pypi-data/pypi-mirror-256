import asyncio
import re
import shutil
import sys
import zipfile as zf
from collections.abc import Iterator
from concurrent.futures.thread import ThreadPoolExecutor
from dataclasses import dataclass, field
from enum import IntEnum, auto
from operator import itemgetter
from pathlib import Path
from threading import Thread
from typing import NamedTuple

import httpx
import questionary as qy
import requests
from bs4 import BeautifulSoup as bs
from bs4 import Tag
from loguru import logger
from rapidfuzz import fuzz, process

BASE = "https://zenius-i-vanisher.com/v5.2/"
SEARCH = f"{BASE}simfiles_search_ajax.php"


class Job(NamedTuple):
    name: str
    thread: Thread


class Jobs:
    tracker: list[Job] = []

    @classmethod
    def track_jobs(cls) -> None:
        running: list[Job] = []
        for job in cls.tracker:
            if job.thread.is_alive():
                running.append(job)
            else:
                logger.info(f"END THREAD: {job.name}")
        cls.tracker = running

    @classmethod
    def add(cls, name: str, thread: Thread) -> None:
        logger.trace(f"START THREAD: {name}")
        thread.daemon = True
        thread.start()
        cls.tracker.append(Job(name, thread))


class Storage:
    root: Path = Path.home() / ".local" / "zenius"
    songs: Path = root / "songs"
    log: Path = root / "vanisher.log"


Storage.songs.mkdir(parents=True, exist_ok=True)


class Group(IntEnum):
    ARCADE = auto()
    SPINOFF = auto()
    OFFICIAL = auto()
    USER = auto()
    INVALID = auto()


@dataclass
class Sim:
    idx: str
    _title: str = ""

    @property
    def site(self) -> str:
        raise NotImplementedError

    @property
    def zipfile(self) -> str:
        raise NotImplementedError

    @property
    def title(self) -> str:
        if self._title == "":
            html = requests.get(self.site).text
            if match := re.search(r"<h1>\s?(.+?)(?=\s\/\s|<\/h1>)", html):
                self._title = match.group(1)
        return self._title


@dataclass
class Category(Sim):
    @property
    def site(self) -> str:
        return f"{BASE}viewsimfilecategory.php?categoryid={self.idx}"

    @property
    def zipfile(self) -> str:
        return f"{BASE}download.php?type=ddrpack&categoryid={self.idx}"


@dataclass
class Simfile(Sim):
    @property
    def site(self) -> str:
        return f"{BASE}viewsimfile.php?simfileid={self.idx}"

    @property
    def zipfile(self) -> str:
        return f"{BASE}download.php?type=ddrsimfile&simfileid={self.idx}"

    @property
    def zipfile_custom(self) -> str:
        return f"{BASE}download.php?type=ddrsimfilecustom&simfileid={self.idx}"


@dataclass
class Result:
    song_name: str
    song_page: str
    pack_name: str
    pack_page: str
    group: str
    difficulties: list[str] = field(default_factory=list)
    artist: str = field(default_factory=str)

    @property
    def song(self) -> Simfile:
        simfile = Simfile("", self.song_name)
        if match := re.search(r"id=(\d+)", self.song_page):
            simfile.idx = match.group(1)
        return simfile

    @property
    def pack(self) -> Category:
        category = Category("", self.pack_name)
        if match := re.search(r"id=(\d+)", self.pack_page):
            category.idx = match.group(1)
        return category

    @property
    def entry(self) -> str:
        return f"{self.song_name} | {self.artist} | {','.join(self.difficulties)} | {self.pack_name}"


def get_group(listing: Tag) -> set[Group]:
    groups = set()
    if (parent := listing.find_parent()) is not None:
        if group := parent.find_previous_sibling():
            if group.text != "User":
                groups.add(Group.OFFICIAL)
                if group.text == "Arcade":
                    groups.add(Group.ARCADE)
                else:
                    groups.add(Group.SPINOFF)
            elif group.text == "User":
                groups.add(Group.USER)
    if not groups:
        return {Group.INVALID}
    return groups


def categories(group: Group) -> Iterator[Category]:
    response = requests.get(f"{BASE}simfiles.php?category=simfiles").content
    soup = bs(response, "lxml")
    for listing in soup.select("tr td.border select"):
        if group in get_group(listing):
            for category in listing.select("option"):
                if (idx := category["value"]) != "0" and isinstance(idx, str):
                    yield Category(idx, category.text)


def search_pack(
    query: str,
    group: Group = Group.USER,
    limit: int = 15,
) -> tuple[Category]:
    packs = list(categories(group))
    titles = [entry.title for entry in packs]
    results = process.extract(
        query,
        choices=titles,
        scorer=fuzz.partial_ratio,
        limit=limit,
    )
    getter = itemgetter(*[result[2] for result in results])
    matches: tuple[Category] = getter(packs)
    return matches


def search_song(title: str = "", artist: str = "") -> list[Result]:
    data = {"songtitle": f"{title}", "songartist": f"{artist}"}
    r = requests.post(SEARCH, data=data).text
    soup = bs(r, "lxml")
    results = []
    current_group = ""
    for tag in soup.find_all("tr"):
        if subtag := tag.find("th"):
            current_group = subtag.text.lower().split(" ")[0]
        entries = tag.find_all("a")
        if len(entries) == 2:
            song, pack = entries
            result = Result(
                song.text,
                f"{BASE}{song['href']}",
                pack.text,
                f"{BASE}{pack['href']}",
                current_group,
            )
            results.append(result)
    if results:
        with asyncio.Runner() as runner:
            results = runner.run(process_results(results))
    return results


async def process_results(results: list[Result]) -> list[Result]:
    async with httpx.AsyncClient() as client:
        tasks = []
        for result in results:
            tasks.append(asyncio.create_task(client.get(result.song.site)))
        responses = await asyncio.gather(*tasks)
    htmls = (r.text for r in responses)
    new_results = []
    for result, html in zip(results, htmls):
        if diffs := re.findall(r"Single(?:(?<!None).)+Done\s-\sLevel\s(\d+)", html):
            result.difficulties = diffs
        if match := re.search(r"\/\s(.*)</h1", html):
            result.artist = match.group(1)
        new_results.append(result)
    return new_results


def download_custom(simfile: Simfile, prefix: Path) -> None:
    archive = prefix / Path(f"{simfile.title}.zip")
    with requests.get(simfile.zipfile_custom, stream=True) as response:
        with open(archive, "wb") as file:
            shutil.copyfileobj(response.raw, file)
    if zf.is_zipfile(archive):
        path = prefix
        if not any([simfile.title + "/" in x for x in zf.ZipFile(archive).namelist()]):
            path = prefix / simfile.title
        zf.ZipFile(archive).extractall(path=path)
        archive.unlink()
        logger.info(f"Downloaded {simfile.title}\n\t{simfile.site}")
    else:
        logger.error(f"Cannot download {simfile.site}")


def download_zip(
    sim: Sim, dump: bool = False, pack: str = "", cwd: bool = False
) -> None:
    if pack:
        prefix = Storage.songs / pack
        prefix.mkdir(parents=True, exist_ok=True)
    elif cwd:
        prefix = Path()
    elif dump:
        prefix = Storage.songs / "dump"
        prefix.mkdir(parents=True, exist_ok=True)
    else:
        prefix = Storage.songs
    archive = prefix / Path(f"{sim.title}.zip")
    with requests.get(sim.zipfile, stream=True) as response:
        with open(archive, "wb") as file:
            shutil.copyfileobj(response.raw, file)
    if zf.is_zipfile(archive):
        path = prefix
        if not any([sim.title + "/" in x for x in zf.ZipFile(archive).namelist()]):
            path = prefix / sim.title
        zf.ZipFile(archive).extractall(path=path)
        archive.unlink()
        logger.info(f"Downloaded {sim.title}\n\t{sim.site}")
    else:
        Path(archive).unlink()
        if isinstance(sim, Simfile):
            download_custom(sim, prefix)
        if isinstance(sim, Category):
            logger.info("No zipfile found, attempting to download songs")
            download_category_zips(sim)


def download_category_zips(category: Category) -> None:
    html = requests.get(category.site).text
    songs = re.findall(r'viewsimfile\.php\?simfileid=(\d+).*?title="(.*?)\s\/', html)
    for idx, title in songs:
        name = f"Downloading for {category.title}: {title}"
        thread = Thread(
            target=download_zip, args=[Simfile(idx, title), False, category.title]
        )
        Jobs.add(name, thread)


def download_group(group: Group) -> None:
    for category in categories(group):
        name = f"Downloading for {group.name}: {category.title}"
        thread = Thread(target=download_zip, args=[category])
        Jobs.add(name, thread)


def download_url(url: str) -> None:
    if match := re.search(r"(category|simfile)id=(\d+)", url):
        if len(match.groups()) == 2:
            typ, idx = match.groups()
            sim = Sim("")
            if typ == "category":
                sim = Category(idx)
                dump = False
            else:
                sim = Simfile(idx)
                dump = True
            print(f"Downloading {typ} {idx}")
            download_zip(sim, dump=dump)
            return
    logger.error(f"Not a valid url: {url}")


def interface(menu: str) -> str:
    if menu == "main":
        choices = [
            qy.Choice("Download bundles", "download", shortcut_key="d"),
            qy.Choice("Song search", "song", shortcut_key="s"),
            qy.Choice("Pack search", "pack", shortcut_key="p"),
        ]
        choice = qy.select(
            "Choose an option", choices=choices, use_shortcuts=True
        ).ask()
        if not choice:
            Jobs.track_jobs()
            jobs = Jobs.tracker
            if len(jobs) > 0:
                print(f"{len(jobs)} Active job(s):")
                for job in jobs:
                    print(f"\t{job.name}")
            message = "Do you want to quit?"
            if qy.confirm(message, default=False).ask() is True:
                return "exit"
        menu = choice
    if menu == "download":
        choices = [qy.Choice("Go back", value=Group.INVALID, shortcut_key="b")]
        choices.extend(
            [qy.Choice(g.name, g, shortcut_key=str(g.value)) for g in list(Group)[:3]]
        )
        group: Group = qy.select(
            "Choose group to download", choices=choices, use_shortcuts=True
        ).ask()
        if group is Group.INVALID or not group:
            return "main"
        name = f"Downloading group: {group.name}"
        print(name)
        thread = Thread(target=download_group, args=[group])
        Jobs.add(name, thread)
        return "download"
    if menu == "song":
        answers = qy.form(
            title=qy.text("Enter song name"), artist=qy.text("Enter artist name")
        ).ask()
        if not answers:
            return "main"
        title = answers.get("title", "")
        artist = answers.get("artist", "")
        if title == "" and artist == "":
            if qy.confirm("Would you like to go back to main menu?").ask():
                return "main"
            return menu
        print("Fetching results...")
        search_results = search_song(title, artist)
        if not search_results:
            print("No results found. Try again.")
            return "song"
        results = [qy.Choice(song.entry, song) for song in search_results]
        result = qy.select("Pick a song", choices=results, show_selected=True).ask()
        if not result:
            return "main"
        options = [
            qy.Choice("Download song", "song"),
            qy.Choice("Download pack", "pack"),
            qy.Choice("Download both", "both"),
        ]
        answer = qy.select("Choose an option", options).ask()
        if answer in ["song", "both"]:
            name = f"Downloading song: {result.song_name} by {result.artist}"
            thread = Thread(target=download_zip, args=[result.song, True])
            Jobs.add(name, thread)
        if answer in ["pack", "both"]:
            name = f"Downloading pack: {result.pack_name}"
            thread = Thread(target=download_zip, args=[result.pack])
            Jobs.add(name, thread)
        return menu
    if menu == "pack":
        query = qy.text(
            "Enter pack name or press leave blank to go back", default=""
        ).ask()
        if query == "" or query is None:
            return "main"
        packs = search_pack(query)
        choices = [qy.Choice("Go back", value=False, shortcut_key="b")]
        choices.extend([qy.Choice(pack.title, pack) for pack in packs])
        answer = qy.checkbox("Select packs to download", choices=choices).ask()
        if not answer or len(answer) == 0:
            return "pack"
        Jobs.track_jobs()
        for pack in answer:
            name = f"Downloading pack: {pack.title}"
            thread = Thread(target=download_zip, args=[pack])
            Jobs.add(name, thread)
        return "pack"
    return "main"


usage = """Usage:
    zenius [-l,--log] [url...]

    Enter the cli by not passing args.
    Log located at $HOME/.local/zenius/vanisher.log
"""


def main() -> None:
    logger.remove()
    logger.add(Storage.log, retention="1 day")
    args = sys.argv[1:]
    if any(x in args for x in ["-h", "--help", "help"]):
        print(usage)
    elif any(x in args for x in ["-l", "--log", "log"]):
        with open(Storage.log) as f:
            shutil.copyfileobj(f, sys.stdout)
    elif args:
        with ThreadPoolExecutor() as tp:
            tp.map(download_url, args)
    else:
        menu = "main"
        while True:
            if menu == "exit":
                break
            Jobs.track_jobs()
            menu = interface(menu)


if __name__ == "__main__":
    main()
