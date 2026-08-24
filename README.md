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

HTML5 + CSS con custom properties + JS vanilla en un solo `<script>` inline. **Cero build**, **cero dependencias en runtime** y, desde el 2026-08-21, **cero peticiones a terceros**: la página entera se sirve desde el propio dominio. Ship the folder.

- Landing (`index.html`): 11 secciones — hero, el juego, **cómo se juega**, 10 mundos, 10 jefes, features, galería, **detrás del juego**, 10 idiomas, **FAQ** y descarga, más el footer. La galería son las 8 capturas del juego en tarjetas 16:9 con lightbox navegable; el tráiler tiene su propio botón en el hero.
  - **Features son 9 tarjetas en una rejilla `auto-fit`**, o sea 3×3 exactas en escritorio. Añadir o quitar una descuadra la última fila: van de tres en tres.
  - **Los fondos de sección ALTERNAN** `--paper` / `--paper2` de arriba abajo. Al insertar una sección hay que mirar las dos vecinas, o quedan dos tonos iguales seguidos y la página pierde el ritmo. Entre bloques hay además un separador de cinco orbes (`.chain-sep`), puro CSS.
> ⚠️ **El bloque `FAQPage` del JSON-LD tiene que decir lo MISMO que las tarjetas de la página.** Google exige que la respuesta marcada sea visible; si se quita una pregunta del HTML y se olvida el JSON-LD, el buscador sigue enseñando una respuesta que ya no existe. Pasó al retirar la de los anuncios.

- Política de privacidad (`/privacy` → `privacy/index.html`): 14 secciones + resumen destacado, con GDPR/RGPD compliance.
- **Bilingüe EN (default) / ES** — toggle en el header, persistencia en `localStorage`, ambos idiomas viven en el mismo HTML mediante `<span data-lang="en|es">` con CSS que oculta el inactivo. Actualiza también `<title>` y `<meta description>`.
- **Tema claro/oscuro** — auto por `prefers-color-scheme` en la primera visita, persistente después.
- **Tipografía** — la misma jerarquía que el juego, vía tres variables en `:root`: `--f-display` (**Lilita One**) para títulos, botones y etiquetas, `--f-body` (**Space Grotesk**) para el cuerpo, y `--f-pixel` (**Press Start 2P**) reservada a los números — contadores, dorsales de las tarjetas de mundo y de jefe, y las cifras de la sección "detrás del juego". Es lo que hace el juego, donde `OrbexUI` cambia el árbol entero a Lilita One y la pixel solo sobrevive en el HUD de partida (marcador, combo, vida del jefe). ⚠️ **Lilita One tiene un único peso**: los encabezados vienen en bold por defecto del navegador, así que hay una regla `h1,h2,h3,h4{font-weight:400}` para que no se sintetice la negrita. Los encabezados que sí van en negrita son los de Space Grotesk y declaran su peso inline, que gana a esa regla. Y como Lilita se lee más pequeña que la pixel al mismo tamaño, los `font-size` heredados van escalados hacia arriba (~×1.4 en textos pequeños, ~×1.35 en titulares) — el juego hace lo mismo con un ×1.5.
- **Fuentes AUTOALOJADAS** (`assets/fonts/*.woff2`, 49 KB las tres) — ver el apartado propio más abajo.
- **Tráiler** — embed de YouTube (`youtube-nocookie.com`) en modal. El `<iframe>` nace **sin `src`**: no se hace ninguna petición a Google hasta que el usuario pulsa "Ver tráiler", y al cerrar el modal se le quita el `src` para detener la reproducción. Es el patrón click-to-load, así que la landing no necesita banner de cookies.
- **Navegación móvil** — por debajo de 1000 px (el mismo breakpoint donde `.navlink` desaparece) el JUGAR de la barra se oculta y aparece una hamburguesa que despliega un panel con el CTA en dorado arriba y los ocho enlaces debajo. Se cierra al elegir enlace, al tocar fuera de la cabecera, con Escape y al pasar a escritorio.
  - ⚠️ **Ese número está en CUATRO sitios** — tres media queries y el `resize` del script — y hay que moverlos juntos. Subió de 860 a 1000 al entrar el enlace de FAQ: con siete enlaces, el idioma, el tema y el CTA, a 860 px la barra ya no cabía y se salía por la derecha (no daba scroll horizontal porque `body` lleva `overflow-x:hidden`, o sea que el síntoma quedaba tapado).
  - ⚠️ Las reglas que ocultan `.nav-burger` y `.nav-play-top` van **cualificadas con `.nav-header`** a propósito: `.icon-btn` y `.btn-play-nav` se declaran más abajo en la hoja con la misma especificidad y ganarían por orden de aparición.
