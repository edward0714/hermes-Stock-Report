# -*- coding: utf-8 -*-
import os, sys

path = '/tmp/hermes-Stock-Report/news/2026/07/2026-07-11.html'

# Read existing content
with open(path, 'r', encoding='utf-8') as f:
    existing = f.read()

# Build the sections to append
sections = []

# Weekly table section
sections.append('\n<div class="section">')
sections.append('<h2>\u7f8e\u80a1\u9031\u7dda 7/6 - 7/10</h2>')
sections.append('<table class="weekly-table">')
sections.append('<tr><th>\u6307\u6578</th><th>7/6(\u4e00)</th><th>7/7(\u4e8c)</th><th>7/8(\u4e09)</th><th>7/9(\u56db)</th><th>7/10(\u4e94)</th><th>\u9031\u6f32\u8dcc\u5e45</th></tr>')
sections.append('<tr><td>S&P 500</td><td>7,537</td><td>7,504</td><td>7,483</td><td>7,544</td><td><strong>7,575</strong></td><td><span class="badge badge-up">+0.50%</span></td></tr>')
sections.append('<tr><td>\u9053\u74ca\u5de5\u696d</td><td>53,056</td><td>52,925</td><td>52,348</td><td>52,487</td><td><strong>52,637</strong></td><td><span class="badge badge-down">-0.78%</span></td></tr>')
sections.append('<tr><td>\u90a3\u65af\u9054\u514b</td><td>26,121</td><td>25,819</td><td>25,871</td><td>26,207</td><td><strong>26,282</strong></td><td><span class="badge badge-up">+0.62%</span></td></tr>')
sections.append('<tr><td>\u8cbb\u57ce\u534a\u5c0e\u9ad4</td><td>12,900</td><td>12,301</td><td>12,575</td><td>12,960</td><td><strong>12,967</strong></td><td><span class="badge badge-up">+0.52%</span></td></tr>')
sections.append('</table>')
sections.append('<p style="margin-top:10px;color:#8888aa;font-size:0.9em;">\u672c\u9031\u7f8e\u80a1\u5448\u73fe\u5178\u578b\u7684V\u578b\u53cd\u8f49\u8d70\u52e2\u3002\u5468\u4e8c\u8cbb\u534a\u6307\u6578\u66b4\u8dcc4.65%\u5275\u4e0b\u672c\u9031\u4f4e\u9ede\uff0cS&P 500\u9031\u4e94\u6536\u57287,575.39\u9ede\u5275\u6b77\u53f2\u65b0\u9ad8\u3002VIX\u6050\u614c\u6307\u6578\u5f9e\u9031\u4e09\u9ad8\u9ede16.90\u56de\u843d\u81f315.03\u3002</p>')
sections.append('</div>')

# US Market section
sections.append('\n<div class="section">')
sections.append('<h2>\u7f8e\u80a1\u60c5\u884c (7\u670810\u65e5\u6536\u76e4)</h2>')
sections.append('<table class="market-table">')
sections.append('<tr><th>\u6307\u6578</th><th>\u6536\u76e4\u50f9</th><th>\u6f32\u8dcc</th><th>\u6f32\u8dcc\u5e45</th></tr>')
sections.append('<tr><td>\u9053\u74ca\u5de5\u696d\u6307\u6578</td><td>52,637.01</td><td class="up">+149.60</td><td><span class="badge badge-up">+0.29%</span></td></tr>')
sections.append('<tr><td>S&P 500</td><td>7,575.39</td><td class="up">+31.75</td><td><span class="badge badge-up">+0.42%</span></td></tr>')
sections.append('<tr><td>\u90a3\u65af\u9054\u514b\u6307\u6578</td><td>26,281.61</td><td class="up">+74.72</td><td><span class="badge badge-up">+0.29%</span></td></tr>')
sections.append('<tr><td>\u8cbb\u57ce\u534a\u5c0e\u9ad4</td><td>12,967.16</td><td class="up">+7.16</td><td><span class="badge badge-up">+0.06%</span></td></tr>')
sections.append('</table>')
sections.append('</div>')

