"""Reel drop v2: overlays per a l'estructura de 5 escenes + esbós (storyboard) amb foto provisional."""
import asyncio, pathlib, sys
from PIL import Image
D = pathlib.Path(__file__).parent
sys.path.insert(0, str(D.parent / "carrusel_drop"))
from svgkit import shoe_svg, leg_panel
from playwright.async_api import async_playwright

FOT = D.parent.parent / "fotos_standard"
OUT = D / "v2"; OUT.mkdir(exist_ok=True)
CSS = """*{margin:0;padding:0;box-sizing:border-box}body{font-family:Inter,sans-serif;color:#E8ECEF;overflow:hidden;background:transparent}
b{color:#D4FF3F}sup{color:#D4FF3F;font-size:24px;font-weight:800}
h2{font-weight:900;font-size:70px;line-height:1;letter-spacing:-2px;text-transform:uppercase;color:#fff}h2 em{font-style:normal;color:#D4FF3F}"""
def ref(*n): return '<sup>' + ''.join(f'[{i}]' for i in n) + '</sup>'

# ---- Escena 1: overlay títol (visible des del fotograma 0)
S1 = """<div style="width:1080px;height:1920px;position:relative">
<div style="position:absolute;top:0;left:0;right:0;height:950px;background:linear-gradient(180deg,rgba(11,15,18,.95) 0%,rgba(11,15,18,.85) 60%,rgba(11,15,18,0) 100%)"></div>
<div style="position:absolute;top:230px;left:70px;right:70px">
<div style="font-weight:900;font-size:100px;line-height:.98;letter-spacing:-3px;text-transform:uppercase;color:#fff">Molèsties al genoll <span style="color:#D4FF3F">quan corres?</span></div>
<div style="display:inline-block;background:#D4FF3F;color:#0B0F12;font-weight:900;font-size:44px;padding:16px 28px;border-radius:14px;margin-top:34px">👟 I el calçat, l'has mirat mai?</div></div></div>"""

# ---- Escena 3: pantalla completa, 3 sabatilles
rows = ""
for uid, h, t, lab, sub in [("z", 26, 26, "0 mm", "Pla · «zero drop»"), ("m", 29, 24, "4–6 mm", "Baix"), ("x", 34, 23, "8–12 mm", "Alt · el més habitual")]:
    rows += (f'<div style="margin-top:46px"><div style="font-size:64px;font-weight:900;color:#D4FF3F">{lab} <span style="font-size:36px;color:#B9C1C6;font-weight:700">{sub}</span></div>'
             f'<div style="margin-left:-40px">{shoe_svg(uid, h, t, w=1020, dims=True, pad=(190, 330, 330, 55), px=3.6)}</div></div>')
S3 = f"""<div style="width:1080px;height:1920px;background:#0B0F12;padding:170px 70px 0">
<h2 style="font-size:96px">De <em>0 a 12 mm</em></h2>{rows}</div>"""

# ---- Escena 4: Marc al mig, cama a cada costat (estat: 'alt' o 'baix' actiu)
def S4(active, top=1000, cw=340, lw=320):
    def card(side, title, txt, leg, on):
        op = 1 if on else .35
        bd = "#D4FF3F" if on else "#2A3238"
        x = "left:24px" if side == "L" else "right:24px"
        return (f'<div style="position:absolute;top:{top}px;{x};width:{cw}px;opacity:{op};background:rgba(11,15,18,.88);border:4px solid {bd};border-radius:26px;padding:20px 8px 18px;text-align:center">'
                f'<div style="font-size:34px;font-weight:900;letter-spacing:1px;color:#D4FF3F">{title}</div>{leg}'
                f'<div style="font-size:30px;font-weight:800;line-height:1.2;margin-top:6px;padding:0 10px">{txt}</div></div>')
    L = card("L", "DROP ALT", f"🔴 Ròtula<br>fins a +15 %{ref(1)}", leg_panel(f"a{active}{top}", 36, 22, "knee", w=lw), active in ("alt", "tots"))
    R = card("R", "DROP BAIX", f"🔴 Bessó i<br>Aquil·les{ref(2,3)}", leg_panel(f"b{active}{top}", 26, 26, "calf", w=lw), active in ("baix", "tots"))
    return f"""<div style="width:1080px;height:1920px;position:relative">{L}{R}
</div>"""

