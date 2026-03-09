import requests
import re
from datetime import datetime

def run():
    url = "https://t.me/s/kg33d"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        # 1. جلب وتنظيف البيانات
        response = requests.get(url, headers=headers, timeout=20)
        links = re.findall(r'(?:vless|vmess|trojan|ss)://[^\s<"\'\s]+', response.text)
        
        clean_links = []
        for l in links:
            c = l.replace('&amp;', '&').split('<')[0].split('"')[0].strip()
            if c not in clean_links: clean_links.append(c)
        
        # 2. بناء الأقسام (تكرار العناصر كما في الصور)
        now = datetime.now().strftime("%Y-%m-%d")
        
        # قسم بطاقات السيرفرات
        server_cards = ""
        for i, link in enumerate(clean_links):
            proto = link.split('://')[0].upper()
            server_cards += f'''
            <div class="bg-white border border-gray-200 p-5 rounded-xl shadow-sm hover:shadow-md transition-all mb-4 text-right">
                <div class="flex justify-between items-center mb-3">
                    <span class="bg-indigo-50 text-indigo-700 px-3 py-1 rounded-lg text-xs font-bold uppercase">{proto} SERVER</span>
                    <button onclick="copyText('{link}')" class="text-gray-400 hover:text-indigo-600"><i class="far fa-copy"></i></button>
                </div>
                <p class="text-[11px] text-gray-400 font-mono break-all mb-4 bg-gray-50 p-2 rounded">{link[:70]}...</p>
                <div class="flex gap-2">
                    <button onclick="copyText('{link}')" class="flex-1 py-3 bg-indigo-600 text-white rounded-xl font-bold text-sm hover:bg-indigo-700 transition-all">نسخ الإعدادات</button>
                    <button onclick="toggleQR('q{i}', '{link}')" class="px-4 bg-gray-100 text-gray-600 rounded-xl hover:bg-gray-200"><i class="fas fa-qrcode"></i></button>
                </div>
                <div id="q{i}" class="hidden mt-4 p-4 border-t flex justify-center"></div>
            </div>'''

        html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Freevmess - V2Ray Tunneling</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Cairo', sans-serif; background-color: #fff; overflow-x: hidden; }}
        .gradient-text {{ background: linear-gradient(135deg, #1e1b4b 0%, #4338ca 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .section-divider {{ position: relative; padding-bottom: 50px; }}
        .section-divider::after {{ content: ''; position: absolute; bottom: 0; left: 0; width: 100%; height: 60px; background-image: url('data:image/svg+xml;utf8,<svg viewBox="0 0 1440 320" xmlns="http://www.w3.org/2000/svg"><path fill="%23f9fafb" fill-opacity="1" d="M0,224L120,213.3C240,203,480,181,720,186.7C960,192,1200,224,1320,240L1440,256L1440,320L1320,320C1200,320,960,320,720,320C480,320,240,320,120,320L0,320Z"></path></svg>'); background-size: cover; }}
    </style>
</head>
<body>

    <nav class="flex justify-between items-center px-6 py-6 max-w-6xl mx-auto">
        <div class="flex items-center gap-3">
            <img src="https://www.freevmess.com/assets/img/logo.png" alt="Logo" class="h-10" onerror="this.src='https://cdn-icons-png.flaticon.com/512/733/733641.png'">
            <div class="leading-none">
                <span class="text-xl font-black text-slate-800 block">Freevmess</span>
                <span class="text-[10px] text-gray-400">V2Ray or Vmess Tunneling</span>
            </div>
        </div>
        <i class="fas fa-bars text-gray-400 text-xl"></i>
    </nav>

    <section class="px-6 pt-16 text-center max-w-4xl mx-auto">
        <h1 class="text-5xl md:text-6xl font-black tracking-tighter mb-6 gradient-text">خادم VMESS <br> مخصص</h1>
        <p class="text-gray-500 text-sm leading-loose mb-10 px-4">خادم v2ray مجاني مميز، خادم بدون v7، حصان طروادة VPN، مقبس ويب vmess وإنشاء حساب v2ray سهل.</p>
        <img src="https://cdni.iconscout.com/illustration/premium/thumb/network-infrastructure-4437294-3684813.png" class="w-72 mx-auto mb-10">
    </section>

    <section class="bg-gray-50 py-16 px-6 text-center">
        <div class="max-w-4xl mx-auto space-y-16">
            <div>
                <img src="https://www.freevmess.com/assets/img/all-devices.png" class="h-24 mx-auto mb-4" onerror="this.style.display='none'">
                <h3 class="text-xl font-bold mb-3">الوصول إلى جميع الأجهزة</h3>
                <p class="text-gray-500 text-sm leading-relaxed">قم بتثبيت تطبيق v2ray وقم بالوصول إلى v2ray/vmess على جميع أجهزة Android وأجهزة الكمبيوتر/أجهزة الكمبيوتر المحمولة وأجهزة iPhone و Windows و GNU/linux و iOS</p>
            </div>
            <div>
                <h2 class="text-3xl font-black text-cyan-500 mb-3 tracking-tighter">FREE ACCESS</h2>
                <h3 class="text-xl font-bold mb-3">مجاني وسهل</h3>
                <p class="text-gray-500 text-sm leading-relaxed">الوصول إلى جميع الخوادم مجاني 100%، ويمكنك الحصول على الوصول إلى الخادم والحساب بسهولة (لا حاجة إلى خطوات معقدة).</p>
            </div>
        </div>
    </section>

    <section class="py-16 px-6 max-w-2xl mx-auto">
        <h2 class="text-2xl font-bold text-slate-800 mb-8 flex items-center gap-2">
            <span class="w-2 h-8 bg-indigo-600 rounded-full"></span>
            أحدث السيرفرات المتاحة
        </h2>
        {server_cards if clean_links else '<p class="text-center py-10">جاري البحث عن سيرفرات...</p>'}
    </section>

    <section class="bg-white px-6 py-12 border-t border-gray-100">
        <div class="max-w-4xl mx-auto space-y-8">
            <div class="text-right">
                <h3 class="text-xl font-bold text-gray-800 mb-4">خادمنا</h3>
                <p class="text-sm text-gray-500 italic bg-slate-50 p-4 rounded-lg border-r-4 border-red-500">" أحد أفضل مزودي الخوادم الافتراضية الخاصة والخوادم المخصصة الذين نعتقد أنهم يقدمون أفضل أداء - فولتر "</p>
            </div>

            <div class="text-right">
                <h3 class="text-xl font-bold text-gray-800 mb-2">الشروط والأحكام</h3>
                <p class="text-xs text-gray-400 leading-loose">تحدد هذه الشروط والأحكام قواعد وأنظمة استخدام موقع freevmess الإلكتروني. بدخولك إلى هذا الموقع نفترض موافقتك على هذه الشروط والأحكام...</p>
                <a href="#" class="text-red-400 text-xs">اقرأ المزيد</a>
            </div>

            <div class="border rounded-xl overflow-hidden">
                <div class="bg-gray-50 p-4 font-bold border-b">اكتشف المزيد</div>
                <div class="divide-y">
                    <div class="p-4 flex justify-between items-center hover:bg-gray-50">
                        <span class="text-sm text-gray-600">أدوات مراقبة الشبكة</span>
                        <i class="fas fa-chevron-left text-gray-300"></i>
                    </div>
                    <div class="p-4 flex justify-between items-center hover:bg-gray-50">
                        <span class="text-sm text-gray-600">مخطط VPN</span>
                        <i class="fas fa-chevron-left text-gray-300"></i>
                    </div>
                    <div class="p-4 flex justify-between items-center hover:bg-gray-50">
                        <span class="text-sm text-gray-600">Websockets</span>
                        <i class="fas fa-chevron-left text-gray-300"></i>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <footer class="bg-slate-50 pt-16 pb-8 px-6 text-center section-divider">
        <p class="text-gray-400 text-sm mb-4">جميع الحقوق محفوظة &copy; Freevmess.com</p>
        <div class="flex justify-center gap-4 text-indigo-600 font-bold text-xs mb-8">
            <a href="#">سياسة الخصوصية</a>
            <a href="#">اتصل بنا</a>
        </div>
        <div class="bg-indigo-900 text-white p-4 rounded-xl text-[10px] leading-relaxed max-w-lg mx-auto">
            إعدادات الخصوصية وملفات تعريف الارتباط تدار بواسطة جوجل. متوافقة مع إطار الشفافية والموافقة.
        </div>
    </footer>

    <div id="toast" class="fixed bottom-10 left-1/2 -translate-x-1/2 bg-slate-800 text-white px-6 py-3 rounded-full text-sm font-bold opacity-0 transition-opacity pointer-events-none z-50">تم النسخ بنجاح! ✅</div>

    <script>
        function copyText(t) {{
            navigator.clipboard.writeText(t);
            const toast = document.getElementById('toast');
            toast.style.opacity = '1';
            setTimeout(() => toast.style.opacity = '0', 2000);
        }}
        function toggleQR(id, link) {{
            const el = document.getElementById(id);
            if (!el.innerHTML) new QRCode(el, {{text: link, width: 140, height: 140}});
            el.classList.toggle('hidden');
        }}
    </script>
</body>
</html>'''
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("✅ تم إنشاء الموقع بالكامل بنجاح!")
            
    except Exception as e: print(f"Error: {e}")

if __name__ == "__main__": run()
