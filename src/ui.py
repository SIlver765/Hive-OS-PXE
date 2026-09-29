"""HTML/CSS/JS for the admin UI. No dependencies, no build step, no external requests."""
import html, re, threading

_ctx = threading.local()

def set_base(b): _ctx.base = b
def base(): return getattr(_ctx, "base", "./")

_ABS = re.compile(r"""(href|action)=(["'])/(?!/)([^"']*)\2""")

def rel(page):
    """Rewrite root-absolute href/action URLs to base-relative ones so the app works mounted at any path (e.g. /apps/<id>/)."""
    return _ABS.sub(lambda m: f'{m.group(1)}={m.group(2)}{m.group(3) or "./"}{m.group(2)}', page)

def e(s): return html.escape(str(s), quote=True)

ICONS = {  # 24x24 stroke icons (lucide-style)
    "status": '<rect x="3" y="3" width="7" height="9" rx="1.5"/><rect x="14" y="3" width="7" height="5" rx="1.5"/><rect x="14" y="12" width="7" height="9" rx="1.5"/><rect x="3" y="16" width="7" height="5" rx="1.5"/>',
    "rigs": '<rect x="2" y="3" width="20" height="7" rx="2"/><rect x="2" y="14" width="20" height="7" rx="2"/><path d="M6 6.5h.01M6 17.5h.01M10 6.5h5M10 17.5h5"/>',
    "groups": '<path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 13 9 5 9-5"/>',
    "image": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="2.5"/><path d="M12 3a9 9 0 0 1 9 9"/>',
    "settings": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1Z"/>',
    "key": '<circle cx="7.5" cy="15.5" r="4.5"/><path d="m10.7 12.3 9.3-9.3M16 7l3 3"/>',
    "logout": '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "alert": '<path d="M12 9v4M12 17h.01"/><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0Z"/>',
    "refresh": '<path d="M3 12a9 9 0 0 1 15.5-6.3L21 8M21 3v5h-5M21 12a9 9 0 0 1-15.5 6.3L3 16M3 21v-5h5"/>',
    "edit": '<path d="M12 20h9M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/>',
    "trash": '<path d="M3 6h18M8 6V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>',
    "skip": '<path d="m5 4 10 8-10 8V4ZM19 5v14"/>',
    "copy": '<rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "upload": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M7 10l5 5 5-5M12 15V3"/>',
    "guide": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V3H6.5A2.5 2.5 0 0 0 4 5.5v14Z"/><path d="M4 19.5A2.5 2.5 0 0 0 6.5 22H20v-5M9 8h7M9 12h5"/>',
    "server": '<rect x="2" y="2" width="20" height="8" rx="2"/><rect x="2" y="14" width="20" height="8" rx="2"/><path d="M6 6h.01M6 18h.01"/>',
}

def icon(name, size=18):
    return (f'<svg class="i" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>')

