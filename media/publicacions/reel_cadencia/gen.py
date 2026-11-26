"""Reel «180 passes per minut: mite o veritat?» (setmana 30/11): càmera lenta d'un corredor a la cinta (consentiment signat).
Textos a la franja de baix (terra), sense tapar el corredor; anotacions al fotograma congelat del contacte."""
import asyncio, pathlib
from playwright.async_api import async_playwright
OUT = pathlib.Path(__file__).parent / "ov"
CSS = "*{margin:0;padding:0;box-sizing:border-box}body{font-family:Inter,sans-serif;background:transparent;color:#fff}sup{color:#D4FF3F;font-size:.5em;font-weight:800}b{color:#D4FF3F}"
def low(html, size=62, top=1330):
    return f'''<div style="width:1080px;height:1920px;position:relative">
<div style="position:absolute;left:0;right:0;top:{top-60}px;height:{1920-top+60}px;background:linear-gradient(180deg,rgba(11,15,18,0) 0%,rgba(11,15,18,.88) 14%,rgba(11,15,18,.92) 100%)"></div>
<div style="position:absolute;top:{top}px;left:64px;right:64px;font-weight:900;font-size:{size}px;line-height:1.05;letter-spacing:-2px;text-transform:uppercase">{html}</div></div>'''
SVG = '''<svg width="1080" height="1920" xmlns="http://www.w3.org/2000/svg">
<line x1="580" y1="520" x2="580" y2="1160" stroke="#D4FF3F" stroke-width="8" stroke-dasharray="26 18"/>
<line x1="410" y1="745" x2="140" y2="985" stroke="#FF4D3D" stroke-width="12" stroke-linecap="round"/>
<circle cx="155" cy="1150" r="44" fill="none" stroke="#FF4D3D" stroke-width="10"/>
<line x1="160" y1="1235" x2="575" y2="1235" stroke="#FF4D3D" stroke-width="8"/>
<polygon points="150,1235 185,1215 185,1255" fill="#FF4D3D"/><polygon points="585,1235 550,1215 550,1255" fill="#FF4D3D"/>
<text x="600" y="560" fill="#D4FF3F" font-family="Inter" font-weight="900" font-size="36">EL COS</text>
</svg>'''
ITEMS = {
 "annot": f'<div style="width:1080px;height:1920px">{SVG}</div>',
 "t0": low('180 passes per minut:<br><b>mite o veritat?</b>', 84, 1320),
 "t1": low('Aterra de <b>taló</b> i amb el peu <b>molt per davant</b> del cos', 62),
 "t2": low('Passa llarga = més <b>frenada</b> i més càrrega a la <b>ròtula</b><sup>[1][2]</sup>', 62),
 "t3": low('<b>Mite:</b> no hi ha cap número màgic', 70),
 "t4": low('Puja la <b>teva</b> cadència un <b>5–10 %</b><sup>[2][3]</sup>', 70),
 "t5": low('Passa més curta → peu més a prop del cos → <b>menys càrrega al genoll</b><sup>[1][2]</sup>', 58),
 "t6": low('Molèsties a la part davantera del genoll? És de les <b>primeres coses</b> que treballem<sup>[3]</sup>', 56),
 "t7": low('Compta les teves passes <b>30 s × 2</b> i escriu-me el número 👇<div style="margin-top:22px;font-size:38px;letter-spacing:-.5px;text-transform:none;font-weight:800;color:#fff">WhatsApp <b>627 148 092</b> · Tonus <b>601 983 214</b><br><b>marcvallfisio.com</b></div>', 60, 1290),
}
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        for k, h in ITEMS.items():
            await pg.set_content(f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body>{h}</body></html>"); await pg.wait_for_timeout(250)
            await pg.screenshot(path=str(OUT / f"{k}.png"), omit_background=True)
        await b.close()
asyncio.run(main())
