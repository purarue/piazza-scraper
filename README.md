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

## HPI

This is used in [HPI](https://github.com/seanbreckenridge/HPI) with the `my.piazza.scraper` module -- it locates, infers my user in the export and returns my posts, allowing me to summarize/query easily:

```bash
$ hpi doctor -S my.piazza.scraper
✅ OK  : my.piazza.scraper
✅     - stats: {'posts': {'count': 22}}
# e.g. extract text from one of the posts
$ hpi query my.piazza.scraper.posts --order-key created --reverse | jq '.[6].text'
"bash doesn't exist where the script assumes it is [which is /usr/bin/bash most linux systems]. You need to run the grading script on the server or change the shebang value at the top"
```
