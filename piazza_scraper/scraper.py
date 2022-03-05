import json
from typing import Dict, Any
from pathlib import Path
import time

import click
from piazza_api import Piazza  # type: ignore[import]

from .config import Config


class Scraper:
    """
    Usage for Scraper:

    >>> s = Scraper() # Initializes scraper/db connection
    >>> s.get(10) #Fetches 10 posts and stores them
    >>> s.print_topics() # Prints list of current topics/tags
    >>> s.print_posts() # Prints all posts in DB
    """

    def __init__(self, courseid: str):
        self.piazza = Piazza()
        self.piazza.user_login(email=Config.username, password=Config.password)
        self.course = self.piazza.network(courseid)
        self.datapath = Path(f"{courseid}.json")
        self.data: Dict[str, Any] = {}
        if self.datapath.exists():
            self.data = json.loads(self.datapath.read_text())
        self.posts = self.data.get("posts", {})

    def parse(self):
        self.data["stats"] = self.course.get_statistics()
        self.get_all_posts()
        # TODO: get users for each id in posts

    def write(self):
        self.data["posts"] = self.posts
        self.datapath.write_text(json.dumps(self.data))

    def get_all_posts(self):
        for post in self.course.iter_all_posts():
            time.sleep(1)
            assert "id" in post
            uid = post["id"]
            self.posts[uid] = post
            self.write()
            print(post["history"][0]["subject"])


@click.command()
@click.argument("COURSEID", type=str)
def main(courseid: str) -> None:
    s = Scraper(courseid)
    s.parse()


if __name__ == "__main__":
    main()
