import asyncio, pathlib
from playwright.async_api import async_playwright
D = pathlib.Path(__file__).parent.resolve(); U = lambda n: (D / n).as_uri()
CSS = "*{margin:0;padding:0;box-sizing:border-box}body{font-family:Inter,sans-serif;background:#0B0F12}"
def pill(t, sub=""):
    s = f'<div style="font-size:30px;font-weight:600;color:#C9D1D6;margin-top:6px">{sub}</div>' if sub else ""
    return f'<div style="position:absolute;left:50px;bottom:40px;right:50px"><div style="display:inline-block;background:#D4FF3F;color:#0B0F12;font-weight:900;font-size:40px;padding:12px 22px;border-radius:12px;text-transform:uppercase;letter-spacing:-.5px">{t}</div>{s}</div>'
def split(img, label, sub="", tag=""):
    t = f'<div style="position:absolute;top:30px;left:50px;font-size:26px;font-weight:800;letter-spacing:4px;color:#D4FF3F">{tag}</div>' if tag else ""
    return f"""<div style="position:relative;width:1080px;height:1920px">
<div style="position:absolute;top:0;left:0;width:1080px;height:1000px;background:#121212;overflow:hidden"><img src="{U(img)}" style="width:1080px;height:1000px">{t}{pill(label, sub)}</div>
<img src="{U('marc_bottom.jpg')}" style="position:absolute;top:1000px;left:0;width:1080px;height:920px">
<div style="position:absolute;top:1000px;left:0;right:0;height:6px;background:#D4FF3F"></div></div>"""
def placeholder(txt):
    return f"""<div style="position:relative;width:1080px;height:1920px"><div style="position:absolute;top:0;left:0;width:1080px;height:1000px;background:#121212;display:flex;align-items:center;justify-content:center;text-align:center;border:6px dashed #D4FF3F"><div style="color:#D4FF3F;font-weight:900;font-size:52px;line-height:1.1;padding:60px">{txt}</div></div>
<img src="{U('marc_bottom.jpg')}" style="position:absolute;top:1000px;left:0;width:1080px;height:920px">{pill_div()}</div>"""
def pill_div(): return ""
F = {
 "1_ganxo": f"""<div style="position:relative;width:1080px;height:1920px"><img src="{U('marc_full.jpg')}" style="width:1080px;height:1920px">
<div style="position:absolute;inset:0 0 auto 0;height:560px;background:linear-gradient(180deg,#0B0F12 55%,rgba(11,15,18,0))"></div>
<div style="position:absolute;top:120px;left:60px;right:60px;font-weight:900;font-size:88px;line-height:.96;letter-spacing:-3px;text-transform:uppercase;color:#fff">Mal a fora <span style="color:#D4FF3F">del genoll quan corres?</span></div></div>""",
 "2_que_es": split("full_leg_crop.png", "Cintilla iliotibial", "Del maluc fins sota el genoll", "QUÈ ÉS"),
 "3_cintilla": split("itb_crop.png", "Cintilla iliotibial", "Molt dura i ancorada al fèmur", "QUÈ ÉS"),
 "4_tfl": split("tfl_crop.png", "Tensor de la fàscia lata", "Hi tira des de davant", "QUI HI TIRA"),
 "5_gmax": split("gmax_crop.png", "Gluti major", "Hi tira des de darrere", "QUI HI TIRA"),
 "6_genoll": placeholder("PLA 3 · FALTA<br><span style='font-size:38px;color:#E8ECEF'>Zoom a la cara de fora del genoll:<br>on fa mal</span>"),
 "7_gmed": split("gmed_crop.png", "Gluti mitjà", "Controla el maluc", "PER QUÈ"),
}
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        for n, h in F.items():
            t = D / "_t.html"; t.write_text(f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body>{h}</body></html>")
            await pg.goto(t.as_uri()); await pg.wait_for_timeout(300); await pg.screenshot(path=str(D / f"sb_{n}.png"))
        await b.close()
asyncio.run(main())
from PIL import Image
fs = sorted(D.glob("sb_*.png")); th = [Image.open(f).resize((300, 533)) for f in fs]
c = Image.new("RGB", (len(th) * 310, 533), "#222")
for k, i in enumerate(th): c.paste(i, (k * 310, 0))
c.save(D / "maquetacio_cintilla.jpg", quality=88)
