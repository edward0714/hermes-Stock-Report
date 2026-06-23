#!/usr/bin/env python3
"""Fetch market data from Yahoo Finance API and print as structured JSON."""
import json
import urllib.request
import urllib.parse
import sys

SYMBOLS = {
    "sp500": "^GSPC",
    "nasdaq": "^IXIC",
    "vix": "^VIX",
    "tnx": "^TNX",
    "gold": "GC=F",
    "wti": "CL=F",
    "btc": "BTC-USD",
    "dxy": "DX-Y.NYB",
    "tw_semiconductor": "^TWSEMI",
}

def fetch_quote(symbol):
    """Fetch current quote data from Yahoo Finance v8 API."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(symbol)}?interval=1d&range=5d"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            result = data["chart"]["result"][0]
            meta = result.get("meta", {})
            current = meta.get("regularMarketPrice")
            previous = meta.get("previousClose")
            change_pct = None
            if current and previous:
                change_pct = round(((current - previous) / previous) * 100, 2)
            return {
                "symbol": symbol,
                "name": meta.get("shortName", symbol),
                "current": current,
                "previous": previous,
                "change_pct": change_pct,
            }
    except Exception as e:
        return {"symbol": symbol, "name": symbol, "current": None, "previous": None, "change_pct": None, "error": str(e)}

if __name__ == "__main__":
    results = {}
    for key, sym in SYMBOLS.items():
        results[key] = fetch_quote(sym)
        print(f"{key}: {json.dumps(results[key])}", flush=True)
    # Also try Taiwan Weighted Index (^TWII)
    results["twii"] = fetch_quote("^TWII")
    print(f"twii: {json.dumps(results['twii'])}", flush=True)
    
    # USD/TWD
    results["usdtwd"] = fetch_quote("USDTWD=X")
    print(f"usdtwd: {json.dumps(results['usdtwd'])}", flush=True)
    
    print("\n=== SUMMARY ===", flush=True)
    for k, v in results.items():
        c = v.get("current")
        cp = v.get("change_pct")
        if c is not None:
            direction = "↑" if cp and cp > 0 else ("↓" if cp and cp < 0 else "→")
            print(f"{k}: {c} ({direction}{abs(cp) if cp else 'N/A'}%)", flush=True)
        else:
            print(f"{k}: N/A (error: {v.get('error', 'unknown')})", flush=True)