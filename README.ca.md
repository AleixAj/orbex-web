# Orbex — landing pública + memòria tècnica del joc

![Godot](https://img.shields.io/badge/Godot-4.6-478CBF?style=for-the-badge&logo=godotengine&logoColor=white&labelColor=2D2D2D)
![GDScript](https://img.shields.io/badge/GDScript-tipatge_estàtic-355170?style=for-the-badge&logo=godotengine&logoColor=white&labelColor=2D2D2D)
![PostgreSQL](https://img.shields.io/badge/Supabase-PostgreSQL_+_RLS-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white&labelColor=2D2D2D)
![Deno](https://img.shields.io/badge/Edge_Functions-TypeScript-000000?style=for-the-badge&logo=deno&logoColor=white&labelColor=2D2D2D)
![Google Play](https://img.shields.io/badge/Google_Play-publicat-3DDC84?style=for-the-badge&logo=googleplay&logoColor=white&labelColor=2D2D2D)
![Landing](https://img.shields.io/badge/Landing-HTML_+_CSS_+_JS_vanilla-e34f26?style=for-the-badge&logo=html5&logoColor=white&labelColor=2D2D2D)

<p>
  <a href="README.md"><img src="docs/readme/lang-es.svg" alt="Español" width="170"></a>
  <a href="README.en.md"><img src="docs/readme/lang-en.svg" alt="English" width="170"></a>
  <img src="docs/readme/lang-ca-active.svg" alt="Català" width="170">
</p>

**Orbex** és un joc per a mòbil publicat a Google Play ([`com.aleix.orbex`](https://play.google.com/store/apps/details?id=com.aleix.orbex)), fet de cap a peus per una sola persona: client, backend, base de dades, pagaments, telemetria, compliment legal i la web que l'acompanya.

**Aquest repositori conté la landing** ([orbex.aleixaj.com](https://orbex.aleixaj.com)). El codi del joc és privat, així que **aquest document n'és la memòria tècnica**: com està muntat per dins, quins problemes d'enginyeria van aparèixer de debò i com es van resoldre.

> **Per què et pot interessar encara que no et dediquis als videojocs.** El joc és l'excusa; la feina és de programari. Aquí hi ha un backend PostgreSQL en producció amb RLS i pentest, un sistema de pagaments amb verificació al servidor i idempotència davant del doble cobrament, consultes optimitzades contra un banc de 200.000 files, telemetria amb retenció automatitzada, compliment del GDPR i de Play Data Safety, i una bateria de proves verificada per mutació. Res d'això no és específic d'un joc.

---

## Índex

- [El projecte en xifres](#el-projecte-en-xifres)
- [Part 1 — La landing (aquest repositori)](#part-1--la-landing-aquest-repositori)
- [Part 2 — El joc](#part-2--el-joc)
  - [Stack i forma del projecte](#stack-i-forma-del-projecte)
  - [Contingut i modes de joc](#contingut-i-modes-de-joc)
  - [Arquitectura del client](#arquitectura-del-client)
  - [El motor de cadena, i una optimització amb mesura](#el-motor-de-cadena-i-una-optimització-amb-mesura)
  - [Backend: model de dades i API](#backend-model-de-dades-i-api)
  - [Seguretat del backend](#seguretat-del-backend)
  - [Escala: el que es trenca amb volum](#escala-el-que-es-trenca-amb-volum)
  - [Pagaments in-app](#pagaments-in-app)
  - [Publicitat](#publicitat)
  - [Identitat i desament al núvol](#identitat-i-desament-al-núvol)
  - [Interruptor remot de versió](#interruptor-remot-de-versió)
  - [Telemetria i equilibri basat en dades](#telemetria-i-equilibri-basat-en-dades)
  - [Anti-trampes: model d'amenaça explícit](#anti-trampes-model-damenaça-explícit)
  - [Moderació i suport dins l'app](#moderació-i-suport-dins-lapp)
  - [Internacionalització](#internacionalització)
  - [Accessibilitat](#accessibilitat)
  - [Estratègia de proves sense CI](#estratègia-de-proves-sense-ci)
  - [Eines pròpies](#eines-pròpies)
  - [Rendiment i desplegament a Android](#rendiment-i-desplegament-a-android)
- [Què demostra el projecte](#què-demostra-el-projecte)
- [Contacte](#contacte)

---

## El projecte en xifres

| | |
|---|---|
| Codi del client | **265 fitxers GDScript**, ~98.000 línies, tipatge estàtic |
| Backend | **27 fitxers SQL**, ~11.000 línies, **113 funcions/RPC** a PostgreSQL |
| Serverless | 3 **Edge Functions** en TypeScript: verificació de compres, sincronització de reemborsaments i traducció del suport |
| Proves | **132 scripts de QA** headless (arnesos, dobles, fuzzing i mesurament), la majoria verificats per mutació |
| Contingut | 256 escenes, **92 nivells**, 10 mons, 16 combats contra caps, 3 modes de joc |
| Catàleg | 214 cosmètics, 75 fites, 54 missions, 9 objectes consumibles |
| Localització | **1.155 claus × 10 idiomes** |
| Serveis globals | 26 autoloads: economia, progrés, rànquing, esdeveniments, pagaments, anuncis, ajustos… |
| Estat | Publicat a Google Play, versió **1.30**, amb jugadors, anuncis i compres reals |

---

## Part 1 — La landing (aquest repositori)

Lloc estàtic que serveix alhora de pàgina de producte i d'URL de la política de privadesa que exigeix Google Play.

### Stack

**HTML5 + CSS amb custom properties + JavaScript vanilla.** Zero build, zero dependències en runtime i zero peticions a tercers: la pàgina sencera se serveix des del mateix domini.

És una decisió, no una limitació. Una landing d'una sola pàgina no necessita bundler, framework ni pipeline: necessita carregar ràpid, ser indexable i no trencar-se. Sense build, desplegar és copiar la carpeta, i l'HTML que veu Google és el mateix que vaig escriure.

### El que té per dins

| | |
|---|---|
| **Bilingüe EN/ES** | Els dos idiomes viuen al mateix HTML (`<span data-lang>`), els commuta el CSS i la preferència persisteix a `localStorage`. Sense JS també es veu un idioma complet |
| **Tema clar/fosc** | Automàtic per `prefers-color-scheme` a la primera visita, persistent després |
| **Demo interactiva en `<canvas>`** | Recreació de la mecànica del joc: una cadena sobre una polilínia Catmull-Rom parametritzada per longitud d'arc, amb la mateixa lògica d'inserció i cascada. Explica el joc sense demanar al visitant que miri un vídeo |
| **Build web jugable** | Export HTML5 del joc real allotjat a itch.io, enllaçat des del hero i des dels dos menús. S'obre en una pestanya a part i no com a *embed*, que és el que manté la promesa de zero peticions a tercers |
| **Accessibilitat** | Skip link, `aria-expanded` / `aria-controls`, `:focus-visible` propi, modals amb el focus atrapat i retornat, tancament amb Escape, i respecta `prefers-reduced-motion` |
| **SEO** | Open Graph, `hreflang`, sitemap i JSON-LD (`VideoGame` + `FAQPage`) sincronitzat amb el contingut visible |
| **Sense bàner de galetes** | L'embed de YouTube neix sense `src` (patró *click-to-load*) i les fonts estan autoallotjades, així que no hi ha cap petició a tercers fins que l'usuari la demana |

### Rendiment

Els assets van passar de **42 MB a 2,6 MB (−94 %)** en la passada d'optimització. Avui la carpeta pesa **4,7 MB** —ha crescut amb la galeria— i el que importa continua mesurat: recórrer la pàgina sencera són **496 KB en 30 peticions, cap a tercers** (mesurat contra producció, no contra el servidor local).

- Els 10 retrats de cap eren 34 MB d'aquells 42: PNG de 1152×2048 que es pinten a ~210 px d'amplada. Cada asset es regenera a la mida a què es pinta (2× la del CSS) en `.webp`, amb un script Python reproduïble.
- La galeria té dues resolucions per imatge: miniatura de 720 px per a les targetes i 1280 px per al visor.
- Les tres fonts van autoallotjades amb subset llatí (**49 KB en total**), en lloc de dues connexions a tercers i un full d'estils bloquejant al camí crític.
- Un únic listener de scroll per a les tres coses que en depenen, que escriu un cop per frame amb `requestAnimationFrame`. Les animacions decoratives es congelen mentre hi ha un modal obert: animaven `filter` i `background-position`, que repinten en lloc de compondre.

### Desplegament

Qualsevol host estàtic. És a **Cloudflare Pages** amb domini propi, i també hi ha configuració a punt per a Netlify i Vercel. Les capçaleres de memòria cau (`immutable` a fonts i imatges) es declaren en els tres formats.

### Estructura i desenvolupament local

```
orbex-web/
├── index.html              landing bilingüe (11 seccions, demo en canvas)
├── privacy/index.html      /privacy — política servida
├── PRIVACY.md              font de veritat bilingüe de la política
├── assets/
│   ├── fonts/              3 woff2 amb subset llatí (49 KB)
│   └── images/             wordmark, mons, caps, orbes, captures, banderes
├── _headers · _redirects · netlify.toml · vercel.json
└── scratchpad/             eines (no es desplega)
```

```bash
python scratchpad/serve.py     # http://localhost:8000
```

És `python -m http.server` amb dues coses a sobre, i totes dues calen: `Cache-Control: no-store` —el servidor nu desa l'HTML a la memòria cau de manera agressiva i, si edites el fitxer, en recarregar no es veu el canvi— i els tipus MIME de `.webp` i `.woff2`, sense els quals Chrome rebutja les fonts **en silenci** i la pàgina recorre a la del sistema, cosa que sembla un problema de CSS.

La **política de privadesa** viu en dos fitxers que s'editen sempre alhora (`PRIVACY.md` i la pàgina servida) i ha d'anar per davant del que fa l'app, no per darrere: la versió anterior va continuar dient "no mostrem anuncis" durant dues setmanes en què l'SDK ja era dins de la build — i aquesta és justament una de les frases que Google Play contrasta amb la declaració de Data Safety.

---

## Part 2 — El joc

### Stack i forma del projecte

| | |
|---|---|
| Motor | Godot 4.6, perfil Mobile (`gl_compatibility`) |
| Llenguatge | GDScript amb tipatge estàtic i `class_name` |
| Plataforma | Android, horitzontal, base 1280×720, `minSdk 24` / `targetSdk 36`, `arm64-v8a` |
| Backend | Supabase — PostgreSQL + PostgREST + Auth anònima + Edge Functions (Deno/TS) |
| Persistència local | Fitxers JSON a `user://` amb escriptura atòmica pròpia |
| Serveis natius | Google Play Billing 8.3.0, AdMob amb el flux de consentiment UMP, Google Sign-In |

### Contingut i modes de joc

10 mons ambientats en èpoques històriques, 8 nivells cadascun i un combat contra un cap que tanca cada món —quatre en dues fases i l'últim en tres, amb un trencament de pantalla entre fase i fase—, més un tutorial de cinc pantalles encadenades.

Sobre aquest mateix contingut funcionen **dos modes més i un esdeveniment setmanal**, i aquí és on hi ha la part d'enginyeria: un mode no és contingut nou, és un joc de banderes sobre el mateix nivell. El que és delicat no és el que fa cada mode, sinó **què se li permet escriure**.

| Mode | Què canvia | Què no pot tocar |
|---|---|---|
| **Supervivència** | El subministrament d'orbes no s'esgota i la velocitat puja segons els orbes destruïts, no amb el temps. Sense objectes, sense victòria possible | Estrelles i rècord de campanya. Tauler propi |
| **Infernal** | La campanya sencera rejugada més difícil. S'obre en acabar els 10 mons i dona accés als 80 nivells de cop | El progrés de campanya: llibreta d'estrelles i rècords **separada**, i tauler a part |
| **Repte setmanal** | Un nivell triat pel servidor, el mateix per a tothom, que es pot jugar encara que el seu món estigui bloquejat | Res del jugador: ni estrelles, ni monedes, ni missions, ni fites |

Tres lliçons que van sortir de construir-los:

- **La separació de llibretes es fa abans d'apujar la dificultat, no després.** Mentre Infernal i campanya pesaven el mateix, barrejar-ne els rècords donava gairebé el mateix resultat i semblava codi de més. Tan bon punt el mode estreny, barrejar-los vol dir **esclafar el rècord de campanya del jugador amb una marca feta en un altre joc**, i això ja no s'arregla a posteriori.
- **L'aïllament són dues meitats, i la que s'oblida és la que s'executa en viu.** El repte bloquejava el que s'escriu *en acabar* la partida, però els comptadors de combos i trets es registren tret a tret: durant un temps, una partida d'un mode declarat aïllat continuava desbloquejant fites i fent avançar missions. No va donar cap error — es va veure mirant el compte d'un jugador que només havia jugat l'esdeveniment.
- **Un mode que es pot repetir sense límit no pot alimentar un comptador.** Supervivència i Infernal es rejuguen sense cost, així que les seves fites compten *nivells diferents* i no partides. Amb un comptador, l'escala sencera —2.050 monedes— es tanca en una tarda repetint el primer nivell del joc.

**Esdeveniment de temporada.** Una divisa paral·lela que es guanya jugant i **caduca**, bescanviable per un catàleg cosmètic propi dins de la seva finestra de dates. Té tres fases i la del mig és la que no és òbvia: després que es tanqui el repartiment hi ha un període de **liquidació** en què ja no es guanya però encara es pot gastar. Sense aquest període, l'esdeveniment castiga justament qui ha jugat fins a l'últim dia i es troba el saldo evaporat — que és exactament el que ensenya a no molestar-se en l'esdeveniment següent. El que s'ha comprat es queda per sempre; el que caduca és la divisa.

### Arquitectura del client

```
+-------------+     +----------------------+     +--------------------+
|  AppRouter  |---->|  OrbexScreen (UI)    |---->|  Nivell (main.gd)  |
| (main.tscn) |     |  menú / món / mapa   |     |  + HUD overlay     |
+-------------+     +----------------------+     +--------------------+
       |                                                    |
       v                                                    v
+-------------+                                    +--------------------+
|  Autoloads  |  progrés · economia · xarxa        |  ChainBall x N     |
|    (26)     |  ajustos · events · pagaments      |  ProjectileBall    |
+-------------+                                    |  Boss              |
       |                                           +--------------------+
       v
+---------------------------------------------------------------------+
|  Supabase — PostgREST (113 RPC) · RLS · pg_cron · Edge Functions     |
+---------------------------------------------------------------------+
```

Tres regles sostenen la separació:

- **`AppRouter` és l'única via per canviar de pantalla.** Cap pantalla no navega a una altra: totes l'hi demanen al router. Això concentra en un sol lloc la càrrega d'escenes, els modals, la pila del botó enrere d'Android i el cicle de vida de la partida.
- **Els SDK natius entren per una porta i només per una.** `Ads` i `Purchases` són autoloads-façana: cap pantalla no parla amb el plugin de Java. Es demana `await Ads.request_reward(placement)` o `Purchases.buy(sku)` i prou. El dia que calgui portar-lo a iOS (StoreKit) o canviar de proveïdor d'anuncis, el canvi queda dins de dos fitxers en lloc d'estar repartit per les cinc pantalles que reparteixen diners.
- **El que es DESA i el que es PINTA són coses diferents.** Un cosmètic equipat es conserva al disc encara que el desbloqueig no es pugui confirmar en aquell moment (arrencada sense xarxa, rol del servidor que encara no ha arribat); el que canvia és què es dibuixa. Sense aquesta separació, una arrencada sense cobertura destruïa la selecció del jugador de manera permanent, perquè el desament següent feia definitiva la pèrdua.

### El motor de cadena, i una optimització amb mesura

El nucli del joc és una filera d'orbes que avança per un camí i admet insercions en qualsevol punt: posició per longitud d'arc (`path_progress`), inserció interpolada, empenta de la subcadena per obrir un forat, recol·locació després d'una eliminació i unió magnètica de dos trams separats quan comparteixen color. Un nivell pot tenir diversos carrils independents.

**El problema.** La funció que col·loca cada orbe feia cinc consultes al camí per bola i per frame (posició, trams amb portal, trams no enganxables i dues capes de profunditat), i totes cinc eren **escombratges lineals del camí sencer**. Els camins es tracen a mà i són densos: 164 punts al primer nivell, **361 al més llarg**. El cost anava amb `boles × punts_del_camí`, no amb boles.

**La mesura.** Amb un banc de frames instrumentat, el nivell més car costava **3,9 ms per frame amb 72 orbes** en una partida normal, i **9,1 ms** en el mode supervivència, que deixa anar el límit d'orbes en pantalla. A 60 fps, el pressupost sencer d'un frame són 16,6 ms.

**La solució.** Cerca binària sobre les distàncies acumulades del camí, més índexs precalculats dels trams marcats. Amb un detall que no perdona: els trams de teletransport mesuren 0 px, així que hi ha valors repetits i cal un `lower_bound` real —quedar-se amb el primer dels empats— en lloc d'una cerca binària genèrica. Amb la genèrica, un orbe surt pel portal equivocat.

| | abans | després |
|---|---|---|
| Nivell més car, partida normal | 3,90 ms/frame | **0,22 ms** |
| Nivell més car, mode supervivència | 9,10 ms/frame | **2,94 ms** |

**La verificació.** Vaig reimplementar les cinc versions lineals dins de l'arnès de proves i les vaig comparar amb les noves sobre **els 92 nivells i els seus 112 carrils**: 178.303 mostres, escombratge fi més les vores exactes de cada segment i els seus veïns a un èpsilon. D'aquestes funcions depenen on es dibuixa cada orbe, el fos dels portals i si un tret travessa un tram. Un *off-by-one* aquí no el caça cap altra prova i no dona error: simplement es veu malament.

### Backend: model de dades i API

**Supabase, amb tota la lògica en funcions de PostgreSQL.** El client no fa `INSERT` ni `UPDATE` contra cap taula: cada escriptura passa obligatòriament per una RPC `SECURITY DEFINER` que valida abans d'escriure.

Subsistemes amb esquema propi:

| Subsistema | Què resol |
|---|---|
| Rànquing | Taulers paginats per àmbit i nivell, posició exacta del jugador i veïnat (tu ± N rivals) |
| Perfils públics | Fitxa d'un altre jugador: sobrenom, cosmètics equipats i estadístiques |
| Cloud save | Còpia del progrés i codis de transferència entre dispositius, d'un sol ús i amb caducitat |
| Compres | Catàleg, bescanvi de rebuts, lliurament idempotent i revocació per reemborsament |
| Repte setmanal | Nivell sortejat al servidor, el mateix per a tothom, amb tauler propi i premis automàtics |
| Bústia | Missatgeria del servidor al jugador, amb lectura i cobrament de recompenses |
| Amics | Alta unilateral, notificacions i tauler filtrat |
| Moderació | Sancions, denúncies entre jugadors i suport in-app |
| Telemetria | Una fila per partida més agregats, amb purga automàtica |

Vuit tasques programades amb **`pg_cron`**: set de nocturnes —purga de telemetria als 90 dies, roll-up diari d'usuaris actius, neteja de comptes anònims orfes, sincronització de reemborsaments amb Google i la retallada de notificacions d'amics, denúncies i missatges de suport— més el tancament setmanal del repte, que reparteix els premis per la bústia.

> El que no es purga és tan deliberat com el que sí: una denúncia sense resoldre o un missatge de suport sense resposta **no s'esborren per vells**, perquè són justament el que encara no ha atès ningú.

### Seguretat del backend

La clau anònima va incrustada a l'APK per disseny, així que **el model d'amenaça assumeix que qualsevol pot invocar qualsevol RPC amb qualsevol argument**. El que impedeix l'abús és el servidor, mai la pantalla.

- **Tota funció `SECURITY DEFINER` fixa el seu `search_path`.** Sense això, un `search_path` manipulat segresta les crides de dins del cos.
- **Cap taula no té política d'escriptura.** RLS és l'única barrera i no es desactiva en cap.
- **Guards de propietat** (`auth.uid() = p_id`) a tota RPC que accepti un identificador de jugador.
- **Grants per columnes** sobre la taula de jugadors: la lectura pública serveix 16 columnes de perfil, i l'economia, la telemetria i l'estat de sanció en queden fora.
- **A `anon` li arriben set funcions, i totes set són de lectura.**

> **Un error real que ensenya la lliçó.** `REVOKE EXECUTE ... FROM anon` **no fa res per si sol**: PostgreSQL concedeix `EXECUTE` a `PUBLIC` en crear qualsevol funció, i els rols n'hereten. La forma correcta és `FROM public, anon`. Tretze funcions tenien aquest error i una era greu: la que assigna rols va quedar accessible des de l'API pública, és a dir, qualsevol amb la clau de l'APK es podia concedir permisos d'administrador. Corregit i verificat amb un **pentest de 8 vectors** —assignació de rol, escriptura directa a taules, enviament de puntuacions, esborrament d'un compte aliè, restauració d'un progrés aliè—: tots bloquejats, amb les dades de la víctima intactes.

També hi ha una norma de verificació: una RPC no es dona per bona fins que **no s'ha cridat contra la base de dades**. Dues funcions es van crear sense cap queixa i van petar en executar-se — una per una variable amb el mateix nom que una columna (`plpgsql` resol primer contra les seves variables), l'altra per tractar com a booleà una funció que llança una excepció. Els assajos funcionals es fan amb un bloc `DO` que acaba en `raise exception`: la transacció s'avorta sola i no hi persisteix ni una fila.

### Escala: el que es trenca amb volum

Amb 20 jugadors tot va ràpid. Els problemes apareixen amb un cens gran, així que les consultes crítiques es van mesurar contra un **banc de 200.000 jugadors i 400.000 files de puntuació**, amb `EXPLAIN (ANALYZE, BUFFERS)`.

**1. L'`OR` del desempat impedia fer servir l'índex.** "Quanta gent va per davant meu" es tradueix de manera natural a `score > X OR (score = X AND fecha < Y)`, i el planificador no pot acotar per índex cap branca dins d'un `OR`: recorre a un escaneig amb la condició com a filtre. Partit en dos recomptes per rang —els conjunts són disjunts—, cada branca entra per l'índex.

| | pla | buffers | ms |
|---|---|---|---|
| Abans | Bitmap Heap Scan de 154.915 files | 2.283 | 28,9 |
| Després | dos Index Only Scan, `Heap Fetches: 0` | **618** | 18,8 |

**2. Un `JOIN` normal es llegia la taula de jugadors sencera a cada crida.** El `LIMIT` d'una pàgina és un valor de *runtime*, així que el planificador estimava milers de files, triava Hash Join i feia `Seq Scan on players`. Un `JOIN LATERAL` no es pot resoldre amb *hash* join, de manera que força el Nested Loop contra la clau primària i el join s'aplica només a les 50 files de la pàgina. És una constant que creix amb el **cens**, no amb qui juga:

| | abans | després |
|---|---|---|
| Primera pàgina del rànquing | 1.432 buffers / 11,1 ms | **785 / 2,6 ms** |
| Primera pàgina de supervivència | 2.505 / 31,6 ms | **885 / 4,8 ms** |

**3. Autovacuum afinat.** Els taulers reben un `upsert` per partida jugada, i els `Index Only Scan` depenen del mapa de visibilitat. Amb el valor per defecte, la neteja no es dispara fins que el 20 % de la taula són tuples mortes: amb 200.000 files això vol dir el mapa obsolet gairebé tota la setmana activa, i la mateixa consulta passa de 202.847 a **601.921 buffers (×3)**. Abaixat a 0,02, amb l'`insert_scale_factor` inclòs, que és el que importa en taules que creixen per inserció.

**Abans de desplegar cada reescriptura, comparació fila a fila contra la versió vigent sobre les dades reals**: 5.460 casos al veïnat del rànquing (tots els àmbits × tots els jugadors × tres radis), 1.155 a la consulta de posició i 273 a la de pàgina. **Zero diferències.** Una consulta el resultat de la qual el jugador veu com la seva posició no es pot validar a ull.

> Un avís de mètode que va costar una tarda: un micro-benchmark que mesura les dues versions **en blocs seguits** no serveix per comparar consultes — l'ordre i l'estat de la memòria cau decideixen el resultat, i la primera mesura va donar exactament el contrari del que era real. El que no enganya és `EXPLAIN (ANALYZE, BUFFERS)` amb mesures alternades i escalfament previ.

### Pagaments in-app

Google Play Billing 8.3.0 amb **verificació al servidor**. És el subsistema amb més superfície d'error del projecte, perquè els errors costen diners de debò en les dues direccions: lliurar sense cobrar, o cobrar sense lliurar.

**El flux.** El client obre la passarel·la de pagament → Google retorna un rebut → una **Edge Function** el valida contra l'API d'`androidpublisher` amb un service account → una RPC atòmica registra la compra i retorna què cal concedir → el client lliura → el servidor confirma la recepció a Google.

Les decisions que el sostenen:

- **L'import el posa el catàleg del servidor, no el client.** El client envia l'SKU; si el servidor respon una altra quantitat, s'ingressa la del servidor. L'única cosa que tria el client és quin SKU va a la passarel·la.
- **El token de compra és únic GLOBALMENT, no per jugador.** Amb un índex únic per `(jugador, token)` —que és el que surt de pensar "cada jugador té les seves compres"— un rebut comprat una vegada valdria per a tots els comptes als quals passessis el token.
- **Tres cinturons contra el doble lliurament**, i calen tots tres: la drecera dels tokens ja liquidats, el registre local de lliurats i el camp `delivered` del servidor. Google **torna a lliurar** a cada connexió tot el que no s'ha consumit, així que és normal que el mateix token torni; n'hi ha prou que l'app es tanqui entre el lliurament i el consum per ingressar dues vegades. Es reprodueix a voluntat amb el mode avió.
- **La confirmació de recepció la fa el servidor.** Google reemborsa automàticament tota compra no confirmada en 3 dies: deixar-ho al client vol dir que qui no torna a obrir el joc desfà la seva pròpia compra amb el producte ja lliurat.
- **Els reemborsaments s'apliquen sols.** Una Edge Function nocturna consulta la llista de compres anul·lades de Google i revoca el contingut permanent. La finestra consultada es **desa**, perquè l'API només retorna 30 dies: sense això, un mes sense executar-la deixa el forat fora d'abast per sempre.

**Com es prova una cosa que mou diners.** Amb un doble del client de facturació i un altre del backend, un arnès recorre els **19 motius d'error del servidor** —els de Google, els de l'SQL i els del transport— més cinc respostes mal formades, i comprova en cadascun que **no es concedeix res i no es consumeix el token**; consumir-lo llençaria una compra pagada. I un altre arnès respon la pregunta que es fa el jugador —*m'emporto alguna cosa si poso el mode avió?*— mesurant el saldo i l'inventari abans i després de cada camí, en lloc de llegir el codi.

> L'error més car d'aquest subsistema no va donar cap error: el permís remot de venda arribava al client i **es descartava a l'última línia**, perquè el parseig construïa el seu diccionari a mà amb tres claus i la quarta es perdia pel camí. La botiga deia "Pròximament" passés el que passés a la base de dades. La regla que en va sortir —una clau nova a la resposta s'ha d'afegir també al parseig del client— ara la vigila una prova que extreu les claus del mateix SQL.

### Publicitat

AdMob darrere de l'autoload-façana, amb tres peces que no són evidents fins que ho proves en un mòbil real:

- **Memòria cau per unitat amb caducitat.** L'anunci recompensat es demanava dins del mateix `await`, així que cada toc esperava fins a 10 segons amb el botó mut. Avui se serveix d'una memòria cau que es reposa sola, amb una caducitat de 50 minuts: AdMob dona per bo un anunci precarregat durant aproximadament una hora, i passat el termini el jugador es quedaria **sense recompensa després d'haver premut**, que és pitjor que esperar.
- **Un vel amb un retard de 350 ms.** Amb l'anunci precarregat no hi ha espera, i un parpelleig de mig frame es llegeix com un error, no com un "carregant".
- **Límits de seguretat sobre cada estat muntat al voltant d'un `await`.** Una corrutina pot morir a mitja espera —el plugin peta, l'arbre desapareix— i llavors la línia que allibera l'estat no s'executa mai. Aquest patró va mossegar tres vegades al mateix fitxer, i totes tres amb un preu diferent: una pantalla bloquejada per sempre, una unitat que no es torna a precarregar mai més, i un botó mort. Totes tres es tanquen igual: l'estat **caduca** en lloc de refiar-se del seu propi alliberament.

### Identitat i desament al núvol

Per jugar no cal compte: sessió anònima per dispositiu. Vincular Google és opcional i **converteix el compte anònim en permanent conservant el mateix `auth.uid()`**, així que puntuacions, perfil i desament sobreviuen sense migrar res.

Els tres casos difícils:

1. **Vincular un compte de Google que ja té identitat pròpia** (reinstal·lar, canviar de mòbil) és el cas *freqüent*, no l'excepcional. Es detecta, es recorre a un inici de sessió normal i s'obre un diàleg que compara els dos progressos perquè el jugador triï; el compte anònim orfe s'esborra perquè no surti duplicat al rànquing.
2. **Un enllaç que triomfa al servidor però la resposta del qual es perd** (temps d'espera esgotat en xarxa mòbil) retorna "aquesta identitat ja existeix" **sobre un mateix** en tornar-ho a provar. Sense una comprovació explícita, el flux de conflicte acabava esborrant el compte propi.
3. **Transferir el progrés a un altre dispositiu** és *moure*, no copiar: el bescanvi planta una làpida que el dispositiu d'origen consumeix en la seva arrencada següent i neteja el que té en local. Sense això, l'origen torna a pujar la seva còpia intacta i duplica compres en bucle.

El desament local fa servir **escriptura atòmica pròpia**: fitxer temporal, relectura i validació, rotació de l'actual a `.bak`, canvi de nom. El mode `WRITE` de Godot trunca en obrir, així que un procés mort a mitja escriptura deixava el fitxer buit i el jugador perdia monedes, estrelles i inventari de cop — un risc gens teòric, perquè diversos serveis bolquen al disc just a `APPLICATION_PAUSED`. La restauració des del núvol és, a més, transaccional, amb un sentinella que permet reprendre-la si mor a mig camí.

### Interruptor remot de versió

Google Play no força res pel seu compte: una build vella s'obre igual per sempre. Dos llindars en una taula del servidor —avís i bloqueig— permeten retirar de circulació una build trencada sense publicar res, i fan de *kill switch*.

Tres propietats decidides expressament:

- **Falla en obert.** Sense xarxa, amb la RPC caiguda o amb una resposta il·legible, es juga. Bloquejar qui no ha pogut verificar deixa penjat qualsevol que vagi en metro.
- **"No s'aplica" i "no ho he pogut comprovar" són estats diferents.** Fusionar-los deixava el client convençut d'estar al dia durant tot el procés; separats, el segon ho torna a provar amb esperes creixents.
- **L'avís surt un cop per versió**, no un per arrencada —es converteix en la pantalla que es tanca sense llegir— ni un per instal·lació, que silenciaria totes les actualitzacions futures.

La comparació de versions és numèrica per trams i tolerant a formats estranys: un `1.10 < 1.9` lexicogràfic hauria bloquejat tothom que tingués la 1.10.

### Telemetria i equilibri basat en dades

Cada partida acabada envia a Supabase una fila amb ~40 camps: resultat, causa de la derrota, fins on va arribar la cadena, precisió, desglossament de la puntuació, objectes utilitzats, temps net sense pauses i la dificultat real amb què es va jugar. Hi ha agregats per jugador i nivell, purga automàtica als 90 dies, límit de freqüència per classe de fila i un interruptor a Opcions pel GDPR.

**Per a què serveix de debò:** el llindar de les estrelles de cada nivell es calibra amb `percentile_cont` sobre les puntuacions reals, no a ull. I les decisions de disseny es prenen amb la mesura al davant:

- La corba de dificultat es va aplanar en comprovar que del món 5 al 9 l'exigència es movia un ±3 % i el món 10 estava **per sota** del 3.
- Una família de missions es va reescriure sencera en descobrir que el jugador més actiu duia **zero monedes de missions en 78 partides**: tres objectius eren matemàticament inassolibles, i un demanava un combo que no havia sortit ni una sola vegada en 268 partides.
- El llindar de la tercera estrella es va abaixar en mesurar que **cap de 51 victòries** no hi arribava; la millor es va quedar a un 1,3 %.
- La dificultat del mode Infernal es va repartir **a parts iguals entre quantitat d'orbes i velocitat**, i no és simetria decorativa: les dues meitats estiren en sentits oposats sobre el rellotge —més orbes allarguen la partida, més velocitat l'escurça—, així que carregar-ho tot en una canvia la durada un 9 % sense que ningú ho hagi demanat. Repartit a l'arrel del factor, l'exigència puja i la partida dura el mateix.

> **Un biaix que invalida la mesura abans de començar: contra quin jugador mesures.** Calibrar el mode Infernal amb la telemetria general no servia de res — 69 de les 82 victòries amb context eren de jugadors nous als tres primers mons, i en aquest mode només s'hi entra després d'haver acabat el joc. Són dues poblacions diferents que disparen a ritmes diferents, així que el percentil agregat descriu algú que no el jugarà mai.

> **I un error de dades que va costar sis dies.** La puntuació d'un combat multifase arribava amb la primera fase comptada dues vegades. No donava error: l'únic símptoma era un residu en una comprovació de consistència, i es va explicar amb una hipòtesi raonable i falsa. Sobre aquelles ràtios inflades es van recalibrar quatre combats **en la direcció contrària**, cosa que els va deixar regalats durant gairebé una setmana. La lliçó va quedar escrita al repositori: un residu sistemàtic es **contrasta amb una altra font** abans d'explicar-lo — n'hi havia prou de comparar-lo amb la taula que el rànquing escriu per un altre camí.

### Anti-trampes: model d'amenaça explícit

El que importa aquí no és la llista de defenses, sinó on és la línia i per què.

**El que imposa el servidor**, i no depèn del client: límits per puntuació enviada, límit de freqüència per jugador, llista blanca de mons i nivells, guards de propietat a cada RPC, i triggers de taula —no un `if` repartit per sis funcions— perquè un jugador sancionat no pugui escriure en cap tauler, ni avui ni en el setè tauler que s'afegeixi d'aquí a un any.

**El que es dona per perdut**: en un dispositiu amb accés als fitxers, el moneder és un JSON local. Qui el pugui editar no necessita fer trampa amb cap compra. Tancar-ho exigiria moure tota l'economia al servidor, que és un cost que aquest projecte no paga.

**El que sí que queda tancat, perquè és el que costa diners**: que una compra real no es pugui convertir en dues. Les defenses es dimensionen amb aquesta jerarquia al davant — blindar les missions i deixar el moneder en local seria seguretat d'aparador.

Tot això està raonat per escrit en un document de disseny intern, inclosa la decisió de **no** portar els comptadors de missions a la base de dades: un servidor no pot validar una missió sense validar el gameplay, així que continua sent el client qui diu "fet".

### Moderació i suport dins l'app

Amb jugadors reals apareixen problemes que no són tècnics, i necessiten eines.

- **Tauler d'administració dins del joc**, amb el rol verificat al servidor (`auth.uid()`, mai un paràmetre): cercador de jugadors, fitxa completa, sancions reversibles i utilitats de desenvolupament. La funció que assigna rols **no s'exposa**: el seu abús és irreversible per definició, així que es queda al tauler de la base de dades. Un administrador no pot sancionar-ne un altre ni sancionar-se a si mateix.
- **Denúncies entre jugadors** amb cinc defenses contra les campanyes coordinades —una fila per parella, límit diari, exigir haver jugat, un sancionat no pot denunciar, purga acotada— i **sense sanció automàtica**: el recompte ordena la llista, però decidir continua sent un botó que prem una persona.
- **Contacte i apel·lació in-app**: el jugador escriu dins del joc i la resposta li arriba a la bústia. Un sancionat **sí que pot escriure**, perquè és la seva única via d'apel·lació i tancar-la deixaria qualsevol error sense marxa enrere.
- **Traducció del suport** amb DeepL a través d'una Edge Function, perquè el joc es publica en deu idiomes. La clau viu al servidor i l'endpoint comprova el rol de qui fa la crida: sense això, és un proxy de traducció de pagament gratuït per a qualsevol que llegeixi la clau de l'APK.

### Internacionalització

**1.155 claus × 10 idiomes** (EN, ES, CA, pt-BR, FR, IT, DE, JA, KO, RU) a partir d'un CSV únic que compila l'importador de Godot; el CSV no es llegeix en runtime. Detecció automàtica de l'idioma del sistema a la primera arrencada i canvi en calent.

El que vaig aprendre fent-ho, i que no surt en cap tutorial:

- **Sense plurals.** L'objectiu no va a la frase, va a la barra de progrés. Amb el rus, que té tres formes de plural, posar `{n}` a cada cadena és la via ràpida cap a traduccions trencades. Quan sí que hi ha xifra, la unitat va a l'etiqueta i el valor va sol: `DÍAS DE RACHA: 3` (dies de ratxa) en lloc de `3 DÍAS`, que el primer dia de qualsevol instal·lació mostrava **"1 DÍAS"** ("1 DIES") en vuit idiomes.
- **La concordança de gènere és el mateix problema amb una altra cara**, i la sortida no és una taula de gèneres: és escriure una frase que no hagi de concordar.
- **El text és una restricció de layout, no un detall final.** Hi ha arnesos que mesuren l'amplada real de cada botó en els deu idiomes contra el seu espai, perquè una etiqueta que se'n passa no es retalla: **eixampla el contenidor**, i en un panell centrat això el fa sortir pels dos costats sense que el layout es queixi.
- **Una auditoria de vocabulari per idioma** va trobar fins a quatre paraules diferents per al mateix concepte dins d'un mateix idioma —el tutorial feia servir un terme que no tornava a aparèixer en tot el joc— i dues cadenes que deien una cosa **falsa**: una prometia als jugadors coreans que no podien escriure el seu nom amb el seu alfabet, quan sí que podien.

### Accessibilitat

Mode daltònic amb dos interruptors independents: paleta alternativa i figures geomètriques sobre l'orbe.

La primera paleta **no funcionava**, i ho va dir un jugador daltònic real: "ho veig pràcticament igual". Mesurada amb la transformació de Viénot-Brettel-Mollon sobre el color que surt del shader, en deuteranopia dos dels quatre colors quedaven a distància 23, i en escala de grisos tots quatre queien dins de 5,6 — es reduïen a dos colors. La paleta actual (Okabe-Ito adaptada) apuja el pitjor cas a 17,2, i el que de debò la separa **és la lluminositat** (L\* 43 / 60 / 79 / 97), que és l'única cosa que conserva qualsevol tipus de daltonisme.

Tot i així, el color sol no n'hi ha prou: un optimitzador sobre els quatre tipus alhora topa al voltant de distància 20. Per això el canal primari són les **figures**, amb el gruix del contorn mesurat a la resolució real a què es pinten — sobre un orbe clar, un farciment blanc té un contrast d'1,06:1 contra el cos, així que la figura només es llegeix per la vora. I les textures del mode clàssic es **generen** amb la mateixa fórmula del shader, perquè un orbe es vegi igual amb skin i sense per construcció.

### Estratègia de proves sense CI

**132 scripts de QA en GDScript**, executables en headless, més un llançador que els executa tots i resumeix què falla. No hi ha framework de testing: són scripts que munten el joc de debò, fan alguna cosa i mesuren.

Els principis que fan que serveixin per a alguna cosa:

- **Verificació per mutació.** Un arnès que no ha estat mai en vermell no prova res. Gairebé tots es validen reintroduint a mà l'error que persegueixen i comprovant que donen vermell. Diverses vegades això va destapar que la prova mesurava una altra cosa: una comprovació buscava un identificador que també apareixia en un comentari, així que passava en verd amb la línia esborrada.
- **Mesurar el resultat, no el codi font.** "M'emporto alguna cosa en mode avió?" es respon mesurant el saldo abans i després, no llegint l'`if`.
- **L'arnès munta l'estat que vol mesurar, mai no l'hereta.** Diverses proves fallaven o passaven segons qui les llancés, perquè llegien el progrés real de la màquina. I tot script que escrigui al disc passa per una xarxa de seguretat que fa una còpia dels fitxers de desament i els restaura, amb identificació per PID, perquè dos arnesos en paral·lel es trepitjaven la còpia.
- **Hi ha coses que només es veuen mirant.** Un efecte de partícules naixia sencer fora de la pantalla i el seu propi comentari afirmava el contrari; l'estat de l'arbre de nodes era perfecte. Per a això, els arnesos de captura rasteritzen i **mesuren el píxel**: l'enfosquiment d'un vel es comprova per la luminància mitjana, no pel valor de la propietat `alpha`.
- **La primera passada completa del llançador va trobar tres arnesos en vermell sobre codi sa**: comprovacions ancorades a la posició d'un literal que havia canviat de lloc. Un arnès que falla sense motiu és pitjor que no tenir-ne cap, perquè ensenya a ignorar els vermells.

A més: un fuzzer que dispara a punts aleatoris durant milers de frames sobre una mostra de nivells, amb una llavor derivada de la ruta perquè un error es pugui reproduir, i un script que carrega tots els GDScript del projecte per caçar errors de compilació que cap prova no tocaria — el fitxer arrel de l'aplicació no el compila cap arnès, i un error de sintaxi allà deixa el joc sense arrencar amb tota la bateria en verd.

### Eines pròpies

- **Plugin d'editor de Godot** (`EditorPlugin` + `@tool` + `_forward_canvas_gui_input`): Maj+clic al viewport per traçar els camins, amb sufixos al nom del marcador que defineixen trams especials (portal, no enganxable, dues capes de profunditat, final de l'esprint d'entrada) i renumeració automàtica en dues passades.
- **Scripts Python** per al que no s'ha de fer a mà: mesurament de la longitud real dels 92 camins —replicant la mètrica exacta del joc— per recalibrar la velocitat per nivell, generació de les textures del mode daltònic, preparació de skins d'orbe amb reassignació del rang tonal, i regeneració de tots els assets de la web a la mida a què es pinten.
- **Simulador en Node** de la demo del canvas de la landing, que llegeix les constants del mateix HTML. Al navegador la mesura enganya: amb la pestanya en segon pla, `requestAnimationFrame` baixa a 1 fps i qualsevol recompte surt a zero.

### Rendiment i desplegament a Android

- Compressió de textures VRAM dual (escriptori i Android) amb auditories automàtiques dels fitxers d'importació: Godot crea el `.import` d'una textura nova amb els valors per defecte i no hereta els de les veïnes — 40 textures van entrar sense comprimir en una sola tanda, sense cap avís.
- Pressupost d'assets vigilat: 45 retrats de perfil van passar de PNG a JPG (4,2 MB → 1,7 MB) perquè són il·lustracions opaques, que és justament el que pitjor comprimeix el PNG.
- Límit de FPS configurable (30/60) i mai "sense límit", per la limitació tèrmica. Els límits de velocitat de la simulació van en píxels per **segon**, no per frame, o l'ajust de FPS canviaria la velocitat de la simulació — inadmissible amb un rànquing al darrere.
- Compliment de Google Play: política de privadesa pròpia amb GDPR/RGPD, esborrament del compte in-app (RPC + cascada + neteja local, inclosa la fila d'`auth.users`, que és on viu el correu), declaració de Data Safety sincronitzada amb el que l'app fa de debò, i classificació IARC.

---

## Què demostra el projecte

Traduït al que es busca en una oferta de feina:

| Competència | On és al projecte |
|---|---|
| **Disseny de bases de dades** | 27 esquemes, 113 RPC, RLS, triggers, índexs parcials, jobs amb `pg_cron` |
| **Optimització de consultes** | Banc de 200.000 files, `EXPLAIN (ANALYZE, BUFFERS)`, `JOIN LATERAL`, autovacuum afinat, verificació fila a fila abans de desplegar |
| **Seguretat** | Pentest de l'API pública, `SECURITY DEFINER` amb `search_path` fix, grants per columnes, model d'amenaça escrit |
| **Integració de pagaments** | Billing amb verificació al servidor, idempotència, doble lliurament tancat amb tres cinturons, reemborsaments automatitzats |
| **Optimització del rendiment** | Perfilatge, coll d'ampolla algorísmic identificat i mesurat (x18), pressupost d'assets |
| **Arquitectura** | Façanes sobre SDK natius, router únic de navegació, separació entre estat desat i estat pintat |
| **Testing** | 132 scripts de QA, verificació per mutació, fuzzing, proves que mesuren píxels |
| **Enginyeria de dades** | Telemetria amb retenció automatitzada i decisions de producte preses amb percentils reals |
| **i18n i a11y** | 10 idiomes amb auditoria de vocabulari; accessibilitat per al daltonisme validada amb literatura científica i amb un usuari real |
| **Compliment normatiu** | GDPR, Play Data Safety, esborrament del compte, moderació, política de privadesa mantinguda |
| **Autonomia** | De la idea a la botiga sense equip: producte, backend, client, art d'UI, web, legal i operació |

I una cosa que no cap a la taula: **la documentació**. El repositori del joc inclou un mapa de decisions on cada elecció no òbvia està escrita amb el seu perquè, la seva mesura i el que va costar l'error anterior. Molts dels avisos que citen aquestes seccions en vénen. És el que fa que un projecte de 98.000 línies escrit per una persona continuï sent modificable un any després.

---

## Contacte

**Aleix** — desenvolupament, backend, disseny, art d'UI i web.

- Correu electrònic: [aleixauque@gmail.com](mailto:aleixauque@gmail.com)
- Web: [aleixaj.com](https://aleixaj.com)
- El joc: [Orbex a Google Play](https://play.google.com/store/apps/details?id=com.aleix.orbex) · [orbex.aleixaj.com](https://orbex.aleixaj.com)

> El codi del joc és privat. Puc ensenyar-lo o comentar qualsevol dels sistemes d'aquí dalt en una entrevista.
