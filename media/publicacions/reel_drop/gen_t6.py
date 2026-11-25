"""Text d'adaptació a l'escena final (substitueix la veu de les 8–12 setmanes), 25/11."""
import asyncio, pathlib
from playwright.async_api import async_playwright
OUT = pathlib.Path(__file__).parent / "v3" / "t6_adaptacio.png"
H = '''<html><head><meta charset=utf-8><style>*{margin:0;padding:0}body{background:transparent;font-family:Inter,sans-serif}</style></head><body>
<div style="width:1080px;height:1920px;position:relative"><div style="position:absolute;left:0;right:0;top:0;height:470px;background:linear-gradient(180deg,rgba(11,15,18,.92) 0%,rgba(11,15,18,.85) 62%,rgba(11,15,18,0) 100%)"></div>
<div style="position:absolute;top:110px;left:60px;right:60px;text-align:center;font-weight:900;text-transform:uppercase;letter-spacing:-2px;line-height:1.02">
<div style="font-size:64px;color:#fff">Vols canviar de drop?</div><div style="font-size:64px;color:#fff">Fes-ho a poc a poc:</div>
<div style="font-size:84px;color:#D4FF3F;margin-top:10px">12 setmanes o més</div></div></div></body></html>'''
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        await pg.set_content(H); await pg.wait_for_timeout(300); await pg.screenshot(path=str(OUT), omit_background=True); await b.close()
asyncio.run(main())
