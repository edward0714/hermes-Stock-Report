#!/usr/bin/env python3
"""Fetch Taiwan stock data from Yahoo Finance."""
import json
import urllib.request
import urllib.parse

STOCKS = {
    "2330.TW": "台積電",
    "2317.TW": "鴻海",
    "2454.TW": "聯發科",
    "2382.TW": "廣達",
    "2603.TW": "長榮",
}

def fetch_stock(symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(symbol)}?interval=1d&range=5d"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            result = data["chart"]["result"][0]
            meta = result.get("meta", {})
            current = meta.get("regularMarketPrice")
            prev_close = meta.get("chartPreviousClose")
            
            closes = result.get("indicators", {}).get("quote", [{}])[0].get("close", [])
            
            # Find last non-null close
            last_c = None
            prev_c = None
            for c in reversed(closes):
                if c is not None:
                    if last_c is None:
                        last_c = c
                    elif prev_c is None:
                        prev_c = c
                        break
            
            # If closes has null at end but meta has price, use meta
            if current and last_c and abs(current - last_c) > 1:
                current = current
            elif current and not last_c:
                current = current
            else:
                current = last_c or current
            
            if prev_c is None:
                prev_c = prev_close
            
            change_pct = None
            if current and prev_c and prev_c != 0:
                change_pct = round(((current - prev_c) / prev_c) * 100, 2)
            
            return {
                "current": round(current, 2) if current else None,
                "previous": round(prev_c, 2) if prev_c else None,
                "change_pct": change_pct,
            }
    except Exception as e:
        return {"current": None, "previous": None, "change_pct": None, "error": str(e)}

if __name__ == "__main__":
    results = {}
    for sym, name in STOCKS.items():
        r = fetch_stock(sym)
        results[sym] = {"name": name, **r}
        c = r.get("current")
        cp = r.get("change_pct")
        p = r.get("previous")
        if c is not None:
            direction = "↑" if cp and cp > 0 else ("↓" if cp and cp < 0 else "→")
            print(f"{name} ({sym}): {c} (prev: {p}) {direction}{abs(cp) if cp else 0:.2f}%")
        else:
            print(f"{name} ({sym}): N/A ({r.get('error', 'unknown')})")
    
    print("\n=== JSON ===")
    print(json.dumps(results, indent=2, ensure_ascii=False))