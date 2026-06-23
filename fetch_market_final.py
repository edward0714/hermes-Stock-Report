#!/usr/bin/env python3
"""Fetch market data properly, handling Taiwan index specially."""
import json
import urllib.request
import urllib.parse

SYMBOLS = {
    "^GSPC": ("sp500", "S&P 500"),
    "^IXIC": ("nasdaq", "NASDAQ Composite"), 
    "^VIX": ("vix", "VIX 恐慌指數"),
    "^TNX": ("tnx", "美債10Y殖利率"),
    "GC=F": ("gold", "黃金"),
    "CL=F": ("wti", "WTI原油"),
    "BTC-USD": ("btc", "比特幣"),
    "DX-Y.NYB": ("dxy", "美元指數"),
    "^TWII": ("twii", "台股加權指數"),
    "USDTWD=X": ("usdtwd", "美元/台幣"),
}

def fetch_chart(symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(symbol)}?interval=1d&range=10d"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            result = data["chart"]["result"][0]
            meta = result.get("meta", {})
            meta_price = meta.get("regularMarketPrice")
            meta_prev = meta.get("chartPreviousClose")
            
            closes = result.get("indicators", {}).get("quote", [{}])[0].get("close", [])
            
            # Find the last non-null close from chart
            last_chart_close = None
            prev_chart_close = None
            for c in reversed(closes):
                if c is not None:
                    if last_chart_close is None:
                        last_chart_close = c
                    elif prev_chart_close is None:
                        prev_chart_close = c
                        break
            
            # If meta_price is available and differs significantly from last_chart_close,
            # use meta_price (it's more real-time)
            current = meta_price if meta_price else last_chart_close
            prev_close = prev_chart_close if prev_chart_close else meta_prev
            
            # For indices that just closed, meta_price is the closing price
            # and last_chart_close might be from a previous day if today's close isn't in chart yet
            if meta_price and last_chart_close and abs(meta_price - last_chart_close) / max(meta_price, last_chart_close) > 0.01:
                # meta_price differs by >1% from chart close - use meta as current
                current = meta_price
                # Try to find a good previous close
                # If meta_prev is available, use that
                if meta_prev and abs(meta_prev - current) / current < 0.5:
                    prev_close = meta_prev
                elif prev_chart_close:
                    prev_close = prev_chart_close
            
            change_pct = None
            if current and prev_close and prev_close != 0:
                change_pct = round(((current - prev_close) / prev_close) * 100, 2)
            
            return {
                "current": round(current, 2) if current else None,
                "previous": round(prev_close, 2) if prev_close else None,
                "change_pct": change_pct,
                "meta_price": meta_price,
                "meta_prev": meta_prev,
                "last_chart_close": last_chart_close,
            }
    except Exception as e:
        return {"current": None, "previous": None, "change_pct": None, "error": str(e)}

if __name__ == "__main__":
    results = {}
    for sym, (key, name) in SYMBOLS.items():
        r = fetch_chart(sym)
        results[key] = {"name": name, **r}
        c = r.get("current")
        cp = r.get("change_pct")
        p = r.get("previous")
        if c is not None:
            direction = "↑" if cp and cp > 0 else ("↓" if cp and cp < 0 else "→")
            print(f"{name}: {c} (prev: {p}) {direction}{abs(cp) if cp else 0:.2f}%")
        else:
            print(f"{name}: N/A ({r.get('error', 'unknown')})")
    
    print("\n=== JSON ===")
    print(json.dumps(results, indent=2, ensure_ascii=False))