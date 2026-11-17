"""
Verification tests for generated docs/ site bundle, RSS/XML feeds, and HTML/CSS invariants.
"""

from __future__ import annotations

import json
import sys
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import build_site
import export_catalog


class TestSiteArtifacts(unittest.TestCase):
    def test_bundle_matches_catalog_count_and_has_summary(self):
        catalog = json.loads((REPO_ROOT / "data" / "tools.json").read_text(encoding="utf-8"))
        bundle = json.loads((DOCS_DIR / "catalog-bundle.json").read_text(encoding="utf-8"))
        self.assertEqual(len(bundle["tools"]), len(catalog["tools"]))
        self.assertEqual(bundle["summary"]["total_tools"], len(catalog["tools"]))
        self.assertGreater(bundle["summary"]["total_stars"], 0)

    def test_rss_and_sitemap_are_valid_xml(self):
        rss_root = ET.fromstring((DOCS_DIR / "feed.xml").read_text(encoding="utf-8"))
        self.assertEqual(rss_root.tag, "rss")
        items = rss_root.findall("./channel/item")
        catalog = json.loads((REPO_ROOT / "data" / "tools.json").read_text(encoding="utf-8"))
        self.assertEqual(len(items), len(catalog["tools"]))

        sitemap_root = ET.fromstring((DOCS_DIR / "sitemap.xml").read_text(encoding="utf-8"))
        self.assertTrue(sitemap_root.tag.endswith("urlset"))

    def test_html_and_css_modern_accessibility_invariants(self):
        html = (DOCS_DIR / "index.html").read_text(encoding="utf-8")
        css = (DOCS_DIR / "styles.css").read_text(encoding="utf-8")

        self.assertIn('<meta name="color-scheme" content="light dark">', html)
        self.assertIn('closedby="any"', html)
        self.assertIn('aria-live="polite"', html)
        self.assertIn('class="skip-link"', html)
        self.assertTrue((DOCS_DIR / "styles.css").exists())
        self.assertTrue((DOCS_DIR / "app.js").exists())
        self.assertTrue((DOCS_DIR / "insights.js").exists())
        self.assertTrue((DOCS_DIR / ".nojekyll").exists())

        self.assertIn('meta[name="color-scheme"][content="dark"]', css)
        self.assertIn("overscroll-behavior: contain", css)
        self.assertIn("container-type: inline-size", css)

    def test_build_site_check_mode_passes(self):
        old_argv = sys.argv
        try:
            sys.argv = ["build_site.py", "--check"]
            self.assertEqual(build_site.main(), 0)
        finally:
            sys.argv = old_argv

    def test_exports_check_mode_and_jsonld_integrity(self):
        old_argv = sys.argv
        try:
            sys.argv = ["export_catalog.py", "--check"]
            self.assertEqual(export_catalog.main(), 0)
        finally:
            sys.argv = old_argv

        catalog = json.loads((REPO_ROOT / "data" / "tools.json").read_text(encoding="utf-8"))
        jsonld = json.loads((REPO_ROOT / "data" / "exports" / "catalog.jsonld").read_text(encoding="utf-8"))
        self.assertEqual(jsonld["@type"], "ItemList")
        self.assertEqual(jsonld["numberOfItems"], len(catalog["tools"]))
        self.assertEqual(len(jsonld["itemListElement"]), len(catalog["tools"]))

        csv_lines = (REPO_ROOT / "data" / "exports" / "tools.csv").read_text(encoding="utf-8").strip().splitlines()
        self.assertEqual(len(csv_lines), len(catalog["tools"]) + 1)


if __name__ == "__main__":
    unittest.main()