- **A11y**: skip link, `aria-label` en todos los botones-icono, `aria-expanded` / `aria-controls` en la hamburguesa, `:focus-visible` propio (el outline por defecto sobre botones dorados no se veía), modales con `role="dialog"`, foco atrapado con Tab, foco devuelto al cerrar, scroll de fondo bloqueado, cierre por Escape, y respeta `prefers-reduced-motion`. `scroll-padding-top` descuenta la cabecera fija para que un ancla no deje el título debajo de ella.
- **Rendimiento** — ver el apartado dedicado más abajo.
- **SEO**: Open Graph + Twitter Card completos, canonical, `hreflang` alternates, `sitemap.xml`, `robots.txt` y **JSON-LD** (`VideoGame` + `FAQPage`). HTML estático — Google/Twitter ven el contenido en la respuesta inicial, no en un shell hidratado.

### El interruptor de lanzamiento (`RELEASE`)

El juego todavía no está publicado, así que **la página entera tiene dos caras** y las dos viven en el mismo HTML. Las conmuta CSS a partir del atributo `data-release` del `<html>`:

```css
html[data-release="soon"] [data-when="live"]{display:none !important}
html[data-release="live"] [data-when="soon"]{display:none !important}
```

**El día del lanzamiento se toca UNA cosa**: `RELEASE.live = true` al principio del `<script>` (y la URL de Play, que ya está escrita ahí). Con eso los CTA pasan a apuntar a la ficha y reaparecen el botón grande, el badge y el QR.

> ⚠️ **Los cuatro CTA de PLAY apuntaban a `#PLACEHOLDER-play-store`**, o sea a ninguna parte: quien pulsaba el botón más grande de la página no iba a ningún sitio y la página se leía como rota. Hoy apuntan a `#descarga`, que es donde se explica en qué punto está el juego. El `href` real lo escribe el script cuando `live` es true; **sin JS se quedan en `#descarga`**, que es un destino honesto y no un enlace roto.
>
> ⚠️ **Los textos NO los pone JS**, los pone CSS. Así no hay parpadeo ni depende de que el script llegue a tiempo, que es el mismo criterio del toggle de idioma.
>
> ⚠️ **El botón, el badge y el QR de la sección de descarga se ven SIEMPRE**, también antes del lanzamiento: quedan preparados y el día que salga solo cambian de rótulo y de destino. Mientras tanto el botón dice "PRÓXIMAMENTE" (corto a propósito: el titular de dos líneas más arriba ya dice "Próximamente en Google Play", y repetirlo entero sonaba a eco) y baja a su propia sección.
>
> ⚠️ **El badge y el QR son placeholders** hasta que exista la ficha — ver *Lo que queda antes de anunciar*.
>
> ⚠️ La píldora del hero (`.status-pill`) es la única pieza que dice en qué punto está el juego, y es lo primero que quiere saber quien llega desde un enlace: si puede jugarlo ya o no.

### La demo de la mecánica (sección "cómo se juega")

Un `<canvas>` que dibuja lo que hace el juego: una cadena de orbes recorre un camino, el tirador del centro inserta uno y las combinaciones de tres o más revientan encadenando combos. Es la pieza que explica el juego a quien no ha jugado nunca a nada parecido, **sin pedirle que vea un vídeo**.

Usa los sprites reales de los orbes (5 KB cada uno en webp, ya descargados por los orbes flotantes) y una polilínea Catmull-Rom parametrizada **por longitud de arco**, igual que el `path_progress` del juego.

