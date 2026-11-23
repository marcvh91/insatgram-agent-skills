"""Carrusel «Els 3 pilars de la força per córrer» · esbós v1 (1080×1350). Il·lustracions 3D a ./3d (three.js)."""
import asyncio, pathlib
from playwright.async_api import async_playwright
D = pathlib.Path(__file__).parent.resolve(); F = D.parent.parent / "fotos_standard"
U = lambda p: (D / "3d" / p).as_uri()
CSS = """*{margin:0;padding:0;box-sizing:border-box}body{font-family:Inter,sans-serif;color:#E8ECEF;background:#0B0F12;overflow:hidden}
.s{width:1080px;height:1350px;position:relative;padding:80px 70px 0;background:radial-gradient(120% 70% at 50% 45%,#141B20 0%,#0B0F12 70%)}
.k{font-size:30px;font-weight:900;letter-spacing:4px;color:#D4FF3F;text-transform:uppercase}
h2{font-weight:900;font-size:76px;line-height:.98;letter-spacing:-2.5px;text-transform:uppercase;color:#fff;margin-top:14px}h2 em{font-style:normal;color:#D4FF3F}
p{font-size:36px;line-height:1.28;font-weight:600;color:#D5DBDF}b{color:#D4FF3F;font-weight:800}sup{color:#D4FF3F;font-size:22px;font-weight:800}
.lab{font-size:28px;font-weight:800;text-align:center;color:#B9C1C6}.lab b{display:block;font-size:34px}
.card{position:absolute;left:70px;right:70px;bottom:46px;display:flex;gap:16px;align-items:center;background:#11171B;border:2px solid #2A3238;border-radius:16px;padding:14px 20px;font-size:22px;color:#9AA5AC;font-weight:600}
.card .pm{background:#326295;color:#fff;font-weight:900;font-size:20px;padding:6px 10px;border-radius:6px;flex-shrink:0}
.pg{position:absolute;top:84px;right:70px;font-size:26px;font-weight:800;color:#5C676E}"""
def ref(*n): return '<sup>' + ''.join(f'[{i}]' for i in n) + '</sup>'
def card(t): return f'<div class="card"><span class="pm">PubMed</span><span>{t}</span></div>'
def pg(n): return f'<div class="pg">{n}/8</div>'

def photo_slide(img, inner, top_band=470, off=330):
    return f"""<div class="s" style="padding:0;background:#0B0F12">
<img src="{(F/img).as_uri()}" style="position:absolute;left:0;top:{off}px;width:1080px">
<div style="position:absolute;left:0;right:0;top:0;height:{top_band+260}px;background:linear-gradient(180deg,#0B0F12 0%,#0B0F12 {int(top_band/(top_band+260)*100)}%,rgba(11,15,18,0) 100%)"></div>
<div style="position:absolute;top:48px;left:70px;right:70px">{inner}</div></div>"""

S = {}
_c = (F / "pro_retrat_bracos_creuats_frontal.jpg").as_uri()
S[1] = f"""<div class="s" style="padding:0;background:#0B0F12">
<div style="position:absolute;inset:0;background:radial-gradient(60% 55% at 50% 52%,#E4E4E2 0%,#C9C9C7 55%,#8E9193 100%)"></div>
<img src="{_c}" style="position:absolute;left:{(1080-748)//2}px;top:230px;height:1120px;-webkit-mask-image:linear-gradient(90deg,transparent 0,#000 12%,#000 88%,transparent 100%)">
<div style="position:absolute;left:0;right:0;top:0;height:470px;background:linear-gradient(180deg,#0B0F12 0%,#0B0F12 52%,rgba(11,15,18,0) 100%)"></div>
<div style="position:absolute;top:48px;left:70px;right:70px"><div class="k">Força per a corredors</div>
<div style="font-weight:900;font-size:92px;line-height:.94;letter-spacing:-3.5px;text-transform:uppercase;color:#fff;margin-top:12px">Els 3 pilars <span style="color:#D4FF3F">de la força per córrer</span></div></div></div>"""

def ill(img, w, h, bottom="", tag=""):
    t = f'<div style="position:absolute;top:16px;left:16px;background:#D4FF3F;color:#0B0F12;font-size:22px;font-weight:900;padding:6px 12px;border-radius:8px;letter-spacing:1px">{tag}</div>' if tag else ""
    return (f'<div style="position:relative;width:{w}px;height:{h}px;border-radius:26px;overflow:hidden;border:2px solid #222B31;box-shadow:0 20px 50px rgba(0,0,0,.45)">'
            f'<img src="{U(img)}" style="width:100%;height:100%;object-fit:cover">{t}'
            f'<div style="position:absolute;left:0;right:0;bottom:0;padding:60px 14px 16px;background:linear-gradient(0deg,rgba(11,15,18,.92),rgba(11,15,18,0))">{bottom}</div></div>')
