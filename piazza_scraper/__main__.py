import click

from .scraper import Scraper


@click.group()
def main() -> None:
    "Scrape posts from Piazza"
    pass


@main.command(short_help="run scraper")
@click.argument("COURSEID", type=str)
def scrape(courseid: str) -> None:
    "Run the piazza scraper for COURSEID"
    s = Scraper(courseid)
    s.parse()
    s.write()


if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
