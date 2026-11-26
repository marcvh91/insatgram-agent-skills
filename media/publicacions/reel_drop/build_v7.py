"""Reel drop v7 · rodatge 26/11 (bamba La Sportiva). Essència del Reel original, més realitzat:
talls amb zoom alternat, títol a dalt, sabatilles que s'il·luminen, targetes de tensió sincronitzades i crida amb contacte."""
import subprocess, pathlib
R = pathlib.Path(__file__).parent; P = pathlib.Path('/home/claude/drop7'); W = P / 'w'; W.mkdir(exist_ok=True)
OV = R / 'v7'; PAD = 0.25
V = '-c:v libx264 -preset medium -crf 17 -pix_fmt yuv420p -r 30'.split(); A = '-c:a pcm_s16le -ar 48000 -ac 2'.split()
def ff(*a): subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', *map(str, a)], check=True)
def dur(f): return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout)
def zc(z, k): return f"scale=round(1080*{z}/2)*2:round(1920*{z}/2)*2,crop=1080:1920:(iw-1080)/2:(ih-1920)*{k},setsar=1"
def seg(out, clip, s, e, z=1.0, k=0.5, ovs=(), vf_extra='', tail=0):
    """ovs: [(png, t_in, t_out)] relatius al segment, amb fosa de 0,15 s."""
    d = round(e - s, 3); ins = ['-ss', s, '-t', d, '-i', P / f'p_{clip}.mov']
    fc = f"[0:v]{zc(z, k)}{vf_extra}[v0]"; last = 'v0'
    for i, (png, a, b) in enumerate(ovs):
        ins += ['-loop', 1, '-t', d, '-i', OV / png if '/' not in str(png) else png]
        fo = f",fade=t=out:st={b - 0.15}:d=0.15:alpha=1" if b < d else ""
        fc += f";[{i+1}:v]format=rgba,fade=t=in:st={a}:d=0.15:alpha=1{fo}[o{i}];[{last}][o{i}]overlay=0:0[v{i+1}]"; last = f'v{i+1}'
    if tail: fc += f";[{last}]tpad=stop_mode=clone:stop_duration={tail}[vt]"; last = 'vt'
    fc += f";[0:a]afade=t=in:d=0.03,afade=t=out:st={d-0.04}:d=0.04{f',apad=pad_dur={tail}' if tail else ''}[a]"
    ff(*ins, '-filter_complex', fc, '-map', f'[{last}]', '-map', '[a]', '-t', d + tail, *V, *A, out)
def concat(name, parts):
    (W / f'{name}.txt').write_text(''.join(f"file '{x}'\n" for x in parts)); ff('-f', 'concat', '-safe', 0, '-i', W / f'{name}.txt', '-c', 'copy', W / f'{name}.mov'); return W / f'{name}.mov'
T5 = R / 'v3' / 't5_canvi.png'
# Bloc A · ganxo, pont, què és
seg(W/'a1.mov', 4171, 0.55, 6.70, 1.0, 0.5, [('t_ganxo.png', 0, 99)])
seg(W/'a2.mov', 4174, 0.45, 4.10, 1.12, 0.3, [(T5, 0, 99)])
ff('-ss', 1.35, '-t', 4.60 + PAD, '-i', P/'p_4176.mov', '-loop', 1, '-i', R/'panels/p2_drop.png', '-filter_complex',
   "[0:v]scale=1080:1920,setsar=1,split[a][b];[a]crop=1080:1200:0:200,boxblur=30:3,eq=brightness=-0.15[bg];[b]scale=918:1632,crop=918:1200:0:120[fg];[bg][fg]overlay=81:0[vid];[1:v]crop=1080:720:0:0,setsar=1[top];[top][vid]vstack[out];[0:a]afade=t=in:d=0.03[a]",
   '-map', '[out]', '-map', '[a]', '-t', 4.60 + PAD, *V, *A, W/'a3.mov')
BA = concat('A', [W/'a1.mov', W/'a2.mov', W/'a3.mov'])
# Bloc B · els 3 tipus: veu de 4179 sobre la il·lustració, cada sabatilla s'il·lumina i s'hi apropa
IL = R / 'v2' / 's3_bambes.png'
def ill(out, s, e, mask, cy, z0, z1):
    d = round(e - s, 3); ins = ['-loop', 1, '-framerate', 30, '-t', d, '-i', IL, '-ss', s, '-t', d, '-i', P/'p_4179.mov']
    zp = f"scale=2160:3840,zoompan=z='{z0}+({z1}-{z0})*on/({d}*30)':x='iw/2-(iw/zoom/2)':y='max(0,min(ih-ih/zoom,{cy*2}-ih/zoom/2))':d=1:s=1080x1920:fps=30,setsar=1"
    fc = f"[0:v]{zp}[v0]"; last = 'v0'
    if mask is not None:
        ins += ['-loop', 1, '-t', d, '-i', OV / f'mask_{mask}.png']
        fc = f"[0:v]scale=1080:1920[il];[2:v]format=rgba,fade=t=in:d=0.2:alpha=1[m];[il][m]overlay=0:0,{zp}[v0]"
    fc += ";[1:a]afade=t=in:d=0.03,afade=t=out:st=%s:d=0.04[a]" % (d - 0.04)
    ff(*ins, '-filter_complex', fc, '-map', f'[{last}]', '-map', '[a]', '-t', d, *V, *A, out)