# Stock table section
sections.append('\n<div class="section">')
sections.append('<h2>\u7f8e\u80a1\u91cd\u9ede\u500b\u80a1 (7\u670810\u65e5\u6536\u76e4)</h2>')
sections.append('<table class="market-table">')
sections.append('<tr><th>\u500b\u80a1</th><th>\u6536\u76e4\u50f9</th><th>\u6f32\u8dcc</th><th>\u6f32\u8dcc\u5e45</th></tr>')
sections.append('<tr><td>Meta</td><td>$669.21</td><td class="up">+37.73</td><td><span class="badge badge-up">+5.97%</span></td></tr>')
sections.append('<tr><td>\u8f1d\u9054(NVDA)</td><td>$210.96</td><td class="up">+8.18</td><td><span class="badge badge-up">+4.03%</span></td></tr>')
sections.append('<tr><td>\u61c9\u7528\u6750\u6599(AMAT)</td><td>$602.50</td><td class="up">+13.84</td><td><span class="badge badge-up">+2.35%</span></td></tr>')
sections.append('<tr><td>AMD</td><td>$557.89</td><td class="up">+11.17</td><td><span class="badge badge-up">+2.04%</span></td></tr>')
sections.append('<tr><td>\u7279\u65af\u62c9(TSLA)</td><td>$407.76</td><td class="up">+1.21</td><td><span class="badge badge-up">+0.30%</span></td></tr>')
sections.append('<tr><td>\u535a\u901a(AVGO)</td><td>$399.97</td><td class="down">-1.14</td><td><span class="badge badge-down">-0.28%</span></td></tr>')
sections.append('<tr><td>Apple</td><td>$315.32</td><td class="down">-0.90</td><td><span class="badge badge-down">-0.28%</span></td></tr>')
sections.append('<tr><td>\u53f0\u7a4d\u96fb ADR</td><td>$434.11</td><td class="down">-2.85</td><td><span class="badge badge-down">-0.65%</span></td></tr>')
sections.append('<tr><td>\u4e9e\u99ac\u905c(AMZN)</td><td>$245.34</td><td class="down">-1.70</td><td><span class="badge badge-down">-0.69%</span></td></tr>')
sections.append('<tr><td>Google(GOOGL)</td><td>$357.18</td><td class="down">-1.71</td><td><span class="badge badge-down">-0.48%</span></td></tr>')
sections.append('<tr><td>\u7f8e\u5149(MU)</td><td>$979.30</td><td class="down">-12.34</td><td><span class="badge badge-down">-1.24%</span></td></tr>')
sections.append('<tr><td>ASML</td><td>$1,797.32</td><td class="down">-6.93</td><td><span class="badge badge-down">-0.38%</span></td></tr>')
sections.append('</table>')
sections.append('</div>')

# Taiwan stock section
sections.append('\n<div class="section">')
sections.append('<h2>\u53f0\u80a1\u60c5\u884c (7\u67089\u65e5\u6536\u76d8, \u5468\u4e94\u53f0\u98a8\u5047\u4f11\u5e02)</h2>')
sections.append('<table class="market-table">')
sections.append('<tr><th>\u6307\u6578</th><th>\u6536\u76e4\u50f9</th><th>\u6f32\u8dcc</th><th>\u6f32\u8dcc\u5e45</th></tr>')
sections.append('<tr><td>\u52a0\u6b0a\u6307\u6578</td><td>45,354.61</td><td class="down">-379.80</td><td><span class="badge badge-down">-0.83%</span></td></tr>')
sections.append('<tr><td>\u53f0\u7a4d\u96fb</td><td>2,415.00</td><td class="down">-50.00</td><td><span class="badge badge-down">-2.03%</span></td></tr>')
sections.append('<tr><td>\u806f\u767c\u79d1</td><td>3,925.00</td><td class="down">-70.00</td><td><span class="badge badge-down">-1.75%</span></td></tr>')
sections.append('<tr><td>\u9d3b\u6d77</td><td>237.50</td><td class="flat">0.00</td><td><span class="badge badge-flat">0.00%</span></td></tr>')
sections.append('<tr><td>\u53f0\u9054\u96fb</td><td>1,880.00</td><td class="down">-5.00</td><td><span class="badge badge-down">-0.27%</span></td></tr>')
sections.append('<tr><td>\u5bcc\u90a6\u91d1</td><td>124.50</td><td class="down">-1.50</td><td><span class="badge badge-down">-1.19%</span></td></tr>')
sections.append('</table>')
sections.append('</div>')

