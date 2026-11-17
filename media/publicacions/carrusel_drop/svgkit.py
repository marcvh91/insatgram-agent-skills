"""Il·lustracions vectorials pròpies: sabatilla lateral i cama amb zones de tensió."""
import math

def cr(pts, closed=False):
    """Catmull-Rom -> path cúbic suau."""
    p = pts[:]
    if closed:
        p = [pts[-1]] + pts + pts[:2]
    else:
        p = [pts[0]] + pts + [pts[-1]]
    d = f"M{p[1][0]:.1f},{p[1][1]:.1f}"
    for i in range(1, len(p) - 2):
        x0, y0 = p[i - 1]; x1, y1 = p[i]; x2, y2 = p[i + 1]; x3, y3 = p[i + 2]
        c1 = (x1 + (x2 - x0) / 6, y1 + (y2 - y0) / 6)
        c2 = (x2 - (x3 - x1) / 6, y2 - (y3 - y1) / 6)
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {x2:.1f},{y2:.1f}"
    return d + (" Z" if closed else "")

L = 600
def spring(x):  # toe spring (forefoot rocker)
    return -44 * ((x - 430) / 170) ** 2 if x > 430 else 0

def shoe(uid, heel_mm, toe_mm, px=3.0, accent="#D4FF3F", upper=("#3B464E", "#12171B"), show_dims=False):
    H, T = heel_mm * px, toe_mm * px
    OS = 9  # outsole
    def base(x):  # midsole top (negative = up)
        return -(OS + H + (T - H) * x / 575) + spring(x)
    xs = [i * 25 for i in range(0, 25)]
    # --- outsole
    bot = [(x, spring(x)) for x in xs if 12 <= x <= 590]
    top_os = [(x, spring(x) - OS) for x in reversed(xs) if 12 <= x <= 590]
    outsole = cr([(4, -10)] + bot + [(597, spring(597) - 6)] + top_os + [(2, -OS - 6)], closed=True)
    # --- midsole
    ms_bot = [(x, spring(x) - OS) for x in xs if 8 <= x <= 588]
    ms_top = [(x, base(x)) for x in reversed(xs) if 6 <= x <= 575]
    midsole = cr([(0, -OS - 10)] + ms_bot + [(598, spring(598) - OS - 8), (594, base(590) + 4)] + ms_top + [(0, base(0) + 8)], closed=True)
    # sidewall sculpt line
    sculpt = cr([(30, (base(30) + spring(30) - OS) / 2 + 4), (200, (base(200) - OS) / 2 + 6), (380, (base(380) - OS) / 2 + 2), (560, (base(560) + spring(560) - OS) / 2)])
    # --- upper
    u = [(4, -55), (8, -105), (22, -140), (62, -165), (105, -140), (150, -160), (195, -178), (250, -150), (320, -120), (400, -88), (470, -62), (530, -42), (570, -26), (590, -10)]
    up_pts = [(x, base(min(x, 575)) + dy) for x, dy in u]
    upper_d = cr([(2, base(0))] + up_pts + [(586, base(575) + 2)] + [(x, base(x)) for x in range(560, 0, -40)], closed=True)
    heel_counter = cr([(2, base(0)), (6, base(6) - 70), (22, base(22) - 128), (70, base(70) - 120), (120, base(120) - 40), (150, base(150) - 2), (60, base(60) + 2)], closed=True)
    toe_cap = cr([(470, base(470)), (505, base(505) - 45), (560, base(560) - 34), (590, base(575) - 10), (586, base(575) + 2)], closed=True)
    stripe = cr([(120, base(120) - 12), (210, base(210) - 70), (330, base(330) - 92), (300, base(300) - 60), (190, base(190) - 22)], closed=True)
    laces = ""
    for i, x in enumerate(range(195, 345, 28)):
        y = base(x) - (160 - (x - 195) * 0.42)
        laces += f'<line x1="{x-12}" y1="{y-6}" x2="{x+14}" y2="{y+4}" stroke="#E8ECEF" stroke-width="7" stroke-linecap="round"/>'
        laces += f'<circle cx="{x-14}" cy="{y+16}" r="4" fill="#0B0F12" opacity=".6"/>'
    tab = f'<path d="M14,{base(14)-135} q-14,-30 6,-40 q14,4 12,36 z" fill="{accent}"/>'
    g = f"""
<defs>
 <linearGradient id="ms{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".7" stop-color="#E3E8EB"/><stop offset="1" stop-color="#B9C2C8"/></linearGradient>
 <linearGradient id="up{uid}" x1="0" y1="0" x2=".3" y2="1"><stop offset="0" stop-color="{upper[0]}"/><stop offset="1" stop-color="{upper[1]}"/></linearGradient>
 <linearGradient id="gl{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset=".45" stop-color="#fff" stop-opacity="0"/></linearGradient>
 <pattern id="mesh{uid}" width="9" height="9" patternUnits="userSpaceOnUse"><circle cx="4.5" cy="4.5" r="1.5" fill="#000" opacity=".35"/></pattern>
 <radialGradient id="sh{uid}"><stop offset="0" stop-color="#000" stop-opacity=".55"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient>
</defs>
<ellipse cx="300" cy="6" rx="320" ry="16" fill="url(#sh{uid})"/>
<path d="{upper_d}" fill="url(#up{uid})"/>
<path d="{upper_d}" fill="url(#mesh{uid})"/>
<path d="{upper_d}" fill="url(#gl{uid})"/>
<path d="{heel_counter}" fill="#0E1215" opacity=".85"/>
<path d="{toe_cap}" fill="#0E1215" opacity=".6"/>
<path d="{stripe}" fill="{accent}" opacity=".95"/>
{laces}{tab}
<path d="{midsole}" fill="url(#ms{uid})"/>
<path d="{sculpt}" fill="none" stroke="#9AA4AA" stroke-width="2.5" opacity=".7"/>
<path d="{outsole}" fill="#1B2024"/>
"""
    if show_dims:
        hb, tb = base(0), base(575)
        g += f"""
<g stroke="{accent}" stroke-width="4" fill="none">
 <line x1="-34" y1="{-OS}" x2="-34" y2="{hb}"/><line x1="-46" y1="{-OS}" x2="-22" y2="{-OS}"/><line x1="-46" y1="{hb}" x2="-22" y2="{hb}"/>
 <line x1="634" y1="{spring(575)-OS}" x2="634" y2="{tb}"/><line x1="622" y1="{spring(575)-OS}" x2="646" y2="{spring(575)-OS}"/><line x1="622" y1="{tb}" x2="646" y2="{tb}"/>
 <line x1="0" y1="{hb}" x2="600" y2="{hb}" stroke-dasharray="10 9" opacity=".7"/>
</g>"""
    return g, base

