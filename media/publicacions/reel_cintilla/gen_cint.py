"""Reel cintilla (rodatge 26/11, a l'aire lliure): títol, targetes 3D, paraules clau i crida. Estil Foto a sang."""
import asyncio, pathlib
from playwright.async_api import async_playwright
OUT = pathlib.Path(__file__).parent / "v2"; OUT.mkdir(exist_ok=True)
CSS = "*{margin:0;padding:0;box-sizing:border-box}body{font-family:Inter,sans-serif;background:transparent;color:#E8ECEF}sup{color:#D4FF3F;font-size:.5em;font-weight:800}"
def band(h): return f'<div style="position:absolute;left:0;right:0;top:0;height:{h}px;background:linear-gradient(180deg,rgba(11,15,18,.9) 0%,rgba(11,15,18,.8) 60%,rgba(11,15,18,0) 100%)"></div>'
def frame(inner): return f'<div style="width:1080px;height:1920px;position:relative">{inner}</div>'
def title():
    return frame(band(400) + '<div style="position:absolute;top:64px;left:50px;right:50px;text-align:center;font-weight:900;font-size:62px;line-height:1.02;letter-spacing:-2px;text-transform:uppercase;color:#fff">Mal a la cara externa<br>del genoll <span style="color:#D4FF3F">quan corres?</span></div>')
def pop(big, sub="", ok=None):
    mark = {True: '<span style="color:#0B0F12">✓ </span>', False: '<span style="color:#0B0F12">✗ </span>', None: ''}[ok]
    s = f'<div style="margin-top:14px;font-weight:800;font-size:38px;color:#fff;letter-spacing:-.5px;text-shadow:0 2px 12px rgba(0,0,0,.6)">{sub}</div>' if sub else ""
    return frame(band(340) + f'<div style="position:absolute;top:66px;left:30px;right:30px;text-align:center"><span style="display:inline-block;background:#D4FF3F;color:#0B0F12;font-weight:900;font-size:60px;letter-spacing:-2px;padding:10px 28px;border-radius:20px;text-transform:uppercase;transform:rotate(-1.5deg)">{mark}{big}</span>{s}</div>')
def card(name, sub):
    """Fons de la targeta 3D: el vídeo 3D (1080×1000) va a y=470."""
    return frame(f'''<div style="position:absolute;inset:0;background:#0B0F12"></div>
<div style="position:absolute;top:150px;left:60px;right:60px;text-align:center">
<div style="font-weight:900;font-size:66px;letter-spacing:-2px;line-height:1;color:#D4FF3F;text-transform:uppercase">{name}</div>
<div style="margin-top:18px;font-weight:700;font-size:40px;color:#fff">{sub}</div></div>''')
def low(big, sub, ok):
    """Text a sota del 3D, en una targeta (no hi ha persona)."""
    col = "#D4FF3F" if ok else "#FF6B5B"; mark = "✓" if ok else "✗"
    return frame(f'''<div style="position:absolute;top:{1500 if ok else 1500}px;left:70px;right:70px;border:4px solid {col};border-radius:24px;padding:22px 28px;background:rgba(11,15,18,.92)">
<div style="font-weight:900;font-size:50px;letter-spacing:-1px;color:{col};text-transform:uppercase">{mark} {big}</div>
<div style="margin-top:8px;font-weight:700;font-size:36px;color:#fff">{sub}</div></div>''')
ITEMS = {
 "t_hook": title(),
 "pop_cintilla": pop("La cintilla?", "Cintilla iliotibial"),
 "card_cint": card("Cintilla iliotibial", "Del maluc fins a sota del genoll<sup>[1]</sup>"),
 "card_tfl": card("Tensor de la fàscia lata", "Hi tira per davant<sup>[1]</sup>"),
 "card_gmax": card("Gluti major", "Hi tira per darrere<sup>[1]</sup>"),
 "card_genoll": card("On fa mal", "La cara externa del genoll"),
 "card_gmed": card("Gluti mitjà", "Menys força en corredores amb cintilla<sup>[4]</sup>"),
 "low_friccio": low("Abans: fricció amb l'os", "Ja no és l'explicació principal<sup>[2]</sup>", False),
 "low_compr": low("Avui: compressió", "D'un teixit amb nervis que hi ha a sota<sup>[2][3]</sup>", True),
 "pop_carrega": pop("+ km o + intensitat", "Massa de pressa<sup>[2]</sup>"),
 "pop_estirar": pop("Estirar-la", "No l'allargarà: és massa rígida<sup>[1]</sup>", False),
 "pop_enfortir": pop("Enfortir el maluc", "El dolor baixa en 2–8 setmanes<sup>[5]</sup>", True),
}
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={"width": 1080, "height": 1920})
        for k, h in ITEMS.items():
            await pg.set_content(f"<html><head><meta charset=utf-8><style>{CSS}</style></head><body>{h}</body></html>"); await pg.wait_for_timeout(250)
            await pg.screenshot(path=str(OUT / f"{k}.png"), omit_background=not k.startswith("card"))
        await b.close()
asyncio.run(main())
