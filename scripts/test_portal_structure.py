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
        ):
            self.assertIn(item, text)
        self.assertNotIn('id: "transfer"', text)

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
        hub_text = HUB_FILE.read_text(encoding="utf-8")
        self.assertIn("USDT 新手手册", html)
        self.assertIn("一个持续更新的公开笔记", html)
        self.assertIn("1. 章节", html)
        self.assertIn("2. 常用外部 App 与工具", html)
        self.assertIn("3. 官方资料入口", html)
        self.assertIn("4. 最近更新", html)
        self.assertIn("Get", html)
        self.assertIn("Earn", html)
        self.assertIn("Spend", html)
        self.assertIn("Tools", html)
        self.assertIn("USDT 是什么？", html)
        self.assertIn("这一区还在整理", html)
        self.assertIn("USDT 不同链转账手续费对比", html)
        self.assertNotIn("Blog", html)
        self.assertNotIn("Transfer", html)
        self.assertNotIn("Latest updates", html)
        self.assertNotIn("Featured paths", html)

    def test_portal_landing_pages_exist(self):
        for name in ("get", "earn", "spend", "tools"):
            path = ROOT / "site" / f"{name}.html"
            self.assertTrue(path.exists(), f"missing landing page: {name}.html")
        self.assertFalse((ROOT / "site" / "transfer.html").exists())

    def test_section_pages_surface_existing_articles(self):
        hub_text = HUB_FILE.read_text(encoding="utf-8")
        get_html = (ROOT / "site/get.html").read_text(encoding="utf-8")
        spend_html = (ROOT / "site/spend.html").read_text(encoding="utf-8")
        earn_html = (ROOT / "site/earn.html").read_text(encoding="utf-8")
        tools_html = (ROOT / "site/tools.html").read_text(encoding="utf-8")
        self.assertIn("section_id: get", get_html)
        self.assertIn("section_id: earn", earn_html)
        self.assertIn("section_id: spend", spend_html)
        self.assertIn("section_id: tools", tools_html)
        self.assertIn("/what-is-usdt.html", hub_text)
        self.assertIn("/how-to-buy-usdt.html", hub_text)
        self.assertIn("/how-to-send-usdt.html", hub_text)
        self.assertIn("/binance-receive-view-transfer-usdt.html", hub_text)
        self.assertIn("/how-to-get-tron-energy.html", hub_text)
        self.assertIn("/use-usdt-for-travel.html", hub_text)
        self.assertIn("/buy-apple-gift-card-with-usdt.html", hub_text)
        self.assertIn("/usdt-vs-usdc.html", hub_text)

    def test_readme_mentions_usdt_hub_portal(self):
        readme = README_FILE.read_text(encoding="utf-8")
        self.assertIn("USDT HUB", readme)
        self.assertIn("Get / Earn / Spend / Tools", readme)


if __name__ == "__main__":
    unittest.main()