def shoe_svg(uid, heel_mm, toe_mm, w=880, show_dims=False, pad=(80, 330, 60, 40), px=3.0):
    g, base = shoe(uid, heel_mm, toe_mm, px=px, show_dims=show_dims)
    l, t, r, b = pad
    vb = f"{-l} {-t} {600 + l + r} {t + b}"
    h = w * (t + b) / (600 + l + r)
    return f'<svg width="{w}" height="{h:.0f}" viewBox="{vb}">{g}</svg>', base


def leg_panel(uid, heel_mm, toe_mm, focus, w=440):
    """Cama lateral estil raig X (mira a la dreta) amb sabatilla. focus: 'knee' o 'calf'."""
    sc = 0.6
    g_shoe, base = shoe(uid, heel_mm, toe_mm, px=3.2)
    AX, AY = 118 * sc, (base(118) - 70) * sc   # turmell en coords globals
    def P(pts): return [(AX + x, AY + y) for x, y in pts]
    leg = cr(P([(24, 10), (30, -60), (42, -160), (66, -268), (90, -306), (92, -330), (84, -372), (100, -470), (92, -560), (76, -660),
                (-56, -660), (-48, -560), (-40, -460), (-18, -360), (6, -300), (-12, -262), (-34, -200), (-28, -130), (-16, -70), (-14, -20), (-26, 12)]), closed=True)
    femur = cr(P([(18, -650), (30, -500), (46, -360)]))
    tibia = cr(P([(52, -290), (36, -160), (16, -20)]))
    fibula = cr(P([(30, -280), (14, -160), (-2, -30)]))
    hot = "#FF4D2E"; cold = "#3FA7FF"
    pat = AX + 86, AY - 322
    achil = cr(P([(-18, -150), (-16, -80), (-18, 0)]))
    calf_c = (AX - 18, AY - 200)
    if focus == "knee":
        hl = (f'<circle cx="{pat[0]}" cy="{pat[1]}" r="85" fill="url(#hot{uid})"/>'
              f'<ellipse cx="{pat[0]}" cy="{pat[1]}" rx="13" ry="22" fill="#FFE1D8"/>'
              f'<path d="{achil}" stroke="{cold}" stroke-width="9" fill="none" stroke-linecap="round" opacity=".7"/>')
    else:
        hl = (f'<ellipse cx="{calf_c[0]}" cy="{calf_c[1]}" rx="50" ry="95" fill="url(#hot{uid})"/>'
              f'<path d="{achil}" stroke="{hot}" stroke-width="14" fill="none" stroke-linecap="round"/>'
              f'<path d="{achil}" stroke="#FFE1D8" stroke-width="4" fill="none" stroke-linecap="round"/>'
              f'<ellipse cx="{pat[0]}" cy="{pat[1]}" rx="13" ry="22" fill="{cold}" opacity=".8"/>')
    top = AY - 700
    return f"""<svg width="{w}" height="{w*(-top+24)/430:.0f}" viewBox="-60 {top} 430 {-top+24}">
<defs>
 <linearGradient id="skin{uid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#1A2228" stop-opacity=".9"/><stop offset=".6" stop-color="#2F3A41" stop-opacity=".9"/><stop offset="1" stop-color="#1F282E" stop-opacity=".9"/></linearGradient>
 <radialGradient id="hot{uid}"><stop offset="0" stop-color="{hot}" stop-opacity=".95"/><stop offset=".5" stop-color="{hot}" stop-opacity=".45"/><stop offset="1" stop-color="{hot}" stop-opacity="0"/></radialGradient>
 <linearGradient id="fade{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0B0F12"/><stop offset="1" stop-color="#0B0F12" stop-opacity="0"/></linearGradient>
 <filter id="bl{uid}"><feGaussianBlur stdDeviation="2"/></filter>
</defs>
<path d="{leg}" fill="url(#skin{uid})" stroke="#5B6870" stroke-width="2.5"/>
<g stroke="#C9D3D8" stroke-linecap="round" fill="none" opacity=".55">
 <path d="{femur}" stroke-width="30"/><path d="{tibia}" stroke-width="24"/><path d="{fibula}" stroke-width="9"/>
</g>
<g stroke="#E8EEF1" stroke-linecap="round" fill="none" opacity=".35" filter="url(#bl{uid})">
 <path d="{femur}" stroke-width="12"/><path d="{tibia}" stroke-width="9"/>
</g>
{hl}
<g transform="scale({sc})">{g_shoe}</g>
<rect x="-60" y="{top}" width="430" height="160" fill="url(#fade{uid})"/>
</svg>"""
