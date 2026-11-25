import base64, html
e = html.escape
def img(f, alt): return f'<img src="data:image/jpeg;base64,{base64.b64encode(open(f,"rb").read()).decode()}" alt="{e(alt)}" loading="lazy">'
def sk(kind, alt):
    shoes = {
     "dues": '<circle cx="45" cy="52" r="11" fill="var(--fig)"/><path d="M18,160 C18,98 30,76 45,74 C60,76 72,98 72,160 Z" fill="var(--fig)"/><g><path d="M6,92 h26 v6 c-6,8 -20,8 -26,4 Z" fill="var(--lime)"/><rect x="6" y="98" width="26" height="9" rx="2" fill="#fff"/><text x="19" y="120" text-anchor="middle" font-size="8" font-weight="800" fill="var(--lime)">ALT</text></g><g><path d="M58,98 h26 v5 c-6,6 -20,6 -26,3 Z" fill="#7cc4ff"/><rect x="58" y="103" width="26" height="4" rx="1" fill="#fff"/><text x="71" y="120" text-anchor="middle" font-size="8" font-weight="800" fill="#7cc4ff">BAIX</text></g>',
     "peus": '<line x1="4" y1="132" x2="86" y2="132" stroke="var(--line)" stroke-width="2"/><path d="M14,70 L26,118 L20,128 L40,128 L36,116 L30,70 Z" fill="var(--fig)"/><path d="M50,60 L62,104 L58,114 L80,112 L72,102 L64,60 Z" fill="var(--fig)" opacity=".7"/><rect x="18" y="122" width="24" height="8" rx="3" fill="var(--lime)"/><rect x="56" y="108" width="24" height="8" rx="3" fill="var(--lime)" opacity=".7"/><text x="45" y="150" text-anchor="middle" font-size="8" font-weight="700" fill="var(--mute)">mòbil a terra</text>',
    }[kind]
    return f'<svg viewBox="0 0 90 160" role="img" aria-label="{e(alt)}"><rect x="1" y="1" width="88" height="158" rx="10" fill="var(--panel2)" stroke="var(--line)" stroke-width="2"/>{shoes}</svg>'
