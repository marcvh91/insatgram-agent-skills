"""Il·lustracions vectorials pròpies (v3): sabatilla realista i cama anatòmica."""

def cr(pts, closed=False):
    """Catmull-Rom -> path cúbic suau."""
    p = ([pts[-1]] + pts + pts[:2]) if closed else ([pts[0]] + pts + [pts[-1]])
    d = f"M{p[1][0]:.1f},{p[1][1]:.1f}"
    for i in range(1, len(p) - 2):
        x0, y0 = p[i - 1]; x1, y1 = p[i]; x2, y2 = p[i + 1]; x3, y3 = p[i + 2]
        d += (f" C{x1 + (x2 - x0) / 6:.1f},{y1 + (y2 - y0) / 6:.1f}"
              f" {x2 - (x3 - x1) / 6:.1f},{y2 - (y3 - y1) / 6:.1f} {x2:.1f},{y2:.1f}")
    return d + (" Z" if closed else "")

LIME = "#D4FF3F"
HX, FX = 75, 430          # punts de mesura: taló i avantpeu (estàndard: ~12 % i ~75 % de la longitud)

def spring(x):            # toe spring
    return -46 * ((x - 440) / 160) ** 2 if x > 440 else 0
def bevel(x):             # bisell del taló
    return -16 * (1 - x / 45) ** 2 if x < 45 else 0

def geom(H, T):
    def stack(x):
        if x <= 95: return H
        if x >= 420:
            return T * (1 - 0.55 * ((x - 525) / 75) ** 2) if x > 525 else T
        t = (x - 95) / 325; t = t * t * (3 - 2 * t)
        return H + (T - H) * t
    def bot(x): return spring(x) + bevel(x)
    def top(x): return spring(x) - stack(x)
    return stack, bot, top

