#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DOKA PRO - Triple Source Mobile Edition 2025
Sources: Exclave VPN + V2ray_Collector + V2RayRootFree
Optimized 100% for Mobile - PWA Ready - Real Ping
"""

from __future__ import annotations

import json
import re
import random
import socket
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Final

import requests

# ==================== الثوابت ====================
SOURCES: Final[dict[str, str]] = {
    "exclave": "https://t.me/s/exclaveVPN",
    "collector": "https://t.me/s/v2nodes",
    "v2root": "https://t.me/s/V2RayRootFree",
}

OUTPUT_FILE: Final[Path] = Path("index.html")
DATA_FILE: Final[Path] = Path("stats.json")
MANIFEST_FILE: Final[Path] = Path("manifest.json")

SUPPORTED_PROTOCOLS: Final[tuple[str, ...]] = ("vmess", "vless", "trojan", "ss", "hysteria2")

REQUEST_HEADERS: Final[dict[str, str]] = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ar-IQ,ar;q=0.9,en;q=0.8",
}

COUNTRY_HINTS: Final[dict[str, str]] = {
    "singapore": "🇸🇬", "germany": "🇩🇪", "netherlands": "🇳🇱",
    "united states": "🇺🇸", "usa": "🇺🇸", "united kingdom": "🇬🇧",
    "japan": "🇯🇵", "france": "🇫🇷", "canada": "🇨🇦",
    "hong kong": "🇭🇰", "uae": "🇦🇪", "turkey": "🇹🇷",
    "india": "🇮🇳", "brazil": "🇧🇷", "russia": "🇷🇺",
    "australia": "🇦🇺", "south korea": "🇰🇷",
}

PROTOCOL_COLORS: Final[dict[str, str]] = {
    "vmess": "#8b5cf6", "vless": "#06b6d4", "trojan": "#f59e0b",
    "ss": "#10b981", "hysteria2": "#ec4899", "unknown": "#6366f1",
}

PROTOCOL_ICONS: Final[dict[str, str]] = {
    "vmess": "fa-bolt", "vless": "fa-feather", "trojan": "fa-shield-haltered",
    "ss": "fa-ghost", "hysteria2": "fa-fire", "unknown": "fa-cube",
}

SOURCE_ICONS: Final[dict[str, str]] = {
    "exclave": "⬡", "collector": "📡", "v2root": "🌐",
}


# ==================== دوال Ping ====================
def extract_host(url: str) -> str | None:
    try:
        if "://" not in url: return None
        encoded = url.split("://", 1)[1]
        if "?" in encoded: encoded = encoded.split("?")[1] if "?" in encoded else encoded
        if url.startswith("vmess://"):
            import base64
            decoded = base64.b64decode(encoded).decode("utf-8", errors="ignore")
            return json.loads(decoded).get("add")
        for part in encoded.split("@"):
            c = part.split(":")[0]
            if "." in c and not c.startswith(("http","tcp","ws","grpc","hysteria","exclave")): return c
        sni = re.search(r'sni=([^&]+)', encoded)
        if sni: return sni.group(1)
        return None
    except: return None

def tcp_ping(host: str) -> int | None:
    try:
        start = time.monotonic()
        with socket.create_connection((host, 443), timeout=1.5):
            return int((time.monotonic() - start) * 1000)
    except: return None

def ping_server(url: str) -> tuple[int | None, bool]:
    host = extract_host(url)
    if not host: return None, False
    for _ in range(2):
        r = tcp_ping(host)
        if r: return r, True
    return None, False

def measure_pings(servers: list[dict]) -> list[dict]:
    print(f"🧪 فحص {len(servers)} سيرفر...")
    with ThreadPoolExecutor(max_workers=30) as ex:
        futures = {ex.submit(ping_server, s["url"]): i for i, s in enumerate(servers)}
        for f in as_completed(futures):
            i = futures[f]
            p, a = f.result()
            servers[i]["ping"] = p if p else random.randint(200, 400)
            servers[i]["alive"] = a
    return servers


# ==================== دوال الجلب ====================
def fetch_page(url: str, name: str) -> str:
    print(f"📥 جلب {name}...")
    try:
        r = requests.get(url, headers=REQUEST_HEADERS, timeout=30)
        r.raise_for_status()
        return r.text
    except Exception as e:
        print(f"❌ {name}: {e}")
        return ""

def extract_links(html: str, source: str) -> list[str]:
    """استخراج الروابط حسب المصدر."""
    if source == "exclave":
        pattern = r'exclave://[^\s<"\'\s]+'
    else:
        protocols = "|".join(SUPPORTED_PROTOCOLS)
        pattern = rf"(?:{protocols})://[^\s<>\"'\s]+"
    
    matches = re.findall(pattern, html, re.IGNORECASE)
    seen: set[str] = set()
    clean: list[str] = []
    for link in matches:
        cleaned = link.replace("&amp;", "&").split("<")[0].split('"')[0].strip()
        if cleaned not in seen:
            seen.add(cleaned)
            clean.append(cleaned)
    return clean

def extract_proto(url: str) -> str:
    url_lower = url.lower()
    for proto in SUPPORTED_PROTOCOLS:
        if f"://{proto}" in url_lower or f"exclave://{proto}" in url_lower:
            return proto.upper()
    return "UNKNOWN"

def detect_country(url: str) -> str:
    for hint, flag in COUNTRY_HINTS.items():
        if hint in url.lower(): return flag
    return "🌍"

def build_servers(links: list[str], source: str) -> list[dict]:
    servers = []
    for link in links:
        proto = extract_proto(link)
        servers.append({
            "url": link, "proto": proto,
            "country": detect_country(link),
            "ping": random.randint(100, 300),
            "alive": False, "source": source,
        })
    return servers


# ==================== توليد Manifest ====================
def gen_manifest() -> str:
    m = {
        "name": "DOKA PRO V2Ray",
        "short_name": "DOKA PRO",
        "description": "أضخم تجميعة سيرفرات V2Ray للهاتف - 3 مصادر",
        "start_url": "/index.html",
        "display": "standalone",
        "orientation": "portrait",
        "background_color": "#0f172a",
        "theme_color": "#8b5cf6",
        "lang": "ar", "dir": "rtl",
        "icons": [{
            "src": "data:image/svg+xml," + (
                "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 512 512'%3E"
                "%3Cdefs%3E%3ClinearGradient id='bg' x1='0%25' y1='0%25' x2='100%25' y2='100%25'%3E"
                "%3Cstop offset='0%25' style='stop-color:%238b5cf6'/%3E%3Cstop offset='100%25' style='stop-color:%234f46e5'/%3E"
                "%3C/linearGradient%3E%3C/defs%3E"
                "%3Crect width='512' height='512' rx='120' fill='url(%23bg)'/%3E"
                "%3Ctext x='256' y='320' text-anchor='middle' font-family='Arial' font-size='220' fill='white' opacity='0.95'%3E🌐%3C/text%3E"
                "%3Ctext x='256' y='400' text-anchor='middle' font-family='Arial' font-weight='bold' font-size='60' fill='white'%3EDOKA%3C/text%3E"
                "%3C/svg%3E"
            ),
            "sizes": "512x512", "type": "image/svg+xml", "purpose": "any maskable"
        }]
    }
    return json.dumps(m, indent=2, ensure_ascii=False)


# ==================== توليد HTML (هاتف) ====================
def gen_html(servers: list[dict], total: int, src_counts: dict) -> str:
    now = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M")
    servers_json = json.dumps(servers, ensure_ascii=False)
    alive = sum(1 for s in servers if s["alive"])

    counts: dict[str, int] = {}
    for s in servers:
        p = s["proto"].lower()
        counts[p] = counts.get(p, 0) + 1

    stats = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "total": total, "alive": alive,
        "by_protocol": counts, "by_source": src_counts,
    }
    DATA_FILE.write_text(json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8")
    MANIFEST_FILE.write_text(gen_manifest(), encoding="utf-8")

    # أزرار البروتوكول
    proto_btns = ""
    for proto in SUPPORTED_PROTOCOLS:
        cnt = counts.get(proto, 0)
        if cnt > 0:
            color = PROTOCOL_COLORS[proto]
            proto_btns += f"""<button class="chip" data-filter="{proto}" style="--c:{color}">{proto.upper()} <span class="cnt">{cnt}</span></button>"""

    # أزرار المصادر
    source_btns = ""
    for src, cnt in src_counts.items():
        if cnt > 0:
            icon = SOURCE_ICONS.get(src, "")
            source_btns += f"""<button class="chip" data-filter="{src}" style="--c:#6366f1">{icon} {src} <span class="cnt">{cnt}</span></button>"""

    return f"""\
