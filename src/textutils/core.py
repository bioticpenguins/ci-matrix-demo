"""Text manipulation utilities."""

import re


def slugify(s: str) -> str:
    """Convert a string to a URL-friendly slug.

    Lowercases the input, replaces non-alphanumeric characters with hyphens,
    collapses consecutive hyphens, and strips leading/trailing hyphens.
    Unicode letters are preserved; only non-letter/non-digit chars become hyphens.
    """
    s = s.lower()
    s = re.sub(r"[^\w]|_", "-", s)
    s = re.sub(r"-+", "-", s)
    return s.strip("-")


def truncate(s: str, n: int, suffix: str = "\u2026") -> str:
    """Truncate s to n characters total (including suffix) if longer than n."""
    if len(s) <= n:
        return s
    if n <= len(suffix):
        return suffix[:n]
    return s[: n - len(suffix)] + suffix


def word_count(s: str) -> int:
    """Count whitespace-separated tokens in s."""
    raise NotImplementedError
