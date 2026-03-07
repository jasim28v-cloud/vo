import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
import random

def run_news():
    rss_url = "https://arabic.rt.com/rss/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        # رابطك المباشر من Adsterra
        my_direct_link = "https://www.effectivegatecpm.com/t3rvmzpu?key=26330eef1cb397212db567d1385dc0b9"

        response = requests.get(rss_url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        # مصفوفة الإعلانات المربعة (نصممها لتشبه الأخبار الجذابة)
        ads_pool = [
            {"t": "احصل على أحدث الهواتف بخصم 90% لفترة محدودة", "i": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?q=80&w=500&auto=format&fit=crop"},
            {"t": "طريقة سحرية لربح 100 دولار يومياً من المنزل", "i": "https://images.unsplash.com/photo-1518458028785-8fbcd101ebb9?q=80&w=500&auto=format&fit=crop"},
            {"t": "أفضل التطبيقات المجانية لعام 2026 - حملها الآن", "i": "https://images.unsplash.com/photo-1611162617474-5b21e879e113?q=80&w=500&auto=format&fit=crop"}
        ]

        news_html = ""
        for i, item in enumerate(items[:12]):
            title = item.title.text
            news_url = item.link.text
            img_url = item.find('enclosure').get('url') if item.find('enclosure') else "https://via.placeholder.com/600x400"
            desc = re.sub('<[^<]+?>', '', item.description.text)[:100] + "..." if item.description else ""
            
            # إضافة خبر طبيعي
            news_html += f'''
            <div class="card">
                <a href="{my_direct_link}" target="_blank">
                    <img src="{img_url}" loading="lazy">
                    <div class="p-3">
                        <h3 class="title">{title}</h3>
                        <p class="text">{desc}</p>
                    </div>
                </a>
                <div class="footer"><a href="{news_url}" target="_blank" class="btn">التفاصيل</a></div>
            </div>'''
            
            # حقن "مربع إعلاني" جذاب بعد كل 3 أخبار
            if (i + 1) % 3 == 0:
                ad = random.choice(ads_pool)
                news_html += f'''
                <div class="card ad-card">
                    <a href="{my_direct_link}" target="_blank">
                        <div class="ad-badge">مُقترح لك</div>
                        <img src="{ad['i']}">
                        <div class="p-3">
                            <h3 class="title" style="color:#2980b9;">{ad['t']}</h3>
                            <p class="text">إعلان ممول - اضغط للمزيد من المعلومات والتفاصيل الحصرية.</p>
                        </div>
                    </a>
                </div>'''

        now = datetime.now().strftime("%I:%M %p")
        
        html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>النضال نيوز</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {{ background: #f0f2f5; font-family: 'Cairo', sans-serif; margin: 0; }}
        header {{ background: #fff; border-bottom: 3px solid #c00; padding: 15px 5%; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 99; }}
        .container {{ max-width: 1200px; margin: 20px auto; padding: 0 15px; display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; }}
        .card {{ background: #fff; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); display: flex; flex-direction: column; }}
        .ad-card {{ border: 2px solid #3498db; position: relative; }}
        .ad-badge {{ position: absolute; top: 10px; right: 10px; background: #3498db; color: #fff; padding: 2px 10px; border-radius: 4px; font-size: 10px; font-weight: bold; }}
        .card a {{ text-decoration: none; color: inherit; }}
        .card img {{ width: 100%; height: 180px; object-fit: cover; }}
        .p-3 {{ padding: 15px; flex-grow: 1; }}
        .title {{ font-size: 16px; margin: 0 0 10px 0; line-height: 1.4; }}
        .text {{ font-size: 12px; color: #666; height: 50px; overflow: hidden; }}
        .footer {{ padding: 10px; border-top: 1px solid #eee; display: flex; justify-content: space-between; }}
        .btn {{ background: #c00; color: #fff; padding: 4px 12px; border-radius: 4px; font-size: 12px; text-decoration: none; }}
        footer {{ background: #1a1a1a; color: #fff; text-align: center; padding: 20px; margin-top: 40px; }}
    </style>
</head>
<body>
    <header><div style="font-size: 24px; font-weight: bold;">النضال <span style="color:#c00;">نيوز</span></div><div style="font-size:12px;">{now}</div></header>
    <div class="container">{news_html}</div>
    <footer>النضال نيوز &copy; 2026</footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(html)
            
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__": run_news()
