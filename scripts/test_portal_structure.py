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
            'id: "transfer"',
            'id: "earn"',
            'id: "spend"',
            'id: "tools"',
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
        hub_text = HUB_FILE.read_text(encoding="utf-8")
        self.assertIn("个人经验分享", html)
        self.assertIn("写给第一次碰 USDT、TRON、钱包的人。", html)
        self.assertIn("这里主要记我自己一路用下来留下来的经验。怎么买 USDT，怎么存 USDT，怎么转 USDT；以及拿到 USDT 以后，它到底还能怎么用", html)
        self.assertIn("1. 章节", html)
        self.assertIn("2. 最近更新", html)
        self.assertIn("Get", html)
        self.assertIn("Transfer", html)
        self.assertIn("Earn", html)
        self.assertIn("Spend", html)
        self.assertIn("Tools", html)
        self.assertIn("USDT 是什么？", html)
        self.assertIn("还在写，先看", html)
        self.assertIn("USDT 不同链转账手续费对比", html)
        self.assertNotIn("Blog", html)
        self.assertNotIn("常用外部 App 与工具", html)
        self.assertNotIn("官方资料入口", html)
        self.assertNotIn("Latest updates", html)
        self.assertNotIn("Featured paths", html)
        self.assertNotIn("TRON / TRC20", html)
        self.assertNotIn("<h1>USDT Hub</h1>", html)
        self.assertNotIn("写给第一次碰 USDT、TRON、钱包和链上转账的人。", html)

    def test_portal_landing_pages_exist(self):
        for name in ("get", "transfer", "earn", "spend", "tools"):
            path = ROOT / "site" / f"{name}.html"
            self.assertTrue(path.exists(), f"missing landing page: {name}.html")

    def test_section_pages_surface_existing_articles(self):
        hub_text = HUB_FILE.read_text(encoding="utf-8")
        get_html = (ROOT / "site/get.html").read_text(encoding="utf-8")
        transfer_html = (ROOT / "site/transfer.html").read_text(encoding="utf-8")
        spend_html = (ROOT / "site/spend.html").read_text(encoding="utf-8")
        earn_html = (ROOT / "site/earn.html").read_text(encoding="utf-8")
        tools_html = (ROOT / "site/tools.html").read_text(encoding="utf-8")
        self.assertIn("section_id: get", get_html)
        self.assertIn("section_id: transfer", transfer_html)
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
        self.assertIn("Get / Transfer / Earn / Spend / Tools", readme)


if __name__ == "__main__":
    unittest.main()
