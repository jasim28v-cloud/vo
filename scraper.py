import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

def run_news():
    rss_url = "https://arabic.rt.com/rss/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        # الرابط الجديد الذي زودتني به لضمان عمل الإعلانات
        my_direct_link = "https://www.effectivegatecpm.com/ywn2a0wz7?key=7433561eca4a0920fafc9d653809bab2"
        
        response = requests.get(rss_url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        
        # استخدام lxml لمعالجة البيانات بسرعة كما هو محدد في ملف التشغيل الآلي
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        ticker_items = " • ".join([item.title.text for item in items[:12]])
        news_html = ""
        
        for i, item in enumerate(items[:20]):
            title = item.title.text
            news_url = item.link.text
            img_element = item.find('enclosure')
            img_url = img_element.get('url') if img_element else "https://via.placeholder.com/800x500/1a1a1a/ffffff?text=ALHADATH+24"
            
            description = item.description.text if item.description else ""
            clean_desc = re.sub('<[^<]+?>', '', description)[:110] + "..."

            news_html += f'''
            <article class="premium-card">
                <div class="badge">{"عاجل" if i < 3 else "حصري"}</div>
                <div class="card-image">
                    <a href="{my_direct_link}" target="_blank">
                        <img src="{img_url}" loading="lazy" alt="news">
                    </a>
                </div>
                <div class="card-content">
                    <h2 class="card-title">{title}</h2>
                    <p class="card-snippet">{clean_desc}</p>
                    <div class="meta-data">
                        <span>🕒 {datetime.now().strftime("%I:%M %p")}</span>
                        <span>🔥 ترند الآن</span>
                    </div>
                    <div class="action-area">
                        <a href="{my_direct_link}" target="_blank" class="btn-main">اقرأ الخبر كاملاً</a>
                        <a href="{news_url}" target="_blank" class="btn-sub">المصدر الأصلي</a>
                    </div>
                </div>
            </article>'''

            # توزيع إعلاني ذكي لزيادة نسبة النقر CTR
            if (i + 1) % 4 == 0:
                news_html += f'''
                <div class="special-ad-block">
                    <a href="{my_direct_link}" target="_blank" class="ad-link">
                        <div class="ad-inner">
                            <span class="live-pulse">LIVE</span>
                            <h3>تغطية مباشرة لأهم أحداث الساعة</h3>
                            <p>انقر هنا للمتابعة اللحظية عبر البث المباشر</p>
                            <div class="ad-cta">دخول سريع ⚡</div>
                        </div>
                    </a>
                </div>'''

        now_date = datetime.now().strftime("%Y-%m-%d")
        
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>الحدث 24 | Alhadath News</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #0d1117; --card: #161b22; --text: #f0f6fc;
            --primary: #f85149; --accent: #58a6ff; --gold: #f2cc60;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ background: var(--bg); font-family: 'Cairo', sans-serif; color: var(--text); padding-top: 130px; }}
        header {{ background: rgba(13, 17, 23, 0.95); backdrop-filter: blur(12px); padding: 15px 5%; position: fixed; top: 0; width: 100%; z-index: 1000; border-bottom: 2px solid var(--primary); display: flex; justify-content: space-between; align-items: center; }}
        .logo {{ font-size: 26px; font-weight: 900; color: #fff; text-decoration: none; }}
        .logo span {{ color: var(--primary); }}
        .ticker-wrap {{ position: fixed; top: 75px; width: 100%; background: var(--primary); color: #fff; overflow: hidden; height: 35px; display: flex; align-items: center; z-index: 999; }}
        .ticker-title {{ background: #000; padding: 0 15px; font-weight: 800; font-size: 13px; z-index: 2; height: 100%; display: flex; align-items: center; }}
        .ticker-scroll {{ white-space: nowrap; animation: scroll 45s linear infinite; font-weight: 600; }}
        @keyframes scroll {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-180%); }} }}
        .container {{ max-width: 1200px; margin: 0 auto 50px; padding: 0 15px; display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 20px; }}
        .premium-card {{ background: var(--card); border-radius: 12px; overflow: hidden; transition: 0.3s; border: 1px solid #30363d; position: relative; }}
        .premium-card:hover {{ transform: translateY(-5px); border-color: var(--primary); box-shadow: 0 8px 24px rgba(0,0,0,0.5); }}
        .badge {{ position: absolute; top: 12px; left: 12px; background: var(--primary); color: #fff; padding: 3px 12px; font-size: 11px; font-weight: 800; border-radius: 4px; z-index: 5; }}
        .card-image {{ height: 200px; overflow: hidden; border-bottom: 1px solid #30363d; }}
        .card-image img {{ width: 100%; height: 100%; object-fit: cover; transition: 0.5s; }}
        .card-content {{ padding: 20px; }}
        .card-title {{ font-size: 18px; font-weight: 800; color: #fff; margin-bottom: 10px; line-height: 1.5; }}
        .card-snippet {{ font-size: 14px; color: #8b949e; margin-bottom: 15px; }}
        .meta-data {{ display: flex; justify-content: space-between; font-size: 11px; color: var(--gold); margin-bottom: 15px; font-weight: 600; }}
        .action-area {{ display: flex; gap: 8px; }}
        .btn-main {{ flex: 2; background: var(--primary); color: #fff; text-decoration: none; text-align: center; padding: 10px; border-radius: 6px; font-weight: 800; font-size: 14px; }}
        .btn-sub {{ flex: 1; background: #21262d; color: #c9d1d9; text-decoration: none; text-align: center; padding: 10px; border-radius: 6px; font-size: 12px; border: 1px solid #30363d; }}
        .special-ad-block {{ grid-column: 1 / -1; background: #161b22; border-radius: 12px; padding: 30px; text-align: center; border: 2px dashed #30363d; }}
        .ad-link {{ text-decoration: none; color: inherit; }}
        .live-pulse {{ background: #ff3e3e; color: #fff; padding: 2px 10px; border-radius: 4px; font-size: 11px; font-weight: 900; animation: blink 1.2s infinite; }}
        @keyframes blink {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.5; }} 100% {{ opacity: 1; }} }}
        .ad-cta {{ margin-top: 15px; background: var(--gold); color: #000; display: inline-block; padding: 8px 30px; border-radius: 4px; font-weight: 900; }}
        @media (max-width: 600px) {{ .container {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <header>
        <a href="#" class="logo">الحدث <span>24</span></a>
        <div style="font-size: 11px; color: #8b949e;">📅 {now_date}</div>
    </header>
    <div class="ticker-wrap">
        <div class="ticker-title">عاجل الآن</div>
        <div class="ticker-scroll">{ticker_items}</div>
    </div>
    <main class="container">{news_html}</main>
    <footer style="text-align:center; padding: 30px; color: #484f58; font-size: 12px;">
        <p>Alhadath 24 &copy; 2026 | Automated by Alhadath24-Bot</p>
    </footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(full_html)
            
    except Exception as e:
        print(f"Shadow Core Execution Error: {e}")

if __name__ == "__main__":
    run_news()