CSS = """
:root{color-scheme:light dark;--bg:#f4f5f7;--sf:#fff;--sf2:#f0f2f5;--fg:#14171c;--mut:#667085;--bd:#e3e6eb;--ac:#f5a623;--acfg:#1a1200;--acd:#b45309;
--ok:#15803d;--okbg:#dcfce7;--bad:#b91c1c;--badbg:#fee2e2;--inf:#1d4ed8;--infbg:#dbeafe;--warn:#a16207;--warnbg:#fef3c7;--sh:0 1px 2px #0000000d,0 4px 16px #0000000a}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0d0f12;--sf:#15181d;--sf2:#1b1f26;--fg:#e8eaee;--mut:#8a93a2;--bd:#262b33;--acd:#f5a623;
--ok:#4ade80;--okbg:#0f2e1a;--bad:#f87171;--badbg:#3a1414;--inf:#7db3ff;--infbg:#122543;--warn:#facc15;--warnbg:#33290b;--sh:none}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:14.5px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:var(--acd);text-decoration:none}a:hover{text-decoration:underline}
.i{flex:none;vertical-align:-3px}
.app{display:grid;grid-template-columns:230px minmax(0,1fr);min-height:100vh}
aside{background:var(--sf);border-right:1px solid var(--bd);padding:18px 12px;display:flex;flex-direction:column;gap:2px;position:sticky;top:0;height:100vh}
.brand{display:flex;align-items:center;gap:10px;padding:4px 10px 18px;font-weight:700;font-size:15px}
.brand b{display:grid;place-items:center;width:32px;height:32px;border-radius:9px;background:var(--ac);color:var(--acfg);font-size:11px;letter-spacing:.5px}
.brand small{display:block;font-weight:500;color:var(--mut);font-size:11.5px;margin-top:-2px}
aside a,aside button.nav{display:flex;align-items:center;gap:10px;padding:9px 12px;border-radius:9px;color:var(--fg);font-weight:500;background:none;border:0;width:100%;font-size:14.5px;cursor:pointer;text-align:left}
aside a:hover,aside button.nav:hover{background:var(--sf2);text-decoration:none}
aside a.on{background:color-mix(in srgb,var(--ac) 18%,transparent);color:var(--fg)}aside a.on .i{color:var(--acd)}
aside .sp{flex:1}
main{padding:28px 32px 60px;max-width:1080px;width:100%;min-width:0}
.ph{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;margin-bottom:22px;flex-wrap:wrap}
h1{font-size:24px;margin:0;letter-spacing:-.02em}.sub{color:var(--mut);margin:2px 0 0}
h2{font-size:15px;margin:0 0 12px;font-weight:650}
.card{background:var(--sf);border:1px solid var(--bd);border-radius:14px;padding:18px 20px;margin-bottom:16px;box-shadow:var(--sh)}
.grid{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));margin-bottom:16px}
.grid .card{margin:0}
.stat .k{color:var(--mut);font-size:12.5px;font-weight:550;text-transform:uppercase;letter-spacing:.05em;display:flex;align-items:center;gap:6px}
.stat .v{font-size:22px;font-weight:700;margin-top:6px;letter-spacing:-.01em;word-break:break-word}
.stat .s{color:var(--mut);font-size:13px;margin-top:2px}
table{width:100%;border-collapse:collapse}
th{font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:var(--mut);text-align:left;font-weight:600;padding:0 12px 8px}
td{padding:11px 12px;border-top:1px solid var(--bd);vertical-align:middle}
tr:hover td{background:var(--sf2)}
.tw{overflow-x:auto;margin:0 -8px}.tw table{min-width:640px}
code,.mono{font:13px ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
.mut{color:var(--mut)}.r{text-align:right;white-space:nowrap}
.badge{display:inline-flex;align-items:center;gap:6px;padding:2px 10px;border-radius:99px;font-size:12.5px;font-weight:600;background:var(--sf2);color:var(--mut)}
.badge::before{content:"";width:7px;height:7px;border-radius:50%;background:currentColor}
.b-done,.b-ok{background:var(--okbg);color:var(--ok)}.b-failed,.b-bad{background:var(--badbg);color:var(--bad)}
.b-flashing,.b-info{background:var(--infbg);color:var(--inf)}.b-flashing::before{animation:pulse 1.1s infinite}
.b-warn{background:var(--warnbg);color:var(--warn)}.b-skip{background:var(--sf2);color:var(--mut)}
@keyframes pulse{50%{opacity:.25}}
.bar{height:8px;background:var(--sf2);border-radius:99px;overflow:hidden;min-width:90px}
.bar i{display:block;height:100%;background:var(--ac);border-radius:99px;transition:width .6s}
.pct{font-size:12px;color:var(--mut);margin-top:3px}
button,.btn{display:inline-flex;align-items:center;gap:7px;font:inherit;font-weight:600;padding:8px 14px;border-radius:9px;border:1px solid var(--ac);background:var(--ac);color:var(--acfg);cursor:pointer;text-decoration:none}
button:hover,.btn:hover{filter:brightness(1.05);text-decoration:none}
button.g,.btn.g{background:transparent;border-color:var(--bd);color:var(--fg)}button.g:hover{background:var(--sf2)}
button.d{background:transparent;border-color:var(--bd);color:var(--bad)}
button.ic{padding:6px 8px;border-radius:8px}
form.inl{display:inline}
input,select,textarea{font:inherit;color:var(--fg);background:var(--bg);border:1px solid var(--bd);border-radius:9px;padding:8px 11px;width:100%;min-width:0}
input:focus,select:focus,textarea:focus{outline:2px solid color-mix(in srgb,var(--ac) 55%,transparent);outline-offset:0;border-color:var(--ac)}
label{display:block;font-size:12.5px;font-weight:600;color:var(--mut)}label>input,label>select,label>textarea{margin-top:5px;font-weight:400}
.fg{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));align-items:end}
.fg .wide{grid-column:1/-1}
.hint{color:var(--mut);font-size:13px;margin:8px 0 0}
.banner{display:flex;gap:10px;align-items:center;padding:11px 14px;border-radius:11px;margin-bottom:16px;font-weight:550}
.banner.ok{background:var(--okbg);color:var(--ok)}.banner.err{background:var(--badbg);color:var(--bad)}.banner.warn{background:var(--warnbg);color:var(--warn)}
.steps{list-style:none;margin:0;padding:0}
.steps li{display:flex;gap:12px;align-items:flex-start;padding:9px 0;border-top:1px solid var(--bd)}.steps li:first-child{border:0}
.dot{width:22px;height:22px;border-radius:50%;border:2px solid var(--bd);display:grid;place-items:center;flex:none;margin-top:1px}
.steps .done .dot{background:var(--ok);border-color:var(--ok);color:#fff}.steps .done .t{color:var(--mut);text-decoration:line-through}
.steps .t{font-weight:600}.steps .d{color:var(--mut);font-size:13px}
.meter{height:6px;background:var(--sf2);border-radius:9px;margin:2px 0 12px;overflow:hidden}.meter i{display:block;height:100%;background:var(--ok);transition:width .5s}
details{margin-top:12px}summary{cursor:pointer;font-weight:600;color:var(--mut)}
pre{background:var(--bg);border:1px solid var(--bd);border-radius:10px;padding:12px;overflow:auto;max-height:280px;font:12.5px/1.5 ui-monospace,Menlo,Consolas,monospace;margin:10px 0 0;white-space:pre-wrap}
.feed{list-style:none;margin:0;padding:0;font-size:13.5px}.feed li{padding:6px 0;border-top:1px solid var(--bd);display:flex;gap:10px}.feed li:first-child{border:0}.feed time{color:var(--mut);flex:none;font:12.5px ui-monospace,Menlo,Consolas,monospace}
.empty{text-align:center;color:var(--mut);padding:26px 10px}
.toolbar{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:14px}.toolbar input{max-width:280px}
.copy{background:none;border:0;color:var(--mut);padding:2px 5px;cursor:pointer}
.dz{border:2px dashed var(--bd);border-radius:12px;padding:22px;text-align:center;color:var(--mut);cursor:pointer}.dz.on{border-color:var(--ac);background:var(--sf2)}
.login{min-height:100vh;display:grid;place-items:center;padding:20px}.login .card{width:100%;max-width:380px;padding:28px}
.login .brand{justify-content:center;padding-bottom:20px}
@media(max-width:820px){
 .app{grid-template-columns:minmax(0,1fr)}
 aside{position:static;height:auto;flex-direction:row;overflow-x:auto;padding:8px;border-right:0;border-bottom:1px solid var(--bd);gap:4px}
 aside .brand,aside .sp{display:none}aside a,aside button.nav{width:auto;white-space:nowrap;padding:8px 11px}
.rt th:nth-child(2),.rt td:nth-child(2),.rt th:nth-child(4),.rt td:nth-child(4),.rt th:nth-child(6),.rt td:nth-child(6){display:none}.tw table{min-width:0}
 main{padding:18px 16px 50px}h1{font-size:21px}}
"""

