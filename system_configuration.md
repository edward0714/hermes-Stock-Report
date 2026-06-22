# Hermes Agent 系統完整配置記錄

## 最後更新時間
2026-06-22 12:10 UTC (台北時間 20:10)

---

## 📋 系統排程配置

### 1. 每日財經晨報 Pro - 含郵件通知

```
Job ID: 169b7d6cd8b1
名稱: 每日財經晨報 Pro - 含郵件通知
排程: 0 0 * * * (每天 00:00 UTC)
台北時間: 每天 08:00
頻率: 每天執行，無限期
執行腳本: daily_financial_report_pro_email.py
工作目錄: /opt/data/.hermes/scripts/
狀態: ✅ 已啟用
傳送目標: origin (當前對話)
```

**執行功能：**
- 生成圖文並茂 HTML 財經晨報
- 推送到 GitHub Pages
- 發送郵件到 jiunwie.hu@gmail.com (標題: YYYY-MM-DD - 每日財經晨報)

---

### 2. 每日定期備份 - Hermes Agent 環境

```
Job ID: 3f8a35bfb6b9
名稱: 每日定期備份 - Hermes Agent 環境（半夜 02:00）
排程: 0 18 * * * (每天 18:00 UTC)
台北時間: 每天 02:00 (半夜)
頻率: 每天執行，無限期
執行腳本: backup_to_gdrive.py
工作目錄: /opt/data/.hermes/scripts/
狀態: ✅ 已啟用
傳送目標: origin (當前對話)
```

**執行功能：**
- 收集所有配置文件
- 建立完整備份檔案 (tar.gz)
- 自動上傳到 Google Drive
- 存放在「Hermes Agent Backup」資料夾

---

## 🔗 重要位置

### 本地配置文件

```
/opt/data/google_token.json                    ← Google OAuth Token
/opt/data/google_client_secret.json            ← Google Client Secret  
/opt/data/.env                                 ← GitHub Token
~/.gitconfig                                   ← Git 全局配置

/opt/data/scripts/prompt_financial_report_pro.md       ← 提示詞框架 (204 行)
/opt/data/.hermes/scripts/daily_financial_report_pro_email.py   ← 晨報腳本 (260 行)
/opt/data/.hermes/scripts/backup_to_gdrive.py          ← 備份腳本

/tmp/hermes-Stock-Report/reports/daily-report-template-pro.html ← HTML 模板 (1120 行)
/tmp/hermes-Stock-Report/news/                                   ← 報告輸出
/tmp/hermes-Stock-Report/.git/config                             ← Git 配置
```

### Google Drive 備份

```
資料夾名: Hermes Agent Backup
Folder ID: 1Bq6R7XkngVSTKLU_K29E49bmXD41D7HU
連結: https://drive.google.com/drive/folders/1Bq6R7XkngVSTKLU_K29E49bmXD41D7HU

備份檔案格式: Hermes-Agent-YYYY-MM-DD-HHmmss.tar.gz
```

---

## 📊 每日自動化時間表 (台北時間)

```
02:00 🌙 → 定期備份開始
         ✓ 收集配置文件
         ✓ 建立備份檔
         ✓ 上傳到 Google Drive

08:00 📊 → 財經晨報生成
         ✓ 生成 HTML 報告
         ✓ 推送 GitHub Pages  
         ✓ 發送郵件通知
```

---

## ✅ 重啟前系統狀態確認

### 排程狀態
- ✅ 每日財經晨報: 已啟用
- ✅ 每日定期備份: 已啟用
- ✅ 全部正常運作

### 認證狀態
- ✅ Google OAuth: 已授權完整作用域
- ✅ GitHub Token: 已配置
- ✅ Git 全局配置: 已設定 (edward0714 <jiunwie.hu@gmail.com>)

### 文件狀態
- ✅ 提示詞框架: 已創建 (204 行)
- ✅ 晨報腳本: 已創建 (260 行)
- ✅ 備份腳本: 已創建 (已測試)
- ✅ HTML 模板: 已創建 (1120 行，導航功能已修復)

### GitHub 連接
- ✅ Repository: edward0714/hermes-Stock-Report
- ✅ Remote: 已配置
- ✅ GitHub Pages: https://edward0714.github.io/hermes-Stock-Report/news/index.html

---

## 🔐 敏感信息備份位置

所有敏感信息已備份到：
- Google Drive: Hermes Agent Backup 資料夾
- 本地備份副本: /tmp/hermes_agent_backup/

**注意**: 備份檔包含認證信息，請妥善保管。

---

## 🚀 重啟步驟

1. 執行: `hermes restart`
2. 等待 Hermes 完全重啟
3. 驗證排程: `hermes cron list`
4. 檢查服務: `hermes status`
5. 測試功能: 執行手動備份或晨報生成

---

## 📝 恢復指南

如果系統需要恢復：
1. 從 Google Drive 下載最新的 Hermes-Agent-*.tar.gz
2. 解壓: `tar -xzf Hermes-Agent-*.tar.gz`
3. 參考備份內的 README.md 恢復文件
4. 重啟 Hermes 系統
5. 重新建立排程任務

---

## 📞 快速命令參考

```bash
# 檢查所有排程
hermes cron list

# 手動執行晨報
/opt/data/.venv/bin/python /opt/data/.hermes/scripts/daily_financial_report_pro_email.py

# 手動執行備份
/opt/data/.venv/bin/python /opt/data/.hermes/scripts/backup_to_gdrive.py

# 暫停特定排程
hermes cron pause 169b7d6cd8b1    # 晨報
hermes cron pause 3f8a35bfb6b9    # 備份

# 恢復特定排程
hermes cron resume 169b7d6cd8b1   # 晨報
hermes cron resume 3f8a35bfb6b9   # 備份

# 重啟 Hermes
hermes restart
```

---

配置記錄完成日期: 2026-06-22
配置版本: 1.0 (最終版)
狀態: ✅ 生產環境就緒
