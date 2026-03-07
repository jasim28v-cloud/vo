import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import shutil

def run_news():
    rss_url = "https://arabic.rt.com/rss/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    ad_link = "https://www.effectivegatecpm.com/t3rvmzpu?key=26330eef1cb397212db567d1385dc0b9"
    
    try:
        # إنشاء مجلد للأخبار إذا لم يكن موجوداً
        if os.path.exists('news'): shutil.rmtree('news')
        os.makedirs('news')

        response = requests.get(rss_url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        ticker_text = " • ".join([item.title.text for item in items[:12]])
        now_time = datetime.now().strftime("%Y-%m-%d %I:%M %p")

        news_cards = ""
        for i, item in enumerate(items[:30]):
            title = item.title.text
            desc = item.description.text if item.description else "تابع التفاصيل الكاملة عبر موقعنا.."
            img_url = item.find('enclosure').get('url') if item.find('enclosure') else "https://via.placeholder.com/800x500"
            file_name = f"news/article-{i}.html"

            # 1. إنشاء صفحة الخبر المنفصلة (التفاصيل الكاملة)
            article_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>{title} - الحدث 24</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Cairo', sans-serif; background: #f0f2f5; margin: 0; padding: 20px; }}
        header {{ background: #003366; color: white; padding: 15px; text-align: center; font-weight: 900; font-size: 24px; position: sticky; top: 0; }}
        .article-container {{ max-width: 800px; margin: 20px auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }}
        .article-container img {{ width: 100%; border-radius: 8px; }}
        .article-container h1 {{ color: #003366; font-size: 24px; margin: 20px 0; }}
        .article-container p {{ line-height: 1.8; color: #444; font-size: 18px; }}
        .ad-banner {{ background: #fff3cd; border: 1px dashed #ffeeba; padding: 20px; text-align: center; margin: 20px 0; cursor: pointer; }}
        .ad-btn {{ background: #d32f2f; color: white; padding: 12px 30px; display: inline-block; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 15px; animation: pulse 2s infinite; }}
        @keyframes pulse {{ 0% {{transform: scale(1);}} 50% {{transform: scale(1.05);}} 100% {{transform: scale(1);}} }}
        .back-home {{ display: block; text-align: center; margin-top: 30px; color: #003366; text-decoration: none; font-weight: bold; }}
    </style>
</head>
<body>
    <header onclick="location.href='../index.html'">الحدث <span>24</span> 📡</header>
    <div class="article-container">
        <img src="{img_url}">
        <h1>{title}</h1>
        
        <div class="ad-banner" onclick="window.open('{ad_link}', '_blank')">
            <p style="margin:0; color:#856404;">بث مباشر للأحداث الجارية وتحديثات لحظية</p>
            <a href="{ad_link}" target="_blank" class="ad-btn">دخول البث الآن</a>
        </div>

        <p>{desc}</p>
        
        <div class="ad-banner" onclick="window.open('{ad_link}', '_blank')" style="background:#e8f4fd; border-color:#b8daff;">
            <p style="margin:0; color:#004085;">قد يهمك أيضاً: توقعات الخبراء لما سيحدث خلال الساعات القادمة</p>
            <a href="{ad_link}" target="_blank" class="ad-btn" style="background:#003366;">إضغط للتفاصيل</a>
        </div>

        <a href="../index.html" class="back-home">← العودة للرئيسية</a>
    </div>
</body>
</html>'''
            with open(file_name, 'w', encoding='utf-8') as f: f.write(article_html)

            # 2. إنشاء كرت الخبر للصفحة الرئيسية
            news_cards += f'''
            <div class="news-card">
                <a href="{file_name}">
                    <div class="img-box">
                        <img src="{img_url}">
                        <div class="tag">عاجل</div>
                    </div>
                    <div class="card-text">
                        <h2>{title}</h2>
                        <span class="date">⏱️ {now_time}</span>
                    </div>
                </a>
            </div>'''

        # 3. إنشاء الصفحة الرئيسية (index.html)
        main_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>الحدث 24 - بوابة الأخبار العالمية</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{ --p: #003366; --a: #d32f2f; }}
        body {{ background: #f5f5f5; font-family: 'Cairo', sans-serif; margin: 0; padding-top: 110px; }}
        header {{ background: #fff; border-bottom: 4px solid var(--p); padding: 12px 5%; position: fixed; top: 0; width: 100%; z-index: 1000; display: flex; justify-content: space-between; align-items: center; box-sizing: border-box; }}
        .logo {{ font-size: 26px; font-weight: 900; color: var(--p); text-decoration: none; }}
        .logo span {{ color: var(--a); }}
        .bell {{ font-size: 22px; cursor: pointer; animation: r 2s infinite; }}
        @keyframes r {{ 0%,100% {{transform:rotate(0)}} 10%,30% {{transform:rotate(15deg)}} 20%,40% {{transform:rotate(-15deg)}} }}
        
        .ticker {{ background: white; border-bottom: 1px solid #ddd; position: fixed; top: 65px; width: 100%; height: 40px; display: flex; align-items: center; z-index: 900; }}
        .ticker-l {{ background: var(--a); color: white; padding: 0 15px; height: 100%; display: flex; align-items: center; font-weight: bold; font-size: 14px; }}
        .ticker-t {{ white-space: nowrap; animation: s 60s linear infinite; font-size: 14px; font-weight: bold; color: #444; }}
        @keyframes s {{ from {{transform:translateX(100%)}} to {{transform:translateX(-100%)}} }}

        .grid {{ max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 15px; padding: 15px; }}
        .news-card {{ background: white; border: 1px solid #ddd; border-radius: 5px; overflow: hidden; transition: 0.3s; }}
        .news-card:hover {{ transform: translateY(-5px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
        .news-card a {{ text-decoration: none; color: inherit; }}
        .img-box {{ height: 190px; position: relative; }}
        .img-box img {{ width: 100%; height: 100%; object-fit: cover; }}
        .tag {{ position: absolute; top: 10px; right: 10px; background: var(--a); color: white; padding: 2px 10px; font-size: 11px; font-weight: bold; }}
        .card-text {{ padding: 15px; }}
        .card-text h2 {{ font-size: 16px; margin: 0; line-height: 1.5; color: #222; }}
        .date {{ font-size: 11px; color: #999; display: block; margin-top: 10px; }}
        @media (max-width: 600px) {{ .grid {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <header>
        <div style="display:flex; align-items:center; gap:15px;">
            <a href="#" class="logo">الحدث <span>24</span></a>
            <div class="bell" onclick="window.open('{ad_link}', '_blank')">🔔</div>
        </div>
        <div style="font-size:11px; color:#666;">{now_time}</div>
    </header>
    <div class="ticker">
        <div class="ticker-l">آخر الأخبار</div>
        <div class="ticker-t">{ticker_text}</div>
    </div>
    <div class="grid">{news_cards}</div>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(main_html)
            
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__": run_news()
