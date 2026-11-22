"""Stories setmana de lesions: pregunta (dl 23) i com demanar cita (dv 27)."""
import asyncio, base64, pathlib
from playwright.async_api import async_playwright
D = pathlib.Path(__file__).parent; F = D.parent.parent / "fotos_standard"
def b64(n): return base64.b64encode((F / n).read_bytes()).decode()
CSS = "*{margin:0;padding:0;box-sizing:border-box}body{width:1080px;height:1920px;font-family:Inter,sans-serif;background:#0B0F12;overflow:hidden}"
def bg(n, pos):
    return f'<img src="data:image/jpeg;base64,{b64(n)}" style="position:absolute;left:0;top:480px;width:1080px;height:1440px;object-fit:cover;object-position:{pos}">'
PREG = f"""<div style="position:relative;width:1080px;height:1920px">{bg("trail_utmb_vallaran_2026_vertical.jpg","50% 40%")}
<div style="position:absolute;inset:0;background:linear-gradient(180deg,#0B0F12 0%,#0B0F12 26%,rgba(11,15,18,0) 36%,rgba(11,15,18,0) 70%,rgba(11,15,18,.6) 100%)"></div>
<div style="position:absolute;top:200px;left:70px;right:70px">
<div style="font-size:30px;font-weight:800;letter-spacing:5px;color:#D4FF3F">SETMANA DE LESIONS</div>
<div style="font-weight:900;font-size:100px;line-height:.98;letter-spacing:-3px;text-transform:uppercase;color:#fff;margin-top:22px">Quina lesió de corredor <span style="color:#D4FF3F">vols que t'expliqui?</span></div>
<div style="font-size:40px;font-weight:600;color:#C9D1D6;margin-top:26px">Vota i divendres t'explico la més votada 👇</div></div>
</div>"""
CITA = f"""<div style="position:relative;width:1080px;height:1920px">{bg("tonus_camilla_bracos_creuats.jpg","50% 40%")}
<div style="position:absolute;inset:0;background:linear-gradient(180deg,#0B0F12 0%,#0B0F12 26%,rgba(11,15,18,0) 36%,rgba(11,15,18,0) 66%,rgba(11,15,18,.9) 82%,rgba(11,15,18,.97) 100%)"></div>
<div style="position:absolute;top:200px;left:70px;right:70px">
<div style="font-weight:900;font-size:104px;line-height:.98;letter-spacing:-3px;text-transform:uppercase;color:#fff">Com demanar <span style="color:#D4FF3F">cita amb mi</span></div></div>
<div style="position:absolute;bottom:170px;left:70px;right:70px">
<div style="font-size:40px;font-weight:600;color:#C9D1D6">Fisioteràpia per a corredors · Tarragona</div>
<div style="margin-top:26px;border:4px solid #D4FF3F;border-radius:26px;padding:26px 34px;background:rgba(11,15,18,.75)">
<div style="font-size:50px;font-weight:800;color:#fff">📲 WhatsApp <span style="color:#D4FF3F">627 148 092</span></div>
<div style="font-size:50px;font-weight:800;color:#fff;margin-top:14px">📞 Tonus <span style="color:#D4FF3F">601 983 214</span></div>
<div style="font-size:36px;color:#B9C1C6;margin-top:6px;padding-left:64px">«demana per mi»</div>
<div style="font-size:50px;font-weight:800;color:#fff;margin-top:14px">🌐 <span style="color:#D4FF3F">marcvallfisio.com</span></div></div></div></div>"""
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        for n, h in (("story_pregunta_lesio", PREG), ("story_cita", CITA)):
            await pg.set_content(f"<html><head><style>{CSS}</style></head><body>{h}</body></html>"); await pg.wait_for_timeout(300)
            await pg.screenshot(path=str(D / f"{n}.png"))
        await b.close()
asyncio.run(main())
