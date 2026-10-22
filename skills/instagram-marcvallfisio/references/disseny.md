# Diseño de diapositivas — estilo elegido: «Foto a sang» (negro + verde lima)

- Plantilla: `templates/carrusel_presentacio.html` del repo (HTML → PNG con Playwright/Chromium; 1080×1350 carrusel, 1080×1920 story).
- Cada diapositiva lleva **foto propia a sangre** con sombreado oscuro de arriba a abajo (rgba(8,12,15,.35) → .92). Texto abajo.
- Colores: negro `#0B0F12`, blanco, gris claro `#D6DEE3` para texto secundario, **acento verde lima `#D4FF3F`**.
- Tipografía: Inter Display Black en **mayúsculas** para títulos; Inter para texto. Kicker en lima, mayúsculas.
- Listas con números en lima; tarjetas translúcidas (blanco 10 %) para bloques; caja de WhatsApp en lima con texto negro.
- Pie: @marcvallfisio + puntos de progreso (activo en lima).
- Stories en vídeo: capa PNG transparente sobre vídeo propio (ffmpeg overlay), texto arriba y abajo, centro libre para stickers.
- Comprobar antes de entregar: legibilidad sobre la foto y que nada se solape con el pie.
- Alternativas descartadas por Marc: azul noche + naranja, crema + verde clínico.

## Estructura fija del texto de la publicación (catalán)
1. Gancho en la primera línea (se ve antes de «més»).
2. 2–3 líneas de contenido, una idea por línea.
3. «Passo consulta a Tonus Fisioteràpia, a Tarragona. Si vols cita amb mi, escriu-me directament per WhatsApp 📲 627 148 092 (també a la bio).»
4. Pregunta para comentarios con 👇.
5. 5–7 hashtags al final, incluyendo #marcvallfisio.
Más: ubicación Tarragona, texto alternativo por diapositiva, post a las 13:30 y story a las 20:30.

## Reels sin grabar
Marc prefiere no grabar: los Reels se montan con diapositivas verticales 1080×1920 (plantilla `templates/reel_vertical.html`) con zoom lento + clips de sus vídeos, unidos con ffmpeg (~20 s). Texto entre y=700 y y=1550 (zona segura). Marc añade la música en la app. Explicarle siempre en lenguaje sencillo, sin jerga.

## Story «Hores lliures»
Plantilla per anunciar hores disponibles: `templates/story_hores_lliures.html` (pàgina publicada i fixada a claude.ai: https://claude.ai/artifact/4t9H3BScyi9jaQhnv5HPHr). Fons negre amb rellotge verd llima que marca la primera hora, etiqueta «Agenda a Tonus Fisioteràpia», títol «Tinc 1 hora lliure / 2 hores lliures», dia + data, hores en caixes llima, a baix dues caixes petites: «WhatsApp 627 148 092 · Amb mi directament» i «Clínica Tonus Fisioteràpia 601 983 214 · Demana per mi» (telèfon de Tonus, sempre amb «demana per mi»). Sense foto i sense frase extra (Marc ho va demanar així).
