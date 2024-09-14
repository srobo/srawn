import contextlib
import dataclasses
import datetime
import re
from collections.abc import Iterator
from pathlib import Path

YEAR_FOLDER_PATTERN = re.compile(r"^(SR20\d{2})$")
ISSUE_FILENAME_PATTERN = re.compile(r"^(20\d{2}-\d{2}-\d{2})-srawn-(\d{2}).md$")


class InvalidPath(ValueError):
    pass


@dataclasses.dataclass(frozen=True)
class ParsedIssuePath:
    path: Path
    date: datetime.date
    issue_number: str
    sryear: str

    @property
    def title(self) -> str:
        return f"{self.sryear} Issue {self.issue_number}"

    @property
    def date_text(self) -> str:
        return self.date.isoformat()


def parse_path(path: Path) -> ParsedIssuePath:
    filename_match = ISSUE_FILENAME_PATTERN.match(path.name)
    if not filename_match:
        raise InvalidPath(
            f"{path.name!r} does not match format. Run the linter.",
        )
    date, issue_number = filename_match.groups()

    folder_match = YEAR_FOLDER_PATTERN.match(path.parent.name)
    if not folder_match:
        raise InvalidPath(
            f"{path.parent.name!r} does not match format. Run the linter.",
        )
    sryear, = folder_match.groups()

    return ParsedIssuePath(
        path,
        datetime.date.fromisoformat(date),
        issue_number,
        sryear,
    )


@contextlib.contextmanager
def exit_on_invalid() -> Iterator[None]:
    try:
        yield
    except InvalidPath as e:
        exit(str(e))


def get_years(root: Path) -> list[Path]:
    return sorted(root.glob("SR20*"), reverse=True)


def get_year_issues(year_root: Path) -> list[ParsedIssuePath]:
    paths = sorted(year_root.glob("*.md"))
    return [parse_path(x) for x in paths]


def get_all_issues(root: Path) -> list[ParsedIssuePath]:
    paths = sorted(root.glob("SR20*/*.md"))
    return [parse_path(x) for x in paths]