# ---- Escena 5: resum en un sol panell (meitat superior) + CTA final
items = [("Canvia a poc a poc", f"12 setmanes o més{ref(4)}"), ("No allarguis de cop", f"cap sortida &gt;10 % més llarga del normal{ref(8)}"), ("El drop no ho és tot", f"lesions prèvies, càrrega i maluc{ref(7)}")]
lis = "".join(f'<div style="display:flex;gap:26px;align-items:flex-start;margin-top:34px"><div style="width:66px;height:66px;border-radius:50%;background:#D4FF3F;color:#0B0F12;font-size:38px;font-weight:900;display:flex;align-items:center;justify-content:center;flex-shrink:0">{i+1}</div><div><div style="font-size:46px;font-weight:900">{a}</div><div style="font-size:34px;color:#B9C1C6;font-weight:600;margin-top:4px">{b}</div></div></div>' for i, (a, b) in enumerate(items))
S5 = f"""<div style="width:1080px;height:960px;background:#0B0F12;padding:90px 80px 0"><h2>Si vols <em>canviar</em></h2>{lis}</div>"""
CTA = (D / "panels" / "ov9_cta.png")

async def render():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        for name, html, size, transp in [("s1_titol", S1, (1080, 1920), True), ("s3_bambes", S3, (1080, 1920), False),
                                          ("s4_tensio", S4("tots"), (1080, 1920), True), ("s4_dalt", S4("tots", top=110, cw=290, lw=270), (1080, 1920), True), ("s4_baix_n40", S4("tots", top=1060, cw=300, lw=280), (1080, 1920), True),
                                          ]:
            await pg.set_viewport_size({"width": size[0], "height": size[1]})
            await pg.set_content(f"<html><head><style>{CSS}</style></head><body>{html}</body></html>"); await pg.wait_for_timeout(250)
            await pg.screenshot(path=str(OUT / f"{name}.png"), omit_background=transp)
        await b.close()
asyncio.run(render())

# ---- Esbós amb fotos provisionals
def full(photo, pos=.5):
    im = Image.open(FOT / photo).convert("RGB"); w, h = im.size; s = 1920 / h
    im = im.resize((int(w * s), 1920)); x = int((im.width - 1080) * pos); return im.crop((x, 0, x + 1080, 1920))
def half(photo, y=.18):
    im = Image.open(FOT / photo).convert("RGB"); w, h = im.size; im = im.resize((1080, int(h * 1080 / w)))
    y0 = int(im.height * y); return im.crop((0, y0, 1080, y0 + 960))
def ov(base, png):
    o = Image.open(png).convert("RGBA"); base = base.copy(); base.paste(o, (0, 0), o); return base
def split(top_png, photo):
    c = Image.new("RGB", (1080, 1920)); c.paste(Image.open(top_png).convert("RGB"), (0, 0)); c.paste(half(photo), (0, 960)); return c

frames = [
    ("1", ov(full("tonus_camilla_tauleta_somriu.jpg", .55), OUT / "s1_titol.png")),
    ("2", split(D / "panels" / "p2_drop.png", "tonus_camilla_tauleta_serios.jpg")),
    ("3", Image.open(OUT / "s3_bambes.png").convert("RGB")),
    ("4", ov(full("tonus_camilla_bracos_creuats.jpg", .5), OUT / "s4_tensio.png")),
    ("5", full("tonus_camilla_tauleta_somriu.jpg", .55)),
]
for n, im in frames: im.save(OUT / f"esbos_{n}.jpg", quality=85)
th = [im.resize((360, 640)) for _, im in frames]
sheet = Image.new("RGB", (360 * 5 + 40, 640), "#222")
for k, im in enumerate(th): sheet.paste(im, (k * 370, 0))
sheet.save(D / "esbos_reel_drop.jpg", quality=88)
