from pathlib import Path

import click


@click.group()
def main() -> None:
    "Scrape posts from Piazza"
    pass


@main.command(short_help="run scraper")
@click.argument("COURSEID", type=str)
def scrape(courseid: str) -> None:
    "Run the piazza scraper for COURSEID"
    from .scraper import Scraper

    s = Scraper(courseid)
    s.parse()
    s.write()


@main.command(short_help="parse file")
@click.argument(
    "JSON_DUMP",
    type=click.Path(
        exists=True, dir_okay=False, readable=True, path_type=Path, resolve_path=True
    ),
)
def parse(json_dump: str) -> None:
    "Parse a dumped json file"
    import IPython  # type: ignore[import]
    from .parse import Export

    res = Export.parse_file(Path(json_dump))  # noqa
    IPython.embed(header=f"Use {click.style('res', fg='green')} to access visit data")


if __name__ == "__main__":
    main()
