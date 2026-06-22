# Shioaji 帳戶高級功能完整指南

## 📊 你的帳戶信息

| 項目 | 數據 |
|------|------|
| **用戶名** | 胡鈞偉 |
| **身份證** | F124955384 |
| **券商** | 9A9U (永豐金) |
| **股票帳戶** | 0351304 (已簽署 ✅) |
| **期貨帳戶** | 00072125 (未簽署 ❌) |

---

## 🎯 10 大帳戶功能詳解

### 1️⃣ **帳戶餘額查詢** (Account Balance)

**功能**：查詢帳戶現金餘額

**CLI 命令**：
```bash
shioaji portfolio balance
```

**Python 方法**：
```python
balance = api.account_balance(account=api.stock_account)
print(f"現金餘額：{balance.acc_balance:,.0f} 元")
```

**HTTP API**：
```bash
curl -X POST http://localhost:8080/api/v1/portfolio/account_balance
```

**返回信息**：
- `acc_balance`：現金餘額（元）
- `date`：查詢時間

---

### 2️⃣ **部位查詢** (List Positions)

**功能**：查詢持有的股票部位（整股和零股）

**查詢整股**：
```bash
# CLI
shioaji portfolio positions

# Python
positions = api.list_positions(account=api.stock_account)
```

**查詢零股**：
```bash
# CLI
shioaji portfolio positions --unit share

# Python
from shioaji import Unit
positions = api.list_positions(account=api.stock_account, unit=Unit.Share)
```

**返回信息（針對每個部位）**：

| 字段 | 說明 |
|------|------|
| `code` | 股票代碼 |
| `direction` | Buy(買) / Sell(賣) |
| `quantity` | 持股數量（張） |
| `price` | 平均成本價 |
| `last_price` | 目前市場價格 |
| `pnl` | 損益金額（元） |
| `cond` | 條件（Current/融資/融券等） |
| `yd_quantity` | 昨日庫存 |

**範例**：
```
代碼: 2890
買賣: Buy
張數: 1
成本: 37.0 元
現價: 39.8 元
損益: +2,800 元
```

---

### 3️⃣ **融資融券查詢** (Account Margin)

**功能**：查詢融資融券信息和保證金

**Python 方法**：
```python
# 查詢新台幣保證金
margin = api.get_account_margin(currency='NTD')

# 查詢美金保證金
margin = api.get_account_margin(currency='USD')
```

**支援幣別**：
- NTD / TWD：新台幣
- USD：美元
- HKD：港幣
- EUR：歐元
- JPY：日幣
- GBP：英鎊
- CAD：加幣

**返回信息**：
- `Bapamt`：融資金額（借款金額）
- `Sapamt`：融券金額（借券金額）
- `Adps`：維持率（%）
- `Adamt`：可用保證金
- `Ybaln`：昨日結算餘額

---

### 4️⃣ **開倉部位查詢** (Open Position)

**功能**：查詢目前持有的長期部位（融資融券使用）

**Python 方法**：
```python
openpos = api.get_account_openposition()
```

**用途**：
- 檢查融資融券的持股狀況
- 計算帳戶維持率
- 監控融資融券成本

---

### 5️⃣ **委託單查詢** (List Orders)

**功能**：查詢所有委託單紀錄

**CLI 命令**：
```bash
shioaji order list
```

**Python 方法**：
```python
orders = api.list_orders()
```

**返回信息（針對每筆委託）**：
- 委託編號 (ID)
- 股票代碼
- 買賣別
- 數量
- 價格
- 委託狀態（未成交/已報價/部分成交/全部成交/已取消）
- 委託時間

**委託狀態說明**：
| 狀態 | 說明 |
|------|------|
| PendingSubmit | 待報價 |
| PendingCancel | 待取消 |
| Filled | 全部成交 |
| PartFilled | 部分成交 |
| Cancelled | 已取消 |

---

### 6️⃣ **成交查詢** (List Trades)

**功能**：查詢已成交的訂單詳情

**Python 方法**：
```python
trades = api.list_trades(account=api.stock_account)

for trade in trades:
    print(f"代碼：{trade.contract.code}")
    print(f"成交數量：{trade.status.order_quantity}")
    print(f"成交價格：{trade.order.price}")
```

**返回信息**：
- 合約信息（代碼、交易所等）
- 委託單信息（數量、價格、條件）
- 成交時間和成交量

---

### 7️⃣ **損益查詢** (Profit & Loss)

**功能**：查詢已平倉的損益情況

**CLI 命令**：
```bash
shioaji portfolio profit-loss
```

**Python 方法**：
```python
from shioaji import ProfitLossType

# 查詢實時損益
pl = api.list_profit_loss(type=ProfitLossType.Realtime)

for item in pl:
    print(f"代碼：{item.code}")
    print(f"買價：{item.buy_price}")
    print(f"賣價：{item.sell_price}")
    print(f"損益：{item.profit} 元")
    print(f"損益率：{item.profit_rate}%")
```

**返回信息（針對每筆成交）**：
- 股票代碼
- 買進數量
- 買價
- 賣價
- 損益金額（元）
- 損益率（%）
- 成交時間

---

