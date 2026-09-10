import json, urllib.request

def get(sym):
    url=f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?range=5d&interval=1d"
    req=urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            d=json.loads(r.read().decode())
        res=d["chart"]["result"][0]
        meta=res["meta"]
        closes=res["indicators"]["quote"][0]["close"]
        ts=res["timestamp"]
        # last non-null close and previous
        vals=[(t,c) for t,c in zip(ts,closes) if c is not None]
        t2,c2=vals[-2]; t1,c1=vals[-1]
        def fdate(t): return __import__("datetime").datetime.utcfromtimestamp(t).strftime("%Y-%m-%d")
        prev_close=meta.get("chartPreviousClose")
        pct=(c1/c2-1)*100 if c2 else 0
        print(f"{sym:10s} last={c1:.4f} ({fdate(t1)}) prev={c2:.4f} ({fdate(t2)}) chg%={pct:+.2f} 52w={meta.get('fiftyTwoWeekHigh')}")
    except Exception as e:
        print(f"{sym:10s} ERROR {e}")

for s in ["^TWII","^DJI","^GSPC","^IXIC","^SOX","NVDA","^VIX","GC=F","CL=F","BTC-USD","TWD=X","EURUSD=X","^TNX"]:
    get(s)