def shoe(uid, heel_mm, toe_mm, px=3.2, dims=False, accent=LIME):
    H, T = heel_mm * px, toe_mm * px
    stack, bot, top = geom(H, T)
    X = list(range(0, 601, 15))
    OS = 11
    # ---- sola (outsole) i mitja sola
    outsole = cr([(x, bot(x)) for x in X] + [(600, top(600) + 4)] + [(x, bot(x) - OS) for x in reversed(X)][:-1] + [(0, bot(0) - OS - 2)], closed=True)
    lugs = "".join(f'<rect x="{x}" y="{bot(x)-5:.1f}" width="9" height="5" rx="1.5" fill="#0A0D0F" transform="rotate({-(bot(x+5)-bot(x))*3:.1f} {x} {bot(x)})"/>' for x in range(26, 575, 22))
    ms = cr([(x, bot(x) - OS) for x in X][1:] + [(601, top(601) + 2)] + [(x, top(x)) for x in reversed(X)] + [(-2, bot(0) - OS - 4)], closed=True)
    sculpt1 = cr([(x, (bot(x) - OS) * .45 + top(x) * .55 + 4) for x in range(30, 560, 40)])
    sculpt2 = cr([(x, (bot(x) - OS) * .2 + top(x) * .8 + 2) for x in range(60, 420, 40)])
    heelpod = cr([(10, (bot(10) - OS + top(10)) / 2 + 6), (80, (bot(80) - OS + top(80)) / 2 + 2), (170, (bot(170) - OS + top(170)) / 2 + 8), (80, (bot(80) - OS + top(80)) / 2 + 9)], closed=True)
    # ---- empenya (upper)
    up = [(-6, -18), (-10, -60), (-6, -112), (8, -150), (34, -164), (70, -152), (108, -140), (142, -156), (168, -186), (190, -196),
          (214, -184), (270, -160), (340, -130), (410, -98), (470, -70), (528, -46), (568, -28), (594, -12), (602, 2)]
    up = [(x, top(min(max(x, 0), 600)) + h) for x, h in up]
    upper = cr(up + [(x, top(x) + 3) for x in range(585, -1, -45)], closed=True)
    collar = cr([(10, top(10) - 146), (40, top(40) - 158), (80, top(80) - 146), (118, top(118) - 136), (148, top(148) - 150), (120, top(120) - 120), (70, top(70) - 122), (30, top(30) - 128)], closed=True)
    counter = cr([(-6, top(0) - 14), (-9, top(0) - 70), (-4, top(0) - 120), (16, top(16) - 140), (60, top(60) - 132), (98, top(98) - 70), (128, top(128) - 10), (60, top(60) + 2)], closed=True)
    toecap = cr([(452, top(452) + 2), (474, top(474) - 46), (530, top(530) - 44), (572, top(572) - 26), (598, top(598) - 8), (600, top(600) + 2)], closed=True)
    vamp = cr([(180, top(180) + 2), (226, top(226) - 70), (300, top(300) - 116), (360, top(360) - 108), (330, top(330) - 64), (300, top(300) + 2)], closed=True)
    swoosh = cr([(110, top(110) - 22), (210, top(210) - 64), (330, top(330) - 92), (350, top(350) - 84), (230, top(230) - 40), (130, top(130) - 10)], closed=True)
    tongue = cr([(150, top(150) - 152), (172, top(172) - 192), (198, top(198) - 202), (212, top(212) - 186), (196, top(196) - 160)], closed=True)
    # cordons i ullets
    def uy(x):
        for (x0, y0), (x1, y1) in zip(up, up[1:]):
            if x0 <= x <= x1: return y0 + (y1 - y0) * (x - x0) / (x1 - x0)
        return up[-1][1]
    eyes = [(x, uy(x) + 16) for x in range(208, 356, 26)]
    lacepanel = cr([(eyes[0][0]-26, eyes[0][1]-10)] + [(x+4, y-12) for x, y in eyes] + [(eyes[-1][0]+30, eyes[-1][1]-4), (eyes[-1][0]+26, eyes[-1][1]+22)] + [(x-6, y+24) for x, y in reversed(eyes)] + [(eyes[0][0]-30, eyes[0][1]+20)], closed=True)
    laces = ""
    for i, (x, y) in enumerate(eyes):
        laces += f'<circle cx="{x-10:.1f}" cy="{y+12:.1f}" r="5.5" fill="#0A0D0F" stroke="#5A666E" stroke-width="1.5"/>'
        laces += f'<path d="M{x-10:.1f},{y+12:.1f} L{x+16:.1f},{y-4:.1f}" stroke="#F4F7F8" stroke-width="7" fill="none" stroke-linecap="round"/>'
        laces += f'<path d="M{x-10:.1f},{y+12:.1f} L{x+16:.1f},{y-4:.1f}" stroke="#B8C2C8" stroke-width="2" fill="none" stroke-linecap="round" transform="translate(0,2)"/>'
    stitch = (f'<path d="{cr([(x, top(x) - 8) for x in range(20, 590, 30)])}" stroke="#7D8990" stroke-width="1.6" stroke-dasharray="5 5" fill="none"/>'
              f'<path d="{cr([(452+4, top(456) - 6), (476, top(476) - 40), (530, top(530) - 38), (570, top(570) - 22)])}" stroke="#7D8990" stroke-width="1.6" stroke-dasharray="5 5" fill="none"/>')
    tab = f'<path d="M6,{top(6)-140:.1f} C-6,{top(6)-176:.1f} 20,{top(6)-190:.1f} 30,{top(30)-160:.1f} Z" fill="{accent}"/>'
    g = f"""<defs>
 <linearGradient id="ms{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset=".55" stop-color="#EEF2F4"/><stop offset="1" stop-color="#BCC5CB"/></linearGradient>
 <linearGradient id="up{uid}" x1="0" y1="0" x2=".25" y2="1"><stop offset="0" stop-color="#4A565E"/><stop offset=".55" stop-color="#2A333A"/><stop offset="1" stop-color="#151B1F"/></linearGradient>
 <radialGradient id="hl{uid}" cx=".55" cy=".25" r=".6"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
 <linearGradient id="ac{uid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#A9CC1F"/><stop offset=".6" stop-color="{accent}"/><stop offset="1" stop-color="#EEFF9A"/></linearGradient>
 <pattern id="mesh{uid}" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(20)"><rect width="8" height="8" fill="none"/><circle cx="4" cy="4" r="1.6" fill="#000" opacity=".38"/></pattern>
 <filter id="soft{uid}" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="9"/></filter>
 <filter id="soft2{uid}" x="-10%" y="-50%" width="120%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>
</defs>
<ellipse cx="300" cy="4" rx="320" ry="14" fill="#000" opacity=".7" filter="url(#soft{uid})"/>
<path d="{upper}" fill="url(#up{uid})"/>
<path d="{upper}" fill="url(#mesh{uid})"/>
<path d="{upper}" fill="url(#hl{uid})"/>
<path d="{collar}" fill="#0F1417"/>
<path d="{tongue}" fill="#3A454C"/>
<path d="{vamp}" fill="#1C2328" opacity=".75"/>
<path d="{counter}" fill="#12171A"/><path d="{counter}" fill="url(#hl{uid})"/>
<path d="{toecap}" fill="#1A2126"/>
<path d="{swoosh}" fill="url(#ac{uid})"/>
<path d="{lacepanel}" fill="#222A30"/>{stitch}{laces}{tab}
<path d="M0,{top(0)+2:.1f} L600,{top(600)+2:.1f}" stroke="#000" stroke-width="10" opacity=".5" filter="url(#soft2{uid})"/>
<path d="{ms}" fill="url(#ms{uid})"/>
<path d="{heelpod}" fill="{accent}" opacity=".9"/>
<path d="{sculpt1}" stroke="#A3ADB3" stroke-width="2.5" fill="none" opacity=".8"/>
<path d="{sculpt2}" stroke="#C6CED3" stroke-width="2" fill="none" opacity=".7"/>
<path d="{outsole}" fill="#1E2428"/>{lugs}
"""
    if dims:
        th, tt = top(HX), top(FX)
        def bar(x, y0, y1, lab, anchor):
            tw = 112; tx = x - 24 - tw if anchor == "end" else x + 24; ty = y1 / 2 - 22
            return (f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1:.1f}" stroke="{accent}" stroke-width="5"/>'
                    f'<line x1="{x-14}" y1="{y0}" x2="{x+14}" y2="{y0}" stroke="{accent}" stroke-width="5"/>'
                    f'<line x1="{x-14}" y1="{y1:.1f}" x2="{x+14}" y2="{y1:.1f}" stroke="{accent}" stroke-width="5"/>'
                    f'<rect x="{tx}" y="{ty:.1f}" width="{tw}" height="44" rx="10" fill="{accent}"/>'
                    f'<text x="{tx+tw/2}" y="{ty+31:.1f}" text-anchor="middle" fill="#0B0F12" font-size="26" font-weight="900" font-family="Inter">{lab}</text>')
        g += f"""
<line x1="-90" y1="0" x2="690" y2="0" stroke="#8A9399" stroke-width="3"/>
<text x="-90" y="-12" text-anchor="start" fill="#8A9399" font-size="30" font-weight="900" font-family="Inter">0</text>
<line x1="{HX}" y1="{th:.1f}" x2="{FX+40}" y2="{th:.1f}" stroke="{accent}" stroke-width="3" stroke-dasharray="10 8" opacity=".9"/>
<line x1="{FX+40}" y1="{th:.1f}" x2="{FX+40}" y2="{tt:.1f}" stroke="#FF4D2E" stroke-width="8"/>
<rect x="{FX+56}" y="{(th+tt)/2-62:.1f}" width="170" height="44" rx="10" fill="#FF4D2E"/>
<text x="{FX+141}" y="{(th+tt)/2-31:.1f}" text-anchor="middle" fill="#fff" font-size="26" font-weight="900" font-family="Inter">drop {heel_mm-toe_mm} mm</text>
{bar(HX, 0, th, f"{heel_mm} mm", "end")}{bar(FX, 0, tt, f"{toe_mm} mm", "start")}"""
    return g, top