JS = """
(function(){
 var live=document.getElementById('live');
 function tick(){ if(document.hidden||!live)return; var a=document.activeElement;
  fetch(location.href,{credentials:'same-origin'}).then(function(r){return r.ok?r.text():null}).then(function(t){
   if(!t)return; var n=new DOMParser().parseFromString(t,'text/html').getElementById('live');
   if(n&&n.innerHTML!==live.innerHTML&&!(a&&live.contains(a)&&/INPUT|SELECT|TEXTAREA/.test(a.tagName)))live.innerHTML=n.innerHTML;}).catch(function(){});}
 if(live)setInterval(tick,3000);
 document.addEventListener('click',function(ev){
  var c=ev.target.closest('[data-copy]');if(c){navigator.clipboard&&navigator.clipboard.writeText(c.dataset.copy);var o=c.innerHTML;c.textContent='Copied';setTimeout(function(){c.innerHTML=o},1200);}
 });
 document.addEventListener('submit',function(ev){var m=ev.target.dataset.confirm;if(m&&!confirm(m))ev.preventDefault();});
 var f=document.getElementById('filter');
 if(f)f.addEventListener('input',function(){var q=f.value.toLowerCase();document.querySelectorAll('#live tbody tr').forEach(function(r){r.style.display=r.textContent.toLowerCase().indexOf(q)<0?'none':''})});
 var b=document.querySelector('.banner');if(b&&b.dataset.auto)setTimeout(function(){b.style.display='none'},5000);
 // image upload with progress
 var dz=document.getElementById('dz'),fi=document.getElementById('file');
 if(dz&&fi){
  dz.addEventListener('click',function(){fi.click()});
  ['dragover','dragenter'].forEach(function(n){dz.addEventListener(n,function(e){e.preventDefault();dz.classList.add('on')})});
  ['dragleave','drop'].forEach(function(n){dz.addEventListener(n,function(){dz.classList.remove('on')})});
  dz.addEventListener('drop',function(e){e.preventDefault();if(e.dataTransfer.files[0])up(e.dataTransfer.files[0])});
  fi.addEventListener('change',function(){if(fi.files[0])up(fi.files[0])});
  function up(file){var st=document.getElementById('upst'),x=new XMLHttpRequest();
   x.open('PUT','images/upload?name='+encodeURIComponent(file.name));x.setRequestHeader('X-CSRF',dz.dataset.csrf);
   x.upload.onprogress=function(e){if(e.lengthComputable)st.textContent='Uploading '+file.name+': '+Math.round(e.loaded/e.total*100)+'%'};
   x.onload=function(){location.href='images?k='+(x.status==200?'ok':'err')+'&m='+encodeURIComponent(x.status==200?'Uploaded '+file.name:x.responseText)};
   x.onerror=function(){st.textContent='Upload failed'};x.send(file);}
 }
})();
"""

FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%23f5a623'/%3E"
           "%3Ctext x='16' y='21' font-family='sans-serif' font-size='12' font-weight='700' text-anchor='middle' fill='%231a1200'%3EPXE%3C/text%3E%3C/svg%3E")

NAV = [("/", "status", "Dashboard"), ("/guide", "guide", "Guide"), ("/rigs", "rigs", "Rigs"), ("/groups", "groups", "Groups"),
       ("/images", "image", "Image"), ("/settings", "settings", "Settings")]

def head(title):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<base href="{base()}"><title>{e(title)} - Hive OS PXE by Silver</title><link rel="icon" href="{FAVICON}"><style>{CSS}</style></head>')

def layout(title, body, csrf, active, sub="", actions="", msg=None, show_logout=False):
    """msg = (kind, text) where kind in ok/err/warn."""
    nav = "".join(f'<a href="{h}" class="{"on" if k == active else ""}">{icon(k)}{l}</a>' for h, k, l in NAV)
    banner = ""
    if msg:
        k, t = msg
        banner = f'<div class="banner {"ok" if k == "ok" else "err" if k == "err" else "warn"}" data-auto="{1 if k == "ok" else ""}">{icon("check" if k == "ok" else "alert")}{e(t)}</div>'
    logout = (f'<form method="post" action="/logout"><input type="hidden" name="csrf" value="{csrf}">'
              f'<button class="nav">{icon("logout")}Log out</button></form>') if show_logout else ""
    out = (head(title) + f'<body><div class="app"><aside><div class="brand"><b>PXE</b><span>Hive OS PXE<small>by Silver</small></span></div>'
            f'{nav}<span class="sp"></span>{logout}</aside><main><div class="ph"><div><h1>{e(title)}</h1>'
            f'{f"<p class=sub>{sub}</p>" if sub else ""}</div><div>{actions}</div></div>{banner}{body}</main></div>'
            f'<script>{JS}</script></body></html>')
    return rel(out).encode()