<!DOCTYPE html><html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <meta name="theme-color" content="#8b5cf6">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="DOKA PRO">
    <title>DOKA PRO • V2Ray</title>
    <link rel="manifest" href="manifest.json">
    <link rel="apple-touch-icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 512 512'%3E%3Crect width='512' height='512' rx='120' fill='%238b5cf6'/%3E%3Ctext x='256' y='320' text-anchor='middle' font-size='220' fill='white'%3E🌐%3C/text%3E%3C/svg%3E">
    <link rel="preconnect" href="https://fonts.googleapis.com"><link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        :root {{ --bg: #0f172a; --surface: #1e293b; --border: #334155; --text: #f1f5f9; --sub: #94a3b8; --pri: #8b5cf6; --suc: #10b981; --dan: #ef4444; }}
        * {{ margin:0; padding:0; box-sizing:border-box; }}
        body {{ font-family: 'Cairo', sans-serif; background: var(--bg); color: var(--text); min-height: 100vh; padding: 12px 12px 32px; padding-top: max(12px, env(safe-area-inset-top)); }}
        .container {{ max-width: 480px; margin: 0 auto; }}
        
        .header {{ display:flex; align-items:center; justify-content:space-between; margin-bottom: 20px; }}
        .logo {{ font-size:1.5rem; font-weight:900; background: linear-gradient(135deg, #8b5cf6, #6366f1); -webkit-background-clip:text; -webkit-text-fill-color:transparent; }}
        .live {{ display:flex; align-items:center; gap:6px; background:var(--surface); padding:6px 14px; border-radius:50px; font-size:0.7rem; font-weight:600; border:1px solid var(--border); }}
        .live-dot {{ width:8px; height:8px; background:var(--suc); border-radius:50%; animation:pulse 2s infinite; }}
        @keyframes pulse {{ 0%,100% {{ box-shadow:0 0 0 0 rgba(16,185,129,0.4); }} 50% {{ box-shadow:0 0 0 10px rgba(16,185,129,0); }} }}
        
        .stats-row {{ display:flex; gap:10px; margin-bottom:20px; }}
        .stat {{ flex:1; background:var(--surface); border:1px solid var(--border); border-radius:20px; padding:16px 10px; text-align:center; }}
        .stat-num {{ font-size:1.8rem; font-weight:900; line-height:1; }}
        .stat-lbl {{ font-size:0.65rem; color:var(--sub); margin-top:4px; }}
        
        .section-title {{ font-size:0.7rem; color:var(--sub); margin-bottom:8px; font-weight:600; }}
        .filters {{ display:flex; gap:6px; overflow-x:auto; padding-bottom:8px; margin-bottom:14px; -webkit-overflow-scrolling:touch; scrollbar-width:none; }}
        .filters::-webkit-scrollbar {{ display:none; }}
        .chip {{ padding:8px 18px; border-radius:50px; border:1px solid var(--border); background:var(--surface); color:var(--sub); font-family:'Cairo',sans-serif; font-weight:700; font-size:0.8rem; white-space:nowrap; cursor:pointer; transition:all 0.2s; display:flex; align-items:center; gap:6px; }}
        .chip.active {{ background:var(--pri); color:white; border-color:transparent; }}
        .cnt {{ font-size:0.65rem; background:rgba(255,255,255,0.2); padding:2px 6px; border-radius:50px; }}
        
        .card {{ background:var(--surface); border:1px solid var(--border); border-radius:20px; padding:16px; margin-bottom:12px; }}
        .card-row {{ display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; }}
        .badge {{ display:flex; align-items:center; gap:6px; }}
        .flag {{ font-size:1.5rem; }}
        .tag {{ padding:4px 10px; border-radius:50px; font-size:0.65rem; font-weight:700; color:white; }}
        .status {{ font-size:0.65rem; font-weight:600; display:flex; align-items:center; gap:3px; }}
        .dot {{ width:5px; height:5px; border-radius:50%; }}
        .dot-up {{ background:var(--suc); }} .dot-down {{ background:var(--dan); }}
        .url-box {{ background:#0f172a; padding:10px 12px; border-radius:12px; font-family:monospace; font-size:0.65rem; color:var(--sub); direction:ltr; text-align:left; word-break:break-all; margin-bottom:10px; }}
        .actions {{ display:flex; gap:8px; }}
        .btn {{ flex:1; padding:12px; border-radius:14px; border:none; font-family:'Cairo',sans-serif; font-weight:700; font-size:0.8rem; cursor:pointer; transition:all 0.2s; display:flex; align-items:center; justify-content:center; gap:6px; color:white; }}
        .btn:active {{ transform:scale(0.96); }}
        .btn-qr {{ width:44px; height:44px; border-radius:14px; border:1px solid var(--border); background:var(--surface); color:var(--text); cursor:pointer; font-size:1rem; flex-shrink:0; }}
        .qr-box {{ margin-top:10px; padding:16px; background:white; border-radius:14px; display:none; justify-content:center; }}
        
        .toast {{ position:fixed; bottom:30px; left:50%; transform:translateX(-50%) translateY(100px); background:#10b981; color:white; padding:12px 24px; border-radius:50px; font-weight:700; font-size:0.85rem; z-index:999; opacity:0; transition:all 0.3s; }}
        .toast.on {{ opacity:1; transform:translateX(-50%) translateY(0); }}
        .stats-page {{ max-width:480px; margin:40px auto; padding:16px; text-align:center; }}
        .stats-card {{ background:var(--surface); border:1px solid var(--border); border-radius:24px; padding:32px 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="logo">🌐 DOKA PRO</div>
            <div class="live"><div class="live-dot"></div> {alive} حي</div>
        </div>

        <div class="stats-row">
            <div class="stat"><div class="stat-num" style="color:#8b5cf6;">{total}</div><div class="stat-lbl">🔰 الإجمالي</div></div>
            <div class="stat"><div class="stat-num" style="color:#10b981;">{alive}</div><div class="stat-lbl">⚡ أونلاين</div></div>
            <div class="stat"><div class="stat-num" style="color:#f59e0b;">{len(src_counts)}</div><div class="stat-lbl">📡 مصادر</div></div>
        </div>

        <div class="section-title">📡 فلترة بالمصدر</div>
        <div class="filters" id="source-filters">
            <button class="chip active" data-filter="all" style="--c:#8b5cf6">🌐 الكل <span class="cnt">{total}</span></button>
            {source_btns}
        </div>

        <div class="section-title">🧩 فلترة بالبروتوكول</div>
        <div class="filters" id="proto-filters">
            {proto_btns}
        </div>

        <div id="list"></div>
        <div id="empty" style="display:none; text-align:center; color:var(--sub); padding:40px;">😴 لا توجد سيرفرات</div>
    </div>

    <div class="toast" id="toast">✅ تم النسخ!</div>

    <div class="stats-page" id="stats-pg" style="display:none;">
        <div class="stats-card">
            <h2 style="margin-bottom:20px;">📊 الإحصائيات</h2>
            <canvas id="chart" style="max-height:300px;"></canvas>
            <p style="color:var(--sub); margin-top:16px;">آخر تحديث: <span id="last-up"></span></p>
            <button onclick="location.reload()" style="margin-top:20px; padding:14px 40px; border-radius:50px; border:none; background:#8b5cf6; color:white; font-family:'Cairo',sans-serif; font-weight:700; cursor:pointer;">⬅️ عودة</button>
        </div>
    </div>

    <div style="text-align:center; padding:20px; color:var(--sub); font-size:0.7rem;">
        © 2026 DOKA PRO • 3 مصادر • <button id="stats-btn" style="background:none; border:none; color:#8b5cf6; cursor:pointer; font-family:'Cairo',sans-serif;">📊 إحصائيات</button>
    </div>

    <script>
        const data = {servers_json};
        const colors = {json.dumps(PROTOCOL_COLORS)};
        const icons = {json.dumps(PROTOCOL_ICONS)};
        const srcIcons = {json.dumps(SOURCE_ICONS)};
        let filter = 'all', chartInst = null;

        function render(f) {{
            filter = f;
            const list = document.getElementById('list');
            let filtered = f === 'all' ? data : data.filter(s => {{
                if (['exclave','collector','v2root'].includes(f)) return s.source === f;
                return s.proto.toLowerCase() === f;
            }});
            if(!filtered.length) {{ list.innerHTML = ''; document.getElementById('empty').style.display='block'; return; }}
            document.getElementById('empty').style.display='none';
            list.innerHTML = filtered.map((s,i) => {{
                const c = colors[s.proto.toLowerCase()] || '#8b5cf6';
                const ic = icons[s.proto.toLowerCase()] || 'fa-link';
                const up = s.alive;
                const srcIcon = srcIcons[s.source] || '';
                return `<div class="card">
                    <div class="card-row">
                        <div class="badge">
                            <span class="flag">${{s.country}}</span>
                            <span class="tag" style="background:${{c}}"><i class="fas ${{ic}}"></i> ${{s.proto}}</span>
                            <span class="status" style="color:${{up?'var(--suc)':'var(--dan)'}}"><span class="dot ${{up?'dot-up':'dot-down'}}"></span> ${{up?'حي':'ميت'}}</span>
                            <span style="font-size:0.7rem;" title="${{s.source}}">${{srcIcon}}</span>
                        </div>
                        <span style="font-size:0.65rem; color:var(--sub);">${{up?s.ping+'ms':'---'}}</span>
                    </div>
                    <div class="url-box">${{s.url}}</div>
                    <div class="actions">
                        <button class="btn" style="background:${{c}}" onclick="cp('${{s.url.replace(/'/g, "\\'")}}')"><i class="far fa-copy"></i> نسخ</button>
                        <button class="btn-qr" onclick="qr('q${{i}}','${{s.url.replace(/'/g, "\\'")}}')"><i class="fas fa-qrcode"></i></button>
                    </div>
                    <div class="qr-box" id="q${{i}}"></div>
                </div>`;
            }}).join('');
        }}

        document.querySelectorAll('.chip').forEach(c => c.addEventListener('click', function() {{
            // تفعيل الزر في كل مجموعات الفلترة
            document.querySelectorAll('.chip').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            // لو ضغط على بروتوكول، نخلي المصدر يعود للكل
            render(this.dataset.filter);
        }}));

        window.cp = t => {{ navigator.clipboard.writeText(t); const toast=document.getElementById('toast'); toast.classList.add('on'); clearTimeout(toast._t); toast._t=setTimeout(()=>toast.classList.remove('on'), 2000); }};
        window.qr = (id, link) => {{ const el=document.getElementById(id); if(el.style.display==='flex') {{ el.style.display='none'; return; }} if(!el.innerHTML) new QRCode(el, {{text:link, width:140, height:140, colorDark:'#1e293b'}}); el.style.display='flex'; }};

        document.getElementById('stats-btn').addEventListener('click', async () => {{
            document.querySelector('.header').style.display='none';
            document.querySelectorAll('.stats-row,.section-title,.filters').forEach(e=>e.style.display='none');
            document.getElementById('list').style.display='none';
            document.querySelector('[style*="text-align:center; padding:20px"]').style.display='none';
            document.getElementById('stats-pg').style.display='block';
            try {{
                const res = await fetch('stats.json');
                const stats = await res.json();
                document.getElementById('last-up').innerText = new Date(stats.last_updated).toLocaleString('ar-SA');
                const ctx = document.getElementById('chart').getContext('2d');
                if(chartInst) chartInst.destroy();
                const labels = Object.keys(stats.by_protocol).map(p=>p.toUpperCase());
                chartInst = new Chart(ctx, {{
                    type:'doughnut',
                    data:{{ labels, datasets:[{{ data:Object.values(stats.by_protocol), backgroundColor:labels.map(l=>colors[l.toLowerCase()]||'#8b5cf6'), borderColor:'#0f172a', borderWidth:3 }}] }},
                    options:{{ responsive:true, plugins:{{ legend:{{ position:'bottom', labels:{{ padding:16, font:{{family:'Cairo',size:13}}, color:'#94a3b8' }} }} }} }}
                }});
            }} catch(e) {{}}
        }});

        render('all');
        console.log('%c🚀 DOKA PRO %c3 Sources %c📱', 'color:#8b5cf6;font-size:1.5rem;font-weight:900;', 'color:#f59e0b;', 'color:#10b981;');
    </script>
</body>
</html>"""


# ==================== الدالة الرئيسية ====================
def main() -> None:
    print("🚀 DOKA PRO - 3 مصادر للهاتف")
    print("=" * 40)

    all_servers: list[dict] = []
    src_counts: dict[str, int] = {}

    for src_name, url in SOURCES.items():
        html = fetch_page(url, src_name)
        if not html: continue
        links = extract_links(html, src_name)
        src_counts[src_name] = len(links)
        all_servers.extend(build_servers(links, src_name))
        print(f"   ✅ {src_name}: {len(links)}")

    # إزالة التكرار
    seen_urls = set()
    unique_servers = []
    for s in all_servers:
        if s["url"] not in seen_urls:
            seen_urls.add(s["url"])
            unique_servers.append(s)
    all_servers = unique_servers

    if not all_servers:
        print("⚠️ لا توجد سيرفرات!")
        return

    print(f"\n📊 إجمالي فريد: {len(all_servers)}")

    # Ping
    all_servers = measure_pings(all_servers)

    # توليد
    total = len(all_servers)
    html = gen_html(all_servers, total, src_counts)
    OUTPUT_FILE.write_text(html, encoding="utf-8")

    alive = sum(1 for s in all_servers if s["alive"])
    print(f"\n🎉 تم! {total} سيرفر ({alive} حي)")
    for src, cnt in src_counts.items():
        print(f"   • {src}: {cnt}")
    print(f"   📱 تصميم هاتف - PWA جاهز")


if __name__ == "__main__":
    main()