CL = [
 ("1", "Ganxo", "0–3 s", "B", img("ref_ganxo.jpg","Bamba davant de l'objectiu"),
  "Has canviat de bambes i ara et fa mal el <b>genoll</b> o l'<b>Aquil·les</b>?",
  "Comença amb la bamba <b>tapant l'objectiu</b> i baixa-la mentre parles fins que se't vegi la cara. Mirada directa.",
  "Títol des del primer fotograma + so de cop"),
 ("2", "La sospita", "3–5 s", "A", img("ref_B.jpg","Primer pla"),
  "Pot ser culpa del <b>drop</b>.",
  "Cella aixecada i dos copets amb el dit a la bamba.",
  "Zoom ràpid al teu primer pla"),
 ("3", "Què és", "5–9 s", "B", img("ref_detall.jpg","Bamba de perfil"),
  "El drop és la diferència d'alçada entre el <b>taló</b> i la <b>punta</b>.",
  "Bamba de perfil sobre la camilla. El dit va lentament del taló a la punta.",
  "Línies lima amb els mil·límetres + il·lustració 0 / 4–6 / 8–12 mm"),
 ("4", "Alt i baix", "9–14 s", "A", sk("dues","Una bamba a cada mà"),
  "Drop <b>alt</b>: més càrrega al <b>genoll</b>. <i>(pausa)</i> Drop <b>baix</b>: més feina per al <b>bessó</b> i l'<b>Aquil·les</b>.",
  "Aixeca la de taló alt a «drop alt»; baixa-la i aixeca la plana a «drop baix».",
  "Etiqueta damunt de cada bamba"),
 ("5", "La idea clau", "14–17 s", "A", img("ref_A.jpg","Pla de cintura amunt"),
  "La càrrega <b>no desapareix</b>: <b>canvia de lloc</b>.",
  "Fes <b>un pas cap a càmera</b> mentre ho dius. Les mans es mouen d'un costat a l'altre a «canvia de lloc».",
  "Paraules clau en lima"),
 ("6", "El risc", "17–21 s", "A", sk("peus","Peus corrent"),
  "Per això, si canvies de drop <b>de cop</b>, el cos no té temps d'adaptar-s'hi.",
  "Mans obertes de cop a «de cop».",
  "A mitja frase, tallo als teus peus corrent (recurs R1)"),
 ("7", "Què fer", "21–24 s", "A", img("ref_A.jpg","Pla de cintura amunt"),
  "Fes-ho a poc a poc: <b>dotze setmanes</b> o més.",
  "Compta amb els dits / mà que baixa a poc a poc.",
  "«12+ SETMANES» en lima"),
 ("8", "Comoditat", "24–26 s", "A", img("ref_A.jpg","Pla de cintura amunt"),
  "I tria la que et sigui <b>més còmoda</b>.",
  "Somriu i abraça la bamba contra el pit.",
  "—"),
 ("9", "Crida", "26–30 s", "C", img("ref_cta.jpg","Caminant cap a càmera"),
  "Et fa mal el genoll o l'Aquil·les quan corres? <b>Escriu-me</b> i ho mirem.",
  "Comença a 3 m i <b>camina cap a càmera</b> mentre parles; para a 1 m i assenyala avall.",
  "WhatsApp, Tonus i web a baix"),
]
REC = [
 ("R1", "Peus corrent", "Mòbil a terra (o a 20 cm), de costat. Passa 3 vegades corrent a ritme suau. Bambes visibles."),
 ("R2", "Canvi de bambes", "Assegut: et treus una bamba i et poses l'altra. Només mans i peus, 5 s."),
 ("R3", "Mans doblegant la bamba", "Primer pla de les mans doblegant la sola i prement el taló. 4 s."),
]
SET = {"A": "Trípode a 1,5 m, cintura amunt", "B": "Trípode a 40 cm, a l'altura del pit", "C": "Trípode del pla A; tu comences a 3 m"}
def card(n, name, t, s, pic, say, act, edit):
    return f'''<li class="clip"><figure>{pic}</figure><div class="txt">
<div class="hd"><label class="chk"><input type="checkbox" id="c{n}"><span>{n}</span></label><b>{e(name)}</b><span class="pill">{e(t)}</span><span class="pill set">Pla {s}</span></div>
<p class="say">«{say}»</p><dl><dt>Què fas</dt><dd>{act}</dd><dt>Edició</dt><dd>{e(edit)}</dd></dl></div></li>'''
clips = "".join(card(*c) for c in CL)
rec = "".join(f'<li class="mini"><label class="chk"><input type="checkbox" id="r{i}"><span>{i}</span></label><div><b>{e(a)}</b><p>{e(b)}</p></div></li>' for i,a,b in REC)
sets = "".join(f'<li><span class="pill set">Pla {k}</span> {e(v)}</li>' for k,v in SET.items())
page = f'''<title>Rodatge Reel drop v6</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@500;600;800;900&display=swap">
<style>
/* Guió de rodatge mòbil: preparació → 9 clips en ordre del Reel → recursos */
:root{{--bg:#0B0F12;--panel:#12181C;--panel2:#171E23;--line:#263038;--fg:#E8ECEF;--mute:#9AA5AC;--lime:#D4FF3F;--fig:#5E6A72;--warn:#FF8A7A;--font:Inter,system-ui,sans-serif;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font:15px/1.5 var(--font);margin:0}}
.wrap{{max-width:760px;margin:0 auto;padding-block:28px 64px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:grid;gap:28px}}
h1{{font-size:clamp(28px,7vw,40px);font-weight:900;letter-spacing:-1.5px;line-height:1.02;margin:0;text-wrap:balance}}
h1 em{{font-style:normal;color:var(--lime)}}
.lead{{color:var(--mute);margin:8px 0 0}}
h2{{font-size:13px;text-transform:uppercase;letter-spacing:.12em;color:var(--lime);margin:0 0 12px}}
section{{display:grid}}
.box{{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:18px}}
.box ul{{margin:0;padding-left:18px;display:grid;gap:6px}}
.light{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:14px}}
.light figure{{margin:0}} .light img{{width:100%;border-radius:10px;display:block}}
.light figcaption{{font-size:13px;color:var(--mute);margin-top:6px}} .light .bad figcaption b{{color:var(--warn)}} .light .good figcaption b{{color:var(--lime)}}
.sets{{list-style:none;padding:0;margin:12px 0 0;display:grid;gap:6px}}
ol.clips,ul.recs{{list-style:none;margin:0;padding:0;display:grid;gap:14px}}
.clip{{display:grid;grid-template-columns:120px 1fr;gap:14px;background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:12px}}
.clip figure{{margin:0}} .clip img,.clip svg{{width:100%;aspect-ratio:9/16;object-fit:cover;border-radius:10px;display:block}}
.txt{{min-width:0;display:grid;gap:8px;align-content:start}}
.hd{{display:flex;flex-wrap:wrap;align-items:center;gap:8px}}
.pill{{font-size:12px;font-weight:700;background:var(--panel2);border:1px solid var(--line);border-radius:99px;padding:2px 9px;color:var(--mute);font-variant-numeric:tabular-nums}}
.pill.set{{color:var(--lime);border-color:color-mix(in srgb,var(--lime) 40%,transparent)}}
.say{{margin:0;font-size:17px;font-weight:600;line-height:1.35}} .say b{{color:var(--lime);font-weight:800}}
dl{{margin:0;display:grid;grid-template-columns:auto 1fr;gap:4px 10px;font-size:14px}} dt{{color:var(--mute);font-weight:600}} dd{{margin:0}}
.chk{{display:inline-flex;align-items:center;gap:6px;cursor:pointer}}
.chk input{{width:20px;height:20px;accent-color:var(--lime)}}
.chk span{{font-weight:900;color:var(--lime)}}
.mini{{display:flex;gap:12px;background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:12px}} .mini p{{margin:2px 0 0;color:var(--mute);font-size:14px}}
input:focus-visible{{outline:2px solid var(--lime);outline-offset:2px}}
@media (max-width:480px){{.clip{{grid-template-columns:92px 1fr}} .say{{font-size:16px}}}}
</style>
<main class="wrap">
<header><h1>Reel drop · <em>rodatge nou</em></h1><p class="lead">9 clips curts, ~30 s en total, en polo de Tonus. Una sola sessió de ~25 min, al mateix lloc i amb la mateixa llum.</p></header>
<section><h2>Abans de gravar</h2><div class="box"><ul>
<li><b>Llum (el que va fallar):</b> tot al mateix lloc i a la mateixa hora. Apaga les bombetes càlides; si hi ha finestra, posa't de cara a la finestra. No barregis la llum de la finestra amb la de les bombetes.</li>
<li><b>Càmera del darrere 1×</b>, no la frontal: la frontal grava en mirall (el logo surt girat) i amb menys qualitat.</li>
<li>4K 30 fps · <b>Vídeo HDR desactivat</b> (Ajustes › Cámara › Grabar vídeo).</li>
<li><b>Bloqueja la llum:</b> abans de cada pla, mantén el dit sobre la teva cara fins que surti «Bloqueo AE/AF». No ho toquis més.</li>
<li>Micro al pit. Els primers plans els retallo jo del 4K: no cal moure el trípode per fer-los.</li>
<li><b>Material:</b> dues bambes amb drop diferent (una de taló alt, 8–12 mm, i una plana, 0–4 mm).</li>
</ul>
<div class="light"><figure class="good">{img("llum_be.jpg","Llum neutra")}<figcaption><b>Així:</b> paret blanca, llum neutra</figcaption></figure><figure class="bad">{img("llum_mal.jpg","Llum càlida")}<figcaption><b>No així:</b> llum groga de bombeta</figcaption></figure></div>
<ul class="sets">{sets}</ul></div></section>
<section><h2>Energia: per què et veies avorrit</h2><div class="box"><ul>
<li>Parla <b>un 30 % més fort i més ràpid</b> del que et sembla natural. A càmera tot es veu més pla.</li>
<li>Comença cada frase <b>ja en moviment</b> (un gest o un pas), mai des de quiet.</li>
<li><b>Somriu</b> el primer mig segon de cada presa.</li>
<li>Una idea, un gest. Mans sempre dins del pla.</li>
<li><b>3 preses</b> de cada clip: normal, amb més energia, i amb més energia i el gest exagerat. Em quedo la millor.</li>
<li>Si t'equivoques, 2 s de silenci i torna a dir la frase sencera. Ja puc transcriure les preses i trio les bones jo.</li>
<li><b>Un vídeo per clip</b> i adjunta'ls al xat (el Drive no em deixa baixar vídeos grans).</li>
</ul></div></section>
<section><h2>Els 9 clips, en l'ordre del Reel</h2><ol class="clips">{clips}</ol></section>
<section><h2>Recursos (sense parlar)</h2><ul class="recs">{rec}</ul></section>
</main>'''
open("index.html","w").write(page)
