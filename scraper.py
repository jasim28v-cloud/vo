import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

def run_news():
    rss_url = "https://arabic.rt.com/rss/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(rss_url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        news_cards = ""
        for item in items[:15]:
            title = item.title.text
            link = item.link.text
            img_url = item.find('enclosure').get('url') if item.find('enclosure') else "https://via.placeholder.com/600x400"
            description = item.description.text if item.description else ""
            clean_desc = re.sub('<[^<]+?>', '', description)[:130] + "..."
            
            news_cards += f'''
            <article class="news-card">
                <a href="{link}" target="_blank" style="text-decoration:none; color:inherit;">
                    <div class="img-wrapper"><img src="{img_url}" loading="lazy"></div>
                    <div class="card-content">
                        <h2 class="card-title">{title}</h2>
                        <p class="card-text">{clean_desc}</p>
                        <div class="card-footer">
                            <span>🕒 {datetime.now().strftime("%I:%M %p")}</span>
                            <span class="badge">عاجل</span>
                        </div>
                    </div>
                </a>
            </article>'''

        now = datetime.now().strftime("%Y-%m-%d | %I:%M %p")
        
        # كود الإعلان المصلح ليظهر كصورة (Advertica Tag)
        advertica_ad = '''
        <div class="ad-box">
            <ins style="width: 300px;height: 250px;display:inline-block" 
                 data-width="300" 
                 data-height="250" 
                 class="b29f4471aa2" 
                 data-domain="//data527.click" 
                 data-affquery="/e3435b2a507722939b6f/29f4471aa2/placementName=default">
            </ins>
            <script src="//data527.click/js/responsive.js" async></script>
        </div>
        '''

        html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>النضال نيوز | Alnidal News</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {{ background: #f0f2f5; font-family: 'Cairo', sans-serif; margin: 0; padding: 0; }}
        header {{ background: #fff; border-bottom: 4px solid #c00; padding: 15px 5%; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 1000; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .logo {{ font-size: 28px; font-weight: 800; color: #1a1a1a; text-decoration: none; }}
        .logo span {{ color: #c00; }}
        .ad-container {{ text-align: center; margin: 25px auto; padding: 10px; }}
        .ad-box {{ display: inline-block; background: #fff; border: 1px solid #eee; border-radius: 8px; padding: 5px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }}
        .container {{ max-width: 1100px; margin: 20px auto; padding: 0 15px; display: grid; grid-template-columns: repeat(auto-fill, minmax(330px, 1fr)); gap: 25px; }}
        .news-card {{ background: #fff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.08); transition: 0.3s; height: 100%; display: flex; flex-direction: column; }}
        .news-card:hover {{ transform: translateY(-5px); box-shadow: 0 8px 25px rgba(0,0,0,0.15); }}
        .img-wrapper img {{ width: 100%; height: 210px; object-fit: cover; }}
        .card-content {{ padding: 20px; flex-grow: 1; }}
        .card-title {{ font-size: 19px; line-height: 1.5; margin: 0 0 12px 0; color: #000; font-weight: 700; }}
        .card-text {{ font-size: 14px; color: #555; line-height: 1.6; height: 65px; overflow: hidden; }}
        .card-footer {{ display: flex; justify-content: space-between; align-items: center; margin-top: 15px; padding-top: 10px; border-top: 1px solid #eee; font-size: 12px; color: #888; }}
        .badge {{ background: #ffeeee; color: #c00; padding: 3px 10px; border-radius: 4px; font-weight: bold; }}
        footer {{ background: #1a1a1a; color: #fff; text-align: center; padding: 40px 0; margin-top: 50px; }}
        @media (max-width: 600px) {{ .container {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <header>
        <a href="#" class="logo">النضال <span>نيوز</span></a>
        <div style="font-size: 11px; color: #666;">تحديث: {now}</div>
    </header>

    <div class="ad-container">
        <p style="font-size: 10px; color: #999; margin-bottom: 8px;">إعلان مروج</p>
        {advertica_ad}
    </div>

    <main class="container">
        {news_cards}
    </main>

    <div class="ad-container">
        {advertica_ad}
    </div>

    <footer>
        <p>النضال نيوز &copy; 2026</p>
        <p style="font-size: 12px; opacity: 0.6;">جميع الحقوق محفوظة | مصدر الأخبار: RT Arabic</p>
    </footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)
            
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__": run_news()
