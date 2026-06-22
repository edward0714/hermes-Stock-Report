# Hermes Agent 系統完整恢復指南

## 📋 概述

本指南用於在 Hermes Agent 系統損毀或需要重建時，從 Google Drive 備份檔案完全恢復系統。恢復過程預計耗時 **15-30 分鐘**。

---

## 🎯 適用場景

- ✅ 系統遭到破壞或數據丟失
- ✅ 需要遷移到新的伺服器或環境
- ✅ 重新初始化 Hermes Agent
- ✅ 復原到備份時的完整系統狀態

---

## 📦 準備工作

### 所需資源

1. **Google Drive 備份檔案**
   - 位置：Google Drive > AI協作區 > Hermes Agent Backup
   - 檔案格式：`Hermes-Agent-YYYY-MM-DD-HHmmss.tar.gz`
   - 最新備份自動每天 02:00 (台北時間) 生成

2. **系統環境**
   - Linux 環境 (Ubuntu 20.04+ 推薦)
   - Bash Shell
   - 基本命令工具：tar, mkdir, cp, chmod 等

3. **網路連接**
   - 能夠連接 Google Drive
   - 能夠連接 GitHub
   - 能夠連接 Hermes Portal (Nous)

### 前置條件檢查

```bash
# 檢查 tar 命令可用
tar --version

# 檢查磁盤空間 (至少 1 GB)
df -h /opt/data

# 檢查網路連接
ping google.com
```

---

## 🔄 完整恢復步驟

### 第 1 步：下載備份檔案

**方式 A：透過 Google Drive 網頁**

1. 打開 https://drive.google.com
2. 進入「AI協作區 > Hermes Agent Backup」資料夾
3. 選擇最新的 `Hermes-Agent-*.tar.gz` 檔案
4. 右鍵 → 下載到本地

**方式 B：直接使用下載連結**

```bash
# 以最新備份 (2026-06-22-121302) 為例
wget "https://drive.google.com/uc?export=download&id=14rtEKLGfI5-pGPQtWN0yGkfPzGVdToEr" \
  -O Hermes-Agent-2026-06-22-121302.tar.gz
```

---

### 第 2 步：驗證備份檔案

```bash
# 檢查檔案大小 (應該 ~30 KB)
ls -lh Hermes-Agent-*.tar.gz

# 驗證壓縮檔完整性
tar -tzf Hermes-Agent-*.tar.gz | head -20

# 查看備份包含的文件
tar -tzf Hermes-Agent-*.tar.gz | wc -l
```

**預期輸出：**
- 檔案大小：25-35 KB
- 包含 10+ 個文件和文件夾
- 應該看到 `README.md`、`metadata.json` 等

---

### 第 3 步：創建恢復目錄

```bash
# 創建臨時恢復目錄
mkdir -p /opt/hermes_recovery
cd /opt/hermes_recovery

# 複製備份檔案到恢復目錄
cp ~/Hermes-Agent-*.tar.gz /opt/hermes_recovery/

# 解壓備份檔案
tar -xzf Hermes-Agent-*.tar.gz

# 檢查解壓結果
ls -la
```

**預期結構：**
```
Hermes-Agent-YYYY-MM-DD-HHMMSS/
├── auth/                          ← 認證文件
│   ├── google_token.json
│   ├── google_client_secret.json
│   ├── .env
│   └── .gitconfig
├── prompts/                        ← 提示詞
│   └── prompt_financial_report_pro.md
├── scripts/                        ← 執行腳本
│   ├── daily_financial_report_pro_email.py
│   └── backup_to_gdrive.py
├── templates/                      ← HTML 模板
│   └── daily-report-template-pro.html
├── docs/                           ← 文檔
│   └── system_backup_checklist.md
├── git_config/                     ← Git 配置
│   └── config
├── README.md                       ← 恢復指南
└── metadata.json                   ← 備份元數據
```

---

### 第 4 步：恢復認證文件

```bash
# 進入解壓目錄
cd Hermes-Agent-YYYY-MM-DD-HHMMSS

# 恢復 Google 認證
cp auth/google_token.json /opt/data/
cp auth/google_client_secret.json /opt/data/

# 恢復 GitHub Token
cp auth/.env /opt/data/

# 恢復 Git 全局配置
cp auth/.gitconfig ~/.gitconfig

# 驗證恢復
ls -la /opt/data/google_token.json
ls -la /opt/data/.env
```

**安全性注意：**
- 這些文件包含敏感的認證信息
- 確保限制文件權限：`chmod 600 /opt/data/google_token.json`
- 不要在公開的 Git 倉庫中提交這些文件

