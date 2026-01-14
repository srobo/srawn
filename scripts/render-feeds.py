#!/usr/bin/env python3

import datetime
from html.parser import HTMLParser
from io import StringIO
from pathlib import Path
import re

from feedgenerator import DefaultFeed
import mistune


def strip_tags(html):
    class MLStripper(HTMLParser):
        def __init__(self):
            super().__init__()
            self.reset()
            self.strict = False
            self.convert_charrefs = True
            self.text = StringIO()

        def handle_data(self, d):
            self.text.write(d)

        def get_data(self):
            return self.text.getvalue()

    s = MLStripper()
    s.feed(html)
    return s.get_data()

FEED_ARGS = {
    "title": "SR(A)WN",
    "link": "https://studentrobotics.org/srawn/",
    "description": "Student Robotics (Almost) Weekly Newsletter",
    "author_name": "Student Robotics"
}


working_dir = Path('.')
feed = DefaultFeed(**FEED_ARGS)
simple_feed = DefaultFeed(**FEED_ARGS)
md = mistune.create_markdown()


for md_path in sorted(working_dir.glob("SR20*/*.md")):
    filename_match = re.match("^(20\d{2}-\d{2}-\d{2})-srawn-(\d{2})$", md_path.stem)
    if not filename_match:
        exit(f"{md_path.stem} does not match format. Run the linter.")
    date, issue = filename_match.groups()

    folder_match = re.match("^(SR20\d{2})$", md_path.parent.name)
    if not folder_match:
        exit(f"{md_path.parent.name} does not match format. Run the linter.")
    sryear, = folder_match.groups()

    link = f"https://studentrobotics.org/srawn/{md_path.parent.stem}/{md_path.stem}.html"
    content = md(md_path.read_text())
    title = f"{sryear} Issue {issue}"
    publish_date = datetime.date.fromisoformat(date)

    feed.add_item(
        title=title,
        link=link,
        unique_id=link,
        pubdate=publish_date,
        description=content,
    )
    simple_feed.add_item(
        title=title,
        link=link,
        unique_id=link,
        pubdate=publish_date,
        description=strip_tags(content),
    )

output_dir = working_dir / "out" / "html"

with (output_dir / "rss.xml").open("w") as f:
    feed.write(f, "utf-8")

with (output_dir / "rss-simple.xml").open("w") as f:
    simple_feed.write(f, "utf-8")
