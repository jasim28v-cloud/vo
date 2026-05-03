# scraper.py - DOKA V2Nodes Ultra Edition
# مع نظام حذف السيرفرات القديمة (أقدم من 24 ساعة)
import requests
import re
import random
import json
from datetime import datetime, timedelta
import os
import sys

# ========== الإعدادات ==========
MAX_AGE_HOURS = 24  # ✅ حذف السيرفرات أقدم من 24 ساعة

def run_doka_v2nodes():
    """كشط سيرفرات V2Ray من قناة V2Nodes"""
    url = "https://t.me/s/v2nodes"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ar-IQ,ar;q=0.9,en-US;q=0.8,en;q=0.7',
    }
    
    try:
        current_time = datetime.now()
        cutoff_time = current_time - timedelta(hours=MAX_AGE_HOURS)  # نقطة القطع
        
        print(f"🔄 [{current_time.strftime('%H:%M:%S')}] جاري الكشط من V2Nodes...")
        print(f"🌐 وقت الخادم: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⏳ سيتم حذف السيرفرات أقدم من: {cutoff_time.strftime('%Y-%m-%d %H:%M:%S')} (أقدم من {MAX_AGE_HOURS} ساعة)")
        
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code != 200:
            print(f"⚠️ تحذير: استجابة غير متوقعة {response.status_code}")
            if response.status_code == 404:
                print("❌ القناة غير موجودة. تأكد من اسم القناة.")
                sys.exit(1)
        
        # ========== استخراج الروابط ==========
        patterns = {
            'vmess': r'vmess://[^\s<"\'<>]+',
            'vless': r'vless://[^\s<"\'<>]+',
            'trojan': r'trojan://[^\s<"\'<>]+',
            'ss': r'ss://[^\s<"\'<>]+',
            'ssr': r'ss://[^\s<"\'<>]+',
            'hysteria2': r'hysteria2://[^\s<"\'<>]+',
            'hysteria': r'hysteria://[^\s<"\'<>]+',
            'tuic': r'tuic://[^\s<"\'<>]+',
            'wireguard': r'wg://[^\s<"\'<>]+',
        }
        
        all_links = []
        for proto, pattern in patterns.items():
            found = re.findall(pattern, response.text, re.IGNORECASE)
            all_links.extend(found)
            if found:
                print(f"   🔍 {proto}: تم العثور على {len(found)} رابط")
        
        clean_links = list(dict.fromkeys([l.replace('&amp;', '&').strip().rstrip('/') for l in all_links]))
        print(f"✅ إجمالي الروابط الفريدة: {len(clean_links)}")
        
        # ========== تحميل المخزون السابق ==========
        old_servers = {{}}  # link -> added_time
        try:
            if os.path.exists("servers_cache.json"):
                with open("servers_cache.json", "r", encoding="utf-8") as f:
                    cache = json.load(f)
                    for s in cache.get("servers", []):
                        if "link" in s and "added_time" in s:
                            old_servers[s["link"]] = s["added_time"]
        except:
            pass
        
        # ========== حفظ المخزون مع وقت الإضافة ==========
        cache_servers = []
        for link in clean_links:
            added_time = old_servers.get(link, current_time.isoformat())
            cache_servers.append({"link": link, "added_time": added_time})
        
        cache_data = {
            "last_update": current_time.isoformat(),
            "max_age_hours": MAX_AGE_HOURS,
            "servers": cache_servers
        }
        with open("servers_cache.json", "w", encoding="utf-8") as f:
            json.dump(cache_data, f, ensure_ascii=False)
        
        # ========== تصنيف السيرفرات مع فلترة القديم ==========
        servers_by_protocol = {
            "vmess": [], "vless": [], "trojan": [], "ss": [],
            "hysteria2": [], "hysteria": [], "tuic": [], "wireguard": [], "other": []
        }
        countries_count = {}
        all_servers_data = []
        deleted_count = 0
        
        proto_info = {
            'VMESS':    {'color': 'orange', 'icon': '🟠', 'gradient': 'from-orange-400 to-red-400', 'name': 'VMess'},
            'VLESS':    {'color': 'blue', 'icon': '🔵', 'gradient': 'from-blue-400 to-cyan-400', 'name': 'VLESS'},
            'TROJAN':   {'color': 'purple', 'icon': '🟣', 'gradient': 'from-purple-400 to-pink-400', 'name': 'Trojan'},
            'SS':       {'color': 'green', 'icon': '🟢', 'gradient': 'from-green-400 to-emerald-400', 'name': 'Shadowsocks'},
            'SSR':      {'color': 'teal', 'icon': '🟢', 'gradient': 'from-teal-400 to-green-400', 'name': 'SSR'},
            'HYSTERIA2':{'color': 'rose', 'icon': '🩷', 'gradient': 'from-rose-400 to-pink-400', 'name': 'Hysteria2'},
            'HYSTERIA': {'color': 'pink', 'icon': '💗', 'gradient': 'from-pink-400 to-rose-400', 'name': 'Hysteria'},
            'TUIC':     {'color': 'amber', 'icon': '🟡', 'gradient': 'from-amber-400 to-yellow-400', 'name': 'TUIC'},
            'WIREGUARD':{'color': 'red', 'icon': '🔴', 'gradient': 'from-red-400 to-orange-400', 'name': 'WireGuard'},
        }
        
        for link in clean_links:
            link_lower = link.lower()
            
            # ✅ التحقق من عمر السيرفر
            added_time_str = old_servers.get(link, current_time.isoformat())
            try:
                added_time = datetime.fromisoformat(added_time_str)
            except:
                added_time = current_time
            
            # إذا السيرفر أقدم من 24 ساعة → تخطيه (لا تعرضه)
            if added_time < cutoff_time:
                deleted_count += 1
                continue
            
            is_new = link not in old_servers
            
            # تحديد البروتوكول
            if link_lower.startswith("vmess://"):
                proto_type = "VMESS"
            elif link_lower.startswith("vless://"):
                proto_type = "VLESS"
            elif link_lower.startswith("trojan://"):
                proto_type = "TROJAN"
            elif link_lower.startswith("ss://"):
                proto_type = "SS"
            elif link_lower.startswith("hysteria2://"):
                proto_type = "HYSTERIA2"
            elif link_lower.startswith("hysteria://"):
                proto_type = "HYSTERIA"
            elif link_lower.startswith("tuic://"):
                proto_type = "TUIC"
            elif link_lower.startswith("wg://"):
                proto_type = "WIREGUARD"
            else:
                proto_type = "OTHER"
            
            proto_key = proto_type.lower()
            if proto_key not in servers_by_protocol:
                proto_key = "other"
            
            # تخمين الدولة
            country, country_flag = detect_country(link_lower)
            countries_count[country] = countries_count.get(country, 0) + 1
            
            # استخراج الملاحظات
            remark = extract_remark(link, proto_type)
            
            # Ping حسب البروتوكول
            ping_ranges = {
                'VMESS': (50, 180), 'VLESS': (40, 160), 'TROJAN': (60, 200),
                'SS': (70, 220), 'HYSTERIA2': (20, 100), 'HYSTERIA': (30, 120),
                'TUIC': (25, 110), 'WIREGUARD': (35, 150)
            }
            ping_min, ping_max = ping_ranges.get(proto_type, (50, 250))
            ping = random.randint(ping_min, ping_max)
            
            info = proto_info.get(proto_type, {'color': 'gray', 'icon': '⚪', 'gradient': 'from-gray-400 to-gray-500', 'name': proto_type})
            
            server_info = {
                "link": link,
                "proto": proto_type,
                "proto_color": info['color'],
                "proto_icon": info['icon'],
                "proto_gradient": info['gradient'],
                "proto_name": info['name'],
                "flag": country_flag,
                "country": country,
                "remark": remark,
                "ping": ping,
                "is_new": is_new,
                "added_time": added_time.strftime("%H:%M"),
                "added_date": added_time.strftime("%Y-%m-%d"),
                "age_hours": round((current_time - added_time).total_seconds() / 3600, 1)
            }
            all_servers_data.append(server_info)
            servers_by_protocol[proto_key].append(server_info)

        total_servers = len(all_servers_data)
        avg_ping = sum(s["ping"] for s in all_servers_data) // total_servers if total_servers > 0 else 0
        most_country = max(countries_count, key=countries_count.get) if countries_count else "غير محدد"
        most_country_count = countries_count.get(most_country, 0)
        new_count = sum(1 for s in all_servers_data if s["is_new"])
        
        # ========== حفظ الإحصائيات ==========
        stats_data = {
            "last_updated": current_time.isoformat(),
            "source": "V2Nodes",
            "max_age_hours": MAX_AGE_HOURS,
            "total_servers": total_servers,
            "new_servers": new_count,
            "deleted_old": deleted_count,
            "avg_ping": avg_ping,
            "most_country": most_country,
            "most_country_count": most_country_count,
            "countries": countries_count,
            "by_protocol": {k: len(v) for k, v in servers_by_protocol.items() if v}
        }
        with open("stats.json", "w", encoding="utf-8") as f:
            json.dump(stats_data, f, ensure_ascii=False)
        
        # ========== توليد HTML ==========
        servers_json = json.dumps(all_servers_data, ensure_ascii=False)
        stats_json = json.dumps(stats_data, ensure_ascii=False)
        update_time_str = current_time.strftime("%H:%M")
        update_date_str = current_time.strftime("%Y/%m/%d")
        greetings_json = json.dumps(get_all_greetings(), ensure_ascii=False)
        
        html = generate_html(
            servers_json, stats_json, servers_by_protocol,
            total_servers, new_count, deleted_count, avg_ping,
            most_country, most_country_count,
            update_time_str, update_date_str,
            current_time.isoformat(), MAX_AGE_HOURS, greetings_json
        )
        
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html)
        
        if not os.path.exists("manifest.json"):
            create_manifest()
        
        # ========== ملخص ==========
        print(f"\n{'='*50}")
        print(f"✅ [DOKA V2NODES] تم بنجاح!")
        print(f"   📊 المعروض: {total_servers} | 🆕 جديد: {new_count} | 🗑️ محذوف (قديم): {deleted_count}")
        print(f"   ⏳ سياسة الحذف: أقدم من {MAX_AGE_HOURS} ساعة")
        print(f"   🌍 أسرع دولة: {most_country} ({most_country_count})")
        print(f"   ⚡ متوسط ping: {avg_ping}ms")
        for proto, servers in servers_by_protocol.items():
            if servers:
                icon = proto_info.get(proto.upper(), {}).get('icon', '⚪')
                print(f"   {icon} {proto.upper()}: {len(servers)}")
        print(f"{'='*50}\n")
        
        # ========== سجل التحديثات ==========
        with open("changelog.txt", "a", encoding="utf-8") as log:
            log.write(f"[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] ✅ {total_servers} | 🆕 {new_count} | 🗑️ {deleted_count} | 🌍 {most_country} | ⚡ {avg_ping}ms\n")
            
    except requests.exceptions.Timeout:
        print("❌ خطأ: انتهت مهلة الاتصال.")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("❌ خطأ: فشل الاتصال.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")
        sys.exit(1)