def shoe_svg(uid, heel_mm, toe_mm, w=880, dims=False, pad=(110, 340, 110, 30), px=3.2):
    g, _ = shoe(uid, heel_mm, toe_mm, px=px, dims=dims)
    l, t, r, b = pad
    return f'<svg width="{w}" height="{w * (t + b) / (600 + l + r):.0f}" viewBox="{-l} {-t} {600 + l + r} {t + b}">{g}</svg>'


def leg_panel(uid, heel_mm, toe_mm, focus, w=440):
    """Cama anatòmica lateral (mira a la dreta). focus: 'knee' o 'calf'."""
    sc = 0.62
    g_shoe, top = shoe(uid, heel_mm, toe_mm, px=3.2)
    AX, AY = 135 * sc, (top(135) - 120) * sc          # turmell
    k = 1.25
    def P(pts): return [(AX + x * k, AY + y * k) for x, y in pts]
    skin = cr(P([(26, 30), (30, -40), (36, -110), (46, -190), (58, -250), (70, -285), (86, -306), (95, -332), (92, -362), (100, -410),
                 (106, -470), (100, -540), (92, -600), (-52, -600), (-46, -540), (-38, -462), (-24, -392), (-6, -334), (-16, -294), (-38, -238),
                 (-42, -184), (-32, -126), (-20, -74), (-17, -30), (-28, 6), (-24, 34)]), closed=True)
    quad = cr(P([(40, -600), (96, -520), (100, -440), (90, -378), (70, -372), (54, -430), (26, -520), (14, -600)]), closed=True)
    hams = cr(P([(-44, -600), (-6, -600), (-2, -470), (-6, -380), (-22, -380), (-36, -470)]), closed=True)
    gastro = cr(P([(-6, -320), (-34, -248), (-38, -186), (-26, -132), (-14, -112), (-2, -150), (6, -230), (4, -300)]), closed=True)
    soleus = cr(P([(-26, -200), (-28, -150), (-18, -96), (-8, -110), (-6, -170)]), closed=True)
    tib_ant = cr(P([(44, -250), (34, -150), (28, -60), (20, -60), (24, -150), (34, -250)]), closed=True)
    femur = cr(P([(24, -600), (34, -470), (50, -350)])); tibia = cr(P([(54, -296), (40, -170), (18, -10)]))
    pt = cr(P([(84, -312), (70, -282)])); achil = cr(P([(-16, -118), (-16, -60), (-20, 6)]))
    pat = (AX + 92 * k, AY - 334 * k)
    HOT, COLD = "#FF4D2E", "#3FA7FF"
    def lab(x, y, tx, ty, txt, anchor="start"):
        return (f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{tx:.1f}" y2="{ty:.1f}" stroke="#E8ECEF" stroke-width="2"/><circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#fff"/>'
                f'<text x="{tx + (6 if anchor=="start" else -6):.1f}" y="{ty+8:.1f}" text-anchor="{anchor}" fill="#fff" font-size="24" font-weight="800" font-family="Inter">{txt}</text>')
    if focus == "knee":
        quad_f, gas_f, sol_f = f"url(#hm{uid})", "#46525A", "#3E4950"
        hl = (f'<circle cx="{pat[0]:.1f}" cy="{pat[1]:.1f}" r="80" fill="url(#glow{uid})"/>'
              f'<path d="{pt}" stroke="{HOT}" stroke-width="13" stroke-linecap="round"/>'
              f'<ellipse cx="{pat[0]:.1f}" cy="{pat[1]:.1f}" rx="15" ry="25" fill="#FFD9CE" stroke="{HOT}" stroke-width="4" transform="rotate(-12 {pat[0]:.1f} {pat[1]:.1f})"/>'
              f'<path d="{achil}" stroke="{COLD}" stroke-width="10" stroke-linecap="round" opacity=".85"/>')
        labels = lab(pat[0] + 16, pat[1] - 4, pat[0] + 70, pat[1] - 70, "Ròtula") + lab(AX + 84 * k, AY - 430 * k, AX + 150 * k, AY - 440 * k, "Quàdriceps") + lab(AX - 18 * k, AY - 60 * k, AX - 70 * k, AY - 140 * k, "Aquil·les", "end")
    else:
        quad_f, gas_f, sol_f = "#46525A", f"url(#hm{uid})", f"url(#hm{uid})"
        gc = (AX - 18 * k, AY - 200 * k)
        hl = (f'<ellipse cx="{gc[0]:.1f}" cy="{gc[1]:.1f}" rx="70" ry="120" fill="url(#glow{uid})"/>'
              f'<path d="{achil}" stroke="{HOT}" stroke-width="14" stroke-linecap="round"/><path d="{achil}" stroke="#FFD9CE" stroke-width="4" stroke-linecap="round"/>'
              f'<ellipse cx="{pat[0]:.1f}" cy="{pat[1]:.1f}" rx="15" ry="25" fill="{COLD}" transform="rotate(-12 {pat[0]:.1f} {pat[1]:.1f})"/>'
              f'<path d="{pt}" stroke="{COLD}" stroke-width="10" stroke-linecap="round"/>')
        labels = lab(gc[0] - 20, gc[1], gc[0] - 70, gc[1] - 70, "Bessó", "end") + lab(AX - 18 * k, AY - 70 * k, AX - 80 * k, AY - 110 * k, "Aquil·les", "end") \
                 + lab(pat[0] + 16, pat[1] - 4, pat[0] + 70, pat[1] - 70, "Ròtula")
    topy = AY - 540 * k
    vb_w = 580
    return f"""<svg width="{w}" height="{w * (-topy + 20) / vb_w:.0f}" viewBox="-150 {topy:.1f} {vb_w} {-topy + 20:.1f}">
<defs>
 <linearGradient id="sk{uid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#1E262C"/><stop offset=".6" stop-color="#303B42"/><stop offset="1" stop-color="#222B31"/></linearGradient>
 <linearGradient id="hm{uid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FF7A5C"/><stop offset="1" stop-color="#C92A12"/></linearGradient>
 <radialGradient id="glow{uid}"><stop offset="0" stop-color="{HOT}" stop-opacity=".75"/><stop offset=".6" stop-color="{HOT}" stop-opacity=".25"/><stop offset="1" stop-color="{HOT}" stop-opacity="0"/></radialGradient>
 <linearGradient id="fd{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0B0F12"/><stop offset="1" stop-color="#0B0F12" stop-opacity="0"/></linearGradient>
 <pattern id="fib{uid}" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(-75)"><line x1="0" y1="0" x2="0" y2="7" stroke="#000" stroke-width="1.4" opacity=".25"/></pattern>
</defs>
<path d="{skin}" fill="url(#sk{uid})" stroke="#66737B" stroke-width="2.5"/>
<g stroke="#D7DFE3" stroke-linecap="round" fill="none" opacity=".22"><path d="{femur}" stroke-width="30"/><path d="{tibia}" stroke-width="24"/></g>
<path d="{hams}" fill="#3A454C"/><path d="{hams}" fill="url(#fib{uid})"/>
<path d="{quad}" fill="{quad_f}"/><path d="{quad}" fill="url(#fib{uid})"/>
<path d="{tib_ant}" fill="#3A454C"/>
<path d="{gastro}" fill="{gas_f}"/><path d="{gastro}" fill="url(#fib{uid})"/>
<path d="{soleus}" fill="{sol_f}" opacity=".85"/>
<path d="{pt}" stroke="#C9D2D7" stroke-width="10" stroke-linecap="round"/>
<path d="{achil}" stroke="#C9D2D7" stroke-width="10" stroke-linecap="round"/>
{hl}
<g transform="scale({sc})">{g_shoe}</g>
{labels}
<rect x="-150" y="{topy:.1f}" width="{vb_w}" height="120" fill="url(#fd{uid})"/>
</svg>"""
