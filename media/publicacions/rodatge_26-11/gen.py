import base64, html
e = html.escape
def img(f, alt, cls=""): return f'<img class="{cls}" src="data:image/jpeg;base64,{base64.b64encode(open(f,"rb").read()).decode()}" alt="{e(alt)}" loading="lazy">'
FIG = 'fill="var(--fig)"'
SK = {
 "cos": f'<circle cx="45" cy="30" r="10" {FIG}/><path d="M24,160 L24,62 C24,48 34,44 45,44 C56,44 66,48 66,62 L66,160 Z" {FIG}/><path d="M66,78 L76,120" stroke="var(--lime)" stroke-width="5" stroke-linecap="round"/><circle cx="76" cy="122" r="5" fill="var(--lime)"/><text x="45" y="154" text-anchor="middle" font-size="8" font-weight="700" fill="var(--bg)">genolls amunt</text>',
 "genoll": f'<path d="M20,0 C30,40 32,70 34,100 C36,130 30,150 28,160 L62,160 C64,140 70,120 70,96 C70,60 64,30 60,0 Z" {FIG}/><circle cx="68" cy="98" r="7" fill="var(--lime)"/><path d="M90,80 L72,96" stroke="var(--lime)" stroke-width="4" stroke-linecap="round"/><text x="45" y="16" text-anchor="middle" font-size="8" font-weight="700" fill="var(--mute)">mòbil a 50 cm</text>',
 "camina": f'<circle cx="45" cy="56" r="6" {FIG}/><path d="M37,64 h16 v40 h-16 Z" {FIG}/><path d="M39,104 l-4,24 M51,104 l4,24" stroke="var(--fig)" stroke-width="5"/><path d="M45,132 L45,150" stroke="var(--lime)" stroke-width="3"/><path d="M39,144 L45,152 L51,144" stroke="var(--lime)" stroke-width="3" fill="none"/><text x="45" y="30" text-anchor="middle" font-size="8" font-weight="700" fill="var(--mute)">comences a 3 m</text>',
 "corre": f'<circle cx="52" cy="40" r="8" {FIG}/><path d="M44,50 L58,50 L54,92 L42,92 Z" {FIG}/><path d="M46,92 L30,120 L22,140 M52,92 L64,118 L80,124" stroke="var(--fig)" stroke-width="6" stroke-linecap="round" fill="none"/><path d="M44,56 L28,76 M58,56 L72,70" stroke="var(--fig)" stroke-width="5" stroke-linecap="round"/><line x1="4" y1="146" x2="86" y2="146" stroke="var(--line)" stroke-width="2"/>',
 "veu": '<rect x="35" y="40" width="20" height="44" rx="10" fill="var(--lime)"/><path d="M26,70 C26,96 64,96 64,70" stroke="var(--lime)" stroke-width="4" fill="none"/><path d="M45,96 L45,118 M33,118 L57,118" stroke="var(--lime)" stroke-width="4"/><text x="45" y="146" text-anchor="middle" font-size="8" font-weight="700" fill="var(--mute)">només àudio</text>',
}
def sk(k, alt): return f'<svg viewBox="0 0 90 160" role="img" aria-label="{e(alt)}"><rect x="1" y="1" width="88" height="158" rx="10" fill="var(--panel2)" stroke="var(--line)" stroke-width="2"/>{SK[k]}</svg>'
def card(n, name, t, pla, pic, say, act, edit, extra=""):
    ex = f'<div class="ex">{extra}</div>' if extra else ""
    return f'''<li class="clip"><figure>{pic}</figure><div class="txt">
<div class="hd"><label class="chk"><input type="checkbox" id="c{e(n)}"><span>{e(n)}</span></label><b>{e(name)}</b><span class="pill">{e(t)}</span><span class="pill set">{e(pla)}</span></div>
<p class="say">«{say}»</p><dl><dt>Què fas</dt><dd>{act}</dd><dt>Edició</dt><dd>{e(edit)}</dd></dl>{ex}</div></li>'''
DROP = [
 ("D1", "Ganxo + portada", "0–6 s", "Pla A", img("ref_ganxo.jpg", "Bamba a l'altura del pit"),
  "Tens molèsties al tendó d'<b>Aquil·les</b> o al <b>genoll</b> quan corres, i mai t'has parat a mirar el <b>calçat</b>?",
  "Comença sense bamba. A «calçat», aixeca-la <b>a l'altura del pit</b> (a sota hi va el títol). En acabar, <b>2 s quiet somrient de veritat</b> amb la bamba: d'aquí trec la portada.",
  "Títol a baix, igual que ara"),
 ("D2", "Pont", "6–11 s", "Pla A", img("ref_pont.jpg", "Pla de cintura amunt amb títol a dalt"),
  "Potser has canviat de bambes i, sense adonar-te'n, també has canviat el <b>drop</b>.",
  "Sense bamba. Mans obertes a «sense adonar-te'n», dit amunt a «drop».",
  "Títol a dalt «El canvi de calçat i l'adaptació al drop!»"),
 ("D3", "Què és el drop", "11–18 s", "Pla A", img("ref_que.jpg", "Dibuix a dalt i tu a baix"),
  "Això és el drop: la diferència d'altura entre el <b>taló</b> i la <b>punta</b>. I aquesta té un drop de <b>__ mil·límetres</b>.",
  "Bamba de perfil a l'altura del pit. Assenyala el taló i després la punta. <b>Mira abans quin drop té</b> (a la web de la marca).",
  "A dalt, el dibuix del drop; a baix, tu"),
 ("D4", "Els 3 tipus (àudio)", "18–25 s", "Veu", img("ref_il.jpg", "Il·lustració de les 3 sabatilles"),
  "N'hi ha de tres tipus. <b>Zero drop</b>: taló i punta a la mateixa altura. <b>Drop baix</b>: de quatre a sis mil·límetres. I <b>drop alt</b>: de vuit a dotze, el més habitual.",
  "Grava-ho com un vídeo normal (al mateix lloc) i <b>somriu mentre parles</b>; només en faig servir l'àudio.",
  "Il·lustració a pantalla completa; cada sabatilla s'il·lumina quan l'anomenes"),
 ("D5", "On va la tensió", "25–35 s", "Pla A, més obert", img("ref_cards.jpg", "Targetes de drop alt i baix a baix"),
  "Les bambes amb drop <b>alt</b> porten la tensió cap al <b>genoll</b>. <i>(pausa)</i> Les de drop <b>baix</b>, cap al tendó d'<b>Aquil·les</b> i el <b>bessó</b>. <i>(pausa)</i> La càrrega <b>no desapareix</b>: <b>canvia de lloc</b>.",
  "Sense bamba. A «drop alt», assenyala avall a la teva <b>dreta</b>; a «drop baix», avall a la teva <b>esquerra</b>. A l'última frase, mira a càmera i mou les mans d'un costat a l'altre. Cara i pit a la <b>meitat de dalt</b>: a baix hi van les targetes.",
  "Targetes DROP ALT i DROP BAIX a baix"),
 ("D6", "L'adaptació", "35–40 s", "Pla A", img("ref_A.jpg", "Pla de cintura amunt"),
  "Si canvies de drop, fes-ho <b>a poc a poc</b>: dona-li de <b>vuit a dotze setmanes</b>.",
  "Compta amb els dits a «vuit a dotze». Ritme tranquil però amb energia.",
  "«8–12 SETMANES» en lima"),
 ("D7", "Crida", "40–45 s", "Pla A", img("ref_cta.jpg", "Caminant cap a càmera"),
  "Et fa mal el genoll o l'Aquil·les quan corres? <b>Escriu-me</b> i ho mirem.",
  "Comença a 3 m i <b>camina cap a càmera</b>; para a 1,5 m, somriu i assenyala avall.",
  "WhatsApp, Tonus i web a baix (si no el fas, es queda la foto actual)"),
]
CINT = [
 ("C1", "Ganxo + portada", "0–4 s", "Pla A", sk("corre", "Entres corrent"),
  "Et fa mal la <b>cara externa del genoll</b> quan corres? Pot ser la <b>cintilla</b>.",
  "Entra <b>corrent</b> al pla, para't i parla amb la mà a la cara externa del genoll. Al final, <b>2 s somrient</b> mirant a càmera (portada).",
  "Títol a dalt des del primer fotograma"),
 ("C2", "Què és", "4–10 s", "Pla A", img("p2_cintilla.jpg", "3D de la cintilla"),
  "És una <b>banda de teixit molt dura</b> que baixa per la cara externa de la cuixa, des del <b>maluc</b> fins a sota del <b>genoll</b>.",
  "Recorre amb la mà el lateral de la cuixa, del maluc al genoll, lentament.",
  "A mitja frase, tallo al 3D de la cintilla"),
 ("C3", "Qui hi tira", "10–16 s", "Pla A", img("p4_tfl_src.jpg", "3D del tensor de la fàscia lata"),
  "Hi tiren <b>dos músculs</b>: el <b>tensor de la fàscia lata</b>, per davant, i el <b>gluti major</b>, per darrere.",
  "«Dos» amb els dits. Toca el davant del maluc i després el gluti (gira't una mica de costat).",
  "3D del tensor i del gluti major, un darrere l'altre"),
 ("C4", "On fa mal", "16–23 s", "Pla C + A", img("p3_genoll.jpg", "3D del genoll"),
  "El dolor surt <b>aquí</b>. Abans es pensava que fregava l'os. Avui sabem que més aviat <b>comprimeix</b> un teixit amb nervis que hi ha a sota.",
  "Primer «El dolor surt aquí» al <b>pla C</b> (detall del genoll, el dit assenyala). La resta al pla A: frega les mans a «fregava» i prem el puny contra la mà a «comprimeix».",
  "3D del genoll + els teus gestos"),
 ("C5", "Per què", "23–30 s", "Pla A", img("p6_gmed.jpg", "3D del gluti mitjà"),
  "Per què? Sobretot per pujar <b>massa de pressa</b> els quilòmetres o la intensitat. I en corredores s'ha vist menys força al <b>gluti mitjà</b>.",
  "Mà que puja ràpid a «massa de pressa». Mà al lateral del maluc a «gluti mitjà».",
  "3D del gluti mitjà"),
 ("C6", "Què fer", "30–38 s", "Pla A", sk("cos", "Pla de genolls amunt"),
  "Què fer? Estirar-la <b>no l'allargarà</b>. El que funciona és <b>enfortir el maluc</b>: als estudis, el dolor baixa en <b>dues a vuit setmanes</b>. I ajusta la càrrega uns dies.",
  "Nega amb el cap a «no l'allargarà». Puny ferm a «enfortir». Dits a «dues a vuit».",
  "A «enfortir el maluc», tallo als teus exercicis a contrallum (S2 i S3)"),
 ("C7", "Crida", "38–42 s", "Pla A", sk("camina", "Camines cap a càmera"),
  "Et fa mal la cara externa del genoll? <b>Escriu-me</b> i ho mirem.",
  "Comença a 3 m i <b>camina cap a càmera</b> mentre parles. Para a 1,5 m i assenyala avall.",
  "WhatsApp, Tonus i web a baix"),
]
REC = [("R1", "Peus i genolls corrent de costat", "Mòbil a l'altura del genoll, a 2 m. Passa 3 vegades corrent suau per davant."),
       ("R2", "S2 i S3 a contrallum", "Ja els tens gravats: envia'ls adjuntats al xat.")]
