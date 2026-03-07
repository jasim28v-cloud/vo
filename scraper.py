import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

def run_news():
    # رابط RSS الخاص بالجزيرة (الأخبار العربية)
    rss_url = "https://www.aljazeera.net/aljazeerarss/a7c29549-5861-4fd5-9111-30ae11157f46/4f9136ff-6060-466d-ad02-e2b216972740"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(rss_url, headers=headers)
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        news_cards = ""
        for item in items[:15]: # جلب آخر 15 خبر
            title = item.title.text
            link = item.link.text
            # استخراج الصورة من التاغ المخصص لها في RSS الجزيرة
            media_content = item.find('media:content') or item.find('enclosure')
            img_url = media_content['url'] if media_content else "https://via.placeholder.com/600x400?text=Alnidal+News"
            
            # تنظيف الوصف
            description = item.description.text if item.description else ""
            clean_desc = re.sub('<[^<]+?>', '', description)[:120] + "..."
            
            news_cards += f'''
            <div class="news-card">
                <div class="news-img" style="background-image: url('{img_url}')"></div>
                <div class="news-body">
                    <h3 class="news-title">{title}</h3>
                    <p class="news-desc">{clean_desc}</p>
                    <a href="{link}" target="_blank" class="read-more">اقرأ الخبر كاملاً</a>
                </div>
            </div>'''

        now = datetime.now().strftime("%Y-%m-%d | %I:%M %p")
        
        html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>النضال نيوز | Alnidal News</title>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {{ --main: #e11d48; --bg: #f8fafc; --text: #1e293b; }}
        body {{ background: var(--bg); color: var(--text); font-family: 'Tajawal', sans-serif; margin: 0; padding: 0; }}
        
        .navbar {{ background: white; padding: 15px 5%; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05); position: sticky; top: 0; z-index: 1000; }}
        .logo {{ font-size: 24px; font-weight: bold; color: var(--main); text-decoration: none; }}
        .update-time {{ font-size: 12px; color: #64748b; }}

        .hero {{ background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1495020689067-958852a7765e?auto=format&fit=crop&q=80&w=1000'); background-size: cover; background-position: center; color: white; padding: 60px 5%; text-align: center; margin-bottom: 40px; }}
        .hero h1 {{ font-size: 36px; margin: 0; }}

        .container {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 25px; padding: 0 5% 50px 5%; max-width: 1200px; margin: 0 auto; }}
        
        .news-card {{ background: white; border-radius: 15px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.05); transition: 0.3s; display: flex; flex-direction: column; }}
        .news-card:hover {{ transform: translateY(-8px); box-shadow: 0 10px 25px rgba(0,0,0,0.1); }}
        
        .news-img {{ height: 200px; background-size: cover; background-position: center; }}
        .news-body {{ padding: 20px; flex-grow: 1; display: flex; flex-direction: column; }}
        .news-title {{ font-size: 18px; margin: 0 0 12px 0; line-height: 1.5; color: #0f172a; }}
        .news-desc {{ font-size: 14px; color: #475569; margin-bottom: 20px; line-height: 1.6; flex-grow: 1; }}
        
        .read-more {{ display: inline-block; background: var(--main); color: white; text-decoration: none; padding: 10px 20px; border-radius: 8px; font-weight: bold; font-size: 14px; text-align: center; transition: 0.2s; }}
        .read-more:hover {{ opacity: 0.9; }}

        footer {{ background: #0f172a; color: white; text-align: center; padding: 40px 0; margin-top: 50px; }}
    </style>
</head>
<body>
    <div class="navbar">
        <a href="#" class="logo">النضال نيوز 📰</a>
        <div class="update-time">آخر تحديث: {now}</div>
    </div>

    <div class="hero">
        <h1>أخبار العالم بين يديك</h1>
        <p>تغطية شاملة ومباشرة من قلب الحدث</p>
    </div>

    <div class="container">
        {news_cards}
    </div>

    <footer>
        <p>النضال نيوز &copy; 2026</p>
        <p style="font-size: 12px; color: #94a3b8;">جميع الحقوق محفوظة - مصدر الأخبار: الجزيرة نت</p>
    </footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)
            
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__": run_news()