def two(l, ls, r, rs):
    return (f'<div style="display:flex;justify-content:space-around"><div class="lab"><b style="color:#B9C1C6">{l}</b>{ls}</div>'
            f'<div class="lab"><b>{r}</b>{rs}</div></div>')
one = lambda t, sub="": f'<div class="lab"><b>{t}</b>{sub}</div>'

S[2] = f"""<div class="s">{pg(2)}<div class="k">Abans de començar</div>
<h2>Fer exercicis <em>≠</em> estar preparat</h2>
<p style="margin-top:30px">Equilibris, gomes i exercicis lleugers sumen. Però <b>si només fas això</b>, et falten peces. Córrer demana tres coses:</p>
<div style="display:flex;justify-content:space-between;margin-top:70px">
{ill('q_paret.png', 300, 560, one('Tendons', 'que aguantin'), '1')}{ill('q_esquat.png', 300, 560, one('Múscul', 'que empenyi'), '2')}{ill('q_salt.png', 300, 560, one('Potència', 'per rebotar'), '3')}</div></div>"""

S[3] = f"""<div class="s">{pg(3)}<div class="k">Pilar 1 · Tendons</div>
<h2>Càrrega <em>alta</em>, tendó més fort</h2>
<div style="display:flex;gap:20px;margin-top:30px">
{ill('q_aquil.png', 490, 640, two('Poca càrrega', 'fibres laxes', 'Càrrega alta', 'tendó més fort'))}
{ill('q_paret.png', 420, 640, one('Cadira a la paret', 'o esquat aguantant'), 'EXEMPLE')}</div>
<p style="margin-top:34px">Carregar el tendó el fa més fort. El que més l'enforteix és <b>la càrrega alta</b>, no fer moltes repeticions lleugeres{ref(1)}.</p>
{card('[1] Lazarczuk SL et al. <i>Sports Med</i> 2022 · Revisió sistemàtica i metaanàlisi · 61 estudis')}</div>"""

S[4] = f"""<div class="s">{pg(4)}<div class="k">Pilar 2 · Múscul</div>
<h2>Pes <em>de debò</em></h2>
<div style="display:flex;gap:20px;margin-top:30px">
{ill('q_muscul.png', 490, 640, two('Abans', '', 'Després', 'més fibra'))}
{ill('q_esquat.png', 420, 640, one('Esquat amb barra', 'càrrega alta'), 'EXEMPLE')}</div>
<p style="margin-top:34px">Esquat, pont de glutis, gambades, bessó i sòleo. Amb <b>càrregues altes</b> (≥80 % del teu màxim) millora el <b>temps</b>{ref(3)} i gastes menys energia a cada passa{ref(2)}.</p>
{card('[2][3] Llanos-Lagos C et al. <i>Sports Med</i> 2024 · 2 revisions sistemàtiques i metaanàlisis')}</div>"""

S[5] = f"""<div class="s">{pg(5)}<div class="k">Pilar 3 · Potència</div>
<h2>Fes la cama <em>més molla</em></h2>
<div style="display:flex;gap:20px;margin-top:30px">
{ill('q_molla.png', 490, 520, two('Tova', "s'enfonsa", 'Rígida', 'rebota'))}
{ill('q_salt.png', 420, 520, one('Salts', 'pliometria'), 'EXEMPLE')}</div>
<p style="margin-top:30px"><b>Salts (pliometria):</b> milloren l'economia, sobretot a ritmes suaus (≤12 km/h){ref(2)}. Primer molts i suaus; després pocs i explosius.<br><b>Empènyer fort 3–5 s</b> contra un objecte fix va funcionar en un assaig{ref(4)}, però en conjunt l'evidència és més feble{ref(2)}.</p>
{card('[4] Lum D et al. <i>Res Q Exerc Sport</i> 2023 · Assaig aleatoritzat · 26 corredors')}</div>"""

