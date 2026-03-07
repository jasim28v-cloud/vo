import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import random

def run_news():
    rss_url = "https://arabic.rt.com/rss/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        # رابطك الربحي
        my_direct_link = "https://www.effectivegatecpm.com/t3rvmzpu?key=26330eef1cb397212db567d1385dc0b9"

        response = requests.get(rss_url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        # إعلانات جذابة
        ads_pool = [
            {"t": "شاهد كيف تغيرت حياة هؤلاء بعد هذا التطبيق", "i": "https://images.unsplash.com/photo-1512428559087-560fa5ceab42?w=500"},
            {"t": "فرصة ذهبية للعمل عن بعد براتب مميز", "i": "https://images.unsplash.com/photo-1522202176988-66273c2fd55f?w=500"}
        ]

        news_html = ""
        for i, item in enumerate(items[:16]):
            title = item.title.text
            news_url = item.link.text
            img_url = item.find('enclosure').get('url') if item.find('enclosure') else "https://via.placeholder.com/600x400"
            
            # تصميم الخبر بستايل RT (عريض وبدون حواف دائرية مبالغ فيها)
            news_html += f'''
            <div class="news-item">
                <a href="{my_direct_link}" target="_blank" class="news-link">
                    <div class="image-container">
                        <img src="{img_url}" loading="lazy">
                        <span class="category-tag">أخبار</span>
                    </div>
                    <div class="content">
                        <h2 class="news-title">{title}</h2>
                    </div>
                </a>
                <div class="news-footer">
                    <a href="{news_url}" target="_blank" class="source-link">المصدر 🔗</a>
                </div>
            </div>'''
            
            # إضافة مربع إعلاني بعد كل 4 أخبار
            if (i + 1) % 4 == 0:
                ad = random.choice(ads_pool)
                news_html += f'''
                <div class="news-item ad-item">
                    <a href="{my_direct_link}" target="_blank" class="news-link">
                        <div class="image-container">
                            <img src="{ad['i']}">
                            <span class="ad-tag">موصى به</span>
                        </div>
                        <div class="content">
                            <h2 class="news-title" style="color: #0056b3;">{ad['t']}</h2>
                        </div>
                    </a>
                </div>'''

        now = datetime.now().strftime("%d/%m/%Y | %I:%M %p")
        
        html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>النضال نيوز | RT Style</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --rt-red: #da251d; --rt-dark: #1a1a1a; --rt-gray: #f4f4f4; }}
        body {{ background: var(--rt-gray); font-family: 'Cairo', sans-serif; margin: 0; padding: 0; color: #333; }}
        
        /* الهيدر بستايل RT */
        header {{ background: var(--rt-dark); color: white; padding: 10px 5%; display: flex; justify-content: space-between; align-items: center; border-bottom: 4px solid var(--rt-red); position: sticky; top: 0; z-index: 1000; }}
        .logo {{ font-size: 24px; font-weight: 900; letter-spacing: -1px; text-transform: uppercase; }}
        .logo span {{ background: var(--rt-red); padding: 0 5px; margin-right: 2px; }}
        .live-dot {{ height: 10px; width: 10px; background-color: var(--rt-red); border-radius: 50%; display: inline-block; margin-left: 5px; animation: blink 1s infinite; }}
        @keyframes blink {{ 0% {{opacity: 1;}} 50% {{opacity: 0.3;}} 100% {{opacity: 1;}} }}

        /* الشبكة الإخبارية */
        .main-container {{ max-width: 1200px; margin: 20px auto; padding: 0 15px; display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1px; background: #ddd; border: 1px solid #ddd; }}
        
        .news-item {{ background: white; transition: 0.3s; position: relative; display: flex; flex-direction: column; }}
        .news-item:hover {{ background: #f9f9f9; }}
        
        .image-container {{ position: relative; width: 100%; height: 180px; overflow: hidden; }}
        .image-container img {{ width: 100%; height: 100%; object-fit: cover; transition: 0.5s; }}
        .news-item:hover img {{ transform: scale(1.05); }}
        
        .category-tag {{ position: absolute; bottom: 0; right: 0; background: var(--rt-red); color: white; padding: 2px 10px; font-size: 12px; font-weight: bold; }}
        .ad-tag {{ position: absolute; top: 0; left: 0; background: #2ecc71; color: white; padding: 2px 10px; font-size: 10px; }}

        .content {{ padding: 15px; flex-grow: 1; }}
        .news-title {{ font-size: 17px; font-weight: 700; line-height: 1.4; margin: 0; color: #1a1a1a; }}
        
        .news-footer {{ padding: 10px 15px; border-top: 1px solid #eee; background: #fafafa; }}
        .source-link {{ font-size: 12px; color: #777; text-decoration: none; font-weight: bold; }}
        .source-link:hover {{ color: var(--rt-red); }}

        .news-link {{ text-decoration: none; color: inherit; height: 100%; display: flex; flex-direction: column; }}

        footer {{ background: var(--rt-dark); color: white; text-align: center; padding: 40px 0; margin-top: 40px; border-top: 5px solid var(--rt-red); }}
        
        @media (max-width: 600px) {{ .main-container {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <header>
        <div class="logo"><span>RT</span> النضال نيوز</div>
        <div style="font-size: 11px;"><span class="live-dot"></span> مباشر | {now}</div>
    </header>

    <div class="main-container">
        {news_html}
    </div>

    <footer>
        <div class="logo" style="margin-bottom:10px;"><span>RT</span> النضال نيوز</div>
        <p style="font-size: 12px; opacity: 0.7;">جميع الحقوق محفوظة © 2026</p>
    </footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(html)
            
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__": run_news()
