import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

def run_news():
    rss_url = "https://www.aljazeera.net/aljazeerarss/a7c29549-5861-4fd5-9111-30ae11157f46/4f9136ff-6060-466d-ad02-e2b216972740"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(rss_url, headers=headers)
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        news_cards = ""
        for item in items[:12]:
            title = item.title.text
            link = item.link.text
            
            # سحب الصورة الأصلية
            media_content = item.find('media:content') or item.find('enclosure')
            img_url = media_content['url'] if media_content else ""
            
            # تنظيف الوصف وتحسينه
            description = item.description.text if item.description else ""
            clean_desc = re.sub('<[^<]+?>', '', description)[:150] + "..."
            
            news_cards += f'''
            <article class="aj-card">
                <a href="{link}" target="_blank" style="text-decoration:none; color:inherit;">
                    <div class="aj-img-wrapper">
                        <img src="{img_url}" alt="{title}" loading="lazy">
                    </div>
                    <div class="aj-content">
                        <h2 class="aj-title">{title}</h2>
                        <p class="aj-desc">{clean_desc}</p>
                        <div class="aj-meta">
                            <span class="aj-date">🕒 {datetime.now().strftime("%d/%m/%Y")}</span>
                        </div>
                    </div>
                </a>
            </article>'''

        now = datetime.now().strftime("%Y-%m-%d | %I:%M %p")
        
        html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>النضال نيوز | Alnidal News</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {{ --aj-blue: #041e42; --aj-gold: #ff9900; --bg: #ffffff; }}
        body {{ background: var(--bg); color: #333; font-family: 'Noto Kufi Arabic', sans-serif; margin: 0; padding: 0; }}
        
        /* Header style like Al Jazeera */
        header {{ border-bottom: 4px solid var(--aj-blue); padding: 15px 5%; display: flex; justify-content: space-between; align-items: center; background: #fff; position: sticky; top:0; z-index:100; }}
        .logo {{ font-size: 28px; font-weight: bold; color: var(--aj-blue); text-decoration: none; display: flex; align-items: center; gap: 10px; }}
        .logo span {{ color: var(--aj-gold); }}

        .container {{ max-width: 1100px; margin: 30px auto; padding: 0 20px; display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 40px; }}
        
        /* Card style inspired by the screenshot */
        .aj-card {{ background: #fff; transition: 0.3s; border-bottom: 1px solid #eee; padding-bottom: 20px; }}
        .aj-card:hover .aj-title {{ color: var(--aj-gold); }}
        
        .aj-img-wrapper {{ width: 100%; height: 220px; overflow: hidden; border-radius: 4px; background: #f0f0f0; }}
        .aj-img-wrapper img {{ width: 100%; height: 100%; object-fit: cover; transition: 0.5s; }}
        .aj-card:hover img {{ transform: scale(1.05); }}
        
        .aj-content {{ padding: 15px 0; }}
        .aj-title {{ font-size: 20px; line-height: 1.4; margin: 10px 0; color: var(--aj-blue); font-weight: 700; }}
        .aj-desc {{ font-size: 15px; color: #555; line-height: 1.6; margin-bottom: 15px; }}
        .aj-meta {{ font-size: 12px; color: #888; display: flex; align-items: center; gap: 10px; }}

        footer {{ background: var(--aj-blue); color: #fff; text-align: center; padding: 30px; margin-top: 60px; }}
        
        @media (max-width: 600px) {{
            .container {{ grid-template-columns: 1fr; }}
            .aj-title {{ font-size: 18px; }}
        }}
    </style>
</head>
<body>
    <header>
        <a href="#" class="logo">النضال <span>نيوز</span></a>
        <div style="font-size: 11px; color: #666;">آخر تحديث: {now}</div>
    </header>

    <main class="container">
        {news_cards}
    </main>

    <footer>
        <p>النضال نيوز - المصدر الأول للأخبار</p>
        <p style="font-size: 11px; opacity: 0.7;">نقل مباشر من الجزيرة نت &copy; 2026</p>
    </footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)
            
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__": run_news()
