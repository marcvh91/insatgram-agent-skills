"""Story resultat enquesta lesions (dt 24/11): guanya la cintilla."""
import asyncio, base64, pathlib, sys
from playwright.async_api import async_playwright
D = pathlib.Path(__file__).parent; F = D.parent.parent / "fotos_standard"
b64 = base64.b64encode((F / "trail_cingle_roca_samarreta_llop.jpg").read_bytes()).decode()
R = [("Cintilla del corredor", 47, True), ("Ruptura muscular (isquio o bessó)", 18, False), ("Tendinopatia (Aquil·les o isquio)", 18, False), ("Fascitis plantar", 18, False)]
if len(sys.argv) > 1: R = [(n, int(p), i == 0) for i, (n, p) in enumerate(zip([r[0] for r in R], sys.argv[1:5]))]
bars = "".join(f'''<div style="position:relative;height:{86 if w else 64}px;border-radius:16px;background:{'#EEF2E6' if w else '#1A2126'};overflow:hidden;margin-top:14px;border:{'3px solid #D4FF3F' if w else '0'}">
<div style="position:absolute;inset:0;width:{p}%;background:{'#D4FF3F' if w else '#3A454C'}"></div>
<div style="position:absolute;inset:0;display:flex;align-items:center;justify-content:space-between;padding:0 24px;font-weight:{900 if w else 700};font-size:{38 if w else 30}px;color:{'#0B0F12' if w else '#E8ECEF'}">
<span style="{'' if w else ''}">{'🏆 ' if w else ''}{n}</span><span style="color:{'#0B0F12' if w else '#C9D1D6'}">{p} %</span></div></div>''' for n, p, w in R)
H = f"""<div style="position:relative;width:1080px;height:1920px;background:#0B0F12">
<img src="data:image/jpeg;base64,{b64}" style="position:absolute;left:0;top:820px;width:1080px;height:1100px;object-fit:cover;object-position:47% 50%">
<div style="position:absolute;left:0;right:0;top:820px;height:260px;background:linear-gradient(180deg,#0B0F12,rgba(11,15,18,0))"></div>
<div style="position:absolute;top:150px;left:70px;right:70px">
<div style="font-size:30px;font-weight:800;letter-spacing:5px;color:#D4FF3F">RESULTAT DE L'ENQUESTA</div>
<div style="font-weight:900;font-size:92px;line-height:.96;letter-spacing:-3px;text-transform:uppercase;color:#fff;margin-top:18px">Guanya la <span style="color:#D4FF3F">cintilla del corredor</span></div>
<div style="margin-top:26px">{bars}</div>
<div style="font-size:38px;font-weight:700;color:#E8ECEF;margin-top:28px">Divendres t'explico per què fa mal al genoll i què pots fer 👇</div></div></div>"""
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        await pg.set_content(f"<html><head><style>*{{margin:0;padding:0;box-sizing:border-box}}body{{font-family:Inter,sans-serif}}</style></head><body>{H}</body></html>"); await pg.wait_for_timeout(400)
        await pg.screenshot(path=str(D / "story_resultat_cintilla.png")); await b.close()
asyncio.run(main())
