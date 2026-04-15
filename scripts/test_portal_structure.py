#!/usr/bin/env python3
"""Portal IA contract checks for the USDT HUB redesign."""

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HUB_FILE = ROOT / "site/_data/hub_sections.yml"
NAV_FILE = ROOT / "site/_includes/nav.html"
INDEX_FILE = ROOT / "site/index.html"
README_FILE = ROOT / "README.md"


class PortalStructureTest(unittest.TestCase):
    def test_hub_sections_data_exists(self):
        self.assertTrue(HUB_FILE.exists(), "missing hub section registry")
        text = HUB_FILE.read_text(encoding="utf-8")
        for item in (
            'id: "get"',
            'id: "earn"',
            'id: "spend"',
            'id: "tools"',
            'id: "blog"',
        ):
            self.assertIn(item, text)

    def test_nav_uses_portal_sections_only(self):
        nav = NAV_FILE.read_text(encoding="utf-8")
        self.assertIn("hub.sections", nav)
        self.assertIn("section.permalink", nav)
        self.assertIn("section.label", nav)
        self.assertNotIn("site-utility-nav", nav)
        self.assertNotIn("怎么买 USDT", nav)
        self.assertNotIn("TRON 能量", nav)

    def test_homepage_contains_portal_sections(self):
        html = INDEX_FILE.read_text(encoding="utf-8")
        self.assertIn("USDT HUB", html)
        self.assertIn("Featured paths", html)
        self.assertIn("Featured tools", html)
        self.assertIn("Latest from Blog", html)
        self.assertNotIn("1. 章节", html)
        for label in (
            "About",
            "Editorial Policy",
            "Methodology",
            "Official Sources",
            "Changelog",
            "Trust block",
        ):
            self.assertNotIn(label, html)

    def test_portal_landing_pages_exist(self):
        for name in ("get", "earn", "spend", "tools", "blog"):
            path = ROOT / "site" / f"{name}.html"
            self.assertTrue(path.exists(), f"missing landing page: {name}.html")

    def test_get_and_spend_pages_surface_existing_articles(self):
        hub_text = HUB_FILE.read_text(encoding="utf-8")
        get_html = (ROOT / "site/get.html").read_text(encoding="utf-8")
        spend_html = (ROOT / "site/spend.html").read_text(encoding="utf-8")
        self.assertIn("section_id: get", get_html)
        self.assertIn("section_id: spend", spend_html)
        self.assertIn("/how-to-buy-usdt.html", hub_text)
        self.assertIn("/how-to-choose-a-wallet.html", hub_text)
        self.assertIn("/use-usdt-for-travel.html", hub_text)
        self.assertIn("/buy-apple-gift-card-with-usdt.html", hub_text)

    def test_readme_mentions_usdt_hub_portal(self):
        readme = README_FILE.read_text(encoding="utf-8")
        self.assertIn("USDT HUB", readme)
        self.assertIn("Get / Earn / Spend / Tools / Blog", readme)


if __name__ == "__main__":
    unittest.main()
