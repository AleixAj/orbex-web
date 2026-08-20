# Privacy Policy — Orbex

**Last updated:** August 20, 2026
**Effective:** August 20, 2026

## 30-second summary

Orbex is a puzzle game built by an independent solo developer (Aleix). To run the online ranking, the events and the cloud backup of your progress, the game stores some basic information on a server.

Two things are worth knowing up front:

- **The game shows ads through Google AdMob.** AdMob uses your device's advertising ID. In the European Economic Area, the UK and Switzerland the game asks for your consent before serving personalised ads.
- **You can link a Google account** so you don't lose your progress if you change phones. If you do, we store the email address of that account. If you don't, the game never asks you for an email.

Beyond that: **we do not access your contacts, photos, calendar, microphone or camera, we do not track your location, and we do not sell your data to anyone.**

You can delete your account and all your data at any time from **Settings → Delete Account** (permanent). If you only want to start over without losing what you own, use Settings → Reset Progress instead. You can also write to playorbex@gmail.com.

---

## 1. Who we are

Orbex is a personal project developed and maintained by Aleix (natural person, Spain), who is the data controller under the GDPR. Contact for anything related to this policy or to your data:

- **Email:** playorbex@gmail.com

## 2. What data we collect

### 2.1 Data sent to the server (Supabase backend)

- **Anonymous identifier (UUID)**: randomly generated on your device the first time you open the game. Not linked to your real identity.
- **Public nickname**: the one you choose in the welcome modal and display in the ranking. It can be anything; it does not need to be your real name.
- **Avatar and profile frame**: your cosmetic selection.
- **Game stats**: games played, levels completed, stars, best combo, bosses defeated, best score, total score, total play time, achievements completed.
- **Scores**: your highest score on each level and each world (global ranking), your best score in the weekly challenge, and your best score per level in Survival mode. Each leaderboard is separate.
- **Friends**: the list of players you have added, and a notification for each player who adds you. Adding someone is one-directional and needs no approval; the other player only sees that you added them.
- **Cloud backup of your progress**: so you don't lose everything if you change or wipe your phone, the game uploads a copy of your progress files. That copy contains your level progress and stars, your currency balances (coins, golden tickets and any seasonal event currency), your power-up inventory, the cosmetic packs you own, your achievements, your daily-reward and free-chest state, your daily and weekly quests, your best weekly-challenge score, and your selected orb skin and profile frame. Your device Settings (volume, language, menu background) are **not** included.
- **Mailbox state**: which in-game announcements you have opened, claimed or deleted, so they behave consistently across devices.
- **Account status**: your account role (regular player, founder, staff) and, if it ever applies, whether the account is under a sanction, why and until when — see section 11.

### 2.2 Linking a Google account (optional)

Playing does not require signing in. The game opens an anonymous session on its own, and that session lives on the device.

From **Settings → Cloud** you can link a Google account. It is entirely optional and its only purpose is recovery: it turns the anonymous account into a permanent one **keeping the same identifier**, so your progress, your scores and your profile carry over untouched.

If you link it:

