"""Reel cintilla v2 · rodatge 26/11 (aire lliure). Talls amb zoom des del 4K, targetes 3D a pantalla completa,
paraules clau a dalt (sobre el cap) i crida amb contacte."""
import subprocess, pathlib
R = pathlib.Path(__file__).parent; S = pathlib.Path('/home/claude/cint/src'); W = pathlib.Path('/home/claude/cint/w'); W.mkdir(exist_ok=True)
OV = R / 'v2'; P3 = pathlib.Path('/home/claude/reel_cintilla_src/panels'); CTA = R.parent / 'reel_drop/v7/cta.png'
V = '-c:v libx264 -preset medium -crf 17 -pix_fmt yuv420p -r 30'.split(); A = '-c:a pcm_s16le -ar 48000 -ac 2'.split()
def ff(*a): subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', *map(str, a)], check=True)
def dur(f): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout)
def crop(z, cx, ht):
    """Retall des del 4K (2160×3840): zoom z, centre horitzontal cx (fracció), cap a ~22 % d'alçada."""
    w, h = 2160 / z, 3840 / z
    x0 = min(max(cx * 2160 - w / 2, 0), 2160 - w); y0 = min(max(ht * 3840 - 0.22 * h, 0), 3840 - h)
    return f"crop={w:.0f}:{h:.0f}:{x0:.0f}:{y0:.0f},scale=1080:1920:flags=lanczos,setsar=1"
def ovl(fc, last, ins, items, d):
    for png, a, b in items:
        k = len(ins) // 6 if False else None
    return fc, last
def talk(out, clip, s, e, z, cx, ht, pops=(), speed=1.0, mute=False, tail=0):
    d = round(e - s, 3); od = round(d / speed, 3)
    ins = ['-ss', s, '-t', d, '-i', S / f'IMG_{clip}.mov']
    fc = f"[0:v]{crop(z, cx, ht)},setpts=PTS/{speed}[v0]"; last = 'v0'
    for i, (png, a, b) in enumerate(pops):
        ins += ['-loop', 1, '-framerate', 30, '-t', od + tail, '-i', png if '/' in str(png) else OV / png]
        fo = f",fade=t=out:st={b-0.12}:d=0.12:alpha=1" if b < od else ""
        fi = f",fade=t=in:st={a}:d=0.12:alpha=1" if a > 0 else ""
        fc += f";[{i+1}:v]format=rgba{fi}{fo}[o{i}];[{last}][o{i}]overlay=0:0:shortest=0:eof_action=pass[v{i+1}]"; last = f'v{i+1}'
    if tail: fc += f";[{last}]tpad=stop_mode=clone:stop_duration={tail}[vt]"; last = 'vt'
    if mute: fc += f";anullsrc=r=48000:cl=stereo,atrim=0:{od + tail}[a]"
    else: fc += f";[0:a]atempo={speed},afade=t=in:d=0.03,afade=t=out:st={od-0.04}:d=0.04{f',apad=pad_dur={tail}' if tail else ''}[a]" if speed == 1.0 else f";[0:a]atempo={speed}[a]"
    ff(*ins, '-filter_complex', fc, '-map', f'[{last}]', '-map', '[a]', '-t', od + tail, *V, *A, out)
