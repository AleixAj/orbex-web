# Privacy Policy — Orbex

**Last updated:** July 13, 2026
**Effective:** July 13, 2026

## 30-second summary

Orbex is a puzzle game built by an independent solo developer (Aleix). To power the online ranking and save your progress in the cloud, the game stores some basic information on a server. **We do not ask for your email, we do not access your contacts or photos, we do not track your location, we do not show ads, and we do not share your data with third parties beyond our backend provider.**

You can delete your account and all your data at any time from **Settings → Delete Account** (permanent — this also erases any purchases). If you only want to start over without losing your purchases, use Settings → Reset Progress instead. You can also write to aleixauque@gmail.com.

---

## 1. Who we are

Orbex is a personal project developed and maintained by Aleix (natural person, Spain). Contact for anything related to this policy or your data:

- **Email:** aleixauque@gmail.com

## 2. What data we collect

### 2.1 Data sent to the server (Supabase backend)

- **Anonymous identifier (UUID)**: randomly generated on your device the first time you open the game. Not linked to your real identity.
- **Public nickname**: the one you choose in the welcome modal and display in the ranking. It can be anything; it does not need to be your real name.
- **Avatar and profile frame**: your cosmetic selection.
- **Game stats**: games played, levels completed, stars, best combo, bosses defeated, best score, total score, total play time, achievements completed.
- **Scores per level and per world**: your highest score on each level and world.
- **Technical metadata**: game language, platform (Android), app version, session count, last activity timestamp. Used only for diagnosing issues and prioritizing development.

### 2.2 Data stored ONLY on your device

