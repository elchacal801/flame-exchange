"""Tests for FLAME TAXII static endpoint generator."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from export_taxii import build_discovery, build_collections, build_manifest


class TestBuildDiscovery:
    def test_discovery_structure(self):
        disc = build_discovery()
        assert disc["title"] == "FLAME TAXII Server"
        assert "default" in disc["default"]
        assert "api_roots" in disc

class TestBuildCollections:
    def test_collections_count(self):
        result = build_collections()
        assert "collections" in result
        assert len(result["collections"]) == 3

    def test_collection_ids_deterministic(self):
        c1 = build_collections()
        c2 = build_collections()
        for i in range(3):
            assert c1["collections"][i]["id"] == c2["collections"][i]["id"]

class TestBuildManifest:
    def test_manifest_structure(self):
        objects = [
            {"type": "x-flame-fraud-scheme", "id": "x-flame-fraud-scheme--abc",
             "modified": "2026-01-01T00:00:00Z", "spec_version": "2.1"}
        ]
        manifest = build_manifest(objects)
        assert "objects" in manifest
        assert len(manifest["objects"]) == 1
        assert manifest["objects"][0]["id"] == "x-flame-fraud-scheme--abc"
