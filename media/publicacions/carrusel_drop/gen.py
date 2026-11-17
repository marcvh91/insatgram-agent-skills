import base64, asyncio, pathlib
from playwright.async_api import async_playwright

D = pathlib.Path(__file__).parent
FOTO = D.parent.parent / "fotos_standard" / "tonus_camilla_tauleta_serios.jpg"
b64 = base64.b64encode(FOTO.read_bytes()).decode()

REFS = {
 1: ("Systematic Review of the Role of Footwear Constructions in Running Biomechanics: Implications for Running-Related Injury and Performance.",
     "Sun X, Lam WK, Zhang X, et al.", "J Sports Sci Med. 2020. PMID: 32132824"),
 2: ("Effects of Foot Strike Techniques on Running Biomechanics: A Systematic Review and Meta-analysis.",
     "Xu Y, Yuan P, Wang R, et al.", "Sports Health. 2020. doi: 10.1177/1941738120934715"),
 3: ("Running shoes for preventing lower limb running injuries in adults.",
     "Relph N, Greaves H, Armstrong R, et al.", "Cochrane Database Syst Rev. 2022. doi: 10.1002/14651858.CD013368.pub2"),
 4: ("Association of Shoe Cushioning Perception and Comfort With Injury Risk in Leisure-Time Runners: A Secondary Analysis of a Randomised Trial.",
     "Malisoux L, Delattre N, Urhausen A, et al.", "Eur J Sport Sci. 2025. doi: 10.1002/ejsc.70063"),
 5: ("Common Risk Factors for Knee Injuries in Runners: A Systematic Review.",
     "Senthil K, Whitaker S, Nazarov M, et al.", "Orthop J Sports Med. 2026. doi: 10.1177/23259671261444314"),
 6: ("How much running is too much? Identifying high-risk running sessions in a 5200-person cohort study.",
     "Frandsen JSB, Hulme A, Parner ET, et al.", "Br J Sports Med. 2025. doi: 10.1136/bjsports-2024-109380"),
}

def cards(ids):
    return '<div class="refs">' + "".join(
        f'<div class="card"><div class="t"><span class="n">[{i}]</span> {REFS[i][0]}</div>'
        f'<div class="a">{REFS[i][1]}</div><div class="j">{REFS[i][2]}</div></div>' for i in ids) + '</div>'

