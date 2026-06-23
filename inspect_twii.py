#!/usr/bin/env python3
"""Inspect raw TWII data."""
import json
import urllib.request
import urllib.parse

url = "https://query1.finance.yahoo.com/v8/finance/chart/%5ETWII?interval=1d&range=5d"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
with urllib.request.urlopen(req, timeout=10) as resp:
    data = json.loads(resp.read())
    print(json.dumps(data, indent=2)[:3000])