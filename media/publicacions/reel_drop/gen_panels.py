"""Panells del Reel «drop»: meitat superior 1080x960 (el Marc parla a la meitat inferior)
+ 2 overlays transparents 1080x1920 (portada amb títol i CTA)."""
import asyncio, pathlib, sys
D = pathlib.Path(__file__).parent
sys.path.insert(0, str(D.parent / "carrusel_drop"))
from svgkit import shoe_svg, leg_panel, shoe
from playwright.async_api import async_playwright

CSS = """*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Inter,sans-serif;color:#E8ECEF;overflow:hidden;background:transparent}
.p{width:1080px;height:960px;background:#0B0F12;padding:70px 60px 40px;display:flex;flex-direction:column;align-items:center}
h2{font-weight:900;font-size:66px;line-height:1;letter-spacing:-2px;text-transform:uppercase;text-align:center;color:#fff}
h2 em{font-style:normal;color:#D4FF3F}
.t{font-size:40px;font-weight:600;text-align:center;line-height:1.25;margin-top:16px}
b{color:#D4FF3F}sup{color:#D4FF3F;font-size:24px;font-weight:800}
.lab{font-size:26px;font-weight:900;letter-spacing:2px;color:#D4FF3F}"""

def ref(*n): return '<sup>' + ''.join(f'[{i}]' for i in n) + '</sup>'

P = {}
P["p2_drop"] = f"""<div class="p"><h2>El <em>drop</em></h2>
<div class="t">Diferència d'altura entre el <b>taló</b> i la <b>punta</b></div>
<div style="margin-top:30px">{shoe_svg("a", 32, 24, w=1000, dims=True, pad=(190, 330, 330, 60))}</div></div>"""

rows = ""
for uid, h, t, lab in [("z", 26, 26, "0 mm"), ("m", 29, 24, "4–6 mm"), ("x", 34, 23, "8–12 mm")]:
    rows += (f'<div style="display:flex;align-items:center;margin-top:6px"><div style="width:220px;font-size:48px;font-weight:900;color:#D4FF3F;white-space:nowrap">{lab}</div>'
             f'{shoe_svg(uid, h, t, w=620, dims=True, pad=(190, 330, 330, 55), px=3.6)}</div>')
P["p3_tipus"] = f"""<div class="p" style="padding-top:50px"><h2>De <em>0 a 12 mm</em></h2>{rows}</div>"""

P["p4_genoll"] = f"""<div class="p" style="padding-top:50px"><h2>Drop <em>alt</em></h2>
<div style="display:flex;align-items:center;gap:20px;margin-top:6px">{leg_panel("k", 36, 22, "knee", w=520)}
<div class="t" style="text-align:left;width:420px;font-size:42px">🔴 <b>Ròtula:</b><br>fins a +15 % de tensió{ref(1)}</div></div></div>"""

P["p5_besso"] = f"""<div class="p" style="padding-top:50px"><h2>Drop <em>baix</em></h2>
<div style="display:flex;align-items:center;gap:20px;margin-top:6px">{leg_panel("c", 26, 26, "calf", w=520)}
<div class="t" style="text-align:left;width:420px;font-size:42px">🔴 <b>Bessó i Aquil·les</b> treballen més{ref(2,3)}<br><br>🔵 Ròtula, menys{ref(1)}</div></div></div>"""

P["p6_lloc"] = """<div class="p" style="justify-content:center"><div style="font-size:92px;font-weight:900;line-height:1.02;letter-spacing:-3px;text-transform:uppercase;text-align:center">La càrrega<br>no desapareix.<br><em style="font-style:normal;color:#D4FF3F">Canvia de lloc.</em></div></div>"""

