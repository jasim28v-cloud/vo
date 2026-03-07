import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

def run_news():
    rss_url = "https://arabic.rt.com/rss/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        # رابطك الإعلاني المباشر
        my_direct_link = "https://www.effectivegatecpm.com/t3rvmzpu?key=26330eef1cb397212db567d1385dc0b9"
        
        response = requests.get(rss_url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        ticker_items = " • ".join([item.title.text for item in items[:10]])
        news_html = ""
        
        for i, item in enumerate(items[:20]):
            title = item.title.text
            news_url = item.link.text
            img_element = item.find('enclosure')
            img_url = img_element.get('url') if img_element else "https://via.placeholder.com/800x500/1a1a1a/ffffff?text=ALHADATH+24"
            
            # استخراج وصف نظيف
            description = item.description.text if item.description else ""
            clean_desc = re.sub('<[^<]+?>', '', description)[:100] + "..."

            news_html += f'''
            <article class="premium-card">
                <div class="badge">حصري</div>
                <div class="card-image">
                    <img src="{img_url}" loading="lazy" alt="news">
                    <div class="image-overlay"></div>
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

            # حقن إعلان "تغطية خاصة" كل 4 أخبار بتصميم مغناطيسي
            if (i + 1) % 4 == 0:
                news_html += f'''
                <div class="special-ad-block">
                    <a href="{my_direct_link}" target="_blank" class="ad-link">
                        <div class="ad-inner">
                            <span class="live-pulse">LIVE</span>
                            <h3>تغطية حية ومباشرة للأحداث المتسارعة</h3>
                            <p>انقر هنا للدخول إلى غرفة البث المباشر</p>
                            <div class="ad-cta">دخول سريع ⚡</div>
                        </div>
                    </a>
                </div>'''

        now = datetime.now().strftime("%Y-%m-%d")
        
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>الحدث 24 | Alhadath Premium</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;800;900&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg: #0f1215; --card-bg: #181d23; --text: #e0e0e0;
            --primary: #e63946; --accent: #457b9d; --gold: #ffb703;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ background: var(--bg); font-family: 'Cairo', sans-serif; color: var(--text); line-height: 1.6; overflow-x: hidden; }}
        
        /* Header & Ticker */
        header {{ background: rgba(24, 29, 35, 0.95); backdrop-filter: blur(10px); padding: 15px 5%; position: fixed; top: 0; width: 100%; z-index: 1000; border-bottom: 2px solid var(--primary); display: flex; justify-content: space-between; align-items: center; }}
        .logo {{ font-size: 28px; font-weight: 900; color: #fff; text-decoration: none; letter-spacing: -1px; }}
        .logo span {{ color: var(--primary); }}
        
        .ticker-wrap {{ position: fixed; top: 70px; width: 100%; background: var(--primary); color: #fff; overflow: hidden; height: 35px; display: flex; align-items: center; z-index: 999; }}
        .ticker-title {{ background: #000; padding: 0 20px; font-weight: 800; font-size: 13px; z-index: 2; height: 100%; display: flex; align-items: center; }}
        .ticker-scroll {{ white-space: nowrap; animation: scroll 40s linear infinite; font-weight: 600; font-size: 14px; }}
        @keyframes scroll {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-150%); }} }}

        /* Grid System */
        .container {{ max-width: 1300px; margin: 140px auto 50px; padding: 0 20px; display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 30px; }}

        /* Premium Card */
        .premium-card {{ background: var(--card-bg); border-radius: 15px; overflow: hidden; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); position: relative; border: 1px solid #2a3139; }}
        .premium-card:hover {{ transform: translateY(-10px); border-color: var(--primary); box-shadow: 0 15px 35px rgba(230, 57, 70, 0.2); }}
        .badge {{ position: absolute; top: 15px; left: 15px; background: var(--primary); color: #fff; padding: 4px 12px; font-size: 11px; font-weight: 800; border-radius: 50px; z-index: 5; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }}
        
        .card-image {{ position: relative; height: 220px; }}
        .card-image img {{ width: 100%; height: 100%; object-fit: cover; transition: 0.6s; }}
        .premium-card:hover .card-image img {{ transform: scale(1.1); }}
        .image-overlay {{ position: absolute; bottom: 0; width: 100%; height: 50%; background: linear-gradient(transparent, rgba(0,0,0,0.8)); }}

        .card-content {{ padding: 20px; }}
        .card-title {{ font-size: 19px; font-weight: 800; color: #fff; margin-bottom: 12px; line-height: 1.4; }}
        .card-snippet {{ font-size: 14px; color: #a0a0a0; margin-bottom: 20px; }}
        
        .meta-data {{ display: flex; justify-content: space-between; font-size: 12px; color: var(--gold); margin-bottom: 20px; font-weight: 600; }}

        .action-area {{ display: flex; gap: 10px; }}
        .btn-main {{ flex: 2; background: var(--primary); color: #fff; text-decoration: none; text-align: center; padding: 10px; border-radius: 8px; font-weight: 800; font-size: 14px; transition: 0.3s; }}
        .btn-sub {{ flex: 1; background: #2a3139; color: #ccc; text-decoration: none; text-align: center; padding: 10px; border-radius: 8px; font-size: 12px; display: flex; align-items: center; justify-content: center; }}
        .btn-main:hover {{ filter: brightness(1.2); }}

        /* Special Ad Block */
        .special-ad-block {{ grid-column: 1 / -1; background: linear-gradient(45deg, #1d242c, #2c3e50); border-radius: 15px; padding: 40px; text-align: center; border: 2px dashed var(--gold); position: relative; }}
        .ad-link {{ text-decoration: none; color: inherit; }}
        .live-pulse {{ position: absolute; top: 20px; right: 20px; background: #ff0000; color: #fff; padding: 5px 15px; border-radius: 5px; font-weight: 900; animation: pulse 1.5s infinite; }}
        @keyframes pulse {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.5; }} 100% {{ opacity: 1; }} }}
        .ad-cta {{ margin-top: 20px; background: var(--gold); color: #000; display: inline-block; padding: 12px 40px; border-radius: 50px; font-weight: 900; }}

        @media (max-width: 768px) {{
            .container {{ grid-template-columns: 1fr; margin-top: 130px; }}
            .logo {{ font-size: 22px; }}
        }}
    </style>
</head>
<body>
    <header>
        <a href="#" class="logo">الحدث <span>24</span></a>
        <div style="font-size: 12px; color: #888; font-weight: 600;">{now}</div>
    </header>
    <div class="ticker-wrap">
        <div class="ticker-title">عاجل الآن</div>
        <div class="ticker-scroll">{ticker_items}</div>
    </div>
    <main class="container">
        {news_html}
    </main>
    <footer style="text-align:center; padding: 50px; color: #555; border-top: 1px solid #222;">
        <p>جميع الحقوق محفوظة لشبكة الحدث 24 &copy; 2026</p>
    </footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(full_html)
        print("Done: Shadow Core optimized index.html has been generated.")
            
    except Exception as e:
        print(f"Error encountered: {e}")

if __name__ == "__main__":
    run_news()