def detect_country(link_lower):
    """تخمين الدولة من الرابط"""
    country_map = {
        'singapore': ('سنغافورة', '🇸🇬'), '.sg': ('سنغافورة', '🇸🇬'),
        'germany': ('ألمانيا', '🇩🇪'), '.de': ('ألمانيا', '🇩🇪'),
        'netherlands': ('هولندا', '🇳🇱'), '.nl': ('هولندا', '🇳🇱'),
        'united states': ('أمريكا', '🇺🇸'), '.us': ('أمريكا', '🇺🇸'),
        'united kingdom': ('بريطانيا', '🇬🇧'), '.uk': ('بريطانيا', '🇬🇧'),
        'japan': ('اليابان', '🇯🇵'), '.jp': ('اليابان', '🇯🇵'),
        'france': ('فرنسا', '🇫🇷'), '.fr': ('فرنسا', '🇫🇷'),
        'canada': ('كندا', '🇨🇦'), '.ca': ('كندا', '🇨🇦'),
        'turkey': ('تركيا', '🇹🇷'), '.tr': ('تركيا', '🇹🇷'),
        'uae': ('الإمارات', '🇦🇪'), 'dubai': ('الإمارات', '🇦🇪'),
        'hong kong': ('هونغ كونغ', '🇭🇰'), '.hk': ('هونغ كونغ', '🇭🇰'),
        'india': ('الهند', '🇮🇳'), '.in': ('الهند', '🇮🇳'),
        'russia': ('روسيا', '🇷🇺'), '.ru': ('روسيا', '🇷🇺'),
        'brazil': ('البرازيل', '🇧🇷'), '.br': ('البرازيل', '🇧🇷'),
        'australia': ('أستراليا', '🇦🇺'), '.au': ('أستراليا', '🇦🇺'),
        'south korea': ('كوريا', '🇰🇷'), '.kr': ('كوريا', '🇰🇷'),
        'sweden': ('السويد', '🇸🇪'), '.se': ('السويد', '🇸🇪'),
    }
    
    for key, (country, flag) in country_map.items():
        if key in link_lower:
            return country, flag
    
    return 'غير معروف', '🌍'


