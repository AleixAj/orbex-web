# Orbex — public landing page + technical write-up of the game

![Godot](https://img.shields.io/badge/Godot-4.6-478CBF?style=for-the-badge&logo=godotengine&logoColor=white&labelColor=2D2D2D)
![GDScript](https://img.shields.io/badge/GDScript-static_typing-355170?style=for-the-badge&logo=godotengine&logoColor=white&labelColor=2D2D2D)
![PostgreSQL](https://img.shields.io/badge/Supabase-PostgreSQL_+_RLS-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white&labelColor=2D2D2D)
![Deno](https://img.shields.io/badge/Edge_Functions-TypeScript-000000?style=for-the-badge&logo=deno&logoColor=white&labelColor=2D2D2D)
![Google Play](https://img.shields.io/badge/Google_Play-published-3DDC84?style=for-the-badge&logo=googleplay&logoColor=white&labelColor=2D2D2D)
![Landing](https://img.shields.io/badge/Landing-HTML_+_CSS_+_vanilla_JS-e34f26?style=for-the-badge&logo=html5&logoColor=white&labelColor=2D2D2D)

<p>
  <a href="README.md"><img src="docs/readme/lang-es.svg" alt="Español" width="170"></a>
  <img src="docs/readme/lang-en-active.svg" alt="English" width="170">
  <a href="README.ca.md"><img src="docs/readme/lang-ca.svg" alt="Català" width="170"></a>
</p>

**Orbex** is a mobile game published on Google Play ([`com.aleix.orbex`](https://play.google.com/store/apps/details?id=com.aleix.orbex)), built end to end by a single person: client, backend, database, payments, telemetry, legal compliance and the website that goes with it.

**This repository contains the landing page** ([orbex.aleixaj.com](https://orbex.aleixaj.com)). The game's code is private, so **this document is its technical write-up**: how it is built on the inside, which engineering problems actually came up and how they were solved.

> **Why it may interest you even if you don't work in games.** The game is the excuse; the work is software. Here you'll find a production PostgreSQL backend with RLS and a pentest, a payment system with server-side verification and idempotency against double charging, queries optimized against a 200,000-row benchmark, telemetry with automated retention, GDPR and Play Data Safety compliance, and a test suite verified by mutation. None of that is specific to games.

---

## Table of contents

- [The project in numbers](#the-project-in-numbers)
- [Part 1 — The landing page (this repository)](#part-1--the-landing-page-this-repository)
- [Part 2 — The game](#part-2--the-game)
  - [Stack and project shape](#stack-and-project-shape)
  - [Content and game modes](#content-and-game-modes)
  - [Client architecture](#client-architecture)
  - [The chain engine, and a measured optimization](#the-chain-engine-and-a-measured-optimization)
  - [Backend: data model and API](#backend-data-model-and-api)
  - [Backend security](#backend-security)
  - [Scale: what breaks under volume](#scale-what-breaks-under-volume)
  - [In-app payments](#in-app-payments)
  - [Advertising](#advertising)
  - [Identity and cloud save](#identity-and-cloud-save)
  - [Remote version switch](#remote-version-switch)
  - [Telemetry and data-driven balancing](#telemetry-and-data-driven-balancing)
  - [Anti-cheat: an explicit threat model](#anti-cheat-an-explicit-threat-model)
  - [In-app moderation and support](#in-app-moderation-and-support)
  - [Internationalization](#internationalization)
  - [Accessibility](#accessibility)
  - [Testing strategy without CI](#testing-strategy-without-ci)
  - [In-house tools](#in-house-tools)
  - [Android performance and deployment](#android-performance-and-deployment)
- [What the project demonstrates](#what-the-project-demonstrates)
- [Contact](#contact)

---

## The project in numbers

| | |
|---|---|
| Client code | **265 GDScript files**, ~98,000 lines, statically typed |
| Backend | **27 SQL files**, ~11,000 lines, **113 functions/RPCs** in PostgreSQL |
| Serverless | 3 **Edge Functions** in TypeScript: purchase verification, refund sync and support translation |
| Tests | **132 headless QA scripts** (harnesses, test doubles, fuzzing and measurement), most of them verified by mutation |
| Content | 256 scenes, **92 levels**, 10 worlds, 16 boss fights, 3 game modes |
| Catalog | 214 cosmetics, 75 achievements, 54 quests, 9 consumable items |
| Localization | **1,155 keys × 10 languages** |
| Global services | 26 autoloads: economy, progress, leaderboard, events, payments, ads, settings… |
| Status | Published on Google Play, version **1.30**, with real players, ads and purchases |

---

## Part 1 — The landing page (this repository)

A static site that serves both as the product page and as the privacy policy URL required by Google Play.

### Stack

**HTML5 + CSS with custom properties + vanilla JavaScript.** Zero build, zero runtime dependencies and zero third-party requests: the entire page is served from its own domain.

It's a decision, not a limitation. A one-page landing doesn't need a bundler, a framework or a pipeline: it needs to load fast, be indexable and not break. With no build, deploying means copying the folder, and the HTML Google sees is the same HTML I wrote.

### What's inside

| | |
|---|---|
| **Bilingual EN/ES** | Both languages live in the same HTML (`<span data-lang>`), CSS switches between them and the preference persists in `localStorage`. Without JS you still see one complete language |
| **Light/dark theme** | Automatic via `prefers-color-scheme` on the first visit, persistent afterwards |
| **Interactive `<canvas>` demo** | A recreation of the game's mechanic: a chain on a Catmull-Rom polyline parameterized by arc length, with the same insertion and cascade logic. It explains the game without asking the visitor to watch a video |
| **Playable web build** | HTML5 export of the real game hosted on itch.io, linked from the hero and both menus. It opens in a separate tab rather than as an *embed*, which is what keeps the zero-third-party-requests promise |
| **Accessibility** | Skip link, `aria-expanded` / `aria-controls`, custom `:focus-visible`, modals with focus trapped and restored, close on Escape, and it respects `prefers-reduced-motion` |
| **SEO** | Open Graph, `hreflang`, sitemap and JSON-LD (`VideoGame` + `FAQPage`) kept in sync with the visible content |
| **No cookie banner** | The YouTube embed starts without a `src` (*click-to-load* pattern) and the fonts are self-hosted, so there is no third-party request at all until the user asks for one |

### Performance

Assets went from **42 MB to 2.6 MB (−94%)** in the optimization pass. Today the folder weighs **4.7 MB** —it has grown with the gallery— and what matters is still measured: scrolling through the entire page costs **496 KB in 30 requests, none to third parties** (measured against production, not against the local server).

- The 10 boss portraits were 34 MB of those 42: 1152×2048 PNGs rendered at ~210 px wide. Each asset is regenerated at the size it's rendered at (2× the CSS size) as `.webp`, with a reproducible Python script.
- The gallery has two resolutions per image: a 720 px thumbnail for the cards and 1280 px for the viewer.
- The three fonts are self-hosted with a Latin subset (**49 KB in total**), instead of two third-party connections and a render-blocking stylesheet on the critical path.
- A single scroll listener for the three things that depend on it, writing once per frame with `requestAnimationFrame`. Decorative animations freeze while a modal is open: they animated `filter` and `background-position`, which repaint instead of compositing.

### Deployment

Any static host. It runs on **Cloudflare Pages** with a custom domain, and there is configuration ready for Netlify and Vercel too. Cache headers (`immutable` on fonts and images) are declared in all three formats.

### Structure and local development

```
orbex-web/
├── index.html              bilingual landing page (11 sections, canvas demo)
├── privacy/index.html      /privacy — served policy
├── PRIVACY.md              bilingual source of truth for the policy
├── assets/
│   ├── fonts/              3 woff2 files with Latin subset (49 KB)
│   └── images/             wordmark, worlds, bosses, orbs, screenshots, flags
├── _headers · _redirects · netlify.toml · vercel.json
└── scratchpad/             tools (not deployed)
```

```bash
python scratchpad/serve.py     # http://localhost:8000
```

It's `python -m http.server` with two things on top, and both are needed: `Cache-Control: no-store` —the bare server caches HTML aggressively and editing the file doesn't show up on reload— and the MIME types for `.webp` and `.woff2`, without which Chrome rejects the fonts **silently** and the page falls back to the system font, which looks like a CSS problem.

The **privacy policy** lives in two files that are always edited together (`PRIVACY.md` and the served page), and it has to stay ahead of what the app does, not behind it: the previous version kept saying "we don't show ads" for two weeks while the SDK was already inside the build — and that's exactly one of the sentences Google Play checks against the Data Safety declaration.

---

## Part 2 — The game

### Stack and project shape

| | |
|---|---|
| Engine | Godot 4.6, Mobile profile (`gl_compatibility`) |
| Language | GDScript with static typing and `class_name` |
| Platform | Android, landscape, 1280×720 base, `minSdk 24` / `targetSdk 36`, `arm64-v8a` |
| Backend | Supabase — PostgreSQL + PostgREST + anonymous Auth + Edge Functions (Deno/TS) |
| Local persistence | JSON files in `user://` with custom atomic writes |
| Native services | Google Play Billing 8.3.0, AdMob with the UMP consent flow, Google Sign-In |

### Content and game modes

10 worlds set in historical eras, 8 levels each and a boss fight closing every world —four of them in two phases and the last one in three, with a screen shatter between phases—, plus a tutorial of five chained screens.

On top of that same content run **two more modes and a weekly event**, and that's where the engineering is: a mode isn't new content, it's a set of flags over the same level. The delicate part isn't what each mode does, but **what it's allowed to write**.

| Mode | What changes | What it can't touch |
|---|---|---|
| **Survival** | The orb supply never runs out and speed increases with orbs destroyed, not with time. No items, no possible victory | Campaign stars and high score. Its own leaderboard |
| **Infernal** | The whole campaign replayed harder. Unlocks after finishing all 10 worlds and gives access to all 80 levels at once | Campaign progress: a **separate** record book for stars and high scores, and a separate leaderboard |
| **Weekly challenge** | A level chosen by the server, the same for everyone, playable even if its world is locked | Nothing that belongs to the player: no stars, no coins, no quests, no achievements |

Three lessons that came out of building them:

- **Separating the record books goes in before raising the difficulty, not after.** While Infernal and the campaign weighed the same, mixing their records gave almost the same result and looked like unnecessary code. As soon as the mode gets tougher, mixing them means **overwriting the player's campaign record with a score set in a different game**, and that can't be fixed after the fact.
- **Isolation has two halves, and the one that gets forgotten is the one that runs live.** The challenge blocked what gets written *at the end* of the match, but the combo and shot counters are recorded shot by shot: for a while, a match in a mode declared isolated kept unlocking achievements and advancing quests. It raised no error — it was spotted by looking at the account of a player who had only played the event.
- **A mode that can be replayed without limit can't feed a counter.** Survival and Infernal can be replayed at no cost, so their achievements count *distinct levels*, not matches. With a counter, the whole ladder —2,050 coins— gets completed in an afternoon by repeating the game's first level.

**Seasonal event.** A parallel currency that's earned by playing and **expires**, redeemable for its own cosmetic catalog within its date window. It has three phases and the middle one is the non-obvious one: after earning closes there's a **settlement** period in which you can no longer earn but can still spend. Without it, the event punishes precisely those who played until the last day and then find their balance evaporated — which is exactly what teaches them not to bother with the next event. What you buy stays forever; what expires is the currency.

### Client architecture

```
+-------------+     +----------------------+     +--------------------+
|  AppRouter  |---->|  OrbexScreen (UI)    |---->|  Level (main.gd)   |
| (main.tscn) |     |  menu / world / map  |     |  + HUD overlay     |
+-------------+     +----------------------+     +--------------------+
       |                                                    |
       v                                                    v
+-------------+                                    +--------------------+
|  Autoloads  |  progress · economy · network      |  ChainBall x N     |
|    (26)     |  settings · events · payments      |  ProjectileBall    |
+-------------+                                    |  Boss              |
       |                                           +--------------------+
       v
+---------------------------------------------------------------------+
|  Supabase — PostgREST (113 RPC) · RLS · pg_cron · Edge Functions     |
+---------------------------------------------------------------------+
```

Three rules hold the separation together:

- **`AppRouter` is the only way to change screens.** No screen navigates to another: they all ask the router. That concentrates scene loading, modals, the Android back-button stack and the match lifecycle in one place.
- **Native SDKs come in through one door and one door only.** `Ads` and `Purchases` are facade autoloads: no screen talks to the Java plugin. You call `await Ads.request_reward(placement)` or `Purchases.buy(sku)` and that's it. The day it has to be ported to iOS (StoreKit) or the ad provider changes, the change stays inside two files instead of being spread across the five screens that hand out money.
- **What gets SAVED and what gets DRAWN are different things.** An equipped cosmetic is kept on disk even if its unlock can't be confirmed at that moment (offline startup, server role not yet received); what changes is what gets drawn. Without that separation, starting up with no signal permanently destroyed the player's selection, because the next save made the loss final.

### The chain engine, and a measured optimization

The core of the game is a row of orbs that advances along a path and accepts insertions at any point: position by arc length (`path_progress`), interpolated insertion, pushing the sub-chain to open a gap, repositioning after a removal and magnetic joining of two separated segments when they share a color. A level can have several independent lanes.

**The problem.** The function that positions each orb made five path queries per ball per frame (position, portal segments, non-attachable segments and two depth layers), and all five were **linear scans of the entire path**. Paths are drawn by hand and they're dense: 164 points in the first level, **361 in the longest**. The cost scaled with `balls × path_points`, not with balls.

**The measurement.** With an instrumented frame benchmark, the most expensive level cost **3.9 ms per frame with 72 orbs** in a normal match, and **9.1 ms** in survival mode, which lifts the on-screen orb limit. At 60 fps the whole frame budget is 16.6 ms.

**The solution.** Binary search over the path's cumulative distances, plus precomputed indices of the marked segments. With one unforgiving detail: teleport segments measure 0 px, so there are repeated values and you need a real `lower_bound` —keeping the first of the ties— instead of a generic binary search. With the generic one, an orb comes out of the wrong portal.

| | before | after |
|---|---|---|
| Most expensive level, normal match | 3.90 ms/frame | **0.22 ms** |
| Most expensive level, survival mode | 9.10 ms/frame | **2.94 ms** |

**The verification.** I reimplemented the five linear versions inside the test harness and compared them with the new ones across **all 92 levels and their 112 lanes**: 178,303 samples, a fine sweep plus the exact edges of each segment and their neighbors within an epsilon. These functions determine where each orb is drawn, how portals fade and whether a shot passes through a segment. An *off-by-one* here isn't caught by any other test and doesn't raise an error: it simply looks wrong.

### Backend: data model and API

**Supabase, with all the logic in PostgreSQL functions.** The client doesn't run `INSERT` or `UPDATE` against any table: every write must go through a `SECURITY DEFINER` RPC that validates before writing.

Subsystems with their own schema:

| Subsystem | What it solves |
|---|---|
| Leaderboard | Paginated boards by scope and level, the player's exact rank and neighborhood (you ± N rivals) |
| Public profiles | Another player's card: nickname, equipped cosmetics and stats |
| Cloud save | Progress backup and transfer codes between devices, single-use and with expiry |
| Purchases | Catalog, receipt redemption, idempotent delivery and revocation on refund |
| Weekly challenge | Level drawn on the server, the same for everyone, with its own leaderboard and automatic rewards |
| Mailbox | Server-to-player messaging, with read status and reward claiming |
| Friends | One-way adding, notifications and a filtered leaderboard |
| Moderation | Sanctions, player reports and in-app support |
| Telemetry | One row per match plus aggregates, with automatic purging |

Eight scheduled jobs with **`pg_cron`**: seven nightly ones —telemetry purge at 90 days, daily active-user roll-up, cleanup of orphaned anonymous accounts, refund sync with Google and trimming of friend notifications, reports and support messages— plus the weekly challenge close, which hands out its rewards through the mailbox.

> What isn't purged is as deliberate as what is: an unresolved report or an unanswered support message **isn't deleted for being old**, because those are precisely what nobody has dealt with yet.

### Backend security

The anonymous key is embedded in the APK by design, so **the threat model assumes anyone can invoke any RPC with any argument**. What prevents abuse is the server, never the screen.

- **Every `SECURITY DEFINER` function pins its `search_path`.** Without that, a manipulated `search_path` hijacks the calls inside the function body.
- **No table has a write policy.** RLS is the only barrier and it isn't disabled on any table.
- **Ownership guards** (`auth.uid() = p_id`) on every RPC that accepts a player identifier.
- **Column-level grants** on the players table: public reads serve 16 profile columns, while the economy, telemetry and sanction status stay out.
- **`anon` can reach seven functions, and all seven are read-only.**

> **A real bug that teaches the lesson.** `REVOKE EXECUTE ... FROM anon` **does nothing on its own**: PostgreSQL grants `EXECUTE` to `PUBLIC` when any function is created, and roles inherit from there. The correct form is `FROM public, anon`. Thirteen functions had that mistake and one was serious: the one that assigns roles was reachable from the public API, meaning anyone with the APK's key could grant themselves admin permissions. Fixed and verified with an **8-vector pentest** —role assignment, direct table writes, score submission, deleting someone else's account, restoring someone else's progress—: all blocked, with the victim's data intact.

There's also a verification rule: an RPC isn't considered good until **it has been called against the database**. Two functions were created without a complaint and blew up when executed — one because of a variable with the same name as a column (`plpgsql` resolves against its variables first), the other because it treated as a boolean a function that raises an exception. Functional trials are done with a `DO` block that ends in `raise exception`: the transaction aborts itself and not a single row persists.

### Scale: what breaks under volume

With 20 players everything is fast. Problems show up with a large player base, so the critical queries were measured against a **benchmark of 200,000 players and 400,000 score rows**, with `EXPLAIN (ANALYZE, BUFFERS)`.

**1. The tie-breaker `OR` prevented index use.** "How many people are ahead of me" translates naturally to `score > X OR (score = X AND fecha < Y)`, and the planner can't bound either branch inside an `OR` via the index: it falls back to a scan with the condition as a filter. Split into two range counts —the sets are disjoint—, each branch goes through the index.

| | plan | buffers | ms |
|---|---|---|---|
| Before | Bitmap Heap Scan of 154,915 rows | 2,283 | 28.9 |
| After | two Index Only Scans, `Heap Fetches: 0` | **618** | 18.8 |

**2. A regular `JOIN` read the entire players table on every call.** A page's `LIMIT` is a *runtime* value, so the planner estimated thousands of rows, chose a Hash Join and did a `Seq Scan on players`. A `JOIN LATERAL` can't be *hash*-joined, so it forces a Nested Loop against the primary key and the join applies only to the 50 rows of the page. It's a constant that grows with the **player base**, not with who is playing:

| | before | after |
|---|---|---|
| First page of the leaderboard | 1,432 buffers / 11.1 ms | **785 / 2.6 ms** |
| First page of survival | 2,505 / 31.6 ms | **885 / 4.8 ms** |

**3. Tuned autovacuum.** The leaderboards receive one `upsert` per match played, and `Index Only Scan`s depend on the visibility map. With the default value, cleanup doesn't kick in until 20% of the table is dead tuples: with 200,000 rows that means a stale map for almost the entire active week, and the same query goes from 202,847 to **601,921 buffers (×3)**. Lowered to 0.02, including `insert_scale_factor`, which is the one that matters for tables that grow by insertion.

**Before deploying each rewrite, a row-by-row comparison against the current version on real data**: 5,460 cases in the leaderboard neighborhood (all scopes × all players × three radii), 1,155 in the rank query and 273 in the page query. **Zero differences.** A query whose result the player sees as their rank can't be validated by eye.

> A methodological warning that cost an afternoon: a micro-benchmark that measures the two versions **in consecutive blocks** is useless for comparing queries — the order and cache state decide the result, and the first measurement showed exactly the opposite of reality. What doesn't lie is `EXPLAIN (ANALYZE, BUFFERS)` with alternating measurement and prior warm-up.

### In-app payments

Google Play Billing 8.3.0 with **server-side verification**. It's the subsystem with the most failure surface in the project, because mistakes cost real money in both directions: delivering without charging, or charging without delivering.

**The flow.** The client launches the payment sheet → Google returns a receipt → an **Edge Function** validates it against the `androidpublisher` API with a service account → an atomic RPC records the purchase and returns what to grant → the client delivers → the server acknowledges the purchase with Google.

The decisions that hold it up:

- **The amount comes from the server's catalog, not the client.** The client sends the SKU; if the server responds with a different amount, the server's amount is credited. The only thing the client chooses is which SKU goes to the payment sheet.
- **The purchase token is unique GLOBALLY, not per player.** With a unique index on `(player, token)` —which is what comes out of thinking "each player has their own purchases"— a receipt bought once would work for every account you passed the token to.
- **Three safety belts against double delivery**, and all three are needed: the shortcut for already-settled tokens, the local log of delivered items and the server's `delivered` field. Google **redelivers** everything that hasn't been consumed on every connection, so the same token coming back is normal; all it takes is the app closing between delivery and consumption to credit twice. It can be reproduced at will with airplane mode.
- **The server does the acknowledgment.** Google automatically refunds any purchase not acknowledged within 3 days: leaving it to the client means that anyone who doesn't reopen the game undoes their own purchase with the product already delivered.
- **Refunds apply themselves.** A nightly Edge Function queries Google's list of voided purchases and revokes the permanent content. The queried window is **persisted**, because the API only returns 30 days: without that, a month without running it leaves the gap out of reach forever.

**How to test something that moves money.** With a test double for the billing client and another for the backend, a harness goes through the **19 server failure reasons** —Google's, the SQL ones and the transport ones— plus five malformed responses, and checks in each one that **nothing is granted and the token isn't consumed**; consuming it would throw away a paid purchase. And another harness answers the question the player asks —*do I get something for free by turning on airplane mode?*— by measuring balance and inventory before and after each path, instead of reading the code.

> The most expensive bug in this subsystem raised no error: the remote sales permission reached the client and **was discarded on the last line**, because the parsing built its dictionary by hand with three keys and the fourth got lost along the way. The store said "Coming soon" no matter what was in the database. The rule that came out of it —a new key in the response must also be added to the client's parsing— is now enforced by a test that extracts the keys from the SQL itself.

### Advertising

AdMob behind the facade autoload, with three pieces that aren't obvious until you test on a real phone:

- **Per-unit cache with expiry.** The rewarded ad was requested inside the `await` itself, so every tap waited up to 10 seconds with an unresponsive button. Today it's served from a cache that refills itself, with a 50-minute expiry: AdMob considers a preloaded ad valid for about an hour, and past that deadline the player would be left **without a reward after having tapped**, which is worse than waiting.
- **An overlay with a 350 ms delay.** With the ad preloaded there's no wait, and a half-frame flicker reads as a glitch, not as "loading".
- **Safety timeouts on every state set up around an `await`.** A coroutine can die mid-wait —the plugin crashes, the tree goes away— and then the line that releases the state never runs. That pattern bit three times in the same file, each time with a different cost: a permanently locked screen, an ad unit that never preloads again, and a dead button. All three are closed the same way: the state **expires** instead of relying on its own release.

### Identity and cloud save

Playing doesn't require an account: an anonymous session per device. Linking Google is optional and **converts the anonymous account into a permanent one while keeping the same `auth.uid()`**, so scores, profile and save data survive without migrating anything.

The three hard cases:

1. **Linking to a Google account that already has its own identity** (reinstalling, switching phones) is the *common* case, not the exceptional one. It's detected, falls back to a normal sign-in and opens a dialog comparing both progress states so the player can choose; the orphaned anonymous account is deleted so it isn't duplicated on the leaderboard.
2. **A link that succeeds on the server but whose response is lost** (timeout on a mobile network) returns "that identity already exists" **against yourself** on retry. Without an explicit check, the conflict flow ended up deleting your own account.
3. **Transferring progress to another device** is *moving*, not copying: redeeming plants a tombstone that the source device consumes on its next startup, clearing local data. Without it, the source uploads its intact copy again and duplicates purchases in a loop.

Local saving uses **custom atomic writes**: temp file, reread and validation, rotation of the current file to `.bak`, rename. Godot's `WRITE` mode truncates on open, so a process killed mid-write left the file empty and the player lost coins, stars and inventory all at once — a far-from-theoretical risk, because several services flush to disk right on `APPLICATION_PAUSED`. Restoring from the cloud is also transactional, with a sentinel that allows it to resume if it dies halfway.

### Remote version switch

Google Play doesn't force anything on its own: an old build keeps opening forever. Two thresholds in a server table —warning and block— make it possible to pull a broken build out of circulation without publishing anything, and they double as a *kill switch*.

Three properties decided on purpose:

- **It fails open.** With no network, with the RPC down or with an unreadable response, you can play. Blocking someone who couldn't verify leaves anyone on the subway stranded.
- **"Doesn't apply" and "couldn't check" are different states.** Collapsing them left the client convinced it was up to date throughout the whole process; separated, the second one retries with increasing backoff.
- **The warning appears once per version**, not once per startup —it becomes the screen you close without reading— nor once per install, which would silence every future update.

Version comparison is numeric per segment and tolerant of odd formats: a lexicographic `1.10 < 1.9` would have blocked everyone on 1.10.

### Telemetry and data-driven balancing

Every finished match sends Supabase a row with ~40 fields: outcome, cause of defeat, how far the chain got, accuracy, score breakdown, items used, net time excluding pauses and the actual difficulty it was played at. There are aggregates per player and level, automatic purging at 90 days, a rate limit per row class and a toggle in Settings for GDPR.

**What it's really for:** the star threshold for each level is calibrated with `percentile_cont` over real scores, not by eye. And design decisions are made with the measurement in front of you:

- The difficulty curve was flattened after confirming that from world 5 to 9 the demand moved ±3% and world 10 was **below** world 3.
- An entire family of quests was rewritten after discovering that the most active player had **zero quest coins in 78 matches**: three objectives were mathematically unreachable, and one asked for a combo that hadn't happened even once in 268 matches.
- The third-star threshold was lowered after measuring that **none of 51 victories** reached it; the best one fell 1.3% short.
- Infernal mode's difficulty was split **equally between orb count and speed**, and it isn't decorative symmetry: the two halves pull in opposite directions on the clock —more orbs lengthen the match, more speed shortens it—, so loading everything onto one changes the duration by 9% without anyone asking for it. Split at the square root of the factor, the demand goes up and the match lasts the same.

> **A bias that invalidates the measurement before you start: which player you measure against.** Calibrating Infernal mode with general telemetry was useless — 69 of the 82 victories with context came from new players in the first three worlds, and you can only enter that mode after finishing the game. They're two different populations shooting at different rates, so the aggregate percentile describes someone who will never play it.

> **And a data bug that cost six days.** The score for a multi-phase fight arrived with the first phase counted twice. It raised no error: the only symptom was a residual in a consistency check, and it was explained with a reasonable and false hypothesis. Based on those inflated ratios, four fights were recalibrated **in the opposite direction**, leaving them trivially easy for almost a week. The lesson was written down in the repository: a systematic residual gets **cross-checked against another source** before explaining it — comparing against the table the leaderboard writes through a different path would have been enough.

### Anti-cheat: an explicit threat model

What matters here isn't the list of defenses, it's where the line is and why.

**What the server enforces**, independently of the client: caps per submitted score, a per-player rate limit, a whitelist of worlds and levels, ownership guards on every RPC, and table triggers —not an `if` spread across six functions— so that a sanctioned player can't write to any leaderboard, neither today nor on the seventh leaderboard added a year from now.

**What's assumed lost**: on a device with file access, the wallet is a local JSON file. Whoever can edit it doesn't need to fake any purchase. Closing that would require moving the entire economy to the server, which is a cost this project doesn't pay.

**What is closed, because it's what costs money**: a real purchase can't be turned into two. The defenses are sized with that hierarchy in mind — hardening quests while leaving the wallet local would be security theater.

All of this is reasoned in writing in an internal design document, including the decision **not** to move quest counters to the database: a server can't validate a quest without validating the gameplay, so it's still the client that says "done".

### In-app moderation and support

With real players come problems that aren't technical, and they need tools.

- **An admin panel inside the game**, with the role verified on the server (`auth.uid()`, never a parameter): player search, full profile, reversible sanctions and development utilities. The function that assigns roles **isn't exposed**: its abuse is irreversible by definition, so it stays in the database dashboard. An admin can't sanction another admin or themselves.
- **Player reports** with five defenses against coordinated campaigns —one row per pair, a daily limit, having to have played, a sanctioned player can't report, bounded purging— and **no automatic sanctions**: the count orders the list, but deciding is still a button a person presses.
- **In-app contact and appeals**: the player writes from inside the game and the reply arrives in their mailbox. A sanctioned player **can still write**, because it's their only way to appeal and closing it would leave any mistake with no way back.
- **Support translation** with DeepL through an Edge Function, because the game is published in ten languages. The key lives on the server and the endpoint checks the caller's role: without that, it's a free paid-translation proxy for anyone who reads the key from the APK.

### Internationalization

**1,155 keys × 10 languages** (EN, ES, CA, pt-BR, FR, IT, DE, JA, KO, RU) from a single CSV compiled by Godot's importer; the CSV isn't read at runtime. Automatic detection of the system language on first launch and hot switching.

What I learned doing it, which doesn't appear in any tutorial:

- **No plurals.** The target doesn't go in the sentence, it goes in the progress bar. With Russian having three plural forms, putting `{n}` in every string is the fast track to broken translations. When there is a number, the unit goes in the label and the value stands alone: `DÍAS DE RACHA: 3` (streak days) instead of `3 DÍAS`, which on the first day of any install showed **"1 DÍAS"** ("1 DAYS") in eight languages.
- **Gender agreement is the same problem with another face**, and the way out isn't a gender table: it's writing a sentence that doesn't need to agree.
- **Text is a layout constraint, not a final detail.** There are harnesses that measure the real width of every button in all ten languages against its slot, because a label that overflows isn't clipped: **it widens the container**, and in a centered panel that pushes it out on both sides without the layout complaining.
- **A vocabulary audit per language** found up to four different words for the same concept within a single language —the tutorial used a term that never appeared again in the whole game— and two strings that said something **false**: one promised Korean players they couldn't write their name in their alphabet, when in fact they could.

### Accessibility

Color-blind mode with two independent toggles: an alternative palette and geometric shapes on the orb.

The first palette **didn't work**, and a real color-blind player said so: "it looks practically the same to me". Measured with the Viénot-Brettel-Mollon transform on the color coming out of the shader, under deuteranopia two of the four colors were at distance 23, and in grayscale all four fell within 5.6 — they collapsed into two colors. The current palette (adapted Okabe-Ito) raises the worst case to 17.2, and what really separates the colors **is lightness** (L\* 43 / 60 / 79 / 97), which is the only thing every type of color blindness preserves.

Even so, color alone isn't enough: an optimizer over all four types at once tops out around distance 20. That's why the primary channel is the **shapes**, with the outline thickness measured at the real resolution they're drawn at — on a light orb, a white fill has a 1.06:1 contrast against the body, so the shape is read only by its outline. And the classic-mode textures are **generated** with the same formula as the shader, so an orb looks the same with and without a skin by construction.

### Testing strategy without CI

**132 QA scripts in GDScript**, runnable headless, plus a runner that executes them all and summarizes what fails. There's no testing framework: they're scripts that boot the real game, do something and measure.

The principles that make them useful:

- **Mutation verification.** A harness that has never been red proves nothing. Almost all of them are validated by manually reintroducing the bug they're chasing and checking that they turn red. Several times that revealed that the test was measuring something else: one check looked for an identifier that also appeared in a comment, so it passed green with the line deleted.
- **Measure the outcome, not the source code.** "Do I get something for free in airplane mode?" is answered by measuring the balance before and after, not by reading the `if`.
- **The harness sets up the state it wants to measure, never inherits it.** Several tests failed or passed depending on who launched them, because they read the machine's real progress. And every script that writes to disk goes through a safety net that backs up and restores the save files, identified by PID, because two harnesses running in parallel were overwriting each other's backup.
- **Some things can only be seen by looking.** A particle effect spawned entirely off-screen and its own comment claimed the opposite; the node tree state was perfect. For that, the capture harnesses rasterize and **measure the pixel**: an overlay's darkening is checked by average luminance, not by the value of the `alpha` property.
- **The runner's first full pass found three harnesses red on healthy code**: checks anchored to the position of a literal that had moved. A harness that fails for no reason is worse than not having one, because it teaches you to ignore red.

On top of that: a fuzzer that fires at random points for thousands of frames over a sample of levels, with a seed derived from the path so a failure can be reproduced, and a script that loads every GDScript in the project to catch compile errors no test would touch — the application's root file isn't compiled by any harness, and a syntax error there leaves the game unable to start with the whole suite green.

### In-house tools

- **A Godot editor plugin** (`EditorPlugin` + `@tool` + `_forward_canvas_gui_input`): Shift+click in the viewport to draw the paths, with suffixes in the marker name that define special segments (portal, non-attachable, two depth layers, end of the entry sprint) and automatic two-pass renumbering.
- **Python scripts** for what shouldn't be done by hand: measuring the real length of the 92 paths —replicating the game's exact metric— to recalibrate speed per level, generating the color-blind mode textures, preparing orb skins with tonal range remapping, and regenerating all the website's assets at the size they're rendered at.
- **A Node simulator** of the landing page's canvas demo, which reads the constants from the HTML itself. In the browser, measurement lies: with the tab in the background `requestAnimationFrame` drops to 1 fps and every count comes out as zero.

### Android performance and deployment

- Dual VRAM texture compression (desktop and Android) with automated audits of the import files: Godot creates a new texture's `.import` with default values and doesn't inherit its neighbors' — 40 textures went in uncompressed in a single batch, without any warning.
- A monitored asset budget: 45 profile portraits went from PNG to JPG (4.2 MB → 1.7 MB) because they're opaque illustrations, which is exactly what PNG compresses worst.
- A configurable FPS cap (30/60) and never "unlimited", because of thermal throttling. The simulation's speed caps are in pixels per **second**, not per frame, or the FPS setting would change the simulation speed — unacceptable with a leaderboard behind it.
- Google Play compliance: a custom privacy policy with GDPR, in-app account deletion (RPC + cascade + local cleanup, including the `auth.users` row, which is where the email lives), a Data Safety declaration in sync with what the app actually does, and IARC rating.

---

## What the project demonstrates

Translated into what a job posting looks for:

| Skill | Where it is in the project |
|---|---|
| **Database design** | 27 schemas, 113 RPCs, RLS, triggers, partial indexes, jobs with `pg_cron` |
| **Query optimization** | 200,000-row benchmark, `EXPLAIN (ANALYZE, BUFFERS)`, `JOIN LATERAL`, tuned autovacuum, row-by-row verification before deploying |
| **Security** | Pentest of the public API, `SECURITY DEFINER` with pinned `search_path`, column-level grants, written threat model |
| **Payment integration** | Billing with server-side verification, idempotency, double delivery closed with three safety belts, automated refunds |
| **Performance optimization** | Profiling, algorithmic bottleneck identified and measured (x18), asset budget |
| **Architecture** | Facades over native SDKs, single navigation router, separation between saved state and drawn state |
| **Testing** | 132 QA scripts, mutation verification, fuzzing, tests that measure pixels |
| **Data engineering** | Telemetry with automated retention and product decisions made with real percentiles |
| **i18n and a11y** | 10 languages with a vocabulary audit; color-blind accessibility validated against scientific literature and with a real user |
| **Compliance** | GDPR, Play Data Safety, account deletion, moderation, maintained privacy policy |
| **Autonomy** | From idea to store with no team: product, backend, client, UI art, web, legal and operations |

And one thing that doesn't fit in the table: **the documentation**. The game's repository keeps a decision map where every non-obvious choice is written down with its reasoning, its measurement and what the previous mistake cost. Many of the warnings quoted in these sections come from there. It's what keeps a 98,000-line project written by one person modifiable a year later.

---

## Contact

**Aleix** — development, backend, design, UI art and web.

- Email: [aleixauque@gmail.com](mailto:aleixauque@gmail.com)
- Web: [aleixaj.com](https://aleixaj.com)
- The game: [Orbex on Google Play](https://play.google.com/store/apps/details?id=com.aleix.orbex) · [orbex.aleixaj.com](https://orbex.aleixaj.com)

> The game's code is private. I'm happy to show it or discuss any of the systems above in an interview.
