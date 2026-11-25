"""Reel drop · versió B dinàmica (25/11). Talls amb zoom, plans de recurs, paraules clau i transicions."""
import subprocess, pathlib
R = pathlib.Path(__file__).parent; S = pathlib.Path('/home/claude/reel_drop_src'); N = pathlib.Path('/home/claude/drop_new')
W = N / 'b'; W.mkdir(exist_ok=True); OV = R / 'v5b'
V = '-c:v libx264 -preset medium -crf 17 -pix_fmt yuv420p -r 30'.split(); A = '-c:a pcm_s16le -ar 48000 -ac 2'.split()
P = 0.25  # farciment per a les transicions
def ff(*a): subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', *map(str, a)], check=True)
def zc(z, yk=0.19): return f"scale=round(1080*{z}/2)*2:round(1920*{z}/2)*2,crop=1080:1920:(iw-1080)/2:(ih-1920)*{yk},setsar=1"
def seg(out, src, s, e, z, pops=(), push=0.0, audio=None):
    """pops: [(png, t0, t1)] relatius al segment. push: zoom lent extra al llarg del pla."""
    d = round(e - s, 3); ins = ['-ss', s, '-t', d, '-i', src]
    if audio: ins += ['-ss', audio, '-t', d, '-i', N / 'd2p.mov']
    vf = zc(z) if not push else f"scale=2160:3840,zoompan=z='{z}+{push}*on/({d}*30)':x='iw/2-(iw/zoom/2)':y='(ih-ih/zoom)*0.98':d=1:s=1080x1920:fps=30,setsar=1"
    fc = f"[0:v]{vf}[v0]"; last = 'v0'
    for i, (png, t0, t1) in enumerate(pops):
        ins += ['-loop', 1, '-t', d, '-i', OV / png]; k = (2 if audio else 1) + i
        fc += f";[{k}:v]format=rgba,fade=t=in:st={t0}:d=0.12:alpha=1,fade=t=out:st={t1-0.1}:d=0.1:alpha=1[o{i}];[{last}][o{i}]overlay=0:0[v{i+1}]"; last = f'v{i+1}'
    ai = '1:a' if audio else '0:a'
    fc += f";[{ai}]afade=t=in:d=0.03,afade=t=out:st={d-0.04}:d=0.04,aresample=48000[a]"
    ff(*ins, '-filter_complex', fc, '-map', f'[{last}]', '-map', '[a]', '-t', d, *V, *A, out); return d
D2 = N / 'd2p.mov'
# Bloc 1 · ganxo + pont (D2), talls amb zoom alternat
segs = [seg(W/'b1.mov', D2, 1.36, 3.27, 1.22, [('title.png', 0, 99)]),
        seg(W/'b2.mov', D2, 3.27, 6.62, 1.0, [('title.png', 0, 99)]),
        seg(W/'b3.mov', D2, 10.82, 11.95, 1.1),
        seg(W/'b4.mov', S/'c1.mov', 6.00, 7.30, 1.6, push=0.15, audio=11.95),
        seg(W/'b5.mov', D2, 55.40, 56.82, 1.0),
        seg(W/'b6.mov', D2, 56.82, 58.95 + P, 1.1, [('pop_cop.png', 0, 0.80), ('pop_lloc.png', 0.85, 99)])]
(W/'l1.txt').write_text(''.join(f"file '{W}/b{i}.mov'\n" for i in range(1, 7)))
ff('-f', 'concat', '-safe', 0, '-i', W/'l1.txt', '-c', 'copy', W/'B1.mov')
# Escenes del muntatge actual, refetes amb 0,25 s de marge a cada costat
ff('-ss', 0.75 - P, '-t', 6.95 + 2*P, '-i', S/'c2.mov', '-loop', 1, '-i', R/'panels/p2_drop.png', '-filter_complex',
   "[0:v]scale=1080:1920,setsar=1,split[a][b];[a]crop=1080:1200:0:200,boxblur=30:3,eq=brightness=-0.15[bg];[b]scale=918:1632,crop=918:1200:0:150[fg];[bg][fg]overlay=81:0[vid];[1:v]crop=1080:720:0:0,setsar=1[top];[top][vid]vstack[out]",
   '-map', '[out]', '-map', '0:a', '-shortest', *V, *A, W/'B2.mov')
