import json
from pathlib import Path
from typing import List, Dict, Any, NamedTuple, Iterator, Optional, cast
from dataclasses import dataclass
from datetime import datetime, timezone

from bs4 import BeautifulSoup  # type: ignore[import]

Json = Dict[str, Any]


def parse_datetime(text: str) -> datetime:
    format = r"%Y-%m-%dT%H:%M:%SZ"
    return datetime.strptime(text, format)


def html_to_text(html: str) -> str:
    return cast(str, BeautifulSoup(html, "html.parser").text)


class Post:
    def __init__(self, raw: Json, *, class_id: str, _post_nr: Optional[int] = None):
        self.raw = raw
        self.class_id = class_id
        self._post_nr = _post_nr  # uid which is incremented for post count

    # serialize helper method for HPI/core.serialize so this calls property methods properly
    def _serialize(self) -> Any:
        return {
            "raw": self.raw,
            "class_id": self.class_id,
            "permalink": self.permalink,
            "text": self.text,
            "created": self.created,
        }

    @property
    def created(self) -> datetime:
        assert "created" in self.raw
        created_str = self.raw["created"]
        naive = datetime.fromisoformat(created_str.rstrip("Z"))
        return naive.replace(tzinfo=timezone.utc)

    @property
    def permalink(self) -> str:
        return f"https://piazza.com/class/{self.class_id}?cid={self.post_nr}"

    @property
    def post_nr(self) -> int:
        if self._post_nr is not None:
            return self._post_nr
        nr: Optional[int] = self.raw.get("nr")
        if nr is not None:
            assert isinstance(nr, int), "Expected nr (post number) to be an integer"
            return nr
        raise RuntimeError("Could not fetch a postnr (or was not set by parent post)")

    @property
    def text(self) -> str:
        assert "subject" in self.raw
        buf = html_to_text(self.raw["subject"])
        if "content" in self.raw:
            buf += f"\n{html_to_text(self.raw['content'])}"
        return buf.strip()

    @classmethod
    def _filter_post_format(cls, blob: Json) -> Iterator[Json]:
        if "subject" in blob and "created" in blob:
            yield blob

    def walk_posts_by_me(self, user_id: str) -> Iterator["Post"]:
        for post in self.walk_posts():
            uid: Optional[str] = None
            if "uid" in post.raw:
                uid = post.raw["uid"]
            elif "id" in post.raw:
                uid = post.raw["id"]
            if uid == user_id:
                yield post

    def walk_posts(self, **kwargs: Any) -> Iterator["Post"]:
        use_raw = kwargs.get("raw", self.raw)
        use_class_id = kwargs.get("class_id", self.class_id)
        use_post_nr = kwargs.get("_post_nr", self.post_nr)
        for blob in self.__class__._filter_post_format(use_raw):
            yield Post(raw=blob, class_id=use_class_id, _post_nr=use_post_nr)
        # use post datetime to remove duplicates
        # check main post body
        if "history" in use_raw:
            assert isinstance(
                use_raw["history"], list
            ), f"Expected history to be a list {use_raw['history']}"
            # history is where all data comes from
            # children can contain history nodes, which get discovered
            # from the recursive call below
            for hst in use_raw["history"]:
                for blob in self.__class__._filter_post_format(hst):
                    yield Post(raw=blob, class_id=use_class_id, _post_nr=use_post_nr)
        # check children (comments)
        if "children" in use_raw:
            assert isinstance(
                use_raw["children"], list
            ), f"Expected children to be a list {use_raw['children']}"
            for ch in use_raw["children"]:
                # breakpoint()
                for blob in self.__class__._filter_post_format(ch):
                    yield Post(raw=blob, class_id=use_class_id, _post_nr=use_post_nr)
                # we've recursed to the bottom -- no more posts
                for hst in ch.get("history", []):
                    yield from self.walk_posts(
                        raw=hst, class_id=use_class_id, _post_nr=use_post_nr
                    )
                for ch in ch.get("children", []):
                    yield from self.walk_posts(
                        raw=ch, class_id=use_class_id, _post_nr=use_post_nr
                    )


class User(NamedTuple):
    uid: str
    name: str
    email: str


@dataclass
class Export:
    class_id: str
    stats: Dict[str, Any]
    users: List[User]
    posts: List[Post]

    @staticmethod
    def parse_file(pth: Path, class_id: Optional[str] = None) -> "Export":
        data = json.loads(pth.read_text())
        # e.g. /somedir/k8ansk12uxq6hf.json -> k8ansk12uxq6hf
        if class_id is None:
            class_id = pth.stem
        return Export(
            class_id=class_id,
            stats=data["stats"],
            users=[
                User(u["user_id"], u["name"], u["email"])
                for u in data["stats"]["users"]
            ],
            posts=[Post(raw, class_id=class_id) for raw in data["posts"].values()],
        )
