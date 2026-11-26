"""Portada del Reel cintilla: fotograma del ganxo (s'atura tocant-se el genoll) amb títol gran dins la zona que es veu a la quadrícula (3:4)."""
import asyncio, pathlib, subprocess
from playwright.async_api import async_playwright
R = pathlib.Path(__file__).parent; S = pathlib.Path('/home/claude/cint/src'); OUT = R / 'v2'
T = '''<html><head><meta charset=utf-8><style>*{margin:0;padding:0}body{background:transparent;font-family:Inter,sans-serif}</style></head><body>
<div style="width:1080px;height:1920px;position:relative">
<div style="position:absolute;left:0;right:0;top:0;height:760px;background:linear-gradient(180deg,rgba(11,15,18,.92) 0%,rgba(11,15,18,.82) 70%,rgba(11,15,18,0) 100%)"></div>
<div style="position:absolute;top:262px;left:56px;right:56px;font-weight:900;font-size:98px;line-height:.98;letter-spacing:-3.5px;text-transform:uppercase;color:#fff">Mal a la cara externa <span style="color:#D4FF3F">del genoll?</span></div>
</div></body></html>'''
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        await pg.set_content(T); await pg.wait_for_timeout(300); await pg.screenshot(path=str(OUT / 't_cover.png'), omit_background=True); await b.close()
asyncio.run(main())
def cover(n, clip, t, z, cx, head, at=0.40):
    w, h = 2160 / z, 3840 / z; x0 = min(max(cx * 2160 - w / 2, 0), 2160 - w); y0 = min(max(head * 3840 - at * h, 0), 3840 - h)
    subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-ss', str(t), '-i', S / f'IMG_{clip}.mov', '-i', OUT / 't_cover.png', '-frames:v', '1', '-filter_complex',
                    f"[0:v]crop={w:.0f}:{h:.0f}:{x0:.0f}:{y0:.0f},scale=1080:1920:flags=lanczos[b];[b][1:v]overlay=0:0", '-q:v', '2', OUT / f'portada_{n}.jpg'], check=True)
cover('A', 4197, 4.25, 1.2, 0.74, 0.39)
cover('B', 4197, 4.6, 1.2, 0.76, 0.41)
cover('C', 4197, 4.9, 1.2, 0.78, 0.42)
cover('D', 4198, 8.4, 1.25, 0.45, 0.21, at=0.38)
