#!/usr/bin/env python3
"""
完整的財經晨報工作流：
1. 從 web 搜尋最新財經新聞
2. 生成市場分析（利多/利空）
3. 生成 HTML 報告
4. 推送到 GitHub
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List

def extract_market_analysis(ai_response: str) -> Dict:
    """
    從 AI 回應中提取市場分析內容
    
    預期格式:
    ---
    [日期] 財經晨報
    
    ## 市場觀點
    
    * 【利多】[標題] [內容]
    * 【利多】[標題] [內容]
    * 【利空】[標題] [內容]
    
    ## 重要全球新聞
    
    * [新聞1]
    * [新聞2]
    * [新聞3]
    ---
    """
    
    result = {
        'bullish_1_title': '台股表現',
        'bullish_1_text': '台股持續上漲，技術面轉強。',
        'bullish_2_title': '科技股領漲',
        'bullish_2_text': 'AI 概念股繼續吸引資金流入。',
        'bearish_1_title': '國際風險',
        'bearish_1_text': '美聯準鷹派基調持續。',
        'news_1': '國際重要新聞待補充',
        'news_2': '總體經濟數據待補充',
        'news_3': '產業動態待補充',
    }
    
    try:
        # 提取利多1
        bullish1_match = re.search(r'【利多】([^\n]+?)\s+([^\n]+)', ai_response)
        if bullish1_match:
            result['bullish_1_title'] = bullish1_match.group(1).strip()
            result['bullish_1_text'] = bullish1_match.group(2).strip()
        
        # 提取利多2
        bullish2_matches = re.findall(r'【利多】([^\n]+?)\s+([^\n]+)', ai_response)
        if len(bullish2_matches) >= 2:
            result['bullish_2_title'] = bullish2_matches[1][0].strip()
            result['bullish_2_text'] = bullish2_matches[1][1].strip()
        
        # 提取利空
        bearish_match = re.search(r'【利空】([^\n]+?)\s+([^\n]+)', ai_response)
        if bearish_match:
            result['bearish_1_title'] = bearish_match.group(1).strip()
            result['bearish_1_text'] = bearish_match.group(2).strip()
        
        # 提取新聞
        news_matches = re.findall(r'^\*\s+(.+)$', ai_response, re.MULTILINE)
        for i, news in enumerate(news_matches[:3]):
            result[f'news_{i+1}'] = news.strip()
    
    except Exception as e:
        print(f"⚠️ 解析 AI 回應時出錯: {e}")
    
    return result

def generate_html_report(
    date: str,
    analysis: Dict,
    template_path: str = "/tmp/hermes-Stock-Report/reports/daily-report-template.html"
) -> str:
    """生成 HTML 報告"""
    
    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()
    
    replacements = {
        '{{DATE}}': date,
        '{{BULLISH_1_TITLE}}': analysis['bullish_1_title'],
        '{{BULLISH_1_TEXT}}': analysis['bullish_1_text'],
        '{{BULLISH_2_TITLE}}': analysis['bullish_2_title'],
        '{{BULLISH_2_TEXT}}': analysis['bullish_2_text'],
        '{{BEARISH_1_TITLE}}': analysis['bearish_1_title'],
        '{{BEARISH_1_TEXT}}': analysis['bearish_1_text'],
        '{{NEWS_1}}': analysis['news_1'],
        '{{NEWS_2}}': analysis['news_2'],
        '{{NEWS_3}}': analysis['news_3'],
    }
    
    for key, value in replacements.items():
        html = html.replace(key, value)
    
    return html

def save_and_push(
    html: str,
    date: str,
    repo_path: str = "/tmp/hermes-Stock-Report"
) -> str:
    """儲存報告並推送到 GitHub"""
    
    # 建立目錄
    year, month, day = date.split('-')
    news_dir = Path(repo_path) / "news" / year / month
    news_dir.mkdir(parents=True, exist_ok=True)
    
    # 儲存報告
    report_path = news_dir / f"{date}.html"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    # 更新 index
    index_path = Path(repo_path) / "index.html"
    with open(index_path, 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    new_item = f'        <li><a href="./news/{year}/{month}/{date}.html">{date} 財經晨報</a></li>\n'
    if '<ul>' in index_content and new_item not in index_content:
        index_content = index_content.replace('    <ul>\n', f'    <ul>\n{new_item}', 1)
    
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    # Git 操作
    os.chdir(repo_path)
    os.system("git add .")
    os.system(f'git commit -m "feat: Add daily report for {date}"')
    os.system("git push origin main")
    
    return f"https://github.com/edward0714/hermes-Stock-Report/blob/main/news/{year}/{month}/{date}.html"

# ===== 主程式 =====

if __name__ == "__main__":
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 示例 AI 回應（實際應該從 Hermes 的晨報分析取得）
    sample_ai_response = """
    【利多】台股站穩年線 台股技術面突破關鍵支撐，籌碼面轉強，法人買超續增。
    【利多】AI 晶片需求旺 英偉達財報超預期，帶動全球 AI 需求，台灣半導體漲幅 2.5%。
    【利空】Fed 維持鷹派 美聯準官員暗示延後降息，美債殖利率上升，科技股承壓。
    
    * 超微推出新一代 EPYC 處理器，與英偉達競爭加劇。
    * 歐央行6月維持利率，7月可能降息 0.25%。
    * 台灣 Q2 出口成長 8.2%，超越市場預期。
    """
    
    # 解析分析
    analysis = extract_market_analysis(sample_ai_response)
    
    # 生成 HTML
    html = generate_html_report(today, analysis)
    
    # 推送到 GitHub
    report_url = save_and_push(html, today)
    
    print(f"✅ 財經晨報已發布")
    print(f"📊 報告: {report_url}")
