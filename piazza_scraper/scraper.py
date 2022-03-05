import os
import json
import time
from typing import Dict, Any
from pathlib import Path

import click
from piazza_api import Piazza  # type: ignore[import]


class Config:
    username = os.environ["PIAZZA_USERNAME"]
    password = os.environ["PIAZZA_PASSWORD"]


class Scraper:
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

    def write(self):
        print(f"Writing to {self.datapath}")
        self.data["posts"] = self.posts
        self.datapath.write_text(json.dumps(self.data))

    def get_all_posts(self):
        for post in self.course.iter_all_posts():
            time.sleep(1)
            assert "id" in post
            uid = post["id"]
            self.posts[uid] = post
            print(post["history"][0]["subject"])


@click.command()
@click.argument("COURSEID", type=str)
def main(courseid: str) -> None:
    s = Scraper(courseid)
    s.parse()
    s.write()


if __name__ == "__main__":
    main()
