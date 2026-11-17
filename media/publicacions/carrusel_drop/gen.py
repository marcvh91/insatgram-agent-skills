import base64, asyncio, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from svgkit import shoe_svg, leg_panel, shoe
from playwright.async_api import async_playwright

D = pathlib.Path(__file__).parent
FOTO = D.parent.parent / "fotos_standard" / "tonus_camilla_tauleta_serios.jpg"
b64 = base64.b64encode(FOTO.read_bytes()).decode()

REFS = {
 1: ("The effect of heel-to-toe drop of running shoes on patellofemoral joint stress during running.",
     "Zhang M, Zhou X, Zhang L, Liu H.", "Gait Posture. 2022. doi: 10.1016/j.gaitpost.2022.02.008"),
 2: ("Shoe heel-toe drop affects running economy.",
     "Renninger K, Beck ON.", "J Appl Physiol. 2026. doi: 10.1152/japplphysiol.00886.2025"),
 3: ("Acute shoe effects on Achilles tendon loading in runners with habitual rearfoot strike pattern.",
     "Zhang X, Deng L, Yang Y, et al.", "Gait Posture. 2020. doi: 10.1016/j.gaitpost.2020.09.027"),
 4: ("Injury risk associated with the transition to minimalist footwear in runners: A systematic review and meta-analysis.",
     "Sánchez-Del Río E, Galán-Arriero I, Palomo-Fernández I, et al.", "Gait Posture. 2026. doi: 10.1016/j.gaitpost.2026.110614"),
 5: ("Running shoes for preventing lower limb running injuries in adults.",
     "Relph N, Greaves H, Armstrong R, et al.", "Cochrane Database Syst Rev. 2022. doi: 10.1002/14651858.CD013368.pub2"),
 6: ("Association of Shoe Cushioning Perception and Comfort With Injury Risk in Leisure-Time Runners: A Secondary Analysis of a Randomised Trial.",
     "Malisoux L, Delattre N, Urhausen A, et al.", "Eur J Sport Sci. 2025. doi: 10.1002/ejsc.70063"),
 7: ("Common Risk Factors for Knee Injuries in Runners: A Systematic Review.",
     "Senthil K, Whitaker S, Nazarov M, et al.", "Orthop J Sports Med. 2026. doi: 10.1177/23259671261444314"),
 8: ("How much running is too much? Identifying high-risk running sessions in a 5200-person cohort study.",
     "Frandsen JSB, Hulme A, Parner ET, et al.", "Br J Sports Med. 2025. doi: 10.1136/bjsports-2024-109380"),
}

def cards(ids, small=False):
    c = ' sm' if small else ''
    return f'<div class="refs{c}">' + "".join(
        f'<div class="card"><div class="t"><span class="n">[{i}]</span> {REFS[i][0]}</div>'
        f'<div class="a">{REFS[i][1]}</div><div class="j">{REFS[i][2]}</div></div>' for i in ids) + '</div>'

