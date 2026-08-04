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

**UI**
- Pantallas completas (menú, mapa, tienda, inventario, perfil, ranking, opciones, daily, buzón) sobre paleta *Light Bronze Forge*.
- 55 avatares de perfil (10 free + 41 premium + 4 VIP) con sistema WYSIWYG de marcos.
- Tienda de packs (Hero VIP + 10 packs de mundo + 5 packs de monedas) cableada end-to-end como stub local: la compra desbloquea avatars/frames/orb skins/backgrounds del mundo, activa perks VIP (+50 % monedas por partida, badge de ranking, cosméticos exclusivos) y refresca las cards con el checkmark de "poseído". Pendiente Google Play Billing para receipt validation.
- Recompensa diaria de 7 días con queue, racha con multiplicador y anti-cheat contra cambio de reloj.
- Cofre gratis por rewarded ad con loot table por rareza (SDK pendiente).
- Buzón de mensajes con backend Supabase (3 RPCs + fallback offline).
- Skins de orbe por mundo (shader universal con recolor por luma).
- Fondos temáticos del menú (2 variantes por mundo + clásico + VIP).

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
|  (22 globs) |                                   |  ProjectileBall  |
+-------------+                                   |  Boss            |
                                                  +------------------+
```

- **`AppRouter`** (`scripts/systems/app_router.gd`): monta pantallas, gestiona overlays modales y carga niveles.
- **`OrbexScreen`** (`scripts/ui/screens/orbex_screen.gd`): contenedor de pantallas. Secciones grandes extraídas en `scripts/ui/screens/sections/`.
- **`main.gd`** (`scripts/systems/main.gd`): controlador del nivel — cadena, combos, vida del jefe.
- **Autoloads** (22): `Notify`, `AchievementService`, `LevelProgress`, `Settings`, `Wallet`, `Inventory`, `DailyRewards`, `FreeReward`, `Quests`, `BackendConfig`, `RankingProvider`, `VersionGate`, `Anim`, `MusicPlayer`, `Sfx`, `OrbSkins`, `ProfileFrames`, `Analytics`, `SaveEpoch`, `CloudSave`, `KeyboardDismiss`, `GoogleSignIn`.

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
- **UI**: menú, mapa, tiendas, inventario, perfil (55 avatares), ranking online, daily, misiones diarias y semanales, buzón, regalo gratis.
- **Ranking**: Supabase con auth anónima + RLS + perfiles públicos + anti-trampas.
- **Cloud save**: copia del progreso en Supabase + códigos de transferencia entre dispositivos (un solo uso, 72 h, con lápida anti-duplicación).
- **Version gate**: dos umbrales en servidor (aviso y bloqueo) para sacar de circulación una build rota sin publicar nada. Falla en abierto.
- **Telemetría de beta**: end-to-end con retention 90 días automatizada y queries de calibración listas.
- **Base de datos**: endurecida (RLS optimizada, caps + rate limit, RPC de borrado GDPR).
- **Audio**: música + SFX en los 10 mundos.
- **i18n**: 10 idiomas con auto-detect y cambio en caliente.
- **Mobile/APK**: landscape, touch validado, VRAM texture compression dual (desktop + Android).

---

## Roadmap pendiente

- [ ] Haptic feedback en disparos críticos / combos.
- [ ] Configuración de niveles desde JSON (`data/levels/`).
- [ ] Conectar Google Play Billing a los packs.
- [ ] Google Sign-In: código listo, pendiente de que funcione en dispositivo. Al activarlo hay que actualizar la política de privacidad (ver tabla en [Política de privacidad](#política-de-privacidad)).
- [ ] AdMob para el cofre gratis. Mismo aviso: toca política + `meta description`.
- [ ] Editor de niveles ampliado (paleta de patrones).
- [ ] Revisar traducciones con hablantes nativos (las 9 no-inglesas están asistidas).

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

Pendientes para subir a Play Store (no bloquean desarrollo — hoy se exporta APK debug a propósito):

- **Build**: AAB + Release, keystore de release, Play App Signing.
- **Cumplimiento**: política de privacidad, Data Safety, IARC, público objetivo (13+). La política real vive en [`PRIVACY.md`](PRIVACY.md) de este repo y se sirve en [orbex.aleixaj.com/privacy](https://orbex.aleixaj.com/privacy). El flujo "delete my data" ya está implementado in-app.
- **Backend**: hardening completado. `players.role` default = `'user'` en prod (verificado 2026-07-18); las 6 cuentas de dev se mantienen como `'admin'` para promo/tests, nuevas altas caen en `'user'`.
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
- Política de privacidad (`/privacy` → `privacy/index.html`): 11 secciones + resumen destacado, con GDPR/RGPD compliance.
- **Bilingüe EN (default) / ES** — toggle en el header, persistencia en `localStorage`, ambos idiomas viven en el mismo HTML mediante `<span data-lang="en|es">` con CSS que oculta el inactivo. Actualiza también `<title>` y `<meta description>`.
- **Tema claro/oscuro** — auto por `prefers-color-scheme` en la primera visita, persistente después.
- **Tráiler** — embed de YouTube (`youtube-nocookie.com`) en modal. El `<iframe>` nace **sin `src`**: no se hace ninguna petición a Google hasta que el usuario pulsa "Ver tráiler", y al cerrar el modal se le quita el `src` para detener la reproducción. Es el patrón click-to-load, así que la landing no necesita banner de cookies.
- **Navegación móvil** — por debajo de 860 px (el mismo breakpoint donde `.navlink` desaparece) el JUGAR de la barra se oculta y aparece una hamburguesa que despliega un panel con JUGAR en dorado arriba y los seis enlaces debajo. Se cierra al elegir enlace, al tocar fuera de la cabecera, con Escape y al pasar a escritorio. ⚠️ Las reglas que ocultan `.nav-burger` y `.nav-play-top` van **cualificadas con `.nav-header`** a propósito: `.icon-btn` y `.btn-play-nav` se declaran más abajo en la hoja con la misma especificidad y ganarían por orden de aparición.
- **A11y**: `aria-label` en todos los botones-icono, `aria-expanded` / `aria-controls` en la hamburguesa, modales con `role="dialog"` y cierre por Escape, respeta `prefers-reduced-motion`.
- **SEO**: Open Graph + Twitter Card completos, canonical, `hreflang` alternates, `sitemap.xml`, `robots.txt`. HTML estático — Google/Twitter ven el contenido en la respuesta inicial, no en un shell hidratado.

### Política de privacidad

Vive en dos ficheros que hay que editar **siempre a la vez** o divergen: `PRIVACY.md` (source of truth bilingüe) y `privacy/index.html` (la página servida). Cada uno lleva el texto EN y ES completo.

Al tocarla, subir la fecha de "Última actualización" en los dos y en los dos idiomas — son cuatro sitios.

**Tiene que ir por delante de lo que hace el juego, no por detrás.** Lo que está pendiente y en qué commit toca:

| Cuándo | Qué cambia |
|---|---|
| Al activar **Google Sign-In** en dispositivo | El resumen dice "no pedimos tu correo" y §2.5 lista "Email" entre lo que NO se recoge. Al vincular, `auth.identities` guarda el email: las dos frases pasan a ser falsas. También §4 ("Nadie más" ve tus datos). |
| Al activar **AdMob** (`ADS_AVAILABLE = true`) | El resumen dice "no mostramos anuncios" y §2.5 lista el ID publicitario de Android (AAID/GAID) entre lo que no se recoge. Además §3 excluye la publicidad como finalidad. Y en `index.html`, la `meta description` dice "sin anuncios agresivos" (3 sitios: línea 7 y las dos entradas de `META`). |
| Al activar **Play Billing** (`BILLING_AVAILABLE = true`) | Revisar las menciones a "compras" de §7, que hoy se refieren a packs comprados con monedas del juego. |

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
| `#PLACEHOLDER-x` | Perfil de X (o quitar el botón) |
| `assets/images/placeholders/google-play-badge.png` | Badge oficial de Google Play |
| `assets/images/placeholders/qr.png` | QR real a la ficha de Play |
| `assets/images/placeholders/og-image.png` | Imagen para social share (1200×630) |
| `assets/images/placeholders/favicon-*.png` | Favicons definitivos |

Ya no se usan (se pueden borrar): `placeholders/hero-gameplay.png` y `placeholders/gameplay-1..3.png` — la galería tira de `assets/images/screenshots/`.

**Peso de las capturas**: las 8 de `screenshots/` suman ~4,4 MB (600 KB cada una, calidad ~95). Van con `loading="lazy"` y la galería está al final de la página, así que no afectan a la primera pintada, pero recomprimir a calidad ~80 las dejaría en ~150 KB sin diferencia visible al tamaño en que se muestran.

⚠️ **`screenshots/7.jpg` está desactualizada**: el ranking muestra pestañas de nivel 1-5 y el build actual tiene 8 niveles por mundo. Hay que recapturarla (y revisar si la misma imagen está subida a la ficha de Play).