---

### 第 5 步：恢復腳本和配置

```bash
# 恢復提示詞框架
cp prompts/prompt_financial_report_pro.md /opt/data/scripts/

# 恢復執行腳本
cp scripts/* /opt/data/.hermes/scripts/

# 恢復 HTML 模板
mkdir -p /tmp/hermes-Stock-Report/reports
cp templates/daily-report-template-pro.html \
   /tmp/hermes-Stock-Report/reports/

# 給予腳本執行權限
chmod +x /opt/data/.hermes/scripts/*.py

# 驗證恢復
ls -lh /opt/data/.hermes/scripts/
```

---

### 第 6 步：恢復 Git 配置和 Repository

```bash
# 如果 Git repository 不存在，需要重新克隆
if [ ! -d /tmp/hermes-Stock-Report ]; then
  git clone https://github.com/edward0714/hermes-Stock-Report.git \
    /tmp/hermes-Stock-Report
fi

# 進入 repository 目錄
cd /tmp/hermes-Stock-Report

# 恢復 Git 配置
cp ../git_config/config .git/

# 驗證 Git 連接
git remote -v
git config user.name
git config user.email
```

**預期輸出：**
```
origin  https://github.com/edward0714/hermes-Stock-Report.git (fetch)
origin  https://github.com/edward0714/hermes-Stock-Report.git (push)
user.name: edward0714
user.email: jiunwie.hu@gmail.com
```

---

### 第 7 步：驗證系統完整性

```bash
# 驗證 Google Workspace 認證
/opt/data/.venv/bin/python /opt/data/skills/productivity/google-workspace/scripts/google_api.py gmail whoami

# 驗證 GitHub 連接
cd /tmp/hermes-Stock-Report && git remote show origin

# 驗證 Python 環境
/opt/data/.venv/bin/python --version

# 驗證 Hermes Agent
hermes status
```

**預期結果：**
- ✅ Gmail 連接正常
- ✅ GitHub remote 正確配置
- ✅ Python 3.13.5
- ✅ Hermes Agent 運行正常

---

### 第 8 步：重新建立 Cronjob 排程

```bash
# 檢查現有排程
hermes cron list

# 如果 cronjob 不存在，使用以下命令重建

# 每日財經晨報 (08:00 台北時間)
hermes cron create \
  --name "每日財經晨報 Pro - 含郵件通知" \
  --schedule "0 0 * * *" \
  --script "daily_financial_report_pro_email.py" \
  --no-agent \
  --deliver "origin"

# 每日定期備份 (02:00 台北時間)
hermes cron create \
  --name "每日定期備份 - Hermes Agent 環境（半夜 02:00）" \
  --schedule "0 18 * * *" \
  --script "backup_to_gdrive.py" \
  --no-agent \
  --deliver "origin"

# 驗證排程已建立
hermes cron list
```

---

### 第 9 步：測試系統功能

#### 測試 1：手動執行財經晨報

```bash
# 執行晨報腳本
/opt/data/.venv/bin/python /opt/data/.hermes/scripts/daily_financial_report_pro_email.py

# 檢查輸出
# 應該看到「✅ 報告已推送到 GitHub Pages」
# 應該看到「✅ 郵件已發送」
```

#### 測試 2：手動執行備份

```bash
# 執行備份腳本
/opt/data/.venv/bin/python /opt/data/.hermes/scripts/backup_to_gdrive.py

# 檢查輸出
# 應該看到「✅ 已上傳到 Google Drive」
# 應該看到備份檔案名稱和大小
```

#### 測試 3：驗證 Google Drive 備份

```bash
# 檢查備份是否已上傳
/opt/data/.venv/bin/python /opt/data/skills/productivity/google-workspace/scripts/google_api.py \
  drive search "Hermes-Agent" --max 5
```

#### 測試 4：驗證 GitHub Pages

```bash
# 檢查報告是否已上傳到 GitHub
curl -s https://edward0714.github.io/hermes-Stock-Report/news/index.html | head -20
```

---

## 🚨 故障排除

### 問題 1：Google 認證失敗

**症狀：** `❌ 無法獲取 access token`

**解決方案：**
```bash
# 重新授權 Google
/opt/data/.venv/bin/python /opt/data/skills/productivity/google-workspace/scripts/google_api.py \
  gmail whoami

# 會提示打開認證連結，完成 OAuth 流程
```

### 問題 2：GitHub 連接失敗

**症狀：** `fatal: could not read Username for 'https://github.com': No such file or directory`