⚠️ **Debajo del marco va una nota que dice lo que la demo NO es** (`.demo-note`): una recreación en el navegador, sin las físicas del juego y sin el pixel art dibujado a mano — que es la mitad de lo que Orbex es. Antes había un rótulo DENTRO del marco que decía *"la misma mecánica del juego"*, y eso era vender la demo por lo que no es: enseña la idea, no el acabado.

⚠️ **La nota va FUERA y al ancho del marco.** Dentro tapaba la cadena en el tramo bajo del camino, y una advertencia sobre lo que la demo no es no debería competir con lo que la demo está enseñando. Con `max-width` propio se leía como un párrafo suelto flotando debajo; al ancho del marco se lee como su pie.

> ⚠️ **CUATRO colores, no cinco** — los mismos que `BALL_COLORS`; el morado es el comodín y no entra en el reparto. Con cinco, además, las cascadas casi no salían.
>
> ⚠️ **El suministro lleva sesgo de pareja (0,3), igual que el `pair_bias` del spawn real.** Sin él, la junta que queda tras un estallido casi nunca vuelve a hacer tres y las cascadas —que son de lo que va el paso 02— no salen: medido, un combo cada 28 s contra los ~15 s de ahora. Por encima de 0,4 la cadena se apelmaza en tramos largos de un color y deja de parecer una partida.
>
> ⚠️ **La cascada NO se resuelve en el mismo frame, y ahí estaba el fallo de diseño.** Con la recursión instantánea los seis orbes desaparecían de golpe: no había nada que ver, y del combo —que es justo lo que el paso 02 promete— solo quedaba un rótulo de 0,4 s. Hoy el estallido deja apuntada la **junta** (los dos tramos que quedan enfrentados y comparten color), el tramo de detrás se cierra con **imán** —más rápido que un hueco normal, `MAGNET` contra `CLOSE`— y revienta **al tocarse**. Que es lo que hace el juego, y convierte un frame en una secuencia de ~2 s que se entiende sola.
>
> ⚠️ **El rótulo `COMBO xN` solo lo puede emitir ese camino**, así que verlo en pantalla es la prueba de que el diferido funciona: `land()` llama a `resolve()` con profundidad 1, que no rotula. Medido en la página real a 57 fps: **un combo cada 12,5 s**, rótulo 40 unidades de ancho sobre 160 y **0 de 333 frames de rótulo fuera del marco**.
>
> ⚠️ **Flota hacia ABAJO si el combo cae en el tramo alto del camino.** Subía siempre, y ahí arriba (y ≈ 16) eso lo sacaba del marco: se veía cortado. La dirección se elige al crearlo y hay un clamp de red.
>
> ⚠️ **La palanca de la frecuencia de combos es el SESGO DE PAREJA, no la preferencia del tirador.** Medido: de 0,30 a 0,35 las cascadas suben del 8,5 % al 12,5 % de los disparos, mientras que subir la preferencia de 0,7 a 0,95 aporta 1-2 puntos — en la mayoría de disparos solo hay un sitio donde combinar, así que no hay nada que preferir. Por encima de 0,38 la cadena se apelmaza en tramos largos de un color.
>
> ⚠️ **El tirador PREFIERE la jugada que encadena** (85 % de las veces que puede elegir). No el 100 %, o la demo se lee como un vídeo en bucle.
>
> ⚠️ **El orbe del cañón es EL QUE SALE.** Se elige un disparo antes (`loadGun`), y el disparo busca dónde ese color hace tres. Si no puede, lo pega junto a otro igual —un disparo de preparación, que también es jugar— y si tampoco, dispara donde sea. Fallar de vez en cuando es lo que hace que parezca una partida.
>
> ⚠️ **El hueco que abre un estallido se cierra DESLIZANDO, y el signo importa.** `pos(j) = front - j*SPACING + off`, o sea que un índice mayor está más atrás: al quitar `n` orbes, los de detrás pasan a índices más bajos y su posición nominal **salta hacia delante**. Hay que arrancarlos con `off` NEGATIVO y dejar que suba a 0. Con el signo al revés saltan hacia delante y luego se deslizan hacia atrás, que es justo lo contrario de lo que hace el juego.
>
> ⚠️ **Se para sola** al salir del viewport (IntersectionObserver) y con la pestaña en segundo plano, el delta va topado a 1/20 s (volver de segundo plano no puede adelantar la cadena media pantalla de un frame), y con `prefers-reduced-motion` no arranca: el hueco lo ocupa un texto que cuenta lo mismo.
>
> ⚠️ **Asignar `canvas.width` LIMPIA el canvas**, así que `resize()` pinta un frame cuando la demo está parada. Sin eso el marco se queda en negro hasta que el observer la vuelva a arrancar — se ve al redimensionar con la sección fuera de pantalla.
>
> ⚠️ **Medir esto en el navegador NO funciona**: con la ventana en segundo plano Chrome baja `requestAnimationFrame` a 1 fps y cualquier conteo de combinaciones sale a cero. La lógica es aritmética de arrays, así que se extrae y se corre en Node — `scratchpad/sim_demo.js` lee las constantes del propio `index.html` y simula 4.000 disparos. Estado actual: **84 % de disparos que combinan, un combo cada ~15 s**.