def r(*n): return '<sup>' + ''.join(f'[{i}]' for i in n) + '</sup>'

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:#0B0F12;font-family:Inter,sans-serif;color:#E8ECEF;overflow:hidden}
.s{position:relative;width:1080px;height:1350px;padding:80px;display:flex;flex-direction:column}
.top{display:flex;justify-content:space-between;font-weight:800;font-size:30px;letter-spacing:4px}
.k{color:#D4FF3F}.pg{color:#6B7378}
h1{font-weight:900;font-size:84px;line-height:.98;letter-spacing:-3px;text-transform:uppercase;margin-top:30px;color:#fff}
h1 em{font-style:normal;color:#D4FF3F}
p{font-size:40px;line-height:1.3;font-weight:500;margin-top:28px}
b{color:#D4FF3F;font-weight:800}
sup{color:#D4FF3F;font-size:23px;font-weight:800;margin-left:3px}
.tag{display:inline-block;background:#D4FF3F;color:#0B0F12;font-weight:900;font-size:34px;padding:14px 24px;border-radius:12px;margin-top:30px;align-self:flex-start}
.refs{margin-top:auto;display:flex;flex-direction:column;gap:12px}
.card{background:#fff;border-radius:14px;padding:14px 22px}
.card .t{color:#2F6DB5;font-weight:700;font-size:20px;line-height:1.28}
.card .n{color:#4E8B4A}
.card .a{color:#111;font-size:18px;margin-top:4px}
.card .j{color:#4E8B4A;font-size:17px;margin-top:3px}
.refs.sm .card{padding:10px 18px}.refs.sm .t{font-size:17px}.refs.sm .a{font-size:15px}.refs.sm .j{font-size:15px}
ul{list-style:none;margin-top:26px}
li{font-size:38px;line-height:1.28;font-weight:500;padding:16px 0 16px 64px;position:relative;border-bottom:2px solid #1E252A}
li:before{content:attr(data-n);position:absolute;left:0;top:17px;width:46px;height:46px;border-radius:50%;background:#D4FF3F;color:#0B0F12;font-weight:900;font-size:28px;display:flex;align-items:center;justify-content:center}
.note{font-size:24px;color:#8A9399;margin-top:14px}
.lab{font-size:26px;font-weight:900;letter-spacing:2px;color:#D4FF3F}
.mm{font-size:22px;font-weight:700;color:#8A9399;margin-top:2px}
"""
def page(body): return f"<html><head><style>{CSS}</style></head><body>{body}</body></html>"


gm, bm = shoe("mn", 10, 10, px=3.0)
mini = f"""<svg width="700" height="340" viewBox="-80 -340 760 370"><defs><radialGradient id="hh"><stop offset="0" stop-color="#FF4D2E" stop-opacity=".95"/><stop offset=".5" stop-color="#FF4D2E" stop-opacity=".4"/><stop offset="1" stop-color="#FF4D2E" stop-opacity="0"/></radialGradient></defs>
{gm}
<ellipse cx="440" cy="-28" rx="95" ry="48" fill="url(#hh)"/>
<path d="M18,{bm(0)-150} C14,{bm(0)-210} 10,{bm(0)-250} 6,{bm(0)-290}" stroke="#FF4D2E" stroke-width="16" stroke-linecap="round" fill="none"/>
<path d="M18,{bm(0)-150} C14,{bm(0)-210} 10,{bm(0)-250} 6,{bm(0)-290}" stroke="#FFE1D8" stroke-width="5" stroke-linecap="round" fill="none"/>
<text x="40" y="{bm(0)-230}" fill="#fff" font-size="30" font-weight="800" font-family="Inter">Aquil·les</text>
<text x="390" y="-95" fill="#fff" font-size="30" font-weight="800" font-family="Inter">Metatarsians</text>
</svg>"""
weeks = "".join(f'<div style="flex:1;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;gap:6px"><div style="width:100%;height:{int(14+i*11)}px;background:{"#D4FF3F" if i==11 else "#5E6B12"};border-radius:6px 6px 0 0"></div><div style="font-size:18px;color:#8A9399;font-weight:700">{i+1}</div></div>' for i in range(12))
S = []
# 1 PORTADA (títol visible des del primer moment)
S.append(f"""<div class="s" style="padding:0">
<img src="data:image/jpeg;base64,{b64}" style="position:absolute;inset:0;width:1080px;height:1350px;object-fit:cover;object-position:50% 60%">
<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,15,18,.97) 0%,rgba(11,15,18,.88) 42%,rgba(11,15,18,0) 66%,rgba(11,15,18,.5) 100%)"></div>
<div style="position:relative;padding:80px">
<div class="top"><span class="k">CORREDORS · GENOLL</span><span class="pg">1/8</span></div>
<h1 style="font-size:92px">Tens mal al genoll quan corres <em>i no saps per què?</em></h1>
<div class="tag">👟 I si fossin les sabatilles?</div>
</div>
<div style="position:absolute;bottom:60px;right:80px;font-size:30px;font-weight:800;color:#fff">Llisca →</div>
</div>""")

# 2 QUÈ ÉS EL DROP
big = shoe_svg("big", 32, 24, w=920, dims=True, pad=(120, 330, 110, 30))
S.append(f"""<div class="s"><div class="top"><span class="k">UNA POSSIBLE CAUSA</span><span class="pg">2/8</span></div>
<h1>El <em>drop</em></h1>
<p>És la diferència d'altura entre el <b>taló</b> i la <b>punta</b> de la sabatilla.</p>
<div style="margin-top:60px;position:relative">{big}
</div>
<p style="font-size:32px;color:#B9C1C6;margin-top:16px">Les dues alçades es mesuren des del terra (0).</p>
<div style="margin-top:50px;align-self:center;border:4px solid #D4FF3F;border-radius:22px;padding:22px 44px;font-size:52px;font-weight:900">32 − 24 = <span style="color:#D4FF3F">8 mm de drop</span></div>
</div>""")

# 3 TIPUS DE DROP
rows = ""
for uid, h, t, lab, sub in [("z", 26, 26, "0 mm", "Pla · «zero drop»"), ("m", 29, 24, "4–6 mm", "Baix"), ("a", 34, 23, "8–12 mm", "Alt · el més habitual")]:
    sv = shoe_svg(uid, h, t, w=690, pad=(130, 340, 200, 20), px=3.6, dims=True)
    rows += f'<div style="display:flex;align-items:center;gap:10px;margin-top:14px;margin-left:-20px"><div style="width:250px;padding-left:20px;flex-shrink:0"><div style="font-size:50px;font-weight:900;color:#D4FF3F;white-space:nowrap">{lab}</div><div style="font-size:28px;font-weight:600;color:#B9C1C6;margin-top:4px">{sub}</div></div>{sv}</div>'
S.append(f"""<div class="s"><div class="top"><span class="k">TIPUS DE DROP</span><span class="pg">3/8</span></div>
<h1>No totes són <em>iguals</em></h1>
{rows}
<p style="margin-top:auto;font-size:34px;color:#B9C1C6">Mira-ho a la fitxa de la teva sabatilla: sovint ve indicat.</p>
</div>""")

# 4 COM ES REPARTEIXEN LES TENSIONS (clau)
legA = leg_panel("la", 36, 22, "knee", w=390)
legB = leg_panel("lb", 26, 26, "calf", w=390)
S.append(f"""<div class="s" style="padding-bottom:60px"><div class="top"><span class="k">EL MÉS IMPORTANT</span><span class="pg">4/8</span></div>
<h1 style="font-size:76px">On va <em>la tensió?</em></h1>
<div style="display:flex;justify-content:space-between;margin-top:10px">
 <div style="width:450px"><div class="lab">DROP ALT (10–15 mm)</div>{legA}
  <div style="font-size:28px;line-height:1.25;margin-top:6px">🔴 <b>Ròtula:</b> +15 % de tensió{r(1)}<br>🔴 Més esforç al genoll{r(2)}</div></div>
 <div style="width:450px"><div class="lab">DROP BAIX / 0 mm</div>{legB}
  <div style="font-size:28px;line-height:1.25;margin-top:6px">🔴 <b>Bessó i Aquil·les</b> treballen més{r(2,3)}<br>🔵 Menys càrrega a la ròtula{r(1)}</div></div>
</div>
<div style="margin-top:18px;font-size:34px;font-weight:800;text-align:center">La càrrega no desapareix: <span style="color:#D4FF3F">canvia de lloc.</span></div>
{cards([1,2,3], small=True)}</div>""")

# 5 CANVIAR DE COP
S.append(f"""<div class="s"><div class="top"><span class="k">COMPTE</span><span class="pg">5/8</span></div>
<h1>Canviar de drop <em>de cop</em> té risc</h1>
<p>Passar de cop a sabatilles minimalistes s'associa a <b>més lesions</b>: metatarsians, Aquil·les i bessó.{r(4)}</p>
<p>Amb drop baix, el tendó d'Aquil·les rep <b>més força</b> a cada passa.{r(3)}</p>
<div style="margin-top:20px;align-self:center">{mini}</div>
{cards([4,3], small=True)}</div>""")

# 6 NO HO ÉS TOT
S.append(f"""<div class="s"><div class="top"><span class="k">PERÒ…</span><span class="pg">6/8</span></div>
<h1>El drop <em>no ho és tot</em></h1>
<ul>
<li data-n="1">Cap tipus de sabatilla redueix clarament les lesions.{r(5)}</li>
<li data-n="2">Qui s'hi troba <b>còmode</b> es lesiona menys.{r(6)}</li>
<li data-n="3">Al genoll pesen més: <b>lesions prèvies</b>, <b>pujades de càrrega</b> i com es mou el <b>maluc</b>.{r(7)}</li>
</ul>
{cards([5,6,7])}</div>""")

# 7 SI VOLS CANVIAR
S.append(f"""<div class="s"><div class="top"><span class="k">SI VOLS CANVIAR DE DROP</span><span class="pg">7/8</span></div>
<h1>Fes-ho <em>a poc a poc</em></h1>
<ul>
<li data-n="1">Alterna-les amb les de sempre.*</li>
<li data-n="2">Dona-hi temps: <b>12 setmanes</b> o més de transició.{r(4)}</li>
<li data-n="3">Cap sortida <b>&gt;10 % més llarga</b> que la més llarga de l'últim mes.{r(8)}</li>
<li data-n="4">Si el dolor no marxa, fes-t'ho mirar.*</li>
</ul>
<div class="note">* Criteri clínic</div>
<div style="margin-top:22px;font-size:22px;font-weight:800;letter-spacing:2px;color:#B9C1C6">EXEMPLE · % DE SORTIDES AMB LES NOVES · SETMANES</div>
<div style="display:flex;gap:8px;height:170px;margin-top:10px">{weeks}</div>
{cards([4,8], small=True)}</div>""")

# 8 CTA
S.append(f"""<div class="s" style="justify-content:center"><div class="top" style="position:absolute;top:80px;left:80px;right:80px"><span class="k">EN RESUM</span><span class="pg">8/8</span></div>
<h1 style="font-size:80px">El drop mou la tensió. <em>No la treu.</em></h1>
<p>Si et fa mal el genoll quan corres, pot ser el drop… o una altra cosa.</p>
<p><b>Vine i ho mirem.</b></p>
<div style="margin-top:60px;border:3px solid #D4FF3F;border-radius:22px;padding:34px">
<div style="font-size:38px;font-weight:800">WhatsApp <b>627 148 092</b></div>
<div style="font-size:38px;font-weight:800;margin-top:14px">Tonus <b>601 983 214</b></div>
<div style="font-size:32px;margin-top:14px;color:#B9C1C6">«Demana per mi» · @marcvallfisio</div>
</div></div>""")

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 1350})
        for i, s in enumerate(S, 1):
            await pg.set_content(page(s)); await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(D / f"drop_{i}.png"))
        await b.close()
asyncio.run(main())
