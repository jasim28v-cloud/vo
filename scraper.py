import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import random

def run_news():
    rss_url = "https://arabic.rt.com/rss/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        # رابطك الربحي المباشر
        my_direct_link = "https://www.effectivegatecpm.com/t3rvmzpu?key=26330eef1cb397212db567d1385dc0b9"

        response = requests.get(rss_url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        breaking_titles = " • ".join([item.title.text for item in items[:10]])

        news_html = ""
        for i, item in enumerate(items[:16]):
            title = item.title.text
            news_url = item.link.text
            img_url = item.find('enclosure').get('url') if item.find('enclosure') else "https://via.placeholder.com/600x400"
            
            # خبر نظامي (عند الضغط يفتح الإعلان)
            news_html += f'''
            <div class="news-item">
                <a href="{my_direct_link}" target="_blank" class="news-link">
                    <div class="image-container">
                        <img src="{img_url}" loading="lazy">
                        <span class="category-tag">أخبار عاجلة</span>
                    </div>
                    <div class="content">
                        <h2 class="news-title">{title}</h2>
                    </div>
                </a>
                <div class="news-footer">
                    <a href="{news_url}" target="_blank" class="source-link">اقرأ التفاصيل 🔗</a>
                </div>
            </div>'''
            
            # إضافة "مربع إعلاني صوري" جذاب بعد كل 3 أخبار
            if (i + 1) % 3 == 0:
                ad_images = [
                    "https://images.unsplash.com/photo-1526628953301-3e589a6a8b74?w=500", 
                    "https://images.unsplash.com/photo-1614680376593-902f74cf0d41?w=500"
                ]
                selected_ad_img = random.choice(ad_images)
                news_html += f'''
                <div class="news-item ad-box">
                    <a href="{my_direct_link}" target="_blank" class="news-link">
                        <div class="image-container">
                            <img src="{selected_ad_img}">
                            <span class="ad-label">إعلان ممول</span>
                        </div>
                        <div class="content">
                            <h2 class="news-title" style="color: #007bff; text-align:center;">إضغط هنا للحصول على المكافأة والتحميل المباشر</h2>
                            <div class="ad-button">عرض الآن</div>
                        </div>
                    </a>
                </div>'''

        now = datetime.now().strftime("%d/%m/%Y | %I:%M %p")
        
        html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>النضال نيوز | RT</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --rt-red: #da251d; --rt-dark: #1a1a1a; }}
        body {{ background: #eee; font-family: 'Cairo', sans-serif; margin: 0; padding-bottom: 60px; }}
        header {{ background: var(--rt-dark); color: white; padding: 10px 5%; display: flex; justify-content: space-between; align-items: center; border-bottom: 4px solid var(--rt-red); position: sticky; top: 0; z-index: 1000; }}
        .logo {{ font-size: 24px; font-weight: 900; }}
        .logo span {{ background: var(--rt-red); padding: 0 5px; }}
        .main-container {{ max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1px; background: #ccc; }}
        .news-item {{ background: white; display: flex; flex-direction: column; }}
        .image-container {{ position: relative; height: 180px; overflow: hidden; }}
        .image-container img {{ width: 100%; height: 100%; object-fit: cover; transition: 0.3s; }}
        .news-item:hover img {{ transform: scale(1.05); }}
        .category-tag {{ position: absolute; bottom: 0; right: 0; background: var(--rt-red); color: white; padding: 2px 10px; font-size: 11px; font-weight: bold; }}
        .ad-label {{ position: absolute; top: 0; left: 0; background: #28a745; color: white; padding: 2px 10px; font-size: 10px; }}
        .content {{ padding: 15px; flex-grow: 1; }}
        .news-title {{ font-size: 16px; font-weight: 700; line-height: 1.5; color: #111; margin: 0; }}
        .news-footer {{ padding: 10px; border-top: 1px solid #eee; text-align: left; }}
        .source-link {{ font-size: 11px; color: #c00; text-decoration: none; font-weight: bold; }}
        .news-link {{ text-decoration: none; color: inherit; }}
        
        /* ستايل زر الإعلان */
        .ad-button {{ background: #007bff; color: white; text-align: center; padding: 8px; margin-top: 10px; border-radius: 4px; font-weight: bold; font-size: 13px; }}
        .ad-box {{ border: 2px solid #007bff22; }}

        .breaking-news {{ position: fixed; bottom: 0; width: 100%; background: var(--rt-dark); color: white; height: 40px; display: flex; align-items: center; z-index: 2000; border-top: 2px solid var(--rt-red); overflow: hidden; }}
        .breaking-label {{ background: var(--rt-red); padding: 0 15px; height: 100%; display: flex; align-items: center; font-weight: 900; font-size: 14px; z-index: 2001; }}
        .breaking-text {{ white-space: nowrap; animation: scroll 60s linear infinite; padding-right: 100%; font-size: 13px; }}
        @keyframes scroll {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
        
        @media (max-width: 600px) {{ .main-container {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <header>
        <div class="logo"><span>RT</span> النضال نيوز</div>
        <div style="font-size: 11px;">تحديث: {now}</div>
    </header>

    <div class="main-container">{news_html}</div>

    <div class="breaking-news">
        <div class="breaking-label">عاجل</div>
        <div class="breaking-text">{breaking_titles}</div>
    </div>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(html)
            
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__": run_news()
