import json
from pathlib import Path
from typing import List, Dict, Any, NamedTuple
from dataclasses import dataclass
from datetime import datetime


def parse_datetime(text: str) -> datetime:
    format = r"%Y-%m-%dT%H:%M:%SZ"
    return datetime.strptime(text, format)


@dataclass
class Post:
    raw: Dict[str, Any]


class User(NamedTuple):
    uid: str
    name: str
    email: str


@dataclass
class Export:
    stats: Dict[str, Any]
    users: List[User]
    posts: List[Post]


def parse_file(pth: Path) -> Export:
    data = json.loads(pth.read_text())

    return Export(
        stats=data["stats"],
        users=[
            User(u["user_id"], u["name"], u["email"]) for u in data["stats"]["users"]
        ],
        posts=[Post(raw) for raw in data["posts"].values()],
    )
