# Piazza Scraper

Scrapes [piazza.com](http://piazza.com).

Modified to dump everything requested to JSON instead of a sqlite database

Removed the updating mechanisms -- this is meant to be used once, after my class is over, to export everything from the course

# Installation

```
pip install git+https://github.com/seanbreckenridge/piazza-scraper
```

# How to Run

Set the `PIAZZA_USERNAME` and `PIAZZA_PASSWORD` environment variables

```
python3 -m piazza_scraper scrape courseid
```

To parse:

```
python3 -m piazza_scraper parse ./courseid.json
```
