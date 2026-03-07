import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

def run_news():
    # رابط RSS الجزيرة
    rss_url = "https://www.aljazeera.net/aljazeerarss/a7c29549-5861-4fd5-9111-30ae11157f46/4f9136ff-6060-466d-ad02-e2b216972740"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(rss_url, headers=headers)
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        news_cards = ""
        for item in items[:15]:
            title = item.title.text
            link = item.link.text
            
            # --- نظام متطور لجلب الصورة ---
            img_url = ""
            # البحث في media:content
            media = item.find('media:content')
            if media and media.get('url'):
                img_url = media['url']
            # البحث في enclosure
            if not img_url:
                enclosure = item.find('enclosure')
                if enclosure and enclosure.get('url'):
                    img_url = enclosure['url']
            # البحث داخل الوصف (Description) كحل أخير
            if not img_url:
                desc_soup = BeautifulSoup(item.description.text if item.description else "", "html.parser")
                img_tag = desc_soup.find('img')
                if img_tag and img_tag.get('src'):
                    img_url = img_tag['src']
            
            # إذا لم توجد صورة نضع صورة افتراضية فخمة
            if not img_url:
                img_url = "https://www.aljazeera.net/wp-content/uploads/2023/12/Interactive-Map-1702555513.jpg"

            # تنظيف الوصف
            description = item.description.text if item.description else ""
            clean_desc = re.sub('<[^<]+?>', '', description)[:140] + "..."
            
            news_cards += f'''
            <article class="aj-card">
                <a href="{link}" target="_blank" style="text-decoration:none; color:inherit;">
                    <div class="aj-img-wrapper">
                        <img src="{img_url}" alt="{title}" onerror="this.src='https://via.placeholder.com/600x400?text=News'">
                    </div>
                    <div class="aj-content">
                        <h2 class="aj-title">{title}</h2>
                        <p class="aj-desc">{clean_desc}</p>
                        <div class="aj-meta">
                            <span>🕒 {datetime.now().strftime("%d/%m/%Y")}</span>
                        </div>
                    </div>
                </a>
            </article>'''

        now = datetime.now().strftime("%Y-%m-%d | %I:%M %p")
        
        # قالب الـ HTML (نفس التصميم الفخم)
        html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>النضال نيوز | أخبار العالم</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {{ --main: #041e42; --gold: #ff9900; }}
        body {{ background: #fdfdfd; color: #333; font-family: 'Noto Kufi Arabic', sans-serif; margin: 0; }}
        header {{ border-bottom: 4px solid var(--main); padding: 15px 5%; background: #fff; display: flex; justify-content: space-between; align-items: center; position: sticky; top:0; z-index:1000; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
        .logo {{ font-size: 26px; font-weight: bold; color: var(--main); text-decoration: none; }}
        .logo span {{ color: var(--gold); }}
        .container {{ max-width: 1100px; margin: 30px auto; padding: 0 20px; display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 35px; }}
        .aj-card {{ background: #fff; border-bottom: 2px solid #eee; padding-bottom: 15px; transition: 0.3s; }}
        .aj-card:hover {{ transform: translateY(-5px); }}
        .aj-img-wrapper {{ width: 100%; height: 210px; overflow: hidden; border-radius: 8px; }}
        .aj-img-wrapper img {{ width: 100%; height: 100%; object-fit: cover; }}
        .aj-title {{ font-size: 19px; line-height: 1.5; margin: 15px 0; color: var(--main); font-weight: 700; }}
        .aj-desc {{ font-size: 14px; color: #666; line-height: 1.7; }}
        .aj-meta {{ font-size: 12px; color: #999; margin-top: 10px; }}
        footer {{ background: var(--main); color: #fff; text-align: center; padding: 30px; margin-top: 50px; }}
    </style>
</head>
<body>
    <header>
        <a href="#" class="logo">النضال <span>نيوز</span></a>
        <div style="font-size: 11px; color: #888;">آخر تحديث: {now}</div>
    </header>
    <main class="container">{news_cards}</main>
    <footer><p>النضال نيوز &copy; 2026 | المصدر: الجزيرة نت</p></footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)
            
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__": run_news()