weeks = "".join(f'<div style="flex:1;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;gap:8px"><div style="width:100%;height:{int(30+i*30)}px;background:{"#D4FF3F" if i==11 else "#5E6B12"};border-radius:8px 8px 0 0"></div><div style="font-size:26px;color:#8A9399;font-weight:800">{i+1}</div></div>' for i in range(12))
P["p7_poc"] = f"""<div class="p"><h2>Canvia <em>a poc a poc</em></h2>
<div class="t"><b>12 setmanes</b> o més de transició{ref(4)}</div>
<div style="display:flex;gap:12px;width:100%;height:440px;margin-top:40px">{weeks}</div>
<div style="font-size:26px;color:#8A9399;font-weight:800;letter-spacing:2px;margin-top:14px">SETMANES · % DE SORTIDES AMB LES NOVES</div></div>"""

items = "".join(f'<div style="display:flex;align-items:center;gap:26px;margin-top:30px;width:100%"><div style="width:70px;height:70px;border-radius:50%;background:#D4FF3F;color:#0B0F12;font-size:40px;font-weight:900;display:flex;align-items:center;justify-content:center;flex-shrink:0">{i}</div><div style="font-size:46px;font-weight:700">{t}</div></div>' for i, t in [(1, "Lesions prèvies"), (2, "Pujades de càrrega"), (3, "Com es mou el maluc")])
P["p8_tot"] = f"""<div class="p" style="align-items:flex-start;padding:70px 90px"><h2 style="text-align:left">El drop <em>no ho és tot</em></h2>
<div class="t" style="text-align:left">Al genoll pesen més:{ref(7)}</div>{items}</div>"""

OV = {}
OV["ov1_titol"] = """<div style="width:1080px;height:1920px;position:relative">
<div style="position:absolute;top:0;left:0;right:0;height:900px;background:linear-gradient(180deg,rgba(11,15,18,.95) 0%,rgba(11,15,18,.85) 60%,rgba(11,15,18,0) 100%)"></div>
<div style="position:absolute;top:230px;left:70px;right:70px">
<div style="font-weight:900;font-size:104px;line-height:.98;letter-spacing:-3px;text-transform:uppercase;color:#fff">Tens mal al genoll quan corres <span style="color:#D4FF3F">i no saps per què?</span></div>
<div style="display:inline-block;background:#D4FF3F;color:#0B0F12;font-weight:900;font-size:44px;padding:16px 28px;border-radius:14px;margin-top:34px">👟 I si fossin les sabatilles?</div></div></div>"""
OV["ov9_cta"] = """<div style="width:1080px;height:1920px;position:relative">
<div style="position:absolute;bottom:0;left:0;right:0;height:900px;background:linear-gradient(0deg,rgba(11,15,18,.96) 0%,rgba(11,15,18,.88) 60%,rgba(11,15,18,0) 100%)"></div>
<div style="position:absolute;bottom:300px;left:70px;right:70px">
<div style="font-weight:900;font-size:78px;line-height:1;letter-spacing:-2px;text-transform:uppercase;color:#fff">Et fa mal el genoll? <span style="color:#D4FF3F">Vine i ho mirem.</span></div>
<div style="margin-top:34px;border:4px solid #D4FF3F;border-radius:24px;padding:30px 36px;background:rgba(11,15,18,.6)">
<div style="font-size:46px;font-weight:800">WhatsApp <span style="color:#D4FF3F">627 148 092</span></div>
<div style="font-size:46px;font-weight:800;margin-top:12px">Tonus <span style="color:#D4FF3F">601 983 214</span></div>
<div style="font-size:36px;margin-top:12px;color:#B9C1C6">«Demana per mi»</div></div></div></div>"""

async def main():
    out = D / "panels"; out.mkdir(exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": 1080, "height": 960})
        for k, h in P.items():
            await pg.set_content(f"<html><head><style>{CSS}</style></head><body>{h}</body></html>"); await pg.wait_for_timeout(250)
            await pg.screenshot(path=str(out / f"{k}.png"))
        await pg.set_viewport_size({"width": 1080, "height": 1920})
        for k, h in OV.items():
            await pg.set_content(f"<html><head><style>{CSS}</style></head><body>{h}</body></html>"); await pg.wait_for_timeout(250)
            await pg.screenshot(path=str(out / f"{k}.png"), omit_background=True)
        await b.close()
asyncio.run(main())