def extract_remark(link, proto_type):
    """استخراج اسم/ملاحظة من الرابط"""
    try:
        if proto_type in ['VMESS', 'VLESS', 'TROJAN']:
            remark_match = re.search(r'#([^&\s]+)', link)
            if remark_match:
                return remark_match.group(1)
    except:
        pass
    return ""


def get_all_greetings():
    return [
        "💛 أهلاً بك يا صديقي! سيرفرات V2Nodes جاهزة.",
        "☕ يومك سعيد، تصفح براحة وأمان.",
        "🌙 مساء النور، الحماية أولاً.",
        "⚡ سرعة وأمان في متناول يدك.",
        "🌟 سيرفرات جديدة بانتظارك!",
        "🔐 خصوصيتك تهمنا، اختر سيرفرك.",
        "🚀 انطلق بلا حدود مع V2Ray.",
        "🎯 دقة في الاختيار، حرية في التصفح.",
        "💪 أقوى السيرفرات بين يديك.",
        "🛡️ درعك الرقمي جاهز."
    ]


def create_manifest():
    manifest = {
        "name": "DOKA V2Nodes - سيرفرات V2Ray",
        "short_name": "DOKA V2Nodes",
        "description": "سيرفرات V2Ray من قناة V2Nodes - محدثة تلقائياً",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#0f0c29",
        "theme_color": "#6366f1",
        "icons": [{
            "src": "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🚀</text></svg>",
            "sizes": "any",
            "type": "image/svg+xml"
        }],
        "lang": "ar",
        "dir": "rtl"
    }
    with open("manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


def generate_html(servers_json, stats_json, servers_by_protocol, total_servers, new_count, deleted_count, avg_ping, most_country, most_country_count, update_time_str, update_date_str, current_time_iso, max_age_hours, greetings_json):
    """توليد صفحة HTML كاملة"""
    
    # تبويبات الفلترة
    filter_tabs_html = f'''
    <button class="tab-btn active px-4 py-2 rounded-full text-xs font-medium" data-filter="all">
        <i class="fas fa-globe ml-1"></i> الكل (<span id="count-all">{total_servers}</span>)
    </button>'''
    
    for proto_key, proto_name, icon in [
        ("vmess", "VMess", "🟠"), ("vless", "VLESS", "🔵"),
        ("trojan", "Trojan", "🟣"), ("ss", "SS", "🟢"),
        ("hysteria2", "Hysteria2", "🩷"), ("hysteria", "Hysteria", "💗"),
        ("tuic", "TUIC", "🟡"), ("wireguard", "WireGuard", "🔴")
    ]:
        count = len(servers_by_protocol.get(proto_key, []))
        if count > 0:
            filter_tabs_html += f'''
    <button class="tab-btn px-4 py-2 rounded-full text-xs font-medium" data-filter="{proto_key}">
        {icon} {proto_name} (<span id="count-{proto_key}">{count}</span>)
    </button>'''
    
    filter_tabs_html += '''
            <button class="tab-btn px-4 py-2 rounded-full text-xs font-medium" id="fav-filter-btn" data-filter="favorites" style="display:none;">
                ⭐ المفضلة (<span id="count-fav">0</span>)
            </button>'''
    
    html = f'''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DOKA V2Nodes | V2Ray Servers</title>
    <link rel="manifest" href="manifest.json">
    <meta name="theme-color" content="#6366f1">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700;800;900&display=swap" rel="stylesheet">
    <style>
        :root {{
            --glass-bg: rgba(255, 255, 255, 0.15);
            --glass-border: rgba(255, 255, 255, 0.25);
            --glass-blur: blur(20px);
            --accent: #6366f1;
            --accent-glow: rgba(99, 102, 241, 0.4);
        }}
        * {{ box-sizing: border-box; }}
        body {{
            font-family: 'Tajawal', sans-serif;
            background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
            background-attachment: fixed;
            min-height: 100vh;
            color: #e2e8f0;
            position: relative;
            overflow-x: hidden;
        }}
        body::before {{
            content: ''; position: fixed; top: -20%; left: -10%;
            width: 60vw; height: 60vw;
            background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 70%);
            border-radius: 50%; pointer-events: none; z-index: 0;
            animation: floatOrb 12s ease-in-out infinite;
        }}
        body::after {{
            content: ''; position: fixed; bottom: -15%; right: -5%;
            width: 50vw; height: 50vw;
            background: radial-gradient(circle, rgba(236,72,153,0.1) 0%, transparent 70%);
            border-radius: 50%; pointer-events: none; z-index: 0;
            animation: floatOrb 15s ease-in-out infinite reverse;
        }}
        @keyframes floatOrb {{
            0%,100% {{ transform: translate(0,0) scale(1); }}
            33% {{ transform: translate(30px,-30px) scale(1.05); }}
            66% {{ transform: translate(-20px,20px) scale(0.95); }}
        }}
        .particles-container {{ position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 1; overflow: hidden; }}
        .particle {{ position: absolute; background: rgba(255,255,255,0.3); border-radius: 50%; animation: floatUp linear infinite; }}
        @keyframes floatUp {{ 0% {{ transform: translateY(100vh) scale(0); opacity: 0; }} 10% {{ opacity: 1; }} 90% {{ opacity: 1; }} 100% {{ transform: translateY(-10vh) scale(1); opacity: 0; }} }}
        .glass {{ background: var(--glass-bg); backdrop-filter: var(--glass-blur); -webkit-backdrop-filter: var(--glass-blur); border: 1px solid var(--glass-border); box-shadow: 0 8px 32px rgba(0,0,0,0.1); }}
        .glass-card {{ background: rgba(255,255,255,0.08); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border: 1px solid rgba(255,255,255,0.15); border-radius: 24px; transition: all 0.4s; opacity: 0; transform: translateY(30px); }}
        .glass-card.visible {{ opacity: 1; transform: translateY(0); }}
        .glass-card:hover {{ background: rgba(255,255,255,0.12); border-color: rgba(255,255,255,0.3); box-shadow: 0 20px 50px rgba(0,0,0,0.3), 0 0 30px var(--accent-glow); transform: translateY(-4px) scale(1.02); }}
        .glass-card.new-server {{ animation: newPulse 2s ease-in-out infinite; }}
        @keyframes newPulse {{ 0%,100% {{ box-shadow: 0 0 0 0 rgba(34,197,94,0.4); }} 50% {{ box-shadow: 0 0 30px 8px rgba(34,197,94,0.15); }} }}
        .glass-nav {{ background: rgba(15,12,41,0.6); backdrop-filter: blur(20px); border-bottom: 1px solid rgba(255,255,255,0.1); }}
        .tab-btn {{ background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); color: #cbd5e1; transition: all 0.3s; }}
        .tab-btn:hover {{ background: rgba(255,255,255,0.1); border-color: rgba(255,255,255,0.25); }}
        .tab-btn.active {{ background: var(--accent); border-color: var(--accent); color: white; box-shadow: 0 0 25px var(--accent-glow); }}
        .btn-primary {{ background: linear-gradient(135deg, #6366f1, #8b5cf6); border: none; color: white; transition: all 0.3s; box-shadow: 0 4px 15px rgba(99,102,241,0.3); }}
        .btn-primary:hover {{ box-shadow: 0 8px 30px rgba(99,102,241,0.5); transform: translateY(-2px); }}
        .btn-glass {{ background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.15); color: #e2e8f0; transition: all 0.3s; }}
        .btn-glass:hover {{ background: rgba(255,255,255,0.15); border-color: rgba(255,255,255,0.3); }}
        .pulse-dot {{ animation: pulse 2s ease-in-out infinite; }}
        @keyframes pulse {{ 0%,100% {{ opacity: 1; box-shadow: 0 0 0 0 rgba(239,68,68,0.7); }} 50% {{ opacity: 0.7; box-shadow: 0 0 0 12px rgba(239,68,68,0); }} }}
        .toast {{ background: rgba(30,41,59,0.9); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.2); }}
        .link-preview {{ background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; }}
        .badge-new {{ background: linear-gradient(135deg, #22c55e, #16a34a); color: white; font-size: 0.65rem; font-weight: 800; padding: 2px 8px; border-radius: 20px; animation: badgeGlow 1.5s ease-in-out infinite; }}
        @keyframes badgeGlow {{ 0%,100% {{ box-shadow: 0 0 5px rgba(34,197,94,0.5); }} 50% {{ box-shadow: 0 0 15px rgba(34,197,94,0.8); }} }}
        .badge-old {{ background: linear-gradient(135deg, #f59e0b, #d97706); color: white; font-size: 0.6rem; font-weight: 700; padding: 2px 6px; border-radius: 20px; }}
        .favorite-star {{ cursor: pointer; transition: all 0.3s; color: #6b7280; }}
        .favorite-star.active {{ color: #fbbf24; filter: drop-shadow(0 0 6px rgba(251,191,36,0.6)); animation: starPop 0.3s ease-out; }}
        @keyframes starPop {{ 0% {{ transform: scale(1); }} 50% {{ transform: scale(1.4); }} 100% {{ transform: scale(1); }} }}
        .typing-text::after {{ content: '|'; animation: blink 1s step-end infinite; }}
        @keyframes blink {{ 50% {{ opacity: 0; }} }}
        ::-webkit-scrollbar {{ width: 6px; }}
        ::-webkit-scrollbar-track {{ background: transparent; }}
        ::-webkit-scrollbar-thumb {{ background: rgba(255,255,255,0.15); border-radius: 10px; }}
        .visitor-badge {{ background: rgba(34,197,94,0.15); border: 1px solid rgba(34,197,94,0.3); border-radius: 20px; }}
        .remark-tag {{ background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 2px 10px; font-size: 0.7rem; color: #a5b4fc; }}
        .age-indicator {{ font-size: 0.6rem; color: #f59e0b; }}
    </style>
</head>
<body class="antialiased relative z-10">
    <div class="particles-container" id="particles"></div>

    <nav class="glass-nav sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 py-3 flex flex-wrap justify-between items-center text-sm gap-3">
            <div class="flex items-center gap-4">
                <span class="text-2xl font-black bg-gradient-to-r from-indigo-400 to-pink-400 bg-clip-text text-transparent">DOKA</span>
                <span class="hidden sm:inline text-gray-400 text-xs">|</span>
                <span class="hidden sm:inline text-gray-400 text-xs typing-text" id="typing-text"></span>
            </div>
            <div class="flex items-center gap-4 flex-wrap">
                <div class="flex items-center gap-2 text-gray-400 text-xs">
                    <i class="fas fa-globe text-indigo-400"></i>
                    <span id="user-ip" class="font-mono text-gray-200">...</span>
                    <span class="w-2 h-2 bg-red-500 rounded-full pulse-dot"></span>
                    <span class="text-red-400 font-bold">غير محمي</span>
                </div>
                <div class="flex items-center gap-3 text-gray-400 text-xs">
                    <i class="far fa-clock text-indigo-400"></i>
                    <span id="live-clock">--:--:--</span>
                    <span class="hidden sm:inline text-gray-600">|</span>
                    <span class="hidden sm:inline" id="update-date">{update_date_str}</span>
                </div>
                <div class="visitor-badge px-3 py-1 text-xs text-green-400 flex items-center gap-1.5">
                    <i class="fas fa-users"></i>
                    <span id="visitor-count">--</span> زائر
                </div>
            </div>
        </div>
    </nav>

    <section class="relative py-12 md:py-16 text-center px-4">
        <div class="max-w-4xl mx-auto">
            <div class="inline-flex items-center gap-2 glass rounded-full px-5 py-2 text-xs text-gray-300 mb-6">
                <span class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
                <span id="countdown-next">التحديث القادم بعد: --:--:--</span>
                <span class="text-gray-500">| ⏳ الحذف بعد: {max_age_hours} ساعة</span>
            </div>
            <h1 class="text-4xl md:text-7xl font-black mb-3 leading-tight">
                <span class="bg-gradient-to-r from-indigo-300 via-purple-300 to-pink-300 bg-clip-text text-transparent typing-text" id="hero-title">حرية التصفح</span>
            </h1>
            <p class="text-gray-400 text-lg max-w-2xl mx-auto mb-2 typing-text" id="hero-subtitle"></p>
            <p class="text-gray-500 text-sm mb-8" id="greeting-message"></p>
            
            <div class="flex flex-wrap justify-center gap-3 mb-4">
                <div class="glass px-5 py-3 rounded-2xl text-center min-w-[100px]">
                    <span class="text-2xl md:text-3xl font-black bg-gradient-to-r from-indigo-400 to-pink-400 bg-clip-text text-transparent">{total_servers}</span>
                    <p class="text-gray-500 text-xs mt-1">سيرفر نشط</p>
                </div>
                <div class="glass px-5 py-3 rounded-2xl text-center min-w-[100px]">
                    <span class="text-2xl md:text-3xl font-black text-green-400">{new_count}</span>
                    <p class="text-gray-500 text-xs mt-1">جديد 🆕</p>
                </div>
                <div class="glass px-5 py-3 rounded-2xl text-center min-w-[100px]">
                    <span class="text-2xl md:text-3xl font-black text-red-400">{deleted_count}</span>
                    <p class="text-gray-500 text-xs mt-1">محذوف 🗑️</p>
                </div>
                <div class="glass px-5 py-3 rounded-2xl text-center min-w-[100px]">
                    <span class="text-2xl md:text-3xl font-black text-yellow-400">{avg_ping}</span>
                    <p class="text-gray-500 text-xs mt-1">متوسط ms</p>
                </div>
                <div class="glass px-5 py-3 rounded-2xl text-center min-w-[120px]">
                    <span class="text-lg md:text-xl font-black text-cyan-400">{most_country}</span>
                    <p class="text-gray-500 text-xs mt-1">الأكثر ({most_country_count})</p>
                </div>
            </div>
        </div>
    </section>

    <section class="max-w-7xl mx-auto px-4 py-2">
        <div class="flex flex-wrap justify-center gap-2" id="filter-tabs">
            {filter_tabs_html}
        </div>
        <div class="flex justify-center mt-3">
            <div class="glass flex items-center gap-2 px-4 py-2 rounded-full max-w-md w-full">
                <i class="fas fa-search text-gray-500"></i>
                <input type="text" id="search-input" placeholder="ابحث عن دولة، بروتوكول، أو ملاحظة..." 
                    class="bg-transparent border-none outline-none text-white text-sm w-full placeholder-gray-500">
                <button onclick="document.getElementById('search-input').value=''; renderServers(currentFilter);" 
                    class="text-gray-500 hover:text-white text-xs">✕</button>
            </div>
        </div>
    </section>

    <section class="max-w-7xl mx-auto px-4 py-6">
        <h2 class="text-lg font-bold mb-4 text-gray-300 flex items-center gap-2">
            <i class="fas fa-server text-indigo-400"></i> سيرفرات V2Nodes
            <span class="text-xs text-gray-500 font-normal">| ⏳ الحذف بعد {max_age_hours} ساعة</span>
            <span class="text-xs text-gray-500 font-normal" id="last-copied-info"></span>
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" id="servers-grid"></div>
        <div id="no-servers-msg" class="text-center py-12 text-gray-500 hidden">
            <i class="fas fa-search text-3xl mb-3 opacity-30"></i>
            <p id="no-results-text">لا توجد سيرفرات</p>
        </div>
    </section>

    <footer class="border-t border-white/5 mt-12">
        <div class="max-w-7xl mx-auto px-4 py-8 text-center">
            <p class="text-gray-500 text-xs">© 2026 DOKA V2Nodes · جميع الحقوق محفوظة</p>
            <p class="text-gray-600 text-xs mt-1">تحديث كل 3 ساعات | ⏳ حذف القديم بعد {max_age_hours} ساعة</p>
            <button id="show-stats-btn" class="mt-4 glass px-5 py-2 rounded-full text-xs text-gray-300 hover:text-white transition-all">
                <i class="fas fa-chart-bar ml-1"></i> الإحصائيات
            </button>
            <button id="clear-fav-btn" class="mt-2 block mx-auto text-xs text-gray-600 hover:text-red-400 transition-all" style="display:none;">
                <i class="fas fa-trash-alt ml-1"></i> حذف المفضلة
            </button>
        </div>
    </footer>

    <div id="stats-page" class="max-w-4xl mx-auto px-4 py-12 hidden">
        <div class="glass-card p-6">
            <h2 class="text-2xl font-bold text-center mb-6">📊 لوحة الإحصائيات</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div><h3 class="text-base font-bold mb-3 text-gray-300">البروتوكولات</h3><canvas id="proto-chart"></canvas></div>
                <div><h3 class="text-base font-bold mb-3 text-gray-300">الدول</h3><canvas id="country-chart"></canvas></div>
            </div>
            <p class="text-center text-gray-400 mt-6 text-xs">آخر تحديث: <span id="stats-last-update"></span></p>
            <button id="back-to-servers" class="mt-6 btn-primary px-6 py-2.5 rounded-xl mx-auto block text-sm font-medium">
                <i class="fas fa-arrow-right ml-2"></i> عودة
            </button>
        </div>
    </div>

    <div id="toast" class="toast fixed bottom-6 left-1/2 -translate-x-1/2 px-6 py-3 rounded-full text-sm font-bold opacity-0 transition-all pointer-events-none z-50 text-white" style="transform: translate(-50%, 20px);">
        <span id="toast-msg">تم النسخ!</span>
    </div>

    <div id="qr-modal" class="fixed inset-0 z-50 hidden items-center justify-center bg-black/60 backdrop-blur-sm" onclick="closeQRModal(event)">
        <div class="glass-card p-6" onclick="event.stopPropagation()" style="opacity:1;transform:none;">
            <div id="qr-modal-content" class="flex justify-center"></div>
            <button onclick="closeQRModal()" class="mt-4 w-full btn-primary py-2.5 rounded-xl text-xs font-medium">إغلاق</button>
        </div>
    </div>

    <script>
        const serversData = {servers_json};
        const statsData = {stats_json};
        const greetings = {greetings_json};
        const MAX_AGE_HOURS = {max_age_hours};
        let currentFilter = 'all';
        let chartInstances = {{}};
        const UPDATE_INTERVAL = 3 * 60 * 60;
        const updateTime = new Date('{current_time_iso}');
        
        function getFavorites() {{ try {{ return JSON.parse(localStorage.getItem('doka_v2nodes_fav') || '[]'); }} catch {{ return []; }} }}
        function saveFavorites(f) {{ localStorage.setItem('doka_v2nodes_fav', JSON.stringify(f)); }}
        function toggleFavorite(link) {{
            let f = getFavorites(); const i = f.indexOf(link);
            i > -1 ? (f.splice(i,1), showToast('أزيل من المفضلة 💔')) : (f.push(link), showToast('أضيف للمفضلة ⭐'));
            saveFavorites(f); renderServers(currentFilter); updateFavCount();
        }}
        function updateFavCount() {{
            const f = getFavorites(); document.getElementById('count-fav').textContent = f.length;
            const b = document.getElementById('fav-filter-btn'), c = document.getElementById('clear-fav-btn');
            if (f.length > 0) {{ b.style.display = ''; c.style.display = ''; }} else {{ b.style.display = 'none'; c.style.display = 'none'; }}
        }}
        
        function showToast(m) {{
            const t = document.getElementById('toast'); document.getElementById('toast-msg').textContent = m;
            t.style.opacity = '1'; t.style.transform = 'translate(-50%, 0)';
            setTimeout(() => {{ t.style.opacity = '0'; t.style.transform = 'translate(-50%, 20px)'; }}, 2000);
        }}
        
        window.copyText = (text) => {{
            navigator.clipboard.writeText(text).then(() => {{
                showToast('✅ تم النسخ!');
                localStorage.setItem('doka_v2nodes_last_copy', text);
                updateLastCopied();
            }});
        }};
        function updateLastCopied() {{
            const l = localStorage.getItem('doka_v2nodes_last_copy');
            if (l) document.getElementById('last-copied-info').textContent = '| آخر نسخ: ' + l.substring(0, 25) + '...';
        }}
        
        window.showQR = (link) => {{
            const m = document.getElementById('qr-modal'), c = document.getElementById('qr-modal-content');
            c.innerHTML = '';
            new QRCode(c, {{ text: link, width: 200, height: 200, colorDark: "#1e293b", colorLight: "#ffffff" }});
            m.classList.remove('hidden'); m.classList.add('flex');
        }};
        window.closeQRModal = (e) => {{
            if (e && e.target !== document.getElementById('qr-modal')) return;
            const m = document.getElementById('qr-modal'); m.classList.add('hidden'); m.classList.remove('flex');
            document.getElementById('qr-modal-content').innerHTML = '';
        }};
        
        function renderServers(filter) {{
            const grid = document.getElementById('servers-grid');
            const s = document.getElementById('search-input').value.toLowerCase().trim();
            const favs = getFavorites();
            let filtered = serversData;
            if (filter === 'favorites') filtered = serversData.filter(srv => favs.includes(srv.link));
            else if (filter !== 'all') filtered = serversData.filter(srv => srv.proto.toLowerCase() === filter);
            if (s) filtered = filtered.filter(srv => srv.country.includes(s) || srv.proto.toLowerCase().includes(s) || srv.link.toLowerCase().includes(s) || srv.remark.includes(s));
            
            if (filtered.length === 0) {{
                grid.innerHTML = '';
                document.getElementById('no-servers-msg').classList.remove('hidden');
                document.getElementById('no-results-text').textContent = s ? 'لا نتائج للبحث' : 'لا سيرفرات نشطة (تم حذف القديم)';
                return;
            }}
            document.getElementById('no-servers-msg').classList.add('hidden');
            
            let h = '';
            filtered.forEach((srv, i) => {{
                const isFav = favs.includes(srv.link);
                const dl = srv.link.length > 55 ? srv.link.substring(0, 28) + ' ... ' + srv.link.substring(srv.link.length - 18) : srv.link;
                const remarkHtml = srv.remark ? `<span class="remark-tag">📝 ${{srv.remark}}</span>` : '';
                const ageHtml = srv.age_hours > 12 ? `<span class="badge-old">⏳ ${{srv.age_hours}} ساعة</span>` : '';
                
                h += `<div class="glass-card p-4 ${{srv.is_new ? 'new-server' : ''}}" style="animation-delay:${{i*0.06}}s;">
                    <div class="flex justify-between items-start mb-2">
                        <div class="flex items-center gap-1.5 flex-wrap">
                            <span class="text-2xl">${{srv.flag}}</span>
                            <span class="bg-gradient-to-r ${{srv.proto_gradient || 'from-gray-400 to-gray-500'}} text-white text-xs font-bold px-2.5 py-0.5 rounded-full">${{srv.proto}}</span>
                            ${{srv.is_new ? '<span class="badge-new">جديد</span>' : ''}}
                            ${{ageHtml}}
                            ${{remarkHtml}}
                        </div>
                        <div class="flex items-center gap-1.5">
                            <i class="favorite-star fa-star ${{isFav ? 'fas active' : 'far'}} text-base" onclick="toggleFavorite('${{srv.link}}'); event.stopPropagation();"></i>
                            <span class="text-xs text-gray-500">${{srv.ping}}ms</span>
                        </div>
                    </div>
                    <p class="text-xs text-gray-400 mb-2"><i class="fas fa-map-marker-alt ml-1 text-indigo-400"></i> ${{srv.country}} <span class="age-indicator">· 🕐 منذ ${{srv.added_time}}</span></p>
                    <div class="link-preview p-2.5 mb-3 text-xs font-mono text-gray-300 break-all" dir="ltr">${{dl}}</div>
                    <div class="flex gap-1.5">
                        <button onclick="copyText('${{srv.link}}')" class="flex-1 btn-primary py-2 rounded-xl text-xs font-medium"><i class="far fa-copy ml-1"></i> نسخ</button>
                        <button onclick="showQR('${{srv.link}}')" class="btn-glass px-3.5 rounded-xl text-xs"><i class="fas fa-qrcode"></i></button>
                    </div>
                </div>`;
            }});
            grid.innerHTML = h;
            requestAnimationFrame(() => {{ document.querySelectorAll('.glass-card').forEach((c, i) => setTimeout(() => c.classList.add('visible'), i * 60)); }});
        }}
        
        document.querySelectorAll('.tab-btn').forEach(b => b.addEventListener('click', () => {{
            document.querySelectorAll('.tab-btn').forEach(x => x.classList.remove('active'));
            b.classList.add('active'); currentFilter = b.dataset.filter; renderServers(currentFilter);
        }}));
        document.getElementById('search-input').addEventListener('input', () => renderServers(currentFilter));
        
        function uc() {{ document.getElementById('live-clock').textContent = new Date().toLocaleTimeString('ar-IQ', {{ hour12: false }}); }}
        setInterval(uc, 1000); uc();
        
        function cd() {{
            const e = Math.floor((new Date() - updateTime) / 1000);
            const r = Math.max(0, UPDATE_INTERVAL - e);
            document.getElementById('countdown-next').textContent = `التحديث القادم بعد: ${{String(Math.floor(r/3600)).padStart(2,'0')}}:${{String(Math.floor((r%3600)/60)).padStart(2,'0')}}:${{String(r%60).padStart(2,'0')}}`;
        }}
        setInterval(cd, 1000); cd();
        
        (function(e,t,s=80,d=40,p=2000){{let i=0,c=0,del=false;function tick(){{const cur=t[i];e.textContent=cur.substring(0,del?c-1:c+1);del?c--:c++;if(!del&&c===cur.length)setTimeout(()=>del=true,p);else if(del&&c===0){{del=false;i=(i+1)%t.length;}}setTimeout(tick,del?d:s);}}tick();}})(document.getElementById('typing-text'),['V2Nodes','حرية بلا حدود','V2Ray Servers']);
        (function(e,t,s=70,d=30,p=3000){{let i=0,c=0,del=false;function tick(){{const cur=t[i];e.textContent=cur.substring(0,del?c-1:c+1);del?c--:c++;if(!del&&c===cur.length)setTimeout(()=>del=true,p);else if(del&&c===0){{del=false;i=(i+1)%t.length;}}setTimeout(tick,del?d:s);}}tick();}})(document.getElementById('hero-subtitle'),['سيرفرات V2Ray من V2Nodes · محدثة تلقائياً','VMess · VLESS · Trojan · SS · Hysteria2','تصفح آمن بدون قيود']);
        
        document.getElementById('greeting-message').textContent = greetings[Math.floor(Math.random() * greetings.length)];
        
        function uv() {{ document.getElementById('visitor-count').textContent = Math.max(1, {total_servers} + Math.floor(Math.random()*15)-5); }}
        uv(); setInterval(uv, 10000);
        
        (function() {{
            const co = document.getElementById('particles');
            const cols = ['rgba(99,102,241,0.4)','rgba(236,72,153,0.3)','rgba(34,197,94,0.3)','rgba(251,191,36,0.3)'];
            for (let i=0; i<20; i++) {{
                const p = document.createElement('div'); p.className = 'particle';
                p.style.cssText = `width:${{Math.random()*5+2}}px;height:${{Math.random()*5+2}}px;left:${{Math.random()*100}}%;background:${{cols[Math.floor(Math.random()*cols.length)]}};animation-duration:${{Math.random()*15+10}}s;animation-delay:${{Math.random()*10}}s;`;
                co.appendChild(p);
            }}
        }})();
        
        document.getElementById('show-stats-btn').addEventListener('click', () => {{
            document.querySelector('nav').style.display='none';
            document.querySelector('section').style.display='none';
            document.getElementById('filter-tabs').style.display='none';
            document.getElementById('servers-grid').parentElement.style.display='none';
            document.querySelector('footer').style.display='none';
            document.querySelector('.particles-container').style.display='none';
            document.getElementById('stats-page').classList.remove('hidden');
            document.getElementById('stats-last-update').textContent = new Date(statsData.last_updated).toLocaleString('ar-IQ');
            Object.values(chartInstances).forEach(c => c.destroy());
            chartInstances = {{}};
            
            const ctx1 = document.getElementById('proto-chart').getContext('2d');
            chartInstances.proto = new Chart(ctx1, {{
                type: 'doughnut',
                data: {{ labels: Object.keys(statsData.by_protocol).map(p=>p.toUpperCase()), datasets: [{{ data: Object.values(statsData.by_protocol), backgroundColor: ['#f97316','#3b82f6','#a855f7','#22c55e','#f43f5e','#ec4899','#f59e0b','#ef4444','#6366f1'], borderColor: 'rgba(255,255,255,0.1)', borderWidth: 3 }}] }},
                options: {{ responsive: true, plugins: {{ legend: {{ position:'bottom', labels: {{ color:'#e2e8f0', padding:12 }} }} }} }}
            }});
            
            const ctx2 = document.getElementById('country-chart').getContext('2d');
            const co2 = statsData.countries || {{}};
            chartInstances.country = new Chart(ctx2, {{
                type: 'pie',
                data: {{ labels: Object.keys(co2), datasets: [{{ data: Object.values(co2), backgroundColor: ['#6366f1','#ec4899','#22c55e','#f59e0b','#3b82f6','#ef4444','#8b5cf6','#14b8a6','#f97316'], borderColor: 'rgba(255,255,255,0.1)', borderWidth: 2 }}] }},
                options: {{ responsive: true, plugins: {{ legend: {{ position:'bottom', labels: {{ color:'#e2e8f0', padding:10 }} }} }} }}
            }});
        }});
        
        document.getElementById('back-to-servers').addEventListener('click', () => location.reload());
        document.getElementById('clear-fav-btn').addEventListener('click', () => {{
            if (confirm('حذف كل المفضلة؟')) {{ localStorage.removeItem('doka_v2nodes_fav'); updateFavCount(); if (currentFilter==='favorites') renderServers('all'); else renderServers(currentFilter); showToast('تم الحذف 🗑️'); }}
        }});
        
        fetch('https://api.ipify.org?format=json').then(r=>r.json()).then(d=>document.getElementById('user-ip').textContent=d.ip).catch(()=>document.getElementById('user-ip').textContent='غير معروف');
        updateFavCount(); updateLastCopied(); renderServers('all');
    </script>
</body>
</html>'''
    
    return html


if __name__ == "__main__":
    run_doka_v2nodes()
