# Shioaji 新手完整設定指南 - 7 步驟到正式交易

## 📋 目錄
1. [開立永豐金帳戶](#1-開立永豐金帳戶)
2. [簽署 API 服務條款](#2簽署-api-下單服務條款)
3. [申請 API Key 和 Secret Key](#3申請-api-key-和-secret-key)
4. [模擬模式測試](#4-完成模擬模式測試)
5. [驗證簽署狀態](#5-確認測試是否通過-signedsignedtrue)
6. [申請並啟用憑證](#6-申請並啟用憑證)
7. [切換到正式環境](#7-切換到正式環境)

---

## 📌 重點提醒

- ✅ **法規要求**：受限於台灣金融法規，新用戶必須完成以下所有步驟才能進行正式環境交易
- ✅ **測試優先**：必須在模擬模式完成測試並通過審核，才能進入正式環境
- ✅ **安全第一**：永遠不要在前端或版本控制中洩露 API Key、Secret Key 或憑證
- ✅ **時間需求**：整個流程通常需要 3-5 個工作天

---

## 1️⃣ 開立永豐金帳戶

### 步驟 1.1：訪問開戶頁面

👉 **開戶連結**
```
https://www.sinotrade.com.tw/openact?strProd=0254&strWeb=0683&s=013211&utm_source=shioaji
```

### 步驟 1.2：選擇帳戶類型

在開戶頁面上，選擇：
- ✅ **DAWHO+大戶投** （同時開設銀行戶和證券戶）

### 步驟 1.3：完成開銀行帳戶

如果你還沒有永豐銀行帳戶：
- 需要先開銀行帳戶作為「交割戶」（股票買賣的資金帳戶）
- 完整填寫個人資訊並驗證身份

### 步驟 1.4：完成開證券帳戶

- 填寫證券開戶表單
- 簽署相關文件
- 完成身份驗證

### ✓ 步驟 1 完成檢查清單

- [ ] 永豐銀行帳戶已開立
- [ ] 永豐證券帳戶已開立
- [ ] 收到帳戶開立確認函
- [ ] 取得：
  - 銀行帳戶號碼
  - 證券帳戶號碼（格式：BROKER_ID-ACCOUNT_ID）
  - Broker ID（通常是永豐的代碼）

---

## 2️⃣ 簽署 API 下單服務條款

### 步驟 2.1：訪問簽署中心

👉 **簽署中心連結**
```
https://www.sinotrade.com.tw/newweb/signCenter/signCenterIndex/
```

### 步驟 2.2：簽署所需文件

**重點：必須分別簽署**

| 帳戶類型 | 需要簽署 | 用途 |
|---------|--------|------|
| **證券帳戶** | ✅ 必須 | 股票下單 |
| **期貨帳戶** | ✅ 必須 | 期貨/選擇權下單 |

### 步驟 2.3：簽署流程

1. 登入簽署中心
2. 找到「API 下單服務」相關文件
3. 仔細閱讀所有條款
4. 確認同意所有條件
5. 完成電子簽署

### 📌 重要提醒

- ⚠️ **仔細閱讀**：簽署前必須完全理解所有條款
- ⚠️ **時間間隔**：簽署時間必須早於 API 測試時間，以利審核通過
- ⚠️ **分別簽署**：證券和期貨需要各別簽署

### ✓ 步驟 2 完成檢查清單

- [ ] 證券 API 下單條款已簽署
- [ ] 期貨/選擇權 API 下單條款已簽署
- [ ] 簽署申請已提交審核

---

## 3️⃣ 申請 API Key 和 Secret Key

### 步驟 3.1：申請 API Key

1. 登入永豐金客戶端
2. 進入「我的帳戶」或「設定」
3. 尋找「API 金鑰管理」或「API 設定」
4. 點擊「申請 API Key」

### 步驟 3.2：取得金鑰

系統會產生：
- **API Key**（14 位英數字組合）
- **Secret Key**（32 位英數字組合）

### 步驟 3.3：妥善保管金鑰

```bash
# 千萬不要：
❌ 上傳到 GitHub
❌ 提交到版本控制
❌ 分享給他人
❌ 放在前端代碼中

# 應該這樣做：
✅ 保存到 .env 文件（不提交到版本控制）
✅ 保存到環境變數
✅ 保存到安全的密碼管理器
```

### 📌 需要確認的事項

- [ ] API Key 已申請成功
- [ ] Secret Key 已妥善記錄
- [ ] 確認 API Key 已開通「交易」權限

### ✓ 步驟 3 完成檢查清單

- [ ] 已取得 API Key
- [ ] 已取得 Secret Key
- [ ] 金鑰已妥善保管
- [ ] 確認已啟用「交易」權限

---

## 4️⃣ 完成模擬模式測試

### 步驟 4.1：設置測試環境

#### 方式 A：Python 直接測試

```bash
# 安裝 Shioaji
pip install shioaji

# 確認版本
python -c "import shioaji; print(shioaji.__version__)"
```

#### 方式 B：使用 Shioaji Server 和 CLI

```bash
# 安裝 shioaji 命令行工具
uv tool install shioaji

# 檢查版本
shioaji server check
```

### 步驟 4.2：登入測試

#### Python 測試

```python
import shioaji as sj

# 進入模擬模式
api = sj.Shioaji(simulation=True)

# 使用金鑰登入
accounts = api.login(
    api_key="YOUR_API_KEY",        # 替換為你的 API Key
    secret_key="YOUR_SECRET_KEY"   # 替換為你的 Secret Key
)

# 確認帳戶已登入
print("登入成功！")
print("帳戶列表：")
for account in accounts:
    print(f"  - {account}")
    print(f"    是否已簽署: {account.signed}")

# 確認帳戶對象
print(f"\n股票帳戶：{api.stock_account}")
print(f"期貨帳戶：{api.futopt_account}")
```

#### CLI 測試

方式 1：使用 .env 文件
```bash
# 創建 .env 文件
cat > .env << EOF
SJ_API_KEY=YOUR_API_KEY
SJ_SEC_KEY=YOUR_SECRET_KEY
SJ_PRODUCTION=false              # 模擬模式
EOF

# 啟動 server（自動讀取 .env）
shioaji server start

# 在另一個終端檢查帳戶
shioaji auth accounts
```

方式 2：使用命令行參數
```bash
shioaji auth login --api-key YOUR_API_KEY --secret-key YOUR_SECRET_KEY --simulation
```

#### HTTP API 測試

```bash
# 1. 啟動 shioaji server（使用 .env）
shioaji server start

# 2. 在另一個終端查詢帳戶
curl http://localhost:8080/api/v1/auth/accounts
```

### 步驟 4.3：證券下單測試

**時間限制：**
- 周一至周五：08:00 ~ 20:00
- 18:00 ~ 20:00：只允許台灣 IP
- 08:00 ~ 18:00：無限制

#### Python 下單測試

```python
import shioaji as sj

api = sj.Shioaji(simulation=True)
api.login(api_key="YOUR_API_KEY", secret_key="YOUR_SECRET_KEY")

# 選擇商品（以台積電為例）
contract = api.Contracts.Stocks.TSE.TSE2890

# 建立委託單
order = sj.StockOrder(
    action=sj.Action.Buy,                    # 買進
    price=28,                                # 價格（必須合理）
    quantity=1,                              # 數量：1 張 = 1000 股
    price_type=sj.StockPriceType.LMT,        # 限價單
    order_type=sj.OrderType.ROD,             # ROD（當日有效）
    order_lot=sj.StockOrderLot.Common,       # 整股
    order_cond=sj.StockOrderCond.Cash,       # 現股交易
    account=api.stock_account                # 使用股票帳戶
)

# 下單
try:
    trade = api.place_order(contract, order)
    print("✅ 證券下單成功！")
    print(f"委託編號：{trade.status.id}")
    print(f"委託狀態：{trade.status.status}")
except Exception as e:
    print(f"❌ 下單失敗：{e}")
```

#### CLI 下單測試

```bash
shioaji order place \
    --code 2890 \
    --action buy \
    --price 28 \
    --quantity 1 \
    --price-type lmt \
    --order-type rod \
    --order-lot common \
    --order-cond cash \
    --account YOUR_BROKER_ID-YOUR_ACCOUNT_ID
```

#### HTTP 下單測試

```bash
curl -X POST http://localhost:8080/api/v1/order/place_order \
  -H "Content-Type: application/json" \
  -d '{
    "contract": {
      "security_type": "STK",
      "exchange": "TSE",
      "code": "2890"
    },
    "stock_order": {
      "action": "Buy",
      "price": 28,
      "quantity": 1,
      "price_type": "LMT",
      "order_type": "ROD",
      "order_lot": "Common",
      "order_cond": "Cash",
      "account": {
        "broker_id": "YOUR_BROKER_ID",
        "account_id": "YOUR_ACCOUNT_ID"
      }
    }
  }'
```

### 步驟 4.4：期貨下單測試

**重要：需要間隔 1 秒以上**

#### Python 期貨下單測試

```python
import shioaji as sj
import time

api = sj.Shioaji(simulation=True)
api.login(api_key="YOUR_API_KEY", secret_key="YOUR_SECRET_KEY")

# 選擇期貨商品（以台股期貨為例）
contract = api.Contracts.Futures.TXF.TXFE6

# 建立期貨委託單
order = sj.FuturesOrder(
    action=sj.Action.Buy,                    # 買進
    price=37000,                             # 價格
    quantity=1,                              # 數量：1 口
    price_type=sj.FuturesPriceType.LMT,      # 限價單
    order_type=sj.OrderType.ROD,             # ROD（當日有效）
    octype=sj.FuturesOCType.Auto,            # 自動倉別
    account=api.futopt_account               # 使用期貨帳戶
)

# 下單
try:
    trade = api.place_order(contract, order)
    print("✅ 期貨下單成功！")
    print(f"委託編號：{trade.status.id}")
    print(f"委託狀態：{trade.status.status}")
except Exception as e:
    print(f"❌ 下單失敗：{e}")
```

#### CLI 期貨下單測試

```bash
shioaji order place \
    --code TXFE6 \
    --security-type FUT \
    --action buy \
    --price 37000 \
    --quantity 1 \
    --price-type lmt \
    --order-type rod \
    --octype auto \
    --account YOUR_BROKER_ID-YOUR_ACCOUNT_ID
```

### ✓ 步驟 4 完成檢查清單

- [ ] 登入測試成功（帳戶顯示）
- [ ] 證券下單測試成功（委託編號產生）
- [ ] 期貨下單測試成功（委託編號產生）
- [ ] 記錄所有委託編號
- [ ] 準備提交測試報告

---

## 5️⃣ 確認測試是否通過 (signed=True)

### 步驟 5.1：查詢簽署狀態

#### Python 查詢

```python
import shioaji as sj

api = sj.Shioaji(simulation=True)
accounts = api.login(api_key="YOUR_API_KEY", secret_key="YOUR_SECRET_KEY")

print("帳戶簽署狀態：")
for account in accounts:
    print(f"\n帳戶：{account}")
    print(f"  類型：{account.__class__.__name__}")
    print(f"  已簽署：{account.signed}")  # ✅ True = 已簽署, ❌ False = 未簽署
```

#### CLI 查詢

```bash
# 方式 1：使用 server 查詢
shioaji auth accounts

# 方式 2：檢查 info 端點
curl http://localhost:8080/api/v1/info
```

### 步驟 5.2：理解簽署狀態

| 狀態 | 含義 | 可進行操作 |
|------|------|---------|
| **signed=True** | ✅ 已簽署並通過審核 | 可以在正式環境下單 |
| **signed=False** | ❌ 未簽署或待審核 | 只能在模擬環境測試 |

### 步驟 5.3：如果未顯示 signed=True

**可能的原因：**

1. 簽署申請尚未通過審核
   - ✓ 等待 1-3 個工作天

2. 簽署時間早於 API 申請時間
   - ✓ 需要重新簽署（簽署時間必須晚於 API 申請時間）

3. 沒有完成測試報告
   - ✓ 按照步驟 4.3 和 4.4 完成測試並提交

### ✓ 步驟 5 完成檢查清單

- [ ] 查詢帳戶狀態
- [ ] 確認 signed=True（至少一個帳戶類型）
- [ ] 如果未顯示 True，確認原因並採取行動

---

## 6️⃣ 申請並啟用憑證

### 步驟 6.1：申請 CA 憑證

1. 登入永豐金客戶端
2. 進入「我的帳戶」或「設定」
3. 尋找「憑證管理」或「CA 憑證」
4. 申請新的 CA 憑證（.pfx 格式）
5. 設置憑證密碼

### 步驟 6.2：下載憑證文件

- 下載 CA 憑證文件（格式：`.pfx` 或 `.p12`）
- 妥善保存密碼
- **不要上傳到版本控制**

### 步驟 6.3：配置憑證到 .env 文件

```bash
# 編輯 .env 文件
cat > .env << EOF
# API 金鑰
SJ_API_KEY=YOUR_API_KEY
SJ_SEC_KEY=YOUR_SECRET_KEY

# CA 憑證（正式環境必須）
SJ_CA_PATH=/path/to/Sinopac.pfx            # 憑證文件路徑
SJ_CA_PASSWD=YOUR_CA_PASSWORD              # 憑證密碼

# 環境設置（still in simulation mode for now）
SJ_PRODUCTION=false
EOF
```

### 步驟 6.4：驗證憑證已載入

#### Python 驗證

```python
import shioaji as sj
import os

# 設置環境變數
os.environ['SJ_CA_PATH'] = '/path/to/Sinopac.pfx'
os.environ['SJ_CA_PASSWD'] = 'YOUR_CA_PASSWORD'

# 仍然在模擬模式下測試
api = sj.Shioaji(simulation=True)
accounts = api.login(api_key="YOUR_API_KEY", secret_key="YOUR_SECRET_KEY")

print("✅ 憑證已載入且登入成功")
```

#### CLI 驗證

```bash
# 啟動 server
shioaji server start

# 在另一個終端檢查狀態
shioaji server status --streams

# 查看日誌中是否有 "CA certificate activated successfully"
```

#### HTTP 驗證

```bash
curl http://localhost:8080/api/v1/info
# 查看回應確認服務正常運行
```

### ✓ 步驟 6 完成檢查清單

- [ ] CA 憑証已申請
- [ ] 憑證文件已下載
- [ ] 憑證密碼已記錄
- [ ] .env 已配置憑證路徑和密碼
- [ ] 驗證憑證已成功載入

---

## 7️⃣ 切換到正式環境

### ⚠️ 重要警告

**在執行此步驟前，請確認：**

- ✅ 已完成步驟 1-6
- ✅ 帳戶顯示 signed=True
- ✅ 模擬環境測試全部成功
- ✅ CA 憑證已成功載入
- ✅ 完全理解正式環境是真實交易環境

### 步驟 7.1：修改 .env 文件

```bash
# 編輯 .env 文件，改為正式模式
cat > .env << EOF
# API 金鑰
SJ_API_KEY=YOUR_API_KEY
SJ_SEC_KEY=YOUR_SECRET_KEY

# CA 憑證（正式環境必須）
SJ_CA_PATH=/path/to/Sinopac.pfx
SJ_CA_PASSWD=YOUR_CA_PASSWORD

# ⚠️ 從 false 改為 true！
SJ_PRODUCTION=true              # 正式環境

EOF
```

### 步驟 7.2：Python 方式切換

```python
import shioaji as sj
import os

# 設置為正式模式（改為 False = 模擬, True = 正式）
api = sj.Shioaji(simulation=False)  # ⚠️ 改為 False（關閉模擬）

# 使用金鑰登入
accounts = api.login(
    api_key="YOUR_API_KEY",
    secret_key="YOUR_SECRET_KEY",
    ca_path=os.environ.get("SJ_CA_PATH"),
    ca_passwd=os.environ.get("SJ_CA_PASSWD")
)

print("✅ 已連接到正式環境！")
print("警告：這是實際交易環境。請謹慎操作。")
for account in accounts:
    print(f"  - {account} (signed={account.signed})")
```

### 步驟 7.3：CLI 方式切換

```bash
# 確保 .env 中 SJ_PRODUCTION=true
shioaji server start

# 驗證連接到正式環境
curl http://localhost:8080/api/v1/info
# 查看回應中 "simulation": false
```

### 步驟 7.4：驗證正式連接

#### Python 驗證

```python
import shioaji as sj

api = sj.Shioaji(simulation=False)
accounts = api.login(api_key="YOUR_API_KEY", secret_key="YOUR_SECRET_KEY")

# 查詢帳戶餘額
for account in accounts:
    if account.signed:
        try:
            balance = api.account_balance(account=account)
            print(f"帳戶 {account.account_id}：")
            print(f"  現金餘額：${balance.acc_balance:,.0f} 元")
        except:
            pass
```

#### HTTP 驗證

```bash
# 查詢帳戶餘額
curl -X POST http://localhost:8080/api/v1/portfolio/account_balance \
  -H 'Content-Type: application/json' \
  -d '{}'
```

### ✓ 步驟 7 完成檢查清單

- [ ] .env 中 SJ_PRODUCTION=true
- [ ] 已連接到正式環境
- [ ] 可以查詢帳戶餘額和部位
- [ ] 確認帳戶資訊無誤

---

## 🎉 全部完成！

恭喜！你已經成功設置 Shioaji 並連接到正式交易環境！

### 📌 接下來的建議

1. **學習下單**
   - 熟悉不同的委託類型
   - 了解風險管理

2. **監控帳戶**
   - 定期查詢餘額
   - 監控部位和損益

3. **自動化交易**
   - 開發交易策略
   - 測試回測系統

4. **持續學習**
   - 閱讀官方文檔
   - 加入社群交流

---

## 🚨 常見問題排除

### Q1：登入失敗「Invalid API Key」

**解決方案：**
- 檢查 API Key 是否正確複製（無空格）
- 確認 API Key 是否已啟用「交易」權限
- 重新申請新的 API Key

### Q2：下單失敗「Account is not signed」

**解決方案：**
- 確認帳戶已簽署 (signed=True)
- 如果未顯示，等待 1-3 個工作天審核
- 檢查簽署時間是否晚於 API 申請時間

### Q3：切換到正式環境後收不到行情

**解決方案：**
- 確認 CA 憑證已正確載入
- 檢查 .env 檔案中的路徑是否正確
- 確認憑證密碼是否正確
- 查看伺服器日誌

### Q4：「Permission denied」錯誤

**解決方案：**
- 檢查 .pfx 檔案的訪問權限
- 確認路徑指向正確的位置
- 如使用相對路徑，確認無誤

### Q5：模擬環境可以，但正式環境出現 502 錯誤

**解決方案：**
- 重啟 shioaji server
- 檢查網路連接
- 確認憑證是否過期
- 聯繫永豐金技術支持

---

## 📞 技術支持

- **永豐金官網**：https://www.sinotrade.com.tw/
- **Shioaji 文檔**：https://sinotrade.github.io/
- **GitHub Issues**：https://github.com/sinotrade/shioaji/issues

---

**最後更新：2026-06-22**
**版本：1.0（完整新手指南）**