### 8️⃣ **交割查詢** (Settlements)

**功能**：查詢股票買賣後的資金結算紀錄

**CLI 命令**：
```bash
shioaji portfolio settlements
```

**Python 方法**：
```python
settlements = api.list_settlements(account=api.stock_account)

for settlement in settlements:
    print(f"日期：{settlement.date}")
    print(f"金額：{settlement.amount} 元")
    print(f"T字：{settlement.tcode}")
```

**返回信息**：
- 交割日期
- 交割金額（應收或應付）
- 交割代碼 (T+0/T+1/T+2)
- 交割狀態

---

### 9️⃣ **行情推播訂閱** (Quote Subscription)

**功能**：即時接收股票行情推播

**Python 方法**：
```python
def handle_quote_event(topic: str, data: dict):
    """行情推播回調"""
    print(f"{topic}: {data}")

# 訂閱行情
api.on_quote(handle_quote_event)
api.subscribe_quote(contracts, quote_type='SimpleQuote')

# 簡單行情包含：開盤、最高、最低、收盤、成交量、成交值等
```

**接收的行情字段**：
- `open`：開盤價
- `high`：最高價
- `low`：最低價
- `close`：收盤價
- `volume`：成交量（股）
- `amount`：成交值（元）
- `bid`：買價
- `ask`：賣價
- `timestamp`：時間

---

### 🔟 **委託回報訂閱** (Order Event Subscription)

**功能**：即時接收委託單的狀態變化

**Python 方法**：
```python
def handle_order_event(state: str, data: dict):
    """委託回報回調"""
    print(f"狀態：{state}")
    print(f"數據：{data}")

# 訂閱委託回報
api.on_report(handle_order_event)
```

**接收的狀態**：
- `StockOrder`：股票委託狀態變化
- `FuturesOrder`：期貨委託狀態變化
- `OptionsOrder`：選擇權委託狀態變化

**事件信息**：
- 委託編號
- 委託狀態
- 成交數量
- 成交價格
- 成交時間
- 錯誤訊息（如有）

---

## 📋 完整 CLI 命令參考

### 帳戶查詢命令

```bash
# 查詢帳戶餘額
shioaji portfolio balance

# 查詢部位
shioaji portfolio positions
shioaji portfolio positions --unit share      # 零股

# 查詢融資融券（期貨帳戶）
shioaji portfolio margin

# 查詢損益
shioaji portfolio profit-loss
shioaji portfolio profit-loss-detail

# 查詢交割
shioaji portfolio settlements

# 查詢交易限額
shioaji portfolio trading-limits
```

### 委託單命令

```bash
# 列出委託單
shioaji order list

# 查詢單一委託
shioaji order status <ORDER_ID>

# 取消委託
shioaji order cancel <ORDER_ID>

# 修改委託
shioaji order update <ORDER_ID> --price <NEW_PRICE>
```

### 行情查詢命令

```bash
# 查詢合約
shioaji data quote <CODE>

# 掃描器查詢
shioaji data scanner --scanner-type change-percent-rank
```

---

## 💡 高級功能示例

### 示例 1：完整帳戶狀況查詢

```python
import shioaji as sj

api = sj.Shioaji(simulation=True)
api.login(api_key="YOUR_KEY", secret_key="YOUR_SECRET")

# 查詢所有信息
balance = api.account_balance(account=api.stock_account)
positions = api.list_positions(account=api.stock_account)

print(f"現金餘額：${balance.acc_balance:,.0f}")
print(f"持股部位：")
for pos in positions:
    print(f"  {pos.code}: {pos.quantity}張 @ {pos.price:.2f}元 (現價{pos.last_price:.2f}元，損益{pos.pnl:,.0f}元)")
```

### 示例 2：監控特定股票損益

```python
positions = api.list_positions(account=api.stock_account)

for pos in positions:
    if pos.code == '2330':  # 台積電
        unrealized_loss = pos.pnl
        unrealized_rate = (pos.last_price - pos.price) / pos.price * 100
        print(f"台積電持倉：{pos.quantity}張")
        print(f"未實現損益：${unrealized_loss:,.0f} ({unrealized_rate:+.2f}%)")
```

### 示例 3：設置自動更新

```python
import time

while True:
    # 每 10 秒更新一次帳戶信息
    balance = api.account_balance(account=api.stock_account)
    print(f"[{time.strftime('%H:%M:%S')}] 現金餘額：${balance.acc_balance:,.0f}")
    time.sleep(10)
```

---

## 🔗 相關資源

- **官方文檔**：https://sinotrade.github.io/
- **GitHub**：https://github.com/sinotrade/shioaji
- **期貨帳戶簽署**：https://www.sinotrade.com.tw/newweb/signCenter/signCenterIndex/

---

## 📌 重要提醒

- ✅ 股票帳戶已簽署，可進行正式交易
- ❌ 期貨帳戶未簽署，需完成簽署才能交易
- 💰 所有金額查詢都基於模擬環境（當前測試）
- 🔒 永遠不要洩露 API Key 和 Secret Key
- 📊 建議定期查詢帳戶狀況，監控風險

---

**最後更新**：2026-06-22
**版本**：2.0（完整帳戶功能指南）