def bare(title, body):
    out = (head(title) + f'<body><div class="login"><div><div class="brand"><b>PXE</b><span>Hive OS PXE<small>by Silver</small></span></div>'
            f'{body}</div></div></body></html>')
    return rel(out).encode()

def badge(state):
    label = {"pending": "Pending", "flashing": "Flashing", "done": "Deployed", "failed": "Failed", "skip": "Skipped"}.get(state, state)
    return f'<span class="badge b-{e(state)}">{label}</span>'

def bar(pct):
    pct = max(0, min(100, int(pct)))
    return f'<div class="bar"><i style="width:{pct}%"></i></div><div class="pct">{pct}%</div>'

def ago(ts):
    import time
    if not ts: return "never"
    d = int(time.time() - ts)
    if d < 10: return "just now"
    if d < 60: return f"{d}s ago"
    if d < 3600: return f"{d // 60}m ago"
    if d < 86400: return f"{d // 3600}h ago"
    return f"{d // 86400}d ago"

def human(n):
    for u in ("B", "KB", "MB", "GB"):
        if n < 1024 or u == "GB": return f"{n:.0f} {u}" if u == "B" else f"{n:.1f} {u}"
        n /= 1024

CSS += """
.gd{padding:0}.gd summary{list-style:none;display:flex;align-items:center;padding:16px 20px;font-weight:650;font-size:15.5px;cursor:pointer;color:var(--fg)}
.gd summary::-webkit-details-marker{display:none}.gd summary::after{content:"";margin-left:auto;width:8px;height:8px;border-right:2px solid var(--mut);border-bottom:2px solid var(--mut);transform:rotate(45deg);transition:transform .2s}
.gd[open] summary::after{transform:rotate(-135deg)}
.gb{padding:0 20px 18px 56px;line-height:1.6}.gb p,.gb ol,.gb ul{margin:.6em 0}.gb li{margin:.35em 0}
.num{display:inline-grid;place-items:center;width:28px;height:28px;border-radius:50%;background:var(--ac);color:var(--acfg);font-weight:700;font-size:13.5px;margin-right:14px;flex:none}
.num.ok{background:var(--ok);color:#fff}
.tip{background:var(--infbg);border-left:4px solid var(--inf);padding:10px 14px;border-radius:8px;margin:12px 0;font-size:14px}
.tip.warn{background:var(--warnbg);border-left-color:var(--warn)}
.gq{border-top:1px solid var(--bd);margin:0}.gq:first-of-type{border:0}.gq summary{padding:12px 0;cursor:pointer;font-weight:600}.gq .gb{padding:0 0 12px 0}
.gl dt{font-weight:650;margin-top:10px}.gl dd{margin:2px 0 0;color:var(--mut)}
@media(max-width:820px){.gb{padding-left:20px}}
"""
