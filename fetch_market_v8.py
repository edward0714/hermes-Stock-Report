#!/usr/bin/env python3
"""Fetch market data from Yahoo Finance v8 chart endpoint with full data extraction."""
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

def fetch_chart(symbol):
    """Fetch from Yahoo Finance v8 chart endpoint."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(symbol)}?interval=1d&range=5d"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            result = data["chart"]["result"][0]
            meta = result.get("meta", {})
            current = meta.get("regularMarketPrice")
            previous = meta.get("previousClose")
            chart_data = result.get("indicators", {}).get("quote", [{}])[0]
            
            # Get close prices from chart data
            closes = chart_data.get("close", [])
            opens = chart_data.get("open", [])
            
            change_pct = None
            if current and previous and previous != 0:
                change_pct = round(((current - previous) / previous) * 100, 2)
            
            return {
                "symbol": symbol,
                "name": meta.get("shortName", symbol),
                "current": current,
                "previous": previous,
                "change_pct": change_pct,
                "closes": closes,
                "opens": opens,
            }
    except Exception as e:
        return {"symbol": symbol, "name": symbol, "current": None, "previous": None, "change_pct": None, "error": str(e)}

if __name__ == "__main__":
    results = {}
    for sym, key in SYMBOLS.items():
        results[key] = fetch_chart(sym)
        r = results[key]
        c = r.get("current")
        cp = r.get("change_pct")
        p = r.get("previous")
        if c is not None:
            direction = "↑" if cp and cp > 0 else ("↓" if cp and cp < 0 else "→")
            print(f"{key}: {c} (prev: {p}) {direction}{abs(cp) if cp else 'N/A'}%")
        else:
            print(f"{key}: N/A ({r.get('error', 'unknown')})")
    
    print("\n=== FULL JSON ===")
    print(json.dumps(results, indent=2))