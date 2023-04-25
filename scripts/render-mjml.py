#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path
from typing import Dict, Optional, Tuple

import jinja2
import mistune

FONTS: Dict[int, Tuple[str, int, Optional[int]]] = {
    0: ("Open Sans", 20, 25),  # Paragraph
    1: ("Open Sans", 35, None),
    2: ("Open Sans", 30, None),
    3: ("Open Sans", 27, None),
    4: ("Open Sans", 25, None),
}


class MJMLRenderer(mistune.HTMLRenderer):

    def block_code(self, code, info=None) -> None:
        raise ValueError("Codespan not supported for SRAWN")

    def block_quote(self, text) -> None:
        raise ValueError("Block quote not supported for SRAWN")

    def heading(self, text: str, level: int) -> str:
        return self.render_paragraph_font(text, level)

    def list(self, text, ordered, level, start=None) -> str:
        rendered_list = super().list(text, ordered, level, start=start)

        if level == 1:
            # Enclose in paragraph if top level
            return self.paragraph(rendered_list)
        else:
            return rendered_list

    def paragraph(self, text: str) -> str:
        return self.render_paragraph_font(text, 0)

    def thematic_break(self) -> str:
        return ''

    def render_paragraph_font(self, text: str, level: int) -> str:
        family, size, line_height = FONTS[level]
        return self.render_paragraph(text, font_size=size, font_family=family, line_height=line_height)

    def render_paragraph(self, text: str, *, font_size: int, font_family: str, line_height: Optional[int]) -> str:
        if line_height is not None:
            return f'<mj-text font-size="{font_size}px" font-family="{font_family}" line-height="{line_height}px">{text}</mj-text>'
        else:
            return f'<mj-text font-size="{font_size}px" font-family="{font_family}">{text}</mj-text>'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Render a markdown file to mjml')
    parser.add_argument('markdown', help='Markdown file to render')
    args = parser.parse_args()

    md_path = Path(args.markdown)
    if not md_path.is_file():
        exit(f"{md_path} is not a file")

    filename_match = re.match("^(20\d{2}-\d{2}-\d{2})-srawn-(\d{2})$", md_path.stem)
    if not filename_match:
        exit(f"{md_path.stem} does not match format. Run the linter.")
    date, issue = filename_match.groups()

    folder_match = re.match("^(SR20\d{2})$", md_path.parent.name)
    if not folder_match:
        exit(f"{md_path.parent.name} does not match format. Run the linter.")
    sryear, = folder_match.groups()


    with md_path.open("r") as fh:
        raw_markdown = fh.read()

    # Remove title from old issues. This prevents duplicate titles in the archive
    # without changing the original files.
    raw_markdown = re.sub("^# SR\(A\)WN \d{4} [—-]+ \d+$", "", raw_markdown, flags=re.MULTILINE)


    md = mistune.create_markdown(renderer=MJMLRenderer())
    content = md(raw_markdown)

    templateLoader = jinja2.FileSystemLoader(searchpath="./templates")
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template("newsletter.mjml.j2")

    output = template.render(
        date=date,
        sryear=sryear,
        issue=issue,
        content=content,
    )
    print(output)
