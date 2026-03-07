import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
import shutil
import random

def run_news():
    rss_url = "https://arabic.rt.com/rss/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    ad_link = "https://www.effectivegatecpm.com/t3rvmzpu?key=26330eef1cb397212db567d1385dc0b9"
    
    try:
        if os.path.exists('news'): shutil.rmtree('news')
        os.makedirs('news')

        response = requests.get(rss_url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'xml')
        items = soup.find_all('item')
        
        ticker_text = " • ".join([item.title.text for item in items[:12]])
        now_time = datetime.now().strftime("%Y-%m-%d %I:%M %p")

        news_cards = ""
        for i, item in enumerate(items[:25]):
            title = item.title.text
            desc = item.description.text if item.description else "تغطية مستمرة لأهم الأحداث العالمية والمحلية على مدار الساعة."
            img_url = item.find('enclosure').get('url') if item.find('enclosure') else "https://via.placeholder.com/800x500"
            file_name = f"news/article-{i}.html"

            # إنشاء صفحة الخبر المنفصلة مع إعلانات داخلية وصور
            article_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Cairo', sans-serif; background: #f4f7f6; margin: 0; padding: 0; }}
        header {{ background: #003366; color: white; padding: 15px; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 1000; }}
        .container {{ max-width: 800px; margin: 20px auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); }}
        .main-img {{ width: 100%; border-radius: 8px; margin-bottom: 20px; }}
        h1 {{ color: #003366; font-size: 26px; line-height: 1.4; }}
        .meta-info {{ color: #888; font-size: 13px; margin-bottom: 20px; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
        .content {{ line-height: 1.9; color: #333; font-size: 18px; }}
        
        /* إعلانات داخل المنشور */
        .internal-ad {{ background: #fff9e6; border: 2px dashed #f1c40f; border-radius: 8px; margin: 25px 0; padding: 15px; text-align: center; cursor: pointer; }}
        .ad-img {{ width: 100%; max-height: 250px; object-fit: cover; border-radius: 5px; margin-bottom: 10px; }}
        .ad-title {{ color: #d32f2f; font-weight: 900; font-size: 18px; margin-bottom: 5px; display: block; }}
        .ad-btn {{ background: #003366; color: white; padding: 10px 25px; display: inline-block; text-decoration: none; border-radius: 5px; font-weight: bold; margin-top: 10px; }}
        
        .footer-ad {{ background: #003366; color: white; padding: 30px; border-radius: 8px; text-align: center; margin-top: 30px; cursor: pointer; }}
        .back-btn {{ display: block; text-align: center; margin-top: 20px; color: #003366; text-decoration: none; font-weight: bold; }}
    </style>
</head>
<body>
    <header onclick="location.href='../index.html'">
        <div style="font-weight:900; font-size:20px;">الحدث <span>24</span></div>
        <div style="font-size:12px;">مباشر 📡</div>
    </header>

    <div class="container">
        <h1>{title}</h1>
        <div class="meta-info">نشر في: {now_time} | القسم: أخبار العالم</div>
        <img src="{img_url}" class="main-img">
        
        <div class="content">
            {desc}
            
            <div class="internal-ad" onclick="window.open('{ad_link}', '_blank')">
                <span class="ad-title">⚠️ خبر عاجل قيد التحديث</span>
                <img src="https://images.pexels.com/photos/158651/news-newsletter-newspaper-information-158651.jpeg?auto=compress&cs=tinysrgb&w=600" class="ad-img">
                <p>لمتابعة تفاصيل هذا الحدث بالفيديو والبث المباشر</p>
                <a href="{ad_link}" class="ad-btn">إضغط هنا للمشاهدة الآن</a>
            </div>

            استمراراً لتغطيتنا، أفادت المصادر أن العمل جارٍ على تحديث كافة البيانات المتعلقة بهذا الخبر الصادر منذ قليل. يمكنك دائماً العودة لصفحتنا الرئيسية لمتابعة آخر التطورات.

            <div class="internal-ad" onclick="window.open('{ad_link}', '_blank')" style="background: #eef2ff; border-color: #003366;">
                <span class="ad-title" style="color:#003366;">🔥 ترند الساعة الآن</span>
                <img src="https://images.pexels.com/photos/3183150/pexels-photo-3183150.jpeg?auto=compress&cs=tinysrgb&w=600" class="ad-img">
                <p>شاهد ما قاله المحللون عن هذا الخبر وتوقعاتهم القادمة</p>
                <a href="{ad_link}" class="ad-btn" style="background:#d32f2f;">دخول التغطية الكاملة</a>
            </div>
        </div>

        <div class="footer-ad" onclick="window.open('{ad_link}', '_blank')">
            <h2>هل تريد استلام تنبيهات الأخبار العاجلة؟</h2>
            <p>سجل الآن مجاناً لتصلك آخر أخبار الحدث 24 فور صدورها</p>
            <div class="ad-btn" style="background:white; color:#003366;">تفعيل التنبيهات مجاناً</div>
        </div>

        <a href="../index.html" class="back-btn">← العودة للرئيسية</a>
    </div>
</body>
</html>'''
            with open(file_name, 'w', encoding='utf-8') as f: f.write(article_html)

            news_cards += f'''
            <div class="news-card">
                <a href="{file_name}">
                    <div class="img-box">
                        <img src="{img_url}">
                        <div class="tag">تفاصيل الخبر</div>
                    </div>
                    <div class="card-text">
                        <h2>{title}</h2>
                        <span class="date">⏱️ {now_time}</span>
                    </div>
                </a>
            </div>'''

        # إنشاء الصفحة الرئيسية
        main_html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>الحدث 24 - Alhadath 24</title>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ background: #f0f2f5; font-family: 'Cairo', sans-serif; margin: 0; padding-top: 110px; }}
        header {{ background: #fff; border-bottom: 4px solid #003366; padding: 10px 5%; position: fixed; top: 0; width: 100%; z-index: 1000; display: flex; justify-content: space-between; align-items: center; box-sizing: border-box; }}
        .logo {{ font-size: 26px; font-weight: 900; color: #003366; text-decoration: none; }}
        .logo span {{ color: #d32f2f; }}
        .ticker {{ background: #fff; border-bottom: 1px solid #ddd; position: fixed; top: 60px; width: 100%; height: 40px; display: flex; align-items: center; z-index: 900; }}
        .ticker-l {{ background: #d32f2f; color: white; padding: 0 15px; height: 100%; display: flex; align-items: center; font-weight: bold; font-size: 14px; }}
        .ticker-t {{ white-space: nowrap; animation: s 60s linear infinite; font-size: 14px; font-weight: bold; color: #444; }}
        @keyframes s {{ from {{transform:translateX(100%)}} to {{transform:translateX(-100%)}} }}
        .grid {{ max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 15px; padding: 15px; }}
        .news-card {{ background: white; border-radius: 6px; overflow: hidden; border: 1px solid #ddd; transition: 0.3s; }}
        .news-card:hover {{ transform: translateY(-5px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
        .news-card a {{ text-decoration: none; color: inherit; }}
        .img-box {{ height: 190px; position: relative; }}
        .img-box img {{ width: 100%; height: 100%; object-fit: cover; }}
        .tag {{ position: absolute; top: 10px; right: 10px; background: #d32f2f; color: white; padding: 2px 10px; font-size: 11px; font-weight: bold; border-radius: 3px; }}
        .card-text {{ padding: 15px; }}
        .card-text h2 {{ font-size: 16px; margin: 0; line-height: 1.5; color: #222; }}
        @media (max-width: 600px) {{ .grid {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <header><a href="#" class="logo">الحدث <span>24</span></a><div style="font-size:20px; cursor:pointer;" onclick="window.open('{ad_link}','_blank')">🔔</div></header>
    <div class="ticker"><div class="ticker-l">عاجل</div><div class="ticker-t">{ticker_text}</div></div>
    <div class="grid">{news_cards}</div>
</body>
</html>'''

        with open("index.html", "w", encoding="utf-8") as f: f.write(main_html)
            
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__": run_news()
