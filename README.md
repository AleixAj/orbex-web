# Orbex — landing pública + memoria técnica del juego

![Godot](https://img.shields.io/badge/Godot-4.6-478CBF?style=for-the-badge&logo=godotengine&logoColor=white&labelColor=2D2D2D)
![GDScript](https://img.shields.io/badge/GDScript-tipado_estático-355170?style=for-the-badge&logo=godotengine&logoColor=white&labelColor=2D2D2D)
![PostgreSQL](https://img.shields.io/badge/Supabase-PostgreSQL_+_RLS-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white&labelColor=2D2D2D)
![Deno](https://img.shields.io/badge/Edge_Functions-TypeScript-000000?style=for-the-badge&logo=deno&logoColor=white&labelColor=2D2D2D)
![Google Play](https://img.shields.io/badge/Google_Play-publicado-3DDC84?style=for-the-badge&logo=googleplay&logoColor=white&labelColor=2D2D2D)
![Landing](https://img.shields.io/badge/Landing-HTML_+_CSS_+_JS_vanilla-e34f26?style=for-the-badge&logo=html5&logoColor=white&labelColor=2D2D2D)

**Orbex** es un juego de móvil publicado en Google Play ([`com.aleix.orbex`](https://play.google.com/store/apps/details?id=com.aleix.orbex)), hecho de principio a fin por una sola persona: cliente, backend, base de datos, pagos, telemetría, cumplimiento legal y la web que lo acompaña.

**Este repositorio contiene la landing** ([orbex.aleixaj.com](https://orbex.aleixaj.com)). El código del juego es privado, así que **este documento es su memoria técnica**: cómo está montado por dentro, qué problemas de ingeniería aparecieron de verdad y cómo se resolvieron.

> **Por qué puede interesarte aunque no te dediques a videojuegos.** El juego es la excusa; el trabajo es de software. Aquí hay un backend PostgreSQL en producción con RLS y pentest, un sistema de pagos con verificación en servidor e idempotencia frente al doble cobro, consultas optimizadas contra un banco de 200.000 filas, telemetría con retención automatizada, cumplimiento de GDPR y Play Data Safety, y una batería de pruebas verificada por mutación. Nada de eso es específico de un juego.

---

## Índice

- [El proyecto en números](#el-proyecto-en-números)
- [Parte 1 — La landing (este repositorio)](#parte-1--la-landing-este-repositorio)
- [Parte 2 — El juego](#parte-2--el-juego)
  - [Stack y forma del proyecto](#stack-y-forma-del-proyecto)
  - [Arquitectura del cliente](#arquitectura-del-cliente)
  - [El motor de cadena, y una optimización con medida](#el-motor-de-cadena-y-una-optimización-con-medida)
  - [Backend: modelo de datos y API](#backend-modelo-de-datos-y-api)
  - [Seguridad del backend](#seguridad-del-backend)
  - [Escala: lo que se rompe con volumen](#escala-lo-que-se-rompe-con-volumen)
  - [Pagos in-app](#pagos-in-app)
  - [Publicidad](#publicidad)
  - [Identidad y guardado en la nube](#identidad-y-guardado-en-la-nube)
  - [Interruptor remoto de versión](#interruptor-remoto-de-versión)
  - [Telemetría y balance por datos](#telemetría-y-balance-por-datos)
  - [Anti-trampas: modelo de amenaza explícito](#anti-trampas-modelo-de-amenaza-explícito)
  - [Moderación y soporte dentro de la app](#moderación-y-soporte-dentro-de-la-app)
  - [Internacionalización](#internacionalización)
  - [Accesibilidad](#accesibilidad)
  - [Estrategia de pruebas sin CI](#estrategia-de-pruebas-sin-ci)
  - [Herramientas propias](#herramientas-propias)
  - [Rendimiento y despliegue en Android](#rendimiento-y-despliegue-en-android)
- [Qué demuestra el proyecto](#qué-demuestra-el-proyecto)
- [Contacto](#contacto)

---

## El proyecto en números

| | |
|---|---|
| Código de cliente | **265 ficheros GDScript**, ~98.000 líneas, tipado estático |
| Backend | **27 ficheros SQL**, ~11.000 líneas, **112 funciones/RPC** en PostgreSQL |
| Serverless | 3 **Edge Functions** en TypeScript: verificación de compra, sincronización de reembolsos y traducción de soporte |
| Pruebas | **130 scripts de QA** headless (arneses, dobles, fuzzing y medición), la mayoría verificados por mutación |
| Contenido | 237 escenas, **92 niveles**, 10 mundos, 16 combates de jefe |
| Localización | **1.155 claves × 10 idiomas** |
| Servicios globales | 26 autoloads: economía, progreso, ranking, eventos, pagos, anuncios, ajustes… |
| Estado | Publicado en Google Play, versión **1.29**, con jugadores y compras reales |

---

## Parte 1 — La landing (este repositorio)

Sitio estático que sirve a la vez de página de producto y de URL de la política de privacidad exigida por Google Play.

### Stack

**HTML5 + CSS con custom properties + JavaScript vanilla.** Cero build, cero dependencias en runtime y cero peticiones a terceros: la página entera se sirve desde el propio dominio.

Es una decisión, no una limitación. Una landing de una página no necesita bundler, framework ni pipeline: necesita cargar rápido, ser indexable y no romperse. Sin build, desplegar es copiar la carpeta, y el HTML que ve Google es el mismo que escribí.

### Lo que tiene por dentro

| | |
|---|---|
| **Bilingüe EN/ES** | Los dos idiomas viven en el mismo HTML (`<span data-lang>`), los conmuta CSS y la preferencia persiste en `localStorage`. Sin JS también se ve un idioma completo |
| **Tema claro/oscuro** | Automático por `prefers-color-scheme` en la primera visita, persistente después |
| **Demo interactiva en `<canvas>`** | Recreación de la mecánica del juego: una cadena sobre una polilínea Catmull-Rom parametrizada por longitud de arco, con la misma lógica de inserción y cascada. Explica el juego sin pedirle al visitante que vea un vídeo |
| **Accesibilidad** | Skip link, `aria-expanded` / `aria-controls`, `:focus-visible` propio, modales con foco atrapado y devuelto, cierre por Escape, y respeta `prefers-reduced-motion` |
| **SEO** | Open Graph, `hreflang`, sitemap y JSON-LD (`VideoGame` + `FAQPage`) sincronizado con el contenido visible |
| **Sin banner de cookies** | El embed de YouTube nace sin `src` (patrón *click-to-load*) y las fuentes están autoalojadas, así que no hay ninguna petición a terceros hasta que el usuario la pide |

### Rendimiento

Los assets pasaron de **42 MB a 2,6 MB (−94 %)**. Una visita que recorre la página entera descarga hoy **1,34 MB en 47 peticiones**.

- Los 10 retratos de jefe eran 34 MB de esos 42: PNG de 1152×2048 que se pintan a ~210 px de ancho. Cada asset se regenera al tamaño en el que se pinta (2× del CSS) en `.webp`, con un script Python reproducible.
- La galería tiene dos resoluciones por imagen: miniatura de 720 px para las tarjetas y 1280 px para el visor.
- Las tres fuentes van autoalojadas con subset latino (**49 KB en total**), frente a dos conexiones a terceros y una hoja bloqueante en el camino crítico.
- Un único listener de scroll para las tres cosas que dependen de él, escribiendo una vez por frame con `requestAnimationFrame`. Las animaciones decorativas se congelan mientras hay un modal abierto: animaban `filter` y `background-position`, que repintan en vez de componer.

### Despliegue

Cualquier host estático. Está en **Cloudflare Pages** con dominio propio, y hay configuración lista también para Netlify y Vercel. Las cabeceras de caché (`immutable` en fuentes e imágenes) se declaran en los tres formatos.

### Estructura y desarrollo local

```
orbex-web/
├── index.html              landing bilingüe (11 secciones, demo en canvas)
├── privacy/index.html      /privacy — política servida
├── PRIVACY.md              fuente de verdad bilingüe de la política
├── assets/
│   ├── fonts/              3 woff2 con subset latino (49 KB)
│   └── images/             wordmark, mundos, jefes, orbes, capturas, banderas
├── _headers · _redirects · netlify.toml · vercel.json
└── scratchpad/             herramientas (no se despliega)
```

```bash
python scratchpad/serve.py     # http://localhost:8000
```

Es `python -m http.server` con dos cosas encima, y las dos hacen falta: `Cache-Control: no-store` —el servidor pelado cachea el HTML de forma agresiva y editar el fichero no se ve al recargar— y los tipos MIME de `.webp` y `.woff2`, sin los cuales Chrome rechaza las fuentes **en silencio** y la página cae a la del sistema, que parece un problema de CSS.

La **política de privacidad** vive en dos ficheros que se editan siempre a la vez (`PRIVACY.md` y la página servida) y tiene que ir por delante de lo que hace la app, no por detrás: la versión anterior siguió diciendo "no mostramos anuncios" durante dos semanas en las que el SDK ya estaba dentro de la build — y ésa es justo una de las frases que Google Play contrasta con la declaración de Data Safety.

---

## Parte 2 — El juego

### Stack y forma del proyecto

| | |
|---|---|
| Motor | Godot 4.6, perfil Mobile (`gl_compatibility`) |
| Lenguaje | GDScript con tipado estático y `class_name` |
| Plataforma | Android, landscape, base 1280×720, `minSdk 24` / `targetSdk 36`, `arm64-v8a` |
| Backend | Supabase — PostgreSQL + PostgREST + Auth anónima + Edge Functions (Deno/TS) |
| Persistencia local | Ficheros JSON en `user://` con escritura atómica propia |
| Servicios nativos | Google Play Billing 8.3.0, AdMob con flujo de consentimiento UMP, Google Sign-In |

### Arquitectura del cliente

```
+-------------+     +----------------------+     +--------------------+
|  AppRouter  |---->|  OrbexScreen (UI)    |---->|  Nivel (main.gd)   |
| (main.tscn) |     |  menú / mundo / mapa |     |  + HUD overlay     |
+-------------+     +----------------------+     +--------------------+
       |                                                    |
       v                                                    v
+-------------+                                    +--------------------+
|  Autoloads  |  progreso · economía · red         |  ChainBall x N     |
|    (26)     |  ajustes · eventos · pagos         |  ProjectileBall    |
+-------------+                                    |  Boss              |
       |                                           +--------------------+
       v
+---------------------------------------------------------------------+
|  Supabase — PostgREST (112 RPC) · RLS · pg_cron · Edge Functions     |
+---------------------------------------------------------------------+
```

Tres reglas sostienen la separación:

- **`AppRouter` es la única vía para cambiar de pantalla.** Ninguna pantalla navega a otra: todas se lo piden al router. Eso concentra en un sitio la carga de escenas, los modales, la pila del botón atrás de Android y el ciclo de vida de la partida.
- **Los SDK nativos entran por una puerta y solo por una.** `Ads` y `Purchases` son autoloads-fachada: ninguna pantalla habla con el plugin de Java. Se pide `await Ads.request_reward(placement)` o `Purchases.buy(sku)` y punto. El día que haya que portar a iOS (StoreKit) o cambiar de proveedor de anuncios, el cambio queda dentro de dos ficheros en vez de repartido por las cinco pantallas que reparten dinero.
- **Lo que se GUARDA y lo que se PINTA son cosas distintas.** Un cosmético equipado se conserva en disco aunque su desbloqueo no se pueda confirmar en ese momento (arranque sin red, rol del servidor que aún no ha llegado); lo que cambia es qué se dibuja. Sin esa separación, un arranque sin cobertura destruía la selección del jugador de forma permanente, porque el siguiente guardado hacía definitiva la pérdida.

### El motor de cadena, y una optimización con medida

El núcleo del juego es una fila de orbes que avanza por un camino y admite inserciones en cualquier punto: posición por longitud de arco (`path_progress`), inserción interpolada, empuje de la subcadena para abrir hueco, recolocación tras una eliminación y unión magnética de dos tramos separados cuando comparten color. Un nivel puede tener varios carriles independientes.

**El problema.** La función que coloca cada orbe hacía cinco consultas al camino por bola y por frame (posición, tramos con portal, tramos no enganchables y dos capas de profundidad), y las cinco eran **barridos lineales del camino entero**. Los caminos se trazan a mano y son densos: 164 puntos en el primer nivel, **361 en el más largo**. El coste iba con `bolas × puntos_del_camino`, no con bolas.

**La medida.** Con un banco de frames instrumentado, el nivel más caro costaba **3,9 ms por frame con 72 orbes** en una partida normal, y **9,1 ms** en el modo de supervivencia, que suelta el límite de orbes en pantalla. A 60 fps el presupuesto entero de un frame son 16,6 ms.

**La solución.** Búsqueda binaria sobre las distancias acumuladas del camino, más índices precalculados de los tramos marcados. Con un detalle que no perdona: los tramos de teletransporte miden 0 px, así que hay valores repetidos y hace falta un `lower_bound` real —quedarse con el primero de los empates— en lugar de una búsqueda binaria genérica. Con la genérica, un orbe sale por el portal equivocado.

| | antes | después |
|---|---|---|
| Nivel más caro, partida normal | 3,90 ms/frame | **0,22 ms** |
| Nivel más caro, modo supervivencia | 9,10 ms/frame | **2,94 ms** |

**La verificación.** Reimplementé las cinco versiones lineales dentro del arnés de prueba y las comparé con las nuevas sobre **los 92 niveles y sus 112 carriles**: 178.303 muestras, barrido fino más los bordes exactos de cada segmento y sus vecinos a un epsilon. De estas funciones cuelgan dónde se dibuja cada orbe, el fundido de los portales y si un disparo atraviesa un tramo. Un *off-by-one* aquí no lo caza ninguna otra prueba y no da error: simplemente se ve mal.

### Backend: modelo de datos y API

**Supabase, con toda la lógica en funciones de PostgreSQL.** El cliente no hace `INSERT` ni `UPDATE` contra ninguna tabla: cada escritura pasa obligatoriamente por una RPC `SECURITY DEFINER` que valida antes de escribir.

Subsistemas con esquema propio:

| Subsistema | Qué resuelve |
|---|---|
| Ranking | Tableros paginados por ámbito y nivel, posición exacta del jugador y vecindario (tú ± N rivales) |
| Perfiles públicos | Ficha de otro jugador: apodo, cosméticos equipados y estadísticas |
| Cloud save | Copia del progreso y códigos de transferencia entre dispositivos, de un solo uso y con caducidad |
| Compras | Catálogo, canje de recibos, entrega idempotente y revocación por reembolso |
| Desafío semanal | Nivel sorteado en servidor, el mismo para todos, con tablero propio y premios automáticos |
| Buzón | Mensajería del servidor al jugador, con lectura y cobro de recompensas |
| Amigos | Alta unilateral, notificaciones y tablero filtrado |
| Moderación | Sanciones, denuncias entre jugadores y soporte in-app |
| Telemetría | Fila por partida más agregados, con purga automática |

Cuatro tareas nocturnas con **`pg_cron`**: purga de telemetría a 90 días, roll-up diario de usuarios activos, limpieza de cuentas huérfanas y sincronización de reembolsos con Google.

### Seguridad del backend

La clave anónima va embebida en el APK por diseño, así que **el modelo de amenaza asume que cualquiera puede invocar cualquier RPC con cualquier argumento**. Lo que impide el abuso es el servidor, nunca la pantalla.

- **Toda función `SECURITY DEFINER` fija su `search_path`.** Sin eso, un `search_path` manipulado secuestra las llamadas de dentro del cuerpo.
- **Ninguna tabla tiene política de escritura.** RLS es la única barrera y no se desactiva en ninguna.
- **Guards de propiedad** (`auth.uid() = p_id`) en toda RPC que acepte un identificador de jugador.
- **Grants columnares** sobre la tabla de jugadores: la lectura pública sirve 16 columnas de perfil, y la economía, la telemetría y el estado de sanción quedan fuera.
- **A `anon` le llegan siete funciones, y las siete son de lectura.**

> **Un fallo real que enseña la lección.** `REVOKE EXECUTE ... FROM anon` **no hace nada por sí solo**: PostgreSQL concede `EXECUTE` a `PUBLIC` al crear cualquier función, y los roles heredan de ahí. La forma correcta es `FROM public, anon`. Trece funciones tenían ese error y una era grave: la que asigna roles quedó alcanzable desde la API pública, o sea que cualquiera con la clave del APK podía concederse permisos de administrador. Corregido y verificado con un **pentest de 8 vectores** —asignación de rol, escritura directa en tablas, envío de puntuaciones, borrado de cuenta ajena, restauración de progreso ajeno—: todos bloqueados, con los datos de la víctima intactos.

También hay verificación de forma: una RPC no se da por buena hasta **haberla llamado contra la base**. Dos funciones se crearon sin una queja y reventaron al ejecutarse — una por una variable con el mismo nombre que una columna (`plpgsql` resuelve primero contra sus variables), otra por tratar como booleano una función que lanza excepción. Los ensayos funcionales se hacen con un bloque `DO` que termina en `raise exception`: la transacción se aborta sola y no persiste ni una fila.

### Escala: lo que se rompe con volumen

Con 20 jugadores todo va rápido. Los problemas aparecen con padrón, así que las consultas críticas se midieron contra un **banco de 200.000 jugadores y 400.000 filas de puntuación**, con `EXPLAIN (ANALYZE, BUFFERS)`.

**1. El `OR` del desempate impedía usar el índice.** "Cuánta gente va por delante de mí" se traduce de forma natural a `score > X OR (score = X AND fecha < Y)`, y el planificador no puede acotar por índice ninguna rama dentro de un `OR`: cae a un escaneo con la condición como filtro. Partido en dos conteos por rango —los conjuntos son disjuntos—, cada rama entra por el índice.

| | plan | buffers | ms |
|---|---|---|---|
| Antes | Bitmap Heap Scan de 154.915 filas | 2.283 | 28,9 |
| Después | dos Index Only Scan, `Heap Fetches: 0` | **618** | 18,8 |

**2. Un `JOIN` normal se leía la tabla de jugadores entera en cada llamada.** El `LIMIT` de una página es un valor de *runtime*, así que el planificador estimaba miles de filas, elegía Hash Join y hacía `Seq Scan on players`. Un `JOIN LATERAL` no se puede *hash*-joinear, de modo que fuerza el Nested Loop contra la clave primaria y el join se aplica solo a las 50 filas de la página. Es una constante que crece con el **padrón**, no con quien juega:

| | antes | después |
|---|---|---|
| Primera página del ranking | 1.432 buffers / 11,1 ms | **785 / 2,6 ms** |
| Primera página de supervivencia | 2.505 / 31,6 ms | **885 / 4,8 ms** |

**3. Autovacuum afinado.** Los tableros reciben un `upsert` por partida jugada, y los `Index Only Scan` dependen del mapa de visibilidad. Con el valor por defecto la limpieza no se dispara hasta que el 20 % de la tabla son tuplas muertas: con 200.000 filas eso es el mapa obsoleto casi toda la semana activa, y la misma consulta pasa de 202.847 a **601.921 buffers (×3)**. Bajado a 0,02, con el `insert_scale_factor` incluido, que es el que importa en tablas que crecen por inserción.

**Antes de desplegar cada reescritura, comparación fila a fila contra la versión vigente sobre los datos reales**: 5.460 casos en el vecindario del ranking (todos los ámbitos × todos los jugadores × tres radios), 1.155 en la consulta de posición y 273 en la de página. **Cero diferencias.** Una consulta cuyo resultado el jugador ve como su puesto no se puede validar a ojo.

> Un aviso de método que costó una tarde: un micro-benchmark que mide las dos versiones **en bloques seguidos** no vale para comparar consultas — el orden y el estado de caché deciden el resultado, y la primera medición dio exactamente lo contrario de lo real. Lo que no miente es `EXPLAIN (ANALYZE, BUFFERS)` con medición alternada y calentamiento previo.

### Pagos in-app

Google Play Billing 8.3.0 con **verificación en servidor**. Es el subsistema con más superficie de fallo del proyecto, porque los errores cuestan dinero de verdad en las dos direcciones: entregar sin cobrar, o cobrar sin entregar.

**El flujo.** El cliente lanza la pasarela → Google devuelve un recibo → una **Edge Function** lo valida contra la API de `androidpublisher` con una service account → una RPC atómica registra la compra y devuelve qué conceder → el cliente entrega → el servidor confirma el acuse de recibo con Google.

Las decisiones que lo sostienen:

- **El importe lo pone el catálogo del servidor, no el cliente.** El cliente manda el SKU; si el servidor responde otra cantidad, se ingresa la del servidor. Lo único que el cliente elige es qué SKU va a la pasarela.
- **El token de compra es único GLOBALMENTE, no por jugador.** Con un índice único por `(jugador, token)` —que es lo que sale de pensar "cada jugador tiene sus compras"— un recibo comprado una vez valdría para todas las cuentas a las que le pasaras el token.
- **Tres cinturones contra la doble entrega**, y hacen falta los tres: el atajo de tokens ya liquidados, el registro local de entregados y el campo `delivered` del servidor. Google **reentrega** en cada conexión todo lo que no se ha consumido, así que el mismo token vuelve de forma normal; basta con que la app se cierre entre la entrega y el consumo para ingresar dos veces. Se reproduce a voluntad con el modo avión.
- **El acuse de recibo lo hace el servidor.** Google reembolsa sola toda compra no confirmada en 3 días: dejarlo al cliente significa que quien no vuelve a abrir el juego deshace su propia compra con el producto ya entregado.
- **Los reembolsos se aplican solos.** Una Edge Function nocturna consulta la lista de compras anuladas de Google y revoca el contenido permanente. La ventana consultada se **persiste**, porque la API solo devuelve 30 días: sin eso, un mes sin ejecutarla deja el hueco fuera de alcance para siempre.

**Cómo se prueba algo que mueve dinero.** Con un doble del cliente de facturación y otro del backend, un arnés recorre los **19 motivos de fallo del servidor** —los de Google, los del SQL y los del transporte— más cinco respuestas malformadas, y comprueba en cada uno que **no se concede nada y no se consume el token**; consumirlo tiraría una compra pagada. Y otro arnés responde la pregunta que se hace el jugador —*¿me llevo algo poniendo el modo avión?*— midiendo el saldo y el inventario antes y después de cada camino, en vez de leer el código.

> El fallo más caro de este subsistema no dio ningún error: el permiso remoto de venta llegaba al cliente y **se descartaba en la última línea**, porque el parseo construía su diccionario a mano con tres claves y la cuarta se caía por el camino. La tienda decía "Próximamente" pasara lo que pasara en la base de datos. La regla que salió de ahí —una clave nueva en la respuesta hay que añadirla también al parseo del cliente— la vigila ahora una prueba que extrae las claves del propio SQL.

### Publicidad

AdMob detrás del autoload-fachada, con tres piezas que no son evidentes hasta probarlo en un móvil real:

- **Caché por unidad con caducidad.** El anuncio recompensado se pedía dentro del propio `await`, así que cada toque esperaba hasta 10 segundos con el botón mudo. Hoy se sirve de una caché que se repone sola, con caducidad de 50 minutos: AdMob da un anuncio precargado por bueno alrededor de una hora, y pasado el plazo el jugador se quedaría **sin recompensa después de haber pulsado**, que es peor que esperar.
- **Un velo con retardo de 350 ms.** Con el anuncio precargado no hay espera, y un parpadeo de medio frame se lee como un fallo, no como "cargando".
- **Topes de seguridad sobre cada estado montado alrededor de un `await`.** Una corrutina puede morir a media espera —el plugin revienta, el árbol se va— y entonces la línea que libera el estado no se ejecuta nunca. Ese patrón mordió tres veces en el mismo fichero, y las tres con precio distinto: pantalla bloqueada para siempre, una unidad que no vuelve a precargarse nunca, y un botón muerto. Los tres se cierran igual: el estado **caduca** en vez de fiarse de su propia liberación.

### Identidad y guardado en la nube

Jugar no requiere cuenta: sesión anónima por dispositivo. Vincular Google es opcional y **convierte la cuenta anónima en permanente conservando el mismo `auth.uid()`**, así que puntuaciones, perfil y guardado sobreviven sin migrar nada.

Los tres casos difíciles:

1. **Vincular a una cuenta de Google que ya tiene identidad propia** (reinstalar, cambiar de móvil) es el caso *frecuente*, no el excepcional. Se detecta, se cae a un inicio de sesión normal y se abre un diálogo que compara los dos progresos para que el jugador elija; la cuenta anónima huérfana se borra para no duplicarlo en el ranking.
2. **Un enlace que triunfa en el servidor pero cuya respuesta se pierde** (tiempo de espera en red móvil) devuelve "esa identidad ya existe" **sobre uno mismo** al reintentar. Sin una comprobación explícita, el flujo de conflicto acababa borrando la propia cuenta.
3. **Transferir progreso a otro dispositivo** es *mover*, no copiar: el canje planta una lápida que el dispositivo origen consume en su siguiente arranque y limpia lo local. Sin eso, el origen vuelve a subir su copia intacta y duplica compras en bucle.

El guardado local usa **escritura atómica propia**: fichero temporal, relectura y validación, rotación del actual a `.bak`, renombrado. El modo `WRITE` de Godot trunca al abrir, así que un proceso muerto a media escritura dejaba el fichero vacío y el jugador perdía monedas, estrellas e inventario de golpe — riesgo nada teórico, porque varios servicios vuelcan a disco justo en `APPLICATION_PAUSED`. La restauración desde la nube es además transaccional, con un centinela que permite reanudarla si muere a mitad.

### Interruptor remoto de versión

Google Play no fuerza nada por su cuenta: una build vieja se abre igual para siempre. Dos umbrales en una tabla del servidor —aviso y bloqueo— permiten sacar de circulación una build rota sin publicar nada, y sirven de *kill switch*.

Tres propiedades decididas a propósito:

- **Falla en abierto.** Sin red, con la RPC caída o con una respuesta ilegible, se juega. Bloquear a quien no ha podido verificar deja tirado a cualquiera en el metro.
- **"No aplica" y "no lo he podido comprobar" son estados distintos.** Colapsarlos dejaba al cliente convencido de estar al día durante todo el proceso; separados, el segundo reintenta con esperas crecientes.
- **El aviso sale una vez por versión**, no una por arranque —se convierte en la pantalla que se cierra sin leer— ni una por instalación, que silenciaría todas las actualizaciones futuras.

La comparación de versiones es numérica por tramos y tolerante a formatos raros: un `1.10 < 1.9` lexicográfico habría bloqueado a todo el que estuviera en la 1.10.

### Telemetría y balance por datos

Cada partida terminada manda a Supabase una fila con ~40 campos: resultado, causa de derrota, hasta dónde llegó la cadena, precisión, desglose de la puntuación, objetos usados, tiempo neto de pausas y la dificultad real con la que se jugó. Hay agregados por jugador y nivel, purga automática a 90 días, límite de frecuencia por clase de fila y un interruptor en Opciones por GDPR.

**Para qué sirve de verdad:** el listón de las estrellas de cada nivel se calibra con `percentile_cont` sobre las puntuaciones reales, no a ojo. Y las decisiones de diseño se toman con la medida delante:

- La curva de dificultad se aplanó al comprobar que del mundo 5 al 9 la exigencia se movía ±3 % y el mundo 10 estaba **por debajo** del 3.
- Una familia de misiones se reescribió entera al descubrir que el jugador más activo llevaba **cero monedas de misiones en 78 partidas**: tres objetivos eran matemáticamente inalcanzables, y uno pedía un combo que no había salido ni una vez en 268 partidas.
- El listón de la tercera estrella se bajó al medir que **ninguna de 51 victorias** llegaba a él; la mejor se quedó a un 1,3 %.

> **Y un fallo de datos que costó seis días.** La puntuación de un combate multifase llegaba con la primera fase contada dos veces. No daba error: el único síntoma era un residuo en una comprobación de consistencia, y se explicó con una hipótesis razonable y falsa. Sobre esos ratios inflados se recalibraron cuatro combates **en la dirección contraria**, dejándolos regalados durante casi una semana. La lección quedó escrita en el repositorio: un residuo sistemático se **contrasta con otra fuente** antes de explicarlo — bastaba comparar contra la tabla que el ranking escribe por otro camino.

### Anti-trampas: modelo de amenaza explícito

Lo importante aquí no es la lista de defensas, es dónde está la línea y por qué.

**Lo que el servidor impone**, y no depende del cliente: topes por puntuación enviada, límite de frecuencia por jugador, lista blanca de mundos y niveles, guards de propiedad en cada RPC, y triggers de tabla —no un `if` repartido por seis funciones— para que un jugador sancionado no pueda escribir en ningún tablero, hoy ni en el séptimo tablero que se añada dentro de un año.

**Lo que se asume perdido**: en un dispositivo con acceso a ficheros, el monedero es un JSON local. Quien pueda editarlo no necesita trampear ninguna compra. Cerrarlo exigiría mover toda la economía al servidor, que es un coste que este proyecto no paga.

**Lo que sí queda cerrado, porque es lo que cuesta dinero**: que una compra real no se pueda convertir en dos. Las defensas se dimensionan con esa jerarquía delante — blindar las misiones dejando el monedero en local sería seguridad de escaparate.

Todo eso está razonado por escrito en un documento de diseño interno, incluida la decisión de **no** llevar los contadores de misiones a la base de datos: un servidor no puede validar una misión sin validar el gameplay, así que sigue siendo el cliente quien dice "hecho".

### Moderación y soporte dentro de la app

Con jugadores reales aparecen problemas que no son técnicos, y necesitan herramientas.

- **Panel de administración dentro del juego**, con el rol verificado en el servidor (`auth.uid()`, nunca un parámetro): buscador de jugadores, ficha completa, sanciones reversibles y utilidades de desarrollo. La función que asigna roles **no se expone**: su abuso es irreversible por definición, así que se queda en el panel de la base de datos. Un administrador no puede sancionar a otro ni a sí mismo.
- **Denuncias entre jugadores** con cinco defensas contra la campaña coordinada —una fila por pareja, límite diario, exigir haber jugado, un sancionado no denuncia, purga acotada— y **sin sanción automática**: el recuento ordena la lista, pero decidir sigue siendo un botón que pulsa una persona.
- **Contacto y apelación in-app**: el jugador escribe dentro del juego y la respuesta le llega a su buzón. Un sancionado **sí puede escribir**, porque es su única vía de apelación y cerrarla dejaría cualquier error sin vuelta atrás.
- **Traducción del soporte** con DeepL a través de una Edge Function, porque el juego se publica en diez idiomas. La clave vive en el servidor y el endpoint comprueba el rol del llamante: sin eso es un proxy de traducción de pago gratis para cualquiera que lea la clave del APK.

### Internacionalización

**1.155 claves × 10 idiomas** (EN, ES, CA, pt-BR, FR, IT, DE, JA, KO, RU) desde un CSV único que compila el importador de Godot; el CSV no se lee en runtime. Detección automática del idioma del sistema en el primer arranque y cambio en caliente.

Lo que aprendí haciéndolo, que no aparece en ningún tutorial:

- **Sin plurales.** El objetivo no va en la frase, va en la barra de progreso. Con el ruso teniendo tres formas de plural, meter `{n}` en cada cadena es la vía rápida a traducciones rotas. Cuando sí hay cifra, la unidad va en la etiqueta y el valor va solo: `DÍAS DE RACHA: 3` en lugar de `3 DÍAS`, que el primer día de cualquier instalación mostraba **"1 DÍAS"** en ocho idiomas.
- **La concordancia de género es el mismo problema con otra cara**, y la salida no es una tabla de géneros: es escribir una frase que no concuerde.
- **El texto es una restricción de layout, no un detalle final.** Hay arneses que miden el ancho real de cada botón en los diez idiomas contra su hueco, porque una etiqueta que se pasa no se recorta: **ensancha el contenedor**, y en un panel centrado eso lo saca por los dos lados sin que el layout se queje.
- **Una auditoría de vocabulario por idioma** encontró hasta cuatro palabras distintas para el mismo concepto dentro de un mismo idioma —el tutorial usaba un término que no volvía a aparecer en todo el juego— y dos cadenas que decían algo **falso**: una prometía a los jugadores coreanos que no podían escribir su nombre en su alfabeto, cuando sí podían.

### Accesibilidad

Modo daltónico con dos interruptores independientes: paleta alternativa y figuras geométricas sobre el orbe.

La primera paleta **no funcionaba**, y lo dijo un jugador daltónico real: "lo veo prácticamente igual". Medida con la transformación de Viénot-Brettel-Mollon sobre el color que sale del shader, en deuteranopia dos de los cuatro colores quedaban a distancia 23, y en escala de grises los cuatro caían dentro de 5,6 — colapsaban a dos colores. La paleta actual (Okabe-Ito adaptada) sube el peor caso a 17,2, y lo que de verdad la separa **es la luminosidad** (L\* 43 / 60 / 79 / 97), que es lo único que conserva cualquier tipo de daltonismo.

Aun así, el color solo no basta: un optimizador sobre los cuatro tipos a la vez topa alrededor de distancia 20. Por eso el canal primario son las **figuras**, con el grosor del contorno medido a la resolución real en la que se pintan — sobre un orbe claro, un relleno blanco tiene contraste 1,06:1 contra el cuerpo, así que la figura se lee solo por su borde. Y las texturas del modo clásico se **generan** con la misma fórmula del shader, para que un orbe se vea igual con y sin skin por construcción.

### Estrategia de pruebas sin CI

**130 scripts de QA en GDScript**, ejecutables en headless, más un lanzador que los corre todos y resume qué falla. No hay framework de testing: son scripts que montan el juego de verdad, hacen algo y miden.

Los principios que hacen que sirvan para algo:

- **Verificación por mutación.** Un arnés que nunca ha estado en rojo no prueba nada. Casi todos se validan reintroduciendo a mano el fallo que persiguen y comprobando que dan rojo. Varias veces eso destapó que la prueba medía otra cosa: una comprobación buscaba un identificador que también aparecía en un comentario, así que pasaba en verde con la línea borrada.
- **Medir el resultado, no el código fuente.** "¿Me llevo algo en modo avión?" se responde midiendo el saldo antes y después, no leyendo el `if`.
- **El arnés monta el estado que quiere medir, nunca lo hereda.** Varias pruebas fallaban o pasaban según quién las lanzara, porque leían el progreso real de la máquina. Y todo script que escriba en disco pasa por una red de seguridad que respalda y restaura los ficheros de guardado, con identificación por PID, porque dos arneses en paralelo se pisaban el respaldo.
- **Hay cosas que solo se ven mirando.** Un efecto de partículas nacía entero fuera de pantalla y su propio comentario afirmaba lo contrario; el estado del árbol de nodos era perfecto. Para eso los arneses de captura rasterizan y **miden el píxel**: el oscurecido de un velo se comprueba por luminancia media, no por el valor de la propiedad `alpha`.
- **La primera pasada completa del lanzador encontró tres arneses en rojo sobre código sano**: comprobaciones ancladas a la posición de un literal que había cambiado de sitio. Un arnés que falla sin motivo es peor que no tenerlo, porque enseña a ignorar los rojos.

Además: un fuzzer que dispara a puntos aleatorios durante miles de frames sobre una muestra de niveles, con semilla derivada de la ruta para que un fallo se reproduzca, y un script que carga todos los GDScript del proyecto para cazar errores de compilación que ninguna prueba tocaría — el fichero raíz de la aplicación no lo compila ningún arnés, y un error de sintaxis ahí deja el juego sin arrancar con toda la batería en verde.

### Herramientas propias

- **Plugin de editor de Godot** (`EditorPlugin` + `@tool` + `_forward_canvas_gui_input`): Shift+clic en el viewport para trazar los caminos, con sufijos en el nombre del marcador que definen tramos especiales (portal, no enganchable, dos capas de profundidad, fin del sprint de entrada) y renumeración automática en dos pasadas.
- **Scripts Python** para lo que no debe hacerse a mano: medición de la longitud real de los 92 caminos —replicando la métrica exacta del juego— para recalibrar la velocidad por nivel, generación de las texturas del modo daltónico, preparación de skins de orbe con remapeo de rango tonal, y regeneración de todos los assets de la web al tamaño en que se pintan.
- **Simulador en Node** de la demo del canvas de la landing, que lee las constantes del propio HTML. En el navegador la medición miente: con la pestaña en segundo plano `requestAnimationFrame` baja a 1 fps y cualquier conteo sale a cero.

### Rendimiento y despliegue en Android

- Compresión de texturas VRAM dual (escritorio y Android) con auditorías automáticas de los ficheros de importación: Godot crea el `.import` de una textura nueva con los valores por defecto y no hereda los de sus vecinas — 40 texturas entraron sin comprimir en una sola tanda, sin dar ningún aviso.
- Presupuesto de assets vigilado: 45 retratos de perfil pasaron de PNG a JPG (4,2 MB → 1,7 MB) por ser ilustraciones opacas, que es justo lo que peor comprime en PNG.
- Límite de FPS configurable (30/60) y nunca "sin límite", por estrangulamiento térmico. Los topes de velocidad de la simulación van en píxeles por **segundo**, no por frame, o el ajuste de FPS cambiaría la velocidad de la simulación — inadmisible con un ranking detrás.
- Cumplimiento de Google Play: política de privacidad propia con GDPR/RGPD, borrado de cuenta in-app (RPC + cascada + limpieza local, incluida la fila de `auth.users`, que es donde vive el correo), declaración de Data Safety sincronizada con lo que la app hace de verdad, y clasificación IARC.

---

## Qué demuestra el proyecto

Traducido a lo que se busca en una oferta:

| Competencia | Dónde está en el proyecto |
|---|---|
| **Diseño de bases de datos** | 27 esquemas, 112 RPC, RLS, triggers, índices parciales, jobs con `pg_cron` |
| **Optimización de consultas** | Banco de 200.000 filas, `EXPLAIN (ANALYZE, BUFFERS)`, `JOIN LATERAL`, autovacuum afinado, verificación fila a fila antes de desplegar |
| **Seguridad** | Pentest de la API pública, `SECURITY DEFINER` con `search_path` fijo, grants columnares, modelo de amenaza escrito |
| **Integración de pagos** | Billing con verificación en servidor, idempotencia, doble entrega cerrada con tres cinturones, reembolsos automatizados |
| **Optimización de rendimiento** | Perfilado, cuello de botella algorítmico identificado y medido (x18), presupuesto de assets |
| **Arquitectura** | Fachadas sobre SDK nativos, router único de navegación, separación entre estado guardado y estado pintado |
| **Testing** | 130 scripts de QA, verificación por mutación, fuzzing, pruebas que miden píxeles |
| **Ingeniería de datos** | Telemetría con retención automatizada y decisiones de producto tomadas con percentiles reales |
| **i18n y a11y** | 10 idiomas con auditoría de vocabulario; accesibilidad para daltonismo validada con literatura científica y con un usuario real |
| **Cumplimiento** | GDPR, Play Data Safety, borrado de cuenta, moderación, política de privacidad mantenida |
| **Autonomía** | De la idea a la tienda sin equipo: producto, backend, cliente, arte de UI, web, legal y operación |

Y una cosa que no cabe en la tabla: **la documentación**. El repositorio del juego lleva un mapa de decisiones donde cada elección no obvia está escrita con su porqué, su medida y lo que costó el error anterior. Muchos de los avisos que citan estas secciones vienen de ahí. Es lo que hace que un proyecto de 98.000 líneas escrito por una persona siga siendo modificable un año después.

---

## Contacto

**Aleix** — desarrollo, backend, diseño, arte de UI y web.

- Email: [aleixauque@gmail.com](mailto:aleixauque@gmail.com)
- Web: [aleixaj.com](https://aleixaj.com)
- El juego: [Orbex en Google Play](https://play.google.com/store/apps/details?id=com.aleix.orbex) · [orbex.aleixaj.com](https://orbex.aleixaj.com)

> El código del juego es privado. Puedo enseñarlo o comentar cualquiera de los sistemas de arriba en una entrevista.