ill(W/'b1.mov', 0.85 - PAD, 4.00, None, 960, 1.0, 1.04)
ill(W/'b2.mov', 4.00, 8.15, 0, 530, 1.02, 1.07)
ill(W/'b3.mov', 8.15, 10.56, 1, 1005, 1.02, 1.07)
ill(W/'b4.mov', 10.56, 13.40 + PAD, 2, 1475, 1.02, 1.07)
BB = concat('B', [W/f'b{i}.mov' for i in range(1, 5)])
# Bloc C · on va la tensió (targetes sota les mans) + adaptació
seg(W/'c1.mov', 4181, 1.45 - PAD, 4.45, 1.10, 0.85, [('d5_alt.png', 0.45, 99)])
seg(W/'c2.mov', 4181, 6.45, 9.85, 1.18, 0.85, [('d5_alt.png', 0, 99), ('d5_baix.png', 0.15, 99)])
seg(W/'c3.mov', 4181, 16.35, 20.05, 1.0, 0.5)
seg(W/'c4.mov', 4183, 0.25, 4.60, 1.0, 0.5)
seg(W/'c5.mov', 4183, 4.60, 6.50 + PAD, 1.16, 0.2, [('pop_setm.png', 0.05, 99)])
BC = concat('C', [W/f'c{i}.mov' for i in range(1, 6)])
# Bloc D · crida a la consulta + contacte (congela l'últim fotograma per llegir-lo)
seg(W/'d1.mov', 4191, 1.95 - PAD, 9.00, 1.12, 0.45, [('cta.png', 4.90, 99)], tail=1.8)
BD = W/'d1.mov'
# Transicions entre blocs + whoosh suau
blocks = [BA, BB, BC, BD]; trans = ['slideleft', 'slideleft', 'fadeblack']
ds = [dur(b) for b in blocks]; ins = sum((['-i', b] for b in blocks), [])
fc = ''; lv, la = '0:v', '0:a'; acc = ds[0]; T = []
for i, t in enumerate(trans, 1):
    off = round(acc - PAD, 3); T.append(off)
    fc += f"[{lv}][{i}:v]xfade=transition={t}:duration={PAD}:offset={off}[xv{i}];[{la}][{i}:a]acrossfade=d={PAD}[xa{i}];"
    lv, la = f'xv{i}', f'xa{i}'; acc += ds[i] - PAD
n = len(T)
fc += f"anoisesrc=c=pink:d=0.45:a=0.5,highpass=f=900,lowpass=f=5500,afade=t=in:d=0.2,afade=t=out:st=0.2:d=0.25,volume=0.09,aformat=sample_rates=48000:channel_layouts=stereo,asplit={n}" + ''.join(f'[w{i}]' for i in range(n)) + ';'
fc += ''.join(f"[w{i}]adelay={int((t-0.12)*1000)}|{int((t-0.12)*1000)}[wd{i}];" for i, t in enumerate(T))
fc += f"[{la}]highpass=f=80,afftdn=nf=-25,acompressor=threshold=-20dB:ratio=3:attack=5:release=100[voz];[voz]" + ''.join(f'[wd{i}]' for i in range(n)) + f"amix=inputs={n+1}:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11[aout]"
ff(*ins, '-filter_complex', fc, '-map', f'[{lv}]', '-map', '[aout]', *V, '-c:a', 'aac', '-b:a', '192k', '-ar', 48000, R/'reel_drop_v7.mp4')
print('durada', dur(R/'reel_drop_v7.mp4'), 'transicions', T)
# Portada: fotograma somrient amb la bamba, reduït un 10 % i baixat perquè el títol quedi dins del retall de la quadrícula
ff('-ss', 6.3, '-i', P/'p_4171.mov', '-i', OV/'t_cover.png', '-frames:v', 1, '-filter_complex',
   "[0:v]split[a][b];[a]scale=1080:1920,boxblur=40:4[bg];[b]scale=972:1728[fg];[bg][fg]overlay=54:192[c];[c][1:v]overlay=0:0", '-q:v', 2, R/'v7'/'portada_v7.jpg')