- Music and SFX volume, language, menu background, other Settings preferences.
- Daily chests opened, free reward cooldown.
- Local power-up inventory and coins.
- Anonymous session refresh token (so you don't have to sign in every time).

#### 2.3 Anonymous gameplay analytics (optional)

To calibrate difficulty and star thresholds during beta, the game sends a small telemetry payload after each attempt: final score, combo, active playtime (excluding paused time), how far the chain reached, hearts lost, powerups used, and cause of defeat. All are attached to your anonymous UUID; no personal data is included. You can **turn this off at any time** from **Settings → Anonymous Stats** — the switch is on by default. Turning it off takes immediate effect and does not affect any other functionality.

### 2.4 What we do NOT collect

- Email.
- Real name, postal address, phone number.
- Location (GPS, wifi, IP geolocation).
- Contacts, photos, calendar, microphone, camera.
- Android Advertising ID (AAID/GAID).
- Third-party tracking cookies or pixels.
- Biometric data.
- Browsing history.

## 3. Why we collect it

We use your data exclusively for:

1. **Game functionality**: saving your progress, showing your position in the global ranking, showing your public profile when other players tap your row.
2. **Technical diagnostics**: identifying bugs, understanding which languages and versions are in use.

**We do NOT use your data for**: advertising, marketing, profiling, AI model training, or sale to third parties.

## 4. Who sees your data

- **You**: see all your data on the in-game Profile screen.
- **Other players**: when they tap your row in the ranking, they see your nickname, avatar, profile frame, and public stats (stars, best combo, bosses defeated, best score, playtime, achievements). Nothing else.
- **Aleix (developer)**: I have admin access to the database via the Supabase panel, solely for maintenance, bug fixing, and responding to deletion requests.
- **Nobody else**.

## 5. Where your data is stored

- **On your device**: in the app's private storage, isolated from other applications by Android.
- **On the server**: at Supabase (infrastructure provider), on servers located in the European Union. Supabase applies encryption in transit (HTTPS/TLS) and at rest.
- Supabase's privacy policy (subprocessor): https://supabase.com/privacy

## 6. How long we keep it

- **Local**: until you uninstall the app, press "Reset Progress", or press "Delete Account".
- **Server**: indefinitely while your account is active, with two exceptions:
  - **Per-attempt telemetry** (`level_attempts`) auto-purges after 90 days by a scheduled job. The aggregated stats (best score, averages, star counts) stay indefinitely.
  - When you press **Delete Account** (see next section) or write requesting deletion, your entire server-side record is erased immediately.

## 7. Your rights (GDPR)

If you live in the European Union, you have the right to:

- **Access** your data: visible in real time on the Profile screen.
- **Correct** your data: change nickname and avatar from the same screen.
- **Delete** your data: **Settings → Delete Account** wipes everything permanently — your server-side profile, all your stats and scores, your local progress, and any purchases. If you only want to start over without losing your purchases, **Settings → Reset Progress** clears the local progress and your ranking score but keeps the account, nickname and purchases. You can also write to **aleixauque@gmail.com** with the UUID shown on your profile screen and I will do it manually.
- **Portability**: request a copy of your data by email; delivered in JSON format.
- **Object** to processing or **withdraw** consent at any time (uninstall the app + request server deletion).
- **File a complaint** with your local data protection authority (in Spain: AEPD, www.aepd.es).

## 8. Children

Orbex targets people aged **13 and up**. We do not knowingly collect data from children under 13. If you are the legal guardian of a minor and believe they have used the game, contact aleixauque@gmail.com to delete the account.

## 9. Security

- All traffic to the server is encrypted via HTTPS/TLS.
- Database access is protected by Row Level Security (RLS): each player can only read and write their own rows.
- We periodically audit the code for vulnerabilities.

No system is 100% secure. If you detect a vulnerability, please email aleixauque@gmail.com.

## 10. Changes to this policy

If we update this policy, we will publish the new version at this same URL with the updated "Last updated" date at the top. Changes take effect immediately.

## 11. Contact

Aleix — aleixauque@gmail.com

---

# Política de Privacidad — Orbex

**Última actualización:** 13 de julio de 2026
**Vigente desde:** 13 de julio de 2026

## Resumen en 30 segundos

Orbex es un juego de puzles desarrollado por una persona independiente (Aleix). Para que el ranking online funcione y tu progreso se guarde en la nube, el juego almacena información básica en un servidor. **No pedimos tu correo, no accedemos a tus contactos ni fotos, no rastreamos tu ubicación, no mostramos anuncios y no compartimos tus datos con terceros ajenos al servidor de backend.**

Puedes borrar tu cuenta y todos tus datos en cualquier momento desde **Opciones → Borrar cuenta** (definitivo — también elimina las compras). Si solo quieres empezar de cero sin perder las compras, usa Opciones → Restablecer progreso. También puedes escribir a aleixauque@gmail.com.

---

## 1. Quién soy

Orbex es un proyecto personal desarrollado y mantenido por Aleix (persona física, España). Contacto para cualquier tema relacionado con esta política o con tus datos:

- **Email:** aleixauque@gmail.com

## 2. Qué datos recogemos

### 2.1 Datos que envías al servidor (backend en Supabase)

- **Identificador anónimo (UUID)**: se genera aleatoriamente en tu dispositivo la primera vez que abres el juego. No está vinculado a tu identidad real.
- **Nombre público (nickname)**: el que eliges tú en el modal de bienvenida y muestras en el ranking. Puede ser cualquier cosa; no tiene que ser tu nombre real.
- **Avatar y marco cosmético**: la selección que hayas hecho para tu perfil.
- **Estadísticas de juego**: partidas jugadas, niveles completados, estrellas, mejor combo, jefes derrotados, mejor puntuación, puntuación total, tiempo total de juego, logros completados.
- **Puntuaciones por nivel y por mundo**: la puntuación más alta que has conseguido en cada nivel y en cada mundo.
- **Metadatos técnicos**: idioma del juego, plataforma (Android), versión de la app, número de sesiones y timestamp de última actividad. Se usan solo para diagnosticar problemas y decidir prioridades de desarrollo.

### 2.2 Datos que se guardan SOLO en tu dispositivo

- Volumen de música y efectos, idioma, fondo del menú, otras preferencias de Opciones.
- Cofres diarios abiertos, cooldown de recompensa gratis.
- Inventario de power-ups y monedas locales.
- Token de refresco de sesión anónima (para no tener que iniciar sesión cada vez).

### 2.3 Analíticas de juego anónimas (opcional)

Para calibrar la dificultad y los umbrales de estrellas durante la beta, el juego envía después de cada partida un pequeño paquete de telemetría: puntuación final, combo, tiempo activo de juego (sin contar la pausa), hasta dónde llegó la cadena, corazones perdidos, power-ups usados y causa de la derrota. Todo se asocia a tu UUID anónimo; no se incluye ningún dato personal. Puedes **desactivarlo en cualquier momento** desde **Opciones → Estadísticas anónimas** — el interruptor está encendido por defecto. Al apagarlo el efecto es inmediato y no afecta al resto de funcionalidades.

### 2.4 Lo que NO recogemos

- Correo electrónico.
- Nombre real, dirección postal, teléfono.
- Ubicación (GPS, wifi, IP geolocalizada).
- Contactos, fotos, calendario, micrófono, cámara.
- ID publicitario de Android (AAID/GAID).
- Cookies o pixels de tracking de terceros.
- Datos biométricos.
- Historial de navegación.

## 3. Para qué usamos tus datos

Los usamos exclusivamente para:

1. **Funcionalidad del juego**: guardar tu progreso, mostrar tu posición en el ranking mundial, mostrar tu perfil público cuando otros jugadores toquen tu fila.
2. **Diagnóstico técnico**: identificar bugs, entender qué idiomas y versiones se usan.

**NO usamos tus datos para**: publicidad, marketing, perfilado, entrenamiento de modelos de IA, venta a terceros.

## 4. Quién ve tus datos

- **Tú**: ves todos tus datos en la pantalla de Perfil dentro del juego.
- **Otros jugadores**: al tocar tu fila en el ranking, ven tu nickname, avatar, marco cosmético y estadísticas públicas (estrellas, mejor combo, jefes derrotados, mejor puntuación, tiempo jugado, logros). No ven ningún otro dato.
- **Aleix (desarrollador)**: tengo acceso administrativo a la base de datos vía el panel de Supabase, exclusivamente para mantenimiento, corrección de errores y respuesta a solicitudes de borrado.
- **Nadie más**.

## 5. Dónde se guardan tus datos

- **En tu dispositivo**: en el almacenamiento privado de la app, aislado del resto de aplicaciones por el sistema Android.
- **En el servidor**: en Supabase (proveedor de infraestructura), en servidores localizados en la Unión Europea. Supabase aplica encriptación en tránsito (HTTPS/TLS) y en reposo.
- Política de privacidad de Supabase (subprocessor): https://supabase.com/privacy

## 6. Cuánto tiempo se conservan

- **Local**: hasta que desinstalas la app, pulsas "Restablecer progreso", o pulsas "Borrar cuenta".
- **Servidor**: indefinidamente mientras tu cuenta esté activa, con dos excepciones:
  - **Telemetría por partida** (`level_attempts`) se auto-purga a los 90 días mediante una tarea programada. Los agregados (mejor puntuación, medias, estrellas) se conservan indefinidamente.
  - Cuando pulsas **Borrar cuenta** (ver siguiente sección) o escribes solicitando borrado, todo tu registro en el servidor se elimina inmediatamente.

## 7. Tus derechos (RGPD / LOPDGDD)

Al vivir en la Unión Europea, tienes derecho a:

- **Acceder** a tus datos: los ves en tiempo real en la pantalla de Perfil.
- **Corregir** tus datos: puedes cambiar nickname y avatar desde el mismo perfil.
- **Borrar** tus datos: **Opciones → Borrar cuenta** borra todo de forma permanente — tu perfil en el servidor, todas tus estadísticas y puntuaciones, tu progreso local y las compras. Si solo quieres empezar de cero sin perder las compras, **Opciones → Restablecer progreso** limpia el progreso local y tu puntuación del ranking pero mantiene la cuenta, el nickname y las compras. También puedes escribir a **aleixauque@gmail.com** con el UUID de tu pantalla de perfil y lo hago manualmente.
- **Portabilidad**: puedes pedir una copia de tus datos por email; te la envío en formato JSON.
- **Oponerte** al tratamiento o **retirar** consentimiento en cualquier momento (borrando la app + solicitando borrado del servidor).
- **Reclamar** ante la Agencia Española de Protección de Datos (AEPD, www.aepd.es) si consideras que no se están cumpliendo tus derechos.

## 8. Menores

Orbex está dirigido a personas de **13 años o más**. No recogemos deliberadamente datos de menores de 13 años. Si eres el tutor legal de un menor y crees que ha usado el juego, contacta con aleixauque@gmail.com para eliminar la cuenta.

## 9. Seguridad

- Todo el tráfico con el servidor va cifrado por HTTPS/TLS.
- El acceso a la base de datos está protegido por Row Level Security (RLS): cada jugador solo puede leer y escribir sus propias filas.
- Auditamos periódicamente el código para detectar vulnerabilidades.

Ningún sistema es 100 % seguro. Si detectas una vulnerabilidad, escribe a aleixauque@gmail.com.

## 10. Cambios en esta política

Si actualizamos esta política, publicaremos la nueva versión en esta misma URL con la fecha de "Última actualización" al principio del documento. Los cambios entran en vigor inmediatamente.

## 11. Contacto

Aleix — aleixauque@gmail.com
