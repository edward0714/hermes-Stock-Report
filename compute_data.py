#!/usr/bin/env python3
"""Accurate TWII data calculation."""
import json
import urllib.request
import urllib.parse

# TWII data from the raw inspection - use the closes array properly
# Chart data timestamps (9 AM Taipei each day):
# Day 1 - Thu Jun 18: open=44447.87, close=45396.99
# Day 2 - Fri Jun 19: open=45500.08, close=45809.19
# Day 3 - Sat Jun 20: (no real trading) close=45877.39
# Day 4 - Sun Jun 21: (no real trading) close=46465.20
# Day 5 - Mon Jun 22: open=46679.57, meta.close=47741.51

# For TWII, the most recent completed session is Monday June 22
# Friday June 19 close = 45809.19
# Monday June 22 close (meta) = 47741.51
twii_prev = 45809.19
twii_close = 47741.51
twii_change = round(((twii_close - twii_prev) / twii_prev) * 100, 2)
print(f"TWII: Current={twii_close}, Prev={twii_prev}, Change={twii_change}%")

# Also print all the data I have in one clean table
print()
print("=" * 80)
print(f"{'Indicator':<25} {'Current':<15} {'Previous':<15} {'Change':<10}")
print("=" * 80)

data = {
    "S&P 500": (7478.09, 7500.58, -0.30),
    "Nasdaq": (26211.61, 26517.93, -1.16),
    "VIX": (17.37, 16.40, 5.91),
    "US 10Y Yield": (4.51, 4.45, 1.35),
    "DXY": (101.03, 100.85, 0.18),
    "Gold": (4199.70, 4224.10, -0.58),
    "WTI Crude": (73.75, 76.60, -3.72),
    "Bitcoin": (64697.63, 63237.54, 2.31),
    "USD/TWD": (31.63, 31.64, -0.02),
    "TWII": (47741.51, 45809.19, twii_change),
}

for name, (cur, prev, chg) in data.items():
    direction = "↑" if chg > 0 else ("↓" if chg < 0 else "→")
    print(f"{name:<25} {cur:<15.2f} {prev:<15.2f} {direction}{abs(chg):<8.2f}%")

print("=" * 80)

print("\n\n=== Taiwan Stocks ===")
tw_stocks = {
    "TSMC": (2510.0, 2385.0, 5.24),
    "Hon Hai": (268.5, 272.0, -1.29),
    "MediaTek": (4465.0, 4460.0, 0.11),
    "Quanta": (380.0, 374.0, 1.60),
    "Evergreen": (193.0, 194.0, -0.52),
}
for name, (cur, prev, chg) in tw_stocks.items():
    direction = "↑" if chg > 0 else ("↓" if chg < 0 else "→")
    print(f"{name:<15} {cur:<12.2f} {prev:<12.2f} {direction}{abs(chg):<6.2f}%")