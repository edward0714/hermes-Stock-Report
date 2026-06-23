#!/usr/bin/env python3
"""Fetch market data and compute change from closes array."""
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
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(symbol)}?interval=1d&range=5d"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            result = data["chart"]["result"][0]
            meta = result.get("meta", {})
            current = meta.get("regularMarketPrice")
            closes = result.get("indicators", {}).get("quote", [{}])[0].get("close", [])
            
            # Find last non-null close
            last_close = None
            prev_close = None
            for c in reversed(closes):
                if c is not None:
                    if last_close is None:
                        last_close = c
                    elif prev_close is None:
                        prev_close = c
                        break
            
            if last_close is not None:
                f_current = last_close
                f_previous = prev_close if prev_close else current
            else:
                f_current = current
                f_previous = prev_close
            
            change_pct = None
            if f_current and f_previous and f_previous != 0:
                change_pct = round(((f_current - f_previous) / f_previous) * 100, 2)
            
            return {
                "symbol": symbol,
                "name": meta.get("shortName", symbol),
                "current": f_current,
                "previous": f_previous,
                "change_pct": change_pct,
            }
    except Exception as e:
        return {"symbol": symbol, "name": symbol, "current": None, "previous": None, "change_pct": None, "error": str(e)}

if __name__ == "__main__":
    results = {}
    for sym, key in SYMBOLS.items():
        r = fetch_chart(sym)
        results[key] = r
        c = r.get("current")
        cp = r.get("change_pct")
        p = r.get("previous")
        if c is not None:
            direction = "↑" if cp and cp > 0 else ("↓" if cp and cp < 0 else "→")
            print(f"{key}: {c:.2f} (prev: {p:.2f}) {direction}{abs(cp) if cp else 0:.2f}%")
        else:
            print(f"{key}: N/A ({r.get('error', 'unknown')})")
    
    print("\n=== JSON ===")
    print(json.dumps(results, indent=2))