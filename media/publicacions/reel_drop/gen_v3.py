"""Reel drop v3: overlays de títol (franja inferior, sobre el tors) per als clips reals."""
import asyncio, pathlib, sys
from playwright.async_api import async_playwright
D = pathlib.Path(__file__).parent; OUT = D / "v3"; OUT.mkdir(exist_ok=True)
CSS = "*{margin:0;padding:0;box-sizing:border-box}body{font-family:Inter,sans-serif;background:transparent}"

def band(title_html, tag, top, fs=96):
    tag_html = f'<div style="display:inline-block;background:#D4FF3F;color:#0B0F12;font-weight:900;font-size:44px;padding:16px 28px;border-radius:14px;margin-top:28px">{tag}</div>' if tag else ""
    return f"""<div style="width:1080px;height:1920px;position:relative">
<div style="position:absolute;left:0;right:0;top:{top-90}px;height:{1920-top+90}px;background:linear-gradient(180deg,rgba(11,15,18,0) 0%,rgba(11,15,18,.82) 22%,rgba(11,15,18,.9) 100%)"></div>
<div style="position:absolute;top:{top}px;left:70px;right:70px">
<div style="font-weight:900;font-size:{fs}px;line-height:.98;letter-spacing:-3px;text-transform:uppercase;color:#fff">{title_html}</div>{tag_html}</div></div>"""

OV = {
    "t1_ganxo": band('Molèsties al genoll <span style="color:#D4FF3F">quan corres?</span>', "👟 I el calçat, l'has mirat mai?", int(sys.argv[1]) if len(sys.argv) > 1 else 1060, int(sys.argv[3]) if len(sys.argv) > 3 else 96),
    "t5_canvi": band('El canvi de calçat <span style="color:#D4FF3F">i l\'adaptació al drop!</span>', "", int(sys.argv[2]) if len(sys.argv) > 2 else 1060),
}

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        for k, h in OV.items():
            await pg.set_content(f"<html><head><style>{CSS}</style></head><body>{h}</body></html>"); await pg.wait_for_timeout(250)
            await pg.screenshot(path=str(OUT / f"{k}.png"), omit_background=True)
        await b.close()
asyncio.run(main())

# --- CTA final amb web (foto del banc + WhatsApp + Tonus + web)
CTA_WEB = """<div style="width:1080px;height:1920px;position:relative">
<div style="position:absolute;bottom:0;left:0;right:0;height:980px;background:linear-gradient(0deg,rgba(11,15,18,.97) 0%,rgba(11,15,18,.9) 62%,rgba(11,15,18,0) 100%)"></div>
<div style="position:absolute;bottom:250px;left:70px;right:70px">
<div style="font-weight:900;font-size:78px;line-height:1;letter-spacing:-2px;text-transform:uppercase;color:#fff">Et fa mal el genoll? <span style="color:#D4FF3F">Vine i ho mirem.</span></div>
<div style="margin-top:30px;border:4px solid #D4FF3F;border-radius:24px;padding:28px 36px;background:rgba(11,15,18,.6)">
<div style="font-size:46px;font-weight:800;color:#fff">WhatsApp <span style="color:#D4FF3F">627 148 092</span></div>
<div style="font-size:46px;font-weight:800;margin-top:10px;color:#fff">Tonus <span style="color:#D4FF3F">601 983 214</span> <span style="font-size:32px;color:#B9C1C6;font-weight:600">«demana per mi»</span></div>
<div style="font-size:46px;font-weight:800;margin-top:10px;color:#fff">🌐 <span style="color:#D4FF3F">marcvallfisio.com</span></div></div></div></div>"""
async def cta():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        await pg.set_content(f"<html><head><style>{CSS}</style></head><body>{CTA_WEB}</body></html>"); await pg.wait_for_timeout(250)
        await pg.screenshot(path=str(OUT / "cta_web.png"), omit_background=True); await b.close()
asyncio.run(cta())