**解決方案：**
```bash
# 重新配置 Git 認證
cd /tmp/hermes-Stock-Report
git config credential.helper store
git pull origin main
# 會提示輸入 GitHub credentials

# 或使用 SSH 金鑰
git remote set-url origin git@github.com:edward0714/hermes-Stock-Report.git
```

### 問題 3：Cronjob 沒有執行

**症狀：** 排程顯示已啟用，但沒有執行

**解決方案：**
```bash
# 檢查 Hermes 排程服務
hermes status

# 手動觸發一次排程
hermes cron run <job_id>

# 檢查排程日誌
hermes logs
```

### 問題 4：腳本執行失敗

**症狀：** 執行腳本時出現 `Permission denied` 或 `module not found`

**解決方案：**
```bash
# 確保腳本可執行
chmod +x /opt/data/.hermes/scripts/*.py

# 確保 Python venv 正常
/opt/data/.venv/bin/python --version

# 重新裝載依賴
source /opt/data/.venv/bin/activate
pip list | grep google
```

---

## 📊 恢復後的驗證清單

恢復完成後，請檢查以下項目：

- [ ] Google Workspace 認證正常 (`hermes status` 顯示 ✓)
- [ ] GitHub 連接正常 (可以 `git pull`)
- [ ] 兩個 Cronjob 已建立 (`hermes cron list` 顯示 2 個)
- [ ] 可以手動執行晨報腳本
- [ ] 可以手動執行備份腳本
- [ ] 手動執行後能看到在 Google Drive 中上傳的備份
- [ ] 手動執行後能看到 GitHub 上推送的報告
- [ ] 手動執行後能收到郵件通知

---

## 🔄 恢復後的後續步驟

1. **立即備份驗證**
   ```bash
   # 執行一次手動備份驗證恢復效果
   /opt/data/.venv/bin/python /opt/data/.hermes/scripts/backup_to_gdrive.py
   ```

2. **排程驗證**
   ```bash
   # 等待下一個排程時間 (或手動執行)
   # 確認晨報和備份正常執行
   ```

3. **更新系統文檔**
   ```bash
   # 根據恢復完成的時間，更新配置記錄
   # 編輯 /opt/data/system_configuration.md
   ```

4. **建立新的備份**
   ```bash
   # 恢復完成後，立即執行一次備份
   # 以新的備份檔案作為「已驗證可恢復的狀態」標記
   ```

---

## 📚 文件索引

| 文件 | 位置 | 用途 |
|------|------|------|
| 恢復指南 | 本文件 | 系統恢復步驟 |
| 系統配置 | `/opt/data/system_configuration.md` | 系統配置記錄 |
| 備份清單 | `/opt/data/system_backup_checklist.md` | 備份內容說明 |
| 晨報腳本 | `/opt/data/.hermes/scripts/daily_financial_report_pro_email.py` | 生成晨報 |
| 備份腳本 | `/opt/data/.hermes/scripts/backup_to_gdrive.py` | 備份系統 |

---

## 💡 重要提醒

1. **定期測試恢復流程**
   - 建議每月執行一次恢復測試
   - 確保備份檔案確實可用
   - 發現問題時及時修正

2. **保護認證文件**
   - Google Token 和 GitHub Token 是敏感信息
   - 不要在公開場合分享或提交到版本控制
   - 限制文件權限：`chmod 600`

3. **備份版本管理**
   - 保留至少 3 份最新備份
   - 檔案名稱中包含時間戳記便於識別
   - 定期清理過舊的備份檔案

4. **文檔更新**
   - 系統有重大更新時，更新此恢復指南
   - 記錄新增的依賴或配置
   - 保持 README.md 與實際系統同步

---

## 📞 常見問題

**Q: 恢復需要多長時間？**
A: 整個流程預計 15-30 分鐘，取決於網路速度和系統性能。

**Q: 可以恢復到之前的某個特定時間點嗎？**
A: 可以。Google Drive 中保存了每天的備份檔案，可以選擇任意日期的備份進行恢復。

**Q: 恢復後需要重新配置什麼嗎？**
A: 不需要。備份檔案包含所有認證和配置，恢復後可以直接使用。

**Q: 如果恢復失敗怎麼辦？**
A: 檢查故障排除部分，或從備份目錄中的 README.md 獲取具體協助。

---

## ✅ 恢復完成確認

當所有步驟完成後，系統應該恢復到備份時的完整狀態，並自動開始執行排程任務。

**恢復成功標誌：**
- ✅ Cronjob 正常執行
- ✅ 收到郵件通知
- ✅ GitHub Pages 更新
- ✅ Google Drive 新建備份檔案

---

**最後更新：2026-06-22**
**版本：1.0 (完整版)**
