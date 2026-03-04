"""Tests for RSS feed generation."""

import xml.etree.ElementTree as ET
from pathlib import Path

import pytest


@pytest.fixture
def feed_path() -> Path:
    return Path(__file__).resolve().parent.parent / "database" / "feed.xml"


class TestRSSFeed:
    def test_feed_file_exists(self, feed_path: Path) -> None:
        assert feed_path.exists(), "database/feed.xml must exist after build"

    def test_feed_is_valid_xml(self, feed_path: Path) -> None:
        tree = ET.parse(feed_path)
        root = tree.getroot()
        assert root.tag == "rss"

    def test_feed_has_channel(self, feed_path: Path) -> None:
        tree = ET.parse(feed_path)
        channel = tree.find(".//channel")
        assert channel is not None

    def test_channel_has_required_elements(self, feed_path: Path) -> None:
        tree = ET.parse(feed_path)
        channel = tree.find(".//channel")
        assert channel.find("title") is not None
        assert channel.find("link") is not None
        assert channel.find("description") is not None

    def test_feed_has_items(self, feed_path: Path) -> None:
        tree = ET.parse(feed_path)
        items = tree.findall(".//channel/item")
        assert len(items) >= 34, f"Expected at least 34 items, got {len(items)}"

    def test_feed_has_tp_and_dl_items(self, feed_path: Path) -> None:
        tree = ET.parse(feed_path)
        items = tree.findall(".//channel/item")
        # Should have 34 TPs + 74 DL rules = 108
        assert len(items) == 108, f"Expected 108 items (34 TPs + 74 DL), got {len(items)}"

    def test_item_has_required_elements(self, feed_path: Path) -> None:
        tree = ET.parse(feed_path)
        first_item = tree.find(".//channel/item")
        assert first_item is not None
        assert first_item.find("title") is not None
        assert first_item.find("link") is not None
        assert first_item.find("description") is not None

    def test_item_has_category_tags(self, feed_path: Path) -> None:
        tree = ET.parse(feed_path)
        first_item = tree.find(".//channel/item")
        categories = first_item.findall("category")
        assert len(categories) > 0

    def test_tp_item_links_to_github_pages(self, feed_path: Path) -> None:
        tree = ET.parse(feed_path)
        first_item = tree.find(".//channel/item")
        link = first_item.find("link").text
        assert "elchacal801.github.io/flame-fraud" in link