def splitseg(out, clip, s, e, lab, mp4, m0, cx, yt, wf, lows=()):
    """Pantalla partida: 3D a dalt i ell a baix, retallat del 4K i centrat."""
    d = round(e - s, 3); w = wf * 2160; h = w * 960 / 1080
    x0 = min(max(cx * 2160 - w / 2, 0), 2160 - w); y0 = min(max(yt * 3840, 0), 3840 - h)
    ins = ['-ss', s, '-t', d, '-i', S / f'IMG_{clip}.mov', '-stream_loop', -1, '-ss', m0, '-i', P3 / mp4, '-loop', 1, '-framerate', 30, '-t', d, '-i', OV / lab]
    fc = (f"[0:v]crop={w:.0f}:{h:.0f}:{x0:.0f}:{y0:.0f},scale=1080:960:flags=lanczos,setsar=1[bot];"
          f"[1:v]setpts=PTS-STARTPTS,fps=30,scale=1080:1000,crop=1080:960:0:20,setsar=1[top];[top][bot]vstack[st];[st][2:v]overlay=0:0[c0]"); last = 'c0'
    for i, (png, a, b) in enumerate(lows):
        ins += ['-loop', 1, '-framerate', 30, '-t', d, '-i', OV / png]
        fo = f",fade=t=out:st={b-0.12}:d=0.12:alpha=1" if b < d else ""
        fc += f";[{i+3}:v]format=rgba,fade=t=in:st={a}:d=0.15:alpha=1{fo}[l{i}];[{last}][l{i}]overlay=0:0[c{i+1}]"; last = f'c{i+1}'
    fc += f";[0:a]afade=t=in:d=0.03,afade=t=out:st={d-0.04}:d=0.04[a]"
    ff(*ins, '-filter_complex', fc, '-map', f'[{last}]', '-map', '[a]', '-t', d, *V, *A, out)
def split3(out, clip, s, e, lab, mp4, m0, cx, yt, wf, lows=()):
    """1/3 a dalt el 3D sencer (sense retallar, centrat sobre fons fosc) i 2/3 a baix ell (1080×1280 del 4K)."""
    d = round(e - s, 3); w = wf * 2160; h = w * 1280 / 1080
    if h > 3840: h = 3840; w = h * 1080 / 1280
    x0 = min(max(cx * 2160 - w / 2, 0), 2160 - w); y0 = min(max(yt * 3840, 0), 3840 - h)
    ins = ['-ss', s, '-t', d, '-i', S / f'IMG_{clip}.mov', '-stream_loop', -1, '-ss', m0, '-i', P3 / mp4, '-loop', 1, '-framerate', 30, '-t', d, '-i', OV / lab]
    fc = (f"[0:v]crop={w:.0f}:{h:.0f}:{x0:.0f}:{y0:.0f},scale=1080:1280:flags=lanczos,setsar=1[bot];"
          f"[1:v]setpts=PTS-STARTPTS,fps=30,scale=-2:640,pad=1080:640:(ow-iw)/2:0:color=0x0B0F12,setsar=1[top];[top][bot]vstack[st];[st][2:v]overlay=0:0[c0]"); last = 'c0'
    for i, (png, a, b) in enumerate(lows):
        ins += ['-loop', 1, '-framerate', 30, '-t', d, '-i', OV / png]
        fo = f",fade=t=out:st={b-0.12}:d=0.12:alpha=1" if b < d else ""
        fc += f";[{i+3}:v]format=rgba,fade=t=in:st={a}:d=0.15:alpha=1{fo}[l{i}];[{last}][l{i}]overlay=0:0[c{i+1}]"; last = f'c{i+1}'
    fc += f";[0:a]afade=t=in:d=0.03,afade=t=out:st={d-0.04}:d=0.04[a]"
    ff(*ins, '-filter_complex', fc, '-map', f'[{last}]', '-map', '[a]', '-t', d, *V, *A, out)
B = pathlib.Path('/home/claude/broll')
def broll(out, vclip, vs, d, aclip, a_s, z, cx, ht, pops=()):
    """Pla de recurs (vídeo d'un clip de suport) amb l'àudio d'un altre clip."""
    vsrc = B / f'IMG_{vclip}.mov' if (B / f'IMG_{vclip}.mov').exists() else S / f'IMG_{vclip}.mov'
    asrc = S / f'IMG_{aclip}.mov' if aclip else vsrc
    ins = ['-ss', vs, '-t', d, '-i', vsrc, '-ss', a_s if aclip else vs, '-t', d, '-i', asrc]
    fc = f"[0:v]scale=2160:3840:flags=lanczos,{crop(z, cx, ht)}[v0]"; last = 'v0'
    for i, (png, a, b) in enumerate(pops):
        ins += ['-loop', 1, '-framerate', 30, '-t', d, '-i', OV / png]
        fi = f",fade=t=in:st={a}:d=0.12:alpha=1" if a > 0 else ""
        fc += f";[{i+2}:v]format=rgba{fi}[o{i}];[{last}][o{i}]overlay=0:0[v{i+1}]"; last = f'v{i+1}'
    fc += f";[1:a]afade=t=in:d=0.03,afade=t=out:st={d-0.04}:d=0.04[a]"
    ff(*ins, '-filter_complex', fc, '-map', f'[{last}]', '-map', '[a]', '-t', d, *V, *A, out)
