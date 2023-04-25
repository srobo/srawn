#!/usr/bin/env python3
import re
from pathlib import Path

import jinja2

# cspell:disable-next-line
templateLoader = jinja2.FileSystemLoader(searchpath="./templates")
templateEnv = jinja2.Environment(loader=templateLoader)
archive_template = templateEnv.get_template("archive-index.html.j2")
year_template = templateEnv.get_template("year-index.html.j2")

working_dir = Path('.')
html_dir = working_dir / "out/html"

years = sorted(working_dir.glob("SR20*"), reverse=True)

# render main index
with html_dir.joinpath("index.html").open("w") as fh:
    fh.write(archive_template.render(years=years))

# render year indices
for year in years:
    year_html_path = html_dir / year
    year_path = working_dir / year
    issues = sorted(year_path.glob("*.md"))
    issue_data = []
    for md_path in issues:
        filename_match = re.match("^(20\d{2}-\d{2}-\d{2})-srawn-(\d{2})$", md_path.stem)
        if not filename_match:
            exit(f"{md_path.stem} does not match format. Run the linter.")
        date, issue = filename_match.groups()

        folder_match = re.match("^(SR20\d{2})$", md_path.parent.name)
        if not folder_match:
            exit(f"{md_path.parent.name} does not match format. Run the linter.")
        sryear, = folder_match.groups()
        issue_data.append((md_path.stem, f"{date}: {sryear} Issue {issue}"))

    with year_html_path.joinpath("index.html").open("w") as fh:
        fh.write(year_template.render(year=year, issues=issue_data))
