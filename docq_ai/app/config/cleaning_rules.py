import re

PAGE_NUMBER_PATTERNS = [
    re.compile(r"Page\s+\d+\s+of\s+\d+", re.IGNORECASE),
]

MULTIPLE_NEWLINES = re.compile(r"\n\s*\n\s*\n+")

MULTIPLE_SPACES = re.compile(r"[ \t]{2,}")

CONTROL_CHARACTERS = re.compile(r"[\x00-\x1F\x7F]")

REPEATED_SYMBOLS = re.compile(r"^[*\-_]{3,}$", re.MULTILINE)

JOINED_WORDS = re.compile(r"([a-z])([A-Z])")

BULLET_PATTERN = re.compile(r"•(?=\w)")