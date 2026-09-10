import json, urllib.request, datetime
def n(sym, n=8):
    url=f"https://query1.finance.yahoo.com/v1/finance/search?q={sym}&newsCount={n}"
    req=urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            d=json.loads(r.read().decode())
        print(f"\n===== {sym} =====")
        for it in d.get("news",[]):
            t=it.get("providerPublishTime"); tstr=datetime.datetime.fromtimestamp(t,datetime.UTC).strftime("%m-%d %H:%M") if t else "?"
            print(f"[{tstr}] ({it.get('publisher','?')}) {it.get('title','')}")
    except Exception as e:
        print(sym,"ERR",e)
for s in ["NVDA","gold price","stock market","Federal Reserve","oil price"]:
    n(s)
