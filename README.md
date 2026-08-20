# Orbex

![Godot](https://img.shields.io/badge/Godot-4.6-478CBF?style=for-the-badge&logo=godotengine&logoColor=white&labelColor=2D2D2D)
![GDScript](https://img.shields.io/badge/GDScript-static_typing-355170?style=for-the-badge&logo=godotengine&logoColor=white&labelColor=2D2D2D)
![Android](https://img.shields.io/badge/Android-APK-3DDC84?style=for-the-badge&logo=android&logoColor=white&labelColor=2D2D2D)
![Resolution](https://img.shields.io/badge/Base-1280x720-c08820?style=for-the-badge&labelColor=2D2D2D)
![Pixel Art](https://img.shields.io/badge/Style-Pixel_Art-efe3cf?style=for-the-badge&labelColor=2D2D2D)

**Orbex** es un juego pixel-art de acción y puntería para Android, desarrollado en **Godot 4.6** por una sola persona. Mecánica tipo *Zuma* con boss: lanzas orbes desde el centro, encadenas combos de 3+ del mismo color y vacías la vida del jefe antes de que la cadena hostil llegue al final del recorrido.

10 mundos × 8 niveles ambientados en épocas históricas (dinosaurios → espacio). Proyecto a la vez juego y *showcase* técnico: motor de cadena propio, plugin de editor de paths, sistema de profundidad sin recortar PNGs, UI nativa completa y backend de ranking online.

> 🌐 **Este repositorio (`orbex-web`) contiene la landing page pública** del juego, desplegada en **[orbex.aleixaj.com](https://orbex.aleixaj.com)**. Es un sitio estático (HTML + CSS + JS vanilla, cero build), bilingüe EN/ES y con tema claro/oscuro. Detalles técnicos al final del documento, en la sección [Landing page](#landing-page-orbex-web--este-repo).
>
> El código del **juego** (Godot 4.6, GDScript) vive en el repositorio principal — lo que sigue documenta ese proyecto.

---

## Tech stack

| Categoría | Detalle |
|---|---|
| Motor | Godot 4.6 (Mobile / `gl_compatibility`) |
| Lenguaje | GDScript tipado estático con `class_name` |
| Plataforma | Android landscape, base 1280×720 |
| Backend | Supabase (PostgreSQL + PostgREST + Auth anónima) |
| Persistencia local | `user://*.save` |
| Editor tooling | `EditorPlugin` custom (`@tool` + `_forward_canvas_gui_input`) |

---

## Cómo probarlo

1. Abre Godot 4.6 e importa la carpeta `orbex/`.
2. El plugin **Orbex Path Editor** viene activado por defecto.
3. Ejecuta `res://scenes/main.tscn` (F5).
4. Clic / toque para apuntar y disparar.

> El `.gitignore` excluye `.godot/`, `builds/`, APKs y `export_presets.cfg`.

---

## Características principales

**Gameplay**
- Motor de cadena propio: avance por `path_progress`, inserción con `lerp`, snap-back, merge con shockwave, multi-cadena por nivel.
- Sistema de profundidad sin recortar PNGs: `FrontMask` (polígonos), tótem universal (bola de cristal, 12 frames) que se ilumina al acercarse la cadena, portales `_Tp` con fade.
- Personaje por mundo con 8 direcciones y profundidad por pose.
- 9 power-ups consumibles (3 slots equipables) + combate de jefe (corazones + ataque propio por mundo).
- Jefes multi-fase (2-3 fases) con transición de rotura de pantalla.
- Bonus pickups deterministas (aparición por bolas destruidas del pool del nivel, sin RNG, sin respawn) para mantener el ranking como habilidad pura.
- **Modo Supervivencia**: cualquier nivel ya superado, con el pool infinito y sin objetos, hasta que la cadena te alcanza. Rampa de velocidad normalizada por nivel y tabla propia.
- **Desafío semanal**: un nivel sorteado en servidor, el mismo para todo el mundo, jugado sin objetos y aislado del resto del progreso. Tabla propia y premios por buzón.
- **Asistencia invisible**: tras varias derrotas seguidas en el mismo nivel, la cadena afloja (o el jefe espacia sus ataques) sin anunciarlo y sin modo fácil que elegir.

**UI**
- Pantallas completas (menú, mapa, tienda, inventario, perfil, ranking, opciones, daily, buzón) sobre paleta *Light Bronze Forge*.
- 103 avatares de perfil (10 free + 41 de mundo + 4 VIP + 40 exclusivos + 8 del evento de temporada) con sistema WYSIWYG de marcos, más 24 marcos, 42 skins de orbe y 45 fondos de menú.
- Tienda de packs (Hero VIP + 10 packs de mundo + 5 packs de monedas) cableada end-to-end como stub local: la compra desbloquea avatars/frames/orb skins/backgrounds del mundo, activa perks VIP (+50 % monedas por partida, badge de ranking, cosméticos exclusivos) y refresca las cards con el checkmark de "poseído". Pendiente Google Play Billing para receipt validation.
- Recompensa diaria de 7 días con queue, racha con multiplicador y anti-cheat contra cambio de reloj.
- Cofre gratis por rewarded ad con loot table por rareza. **SDK de AdMob integrado** (unidades de prueba); los cuatro puntos de rewarded y el intersticial pasan por el autoload `Ads` y por ningún otro sitio.
- Buzón de mensajes con backend Supabase (3 RPCs + fallback offline).
- Skins de orbe por mundo (shader universal con recolor por luma).
- Fondos temáticos del menú (2 variantes por mundo + clásico + VIP + exclusivos).
- **Eventos de temporada**: ventana de fechas con divisa propia que caduca, catálogo de cosméticos exclusivos y fase de liquidación para gastar lo ganado.
- **Amigos** (alta unilateral, notificaciones y tabla filtrada), **misiones** diarias y semanales con reroll, y **69 logros**.
- **Panel de admin dentro del juego** (admin-only, verificado en servidor): buscador de jugadores, ficha completa, sanciones y herramientas de desarrollo.

**Herramientas y arquitectura**
- Plugin **Orbex Path Editor**: Shift+clic para trazar paths, sufijos especiales (`_Tp`, `_NoHook`, `_Front`, `_FrontMax`, `_Sprint`).
- Backend Supabase: leaderboard, perfiles públicos, auth anónima, RLS, anti-trampas con caps en servidor, sistema de roles.
- **Telemetría** (autoload `Analytics`): payload rico por partida a Supabase con caps + rate limit anti-bot; toggle en Opciones por GDPR. Con datos beta reales, `percentile_cont` sobre `level_attempts.score` recalibra los star_thresholds.
- **Cron jobs**: purga automática a 90 días de `level_attempts` + roll-up diario de DAU.
- **GDPR "delete my account"**: RPC + cascade + limpieza local → next launch parece primera instalación.
- Audio: música por mundo (lazy load + caché), menú con 4 temas en rotación, pool polifónico de SFX.
- **i18n** en 10 idiomas con auto-detección del locale del sistema.

---

## Arquitectura

```
+-------------+     +----------------------+     +------------------+
|  AppRouter  |---->|  OrbexScreen (UI)    |---->|  Nivel (main.gd) |
| (main.tscn) |     |  menú/zona/nivel     |     |  + HUD overlay   |
+-------------+     +----------------------+     +------------------+
       |                                                  |
       v                                                  v
+-------------+                                   +------------------+
|  Autoloads  |   notify / save / unlock          |  ChainBall x N   |
|  (26 globs) |                                   |  ProjectileBall  |
+-------------+                                   |  Boss            |
                                                  +------------------+
```

- **`AppRouter`** (`scripts/systems/app_router.gd`): monta pantallas, gestiona overlays modales y carga niveles.
- **`OrbexScreen`** (`scripts/ui/screens/orbex_screen.gd`): contenedor de pantallas. Secciones grandes extraídas en `scripts/ui/screens/sections/`.
- **`main.gd`** (`scripts/systems/main.gd`): controlador del nivel — cadena, combos, vida del jefe.
- **Autoloads** (26): `Notify`, `AchievementService`, `LevelProgress`, `Settings`, `Wallet`, `Inventory`, `DailyRewards`, `FreeReward`, `Quests`, `BackendConfig`, `RankingProvider`, `Challenge`, `SummerEvent`, `VersionGate`, `Anim`, `MusicPlayer`, `Sfx`, `OrbSkins`, `ProfileFrames`, `Analytics`, `SaveEpoch`, `CloudSave`, `KeyboardDismiss`, `GoogleSignIn`, `Ads`, `Purchases`.
  > `Ads` y `Purchases` son **puertas**: el SDK entra por ahí y solo por ahí. Ninguna pantalla habla con el plugin — se pide `await Ads.request_reward(placement)` y punto. `Purchases` sigue vacío hasta que entre Play Billing.

> Para detalles de mecánicas, balanceo, sistemas y "dónde está qué" → `CLAUDE.md` en el repo del juego.

---

## Estructura del proyecto

```
orbex/
|-- addons/orbex_path_editor/     Plugin de editor para trazar paths
|-- assets/                       arte, audio, fuentes, sprites de UI
|-- scenes/
|   |-- entities/                 boss/ player/ totem/ bonus/ + chain_ball, projectile_ball
|   |-- levels/NN_zona/           <zona>_01..08.tscn
|   |-- ui/                       components/ screens/ overlays/ hud.tscn
|   `-- main.tscn
|-- scripts/
|   |-- entities/                 chain_ball, player, boss, front_mask, totem...
|   |-- systems/                  app_router, main, autoloads, sql/
|   `-- ui/                       components/ overlays/ screens/sections/
|-- design/                       docs internas (no se publican)
|-- project.godot
|-- README.md
`-- CLAUDE.md                     mapa de navegación del repo
```

---

## Estado actual

- **Mecánica**: completa (cadena, inserción, combos, multi-cadena, portales, profundidad, jefes multi-fase).
- **Contenido**: 10 mundos, **80 niveles** + tutorial + 6 fases extra de jefe.
- **Personajes**: los 10 mundos con 8 direcciones y profundidad por pose.
- **UI**: menú, mapa, tiendas, inventario, perfil (103 avatares), ranking online, daily, misiones diarias y semanales, buzón, cofre gratis, amigos, eventos y panel de admin.
- **Modos**: campaña, **supervivencia** (por nivel, al superarlo) y **desafío semanal** (nivel sorteado en servidor, con premios).
- **Ranking**: Supabase con auth anónima + RLS + perfiles públicos + anti-trampas.
- **Cloud save**: copia del progreso en Supabase + códigos de transferencia entre dispositivos (un solo uso, 72 h, con lápida anti-duplicación).
- **Version gate**: dos umbrales en servidor (aviso y bloqueo) para sacar de circulación una build rota sin publicar nada. Falla en abierto.
- **Telemetría de beta**: end-to-end con retention 90 días automatizada y queries de calibración listas.
- **Base de datos**: endurecida (RLS optimizada, caps + rate limit, RPC de borrado GDPR, grants columnares, moderación de cuentas).
- **Monetización**: SDK de AdMob integrado con unidades de prueba y consentimiento UMP; Play Billing pendiente (`BILLING_AVAILABLE = false`), así que hoy no se cobra nada dentro de la app.
- **Identidad**: sesión anónima por dispositivo, vinculación opcional con Google (conservando el mismo `auth.uid()`) y códigos de transferencia.
- **Audio**: música + SFX en los 10 mundos.
- **i18n**: 10 idiomas con auto-detect y cambio en caliente.
- **Mobile/APK**: landscape, touch validado, VRAM texture compression dual (desktop + Android).

---

## Roadmap pendiente

- [ ] Conectar Google Play Billing a los packs (Fase 3). Al activarlo hay que tocar §4 de la política — ver la tabla de [Política de privacidad](#política-de-privacidad).
- [ ] AdMob: flip a unidades reales (`USE_TEST_AD_UNITS = false`) y repaso del match rate en el panel.
- [ ] Haptic feedback en disparos críticos / combos.
- [ ] Configuración de niveles desde JSON (`data/levels/`).
- [ ] Editor de niveles ampliado (paleta de patrones).
- [ ] Revisar traducciones con hablantes nativos (las 9 no-inglesas están asistidas).

Hecho recientemente:

- [x] Google Sign-In funcionando en dispositivo (2026-08-04).
- [x] AdMob integrado con unidades de prueba y flujo de consentimiento UMP (2026-08-20).
- [x] Política de privacidad al día con anuncios, Google Sign-In, modos nuevos y base legal (2026-08-20).

---

## Localización (i18n)

10 idiomas: **EN** (base), **ES**, **CA**, **pt-BR**, **FR**, **IT**, **DE**, **JA**, **KO**, **RU**.

- Fuente única: `assets/i18n/translations.csv` (`keys,en,es,ca,pt_BR,...`).
- Compilado a `.translation` por el importer de Godot y registrado vía `[internationalization]` en `project.godot`. **El CSV no se lee en runtime**.
- Auto-detect en primer arranque (`OS.get_locale()`, fallback a EN). Selector con banderas en Opciones + name picker.
- Cambio en caliente vía `Settings.set_language()` → señal `language_changed` → reconstrucción de la pantalla activa. Labels en `.tscn` con `auto_translate_mode = ALWAYS` se retraducen solas.
- Persistencia por dispositivo en `user://settings.save`.

**Añadir un idioma**: nueva columna en el CSV + entrada en `LANGUAGES` (`settings.gd`) + path en `project.godot`.

**Añadir una clave**: fila al CSV + `tr("MI_CLAVE")` en el código.

---

## Publicación en Google Play

El juego está en **beta cerrada** en Play (AAB de release firmado con Play App Signing). Lo que queda para producción:

- **Cumplimiento**: la política real vive en [`PRIVACY.md`](PRIVACY.md) de este repo y se sirve en [orbex.aleixaj.com/privacy](https://orbex.aleixaj.com/privacy). El flujo "delete my data" ya está implementado in-app.
- ⚠️ **Data Safety pendiente de repasar.** Desde que el SDK de AdMob entró en la build (2026-08-20) la app recoge el identificador publicitario y Google Sign-In guarda un correo cuando el jugador vincula. La política ya lo declara; **la declaración de Play Console tiene que decir lo mismo o rechazan la actualización**.
- **IARC** y público objetivo (13+), con la clasificación al día tras añadir publicidad.
- **Backend**: hardening completado. `players.role` default = `'user'` en prod (verificado 2026-08-20); las cuentas de staff se mantienen como `'admin'` para moderación y pruebas, y las nuevas altas caen en `'user'`.
- **Ficha**: icono 512×512, gráfico destacado 1024×500, capturas landscape, textos EN/ES en `design/STORE_TEXTS.md` del repo del juego. Idioma primario: **English (US)**.

Permisos mínimos ya validados (`INTERNET` + `ACCESS_NETWORK_STATE`), `targetSdk 36` / `minSdk 24`, solo `arm64-v8a`.

---

## Autoría

Proyecto personal de **Aleix**. Diseño, código, arte de UI y level design por una sola persona — pensado como showcase técnico y como excusa para construir un juego completo (gameplay, UI, herramientas, persistencia, plataforma) desde cero en un motor open source.

Sugerencias y revisiones de código bienvenidas.

- Email: [playorbex@gmail.com](mailto:playorbex@gmail.com)
- Web: [aleixaj.com](https://aleixaj.com)

---

## Landing page (`orbex-web` — este repo)

Landing pública del juego, desplegada en **[orbex.aleixaj.com](https://orbex.aleixaj.com)**. Ese subdominio también es la URL de referencia de la política de privacidad exigida por Google Play.

### Stack

HTML5 + CSS con custom properties + JS vanilla en un solo `<script>` inline. **Cero build**, **cero dependencias en runtime**. Ship the folder.

- Landing (`index.html`): 8 secciones (hero, el juego, 10 mundos, 10 jefes, features, galería, 10 idiomas, descarga, footer). La galería son las 8 capturas del juego en tarjetas 16:9 con lightbox; el tráiler tiene su propio botón en el hero.
  - **Features son 9 tarjetas en una rejilla `auto-fit`**, o sea 3×3 exactas en escritorio. Añadir o quitar una descuadra la última fila: van de tres en tres.
- Política de privacidad (`/privacy` → `privacy/index.html`): 14 secciones + resumen destacado, con GDPR/RGPD compliance.
- **Bilingüe EN (default) / ES** — toggle en el header, persistencia en `localStorage`, ambos idiomas viven en el mismo HTML mediante `<span data-lang="en|es">` con CSS que oculta el inactivo. Actualiza también `<title>` y `<meta description>`.
- **Tema claro/oscuro** — auto por `prefers-color-scheme` en la primera visita, persistente después.
- **Tipografía** — la misma jerarquía que el juego, vía tres variables en `:root`: `--f-display` (**Lilita One**) para títulos, botones y etiquetas, `--f-body` (**Space Grotesk**) para el cuerpo, y `--f-pixel` (**Press Start 2P**) reservada a los números — contadores del hero y dorsales de las tarjetas de mundo y de jefe. Es lo que hace el juego, donde `OrbexUI` cambia el árbol entero a Lilita One y la pixel solo sobrevive en el HUD de partida (marcador, combo, vida del jefe). ⚠️ **Lilita One tiene un único peso**: los encabezados vienen en bold por defecto del navegador, así que hay una regla `h1,h2,h3,h4{font-weight:400}` para que no se sintetice la negrita. Los encabezados que sí van en negrita son los de Space Grotesk y declaran su peso inline, que gana a esa regla. Y como Lilita se lee más pequeña que la pixel al mismo tamaño, los `font-size` heredados van escalados hacia arriba (~×1.4 en textos pequeños, ~×1.35 en titulares) — el juego hace lo mismo con un ×1.5.
- **Tráiler** — embed de YouTube (`youtube-nocookie.com`) en modal. El `<iframe>` nace **sin `src`**: no se hace ninguna petición a Google hasta que el usuario pulsa "Ver tráiler", y al cerrar el modal se le quita el `src` para detener la reproducción. Es el patrón click-to-load, así que la landing no necesita banner de cookies.
- **Navegación móvil** — por debajo de 860 px (el mismo breakpoint donde `.navlink` desaparece) el JUGAR de la barra se oculta y aparece una hamburguesa que despliega un panel con JUGAR en dorado arriba y los seis enlaces debajo. Se cierra al elegir enlace, al tocar fuera de la cabecera, con Escape y al pasar a escritorio. ⚠️ Las reglas que ocultan `.nav-burger` y `.nav-play-top` van **cualificadas con `.nav-header`** a propósito: `.icon-btn` y `.btn-play-nav` se declaran más abajo en la hoja con la misma especificidad y ganarían por orden de aparición.
- **A11y**: `aria-label` en todos los botones-icono, `aria-expanded` / `aria-controls` en la hamburguesa, modales con `role="dialog"` y cierre por Escape, respeta `prefers-reduced-motion`.
- **Rendimiento** — ver el apartado dedicado más abajo.
- **SEO**: Open Graph + Twitter Card completos, canonical, `hreflang` alternates, `sitemap.xml`, `robots.txt`. HTML estático — Google/Twitter ven el contenido en la respuesta inicial, no en un shell hidratado.

### Rendimiento

El tráiler se veía a tirones y el motivo no era el vídeo, sino el compositor saturado mientras reproduce. Lo que se hizo, y **por qué no conviene deshacerlo**:

- **`.modal-backdrop` no lleva `backdrop-filter`.** Un desenfoque a pantalla completa se recalcula cada vez que cambia algo por debajo, y con el tráiler abierto eso es cada fotograma. Peor todavía: `#orbex-trail` está en z-index 90 y el modal en 100, así que cada partícula del rastro nacía *debajo* del desenfoque y disparaba un reblur de toda la ventana ~35 veces por segundo. Se compensa con la opacidad del fondo (0,93).
- **`body.modal-open` congela lo decorativo** mientras hay un modal: oculta el rastro (y corta su generación), apaga el `backdrop-filter` de la cabecera y pausa `logoPulse` y `forgeShift`. Esas dos animan `filter` y `background-position`, que repintan en vez de componer, y corrían siempre aunque estuvieran fuera de pantalla.
- La clase la recalcula `syncModalOpen()` mirando si queda **algún** `.modal-backdrop.open`. Escape llama a los dos cierres, y uno no puede descongelar lo que el otro sigue usando.
- **El parallax del hero escribe una vez por frame** (`requestAnimationFrame`) y no hace nada por debajo del hero. El evento `scroll` se dispara más veces que fotogramas hay.
- Las partículas del rastro se limpian con `animationend`, no con un `setTimeout` cada una.
- Todas las imágenes `loading="lazy"` llevan `decoding="async"` para que decodificar las capturas no bloquee el hilo principal al entrar en la galería.

### Política de privacidad

Vive en dos ficheros que hay que editar **siempre a la vez** o divergen: `PRIVACY.md` (source of truth bilingüe) y `privacy/index.html` (la página servida). Cada uno lleva el texto EN y ES completo.

Al tocarla, subir la fecha de "Última actualización" en los dos y en los dos idiomas — son cuatro sitios.

⚠️ **La política ya no se puede regenerar desde `_source/Orbex Privacy.dc.html`.** Ese fichero es el canvas de diseño original y se quedó en la versión del 2026-08-04; además está en `.gitignore`, así que ni se versiona ni se despliega. La fuente de verdad son los dos ficheros de arriba.

**Tiene que ir por delante de lo que hace el juego, no por detrás**, y la versión del 2026-08-04 demostró lo fácil que es que se quede detrás: siguió diciendo "no pedimos tu correo" y "no mostramos anuncios" durante dos semanas en las que Google Sign-In ya vinculaba correos y el SDK de AdMob ya estaba dentro de la build. Las dos frases eran justo las dos que Google Play contrasta con la declaración de Data Safety.

⚠️ **Al tocar la política hay que revisar también la declaración de Data Safety de Play Console.** Las dos tienen que decir lo mismo; si divergen, Play rechaza la actualización.

Al día desde el 2026-08-20 (14 apartados). Lo que cubre y que no estaba antes: publicidad y AdMob (§3), vinculación con Google (2.2), amigos, desafío semanal y supervivencia (2.1), economía y tiempo de app dentro de la telemetría opcional (2.5), base legal por finalidad (§5), compras (§4) y sanciones de cuenta (§11).

Lo que queda pendiente:

| Cuándo | Qué cambia |
|---|---|
| Al pasar AdMob a **unidades reales** (`USE_TEST_AD_UNITS = false`) | Nada en el texto — §3 ya está redactado para los dos casos. Sí hay que repasar la Data Safety de Play. |
| Al activar **Play Billing** (`BILLING_AVAILABLE = true`) | §4 dice "Orbex no vende nada dentro de la app": pasa a ser falso. Hay que describir qué recibimos de Google Play y revisar las menciones a compras de §9. |
| Al añadir un **evento de temporada nuevo** | 2.1 nombra la divisa del evento de forma genérica a propósito; comprobar que sigue siendo cierto. |
| Si alguna vez se recoge algo **nuevo del jugador** | La regla es que 2.1/2.5 lo listen ANTES de que la build salga. Los apartados que más envejecen son 2.1 (tablas nuevas) y 2.5 (telemetría nueva). |

### Estructura

```
orbex-web/
├── index.html               landing (bilingüe)
├── privacy/index.html       /privacy — política real
├── PRIVACY.md               source-of-truth bilingüe
├── assets/
│   └── images/
│       ├── orbex-title.png  wordmark
│       ├── zones/           10 escudos de mundo
│       ├── bosses/          10 retratos verticales de jefe
│       ├── orbs/            5 orbes
│       ├── icons/           UI icons
│       ├── avatars/         3 avatares
│       ├── bg/              3 fondos de mundo
│       ├── screenshots/     8 capturas reales del juego (1280×720)
│       ├── flags/           10 banderas de idioma
│       └── placeholders/    ⚠️ sustituir antes de lanzar
├── robots.txt sitemap.xml
├── _headers _redirects       Cloudflare Pages / Netlify
├── netlify.toml vercel.json
└── README.md                 este archivo
```

### Probar localmente

```bash
python -m http.server 8000
# → http://localhost:8000/   y   http://localhost:8000/privacy/
```

### Deploy

Cualquier host estático. Recomendado **Cloudflare Pages**: framework "None", output `/`, `_headers` + `_redirects` se aplican automáticamente. Alternativas con config incluida: **Netlify** (`netlify.toml`) y **Vercel** (`vercel.json`).

Custom domain `orbex.aleixaj.com` apunta al proyecto de Pages vía CNAME automático (dominio ya en Cloudflare).

### Placeholders a sustituir antes de anunciar

Buscar en `index.html`:

| Placeholder | Sustituir por |
|---|---|
| `#PLACEHOLDER-play-store` | URL real de Google Play (**4 apariciones**: nav, panel móvil, hero, descarga) |
| `#PLACEHOLDER-terminos` | Página de términos de uso |
| `assets/images/placeholders/google-play-badge.png` | Badge oficial de Google Play |
| `assets/images/placeholders/qr.png` | QR real a la ficha de Play |
| `assets/images/placeholders/og-image.png` | Imagen para social share (1200×630) |
| `assets/images/placeholders/favicon-*.png` | Favicons definitivos |

Ya no se usan (se pueden borrar): `placeholders/hero-gameplay.png` y `placeholders/gameplay-1..3.png` — la galería tira de `assets/images/screenshots/`.

**Peso de las capturas**: las 8 de `screenshots/` están recomprimidas a **calidad 85** y suman ~2,2 MB (venían a ~4,4 MB con calidad ~95). Los originales sin recomprimir se conservan fuera del repo, así que se pueden regenerar. Si se sustituye alguna, pasarla por la misma calidad antes de commitear.

⚠️ **`screenshots/7.jpg` está desactualizada**: el ranking muestra pestañas de nivel 1-5 y el build actual tiene 8 niveles por mundo. Hay que recapturarla (y revisar si la misma imagen está subida a la ficha de Play).