- Google returns your **email address**, and we store it (in Supabase's authentication system) as the credential for that account. The game shows it in the Cloud panel so you know which account you linked.
- We do **not** receive your Google password, your contacts, your Drive files, or anything else from your Google account.
- Your email is never public: it does not appear in the ranking, in your profile, or to any other player.
- You can leave the link at any time from **Settings → Cloud → Switch account**, which returns the device to a fresh anonymous account. Deleting your account (section 9) also erases the linked email.

Google's privacy policy: https://policies.google.com/privacy

### 2.3 Transfer codes (moving to another phone)

If you have not linked Google, your account stays tied to your device. To move it, the game lets you generate a **transfer code** from Settings → Cloud. About that code:

- It is **single use** and expires after **72 hours**.
- We store only an irreversible hash of it (MD5), never the code itself.
- Redeeming it on the new phone **moves** the account: the origin account is deleted from the server, freeing up its nickname, and the origin device wipes its local progress the next time it opens the game. It is a move, not a copy.

### 2.4 Data stored ONLY on your device

- Music and SFX volume, language, menu background, FPS limit, colourblind options, and the rest of your Settings preferences.
- Session refresh token (so you don't have to sign in every time).

### 2.5 Anonymous gameplay analytics (optional, on by default)

To calibrate difficulty, star thresholds and the in-game economy, the game sends anonymous telemetry:

- **After each attempt**: final score and how it broke down, combo, active playtime (excluding paused time), how far the chain reached, hearts lost, power-ups used, cause of defeat, and whether the invisible difficulty assist was active.
- **In-game economy**: aggregate counters of how many coins you earn and spend, grouped by source (level victory, achievement, quest, purchase of a given power-up…). Totals only, never a transaction log.
- **Playtime**: total time with the app in the foreground, alongside the time spent in actual matches.
- **Technical metadata**: game language, platform (Android), app version, session count and last activity timestamp.

All of it is attached to your anonymous UUID and none of it contains personal data. You can **turn all of it off at any time** from **Settings → Anonymous Stats** — the switch is on by default and covers every item on this list. Turning it off takes effect immediately and does not affect any other functionality.

### 2.6 What we do NOT collect

- Your real name, postal address or phone number.
- Your email — unless you deliberately link a Google account (section 2.2).
- Location (GPS, wifi, IP geolocation).
- Contacts, photos, calendar, microphone, camera.
- Biometric data.
- Browsing history.
- Payment or card details (section 4).

## 3. Advertising

Orbex shows ads through **Google AdMob** (Google Ireland Limited). There are two kinds and they behave differently:

- **Rewarded ads — always optional.** They only play if you press a button that says so: continuing after a defeat, doubling the coins from a victory, tripling the daily reward, or opening the free chest. No content in the game is locked behind watching one.
- **Interstitials — occasional.** A full-screen ad between games, capped by frequency and never shown right after a campaign defeat.

**What AdMob receives.** Google receives your device's **advertising ID (AAID)**, IP address, device and app information, and how you interact with the ad. That is how ads are selected and how fraud is prevented. **Google does not receive your nickname, your progress, your scores or your Orbex identifier** — the game does not send them and the ad SDK has no access to them.

**Consent.** In the European Economic Area, the UK and Switzerland the game presents Google's official consent form (UMP) the first time it runs, and personalised ads are only served if you accept. Whatever you choose, the game works exactly the same.

**Managing it from your phone.** You can reset or delete your advertising ID at any time from Android's **Settings → Privacy → Ads**. Deleting it stops ads from being personalised; you will still see ads, just untargeted ones.

Google's advertising policy: https://policies.google.com/technologies/ads

## 4. Purchases

Orbex does not currently sell anything inside the app. If and when in-app purchases are enabled, **Google Play handles the payment end to end**: we never see or store your card, your billing address or your Google account balance. All we would receive is confirmation that a given product was bought by your account, so the game can unlock it.

## 5. Why we use your data

- **Running the game**: saving and restoring your progress, the ranking, the events, friends and the mailbox.
  *Legal basis: performance of the service you asked for (GDPR art. 6.1.b).*
- **Keeping it working**: fixing bugs, calibrating difficulty, preventing cheating and abuse.
  *Legal basis: legitimate interest (GDPR art. 6.1.f).*
- **Anonymous gameplay analytics** (2.5).
  *Legal basis: your consent — the switch in Settings (GDPR art. 6.1.a).*
- **Personalised advertising** (section 3).
  *Legal basis: your consent — Google's UMP form (GDPR art. 6.1.a).*

**We do NOT use your data for**: marketing emails, profiling you as a person, training AI models, or selling to third parties.

## 6. Who sees your data

- **You**: all of your data is on the in-game Profile screen.
- **Other players**: when they tap your row in the ranking they see your nickname, avatar, profile frame and public stats (stars, best combo, bosses defeated, best score, playtime, achievements). If you add someone as a friend, that player is told you added them. Nothing else is visible to anyone.
- **Aleix (developer)**: I have admin access to the database, both through the Supabase panel and through an admin screen inside the game, solely for maintenance, bug fixing, moderation and answering deletion requests. That screen shows the same profile data plus technical fields (app version, session count, currency counters).
- **Supabase**: the infrastructure provider hosting the database (processor).
- **Google**: AdMob for advertising (section 3) and, only if you link it, Google Sign-In for authentication (section 2.2).
- **Nobody else.** We do not share, rent or sell data to any other party.

## 7. Where your data is stored

- **On your device**: in the app's private storage, isolated from other applications by Android.
- **On the server**: at Supabase (infrastructure provider), on servers located in the European Union. Supabase applies encryption in transit (HTTPS/TLS) and at rest.
- **Advertising data** is processed by Google under its own terms and may be transferred outside the EU under the safeguards described in Google's policy.

Supabase's privacy policy (subprocessor): https://supabase.com/privacy

## 8. How long we keep it

- **Local**: until you uninstall the app, press "Reset Progress", or press "Delete Account".
- **Server**: indefinitely while your account is active, with these exceptions:
  - **Per-attempt telemetry** (`level_attempts`) auto-purges after 90 days by a scheduled job. The aggregated stats (best score, averages, star counts) stay indefinitely.
  - **Friend notifications** are purged by a scheduled job: read ones after 90 days, plus anything beyond the 120 most recent per player. Pending notifications are never deleted by age — they are how you find out who added you.
  - **Transfer codes** expire 72 hours after being generated, and are deleted once redeemed.
  - **Weekly challenge**: each week's leaderboard is closed and its prizes delivered by a scheduled job. Prize messages that expire without being claimed are deleted.
  - **Accounts that never chose a nickname**: if you open the game but never pick a nickname, the only thing that exists on the server is an empty anonymous session. A scheduled job deletes it after **30 days** with no activity. Your local progress on the device is not affected.
  - When you press **Delete Account** (see next section) or write requesting deletion, your entire server-side record is erased immediately — including the authentication account itself and any linked Google email, not just your game data.

## 9. Your rights (GDPR)

If you live in the European Union, you have the right to:

- **Access** your data: visible in real time on the Profile screen. For anything not shown there, ask by email.
- **Correct** your data: change nickname, avatar and frame from that same screen.
- **Delete** your data: **Settings → Delete Account** wipes everything permanently — your server-side profile, all your stats and scores, your friends, your mailbox, your cloud backup, your local progress and any linked Google account. If you only want to start over, **Settings → Reset Progress** clears your progress and your ranking score but keeps the account, the nickname and the cosmetics you own. You can also write to **playorbex@gmail.com** with the UUID shown on your profile screen and I will do it manually.
- **Portability**: request a copy of your data by email; delivered in JSON format.
- **Object** to processing or **withdraw** consent at any time: the analytics switch and Android's advertising settings both take effect immediately, and you can always uninstall the app and request server-side deletion.
- **File a complaint** with your local data protection authority (in Spain: AEPD, www.aepd.es).

We answer any of these within 30 days, and normally much sooner.

## 10. Children

Orbex targets people aged **13 and up**, and its Google Play content rating reflects that. We do not knowingly collect data from children under 13, and the game is neither designed for nor directed at them. If you are the legal guardian of a minor and believe they have used the game, contact playorbex@gmail.com and we will delete the account.

## 11. Fair play and account sanctions

Nicknames are public, so the game rejects impersonation of staff and offensive names at the point where you pick one. If an account breaks those rules or manipulates the leaderboards, we can restrict it: a sanctioned account disappears from the leaderboards and cannot submit scores, change its nickname or avatar, or add friends. **It can still play** — the single-player game is unaffected.

When that happens we record the reason and the date. Sanctions can be temporary or permanent, they are always reversible on our side, and you can appeal any of them by writing to playorbex@gmail.com.

## 12. Security

- All traffic to the server is encrypted via HTTPS/TLS.
- Database access is protected by Row Level Security (RLS): every write goes through a controlled procedure, and each player can only read and write their own rows.
- Administrative operations are restricted to staff accounts and verified on the server, never trusted from the app.
- We periodically audit the code for vulnerabilities.

No system is 100% secure. If you detect a vulnerability, please email playorbex@gmail.com.

## 13. Changes to this policy

If we update this policy, we will publish the new version at this same URL with the updated "Last updated" date at the top. For changes that materially affect how we use your data, we will also announce it in the in-game mailbox. Changes take effect on publication.

## 14. Contact

Aleix — playorbex@gmail.com

---

# Política de Privacidad — Orbex

**Última actualización:** 20 de agosto de 2026
**Vigente desde:** 20 de agosto de 2026

## Resumen en 30 segundos

Orbex es un juego de puzles desarrollado por una persona independiente (Aleix). Para que funcionen el ranking online, los eventos y la copia de tu progreso en la nube, el juego guarda información básica en un servidor.

Hay dos cosas que conviene saber desde el principio:

- **El juego muestra anuncios a través de Google AdMob.** AdMob usa el identificador publicitario de tu dispositivo. En el Espacio Económico Europeo, Reino Unido y Suiza el juego te pide consentimiento antes de mostrarte anuncios personalizados.
- **Puedes vincular una cuenta de Google** para no perder tu progreso si cambias de móvil. Si lo haces, guardamos el correo de esa cuenta. Si no lo haces, el juego no te pide ningún correo.

Más allá de eso: **no accedemos a tus contactos, fotos, calendario, micrófono ni cámara, no rastreamos tu ubicación y no vendemos tus datos a nadie.**

Puedes borrar tu cuenta y todos tus datos en cualquier momento desde **Opciones → Borrar cuenta** (definitivo). Si solo quieres empezar de cero sin perder lo que tienes, usa Opciones → Restablecer progreso. También puedes escribir a playorbex@gmail.com.

---

## 1. Quién soy

Orbex es un proyecto personal desarrollado y mantenido por Aleix (persona física, España), que es el responsable del tratamiento a efectos del RGPD. Contacto para cualquier tema relacionado con esta política o con tus datos:

- **Email:** playorbex@gmail.com

## 2. Qué datos recogemos

### 2.1 Datos que envías al servidor (backend en Supabase)

- **Identificador anónimo (UUID)**: se genera aleatoriamente en tu dispositivo la primera vez que abres el juego. No está vinculado a tu identidad real.
- **Nombre público (nickname)**: el que eliges en el modal de bienvenida y muestras en el ranking. Puede ser cualquier cosa; no tiene que ser tu nombre real.
- **Avatar y marco cosmético**: la selección que hayas hecho para tu perfil.
- **Estadísticas de juego**: partidas jugadas, niveles completados, estrellas, mejor combo, jefes derrotados, mejor puntuación, puntuación total, tiempo total de juego, logros completados.
- **Puntuaciones**: tu mejor marca en cada nivel y en cada mundo (ranking global), tu mejor puntuación del desafío semanal y tu mejor marca por nivel en el modo Supervivencia. Cada tabla es independiente.
- **Amigos**: la lista de jugadores que has añadido y una notificación por cada jugador que te añade a ti. Añadir es unilateral y no requiere aprobación; la otra persona solo ve que la has añadido.
- **Copia de seguridad de tu progreso**: para que no lo pierdas todo si cambias o formateas el móvil, el juego sube una copia de tus ficheros de progreso. Esa copia contiene tu avance por niveles y estrellas, tus saldos de divisas (monedas, tickets dorados y la divisa del evento de temporada si la hay), tu inventario de power-ups, los packs cosméticos que tengas, tus logros, el estado de la recompensa diaria y del cofre gratis, tus misiones diarias y semanales, tu mejor marca del desafío semanal, y la skin de orbe y el marco de perfil que tengas elegidos. Las preferencias de Opciones de tu dispositivo (volumen, idioma, fondo del menú) **no** viajan.
- **Estado del buzón**: qué avisos del juego has abierto, reclamado o borrado, para que se comporten igual en todos tus dispositivos.
- **Estado de la cuenta**: el rol de tu cuenta (jugador normal, founder, staff) y, si alguna vez procede, si está sancionada, por qué y hasta cuándo — ver el apartado 11.

### 2.2 Vincular una cuenta de Google (opcional)

Jugar no exige iniciar sesión. El juego abre por su cuenta una sesión anónima, y esa sesión vive en el dispositivo.

Desde **Opciones → Nube** puedes vincular una cuenta de Google. Es totalmente opcional y su única finalidad es la recuperación: convierte la cuenta anónima en permanente **conservando el mismo identificador**, así que tu progreso, tus puntuaciones y tu perfil pasan intactos.

Si la vinculas:

- Google nos devuelve tu **dirección de correo**, y la guardamos (en el sistema de autenticación de Supabase) como credencial de esa cuenta. El juego te la muestra en el panel de Nube para que sepas con qué cuenta la has vinculado.
- **No** recibimos tu contraseña de Google, ni tus contactos, ni tus archivos de Drive, ni nada más de tu cuenta de Google.
- Tu correo no es público en ningún momento: no aparece en el ranking, ni en tu perfil, ni para ningún otro jugador.
- Puedes deshacer la vinculación cuando quieras desde **Opciones → Nube → Cambiar cuenta**, que deja el dispositivo con una cuenta anónima nueva. Borrar la cuenta (apartado 9) también elimina el correo vinculado.

Política de privacidad de Google: https://policies.google.com/privacy

### 2.3 Códigos de transferencia (cambiar de móvil)

Si no has vinculado Google, tu cuenta va ligada a tu dispositivo. Para moverla, el juego te deja generar un **código de transferencia** desde Opciones → Nube. Sobre ese código:

- Es de **un solo uso** y caduca a las **72 horas**.
- En la base de datos solo guardamos un hash irreversible (MD5), nunca el código en claro.
- Canjearlo en el móvil nuevo **mueve** la cuenta: la cuenta de origen se borra del servidor, liberando su apodo, y el dispositivo de origen limpia su progreso local la próxima vez que abras el juego. Es un traslado, no una copia.

### 2.4 Datos que se guardan SOLO en tu dispositivo

- Volumen de música y efectos, idioma, fondo del menú, límite de FPS, opciones de daltonismo y el resto de preferencias de Opciones.
- Token de refresco de sesión (para no tener que iniciar sesión cada vez).

### 2.5 Analíticas de juego anónimas (opcional, activadas por defecto)

Para calibrar la dificultad, los umbrales de estrellas y la economía del juego, se envía telemetría anónima:

- **Después de cada partida**: puntuación final y su desglose, combo, tiempo activo de juego (sin contar la pausa), hasta dónde llegó la cadena, corazones perdidos, power-ups usados, causa de la derrota y si la asistencia invisible de dificultad estaba activa.
- **Economía del juego**: contadores agregados de cuántas monedas ganas y gastas, agrupados por origen (victoria de nivel, logro, misión, compra de un power-up concreto…). Solo totales, nunca un registro de operaciones.
- **Tiempo de uso**: tiempo total con la app en primer plano, además del tiempo dentro de las partidas.
- **Metadatos técnicos**: idioma del juego, plataforma (Android), versión de la app, número de sesiones y fecha de última actividad.

Todo se asocia a tu UUID anónimo y nada de ello contiene datos personales. Puedes **desactivarlo entero en cualquier momento** desde **Opciones → Estadísticas anónimas** — el interruptor está encendido por defecto y cubre todos los puntos de esta lista. Al apagarlo el efecto es inmediato y no afecta al resto de funcionalidades.

### 2.6 Lo que NO recogemos

- Tu nombre real, dirección postal o teléfono.
- Tu correo — salvo que vincules deliberadamente una cuenta de Google (apartado 2.2).
- Ubicación (GPS, wifi, IP geolocalizada).
- Contactos, fotos, calendario, micrófono, cámara.
- Datos biométricos.
- Historial de navegación.
- Datos de pago o de tarjeta (apartado 4).

## 3. Publicidad

Orbex muestra anuncios a través de **Google AdMob** (Google Ireland Limited). Hay dos tipos y se comportan de forma distinta:

- **Anuncios recompensados — siempre opcionales.** Solo se reproducen si pulsas un botón que lo anuncia: continuar tras una derrota, doblar las monedas de una victoria, triplicar la recompensa diaria o abrir el cofre gratuito. Ningún contenido del juego está bloqueado detrás de ver uno.
- **Intersticiales — ocasionales.** Un anuncio a pantalla completa entre partidas, limitado por frecuencia y nunca justo después de una derrota de campaña.

**Qué recibe AdMob.** Google recibe el **identificador publicitario (AAID)** de tu dispositivo, tu dirección IP, información del dispositivo y de la app, y cómo interactúas con el anuncio. Es así como se eligen los anuncios y como se previene el fraude. **Google no recibe tu apodo, tu progreso, tus puntuaciones ni tu identificador de Orbex** — el juego no se los envía y el SDK de anuncios no tiene acceso a ellos.

**Consentimiento.** En el Espacio Económico Europeo, Reino Unido y Suiza el juego presenta el formulario oficial de consentimiento de Google (UMP) la primera vez que se abre, y solo se sirven anuncios personalizados si aceptas. Elijas lo que elijas, el juego funciona exactamente igual.

**Cómo gestionarlo desde tu móvil.** Puedes restablecer o eliminar tu identificador publicitario cuando quieras desde **Ajustes → Privacidad → Anuncios** de Android. Al eliminarlo, los anuncios dejan de ser personalizados; seguirás viendo anuncios, pero sin segmentar.

Política de publicidad de Google: https://policies.google.com/technologies/ads

## 4. Compras

Ahora mismo Orbex no vende nada dentro de la app. Si en algún momento se activan las compras integradas, **Google Play gestiona el pago de principio a fin**: nunca vemos ni guardamos tu tarjeta, tu dirección de facturación ni el saldo de tu cuenta de Google. Lo único que recibiríamos es la confirmación de que tu cuenta ha comprado un producto concreto, para que el juego pueda desbloquearlo.

## 5. Para qué usamos tus datos

- **Hacer funcionar el juego**: guardar y restaurar tu progreso, el ranking, los eventos, los amigos y el buzón.
  *Base legal: ejecución del servicio que has pedido (RGPD art. 6.1.b).*
- **Mantenerlo en marcha**: corregir errores, calibrar la dificultad y prevenir trampas y abusos.
  *Base legal: interés legítimo (RGPD art. 6.1.f).*
- **Analíticas de juego anónimas** (2.5).
  *Base legal: tu consentimiento — el interruptor de Opciones (RGPD art. 6.1.a).*
- **Publicidad personalizada** (apartado 3).
  *Base legal: tu consentimiento — el formulario UMP de Google (RGPD art. 6.1.a).*

**NO usamos tus datos para**: correos comerciales, perfilarte como persona, entrenar modelos de IA o venderlos a terceros.

## 6. Quién ve tus datos

- **Tú**: todos tus datos están en la pantalla de Perfil dentro del juego.
- **Otros jugadores**: al tocar tu fila en el ranking ven tu nickname, avatar, marco cosmético y estadísticas públicas (estrellas, mejor combo, jefes derrotados, mejor puntuación, tiempo jugado, logros). Si añades a alguien como amigo, esa persona ve que la has añadido. Nadie ve ningún otro dato.
- **Aleix (desarrollador)**: tengo acceso administrativo a la base de datos, tanto por el panel de Supabase como por una pantalla de administración dentro del juego, exclusivamente para mantenimiento, corrección de errores, moderación y respuesta a solicitudes de borrado. Esa pantalla muestra los mismos datos del perfil más campos técnicos (versión de la app, número de sesiones, contadores de divisas).
- **Supabase**: el proveedor de infraestructura que aloja la base de datos (encargado del tratamiento).
- **Google**: AdMob para la publicidad (apartado 3) y, solo si la vinculas, Google Sign-In para la autenticación (apartado 2.2).
- **Nadie más.** No compartimos, cedemos ni vendemos datos a ninguna otra parte.

## 7. Dónde se guardan tus datos

- **En tu dispositivo**: en el almacenamiento privado de la app, aislado del resto de aplicaciones por el sistema Android.
- **En el servidor**: en Supabase (proveedor de infraestructura), en servidores localizados en la Unión Europea. Supabase aplica cifrado en tránsito (HTTPS/TLS) y en reposo.
- **Los datos de publicidad** los trata Google bajo sus propios términos y pueden transferirse fuera de la UE con las garantías descritas en su política.

Política de privacidad de Supabase (subencargado): https://supabase.com/privacy

## 8. Cuánto tiempo se conservan

- **Local**: hasta que desinstalas la app, pulsas "Restablecer progreso" o pulsas "Borrar cuenta".
- **Servidor**: indefinidamente mientras tu cuenta esté activa, con estas excepciones:
  - **Telemetría por partida** (`level_attempts`) se auto-purga a los 90 días mediante una tarea programada. Los agregados (mejor puntuación, medias, estrellas) se conservan indefinidamente.
  - **Notificaciones de amistad**: una tarea programada borra las leídas de más de 90 días y todo lo que quede fuera de las 120 más recientes por jugador. Las pendientes no se borran por antigüedad — son la forma que tienes de enterarte de quién te ha añadido.
  - **Los códigos de transferencia** caducan a las 72 horas de generarse, y se borran en cuanto se canjean.
  - **Desafío semanal**: cada semana una tarea programada cierra la tabla y reparte los premios. Los mensajes de premio que caducan sin reclamarse se eliminan.
  - **Cuentas que nunca eligieron apodo**: si abres el juego pero no llegas a poner apodo, lo único que existe en el servidor es una sesión anónima vacía. Una tarea programada la borra tras **30 días** sin actividad. Tu progreso local en el dispositivo no se toca.
  - Cuando pulsas **Borrar cuenta** (ver siguiente apartado) o escribes solicitando el borrado, todo tu registro en el servidor se elimina inmediatamente — incluida la propia cuenta de autenticación y el correo de Google vinculado, no solo tus datos de juego.

## 9. Tus derechos (RGPD / LOPDGDD)

Al vivir en la Unión Europea, tienes derecho a:

- **Acceder** a tus datos: los ves en tiempo real en la pantalla de Perfil. Para lo que no aparezca ahí, pídelo por email.
- **Corregir** tus datos: puedes cambiar nickname, avatar y marco desde esa misma pantalla.
- **Borrar** tus datos: **Opciones → Borrar cuenta** borra todo de forma permanente — tu perfil en el servidor, todas tus estadísticas y puntuaciones, tus amigos, tu buzón, tu copia en la nube, tu progreso local y la cuenta de Google vinculada. Si solo quieres empezar de cero, **Opciones → Restablecer progreso** limpia tu progreso y tu puntuación del ranking pero mantiene la cuenta, el apodo y los cosméticos que tengas. También puedes escribir a **playorbex@gmail.com** con el UUID de tu pantalla de perfil y lo hago manualmente.
- **Portabilidad**: puedes pedir una copia de tus datos por email; te la envío en formato JSON.
- **Oponerte** al tratamiento o **retirar** el consentimiento en cualquier momento: el interruptor de analíticas y los ajustes de publicidad de Android surten efecto inmediato, y siempre puedes desinstalar la app y solicitar el borrado del servidor.
- **Reclamar** ante la Agencia Española de Protección de Datos (AEPD, www.aepd.es) si consideras que no se están cumpliendo tus derechos.

Respondo a cualquiera de estas solicitudes en un plazo máximo de 30 días, y normalmente mucho antes.

## 10. Menores

Orbex está dirigido a personas de **13 años o más**, y su clasificación de contenido en Google Play lo refleja. No recogemos deliberadamente datos de menores de 13 años, y el juego ni está diseñado ni dirigido a ellos. Si eres el tutor legal de un menor y crees que ha usado el juego, escribe a playorbex@gmail.com y eliminaremos la cuenta.

## 11. Juego limpio y sanciones de cuenta

Los apodos son públicos, así que el juego rechaza la suplantación de personal del juego y los nombres ofensivos en el momento de elegirlos. Si una cuenta incumple esas normas o manipula las tablas de clasificación, podemos restringirla: una cuenta sancionada desaparece de las clasificaciones y no puede enviar puntuaciones, cambiar su apodo o avatar, ni añadir amigos. **Puede seguir jugando** — la parte de un jugador no se ve afectada.

Cuando eso ocurre registramos el motivo y la fecha. Las sanciones pueden ser temporales o permanentes, siempre son reversibles por nuestra parte, y puedes recurrir cualquiera de ellas escribiendo a playorbex@gmail.com.

## 12. Seguridad

- Todo el tráfico con el servidor va cifrado por HTTPS/TLS.
- El acceso a la base de datos está protegido por Row Level Security (RLS): toda escritura pasa por un procedimiento controlado y cada jugador solo puede leer y escribir sus propias filas.
- Las operaciones administrativas están restringidas a cuentas de staff y se verifican en el servidor, nunca se dan por buenas desde la app.
- Auditamos periódicamente el código para detectar vulnerabilidades.

Ningún sistema es 100 % seguro. Si detectas una vulnerabilidad, escribe a playorbex@gmail.com.

## 13. Cambios en esta política

Si actualizamos esta política, publicaremos la nueva versión en esta misma URL con la fecha de "Última actualización" al principio del documento. Para cambios que afecten de forma sustancial a cómo usamos tus datos, lo anunciaremos además en el buzón dentro del juego. Los cambios entran en vigor al publicarse.

## 14. Contacto

Aleix — playorbex@gmail.com
