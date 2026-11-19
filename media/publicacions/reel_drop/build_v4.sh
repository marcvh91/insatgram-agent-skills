#!/bin/bash
# Muntatge Reel drop v3. Ús: build_v3.sh <dir_clips>  (c1..c5.mov)
set -e
S=${1:-/home/claude/reel_drop_src}; R=$(cd "$(dirname "$0")" && pwd); W=$S/work; mkdir -p $W
V="-c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -r 30"
A="-c:a aac -b:a 192k -ar 48000 -ac 2"
# 1 · ganxo: títol des del fotograma 0 fins a 4,0 s; després es veu la sabatilla
ffmpeg -v error -y -ss 1.55 -t 5.45 -i $S/c1.mov -loop 1 -i $R/v3/t1_ganxo.png -filter_complex \
 "[0:v]scale=1080:1920,setsar=1[v];[1:v]format=rgba,null[o];[v][o]overlay=0:0:shortest=1[out]" \
 -map "[out]" -map 0:a $V $A $W/s1.mp4
# 2 · què és el drop: panell a dalt (720) + vídeo a baix (1200) amb laterals difuminats
ffmpeg -v error -y -ss 0.75 -t 6.95 -i $S/c2.mov -loop 1 -i $R/panels/p2_drop.png -filter_complex \
 "[0:v]scale=1080:1920,setsar=1,split[a][b];[a]crop=1080:1200:0:200,boxblur=30:3,eq=brightness=-0.15[bg];\
[b]scale=918:1632,crop=918:1200:0:150[fg];[bg][fg]overlay=81:0[vid];[1:v]crop=1080:720:0:0,setsar=1[top];\
[top][vid]vstack[out]" -map "[out]" -map 0:a -shortest $V $A $W/s2.mp4
# 3 · tipus: 3 sabatilles a pantalla completa + veu
ffmpeg -v error -y -loop 1 -i $R/v2/s3_bambes.png -ss 1.25 -t 17.05 -i $S/n41.mov -filter_complex \
 "[0:v]scale=1188:2112,zoompan=z='1+0.0001*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,setsar=1[out]" \
 -map "[out]" -map 1:a -t 17.05 $V $A $W/s3.mp4
# 4 · on va la tensió: dibuixos a les cantonades de dalt
ffmpeg -v error -y -ss 1.0 -t 11.9 -i $S/n40.mov -i $R/v2/s4_dalt.png -filter_complex \
 "[0:v]scale=1080:1920,setsar=1[v];[v][1:v]overlay=0:0[out]" -map "[out]" -map 0:a $V $A $W/s4.mp4
# 5 · consells (títol) + cita (targeta WhatsApp)
ffmpeg -v error -y -ss 0.5 -t 19.75 -i $S/c5.mov -loop 1 -i $R/v3/t5_canvi.png -loop 1 -i $R/panels/ov9_cta.png -filter_complex \
 "[0:v]scale=1080:1920,setsar=1[v];[v][1:v]overlay=0:0:shortest=1:enable='lt(t,13.6)'[v1];[2:v]format=rgba,fade=t=in:st=14.1:d=0.3:alpha=1[c];[v1][c]overlay=0:0:shortest=1:enable='gte(t,14.1)'[out]" \
 -map "[out]" -map 0:a $V $A $W/s5.mp4
printf "file '%s'\n" $W/s1.mp4 $W/s2.mp4 $W/s3.mp4 $W/s4.mp4 $W/s5.mp4 > $W/list.txt
ffmpeg -v error -y -f concat -safe 0 -i $W/list.txt -c copy $W/concat.mp4
ffmpeg -v error -y -i $W/concat.mp4 -c:v copy -af "highpass=f=80,afftdn=nf=-25,acompressor=threshold=-20dB:ratio=3:attack=5:release=100,loudnorm=I=-14:TP=-1.5:LRA=11" $A $R/reel_drop.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 $R/reel_drop.mp4