#### La posición de cada orbe: dos desplazamientos, y los tres fallos que costaron

`pos(j) = front - j*SPACING + off - pu`. El hueco nominal lo da el **índice**; encima van dos correcciones que siempre tienden a cero:

| | qué es | quién lo pone |
|---|---|---|
| `off` | lo que le queda por deslizar tras un estallido | `resolve()`, en negativo: el orbe **salta** hacia delante al bajar de índice y `off` lo devuelve a donde estaba |
| `pu` | el hueco que la cadena abre **mientras la bola llega** | el vuelo del disparo, creciendo de 0 a `SPACING` |

⚠️ **La invariante es que dos orbes consecutivos nunca están a menos de `SPACING`.** Medida sobre la página real interceptando `drawImage` —que es lo único que dice dónde se pinta cada orbe de verdad— sobre 85.211 pares visibles: **mínimo 9,49 de 9,70 nominal y cero solapes**. Ese 9,49 no es un fallo: es la curva cerrada de la derecha, donde la distancia en línea recta es algo menor que la recorrida por el camino.

Los tres fallos que rompían la invariante, y **ninguno daba error**: la cadena simplemente se montaba sobre sí misma.

1. **El suministro miraba la posición NOMINAL del último orbe, ignorando su `off`.** Tras un estallido los de detrás llevan `off` negativo —están más atrás de lo que su índice dice—, así que la cuenta creía que sobraba sitio y metía orbes **nuevos en medio de la cadena**, encima de los que ya estaban. Es el que se veía. Medido: separación mínima **−222** (o sea que se cruzaban de sitio) en el 1,1 % de los pares.
2. **El orbe insertado nacía con `off = 0`** en vez de heredar el del hueco que ocupa, así que aterrizaba desplazado siempre que la cadena viniera deslizando.
3. **El objetivo del disparo viajaba como ÍNDICE.** Si la cabeza caía por el agujero durante el vuelo, todos los índices bajaban uno y la bola entraba un hueco por detrás de donde había volado. Pasa en ~1 de cada 8 disparos (la cabeza cae cada ~1,9 s y el vuelo dura 0,24 s). Hoy viaja como **referencia al orbe**, y `land()` lo localiza con `indexOf`.

⚠️ **Y el hueco se abre DURANTE el vuelo, no al aterrizar** (`pu`), que es lo que hace el juego en `_push_subchain_until_clear`. No es cosmética: la bola nueva tiene que ocupar el sitio donde estaba la que desplaza, así que si el hueco se abriera al aterrizar las dos coincidirían **en el mismo punto** durante el tercio de segundo que tarda en deslizarse. Con el empuje ya hecho, al subir un índice cada orbe de detrás ese `SPACING` lo aporta el propio índice: se suelta el `pu` y las posiciones salen continuas.

⚠️ **Al tocar cualquiera de las dos correcciones hay que volver a medir la separación**, y hacerlo **en la página**: un modelo aparte de la lógica se desincroniza del código real, y aquí el fallo era precisamente que el modelo mental (el índice) y la posición real no coincidían.

#### Los contadores

