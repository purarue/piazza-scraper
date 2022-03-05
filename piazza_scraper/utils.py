from datetime import datetime
import re
import html


def remove_tags(text: str) -> str:
    """
    Converts HTML to Python Unicode String
    """
    cleanr = re.compile("<.*?>")
    cleantext = re.sub(cleanr, "", text)
    return html.unescape(cleantext)


def parse_time(text: str = "2016-03-16T17:31:14Z") -> datetime:

    """
    Converts Piazza Date-time format into a
    pythonic construct.

    Examples of Piazza Datetime:
    - 2016-03-16T17:31:14Z
    """

    format = "%Y-%m-%dT%H:%M:%SZ"
    return datetime.strptime(text, format)


def parse_day(text: str = "01/18") -> datetime:
    if len(text) < 6:
        text += "/16"
    print(text)
    format = r"%m/%d/%y"
    return datetime.strptime(text, format)