ff('-loop', 1, '-i', R/'v2/s3_bambes.png', '-ss', 3.25 - P, '-t', 10.4 + 2*P, '-i', S/'a3.m4a', '-filter_complex',
   "[0:v]scale=1188:2112,zoompan=z='1+0.0001*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,setsar=1[out]",
   '-map', '[out]', '-map', '1:a', '-t', 10.4 + 2*P, *V, *A, W/'B3.mov')
ff('-ss', 1.0 - P, '-t', 11.9 + 2*P, '-i', S/'n40.mov', '-i', R/'v2/s4_baix_n40.png', '-filter_complex',
   "[0:v]scale=1080:1920,setsar=1[v];[v][1:v]overlay=0:0[out]", '-map', '[out]', '-map', '0:a', *V, *A, W/'B4.mov')
# Bloc 5 · adaptació (8–12 setmanes) amb ell a càmera
seg(W/'b7.mov', S/'c5.mov', 14.60 - P, 18.40, 1.0); seg(W/'b8.mov', S/'c5.mov', 18.40, 20.25 + P, 1.2, [('pop_setm.png', 0.1, 99)])
(W/'l5.txt').write_text(f"file '{W}/b7.mov'\nfile '{W}/b8.mov'\n"); ff('-f', 'concat', '-safe', 0, '-i', W/'l5.txt', '-c', 'copy', W/'B5.mov')
# Bloc 6 · cita (foto + dades), 3,2 s
FOTO = R/'../../fotos_standard/tonus_camilla_tauleta_somriu.jpg'
ff('-loop', 1, '-i', FOTO, '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-loop', 1, '-i', R/'v3/cta_web.png', '-filter_complex',
   "[0:v]scale=-2:2112,crop=1188:2112:(iw-1188)*0.55:0,zoompan=z='1+0.0012*on':x='iw/2-(iw/zoom/2)':y='ih/3-(ih/zoom/3)':d=1:s=1080x1920:fps=30,setsar=1[p];[2:v]format=rgba,fade=t=in:st=0.15:d=0.3:alpha=1[c];[p][c]overlay=0:0[out]",
   '-map', '[out]', '-map', '1:a', '-t', 3.2 + P, *V, *A, W/'B6.mov')
# Transicions
blocks = [W/f'B{i}.mov' for i in range(1, 7)]; trans = ['zoomin', 'slideleft', 'slideup', 'smoothleft', 'fadeblack']
dur = lambda f: float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', f], capture_output=True, text=True).stdout)
ds = [dur(b) for b in blocks]; ins = sum((['-i', b] for b in blocks), [])
fc = ''; lv, la = '0:v', '0:a'; acc = ds[0]; T = []
for i, t in enumerate(trans, 1):
    off = round(acc - P, 3); T.append(off)
    fc += f"[{lv}][{i}:v]xfade=transition={t}:duration={P}:offset={off}[xv{i}];[{la}][{i}:a]acrossfade=d={P}[xa{i}];"
    lv, la = f'xv{i}', f'xa{i}'; acc = acc + ds[i] - P
# whoosh suau a cada transició
nw = len(T); fc += f"anoisesrc=c=pink:d=0.45:a=0.5,highpass=f=900,lowpass=f=5500,afade=t=in:d=0.2,afade=t=out:st=0.2:d=0.25,volume=0.10,aformat=sample_rates=48000:channel_layouts=stereo,asplit={nw}" + ''.join(f'[w{i}]' for i in range(nw)) + ';'
fc += ''.join(f"[w{i}]adelay={int((t - 0.12)*1000)}|{int((t - 0.12)*1000)}[wd{i}];" for i, t in enumerate(T))
fc += f"[{la}]highpass=f=80,afftdn=nf=-25,acompressor=threshold=-20dB:ratio=3:attack=5:release=100[voz];[voz]" + ''.join(f'[wd{i}]' for i in range(nw)) + f"amix=inputs={nw+1}:normalize=0:duration=first,loudnorm=I=-14:TP=-1.5:LRA=11[aout]"
ff(*ins, '-filter_complex', fc, '-map', f'[{lv}]', '-map', '[aout]', *V, '-c:a', 'aac', '-b:a', '192k', '-ar', 48000, N/'reel_drop_B.mp4')
print('durada', dur(N/'reel_drop_B.mp4'), 'transicions', T)