Las siete cifras que cuentan hacia arriba al entrar en pantalla (`.tally`). El valor final **ya viene escrito en el HTML**, y la animación arranca en el primer frame de `requestAnimationFrame`, no antes: sin JS, con `prefers-reduced-motion` o con rAF estrangulado, lo que se lee es el número bueno.

⚠️ **La animación va en su PROPIA función, y eso no es estilo.** `var` es de ámbito de FUNCIÓN, así que con el bucle dentro del callback del observer las tres cifras que entran a la vez compartían `el`, `to` y `t0`: las tres acababan animando el **último** elemento y las anteriores se quedaban clavadas en el 0 del primer frame. En pantalla se leía **"0 mundos, 0 niveles, 16 jefes"** — y el patrón delata la causa, porque **siempre acierta la última de cada grupo**.

⚠️ Diagnostiqué esto mal la primera vez: lo atribuí al estrangulamiento de rAF (con la ventana tapada Chrome lo baja a 1 fps, y la cifra se queda en 0 mientras tanto) y añadí una guarda de `document.hidden` que no arreglaba nada. **El síntoma es idéntico y la causa no**: si es el estrangulamiento, se recupera al volver a la ventana; si es el cierre, no se recupera nunca.

⚠️ **Por debajo de 10 no se anima**: el "1" de "una persona" solo puede contarse desde 0, que es feo y además falso mientras dura.

#### Los iconos de los CTA del hero van en SVG, no como glifo

⚠️ **`text-shadow` SE HEREDA**, y los dos botones del hero llevan el contorno de ocho sombras (`--text-outline`) que esta página usa para sostener el texto claro sobre dorado. El triángulo de "ver tráiler" era un `&#9654;` de **9 px**: a ese tamaño ocho sombras a 1,5 px son tan gruesas como el propio carácter, y se veía **duplicado y emborronado**. Encima Lilita One no tiene ese carácter, así que caía a una fuente del sistema con sus propias métricas y quedaba descentrado dentro del círculo.

Hoy es un SVG, que no hereda sombras de texto y se centra exactamente. Dos cosas suyas que **no se leen en el número del `width`**:

- ⚠️ **Un triángulo se centra por su CENTROIDE, no por su caja.** La masa de uno que apunta a la derecha está a un tercio de la base, así que centrado por caja se ve corrido a la izquierda. El `viewBox` de 12×12 con la base en x=3,6 y el vértice en x=10,8 deja el centroide en (6,6) exacto — medido sobre el píxel: desvío **0,00 px** en los dos ejes.
- ⚠️ **El dibujo no llena el `viewBox`**: ocupa el 60 % de ancho y el 63 % de alto. A `width=11` el triángulo salía de 5 px y se perdía dentro del círculo (**24 %** de su diámetro, cuando lo habitual en un botón de play es 40-45 %). A 16 mide ~10 px. **Al tocar el tamaño hay que mirar el DIBUJO, no la caja.**

⚠️ La X de cerrar de los modales sí sigue siendo un glifo (`&times;`) y está bien: sus botones no heredan ningún contorno. Lo que no puede repetirse es meter un glifo **dentro de un botón que lleve `--text-outline`**.

### Rendimiento

**Los assets pasaron de 42 MB a 2,6 MB (−94 %) el 2026-08-21**, y una visita que recorre la página entera descarga hoy **1,34 MB en 47 peticiones, ninguna a un tercero**.

- **Los 10 retratos de jefe eran 34 MB de los 42** — PNG de 1152×2048 que se pintan a ~210 px de ancho. En webp a 576×1024 son ~75 KB cada uno. Iban con `loading="lazy"`, así que no rompían la carga inicial, pero llegar a la sección de jefes costaba 34 MB en datos móviles.
- Los escudos de mundo (3,4 MB), los orbes, el wordmark y el fondo del hero siguieron el mismo camino: **cada asset se genera al tamaño en que se PINTA**, con el ancho a 2× del tamaño CSS.
- **La galería tiene dos tamaños**: `N-thumb.webp` (720 px) para las tarjetas y `N.webp` (1280 px) para el lightbox, que es donde se mira de verdad. Con un solo fichero, entrar en la galería costaba 1,5 MB en vez de 525 KB.
- Los originales están en **`_source/originals/`**, que está en `.gitignore` y no se despliega: no se ha borrado nada y se puede regenerar con `scratchpad/webpify.py`.
- El **hero** precarga su fondo y el wordmark con `fetchpriority="high"` (son el LCP).
- Todas las imágenes llevan `width`/`height` o van dentro de un contenedor con `aspect-ratio`, para que nada salte al cargar. ⚠️ Si el CSS fija solo el ancho, el `height` del HTML se aplica **como alto fijo** y deforma la imagen: por eso `.float-orb` lleva `height:auto`, que es lo que hace que los dos atributos sirvan solo de proporción.

