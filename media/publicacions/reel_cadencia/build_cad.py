"""Maqueta del Reel «180 passes per minut?» · 25 s, només text (música des de l'app)."""
import subprocess, pathlib
R = pathlib.Path(__file__).parent; OV = R / 'ov'; W = pathlib.Path('/home/claude/tecnica/w'); W.mkdir(exist_ok=True)
SLOW = '/mnt/user-data/uploads/IMG_4164.mov'; REAL = '/mnt/user-data/uploads/IMG_4163.mov'
V = '-c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -r 30 -an'.split()
def ff(*a): subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', *map(str, a)], check=True)
def seg(out, src, s, d, ovs, freeze=False):
    ins = (['-ss', s, '-i', src] if freeze else ['-ss', s, '-t', d, '-i', src])
    fc = "[0:v]scale=1080:1920:flags=lanczos,setsar=1" + (f",trim=end_frame=1,loop=loop={int(d*30)}:size=1:start=0,setpts=N/30/TB" if freeze else "") + "[v0]"; last = 'v0'
    for i, png in enumerate(ovs):
        ins += ['-loop', 1, '-framerate', 30, '-t', d, '-i', OV / png]; fc += f";[{last}][{i+1}:v]overlay=0:0[v{i+1}]"; last = f'v{i+1}'
    ff(*ins, '-filter_complex', fc, '-map', f'[{last}]', '-t', d, *V, out)
P = [('a', SLOW, 20.14, 3.5, ['annot.png', 't0.png'], True),
     ('b', SLOW, 20.14, 4.0, ['annot.png', 't1.png'], True),
     ('c', SLOW, 20.3, 4.6, ['t2.png'], False),
     ('d', SLOW, 25.0, 3.6, ['t3.png'], False),
     ('e', REAL, 5.0, 4.4, ['t4.png'], False),
     ('f', REAL, 9.4, 4.6, ['t5.png'], False),
     ('g', SLOW, 28.6, 4.6, ['t6.png'], False),
     ('h', SLOW, 33.2, 6.0, ['t7.png'], False)]
for n, src, s, d, ovs, fr in P: seg(W / f'{n}.mp4', src, s, d, ovs, fr)
(W / 'l.txt').write_text(''.join(f"file '{W}/{p[0]}.mp4'\n" for p in P))
ff('-f', 'concat', '-safe', 0, '-i', W / 'l.txt', '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo', '-c:v', 'copy', '-c:a', 'aac', '-shortest', R / 'reel_cadencia_maqueta.mp4')