def r(*n): return '<sup>' + ''.join(f'[{i}]' for i in n) + '</sup>'

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:#0B0F12;font-family:Inter,sans-serif;color:#E8ECEF;overflow:hidden}
.s{position:relative;width:1080px;height:1350px;padding:80px;display:flex;flex-direction:column}
.top{display:flex;justify-content:space-between;font-weight:800;font-size:30px;letter-spacing:4px}
.k{color:#D4FF3F}.pg{color:#6B7378}
h1{font-weight:900;font-size:88px;line-height:.98;letter-spacing:-3px;text-transform:uppercase;margin-top:34px;color:#fff}
h1 em{font-style:normal;color:#D4FF3F}
p{font-size:42px;line-height:1.32;font-weight:500;margin-top:34px}
b{color:#D4FF3F;font-weight:800}
sup{color:#D4FF3F;font-size:24px;font-weight:800;margin-left:4px}
.tag{display:inline-block;background:#D4FF3F;color:#0B0F12;font-weight:900;font-size:32px;padding:14px 22px;border-radius:12px;margin-top:30px;align-self:flex-start;letter-spacing:1px}
.refs{margin-top:auto;display:flex;flex-direction:column;gap:14px}
.card{background:#fff;border-radius:14px;padding:16px 22px}
.card .t{color:#2F6DB5;font-weight:700;font-size:21px;line-height:1.3}
.card .n{color:#4E8B4A}
.card .a{color:#111;font-size:19px;margin-top:5px}
.card .j{color:#4E8B4A;font-size:18px;margin-top:4px}
.row{display:flex;gap:24px;margin-top:34px}
.box{flex:1;border:3px solid #2A3238;border-radius:20px;padding:26px}
.box h3{font-size:30px;font-weight:900;color:#D4FF3F;letter-spacing:1px}
.box div{font-size:34px;line-height:1.3;margin-top:12px;font-weight:500}
ul{list-style:none;margin-top:30px}
li{font-size:40px;line-height:1.3;font-weight:500;padding:18px 0 18px 64px;position:relative;border-bottom:2px solid #1E252A}
li:before{content:attr(data-n);position:absolute;left:0;top:18px;width:46px;height:46px;border-radius:50%;background:#D4FF3F;color:#0B0F12;font-weight:900;font-size:28px;display:flex;align-items:center;justify-content:center}
.note{font-size:24px;color:#8A9399;margin-top:18px}
"""

def page(body): return f"<html><head><style>{CSS}</style></head><body>{body}</body></html>"

S = []
# 1 PORTADA
S.append(f"""<div class="s" style="padding:0">
<img src="data:image/jpeg;base64,{b64}" style="position:absolute;inset:0;width:1080px;height:1350px;object-fit:cover;object-position:50% 60%">
<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(11,15,18,.96) 0%,rgba(11,15,18,.85) 38%,rgba(11,15,18,0) 62%,rgba(11,15,18,.55) 100%)"></div>
<div style="position:relative;padding:80px">
<div class="top"><span class="k">SABATILLES · GENOLL</span><span class="pg">1/7</span></div>
<h1 style="font-size:104px">El drop et fa mal <em>al genoll?</em></h1>
<div class="tag">Què diu la ciència (i què no)</div>
</div>
<div style="position:absolute;bottom:60px;right:80px;font-size:30px;font-weight:800;color:#fff">Llisca →</div>
</div>""")

# 2 QUÈ ÉS EL DROP
svg = """<svg width="920" height="400" viewBox="0 0 920 400">
<path d="M90 170 Q90 70 200 60 L330 60 Q420 70 520 150 L800 205 Q850 215 850 245 L90 245 Z" fill="#1E252A" stroke="#E8ECEF" stroke-width="4"/>
<path d="M90 170 L90 320 L850 320 L850 245 Z" fill="#D4FF3F"/>
<line x1="60" y1="170" x2="60" y2="320" stroke="#fff" stroke-width="4"/><line x1="48" y1="170" x2="72" y2="170" stroke="#fff" stroke-width="4"/><line x1="48" y1="320" x2="72" y2="320" stroke="#fff" stroke-width="4"/>
<line x1="880" y1="245" x2="880" y2="320" stroke="#fff" stroke-width="4"/><line x1="868" y1="245" x2="892" y2="245" stroke="#fff" stroke-width="4"/><line x1="868" y1="320" x2="892" y2="320" stroke="#fff" stroke-width="4"/>
<text x="20" y="370" fill="#E8ECEF" font-size="28" font-weight="800" font-family="Inter">Taló 32 mm</text>
<text x="720" y="370" fill="#E8ECEF" font-size="28" font-weight="800" font-family="Inter">Punta 24 mm</text>
<text x="300" y="300" fill="#0B0F12" font-size="34" font-weight="900" font-family="Inter">DROP = 32 − 24 = 8 mm</text>
</svg>"""
S.append(f"""<div class="s"><div class="top"><span class="k">PRIMER, QUÈ ÉS</span><span class="pg">2/7</span></div>
<h1>El <em>drop</em></h1>
<p>És la diferència d'altura entre el <b>taló</b> i la <b>punta</b> de la sabatilla.</p>
<div style="margin-top:50px">{svg}</div>
<div class="row" style="margin-top:40px">
<div class="box"><h3>0 mm</h3><div>Pla</div></div>
<div class="box"><h3>4–6 mm</h3><div>Baix</div></div>
<div class="box"><h3>8–12 mm</h3><div>Alt (el clàssic)</div></div>
</div></div>""")

# 3 EL DROP NO DECIDEIX
S.append(f"""<div class="s"><div class="top"><span class="k">MITE</span><span class="pg">3/7</span></div>
<h1>«Hi ha un drop <em>perfecte»</em></h1>
<div class="tag">FALS</div>
<p>No hi ha prou dades per recomanar cap drop concret.{r(1)}</p>
<p>El que reparteix la càrrega és <b>com trepitges</b>{r(2)}:</p>
<div class="row">
<div class="box"><h3>TALÓ</h3><div>Més càrrega al <b>genoll</b></div></div>
<div class="box"><h3>AVANTPEU</h3><div>Més càrrega al <b>turmell i l'Aquil·les</b></div></div>
</div>
{cards([1,2])}</div>""")

# 4 CAP SABATILLA MÀGICA
S.append(f"""<div class="s"><div class="top"><span class="k">EL QUE SÍ SABEM</span><span class="pg">4/7</span></div>
<h1>No hi ha sabatilla <em>màgica</em></h1>
<p>Cap tipus de sabatilla redueix clarament les lesions. Triar-la pel tipus de peu <b>tampoc ajuda</b>.{r(3)}</p>
<p>Qui nota que amorteix i <b>s'hi troba bé</b> es lesiona menys.{r(4)}</p>
<div class="tag">👟 Tria per comoditat</div>
{cards([3,4])}</div>""")

# 5 DOLOR LATERAL
S.append(f"""<div class="s"><div class="top"><span class="k">DOLOR A FORA DEL GENOLL</span><span class="pg">5/7</span></div>
<h1>Abans de culpar <em>la sabatilla</em>, mira això</h1>
<p>Els factors de risc més repetits en lesions de genoll en corredors:{r(5)}</p>
<ul>
<li data-n="1"><b>Lesions prèvies</b></li>
<li data-n="2"><b>Pujades de càrrega</b> (km, ritme, desnivell)</li>
<li data-n="3">Com es mouen el <b>maluc i la pelvis</b></li>
</ul>
{cards([5])}</div>""")

# 6 SI VOLS CANVIAR
S.append(f"""<div class="s"><div class="top"><span class="k">SI VOLS CANVIAR DE DROP</span><span class="pg">6/7</span></div>
<h1>Fes-ho <em>a poc a poc</em></h1>
<ul>
<li data-n="1">Alterna-les amb les de sempre.*</li>
<li data-n="2">Comença amb sortides curtes i suaus.*</li>
<li data-n="3">Cap sortida <b>&gt;10 % més llarga</b> que la més llarga de l'últim mes.{r(6)}</li>
<li data-n="4">Si el dolor no millora, fes-t'ho mirar.*</li>
</ul>
<div class="note">* Criteri clínic</div>
{cards([6])}</div>""")

# 7 CTA
S.append(f"""<div class="s" style="justify-content:center"><div class="top" style="position:absolute;top:80px;left:80px;right:80px"><span class="k">EN RESUM</span><span class="pg">7/7</span></div>
<h1 style="font-size:80px">El drop mou la càrrega. <em>No la treu.</em></h1>
<p>Si et fa mal el genoll quan corres, el problema rarament és només la sabatilla.</p>
<p><b>Vine i mirem què hi ha darrere.</b></p>
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
