#!/usr/bin/env python3
"""Refresh the TRON energy snapshot inside site/_data/usdt_fee_tool.json."""

from __future__ import annotations

import json
import urllib.request
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "site/_data/usdt_fee_tool.json"
TRONGRID_URL = "https://api.trongrid.io/wallet/getaccountresource"
SAMPLE_ADDRESS = "T9yD14Nj9j7xAB4dbGeiX9h8unkKHxuWwb"
SAFE_MARGIN = 0.9


def fetch_snapshot() -> dict:
    payload = json.dumps({"address": SAMPLE_ADDRESS, "visible": True}).encode("utf-8")
    request = urllib.request.Request(
        TRONGRID_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        body = json.load(response)

    total_energy_limit = body["TotalEnergyLimit"]
    total_energy_weight = body["TotalEnergyWeight"]
    energy_per_trx = round(total_energy_limit / total_energy_weight, 3)
    safe_energy_per_trx = round(energy_per_trx * SAFE_MARGIN, 3)

    return {
        "capturedAt": str(date.today()),
        "source": TRONGRID_URL,
        "sampleAddress": SAMPLE_ADDRESS,
        "totalEnergyLimit": total_energy_limit,
        "totalEnergyWeight": total_energy_weight,
        "energyPerTrx": energy_per_trx,
        "safeEnergyPerTrx": safe_energy_per_trx,
    }


def main() -> int:
    payload = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    snapshot = fetch_snapshot()

    tron = payload["tronEnergy"]
    tron["lastUpdated"] = snapshot["capturedAt"]
    tron["networkSnapshot"].update(
        {
            "capturedAt": snapshot["capturedAt"],
            "source": snapshot["source"],
            "sampleAddress": snapshot["sampleAddress"],
            "totalEnergyLimit": snapshot["totalEnergyLimit"],
            "totalEnergyWeight": snapshot["totalEnergyWeight"],
            "energyPerTrx": snapshot["energyPerTrx"],
        }
    )
    tron["modes"]["current"]["energyPerTrx"] = snapshot["energyPerTrx"]
    tron["modes"]["safe"]["energyPerTrx"] = snapshot["safeEnergyPerTrx"]
    payload["lastUpdated"] = snapshot["capturedAt"]

    DATA_FILE.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        "Updated TRON energy snapshot:",
        f"energyPerTrx={snapshot['energyPerTrx']}",
        f"safeEnergyPerTrx={snapshot['safeEnergyPerTrx']}",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
