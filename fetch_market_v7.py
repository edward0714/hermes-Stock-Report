#!/usr/bin/env python3
"""Fetch market data from Yahoo Finance using quote endpoint for change data."""
import json
import urllib.request
import urllib.parse

SYMBOLS = {
    "^GSPC": "sp500",
    "^IXIC": "nasdaq", 
    "^VIX": "vix",
    "^TNX": "tnx",
    "GC=F": "gold",
    "CL=F": "wti",
    "BTC-USD": "btc",
    "DX-Y.NYB": "dxy",
    "^TWII": "twii",
    "USDTWD=X": "usdtwd",
}

def fetch_quote_v7(symbol):
    """Fetch from Yahoo Finance quote endpoint for more complete data."""
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={urllib.parse.quote(symbol)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            result = data["quoteResponse"]["result"][0]
            current = result.get("regularMarketPrice")
            previous = result.get("regularMarketPreviousClose")
            change_pct = result.get("regularMarketChangePercent")
            change = result.get("regularMarketChange")
            return {
                "symbol": symbol,
                "name": result.get("shortName", symbol),
                "current": current,
                "previous": previous,
                "change": change,
                "change_pct": round(change_pct, 2) if change_pct else None,
            }
    except Exception as e:
        return {"symbol": symbol, "name": symbol, "current": None, "previous": None, "change": None, "change_pct": None, "error": str(e)}

if __name__ == "__main__":
    results = {}
    for sym, key in SYMBOLS.items():
        results[key] = fetch_quote_v7(sym)
        r = results[key]
        c = r.get("current")
        cp = r.get("change_pct")
        if c is not None:
            direction = "↑" if cp and cp > 0 else ("↓" if cp and cp < 0 else "→")
            print(f"{key}: {c} (prev: {r.get('previous')}) {direction}{abs(cp) if cp else 'N/A'}%")
        else:
            print(f"{key}: N/A ({r.get('error', 'unknown')})")
    
    print("\n=== JSON ===")
    print(json.dumps(results, indent=2))