# Commodities section
sections.append('\n<div class="section">')
sections.append('<h2>\u539f\u7269\u6599\u3001\u532f\u5e02\u8207\u52a0\u5bc6\u8ca8\u5e63</h2>')
sections.append('<table class="market-table">')
sections.append('<tr><th>\u5546\u54c1\u8207\u532f\u7387</th><th>\u6700\u65b0\u5831\u50f9</th><th>\u6f32\u8dcc</th><th>\u6f32\u8dcc\u5e45</th></tr>')
sections.append('<tr><td>\u897f\u5fb7\u5dde\u539f\u6cb9</td><td>$71.51</td><td class="down">-0.57</td><td><span class="badge badge-down">-0.79%</span></td></tr>')
sections.append('<tr><td>\u9ec3\u91d1\u671f\u8ca8</td><td>$4,128.90</td><td class="down">-1.70</td><td><span class="badge badge-down">-0.04%</span></td></tr>')
sections.append('<tr><td>\u7f8e\u5143\u6307\u6578</td><td>100.96</td><td class="up">+0.02</td><td><span class="badge badge-up">+0.02%</span></td></tr>')
sections.append('<tr><td>\u7f8e\u570b10\u5e74\u516c\u50b5\u6b96\u5229\u7387</td><td>4.569%</td><td class="up">+0.030</td><td><span class="badge badge-up">+0.66%</span></td></tr>')
sections.append('<tr><td>\u6bd4\u7279\u5e63</td><td>$64,011</td><td class="up">+818</td><td><span class="badge badge-up">+1.29%</span></td></tr>')
sections.append('</table>')
sections.append('</div>')

# News section
sections.append('\n<div class="section">')
sections.append('<h2>\u672c\u9031\u91cd\u9ede\u65b0\u805e</h2>')
sections.append('<ul class="news-list">')
sections.append('<li><strong>SK\u6d77\u529b\u58eb ADR\u90a3\u65af\u9054\u514b\u639b\u724c\u9996\u65e5\u52c1\u626c13%</strong><br><span class="source">SK Hynix 7\u670810\u65e5\u5728\u7f8e\u639b\u724c\uff0c\u9996\u65e5\u5927\u8dcc13%\u3002\u53f0\u80a1\u56e0\u98b1\u98a8\u4f11\u5e02\u672a\u80fd\u5373\u6642\u53cd\u6620\u5229\u591a\u3002</span></li>')
sections.append('<li><strong>AI\u8cc7\u91d1\u958b\u59cb\u8f2a\u52d5\uff0c\u6676\u7247\u80a1\u964d\u6eab\u3001\u8edf\u9ad4\u80a1\u63a5\u68d2</strong><br><span class="source">Meta\u5ba3\u5e03\u5099\u589eAI\u904b\u7b97\u5bb9\u91cf\uff0c\u5e36\u52d5\u80a1\u50f9\u98c6\u53475.97%\u3002\u9ad8\u76db\u6307\u51faAI\u6295\u8cc7\u6b63\u5f9e\u786c\u9ad4\u8f49\u5411\u8edf\u9ad4\u61c9\u7528\u3002</span></li>')
sections.append('<li><strong>\u7f8e\u570b6\u6708CPI\u5e74\u589e2.6%\u527517\u500b\u6708\u65b0\u9ad8</strong><br><span class="source">\u806f\u6e96\u6703\u964d\u606f\u9810\u671f\u518d\u53d7\u8003\u9a57\uff0c10\u5e74\u671f\u516c\u50b5\u6b96\u5229\u7387\u6500\u5347\u81f34.569%\u3002</span></li>')
sections.append('<li><strong>\u53f0\u80a1\u5468\u4e94\u98b1\u98a8\u5047\uff0c\u6295\u8cc7\u4eba\u932f\u5931\u5343\u5104\u53cd\u5f48\u884c\u60c5</strong><br><span class="source">\u8ca1\u5718\u4f30\u7b97\u53f0\u80a1\u82e5\u6b63\u5e38\u4ea4\u6613\uff0c\u52a0\u6b0a\u6307\u6578\u6709\u671b\u53cd\u5f48500-800\u9ede\u3002</span></li>')
sections.append('</ul>')
sections.append('</div>')

# Footer
sections.append('\n<a class="back-link" href="../../index.html">\u2190 \u56de\u5230\u6b77\u53f2\u5831\u544a\u5217\u8868</a>')
sections.append('<div class="footer">')
sections.append('\u6bcf\u65e5\u8ca1\u7d93\u6668\u5831\u7531AI\u81ea\u52d5\u7522\u751f - \u50c5\u4f9b\u53c3\u8003\uff0c\u6295\u8cc7\u6c7a\u7b56\u8acb\u81ea\u884c\u5224\u65b7<br>')
sections.append('2026\u5e747\u670811\u65e5')
sections.append('</div>')

sections.append('\n</div>')
sections.append('</body>')
sections.append('</html>')

# Append to file
with open(path, 'a', encoding='utf-8') as f:
    f.write('\n'.join(sections))

print(f'Final size: {os.path.getsize(path)} bytes')
print('Done!')
