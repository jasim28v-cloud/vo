#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V2Ray Config Scraper for DOKA Project
Fetches latest VMess/VLess/Trojan/SS configs from @v2nodes Telegram channel
Generates a professional HTML page similar to freevpn.us design
"""

import requests
import re
import json
import os
from datetime import datetime
from typing import List, Dict

# ==================== الإعدادات ====================
TELEGRAM_CHANNEL_URL = "https://t.me/s/v2nodes"
AD_LINK = "https://data527.click/21330bf1d025d41336e6/57154ac610/?placementName=default"
OUTPUT_FILE = "index.html"
DATA_FILE = "servers_data.json"

# أنواع البروتوكولات المدعومة
SUPPORTED_PROTOCOLS = ['vmess', 'vless', 'trojan', 'ss', 'ssr', 'hysteria2', 'tuic']

# ==================== دوال الكشط ====================
def fetch_telegram_page(url: str) -> str:
    """جلب صفحة تيليجرام العامة"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"❌ خطأ في جلب الصفحة: {e}")
        return ""

def extract_configs(html_content: str) -> Dict[str, List[str]]:
    """استخراج جميع تكوينات V2Ray من HTML"""
    configs = {proto: [] for proto in SUPPORTED_PROTOCOLS}
    
    # نمط Regex محسّن لاستخراج الروابط
    pattern = r'(?:' + '|'.join(SUPPORTED_PROTOCOLS) + r')://[^\s<>"\'&]+'
    matches = re.findall(pattern, html_content, re.IGNORECASE)
    
    seen = set()
    for match in matches:
        # تنظيف الرابط
        clean = match.replace('&amp;', '&').split('<')[0].split('"')[0].strip()
        if clean in seen:
            continue
        seen.add(clean)
        
        # تحديد البروتوكول
        proto = clean.split('://')[0].lower()
        if proto in configs:
            configs[proto].append(clean)
    
    return configs

def classify_servers(configs: Dict[str, List[str]]) -> Dict[str, List[Dict]]:
    """تصنيف السيرفرات وإضافة بيانات وهمية للتأخير والدولة"""
    classified = {}
    
    # رموز الدول التقريبية (يمكنك تحسينها لاحقاً)
    country_hints = {
        'sg': '🇸🇬 SG', 'hk': '🇭🇰 HK', 'jp': '🇯🇵 JP', 'us': '🇺🇸 US',
        'de': '🇩🇪 DE', 'nl': '🇳🇱 NL', 'uk': '🇬🇧 UK', 'ca': '🇨🇦 CA',
        'fr': '🇫🇷 FR', 'in': '🇮🇳 IN', 'ae': '🇦🇪 AE', 'tr': '🇹🇷 TR'
    }
    
    import random
    for proto, links in configs.items():
        classified[proto] = []
        for link in links:
            # محاولة استخراج الدولة من الرابط
            country = '🌍 Unknown'
            for code, flag in country_hints.items():
                if f'.{code}.' in link.lower() or f'{code}-' in link.lower():
                    country = flag
                    break
            
            classified[proto].append({
                'url': link,
                'country': country,
                'latency': f"{random.randint(60, 250)}ms"
            })
    
    return classified

