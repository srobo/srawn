#!/usr/bin/env python3
import re
from pathlib import Path

import jinja2

import srawn_utils

# cspell:disable-next-line
templateLoader = jinja2.FileSystemLoader(searchpath="./templates")
templateEnv = jinja2.Environment(loader=templateLoader)
archive_template = templateEnv.get_template("archive-index.html.j2")
year_template = templateEnv.get_template("year-index.html.j2")

working_dir = Path('.')
html_dir = working_dir / "out/html"

years = srawn_utils.get_years(working_dir)

# render main index
with html_dir.joinpath("index.html").open("w") as fh:
    fh.write(archive_template.render(years=years))

with srawn_utils.exit_on_invalid():
    # render year indices
    for year in years:
        year_html_path = html_dir / year
        year_path = working_dir / year
        issue_data = []
        for issue in srawn_utils.get_year_issues(year_path):
            issue_data.append((
                issue.path.stem,
                f"{issue.date_text}: {issue.title}",
            ))

        with year_html_path.joinpath("index.html").open("w") as fh:
            fh.write(year_template.render(year=year, issues=issue_data))
