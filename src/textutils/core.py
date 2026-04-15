"""Text manipulation utilities."""


def slugify(s: str) -> str:
    """Convert a string to a URL-friendly slug."""
    raise NotImplementedError


def truncate(s: str, n: int, suffix: str = "\u2026") -> str:
    """Truncate s to n characters, appending suffix if truncated."""
    raise NotImplementedError


def word_count(s: str) -> int:
    """Count whitespace-separated tokens in s."""
    raise NotImplementedError
