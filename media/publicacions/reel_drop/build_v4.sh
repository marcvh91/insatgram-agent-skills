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
ffmpeg -v error -y -loop 1 -i $R/v2/s3_bambes.png -ss 3.25 -t 10.4 -i $S/a3.m4a -filter_complex \
 "[0:v]scale=1188:2112,zoompan=z='1+0.0001*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1920:fps=30,setsar=1[out]" \
 -map "[out]" -map 1:a -t 10.4 $V $A $W/s3.mp4
# 4 · on va la tensió: dibuixos a baix (els assenyala)
ffmpeg -v error -y -ss 1.0 -t 11.9 -i $S/n40.mov -i $R/v2/s4_baix_n40.png -filter_complex \
 "[0:v]scale=1080:1920,setsar=1[v];[v][1:v]overlay=0:0[out]" -map "[out]" -map 0:a $V $A $W/s4.mp4
# 5a · canvi de calçat i adaptació al drop (títol) — va just després del ganxo
ffmpeg -v error -y -ss 0.5 -t 13.75 -i $S/c5.mov -loop 1 -i $R/v3/t5_canvi.png -filter_complex \
 "[0:v]scale=1080:1920,setsar=1[v];[v][1:v]overlay=0:0:shortest=1[out]" -map "[out]" -map 0:a $V $A $W/s5a.mp4
# 6 · cita: foto del banc (tonus_camilla_tauleta_somriu) + WhatsApp, Tonus i web, amb la veu del clip 5
FOTO=$R/../../fotos_standard/tonus_camilla_tauleta_somriu.jpg
ffmpeg -v error -y -loop 1 -i $FOTO -ss 14.55 -t 5.7 -i $S/c5.mov -loop 1 -i $R/v3/cta_web.png -filter_complex \
 "[0:v]scale=-2:2112,crop=1188:2112:(iw-1188)*0.55:0,zoompan=z='1+0.0012*on':x='iw/2-(iw/zoom/2)':y='ih/3-(ih/zoom/3)':d=1:s=1080x1920:fps=30,setsar=1[p];\
[2:v]format=rgba,fade=t=in:st=0:d=0.3:alpha=1[c];[p][c]overlay=0:0:shortest=1[out]" -map "[out]" -map 1:a -t 5.7 $V $A $W/s6.mp4
printf "file '%s'\n" $W/s1.mp4 $W/s5a.mp4 $W/s2.mp4 $W/s3.mp4 $W/s4.mp4 $W/s6.mp4 > $W/list.txt
ffmpeg -v error -y -f concat -safe 0 -i $W/list.txt -c copy $W/concat.mp4
ffmpeg -v error -y -i $W/concat.mp4 -c:v copy -af "highpass=f=80,afftdn=nf=-25,acompressor=threshold=-20dB:ratio=3:attack=5:release=100,loudnorm=I=-14:TP=-1.5:LRA=11" $A $R/reel_drop.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 $R/reel_drop.mp4