Y lo que ya estaba, que **no conviene deshacer**:

- **`.modal-backdrop` no lleva `backdrop-filter`.** Un desenfoque a pantalla completa se recalcula cada vez que cambia algo por debajo, y con el tráiler abierto eso es cada fotograma. Peor todavía: `#orbex-trail` está en z-index 90 y el modal en 100, así que cada partícula del rastro nacía *debajo* del desenfoque y disparaba un reblur de toda la ventana ~35 veces por segundo. Se compensa con la opacidad del fondo (0,93).
- **`body.modal-open` congela lo decorativo** mientras hay un modal: oculta el rastro (y corta su generación), apaga el `backdrop-filter` de la cabecera y pausa `logoPulse` y `forgeShift`. Esas dos animan `filter` y `background-position`, que repintan en vez de componer, y corrían siempre aunque estuvieran fuera de pantalla.
- La clase la recalcula `syncModalOpen()` mirando si queda **algún** `.modal-backdrop.open`. Escape llama a los dos cierres, y uno no puede descongelar lo que el otro sigue usando.
- **UN solo listener de scroll** para las tres cosas que dependen de él —parallax del hero, barra de progreso de lectura y enlace activo de la barra— y escribiendo **una vez por frame** (`requestAnimationFrame`). El evento se dispara muchas más veces que fotogramas hay; con tres listeners separados se paga tres veces el mismo trabajo. La barra de progreso anima `transform` y no `width`, que dispararía layout en cada frame.
- Las partículas del rastro se limpian con `animationend`, no con un `setTimeout` cada una.
- Todas las imágenes `loading="lazy"` llevan `decoding="async"`.

### Fuentes propias

Las tres fuentes se sirven desde `assets/fonts/` como woff2 con subset latino (**49 KB en total**), en vez de pedirlas a Google Fonts.

- Quita **dos conexiones a terceros** y una hoja de estilos bloqueante del camino crítico.
- Y quita una petición a Google en cada visita, que es lo coherente con una landing que no necesita banner de cookies — y con una **política de privacidad** que explica qué datos se recogen y a quién se le mandan. La página de `/privacy` usa las mismas.
- El subset cubre latino + latin-ext + puntuación + unos símbolos. **Lo que caiga fuera** —el 日本語 / 한국어 / РУССКИЙ de la sección de idiomas— cae al `system-ui` de la pila, que es exactamente lo que ya pasaba con Google Fonts: ninguna de las tres fuentes tiene esos alfabetos.
- Space Grotesk va como **variable** (un solo fichero para los pesos 300-700).
- Se regeneran desde los TTF de `_source/_ds/.../assets/fonts/` con `fontTools` (`pip install fonttools brotli`); la receta está en `scratchpad/`.
- ⚠️ Llevan `Cache-Control: immutable` en los tres ficheros de host (`_headers`, `netlify.toml`, `vercel.json`). Sin esa regla se revalidarían en cada visita, que es justo lo que se gana al autoalojarlas.

### Política de privacidad

Vive en dos ficheros que hay que editar **siempre a la vez** o divergen: `PRIVACY.md` (source of truth bilingüe) y `privacy/index.html` (la página servida). Cada uno lleva el texto EN y ES completo.

Al tocarla, subir la fecha de "Última actualización" en los dos y en los dos idiomas — son cuatro sitios.

⚠️ **La política ya no se puede regenerar desde `_source/Orbex Privacy.dc.html`.** Ese fichero es el canvas de diseño original y se quedó en la versión del 2026-08-04; además está en `.gitignore`, así que ni se versiona ni se despliega. La fuente de verdad son los dos ficheros de arriba.

