#!/usr/bin/env python3
"""
每日財經晨報生成器 - 將 Hermes 的分析結果轉成 HTML 並上傳到 GitHub
"""
import json
import os
from datetime import datetime
from pathlib import Path

def generate_daily_report(
    date: str,
    bullish_1_title: str,
    bullish_1_text: str,
    bullish_2_title: str,
    bullish_2_text: str,
    bearish_1_title: str,
    bearish_1_text: str,
    news_1: str,
    news_2: str,
    news_3: str,
) -> str:
    """
    生成 HTML 報告
    
    Args:
        date: 日期字串 (YYYY-MM-DD)
        其他參數：市場觀點和新聞內容
    
    Returns:
        HTML 字串
    """
    
    # 讀取模板
    template_path = Path(__file__).parent / "daily-report-template.html"
    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 替換變數
    replacements = {
        '{{DATE}}': date,
        '{{BULLISH_1_TITLE}}': bullish_1_title,
        '{{BULLISH_1_TEXT}}': bullish_1_text,
        '{{BULLISH_2_TITLE}}': bullish_2_title,
        '{{BULLISH_2_TEXT}}': bullish_2_text,
        '{{BEARISH_1_TITLE}}': bearish_1_title,
        '{{BEARISH_1_TEXT}}': bearish_1_text,
        '{{NEWS_1}}': news_1,
        '{{NEWS_2}}': news_2,
        '{{NEWS_3}}': news_3,
    }
    
    for key, value in replacements.items():
        html = html.replace(key, value)
    
    return html

def save_report(html: str, date: str, repo_path: str = "/tmp/hermes-Stock-Report"):
    """
    儲存 HTML 報告到指定目錄
    
    Args:
        html: HTML 內容
        date: 日期 (YYYY-MM-DD)
        repo_path: Repo 根目錄路徑
    """
    
    # 建立日期目錄結構 news/YYYY/MM/
    year, month, day = date.split('-')
    news_dir = Path(repo_path) / "news" / year / month
    news_dir.mkdir(parents=True, exist_ok=True)
    
    # 儲存檔案
    file_path = news_dir / f"{date}.html"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 報告已建立: {file_path}")
    return file_path

def update_index(date: str, repo_path: str = "/tmp/hermes-Stock-Report"):
    """
    更新首頁 index.html，加入新報告的連結
    
    Args:
        date: 日期 (YYYY-MM-DD)
        repo_path: Repo 根目錄路徑
    """
    
    index_path = Path(repo_path) / "index.html"
    year, month, day = date.split('-')
    report_link = f"./news/{year}/{month}/{date}.html"
    
    # 讀取現有 index
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 在 <ul> 中插入新項目
    new_item = f'        <li><a href="{report_link}">{date} 財經晨報</a></li>\n'
    
    # 找到第一個 </ul> 並在之前插入
    if '<ul>' in content:
        content = content.replace('    <ul>\n', f'    <ul>\n{new_item}', 1)
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 首頁已更新")

def git_push(date: str, repo_path: str = "/tmp/hermes-Stock-Report"):
    """
    提交並推送到 GitHub
    
    Args:
        date: 日期 (YYYY-MM-DD)
        repo_path: Repo 根目錄路徑
    """
    
    os.chdir(repo_path)
    
    # git add
    os.system("git add .")
    
    # git commit
    commit_msg = f"feat: Add daily report for {date}"
    os.system(f'git commit -m "{commit_msg}"')
    
    # git push
    result = os.system("git push origin main")
    
    if result == 0:
        print(f"✅ 已推送到 GitHub")
    else:
        print(f"⚠️ 推送失敗，請檢查網路或認證")

if __name__ == "__main__":
    # 示例使用
    today = datetime.now().strftime("%Y-%m-%d")
    
    html = generate_daily_report(
        date=today,
        bullish_1_title="台股站穩年線",
        bullish_1_text="台股技術面突破關鍵支撐，籌碼面轉強，法人買超續增強市場信心。",
        bullish_2_title="AI 概念股續漲",
        bullish_2_text="英偉達財報超預期，帶動全球 AI 晶片需求，台灣半導體指數漲幅達 2.5%。",
        bearish_1_title="美聯準鷹派基調不變",
        bearish_1_text="Fed 官員暗示可能延後降息，美債殖利率上升，科技股承壓。",
        news_1="超微 (AMD) 宣布推出新一代 EPYC 處理器，競爭力大幅提升。",
        news_2="歐洲央行維持基準利率不變，但表示下月可能降息 0.25%。",
        news_3="台灣今年 Q2 出口成長 8.2%，超越市場預期，經濟動能強勁。",
    )
    
    file_path = save_report(html, today)
    update_index(today)
    git_push(today)
    
    print("\n📊 財經晨報流程完成！")
    print(f"📝 報告連結: https://github.com/edward0714/hermes-Stock-Report/blob/main/news/{today.replace('-', '/')}/{today}.html")
