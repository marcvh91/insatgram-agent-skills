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
ERR = [
 ("E1", "Ganxo", "0–3 s", "Pla A", img("ref_A.jpg", "Cintura amunt"),
  "Si comences a córrer, evita aquests <b>quatre errors</b>.",
  "Entra al pla caminant i para't. A «quatre errors», ensenya <b>4 dits</b> a càmera.",
  "Títol «4 ERRORS QUAN COMENCES A CÓRRER» a dalt"),
 ("E2", "Massa de cop", "3–11 s", "Pla A", img("ref_corre.jpg", "Recurs corrent"),
  "U: fer de cop una sortida molt més llarga del que estàs acostumat. Més d'un <b>deu per cent</b> per sobre de la teva sortida més llarga del mes ja augmenta el risc de lesió.",
  "Dit 1. A «molt més llarga», obre els braços.",
  "A mitja frase, recurs teu corrent pel passeig (ja el tinc) + «+10 % = més risc»"),
 ("E3", "Lesions d'abans", "11–17 s", "Pla B", img("ref_banc.jpg", "Foto al banc amb mà al genoll"),
  "Dos: oblidar-te de les <b>lesions que ja has tingut</b>. És el factor de risc que més es repeteix.",
  "Dits 2. Més a prop de càmera (pla B, 45°).",
  "Talls a les teves fotos al banc amb la mà al genoll i a l'Aquil·les (ja les tinc)"),
 ("E4", "Sense pla", "17–23 s", "Pla A", img("ref_detall.jpg", "Detall de mans"),
  "Tres: córrer <b>sense pla</b> i només un dia per setmana. Millor <b>dos o tres</b> sortides curtes.",
  "Dits 3. Després, grava el recurs R1 (llibreta).",
  "Recurs R1: escrivint el pla setmanal + «2–3 sortides/setmana»"),
 ("E5", "La bamba", "23–30 s", "Pla B", img("ref_detall.jpg", "Bamba a la mà"),
  "Quatre: triar la bamba pel <b>tipus de peu</b>. Cap estudi diu que funcioni. Tria la que et sigui <b>més còmoda</b>.",
  "Dits 4, amb una bamba a la mà. A «la més còmoda», somriu i abraça-la.",
  "«✗ Per tipus de peu · ✓ La més còmoda»"),
 ("E6", "Tancament", "30–34 s", "Pla A", img("ref_cta.jpg", "Caminant cap a càmera"),
  "Guarda't el vídeo i passa'l a qui està començant a córrer.",
  "Comença a 3 m i camina cap a càmera; acaba amb un somriure.",
  "«4 ERRORS» resum en una línia (sense contactes)"),
]
REC = [("R1", "Llibreta amb el pla", "Mòbil des de dalt (vista zenital). Escrius «Dl 20 min · Dc 20 min · Ds 30 min». 6–8 s."),
       ("R2", "Bamba de prop", "Primer pla de les mans girant la bamba i prement la sola. 5 s."),
       ("R3", "Dits a càmera", "Primer pla de la mà comptant 1, 2, 3, 4 (un clip per número, 2 s cadascun).")]
err = "".join(card(*c) for c in ERR)
rec = "".join(f'<li class="mini"><label class="chk"><input type="checkbox" id="r{i}"><span>{i}</span></label><div><b>{e(a)}</b><p>{e(b)}</p></div></li>' for i, a, b in REC)
page = f'''<title>Rodatge errors de principiant</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@500;600;800;900&display=swap">
<style>
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
.chk{{display:inline-flex;align-items:center;gap:6px;cursor:pointer}} .chk input{{width:20px;height:20px;accent-color:var(--lime)}} .chk span{{font-weight:900;color:var(--lime)}}
.mini{{display:flex;gap:12px;background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:12px}} .mini p{{margin:2px 0 0;color:var(--mute);font-size:14px}}
input:focus-visible{{outline:2px solid var(--lime);outline-offset:2px}}
@media (max-width:480px){{.clip{{grid-template-columns:92px 1fr}} .say{{font-size:16px}}}}
</style>
<main class="wrap">
<header><h1>Rodatge <em>4 errors quan comences a córrer</em></h1><p class="lead">Dc 2/12 a les 13:00 a la consulta · ~20 min · es publica dc 9/12. 6 clips parlant + 3 recursos curts. Els plans corrent i les fotos al banc ja els tinc del 26/11.</p></header>
<section><h2>Normes</h2><div class="box"><ul>
<li><b>Polo de Tonus</b>, paret blanca, <b>sense bombetes grogues</b>; tots els clips seguits, amb la mateixa llum.</li>
<li><b>Càmera del darrere 1×</b>, 4K 30 fps, <b>vídeo HDR desactivat</b>, <b>bloqueig AE/AF</b> sobre la teva cara.</li>
<li><b>Pla A:</b> trípode a 1,5 m, cintura amunt. <b>Pla B:</b> trípode a 1 m i girat 45°.</li>
<li>Teleprompter en un altre aparell just sota l'objectiu (reel «Errors»).</li>
<li>Energia +30 %, comença cada frase en moviment, 3 preses de cada. Un vídeo per clip, adjuntat al xat.</li>
</ul></div></section>
<section><h2><span>1 ·</span> Clips parlant</h2><ol class="clips">{err}</ol></section>
<section><h2><span>2 ·</span> Recursos (sense parlar)</h2><ul class="recs">{rec}</ul></section>
</main>'''
open("index.html", "w").write(page)
