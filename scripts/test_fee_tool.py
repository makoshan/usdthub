#!/usr/bin/env python3
"""Contract checks for the USDT fee comparison tool source files."""

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "site/_data/usdt_fee_tool.json"
PAGE_FILE = ROOT / "site/usdt-gas-fee-comparison.html"
ENERGY_PAGE_FILE = ROOT / "site/tron-energy-calculator.html"
SCRIPT_FILE = ROOT / "site/assets/js/usdt-fee-tool.js"
NAV_FILE = ROOT / "site/_includes/nav.html"
INDEX_FILE = ROOT / "site/index.html"

EXPECTED_NETWORKS = {
    "trc20",
    "erc20",
    "bep20",
    "polygon",
    "solana",
    "ton",
}


class FeeToolContractTest(unittest.TestCase):
    def test_data_file_exists_and_has_expected_shape(self):
        self.assertTrue(DATA_FILE.exists(), "missing site/_data/usdt_fee_tool.json")
        payload = json.loads(DATA_FILE.read_text(encoding="utf-8"))

        self.assertIn("lastUpdated", payload)
        self.assertIn("profiles", payload)
        self.assertIn("networks", payload)
        self.assertIn("tronEnergy", payload)
        self.assertEqual(3, len(payload["profiles"]))

        networks = payload["networks"]
        self.assertEqual(6, len(networks))
        self.assertEqual(EXPECTED_NETWORKS, {item["id"] for item in networks})

        for item in networks:
            self.assertIn("feeUsd", item)
            self.assertLessEqual(item["feeUsd"]["low"], item["feeUsd"]["typical"])
            self.assertLessEqual(
                item["feeUsd"]["typical"],
                item["feeUsd"]["high"],
            )
            self.assertTrue(item["gasToken"])
            self.assertTrue(item["speed"])
            self.assertTrue(item["bestFor"])
            self.assertTrue(item["watchFor"])

        tron = payload["tronEnergy"]
        self.assertIn("dailyEnergySupply", tron)
        self.assertIn("modes", tron)
        self.assertIn("transferEnergy", tron)
        self.assertIn("sources", tron)
        self.assertGreater(tron["dailyEnergySupply"], 0)
        self.assertGreater(tron["transferEnergy"]["oldAddress"], 0)
        self.assertGreater(
            tron["transferEnergy"]["newAddress"],
            tron["transferEnergy"]["oldAddress"],
        )
        self.assertIn("current", tron["modes"])
        self.assertIn("safe", tron["modes"])
        self.assertGreater(tron["modes"]["current"]["energyPerTrx"], 0)
        self.assertGreater(tron["modes"]["safe"]["energyPerTrx"], 0)

    def test_fee_page_embeds_data_and_script_hooks(self):
        self.assertTrue(PAGE_FILE.exists(), "missing tool page source")
        html = PAGE_FILE.read_text(encoding="utf-8")

        self.assertIn("data-fee-tool", html)
        self.assertIn('id="usdt-fee-tool-data"', html)
        self.assertIn("/assets/js/usdt-fee-tool.js", html)
        self.assertIn("data-profile-select", html)
        self.assertIn("data-amount-input", html)
        self.assertIn("data-fee-table-body", html)

    def test_tron_energy_page_embeds_data_and_script_hooks(self):
        self.assertTrue(ENERGY_PAGE_FILE.exists(), "missing TRON energy page source")
        html = ENERGY_PAGE_FILE.read_text(encoding="utf-8")

        self.assertIn("data-energy-tool", html)
        self.assertIn('id="usdt-fee-tool-data"', html)
        self.assertIn("/assets/js/usdt-fee-tool.js", html)
        self.assertIn("data-staked-trx", html)
        self.assertIn("data-transfer-count", html)
        self.assertIn("data-address-type", html)
        self.assertIn("data-energy-mode", html)
        self.assertIn("65,000", html)
        self.assertIn("130,000", html)
        self.assertIn("动态能量模型", html)

    def test_browser_script_exists(self):
        self.assertTrue(SCRIPT_FILE.exists(), "missing browser script")
        js = SCRIPT_FILE.read_text(encoding="utf-8")
        self.assertIn("usdt-fee-tool-data", js)
        self.assertIn("data-fee-table-body", js)
        self.assertIn("Intl.NumberFormat", js)
        self.assertIn("data-energy-summary", js)
        self.assertIn("data-energy-table", js)
        self.assertIn("transferEnergy", js)

    def test_site_surfaces_link_to_tool(self):
        nav_html = NAV_FILE.read_text(encoding="utf-8")
        index_html = INDEX_FILE.read_text(encoding="utf-8")
        self.assertIn("/usdt-gas-fee-comparison.html", nav_html)
        self.assertIn("./usdt-gas-fee-comparison.html", index_html)


if __name__ == "__main__":
    unittest.main()
