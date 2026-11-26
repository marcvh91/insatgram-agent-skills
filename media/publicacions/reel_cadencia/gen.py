"""Reel «180 passes per minut: mite o veritat?» (setmana 30/11): càmera lenta d'un corredor a la cinta (consentiment signat).
Textos a la franja de baix (terra), sense tapar el corredor; anotacions al fotograma congelat del contacte."""
import asyncio, pathlib
from playwright.async_api import async_playwright
OUT = pathlib.Path(__file__).parent / "ov"
CSS = "*{margin:0;padding:0;box-sizing:border-box}body{font-family:Inter,sans-serif;background:transparent;color:#fff}sup{color:#D4FF3F;font-size:.5em;font-weight:800}b{color:#D4FF3F}"
def low(html, size=62, top=1330):
    return f'''<div style="width:1080px;height:1920px;position:relative">
<div style="position:absolute;left:0;right:0;top:{top-40}px;height:{1920-top+40}px;background:linear-gradient(180deg,rgba(11,15,18,0) 0%,rgba(11,15,18,.9) 8%,rgba(11,15,18,.94) 100%)"></div>
<div style="position:absolute;top:{top}px;left:64px;right:64px;font-weight:900;font-size:{size}px;line-height:1.05;letter-spacing:-2px;text-transform:uppercase">{html}</div></div>'''
SVG = '''<svg width="1080" height="1920" xmlns="http://www.w3.org/2000/svg">
<circle cx="510" cy="1120" r="70" fill="none" stroke="#FF4D3D" stroke-width="12"/>
<line x1="360" y1="960" x2="450" y2="1058" stroke="#FF4D3D" stroke-width="10" stroke-linecap="round"/>
<polygon points="466,1076 428,1064 454,1038" fill="#FF4D3D"/>
<rect x="150" y="890" width="230" height="78" rx="14" fill="#FF4D3D"/>
<text x="265" y="944" text-anchor="middle" fill="#fff" font-family="Inter" font-weight="900" font-size="46">TALÓ</text>
</svg>'''
T = 1335
ITEMS = {
 "annot": f'<div style="width:1080px;height:1920px">{SVG}</div>',
 "t0": low('180 passes per minut:<br><b>mite o veritat?</b>', 100, T),
 "t1": low('Mira com aterra:<br>de <b>taló</b> 👆', 96, T),
 "t2": low('Taló + passa llarga:<br>més <b>frenada</b> i més<br>càrrega al <b>genoll</b><sup>[1][2]</sup>', 84, T),
 "t3": low('<b>Mite:</b> no hi ha cap<br>número màgic', 96, T),
 "t4": low('Puja la <b>teva</b><br>cadència un <b>5–10 %</b><sup>[2][3]</sup>', 96, T),
 "t5": low('Passa més curta,<br>menys taló i <b>menys<br>càrrega al genoll</b><sup>[1][2]</sup>', 84, T),
 "t6": low('Et fa mal el genoll?<br>És de les <b>primeres<br>coses</b> que treballem<sup>[3]</sup>', 84, T),
 "t7": low('Compta les passes<br><b>30 s × 2</b> i escriu-me<br>el número 👇<div style="margin-top:26px;font-size:42px;letter-spacing:-.5px;text-transform:none;font-weight:800;color:#fff">WhatsApp <b>627 148 092</b> · Tonus <b>601 983 214</b><br><b>marcvallfisio.com</b></div>', 76, 1310),
}
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        for k, h in ITEMS.items():
            await pg.set_content(f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body>{h}</body></html>"); await pg.wait_for_timeout(250)
            await pg.screenshot(path=str(OUT / f"{k}.png"), omit_background=True)
        await b.close()
asyncio.run(main())