drop = "".join(card(*c) for c in DROP); cint = "".join(card(*c) for c in CINT)
rec = "".join(f'<li class="mini"><label class="chk"><input type="checkbox" id="r{i}"><span>{i}</span></label><div><b>{e(a)}</b><p>{e(b)}</p></div></li>' for i, a, b in REC)
page = f'''<title>Rodatge drop i cintilla</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@500;600;800;900&display=swap">
<style>
/* Guió de rodatge mòbil: part 1 (drop, avui) i part 2 (cintilla), cada clip amb text literal, gest i edició */
:root{{--bg:#0B0F12;--panel:#12181C;--panel2:#171E23;--line:#263038;--fg:#E8ECEF;--mute:#9AA5AC;--lime:#D4FF3F;--fig:#5E6A72;--font:Inter,system-ui,sans-serif;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font:15px/1.5 var(--font);margin:0}}
.wrap{{max-width:760px;margin:0 auto;padding-block:28px 64px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:grid;gap:30px}}
h1{{font-size:clamp(28px,7vw,40px);font-weight:900;letter-spacing:-1.5px;line-height:1.02;margin:0;text-wrap:balance}} h1 em{{font-style:normal;color:var(--lime)}}
.lead{{color:var(--mute);margin:8px 0 0}}
h2{{font-size:22px;font-weight:900;letter-spacing:-.5px;margin:0 0 4px}} h2 span{{color:var(--lime)}}
h3{{font-size:13px;text-transform:uppercase;letter-spacing:.12em;color:var(--lime);margin:18px 0 10px}}
section{{display:grid}} .sub{{color:var(--mute);margin:0 0 6px}}
.box{{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:18px}}
.box ul{{margin:0;padding-left:18px;display:grid;gap:6px}}
ol.clips,ul.recs{{list-style:none;margin:0;padding:0;display:grid;gap:14px}}
.clip{{display:grid;grid-template-columns:120px 1fr;gap:14px;background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:12px}}
.clip figure{{margin:0}} .clip figure img,.clip svg{{width:100%;aspect-ratio:9/16;object-fit:cover;border-radius:10px;display:block}}
.txt{{min-width:0;display:grid;gap:8px;align-content:start}}
.hd{{display:flex;flex-wrap:wrap;align-items:center;gap:8px}}
.pill{{font-size:12px;font-weight:700;background:var(--panel2);border:1px solid var(--line);border-radius:99px;padding:2px 9px;color:var(--mute);font-variant-numeric:tabular-nums}}
.pill.set{{color:var(--lime);border-color:color-mix(in srgb,var(--lime) 40%,transparent)}}
.say{{margin:0;font-size:17px;font-weight:600;line-height:1.35}} .say b{{color:var(--lime);font-weight:800}}
dl{{margin:0;display:grid;grid-template-columns:auto 1fr;gap:4px 10px;font-size:14px}} dt{{color:var(--mute);font-weight:600}} dd{{margin:0}}
.ex img.il{{width:100%;max-width:220px;border-radius:10px;display:block}}
.chk{{display:inline-flex;align-items:center;gap:6px;cursor:pointer}} .chk input{{width:20px;height:20px;accent-color:var(--lime)}} .chk span{{font-weight:900;color:var(--lime)}}
.mini{{display:flex;gap:12px;background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:12px}} .mini p{{margin:2px 0 0;color:var(--mute);font-size:14px}}
input:focus-visible{{outline:2px solid var(--lime);outline-offset:2px}}
@media (max-width:480px){{.clip{{grid-template-columns:92px 1fr}} .say{{font-size:16px}}}}
</style>
<main class="wrap">
<header><h1>Rodatge <em>drop i cintilla</em></h1><p class="lead">Part 1: el Reel del drop sencer, 7 clips (~45 s), tot en una sessió perquè la llum sigui la mateixa. Part 2: el Reel de la cintilla sencer, en 7 clips i uns 42 s.</p></header>
<section><h2>Normes per a tots els clips</h2><div class="box"><ul>
<li><b>Càmera del darrere 1×</b> (la frontal grava en mirall), 4K 30 fps, <b>vídeo HDR desactivat</b>.</li>
<li><b>Bloqueja la llum:</b> mantén el dit sobre la teva cara fins que surti «Bloqueo AE/AF», i no ho toquis més durant aquell bloc.</li>
<li>Tots els clips d'un mateix Reel, <b>al mateix lloc, a la mateixa hora i amb la mateixa roba</b>. Mai a contrallum.</li>
<li>Micro al pit. Els primers plans els retallo jo del 4K.</li>
<li><b>Energia:</b> parla un 30 % més fort i més ràpid del que et sembla natural, comença cada frase ja en moviment i <b>somriu</b> el primer mig segon.</li>
<li><b>3 preses</b> de cada clip (normal, amb més energia, amb el gest exagerat). Si t'equivoques, 2 s de silenci i repeteix la frase sencera.</li>
<li><b>Un vídeo per clip</b>, adjuntats al xat (no al Drive).</li>
</ul></div></section>
<section><h2><span>1 ·</span> Drop · avui</h2><p class="sub">Polo de Tonus, paret blanca, sense bombetes grogues. Una sola bamba (D1 i D3). Grava tots els clips seguits.</p>
<ol class="clips">{drop}</ol></section>
<section><h2><span>2 ·</span> Cintilla · Reel sencer</h2><p class="sub">Roba de córrer, a l'aire lliure. Ombra uniforme o dia ennuvolat; si fa sol, que et toqui de cara o de costat, mai per darrere.</p>
<div class="box"><ul>
<li><b>Pla A:</b> trípode a 2,5 m, a l'altura del maluc, que es vegi de genolls amunt (cal veure la cuixa i el maluc).</li>
<li><b>Pla C:</b> mòbil a 50 cm del genoll, a la seva altura, només per al «El dolor surt aquí».</li>
</ul></div>
<h3>Clips, en l'ordre del Reel</h3><ol class="clips">{cint}</ol>
<h3>Recursos</h3><ul class="recs">{rec}</ul></section>
</main>'''
open("index.html", "w").write(page)
