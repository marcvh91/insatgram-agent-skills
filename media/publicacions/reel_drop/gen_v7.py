"""Reel drop v7 (rodatge 26/11): overlays nous. Títol del ganxo a dalt (sobre el cap), targetes de tensió
més baixes (sota les mans), crida amb contacte i màscares per il·luminar cada sabatilla."""
import asyncio, pathlib, sys
from PIL import Image, ImageDraw
D = pathlib.Path(__file__).parent; OUT = D / "v7"; OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(D.parent / "carrusel_drop")); sys.path.insert(0, str(D))
from svgkit import leg_panel
from playwright.async_api import async_playwright
CSS = """*{margin:0;padding:0;box-sizing:border-box}body{font-family:Inter,sans-serif;color:#E8ECEF;background:transparent}
sup{color:#D4FF3F;font-size:22px;font-weight:800}"""
def ref(*n): return '<sup>' + ''.join(f'[{i}]' for i in n) + '</sup>'
def topband(h): return f'<div style="position:absolute;left:0;right:0;top:0;height:{h}px;background:linear-gradient(180deg,rgba(11,15,18,.93) 0%,rgba(11,15,18,.86) 62%,rgba(11,15,18,0) 100%)"></div>'
TITLE = 'Molèsties al tendó d\'Aquil·les <span style="color:#D4FF3F">o al genoll quan corres?</span>'
def title(top, fs, h, TITLE=TITLE):
    return f'''<div style="width:1080px;height:1920px;position:relative">{topband(h)}
<div style="position:absolute;top:{top}px;left:60px;right:60px;text-align:center;font-weight:900;font-size:{fs}px;line-height:1;letter-spacing:-2.5px;text-transform:uppercase;color:#fff">{TITLE}</div></div>'''
def cards(show_baix, top=1160, show_alt=True, cw=300, lw=270):
    """Targetes grans als costats (com a la v2), apareixen quan les anomena."""
    def card(side, t, txt, leg, vis):
        x = "left:24px" if side == "L" else "right:24px"
        return (f'<div style="position:absolute;top:{top}px;{x};width:{cw}px;opacity:{1 if vis else 0};background:rgba(11,15,18,.9);border:4px solid #D4FF3F;border-radius:26px;padding:18px 8px 16px;text-align:center">'
                f'<div style="font-size:34px;font-weight:900;letter-spacing:1px;color:#D4FF3F">{t}</div>{leg}'
                f'<div style="font-size:30px;font-weight:800;line-height:1.2;margin-top:6px">{txt}</div></div>')
    L = card("L", "DROP ALT", f"🔴 Genoll (ròtula)<br>fins a +15 %{ref(1)}", leg_panel(f"a{show_baix}{show_alt}", 36, 22, "knee", w=lw), show_alt)
    R = card("R", "DROP BAIX", f"🔴 Bessó i<br>Aquil·les{ref(2,3)}", leg_panel(f"b{show_baix}{show_alt}", 26, 26, "calf", w=lw), show_baix)
    return f'<div style="width:1080px;height:1920px;position:relative">{L}{R}</div>'
POP = lambda big, sub: f'''<div style="width:1080px;height:1920px;position:relative">{topband(330)}
<div style="position:absolute;top:70px;left:0;right:0;text-align:center"><span style="display:inline-block;background:#D4FF3F;color:#0B0F12;font-weight:900;font-size:66px;letter-spacing:-2px;padding:12px 30px;border-radius:22px;text-transform:uppercase;transform:rotate(-2deg)">{big}</span>
<div style="margin-top:14px;font-weight:800;font-size:40px;color:#fff;letter-spacing:-1px">{sub}</div></div></div>'''
CTA = """<div style="width:1080px;height:1920px;position:relative">
<div style="position:absolute;bottom:0;left:0;right:0;height:820px;background:linear-gradient(0deg,rgba(11,15,18,.96) 0%,rgba(11,15,18,.88) 60%,rgba(11,15,18,0) 100%)"></div>
<div style="position:absolute;bottom:150px;left:70px;right:70px">
<div style="font-weight:900;font-size:76px;line-height:1;letter-spacing:-2px;text-transform:uppercase;color:#fff">Escriu-me <span style="color:#D4FF3F">i ho mirem.</span></div>
<div style="margin-top:28px;border:4px solid #D4FF3F;border-radius:24px;padding:26px 34px;background:rgba(11,15,18,.6)">
<div style="font-size:44px;font-weight:800;color:#fff">WhatsApp <span style="color:#D4FF3F">627 148 092</span></div>
<div style="font-size:44px;font-weight:800;margin-top:10px;color:#fff">Tonus <span style="color:#D4FF3F">601 983 214</span> <span style="font-size:30px;color:#B9C1C6;font-weight:600">«demana per mi»</span></div>
<div style="font-size:44px;font-weight:800;margin-top:10px;color:#fff">🌐 <span style="color:#D4FF3F">marcvallfisio.com</span></div></div></div></div>"""
ITEMS = {"t_final": title(80, 76, 420, TITLE='I tu, <span style="color:#D4FF3F">quin drop portes?</span>'), "t_ganxo": title(70, 64, 430), "t_cover": title(265, 74, 640), "d5_alt": cards(False), "d5_tots": cards(True), "d5_baix": cards(True, show_alt=False),
         "t_final": title(80, 84, 360, 'I tu, <span style="color:#D4FF3F">quin drop portes?</span>'), "pop_setm": POP("8–12 setmanes", "d'adaptació a un drop nou"), "pop_lloc": POP("Canvia de lloc", "la càrrega no desapareix"), "cta": CTA}
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        for k, h in ITEMS.items():
            await pg.set_content(f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body>{h}</body></html>"); await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(OUT / f"{k}.png"), omit_background=True)
        await b.close()
asyncio.run(main())
# màscares de les 3 sabatilles (enfosqueix les files no actives)
ROWS = [(300, 760), (760, 1250), (1250, 1700)]
for i in range(3):
    m = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(m)
    for j, (a, b) in enumerate(ROWS):
        if j != i: d.rectangle([0, a, 1080, b], fill=(11, 15, 18, 190))
    m.save(OUT / f"mask_{i}.png")
