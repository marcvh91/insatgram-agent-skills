"""Nou títol del Reel drop (24/11): Aquil·les o genoll. Regenera t1_ganxo, cover_title i portada."""
import asyncio, pathlib
from PIL import Image
from playwright.async_api import async_playwright
D = pathlib.Path(__file__).parent; OUT = D / "v3"; F = D.parent.parent / "fotos_standard"
CSS = "*{margin:0;padding:0;box-sizing:border-box}body{font-family:Inter,sans-serif;background:transparent}"
T = 'Molèsties al tendó d\'Aquil·les <span style="color:#D4FF3F">o al genoll quan corres?</span>'
def band(top, fs):
    return f"""<div style="width:1080px;height:1920px;position:relative">
<div style="position:absolute;left:0;right:0;top:{top-90}px;height:{1920-top+90}px;background:linear-gradient(180deg,rgba(11,15,18,0) 0%,rgba(11,15,18,.82) 22%,rgba(11,15,18,.9) 100%)"></div>
<div style="position:absolute;top:{top}px;left:70px;right:70px">
<div style="font-weight:900;font-size:{fs}px;line-height:.98;letter-spacing:-3px;text-transform:uppercase;color:#fff">{T}</div>
<div style="display:inline-block;background:#D4FF3F;color:#0B0F12;font-weight:900;font-size:42px;padding:14px 26px;border-radius:14px;margin-top:24px">👟 I el calçat, l'has mirat mai?</div></div></div>"""
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        for name, top, fs in (("t1_ganxo", 1440, 74), ("cover_title", 1290, 84)):
            await pg.set_content(f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body>{band(top, fs)}</body></html>"); await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(OUT / f"{name}.png"), omit_background=True)
        await b.close()
asyncio.run(main())
ph = Image.open(F / "polo_tonus_kiprun_somriu_2.jpg").convert("RGB"); w, h = ph.size; s = max(1080 / w, 1920 / h)
ph = ph.resize((round(w * s), round(h * s))); x = (ph.width - 1080) // 2; y = (ph.height - 1920) // 2; ph = ph.crop((x, y, x + 1080, y + 1920)).convert("RGBA")
ph.alpha_composite(Image.open(OUT / "cover_title.png")); ph.convert("RGB").save(OUT / "portada.jpg", quality=92)
