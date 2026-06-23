#!/usr/bin/env python3

import datetime
from pathlib import Path
import re

from feedgenerator import DefaultFeed
import mistune

import srawn_utils

working_dir = Path('.')
feed = DefaultFeed(
    title="SR(A)WN",
    link="https://studentrobotics.org/srawn/",
    description="Student Robotics (Almost) Weekly Newsletter",
    author_name="Student Robotics"
)
md = mistune.create_markdown()


for issue in srawn_utils.get_all_issues(working_dir):
    md_path = issue.path
    link = f"https://studentrobotics.org/srawn/{md_path.parent.stem}/{md_path.stem}.html"
    content = md(md_path.read_text())

    feed.add_item(
        title=issue.title,
        link=link,
        description=content,
        unique_id=link,
        pubdate=issue.date,
        content=content
    )

with (working_dir / "out" / "html" / "rss.xml").open("w") as f:
    feed.write(f, "utf-8")