**Tiene que ir por delante de lo que hace el juego, no por detrás**, y la versión del 2026-08-04 demostró lo fácil que es que se quede detrás: siguió diciendo "no pedimos tu correo" y "no mostramos anuncios" durante dos semanas en las que Google Sign-In ya vinculaba correos y el SDK de AdMob ya estaba dentro de la build. Las dos frases eran justo las dos que Google Play contrasta con la declaración de Data Safety.

⚠️ **Al tocar la política hay que revisar también la declaración de Data Safety de Play Console.** Las dos tienen que decir lo mismo; si divergen, Play rechaza la actualización.

Al día desde el 2026-08-24 (14 apartados). Lo que cubre y que no estaba antes: publicidad y AdMob (§3), vinculación con Google (2.2), amigos, desafío semanal y supervivencia (2.1), economía y tiempo de app dentro de la telemetría opcional (2.5), base legal por finalidad (§5), compras (§4) y sanciones de cuenta (§11).

**Lo último que entró (2026-08-24) es el apartado 2.6, y viene de la 1.21**: CONTACTO y DENUNCIAR dejaron de abrir un `mailto:` y pasaron a guardar **texto que escribe el jugador** en la base. Eso obliga a tres cosas a la vez y ninguna se puede dejar a medias — el apartado que lo describe (2.6, con lo que se envía, quién lo lee y los 90 días de retención), **DeepL** como proveedor en §6 y §7 (la traducción del panel de soporte manda ese texto a un tercero), y la casilla **Mensajes › Otros mensajes in-app** de la Data Safety de Play Console.

⚠️ **La clave de DeepL es la del plan API FREE, cuyos términos permiten a DeepL usar los textos enviados para mejorar su servicio.** La política lo dice con esas palabras porque es lo que hay, y por eso 2.6 le pide al jugador que no escriba datos personales que no hagan falta. Es también el matiz que §5 tiene que hacer sobre el "no entrenamos modelos de IA": no lo hacemos nosotros, pero el proveedor puede. **Pasar a la API Pro haría falso ese párrafo** — al hacerlo, reescribir los tres sitios (2.6, §5 y §6).

Lo que queda pendiente:

| Cuándo | Qué cambia |
|---|---|
| Al pasar AdMob a **unidades reales** (`USE_TEST_AD_UNITS = false`) | Nada en el texto — §3 ya está redactado para los dos casos. Sí hay que repasar la Data Safety de Play. |
| Al activar **Play Billing** (`BILLING_AVAILABLE = true`) | §4 dice "Orbex no vende nada dentro de la app": pasa a ser falso. Hay que describir qué recibimos de Google Play y revisar las menciones a compras de §9. |
| Al añadir un **evento de temporada nuevo** | 2.1 nombra la divisa del evento de forma genérica a propósito; comprobar que sigue siendo cierto. |
| Si se cambia el **plan de DeepL** a Pro | Sus términos sí garantizan borrado y no entrenamiento: 2.6, §5 y §6 pasan a decir de más. Reescribir los tres. |
| Si alguna vez se recoge algo **nuevo del jugador** | La regla es que 2.1/2.5/2.6 lo listen ANTES de que la build salga. Los apartados que más envejecen son 2.1 (tablas nuevas), 2.5 (telemetría nueva) y 2.6 (texto libre nuevo). |

### Estructura

```
orbex-web/
├── index.html               landing (bilingüe)
├── privacy/index.html       /privacy — política real
├── PRIVACY.md               source-of-truth bilingüe
├── assets/
│   ├── fonts/               3 woff2 con subset latino (49 KB)
│   └── images/
│       ├── orbex-title.webp wordmark
│       ├── zones/           10 escudos de mundo
│       ├── bosses/          10 retratos verticales de jefe
│       ├── orbs/            5 orbes (también los usa la demo del canvas)
│       ├── icons/           UI icons
│       ├── avatars/         3 avatares
│       ├── bg/              fondo del hero
│       ├── screenshots/     8 capturas + sus 8 miniaturas (-thumb)
│       ├── flags/           10 banderas de idioma (PNG: pixel art)
│       └── placeholders/    ⚠️ sustituir antes de lanzar
├── _source/originals/       ⚠️ los PNG/JPG originales, gitignored
├── robots.txt sitemap.xml
├── _headers _redirects       Cloudflare Pages / Netlify
├── netlify.toml vercel.json
└── README.md                 este archivo
```

