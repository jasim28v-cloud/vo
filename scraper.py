import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

def run_news():
    rss_url = "https://arabic.rt.com/rss/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        my_direct_link = "https://www.effectivegatecpm.com/t3rvmzpu?key=26330eef1cb397212db567d1385dc0b9"

        response = requests.get(rss_url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        news_cards = ""
        for item in items[:15]:
            title = item.title.text
            news_url = item.link.text
            img_url = item.find('enclosure').get('url') if item.find('enclosure') else "https://via.placeholder.com/600x400"
            description = item.description.text if item.description else ""
            clean_desc = re.sub('<[^<]+?>', '', description)[:110] + "..."
            
            news_cards += f'''
            <article class="news-card">
                <a href="{my_direct_link}" target="_blank" style="text-decoration:none; color:inherit;">
                    <div class="img-wrapper">
                        <img src="{img_url}" loading="lazy">
                    </div>
                    <div class="card-content">
                        <h2 class="card-title">{title}</h2>
                        <p class="card-text">{clean_desc}</p>
                    </div>
                </a>
                <div class="card-footer">
                    <a href="{my_direct_link}" target="_blank" class="source-btn">تـفاصيل الخبر 📖</a>
                    <span style="font-size:10px; color:#999;">🕒 {datetime.now().strftime("%I:%M %p")}</span>
                </div>
            </article>'''

        now = datetime.now().strftime("%Y-%m-%d | %I:%M %p")
        
        html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>النضال نيوز | Alnidal News</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {{ background: #f0f2f5; font-family: 'Cairo', sans-serif; margin: 0; }}
        header {{ background: #fff; border-bottom: 4px solid #c00; padding: 15px 5%; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 1000; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .logo {{ font-size: 26px; font-weight: 800; color: #1a1a1a; text-decoration: none; }}
        .logo span {{ color: #c00; }}
        .container {{ max-width: 1100px; margin: 30px auto; padding: 0 15px; display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 25px; }}
        .news-card {{ background: #fff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.08); transition: 0.3s; display: flex; flex-direction: column; cursor: pointer; }}
        .news-card:hover {{ transform: translateY(-5px); box-shadow: 0 8px 25px rgba(0,0,0,0.15); }}
        .img-wrapper img {{ width: 100%; height: 200px; object-fit: cover; }}
        .card-content {{ padding: 15px; flex-grow: 1; }}
        .card-title {{ font-size: 17px; line-height: 1.5; margin: 0 0 10px 0; color: #000; font-weight: 700; }}
        .card-text {{ font-size: 13px; color: #555; line-height: 1.6; height: 60px; overflow: hidden; }}
        .card-footer {{ padding: 15px; border-top: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; background: #fafafa; }}
        .source-btn {{ background: #c00; color: #fff; padding: 6px 15px; border-radius: 6px; text-decoration: none; font-size: 12px; font-weight: bold; transition: 0.3s; }}
        .source-btn:hover {{ background: #1a1a1a; }}
        footer {{ background: #1a1a1a; color: #fff; text-align: center; padding: 30px; margin-top: 50px; }}
        @media (max-width: 600px) {{ .container {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <header>
        <a href="#" class="logo">النضال <span>نيوز</span></a>
        <div style="font-size: 11px; color: #666;">تحديث: {now}</div>
    </header>
    <main class="container">{news_cards}</main>
    <footer>
        <p>النضال نيوز &copy; 2026</p>
    </footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)
            
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__": run_news()
