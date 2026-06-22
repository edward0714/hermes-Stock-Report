#!/usr/bin/env python3
"""
完整的財經晨報工作流 - 自動更新 GitHub Pages
包含：
1. 生成 HTML 報告
2. 更新 news/index.html 的動態連結結構
3. 推送到 GitHub
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict

def extract_market_analysis(ai_response: str) -> Dict:
    """從 AI 回應中提取市場分析內容"""
    
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

def save_report(html: str, date: str, repo_path: str = "/tmp/hermes-Stock-Report") -> str:
    """儲存報告到指定目錄"""
    
    year, month, day = date.split('-')
    news_dir = Path(repo_path) / "news" / year / month
    news_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = news_dir / f"{date}.html"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 報告已建立: {file_path}")
    return str(file_path)

def update_news_index(date: str, repo_path: str = "/tmp/hermes-Stock-Report"):
    """
    動態更新 news/index.html
    自動檢測目錄結構，建立年份/月份的可摺疊導航
    """
    
    news_dir = Path(repo_path) / "news"
    
    # 掃描所有報告並組織成結構
    reports_by_year_month = {}
    
    for html_file in sorted(news_dir.glob("**/*.html")):
        if html_file.name == "index.html":
            continue
        
        # 提取年、月
        parts = html_file.relative_to(news_dir).parts
        if len(parts) >= 3:  # news/YYYY/MM/YYYY-MM-DD.html
            year = parts[0]
            month = parts[1]
            
            if year not in reports_by_year_month:
                reports_by_year_month[year] = {}
            if month not in reports_by_year_month[year]:
                reports_by_year_month[year][month] = []
            
            reports_by_year_month[year][month].append({
                'name': html_file.stem,  # YYYY-MM-DD
                'path': str(html_file.relative_to(news_dir))
            })
    
    # 生成 HTML
    html_content = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📊 AI助理財經新聞總覽 📈</title>
    <style>
        body { 
            font-family: 'Helvetica Neue', Arial, sans-serif; 
            line-height: 1.6; 
            margin: 0; 
            padding: 20px; 
            background-image: url('background.jpg');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-color: #121212;
            color: #e0e0e0;
        }
        .container {
            background: rgba(30, 30, 30, 0.9);
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
            border: 1px solid #333;
            width: 90%;
            margin: 0 auto;
        }
        @media (min-width: 768px) {
            .container { width: 60%; }
        }
        h1 { 
            color: #f0f0f0; 
            border-bottom: 2px solid #3498db; 
            padding-bottom: 10px; 
            font-size: 1.5em; 
        }
        .year-section {
            margin-top: 20px;
        }
        .collapsible { 
            cursor: pointer; 
            color: #5dade2; 
            font-weight: bold; 
            margin-bottom: 5px; 
            display: block; 
            padding: 10px 0; 
            font-size: 1.1em;
            user-select: none;
        }
        .collapsible:hover { color: #85c1e9; }
        .collapsible.year-header {
            font-size: 1.15em;
            margin-top: 10px;
        }
        .content { 
            display: none; 
            padding-left: 20px; 
            margin-bottom: 10px; 
        }
        .content.show { 
            display: block; 
        }
        .month-content {
            display: none;
            padding-left: 20px;
        }
        .month-content.show {
            display: block;
        }
        ul {
            list-style: none;
            padding: 0;
        }
        li { 
            margin: 8px 0; 
        }
        a { 
            text-decoration: none; 
            color: #5dade2; 
        }
        a:hover { 
            text-decoration: underline; 
            color: #85c1e9;
        }
        .back-link {
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #444;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 AI助理財經新聞總覽 📈</h1>
"""
    
    # 按年份倒序（最新的在前）
    for year in sorted(reports_by_year_month.keys(), reverse=True):
        year_id = f"year-{year}"
        html_content += f'        <div class="collapsible year-header" onclick="toggleYear(this)">▼ {year}年</div>\n'
        html_content += f'        <div class="content show">\n'
        
        # 按月份倒序
        for month in sorted(reports_by_year_month[year].keys(), reverse=True):
            month_id = f"month-{year}-{month}"
            html_content += f'            <div class="collapsible" onclick="toggleMonth(this)">▼ {month}月</div>\n'
            html_content += f'            <div class="month-content show">\n'
            html_content += f'                <ul>\n'
            
            # 按日期倒序（最新的在前）
            for report in sorted(reports_by_year_month[year][month], key=lambda x: x['name'], reverse=True):
                html_content += f'                    <li><a href="{report["path"]}">📄 {report["name"]} 財經晨報</a></li>\n'
            
            html_content += f'                </ul>\n'
            html_content += f'            </div>\n'
        
        html_content += f'        </div>\n'
    
    html_content += """        <div class="back-link">
            <a href="../index.html">← 回到首頁</a>
        </div>
    </div>

    <script>
        function toggleYear(el) {
            var content = el.nextElementSibling;
            if (content.classList.contains('show')) {
                content.classList.remove('show');
                el.innerHTML = el.innerHTML.replace("▼", "▶");
            } else {
                content.classList.add('show');
                el.innerHTML = el.innerHTML.replace("▶", "▼");
            }
        }
        
        function toggleMonth(el) {
            var content = el.nextElementSibling;
            if (content.classList.contains('show')) {
                content.classList.remove('show');
                el.innerHTML = el.innerHTML.replace("▼", "▶");
            } else {
                content.classList.add('show');
                el.innerHTML = el.innerHTML.replace("▶", "▼");
            }
        }
        
        // 預設展開最新年份和月份
        window.addEventListener('load', function() {
            let years = document.querySelectorAll('.year-header');
            if (years.length > 0) {
                // 最新年份預設為展開狀態（已由 CSS 設定）
            }
        });
    </script>
</body>
</html>
"""
    
    # 寫入 index 檔案
    index_path = Path(repo_path) / "news" / "index.html"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ news/index.html 已更新")

def git_push(date: str, repo_path: str = "/tmp/hermes-Stock-Report"):
    """提交並推送到 GitHub"""
    
    os.chdir(repo_path)
    os.system("git add .")
    os.system(f'git commit -m "feat: Add daily report for {date}"')
    result = os.system("git push origin main")
    
    if result == 0:
        print(f"✅ 已推送到 GitHub")
    else:
        print(f"⚠️ 推送失敗，請檢查網路或認證")

# ===== 主程式 =====

if __name__ == "__main__":
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 示例 AI 回應
    sample_ai_response = """
    【利多】台股站穩年線 台股技術面突破關鍵支撐，籌碼面轉強，法人買超續增。
    【利多】AI 晶片需求旺 英偉達財報超預期，帶動全球 AI 需求，台灣半導體漲幅 2.5%。
    【利空】Fed 維持鷹派 美聯準官員暗示延後降息，美債殖利率上升，科技股承壓。
    
    * 超微推出新一代 EPYC 處理器，與英偉達競爭加劇。
    * 歐央行6月維持利率，7月可能降息 0.25%。
    * 台灣 Q2 出口成長 8.2%，超越市場預期。
    """
    
    # 執行流程
    analysis = extract_market_analysis(sample_ai_response)
    html = generate_html_report(today, analysis)
    save_report(html, today)
    update_news_index(today)
    git_push(today)
    
    print(f"\n✅ 財經晨報工作流完成！")
    print(f"📊 報告: https://edward0714.github.io/hermes-Stock-Report/news/index.html")