> ⚠️ **Todo lo que se pinta va en `.webp` menos las banderas**, que son pixel art de 4-5 KB y no ganan nada al convertirse. Los `.png`/`.jpg` de los que salen viven en `_source/originals/` con la misma jerarquía de carpetas: `_source/` está en `.gitignore` y en `.netlifyignore`, así que ni se versiona ni se despliega. Para regenerarlo todo, `python scratchpad/webpify.py`.

### Probar localmente

```bash
python scratchpad/serve.py
# → http://localhost:8000/   y   http://localhost:8000/privacy/
```

Es `python -m http.server` con dos cosas encima, y las dos hacen falta:

- **`Cache-Control: no-store`** — el servidor pelado manda `Last-Modified` y el navegador cachea el HTML de forma agresiva: editas `index.html`, recargas y no ves el cambio. Es lo que obliga a andar recargando con `?v=2`.
- **Tipos MIME de `.webp` y `.woff2`** — sin ellos las fuentes se sirven como `application/octet-stream` y Chrome las rechaza **en silencio**: la página cae a la fuente del sistema y parece un problema del CSS.

⚠️ Solo para desarrollo. En producción las cabeceras las ponen `_headers`, `netlify.toml` o `vercel.json`, que sí cachean de verdad.

### Deploy

Cualquier host estático. Recomendado **Cloudflare Pages**: framework "None", output `/`, `_headers` + `_redirects` se aplican automáticamente. Alternativas con config incluida: **Netlify** (`netlify.toml`) y **Vercel** (`vercel.json`).

Custom domain `orbex.aleixaj.com` apunta al proyecto de Pages vía CNAME automático (dominio ya en Cloudflare).

### Lo que queda antes de anunciar

**El enlace a Google Play ya no es un placeholder**: es el interruptor `RELEASE` (ver su apartado). El día del lanzamiento se pone `live: true` y se comprueba que la URL de la ficha es la buena.

Lo que sí sigue siendo un placeholder, todo dentro de `assets/images/placeholders/`:

| Placeholder | Sustituir por | Dónde se ve |
|---|---|---|
| `og-image.png` | Imagen para redes, 1200×630 | Solo al compartir el enlace |
| `favicon-32.png` · `favicon-192.png` | Favicons definitivos | Pestaña del navegador y `apple-touch-icon` |
| `google-play-badge.png` | Badge oficial de Google Play | Solo con `RELEASE.live = true` |
| `qr.png` | QR real a la ficha de Play | Solo con `RELEASE.live = true` |

Los dos últimos **no se pintan hoy**, así que no corre prisa: entran con el mismo flip.

También pendiente:

- **Términos de uso**: su enlace se retiró del footer porque no llevaba a ninguna parte. Google Play no los exige (solo la política de privacidad); cuando exista la página, se vuelve a añadir el `<li>`.
- ⚠️ **`screenshots/7.jpg` está desactualizada**: el ranking muestra pestañas de nivel 1-5 y el build actual tiene 8 niveles por mundo. Hay que recapturarla (y revisar si la misma imagen está subida a la ficha de Play). Al sustituirla hay que regenerar **las dos versiones** — la de 1280 y su `-thumb`.
- Ya no se usan y se pueden borrar: `placeholders/hero-gameplay.png` y `placeholders/gameplay-1..3.png`.

### Herramientas (`scratchpad/`, no se despliega)

| Script | Para qué |
|---|---|
| `webpify.py` | Regenera todos los `.webp` desde `_source/originals/` al tamaño en que se pintan |
| `serve.py` | Servidor local sin caché y con los MIME correctos (ver *Probar localmente*) |
| `sim_demo.js` | Simula 4.000 disparos de la demo del canvas leyendo sus constantes del `index.html`. Es la única forma de medir el ritmo de combos: en el navegador rAF baja a 1 fps con la ventana en segundo plano y la medida miente |