days = [("Dl", "Cursa suau", 0), ("Dt", "Força<br>1 + 2", 1), ("Dc", "Sèries", 0), ("Dj", "Cursa suau", 0), ("Dv", "Força<br>2 + 3", 1), ("Ds", "Descans", 2), ("Dg", "Tirada llarga", 0)]
cells = "".join(f'<div style="flex:1;border-radius:18px;padding:22px 6px;text-align:center;background:{"#D4FF3F" if f==1 else "#151C21"};color:{"#0B0F12" if f==1 else ("#5C676E" if f==2 else "#E8ECEF")};border:2px solid {"#D4FF3F" if f==1 else "#2A3238"}"><div style="font-size:30px;font-weight:900">{d}</div><div style="font-size:23px;font-weight:800;margin-top:12px;line-height:1.15">{t}</div></div>' for d, t, f in days)
S[6] = f"""<div class="s">{pg(6)}<div class="k">Com ho encaixo?</div>
<h2>Combina <em>els 3</em></h2>
<p style="margin-top:28px">Combinar mètodes (càrrega alta + pliometria) és el que <b>més millora el rendiment</b>{ref(3)}.</p>
<div style="display:flex;gap:10px;margin-top:50px">{cells}</div>
<p style="margin-top:44px;font-size:30px;color:#9AA5AC">Exemple orientatiu. Als estudis es feien <b>d'1 a 4 sessions</b> de força per setmana{ref(2,3)}. La força, lluny de les sèries o en dies de cursa suau.</p>
<div style="display:flex;justify-content:space-between;margin-top:30px">{ill('q_paret.png', 290, 290, '', '1')}{ill('q_esquat.png', 290, 290, '', '2')}{ill('q_salt.png', 290, 290, '', '3')}</div>
{card('[3] Llanos-Lagos C et al. <i>Sports Med</i> 2024;54:1801 · Revisió sistemàtica i metaanàlisi')}</div>"""

row = lambda ic, col, t: f'<div style="display:flex;gap:24px;align-items:flex-start;margin-top:30px"><div style="width:62px;height:62px;border-radius:50%;background:{col};color:#0B0F12;font-size:36px;font-weight:900;display:flex;align-items:center;justify-content:center;flex-shrink:0">{ic}</div><p style="font-size:34px">{t}</p></div>'
S[7] = f"""<div class="s">{pg(7)}<div class="k">Sense vendre fum</div>
<h2>I les <em>lesions?</em></h2>
<div style="margin-top:34px;border:3px solid #D4FF3F;border-radius:22px;padding:22px 30px"><p style="font-size:38px"><b>Rendiment:</b> sí, clar. La força millora l'economia i el temps de cursa{ref(5)}.</p></div>
{row('✓', '#D4FF3F', 'Programa de maluc i core <b>guiat per un fisio</b>: un 39 % menys de lesions per sobrecàrrega en corredors que començaven' + ref(6))}
{row('✓', '#D4FF3F', 'Força del peu, amb seguiment: menys lesions en un any' + ref(7))}
{row('✗', '#FF5A5A', 'Programa de força <b>pel teu compte</b>, amb un vídeo: no va reduir lesions' + ref(8))}
<p style="margin-top:36px;font-size:38px;font-weight:800;color:#fff">Ajuda quan és <span style="color:#D4FF3F">guiat i progressiu.</span></p>
{card('[5] Ramos-Campo DJ <i>JSCR</i> 2025 · [6] Leppänen M <i>BJSM</i> 2024 · [7] Taddei UT <i>AJSM</i> 2020 · [8] Toresdahl BG <i>Sports Health</i> 2020')}</div>"""

S[8] = f"""<div class="s" style="padding:0;background:#0B0F12">
<img src="{(F/'trail_utmb_vallaran_2026_horitzontal.jpg').as_uri()}" style="position:absolute;top:0;left:-800px;height:1350px;filter:brightness(.8) contrast(1.1) saturate(1.08)">
<div style="position:absolute;left:0;right:0;top:0;height:420px;background:linear-gradient(180deg,rgba(11,15,18,.92) 0%,rgba(11,15,18,.75) 55%,rgba(11,15,18,0) 100%)"></div>
<div style="position:absolute;left:0;right:0;bottom:0;height:470px;background:linear-gradient(0deg,rgba(11,15,18,.95) 0%,rgba(11,15,18,.85) 60%,rgba(11,15,18,0) 100%)"></div>
<div style="position:absolute;top:48px;left:70px;right:70px;font-weight:900;font-size:84px;line-height:.96;letter-spacing:-2.5px;text-transform:uppercase;color:#fff">Vols el teu <span style="color:#D4FF3F">pla de força?</span></div>
<div style="position:absolute;bottom:60px;left:70px;right:70px;border:4px solid #D4FF3F;border-radius:22px;padding:22px 30px;background:rgba(11,15,18,.7)">
<div style="font-size:40px;font-weight:800">WhatsApp <span style="color:#D4FF3F">627 148 092</span></div>
<div style="font-size:40px;font-weight:800;margin-top:8px">Tonus <span style="color:#D4FF3F">601 983 214</span> <span style="font-size:28px;color:#B9C1C6;font-weight:600">«demana per mi»</span></div>
<div style="font-size:40px;font-weight:800;margin-top:8px">🌐 <span style="color:#D4FF3F">marcvallfisio.com</span></div></div></div>"""

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg_ = await b.new_page(viewport={"width": 1080, "height": 1350})
        for n, h in S.items():
            t = D / "_tmp.html"; t.write_text(f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body>{h}</body></html>")
            await pg_.goto(t.as_uri()); await pg_.wait_for_timeout(500)
            await pg_.screenshot(path=str(D / f"forca_{n}.png"))
        await b.close()
asyncio.run(main())
