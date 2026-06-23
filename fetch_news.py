#!/usr/bin/env python3
"""Search for financial news from various public sources."""
import json
import urllib.request
import urllib.parse

def fetch_text(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        return f"ERROR: {e}"

# Try Google News RSS
urls = [
    ("Google Finance US Markets", "https://www.gstatic.com/finance/markets/market_data.json"),
    ("Google Finance News", "https://www.google.com/finance/markets/news?hl=en"),
]

for name, url in urls:
    print(f"\n=== {name} ===")
    content = fetch_text(url)
    print(content[:2000])
    print("...")