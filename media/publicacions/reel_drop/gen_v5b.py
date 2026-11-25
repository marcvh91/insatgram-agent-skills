"""Overlays de la versió dinàmica (B) del Reel drop, 25/11: títol a dalt (cap a sobre del cap) i paraules clau."""
import asyncio, pathlib
from playwright.async_api import async_playwright
OUT = pathlib.Path(__file__).parent / "v5b"
CSS = "*{margin:0;padding:0;box-sizing:border-box}body{font-family:Inter,sans-serif;background:transparent}"
GRAD = '<div style="position:absolute;left:0;right:0;top:0;height:{h}px;background:linear-gradient(180deg,rgba(11,15,18,.92) 0%,rgba(11,15,18,.85) 60%,rgba(11,15,18,0) 100%)"></div>'
def title():
    return f'''<div style="width:1080px;height:1920px;position:relative">{GRAD.format(h=400)}
<div style="position:absolute;top:70px;left:60px;right:60px;text-align:center;font-weight:900;font-size:68px;line-height:1;letter-spacing:-2.5px;text-transform:uppercase;color:#fff">Molèsties al tendó d'Aquil·les<br><span style="color:#D4FF3F">o al genoll quan corres?</span></div></div>'''
def pop(txt, sub=""):
    s = f'<div style="margin-top:14px;font-weight:800;font-size:40px;color:#fff;letter-spacing:-1px">{sub}</div>' if sub else ""
    return f'''<div style="width:1080px;height:1920px;position:relative">{GRAD.format(h=330)}
<div style="position:absolute;top:70px;left:0;right:0;text-align:center"><span style="display:inline-block;background:#D4FF3F;color:#0B0F12;font-weight:900;font-size:62px;letter-spacing:-2px;padding:12px 30px;white-space:nowrap;border-radius:22px;text-transform:uppercase;transform:rotate(-2deg)">{txt}</span>{s}</div></div>'''
ITEMS = {"title": title(), "pop_drop": pop("El drop 👟"), "pop_cop": pop("De cop"),
         "pop_lloc": pop("La càrrega canvia de lloc"), "pop_setm": pop("8–12 setmanes", "per adaptar-te a un drop nou")}
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        for k, html in ITEMS.items():
            await pg.set_content(f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body>{html}</body></html>"); await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(OUT / f"{k}.png"), omit_background=True)
        await b.close()
asyncio.run(main())