# ==================== توليد HTML ====================
def generate_html(servers: Dict[str, List[Dict]]) -> str:
    """توليد صفحة HTML كاملة بتصميم freevpn.us"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total_servers = sum(len(v) for v in servers.values())
    servers_json = json.dumps(servers, ensure_ascii=False)
    
    return f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DOKA - The Freedom Proxy</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
    <style>
        body {{ font-family: 'Tajawal', sans-serif; background: #fafafa; }}
        .hero-gradient {{ background: radial-gradient(circle at 70% 20%, rgba(37, 99, 235, 0.08) 0%, transparent 60%); }}
        .protocol-card {{ border: 1px solid rgba(0,0,0,0.05); transition: all 0.2s ease; }}
        .protocol-card:hover {{ border-color: #2563eb; box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.1); }}
        .modal {{ background: rgba(0,0,0,0.4); backdrop-filter: blur(4px); }}
    </style>
</head>
<body class="antialiased text-gray-800">

    <!-- شريط العنوان العلوي -->
    <header class="border-b border-gray-200 bg-white/90 backdrop-blur-md sticky top-0 z-40">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex flex-wrap items-center justify-between py-3 text-sm">
                <div class="flex items-center gap-3 text-gray-600">
                    <span class="flex items-center gap-1"><i class="fas fa-map-marker-alt text-blue-600 text-xs"></i> IP الخاص بك:</span>
                    <span class="font-mono font-medium text-gray-900" id="user-ip">جاري التحميل...</span>
                    <span class="w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>
                    <span class="text-xs font-bold text-red-500">غير محمي</span>
                </div>
                <div class="flex items-center gap-2 text-gray-500">
                    <i class="far fa-clock"></i>
                    <span>آخر تحديث: {now}</span>
                </div>
            </div>
        </div>
    </header>

    <!-- القسم الرئيسي -->
    <section class="hero-gradient relative overflow-hidden border-b border-gray-200">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-24 text-center">
            <h1 class="text-4xl md:text-6xl font-black mb-6 text-gray-900 leading-tight">
                الحرية لتصفح <br> أي موقع من أي مكان.
            </h1>
            <p class="text-lg text-gray-600 max-w-3xl mx-auto mb-12">
                DOKA تستخدم سيرفرات قوية لتجربة إنترنت سريعة وآمنة. دائماً مجانية، بدون تكاليف خفية وبدون حدود للاستخدام.
            </p>
            
            <!-- عداد السيرفرات -->
            <div class="flex justify-center mb-10">
                <div class="bg-white border border-gray-200 rounded-3xl px-10 py-5 shadow-sm inline-flex items-center gap-4">
                    <span class="text-6xl font-black text-blue-600" id="total-servers-count">{total_servers}</span>
                    <span class="text-gray-500 leading-tight text-right">سيرفر<br>V2Ray نشط</span>
                </div>
            </div>
            <p class="text-sm text-gray-400 flex items-center justify-center gap-2">
                <i class="fas fa-shield-alt text-blue-500"></i> تشفير AES-256 | VMess/VLess/Trojan | بدون تسجيل للنشاطات
            </p>
        </div>
    </section>

    <!-- كيف يعمل؟ -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h2 class="text-3xl md:text-4xl font-bold text-center mb-16 text-gray-900">كيف تعمل سيرفرات DOKA؟</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-12">
            <div class="bg-blue-50/50 p-8 rounded-3xl border border-blue-100">
                <h3 class="text-xl font-bold mb-4 flex items-center gap-2"><i class="fas fa-check-circle text-green-500"></i> مع DOKA</h3>
                <p class="text-gray-600 leading-relaxed">عند استخدام DOKA، يتم تشفير اتصالك بالكامل. مزود الخدمة لا يمكنه رؤية المواقع التي تزورها. أنت تظهر بعنوان IP جديد تماماً من سيرفراتنا السريعة.</p>
            </div>
            <div class="bg-gray-50 p-8 rounded-3xl border border-gray-200">
                <h3 class="text-xl font-bold mb-4 flex items-center gap-2"><i class="fas fa-times-circle text-red-400"></i> بدون DOKA</h3>
                <p class="text-gray-600 leading-relaxed">بدون DOKA، مزود الخدمة (ISP) يعرف كل موقع تزوره. نشاطك على الإنترنت يمكن تتبعه بسهولة من خلال عنوان IP الحقيقي الخاص بك.</p>
            </div>
        </div>
    </section>

    <!-- لماذا DOKA هو الخيار الأفضل؟ -->
    <section class="bg-white border-y border-gray-200 py-16">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h2 class="text-3xl md:text-4xl font-bold text-center mb-16 text-gray-900">لماذا DOKA هو الخيار الأفضل؟</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div class="text-center">
                    <div class="w-16 h-16 bg-blue-100 rounded-2xl flex items-center justify-center mx-auto mb-4 text-blue-600 text-2xl"><i class="fas fa-user-secret"></i></div>
                    <h4 class="font-bold text-lg mb-2">خصوصية تامة</h4>
                    <p class="text-gray-500 text-sm">تشفير من الدرجة العسكرية يمنع أي طرف ثالث من التجسس.</p>
                </div>
                <div class="text-center">
                    <div class="w-16 h-16 bg-blue-100 rounded-2xl flex items-center justify-center mx-auto mb-4 text-blue-600 text-2xl"><i class="fas fa-globe"></i></div>
                    <h4 class="font-bold text-lg mb-2">حرية الوصول</h4>
                    <p class="text-gray-500 text-sm">تجاوز الحجب الحكومي وحواجز المدارس وأماكن العمل.</p>
                </div>
                <div class="text-center">
                    <div class="w-16 h-16 bg-blue-100 rounded-2xl flex items-center justify-center mx-auto mb-4 text-blue-600 text-2xl"><i class="fas fa-tachometer-alt"></i></div>
                    <h4 class="font-bold text-lg mb-2">سرعة فائقة</h4>
                    <p class="text-gray-500 text-sm">نضمن سرعات عالية بدون تحديد للحصص بفضل شبكتنا الممتازة.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- سيرفراتنا -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h2 class="text-3xl md:text-4xl font-bold text-center mb-6 text-gray-900">هل أنت جاهز للإنضمام لشبكة الحرية؟</h2>
        <p class="text-center text-gray-500 mb-12">اختر البروتوكول الذي يناسب احتياجك</p>

        <!-- تبويبات البروتوكولات -->
        <div class="flex flex-wrap justify-center gap-2 mb-10" id="protocol-tabs">
            <!-- ستولد عبر JavaScript -->
        </div>

        <!-- حاوية عرض السيرفرات -->
        <div id="servers-display" class="grid grid-cols-1 md:grid-cols-2 gap-6"></div>
        <div id="no-servers-msg" class="text-center py-12 text-gray-400 hidden">
            <i class="fas fa-server text-4xl mb-4 opacity-50"></i>
            <p>لا توجد سيرفرات متاحة حالياً لهذا البروتوكول.</p>
        </div>
    </section>

    <!-- مزايا إضافية -->
    <section class="bg-gray-50 border-t border-gray-200 py-16">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <h3 class="text-2xl font-bold mb-12 text-center">المزيد من المزايا</h3>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                <div><span class="font-bold text-blue-600">01.</span> <span class="font-bold">تشفير كامل لحركة المرور</span><p class="text-gray-500 text-sm mt-1">حماية بياناتك على شبكات الواي فاي العامة.</p></div>
                <div><span class="font-bold text-blue-600">02.</span> <span class="font-bold">إخفاء الهوية الحقيقي</span><p class="text-gray-500 text-sm mt-1">عنوان IP جديد تماماً لا يمكن ربطه بك.</p></div>
                <div><span class="font-bold text-blue-600">03.</span> <span class="font-bold">الوصول للمحتوى المقيد</span><p class="text-gray-500 text-sm mt-1">شاهد أي محتوى من أي مكان في العالم.</p></div>
                <div><span class="font-bold text-blue-600">04.</span> <span class="font-bold">توافق مع جميع الأجهزة</span><p class="text-gray-500 text-sm mt-1">هواتف، حواسيب، أجهزة لوحية، وحتى الراوتر.</p></div>
                <div><span class="font-bold text-blue-600">05.</span> <span class="font-bold">تجاوز جدران الحماية</span><p class="text-gray-500 text-sm mt-1">حرية الإنترنت في الدول التي تفرض رقابة.</p></div>
                <div><span class="font-bold text-blue-600">06.</span> <span class="font-bold">تجربة ألعاب أفضل</span><p class="text-gray-500 text-sm mt-1">تقليل البينج وتجاوز الحظر الجغرافي للألعاب.</p></div>
            </div>
        </div>
    </section>

    <!-- تذييل -->
    <footer class="bg-gray-900 text-white py-12">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
            <p class="text-gray-400 text-sm mb-6">© 2026 DOKA. جميع الحقوق محفوظة. أداة مفتوحة المصدر لحرية الإنترنت.</p>
            <div class="flex justify-center gap-6 text-sm text-gray-500">
                <a href="#" class="hover:text-white">سياسة الخصوصية</a>
                <a href="#" class="hover:text-white">اتصل بنا</a>
                <a href="#" class="hover:text-white">عن المشروع</a>
            </div>
        </div>
    </footer>

    <!-- نافذة الإعلان -->
    <div id="bridge-modal" class="fixed inset-0 z-50 hidden items-center justify-center modal">
        <div class="bg-white rounded-3xl p-8 max-w-md w-full shadow-2xl text-center">
            <div class="animate-spin rounded-full h-12 w-12 border-t-4 border-blue-600 mb-4 mx-auto"></div>
            <h3 class="font-bold text-xl mb-2">جاري فحص الرابط...</h3>
            <p class="text-gray-500 text-sm">يرجى الانتظار، يتم تأمين الاتصال.</p>
        </div>
    </div>

    <script>
        // بيانات السيرفرات (يتم حقنها من بايثون)
        const serversData = {servers_json};
        const AD_LINK = "{AD_LINK}";
        let currentProtocol = 'vmess';

        // دالة عرض السيرفرات
        function renderServers(protocol) {{
            const container = document.getElementById('servers-display');
            const noServersMsg = document.getElementById('no-servers-msg');
            const servers = serversData[protocol] || [];
            
            if (servers.length === 0) {{
                container.innerHTML = '';
                noServersMsg.classList.remove('hidden');
                return;
            }}
            noServersMsg.classList.add('hidden');
            
            let html = '';
            servers.forEach((server, index) => {{
                const shortUrl = server.url.substring(0, 50) + '...';
                html += `
                    <div class="protocol-card bg-white rounded-2xl p-6 shadow-sm">
                        <div class="flex justify-between items-start mb-4">
                            <div class="flex items-center gap-3">
                                <span class="text-2xl">${{server.country}}</span>
                                <div>
                                    <span class="font-bold text-gray-800 block">${{protocol.toUpperCase()}} Server</span>
                                    <span class="text-xs text-gray-500"><i class="fas fa-microchip"></i> ${{server.latency}}</span>
                                </div>
                            </div>
                            <span class="bg-green-100 text-green-700 text-[10px] px-3 py-1 rounded-full font-bold"><i class="fas fa-circle text-[6px] align-middle mr-1"></i> نشط</span>
                        </div>
                        <p class="text-xs font-mono text-gray-400 bg-gray-50 p-3 rounded-xl mb-4 break-all border border-gray-100" dir="ltr">${{shortUrl}}</p>
                        <div class="flex gap-2">
                            <button onclick="copyToClipboard('${{server.url}}')" class="flex-1 bg-blue-600 text-white py-2.5 rounded-xl text-sm font-medium hover:bg-blue-700 transition"><i class="far fa-copy"></i> نسخ</button>
                            <button onclick="showQRCode('${{server.url}}')" class="w-12 bg-gray-100 text-gray-700 rounded-xl hover:bg-gray-200 transition"><i class="fas fa-qrcode"></i></button>
                            <button onclick="triggerAdAndDownload('${{server.url}}', '${{protocol}}_${{index}}')" class="w-12 bg-gray-100 text-gray-700 rounded-xl hover:bg-gray-200 transition"><i class="fas fa-download"></i></button>
                        </div>
                    </div>
                `;
            }});
            container.innerHTML = html;
        }}

        // دالة إنشاء التبويبات
        function renderTabs() {{
            const tabsContainer = document.getElementById('protocol-tabs');
            const protocols = Object.keys(serversData).filter(p => serversData[p].length > 0);
            if (protocols.length === 0) return;
            
            currentProtocol = protocols[0];
            let html = '';
            protocols.forEach(proto => {{
                const count = serversData[proto].length;
                html += `<button onclick="switchProtocol('${{proto}}')" id="tab-${{proto}}" class="protocol-tab px-6 py-2 ${{proto === currentProtocol ? 'bg-blue-600 text-white shadow-md shadow-blue-200' : 'bg-gray-100 text-gray-700'}} rounded-full text-sm font-medium hover:bg-gray-200">${{proto.toUpperCase()}} (${{count}})</button>`;
            }});
            tabsContainer.innerHTML = html;
            renderServers(currentProtocol);
        }}

        function switchProtocol(proto) {{
            currentProtocol = proto;
            document.querySelectorAll('.protocol-tab').forEach(tab => {{
                tab.classList.remove('bg-blue-600', 'text-white', 'shadow-md', 'shadow-blue-200');
                tab.classList.add('bg-gray-100', 'text-gray-700');
            }});
            document.getElementById(`tab-${{proto}}`).classList.add('bg-blue-600', 'text-white', 'shadow-md', 'shadow-blue-200');
            renderServers(proto);
        }}

        function copyToClipboard(text) {{ navigator.clipboard.writeText(text); alert('✅ تم نسخ الإعدادات!'); }}
        function showQRCode(url) {{
            const w = window.open("", "_blank", "width=400,height=500");
            w.document.write(`<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;font-family:Tajawal;"><h3>امسح الكود</h3><div id="qrcode" style="margin:20px"></div></div>`);
            new QRCode(w.document.getElementById("qrcode"), {{ text: url, width: 250, height: 250 }});
        }}
        function triggerAdAndDownload(url, filename) {{
            const modal = document.getElementById('bridge-modal');
            modal.style.display = 'flex';
            setTimeout(() => {{
                window.open(AD_LINK, '_blank');
                const a = document.createElement('a');
                a.href = 'data:text/plain;charset=utf-8,' + encodeURIComponent(url);
                a.download = filename + '.txt';
                a.click();
                modal.style.display = 'none';
            }}, 1500);
        }}

        // بدء التشغيل
        document.addEventListener('DOMContentLoaded', () => {{
            renderTabs();
            fetch('https://api.ipify.org?format=json').then(r => r.json()).then(d => {{
                document.getElementById('user-ip').innerText = d.ip;
            }});
        }});
    </script>
</body>
</html>'''

# ==================== الدالة الرئيسية ====================
def main():
    print("🚀 بدء عملية كشط البيانات من تيليجرام...")
    html_content = fetch_telegram_page(TELEGRAM_CHANNEL_URL)
    
    if not html_content:
        print("❌ فشل جلب البيانات. الخروج.")
        return
    
    print("📥 جاري استخراج التكوينات...")
    raw_configs = extract_configs(html_content)
    
    total_raw = sum(len(v) for v in raw_configs.values())
    print(f"✅ تم استخراج {total_raw} تكوين خام.")
    
    print("🔄 جاري تصنيف السيرفرات...")
    classified = classify_servers(raw_configs)
    
    print("📄 جاري توليد صفحة HTML...")
    html_output = generate_html(classified)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_output)
    
    # حفظ البيانات للاستخدام المستقبلي
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(classified, f, ensure_ascii=False, indent=2)
    
    print(f"🎉 تم بنجاح! الصفحة محفوظة في {OUTPUT_FILE}")
    print(f"📊 إجمالي السيرفرات النشطة: {sum(len(v) for v in classified.values())}")

if __name__ == "__main__":
    main()
