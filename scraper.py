import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

def run_news():
    # تم تغيير الرابط ليجلب أخبار الفن والمشاهير بدلاً من الأخبار العامة
    rss_url = "https://arabic.rt.com/rss/news/entertainment/"
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ar-IQ,ar;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://www.google.com/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Sec-Ch-Ua': '"Google Chrome";v="124", "Not:A-Brand";v="8", "Chromium";v="124"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"'
}
    
    try:
        # الرابط المباشر الخاص بك
        my_direct_link = "https://data527.click/21330bf1d025d41336e6/57154ac610/?placementName=default"
        
        # أكواد الإعلانات الإضافية
        ad_ins_code = '<ins style="width: 300px;height:250px" data-width="300" data-height="250" class="g2fb0b4c321" data-domain="//data527.click" data-affquery="/e3435b2a507722939b6f/2fb0b4c321/?placementName=default"><script src="//data527.click/js/responsive.js" async></script></ins>'
        ad_script_code = '<script type="text/javascript" src="//data527.click/129ba2282fccd3392338/b1a648bd38/?placementName=default"></script>'
        
        response = requests.get(rss_url, headers=headers, timeout=20)
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        ticker_items = " • ".join([item.title.text for item in items[:12]])
        news_html = ""
        
        for i, item in enumerate(items[:20]):
            title = item.title.text
            news_url = item.link.text
            img_element = item.find('enclosure')
            img_url = img_element.get('url') if img_element else "https://via.placeholder.com/800x500/1a1a1a/ffffff?text=CELEBRITY+NEWS"
            
            description = item.description.text if item.description else ""
            clean_desc = re.sub('<[^<]+?>', '', description)[:110] + "..."

            news_html += f'''
            <article class="glass-card">
                <div class="badge">{"ترند الآن" if i < 3 else "مشاهير"}</div>
                <div class="card-image">
                    <a href="{my_direct_link}" target="_blank">
                        <img src="{img_url}" loading="lazy" alt="news">
                    </a>
                </div>
                <div class="card-content">
                    <h2 class="card-title">{title}</h2>
                    <p class="card-snippet">{clean_desc}</p>
                    <div class="meta-data">
                        <span>🕒 {datetime.now().strftime("%I:%M %p")}</span>
                        <span class="trending-fire">🔥 حصري</span>
                    </div>
                    <div class="action-area">
                        <a href="{my_direct_link}" target="_blank" class="btn-prime">شاهد التفاصيل</a>
                        <a href="{news_url}" target="_blank" class="btn-outline">المصدر</a>
                    </div>
                </div>
            </article>'''

            if (i + 1) % 4 == 0:
                news_html += f'''
                <div class="ad-slot-wrapper">
                    {ad_ins_code}
                </div>'''

        now_date = datetime.now().strftime("%Y-%m-%d")
        
        full_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>مشاهير ترند | عالم النجوم</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{
            --glass-bg: rgba(255, 255, 255, 0.07);
            --glass-border: rgba(255, 255, 255, 0.15);
            --primary-accent: #f093fb;
            --danger-accent: #f5576c;
            --text-main: #ffffff;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            background: linear-gradient(135deg, #2d3436, #000000);
            background-attachment: fixed;
            background-size: cover;
            font-family: 'Cairo', sans-serif; 
            color: var(--text-main); 
            padding-top: 150px;
        }}
        
        header {{ 
            background: rgba(0, 0, 0, 0.6); 
            backdrop-filter: blur(25px); 
            padding: 15px 5%; 
            position: fixed; top: 0; width: 100%; z-index: 1000; 
            border-bottom: 1px solid var(--glass-border);
            display: flex; justify-content: space-between; align-items: center; 
        }}
        .logo {{ font-size: 26px; font-weight: 900; color: #fff; text-decoration: none; }}
        .logo span {{ color: var(--danger-accent); text-shadow: 0 0 10px var(--danger-accent); }}
        
        .ticker-wrap {{ 
            position: fixed; top: 85px; width: 100%; 
            background: rgba(245, 87, 108, 0.85); 
            backdrop-filter: blur(10px);
            color: #fff; overflow: hidden; height: 40px; 
            display: flex; align-items: center; z-index: 999;
        }}
        .ticker-title {{ background: #000; padding: 0 20px; font-weight: 900; z-index: 2; height: 100%; display: flex; align-items: center; font-size: 13px; }}
        .ticker-scroll {{ white-space: nowrap; animation: scroll 60s linear infinite; }}
        @keyframes scroll {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-250%); }} }}

        .container {{ max-width: 1250px; margin: 0 auto 50px; padding: 0 20px; display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 30px; }}
        
        .glass-card {{ 
            background: var(--glass-bg); 
            backdrop-filter: blur(20px);
            border-radius: 25px; overflow: hidden; 
            transition: 0.4s; 
            border: 1px solid var(--glass-border); 
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }}
        .glass-card:hover {{ transform: scale(1.03); border-color: var(--primary-accent); }}
        
        .badge {{ position: absolute; top: 15px; left: 15px; background: var(--danger-accent); color: #fff; padding: 4px 15px; font-size: 11px; font-weight: 700; border-radius: 10px; z-index: 5; }}
        .card-image {{ height: 210px; overflow: hidden; }}
        .card-image img {{ width: 100%; height: 100%; object-fit: cover; }}
        
        .card-content {{ padding: 25px; }}
        .card-title {{ font-size: 19px; font-weight: 700; color: #fff; margin-bottom: 12px; line-height: 1.5; }}
        .card-snippet {{ font-size: 13px; color: #ccc; margin-bottom: 20px; }}
        
        .meta-data {{ display: flex; justify-content: space-between; font-size: 11px; color: var(--primary-accent); margin-bottom: 20px; border-top: 1px solid var(--glass-border); padding-top: 15px; }}
        
        .action-area {{ display: flex; gap: 10px; }}
        .btn-prime {{ flex: 2; background: linear-gradient(90deg, #f5576c, #f093fb); color: #fff; text-decoration: none; text-align: center; padding: 12px; border-radius: 12px; font-weight: 700; }}
        .btn-outline {{ flex: 1; background: rgba(255,255,255,0.05); color: #fff; text-decoration: none; text-align: center; padding: 12px; border-radius: 12px; font-size: 12px; border: 1px solid var(--glass-border); }}
        
        .ad-slot-wrapper {{ grid-column: 1 / -1; display: flex; justify-content: center; padding: 20px; background: rgba(255,255,255,0.02); border-radius: 20px; border: 1px dashed var(--glass-border); }}
        
        footer {{ text-align: center; padding: 40px; color: rgba(255,255,255,0.4); font-size: 12px; border-top: 1px solid var(--glass-border); }}
        
        @media (max-width: 600px) {{ .container {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    {ad_script_code} <header>
        <a href="#" class="logo">مشاهير <span>ترند</span></a>
        <div style="font-size: 12px; letter-spacing: 1px;">📅 {now_date}</div>
    </header>

    <div class="ticker-wrap">
        <div class="ticker-title">آخر أخبار النجوم</div>
        <div class="ticker-scroll">{ticker_items}</div>
    </div>

    <main class="container">
        {news_html}
    </main>

    <footer>
        <p>Celebrity Trend Dashboard &copy; 2026</p>
    </footer>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(full_html)
        print("تم التحديث! موقع 'مشاهير ترند' جاهز الآن مع الإعلانات.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_news()