def silhouette(out, clip, s, d, audio_clip, a_s, a_d, pops):
    """Exercici a contrallum (S2/S3) amb la veu de la frase; si la veu és més curta, silenci al final."""
    ins = ['-ss', s, '-t', d, '-i', S / f'IMG_{clip}.mov', '-ss', a_s, '-t', a_d, '-i', S / f'IMG_{audio_clip}.mov']
    fc = f"[0:v]{crop(1.05, 0.5, 0.25)}[v0]"; last = 'v0'
    for i, (png, a, b) in enumerate(pops):
        ins += ['-loop', 1, '-framerate', 30, '-t', d, '-i', OV / png]
        fo = f",fade=t=out:st={b-0.12}:d=0.12:alpha=1" if b < d else ""
        fc += f";[{i+2}:v]format=rgba,fade=t=in:st={a}:d=0.12:alpha=1{fo}[o{i}];[{last}][o{i}]overlay=0:0[v{i+1}]"; last = f'v{i+1}'
    fc += f";[1:a]afade=t=in:d=0.03,afade=t=out:st={a_d-0.05}:d=0.05,apad=whole_dur={d}[a]"
    ff(*ins, '-filter_complex', fc, '-map', f'[{last}]', '-map', '[a]', '-t', d, *V, *A, out)
def card(out, clip, s, e, cardpng, mp4, m0, lows=()):
    """Àudio del clip, imatge = targeta 3D (fons + vídeo 3D a y=470) amb petita entrada en zoom."""
    d = round(e - s, 3)
    ins = ['-ss', s, '-t', d, '-i', S / f'IMG_{clip}.mov', '-loop', 1, '-framerate', 30, '-t', d, '-i', OV / cardpng, '-stream_loop', -1, '-ss', m0, '-i', P3 / mp4]
    fc = "[2:v]setpts=PTS-STARTPTS,fps=30,scale=1350:1250,crop=1080:1250:135:0[m];[1:v][m]overlay=0:330:shortest=1[c0]"; last = 'c0'
    for i, (png, a, b) in enumerate(lows):
        ins += ['-loop', 1, '-framerate', 30, '-t', d, '-i', OV / png]
        fo = f",fade=t=out:st={b-0.12}:d=0.12:alpha=1" if b < d else ""
        fc += f";[{i+3}:v]format=rgba,fade=t=in:st={a}:d=0.15:alpha=1{fo}[l{i}];[{last}][l{i}]overlay=0:0[c{i+1}]"; last = f'c{i+1}'
    fc += f";[{last}]zoompan=z='if(lt(on,8),1.07-0.07*on/8,1)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,setsar=1[v]"
    fc += f";[0:a]afade=t=in:d=0.03,afade=t=out:st={d-0.04}:d=0.04[a]"
    ff(*ins, '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-t', d, *V, *A, out)
