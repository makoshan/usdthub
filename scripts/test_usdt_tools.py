#!/usr/bin/env python3
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'site'
DOCS = ROOT / 'docs'
JS = SITE / 'assets/js/usdt-fee-tool.js'
DATA = SITE / '_data/usdt_fee_tool.json'
issues = []

def check(path, needles):
    text = path.read_text(encoding='utf-8')
    for needle in needles:
        if needle not in text:
            issues.append(f"{path.name}: missing {needle}")
    return text

fee_src = check(SITE / 'usdt-gas-fee-comparison.html', [
    'USDT 不同链转账手续费对比',
    'data-fee-tool',
    'tron-energy-calculator.html',
    "usdt-fee-tool.js",
])
energy_src = check(SITE / 'tron-energy-calculator.html', [
    'TRON 能量计算器：质押多少 TRX，够转几笔 USDT',
    'data-energy-tool',
    'data-staked-trx',
    'data-transfer-count',
    'data-address-type',
    'data-energy-mode',
    "usdt-fee-tool.js",
])
fee_built = check(DOCS / 'usdt-gas-fee-comparison.html', [
    'USDT 不同链转账手续费对比',
    'data-fee-tool',
    'TRON 要单独看',
])
energy_built = check(DOCS / 'tron-energy-calculator.html', [
    'TRON 能量计算器：质押多少 TRX，够转几笔 USDT',
    'data-energy-tool',
    'data-energy-table',
])
check(JS, ['renderFeeTool()', 'renderEnergyTool()', 'data-energy-tool'])
check(DATA, ['"tronEnergy"', '"energyPerTrx"', '"payNums"'])

if 'data-energy-tool' in fee_src:
    issues.append('fee page should not embed data-energy-tool after split')
if 'data-fee-tool' in energy_src:
    issues.append('energy page should not embed data-fee-tool after split')

# Formula sanity based on current snapshot data file values.
import json
payload = json.loads(DATA.read_text(encoding='utf-8'))
energy_per_trx = payload['tronEnergy']['networkSnapshot']['energyPerTrx']
old_per_tx = payload['tronEnergy']['transferEnergy']['oldAddress']
new_per_tx = payload['tronEnergy']['transferEnergy']['newAddress']
if int(10000 * energy_per_trx) <= 0:
    issues.append('network snapshot ratio must produce positive daily energy')
if old_per_tx >= new_per_tx:
    issues.append('new-address transfer energy should be higher than old-address energy')

if issues:
    print('FAIL')
    for item in issues:
        print('-', item)
    sys.exit(1)

print('OK: fee comparison page + TRON energy calculator page + shared data/js regression checks passed')
