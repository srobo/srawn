#!/usr/bin/env python3

import datetime
from pathlib import Path
import re

from feedgenerator import DefaultFeed
import mistune


working_dir = Path('.')
feed = DefaultFeed(
    title="SR(A)WN",
    link="https://studentrobotics.org/srawn/",
    description="Student Robotics (Almost) Weekly Newsletter",
    author_name="Student Robotics"
)
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

    feed.add_item(
        title=f"{sryear} Issue {issue}",
        link=link,
        description=content,
        unique_id=link,
        pubdate=datetime.date.fromisoformat(date),
        content=content
    )

with (working_dir / "out" / "html" / "rss.xml").open("w") as f:
    feed.write(f, "utf-8")