seq = []
def add(f): seq.append(f); return f
# 1 · Ganxo: arriba corrent (velocitat real, retallat) i parla; títol des del primer fotograma
broll(add(W/'00.mov'), 4220, 3.75, 0.8, None, 0, 1.0, 0.5, 0.2)
talk(add(W/'01.mov'), 4197, 4.00, 5.25, 1.2, 0.76, 0.41)
talk(add(W/'02.mov'), 4195, 6.66, 11.05, 1.15, 0.5, 0.17, [('t_hook.png', 0, 2.75), ('pop_cintilla.png', 2.75, 99)])
# 2 · Què és (a dalt 3D, a baix ell)
talk(add(W/'03.mov'), 4198, 0.85, 2.30, 1.3, 0.45, 0.21)
split3(add(W/'04.mov'), 4198, 2.30, 7.35, 's2_cint.png', 'p2_cintilla.mp4', 1.0, 0.45, 0.15, 0.92)
# 3 · Qui hi tira
talk(add(W/'05.mov'), 4200, 0.35, 2.25, 1.7, 0.47, 0.40)
split3(add(W/'06.mov'), 4200, 2.25, 4.70, 's2_tfl.png', 'p4_tfl_src.mp4', 0.0, 0.47, 0.36, 0.76)
split3(add(W/'07.mov'), 4200, 4.70, 6.75, 's2_gmax.png', 'p5_gmax.mp4', 1.5, 0.47, 0.36, 0.76)
# 4 · On fa mal i per què
talk(add(W/'08.mov'), 4206, 1.00, 2.85, 1.0, 0.5, 0.0)
split3(add(W/'09.mov'), 4206, 2.85, 12.25, 's2_genoll.png', 'p3_genoll.mp4', 0.5, 0.5, 0.12, 1.0, [('l2_friccio.png', 2.6, 5.4), ('l2_compr.png', 5.6, 99)])
# 5 · Per què apareix
talk(add(W/'10.mov'), 4211, 1.20, 2.95, 1.35, 0.5, 0.32, [('pop_carrega.png', 0.4, 99)])
broll(add(W/'10b.mov'), 4225, 3.90, 1.75, 4211, 2.95, 1.3, 0.5, 0.30, [('pop_carrega.png', 0, 99)])
talk(add(W/'10c.mov'), 4211, 4.70, 6.15, 1.35, 0.5, 0.32, [('pop_carrega.png', 0, 99)])
split3(add(W/'11.mov'), 4211, 6.15, 9.40, 's2_gmed.png', 'p6_gmed.mp4', 0.5, 0.5, 0.13, 0.92)
# 6 · Què fer: estirar ✗ (ell) → enfortir ✓ i ajustar la càrrega (exercici a contrallum)
talk(add(W/'12.mov'), 4212, 1.50, 5.40, 1.3, 0.48, 0.33, [('pop_estirar.png', 1.35, 99)])
silhouette(add(W/'13.mov'), 4152, 2.80, 4.6, 4212, 5.40, 3.0, [('pop_enfortir.png', 0.1, 2.5), ('pop_carrega2.png', 2.5, 99)])
# 7 · Crida
talk(add(W/'14.mov'), 4214, 0.00, 7.95, 1.6, 0.52, 0.34, [(CTA, 6.0, 99)], tail=1.5)
(W/'l.txt').write_text(''.join(f"file '{x}'\n" for x in seq))
ff('-f', 'concat', '-safe', 0, '-i', W/'l.txt', '-c', 'copy', W/'join.mov')
# whoosh a l'entrada/sortida de cada targeta 3D
cuts = []; t = 0
for f in seq:
    d = dur(f); n = f.name
    if n in ('01.mov', '04.mov', '06.mov', '09.mov', '11.mov', '13.mov', '14.mov'): cuts.append(t)
    t += d
n = len(cuts)
fc = f"anoisesrc=c=pink:d=0.4:a=0.5,highpass=f=900,lowpass=f=5500,afade=t=in:d=0.15,afade=t=out:st=0.15:d=0.25,volume=0.08,aformat=sample_rates=48000:channel_layouts=stereo,asplit={n}" + ''.join(f'[w{i}]' for i in range(n)) + ';'
fc += ''.join(f"[w{i}]adelay={max(0,int((c-0.15)*1000))}|{max(0,int((c-0.15)*1000))}[wd{i}];" for i, c in enumerate(cuts))
fc += "[0:a]highpass=f=100,afftdn=nf=-25,acompressor=threshold=-20dB:ratio=3:attack=5:release=100[voz];[voz]" + ''.join(f'[wd{i}]' for i in range(n)) + f"amix=inputs={n+1}:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11[aout]"
ff('-i', W/'join.mov', '-filter_complex', fc, '-map', '0:v', '-map', '[aout]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', R/'reel_cintilla_v2.mp4')
print('durada', dur(R/'reel_cintilla_v2.mp4'))
