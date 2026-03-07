import requests
from bs4 import BeautifulSoup
from datetime import datetime
import random

def run_news():
    # مصدر الأخبار: RT Arabic العام لضمان تنوع المحتوى (سياسي، رياضي، تقني)
    rss_url = "https://arabic.rt.com/rss/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        # رابطك الربحي الذكي من Adsterra
        my_direct_link = "https://www.effectivegatecpm.com/t3rvmzpu?key=26330eef1cb397212db567d1385dc0b9"
        
        response = requests.get(rss_url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        # عناوين شريط "آخر الأخبار" العلوي
        ticker_text = " • ".join([item.title.text for item in items[:12]])

        news_html = ""
        for i, item in enumerate(items[:24]):
            title = item.title.text
            news_url = item.link.text
            img_url = item.find('enclosure').get('url') if item.find('enclosure') else "https://via.placeholder.com/600x400/003366/ffffff?text=Alhadath24"
            
            # تصميم البلوك الاحترافي (نفس توزيع كووورة)
            news_html += f'''
            <div class="news-card">
                <a href="{my_direct_link}" target="_blank" class="main-link">
                    <div class="img-wrapper">
                        <img src="{img_url}" loading="lazy">
                        <div class="label">حصري</div>
                    </div>
                    <div class="card-body">
                        <h2 class="title">{title}</h2>
                        <div class="card-meta">📅 اليوم | ⏱️ الآن</div>
                    </div>
                </a>
                <div class="card-footer">
                    <a href="{news_url}" target="_blank" class="details-btn">تفاصيل الخبر 🔗</a>
                </div>
            </div>'''
            
            # إعلان "تغطية خاصة" بعد كل 4 أخبار لزيادة الـ CTR
            if (i + 1) % 4 == 0:
                news_html += f'''
                <div class="news-card ad-special">
                    <a href="{my_direct_link}" target="_blank" class="main-link">
                        <div class="ad-container">
                            <div class="ad-tag">موصى به ⭐</div>
                            <h3>بث مباشر وتغطية شاملة لأهم أحداث الساعة</h3>
                            <p>اضغط هنا للمشاهدة والمتابعة اللحظية</p>
                            <div class="ad-button-f">دخول الآن</div>
                        </div>
                    </a>
                </div>'''

        now = datetime.now().strftime("%Y-%m-%d | %I:%M %p")
        
        html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>الحدث 24 - Alhadath 24</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --primary: #003366; --accent: #d32f2f; --bg: #f4f4f4; }}
        body {{ background: var(--bg); font-family: 'Cairo', sans-serif; margin: 0; padding-top: 110px; }}
        
        /* تصميم الهيدر (فخامة كووورة) */
        header {{ background: #fff; padding: 12px 6%; position: fixed; top: 0; width: 100%; z-index: 2000; display: flex; justify-content: space-between; align-items: center; border-bottom: 4px solid var(--primary); box-sizing: border-box; box-shadow: 0 2px 15px rgba(0,0,0,0.1); }}
        .logo {{ font-size: 26px; font-weight: 900; color: var(--primary); text-decoration: none; }}
        .logo span {{ color: var(--accent); }}
        
        /* شريط عاجل السفلي (ستايل القنوات العالمية) */
        .ticker-bar {{ background: #fff; border-bottom: 1px solid #ddd; position: fixed; top: 65px; width: 100%; height: 40px; display: flex; align-items: center; z-index: 1500; overflow: hidden; }}
        .ticker-label {{ background: var(--accent); color: #fff; padding: 0 25px; height: 100%; display: flex; align-items: center; font-weight: 900; font-size: 14px; z-index: 10; box-shadow: 5px 0 10px rgba(0,0,0,0.1); }}
        .ticker-text-move {{ white-space: nowrap; animation: scroll 60s linear infinite; color: #444; font-size: 14px; font-weight: 700; }}
        @keyframes scroll {{ from {{ transform: translateX(100%); }} to {{ transform: translateX(-100%); }} }}

        /* حاوية الأخبار (Grid) */
        .main-grid {{ max-width: 1200px; margin: 20px auto; display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 15px; padding: 0 15px; }}
        
        .news-card {{ background: #fff; border: 1px solid #e0e0e0; border-radius: 4px; overflow: hidden; transition: 0.3s; display: flex; flex-direction: column; }}
        .news-card:hover {{ transform: translateY(-5px); box-shadow: 0 8px 20px rgba(0,0,0,0.1); }}
        
        .img-wrapper {{ position: relative; height: 190px; overflow: hidden; }}
        .img-wrapper img {{ width: 100%; height: 100%; object-fit: cover; transition: 0.5s; }}
        .news-card:hover .img-wrapper img {{ transform: scale(1.08); }}
        .label {{ position: absolute; top: 10px; right: 10px; background: var(--accent); color: #fff; padding: 3px 12px; font-size: 11px; font-weight: bold; border-radius: 2px; }}
        
        .card-body {{ padding: 15px; flex-grow: 1; }}
        .title {{ font-size: 17px; font-weight: 700; color: #222; margin: 0; line-height: 1.6; height: 55px; overflow: hidden; }}
        .card-meta {{ font-size: 11px; color: #888; margin-top: 15px; border-top: 1px solid #f9f9f9; padding-top: 10px; }}
        
        .card-footer {{ background: #fcfcfc; padding: 10px 15px; border-top: 1px solid #eee; }}
        .details-btn {{ text-decoration: none; color: var(--primary); font-size: 12px; font-weight: bold; }}

        /* ستايل الإعلان الفخم */
        .ad-special {{ background: #fffdf2; border: 1px solid #ffe082; }}
        .ad-container {{ padding: 30px 20px; text-align: center; }}
        .ad-tag {{ color: #f57c00; font-weight: 900; font-size: 12px; margin-bottom: 10px; }}
        .ad-button-f {{ background: var(--primary); color: #fff; padding: 10px 30px; border-radius: 4px; display: inline-block; margin-top: 15px; font-weight: 900; }}
        
        .main-link {{ text-decoration: none; color: inherit; }}

        @media (max-width: 600px) {{ 
            .main-grid {{ grid-template-columns: 1fr; }} 
            header {{ padding: 10px 20px; }}
            body {{ padding-top: 100px; }}
        }}
    </style>
</head>
<body>
    <header>
        <a href="#" class="logo">الحدث <span>24</span> 📡</a>
        <div style="font-size: 11px; background: #f0f0f0; padding: 5px 10px; border-radius: 4px; color: #555;">{now}</div>
    </header>

    <div class="ticker-bar">
        <div class="ticker-label">عاجل</div>
        <div class="ticker-text-move">{ticker_text}</div>
    </div>

    <div class="main-grid">{news_html}</div>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(html)
            
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__": run_news()
