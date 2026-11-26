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
        fc += f";[{i+1}:v]format=rgba,fade=t=in:st={a}:d=0.12:alpha=1{fo}[o{i}];[{last}][o{i}]overlay=0:0:shortest=0:eof_action=pass[v{i+1}]"; last = f'v{i+1}'
    if tail: fc += f";[{last}]tpad=stop_mode=clone:stop_duration={tail}[vt]"; last = 'vt'
    if mute: fc += f";anullsrc=r=48000:cl=stereo,atrim=0:{od + tail}[a]"
    else: fc += f";[0:a]atempo={speed},afade=t=in:d=0.03,afade=t=out:st={od-0.04}:d=0.04{f',apad=pad_dur={tail}' if tail else ''}[a]" if speed == 1.0 else f";[0:a]atempo={speed}[a]"
    ff(*ins, '-filter_complex', fc, '-map', f'[{last}]', '-map', '[a]', '-t', od + tail, *V, *A, out)
def card(out, clip, s, e, cardpng, mp4, m0, lows=()):
    """Àudio del clip, imatge = targeta 3D (fons + vídeo 3D a y=470) amb petita entrada en zoom."""
    d = round(e - s, 3)
    ins = ['-ss', s, '-t', d, '-i', S / f'IMG_{clip}.mov', '-loop', 1, '-framerate', 30, '-t', d, '-i', OV / cardpng, '-stream_loop', -1, '-ss', m0, '-i', P3 / mp4]
    fc = "[2:v]setpts=PTS-STARTPTS,fps=30,scale=1080:1000[m];[1:v][m]overlay=0:470:shortest=1[c0]"; last = 'c0'
    for i, (png, a, b) in enumerate(lows):
        ins += ['-loop', 1, '-framerate', 30, '-t', d, '-i', OV / png]
        fo = f",fade=t=out:st={b-0.12}:d=0.12:alpha=1" if b < d else ""
        fc += f";[{i+3}:v]format=rgba,fade=t=in:st={a}:d=0.15:alpha=1{fo}[l{i}];[{last}][l{i}]overlay=0:0[c{i+1}]"; last = f'c{i+1}'
    fc += f";[{last}]zoompan=z='if(lt(on,8),1.07-0.07*on/8,1)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,setsar=1[v]"
    fc += f";[0:a]afade=t=in:d=0.03,afade=t=out:st={d-0.04}:d=0.04[a]"
    ff(*ins, '-filter_complex', fc, '-map', '[v]', '-map', '[a]', '-t', d, *V, *A, out)
seq = []
def add(f): seq.append(f); return f
# 1 · Ganxo: entra corrent (×3) i parla; títol des del primer fotograma
add(talk(W/'01.mov', 4195, 0.60, 6.66, 1.0, 0.5, 0.2, [('t_hook.png', 0, 99)], speed=3.0, mute=True) or W/'01.mov')
add(talk(W/'02.mov', 4195, 6.66, 11.05, 1.15, 0.5, 0.17, [('t_hook.png', 0, 2.75), ('pop_cintilla.png', 2.75, 99)]) or W/'02.mov')
# 2 · Què és
add(talk(W/'03.mov', 4198, 0.85, 2.30, 1.3, 0.45, 0.21) or W/'03.mov')
add(card(W/'04.mov', 4198, 2.30, 5.80, 'card_cint.png', 'p2_cintilla.mp4', 1.0) or W/'04.mov')
add(talk(W/'05.mov', 4198, 5.80, 7.35, 1.45, 0.45, 0.21) or W/'05.mov')
# 3 · Qui hi tira
add(talk(W/'06.mov', 4200, 0.35, 2.25, 1.7, 0.47, 0.40) or W/'06.mov')
add(card(W/'07.mov', 4200, 2.25, 4.70, 'card_tfl.png', 'p4_tfl_src.mp4', 0.0) or W/'07.mov')
add(card(W/'08.mov', 4200, 4.70, 6.75, 'card_gmax.png', 'p5_gmax.mp4', 1.5) or W/'08.mov')
# 4 · On fa mal i per què (fricció ✗ → compressió ✓)
add(talk(W/'09.mov', 4206, 1.00, 2.85, 1.0, 0.5, 0.0) or W/'09.mov')
add(card(W/'10.mov', 4206, 2.85, 12.25, 'card_genoll.png', 'p3_genoll.mp4', 0.5, [('low_friccio.png', 2.6, 5.4), ('low_compr.png', 5.6, 99)]) or W/'10.mov')
# 5 · Per què apareix
add(talk(W/'11.mov', 4211, 1.20, 6.15, 1.35, 0.5, 0.32, [('pop_carrega.png', 1.6, 99)]) or W/'11.mov')
add(card(W/'12.mov', 4211, 6.15, 9.40, 'card_gmed.png', 'p6_gmed.mp4', 0.5) or W/'12.mov')
# 6 · Què fer
add(talk(W/'13.mov', 4212, 1.50, 5.30, 1.3, 0.48, 0.33, [('pop_estirar.png', 1.35, 99)]) or W/'13.mov')
add(talk(W/'14.mov', 4212, 5.30, 8.40, 1.45, 0.48, 0.31, [('pop_enfortir.png', 0.25, 99)]) or W/'14.mov')
# 7 · Crida
add(talk(W/'15.mov', 4214, 0.00, 7.95, 1.6, 0.52, 0.34, [(CTA, 6.0, 99)], tail=2.0) or W/'15.mov')
(W/'l.txt').write_text(''.join(f"file '{x}'\n" for x in seq))
ff('-f', 'concat', '-safe', 0, '-i', W/'l.txt', '-c', 'copy', W/'join.mov')
# whoosh a l'entrada/sortida de cada targeta 3D
cuts = []; t = 0
for f in seq:
    d = dur(f); n = f.name
    if n in ('04.mov', '07.mov', '10.mov', '12.mov') or n in ('05.mov', '09.mov', '11.mov', '13.mov'): cuts.append(t)
    t += d
n = len(cuts)
fc = f"anoisesrc=c=pink:d=0.4:a=0.5,highpass=f=900,lowpass=f=5500,afade=t=in:d=0.15,afade=t=out:st=0.15:d=0.25,volume=0.08,aformat=sample_rates=48000:channel_layouts=stereo,asplit={n}" + ''.join(f'[w{i}]' for i in range(n)) + ';'
fc += ''.join(f"[w{i}]adelay={max(0,int((c-0.15)*1000))}|{max(0,int((c-0.15)*1000))}[wd{i}];" for i, c in enumerate(cuts))
fc += "[0:a]highpass=f=100,afftdn=nf=-25,acompressor=threshold=-20dB:ratio=3:attack=5:release=100[voz];[voz]" + ''.join(f'[wd{i}]' for i in range(n)) + f"amix=inputs={n+1}:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11[aout]"
ff('-i', W/'join.mov', '-filter_complex', fc, '-map', '0:v', '-map', '[aout]', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', R/'reel_cintilla_v2.mp4')
print('durada', dur(R/'reel_cintilla_v2.mp4'))
