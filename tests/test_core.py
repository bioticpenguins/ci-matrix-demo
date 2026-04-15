"""Tests for textutils.core."""

import pytest

from textutils.core import slugify, truncate, word_count


class TestSlugify:
    def test_basic(self) -> None:
        assert slugify("Hello World") == "hello-world"

    def test_collapses_runs(self) -> None:
        assert slugify("foo   bar---baz") == "foo-bar-baz"

    def test_trims_edges(self) -> None:
        assert slugify("  --hello--  ") == "hello"

    def test_unicode_letters_preserved(self) -> None:
        # letters outside ASCII are kept (lowercased), separators are replaced
        assert slugify("Ångström") == "ångström"

    def test_empty_string(self) -> None:
        assert slugify("") == ""

    def test_only_separators(self) -> None:
        assert slugify("---") == ""


class TestTruncate:
    pass

    def test_n_smaller_than_suffix(self) -> None:
        # n=2 with suffix="..." (3 chars) — no room for content, clip suffix
        assert truncate("hello", 2, "...") == ".."


class TestWordCount:
    pass
