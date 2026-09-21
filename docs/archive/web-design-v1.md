# Web design v1

Superseded 2026-09-21 by [web-design.md](../web-design.md). v1 is the civic-fact-desk IA: sleeve → slice, catalog as site, preview as a different prefix. It predated the design-philosophy rewrite (modern, welcoming, civic publisher, generous). Do not implement from this file.

Front-end Architect. Information architecture, SEO, navigation, and HTTP surface of the civic CMS. Persona: [front-end-architect.md](../personas/front-end-architect.md). Tone: [design-philosophy.md](../design-philosophy.md). How a slice **looks** is [design-system.md](../design-system.md) (UI/UX Developer). How it **reads** is [editorial-guidelines.md](../editorial-guidelines.md) (Content Editor). Serving pointers: [architectural-blueprint.md](../architectural-blueprint.md) (Platform). Topic menu: [topic-charters.md](../next/topic-charters.md).

```text
role:           civic fact desk — findable official numbers, no verdict
shape:          sleeve → slice (citizen question) → optional geography
stack:          Astro SSG; one vintage per render tree; two prefixes
cms:            templates + one vintage → one tree (home, hubs, slices, house, 404)
now:            `/` is the desk home (`index.html`); slices at `/{sleeve}/{slice}`
```

## Decision

A citizen reaches one **question**, on one **stable URL**, bound to one **published** vintage. Preview uses the same templates and the same relative paths. Isolation is a different, non-public prefix plus `noindex` — not a `/preview` path on the citizen host.

The CMS is that tree, not a folder of hand-built pages. One Astro build per vintage emits every page type below. A template in git is not a public URL until it **binds in this vintage**.

USAFacts is the *answer-page role* (question, fact-lede, evidence, method). Do not copy `/answers/…/country/united-states/`, a search box, newsletter, or media desk.

Content Editor writes the citizen question and the fact-lede. This file maps those words onto routes, `<title>`, meta, and chrome. It does not invent a second question.

## Now vs target

| | Built today (preview tree, 2026-09-19) | Required (this file) |
|--|-----------------|----------------------|
| CMS tree | One build → desk home, five hubs, three bound slices, house, 404 | Met |
| Home | `/` is the desk home; H1 is the Purpose sentence; `.fast-facts` from the catalog | Met |
| Slice URL | `/prices/retail-prices`, `/people/population`, `/money/union` | Met |
| Catalog | `site.json` in bound inputs; shell, home, hubs, and `/sources` read it | Met; must also feed the slice hottest-rail |
| `<title>` | `citizen_question` on a slice; hub, house, and 404 formulas | Met |
| Head | title, description, OG, `twitter:card`, JSON-LD; no canonical or `og:url` in shared HTML | Met; citizen serve injects the absolute URLs |
| Nav | `SiteShell` on every page: skip link, lockup → `/`, five sleeves, breadcrumb, footer | Met |
| Serve | Slashless path → `{path}/index.html`; `{path}/` 301 → `{path}`; preview sends `noindex, nofollow` and `private, no-store` | Met; `robots.txt` and sitemap still owed on the citizen prefix |
| Hottest-rail | Hashes plus catalog siblings from `site.json` | Met |
| 404 body | H1 and a link to `/` | Quiet sentence, links to `/` and the five sleeves |

`/` is the landing page. Do not serve a slice body at `/`. Each page type is its own route (`/prices/retail-prices`, `/people/population`, `/how-this-works`, …). The C1 question has one public URL: `/prices/retail-prices`. Do not keep a second copy of that article at `/`. Do not 301 `/` to C1.

Do not wait for a second published slice to move C1 off `/`. Do not retune the pipeline for URLs. Slugs live on the template, not in Parquet.

---

## Page types

| Type | Job | Observations |
|------|-----|----------------|
| **Desk home** | Bound facts from **this desk’s catalog** | Fast-facts slots from that catalog only |
| **Sleeve hub** | List of catalog slices in that sleeve | Optional one-line bound fact per slice; not a second explainer |
| **Slice** | Answer page: question → fact-lede → evidence → method | Required. Scan path in the editorial guidelines |
| **Geography slice** | Same template, one bound unit | Later, named. Pre-render from **this** vintage. Districts parked |
| **House** | How this works; sources | No invented figures. Cites if a number appears |
| **Retained vintage** | What the page said then | Same tree under `/archive/{vintage_id}`; not in the sitemap |
| **Preview** | Full desk including unpublished slices | Same relative paths; different host; not a page type in the tree |

Do not add: search, subscribe, social row, press kit, newsletter, chat, “get notified”, download hub, most-viewed, live AQI pin-map, how-to filing pages.

---

## Site shell (shared layout)

One layout wraps every route. It is **not** a page type and it has **no** URL of its own. Header and footer live here. `main` is the page type.

```text
[ skip link → #main ]
[ 3px --mark rule ]
header    Prism lockup → `/`     People  Work  Money  Prices  Delivery
main      desk home | sleeve hub | slice | house | 404
footer    sleeves · how this works · sources
```

`index.html` at the tree root is the desk home. A slice’s `index.html` lives under that slice’s path (`prices/retail-prices/index.html`), never at `/`. Slice interior (hero, stat-row, chart wells) is [design-system.md](../design-system.md) — not this shell.

Skip link is the first focusable control (`Skip to content`, `href="#main"`). `<main id="main">` wraps the page type. Tokens for the link are UI/UX Developer.

---

## Page URLs and hierarchy

**Rules.** ASCII kebab-case. Lowercase. No trailing slash (matches `src/cms/astro.config.mjs`). No `.html` in the citizen path. No charter id (`c1`) and no `vintage_id` in a live path. English official names for geography slugs. Stable when a vintage refreshes — new numbers, same URL.

```text
/                                  desk home
/{sleeve}                          sleeve hub
/{sleeve}/{slice}                  national (or Union-only) slice
/{sleeve}/{slice}/{geo}            later: one state / UT
/how-this-works                    house: official sources, no verdict
/sources                           house: producers as cited
/archive/{vintage_id}/…            retained published tree (same paths under the prefix)
```

**Sleeves.** Same five as [team.md](../team.md). Front matter `sleeve` is the token. First URL segment and chrome labels are this table. Unknown token fails the render. Not topic-family nicknames, not USAFacts chapters.

| `sleeve` (front matter) | Path | Header link | Hub H1 / breadcrumb |
|-------------------------|------|-------------|---------------------|
| `people` | `/people` | People | People |
| `work` | `/work` | Work | Work |
| `money` | `/money` | Money | Money |
| `prices-and-production` | `/prices` | Prices | Prices and production |
| `delivery` | `/delivery` | Delivery | Delivery |

Header uses the short **Header link** column so the row wraps. Hub title, breadcrumb, and hub `<title>` use **Hub H1**. Footer sleeve names match the header links.

**Wave 1–2 slices.** `slug` is declared on the template. `template_id` stays internal. `sleeve` in this table is the **path** first segment (see token map above).

| Charter | Path sleeve | `slug` | Citizen path | Citizen question |
|---------|-------------|--------|--------------|------------------|
| C1 | prices | `retail-prices` | `/prices/retail-prices` | How fast are retail prices rising in India, including food? |
| C2 | people | `population` | `/people/population` | How many people live in India, where, and how is that changing? |
| C3 | money | `union` | `/money/union` | What does the Union collect, and what does it spend it on? |
| C4 | work | `labour` | `/work/labour` | How many people are working, seeking work, and what do they earn? |
| C5 | money | `states` | `/money/states` | What do states and UTs collect and spend? |
| C6 | people | `school` | `/people/school` | Who is in school, and what does the official record say about schools? |
| C7 | people | `health` | `/people/health` | How do births, deaths, child survival, and nutrition stand in the official record? |
| C8 | delivery | `food-and-farm` | `/delivery/food-and-farm` | What does the official record say about foodgrain, and what does the public food system deliver? |

C9–C20 get a `slug` when Charter opens them. Do not mint `/answers/` or a 10-K path.

**In-page questions** (C1 `#food`, `#states`, …) stay hashes on the slice until Charter splits them. A hash is not a second canonical.

**Geography (later).** `{geo}` is the official English name, kebab-case, from the geography frame — not an LGD code in the path. National slice has no `{geo}` segment. Do not ship thin doorway pages (a number and no evidence). A geography URL is the same slice template bound to that unit. Client filter over observations already in **this** vintage is allowed; a dropdown that fetches another vintage is not.

**Aliases.** One public slug per slice. If a path must move, 301 the old path to the new one on the **citizen** prefix only. Do not 301 preview. Moving C1 off `/` is not an alias: `/` stays the desk home.

---

## CMS tree (desk → site)

Not a hand-built page per charter. Not one Astro route that *is* C1.

```text
templates in git  +  each template’s bound vintage
        → bind every template this desk can complete
        → filter by cms_mode (preview: all; citizen: published only)
        → site.json (route catalog for this desk)
        → one Astro SSG
        → data/renders/{vintage_id}/
```

A template in git that cannot bind (missing vintage) is omitted from the catalog. It does not fail the whole tree unless it is a **required** template. It is not listed on home, hubs, or hottest-rail.

### Inclusion

| In this desk | Preview | Citizen (publish) |
|--|---------|-------------------|
| Desk home, five hubs, house, 404 | Always | Always |
| Slice | Bind succeeded | Bind succeeded **and** `bound_vintage_id` is the citizen pointer |
| Geography slice | Later | Later |
| `/archive/{vintage_id}` | Later | Later |
| `robots.txt` / `sitemap.xml` | Not in the tree | Citizen **serve** only |

C2 and C3 on preview while citizen is still C1 is expected. Do not 301 preview. Do not list unpublished slices on the citizen home.

### On-disk tree

Citizen path has no trailing slash and no `.html`. Every page except 404 is `index.html` in that folder. Do not also emit `{path}.html` (a second URL). Root `index.html` is the desk home, never the C1 article.

```text
data/renders/{vintage_id}/
  index.html                              /
  404.html                                HTTP 404
  how-this-works/index.html               /how-this-works
  sources/index.html                      /sources
  people/index.html                       /people
  work/index.html                         /work
  money/index.html                        /money
  prices/index.html                       /prices
  delivery/index.html                     /delivery
  prices/retail-prices/index.html         /prices/retail-prices   (C1, when bound)
  money/union/index.html                  /money/union            (C3, when bound)
  _astro/                                 hashed assets; not a page
  {sleeve}/{slice}/charts/{id}.vl.json    not a page; not in the sitemap
```

Vega JSON sits beside its slice so two templates cannot collide on `/charts/{id}`. It is not a page type and must not be linked as a citizen URL.

**COMPLETE** for this wave requires: desk home, `404.html`, both house pages, all five hubs, and every **required** slice file (C1 → `prices/retail-prices/index.html`). A non-required template that did not bind does not block COMPLETE. Tests that treat root `index.html` as C1 are wrong once this tree ships.

### URL resolution (both prefixes)

The render tree is the **document root** of that prefix. Isolation is a different host (or equivalent private origin), never a `/preview` path segment on the citizen host.

```text
GET {path}           → {path}/index.html     200
GET /                → index.html            200
GET {path}/          → 301 to {path}         keep trailingSlash never
GET unknown          → 404.html              404
GET /_astro/…        → file                  200; not in the sitemap
```

Platform serving must map a slashless path to `index.html` without advertising a trailing-slash URL. Python’s default directory redirect is not this contract.

All `href` and asset URLs in the HTML are root-relative from that origin (`/prices/retail-prices`, `/_astro/…`). Do not bake `{CITIZEN_ORIGIN}` into nav, canonical, or assets in the shared file.

### Route catalog (`site.json`)

Bound inputs, not a citizen URL. Do not serve `/site.json`. Home, hubs, header/footer, home `.fast-facts`, and head tags read this object. They do not glob `src/cms/templates/` to decide what is live.

```text
vintage_id
sleeves[]     locked five: token, path, header_label, hub_label
slices[]      only bound-in-this-vintage:
                template_id, sleeve, slug, path,
                citizen_question, fact_lede (plain text after bind),
                fact_lede_one_line (first sentence of fact_lede),
                vintage_id (that slice's bound vintage, not the tree's)
house[]       /how-this-works, /sources
```

Fail the render if: two catalog slices share sleeve+slug; `slug` or `citizen_question` is missing; `sleeve` is not in the token table; a slice path collides with a hub or house path; the bound fact-lede is empty while the slice H1 shows; `fact_lede_one_line` is empty while a home or hub card for that slice shows.

### Astro files (UI/UX implements; do not invent others)

```text
src/cms/src/layouts/SiteShell.astro              shared shell; no URL
src/cms/src/pages/index.astro                    desk home
src/cms/src/pages/how-this-works.astro           house
src/cms/src/pages/sources.astro                  house
src/cms/src/pages/404.astro                      404
src/cms/src/pages/[sleeve]/index.astro           hub; params = five path segments
src/cms/src/pages/[sleeve]/[slice]/index.astro   slice; params = catalog only
```

Unknown sleeve or slug is a 404, not an empty invented page. Empty **hubs** are 200 (quiet empty). `trailingSlash: "never"` stays. `build.format` must produce the on-disk tree above (directory `index.html`, not a parallel `{path}.html`).

Do not add `/answers/`, geography folders, or `archive/` this wave.

---

## Navigation and UI/UX architecture

Site chrome is UI/UX Developer, not Content Editor copy. Tokens and first-screen scan path stay in [design-system.md](../design-system.md). The regions below are the shared shell in [Site shell](#site-shell-shared-layout). Lists of slices are **catalog** lists, not the git templates folder.

```text
[ skip → #main ]
[ 3px --mark rule ]
[ Prism ]     People  Work  Money  Prices  Delivery     ← header
[ breadcrumb on hub + slice ]
[ main ]
[ footer: sleeves · how this works · sources ]
```

**Header.** Text lockup `Prism` always links to the desk home `/`, never to C1. Sleeve links list the five sleeves (a sleeve with no catalog slice still goes to its hub — quiet empty, no invented figures). Current sleeve: `aria-current="page"` on that hub; on a slice, `aria-current="true"` on its sleeve link. No search, subscribe, social, or “Ask the data”. No geography picker until geography routes exist.

**Breadcrumb** (hub and slice, not home, not house): `Prism / {Hub H1} / {citizen question}`. Links: home, sleeve hub, current page is text. The question in the crumb is the H1, not the slug. House pages have no breadcrumb.

**Slice body.** Layout primitives Content Editor may name (`hero`, `stat-row`, `section`, `how-this-is-measured`, compact source byline). `.hottest-rail` is further questions on **this** page (hashes) plus links to **catalog** sibling slices — featured citizen questions, not scoops. Author-written in-page hashes render first, in template order. Then up to three sibling links taken from `site.json`, in catalog order (charter order), the current slice excluded, link text the sibling's `citizen_question` verbatim. If the catalog has no sibling, the rail is hashes alone — no empty group, heading, or placeholder. Templates do not type sibling questions. Render must not emit an `href` whose path is missing from this vintage’s catalog.

**Desk home.** Not a news homepage and not GDP as the hero ([topic-charters.md](../next/topic-charters.md) C16). Order:

1. Skip link + lockup + sleeve nav (the shell)
2. H1 = desk line: the Purpose sentence in [vision.md](../vision.md) (“A shared, checkable picture of India that does not belong to a party, a ministry, or a news cycle.”). Not a slogan box; not a second citizen question
3. `.fast-facts` — one card per catalog slice, Wave order (C1, C2, C3, …), at most four. Do not pad with unpublished templates. The `citizen_question` is the only link, to that slice path. The bound one-liner is `fact_lede_one_line` — the first sentence of that slice's plain-text fact-lede — and is not a link. Each card carries `data-vintage-id` from **that slice's** catalog entry; `<html data-vintage-id>` stays the tree vintage. The slice `<title>`, `meta description`, and `QAPage` `acceptedAnswer` keep the full `fact_lede`. This is the only slice list on home. Do not also emit a home `.hottest-rail`

Do not repeat the five sleeve hubs in `main`. Header and footer already list them. A hub with no catalog slice still stays in that chrome (quiet empty, no invented figures). `.hottest-rail` stays a **slice** region (in-page hashes and catalog siblings), not a second home index. `.sleeve-index` stays a **hub** (and house) list of slices, not a third copy of the sleeve nav.

**Sleeve hub.** Hub H1, then each catalog slice in that sleeve as its citizen question. The optional one-line bound fact is `fact_lede_one_line`. Each `.sleeve-index` card carries `data-vintage-id` from that slice's catalog entry. Canonical of every number remains the slice URL.

**Footer.** Five header sleeve links, `/how-this-works`, `/sources`. No engagement SDK. No party or ministry campaign strip.

**House body.** Content Editor. Until that copy exists, UI/UX ships the route with the house H1 from the title formula, links to `/` and sleeves, and **no figures**. Do not invent a producer bibliography.

**Interaction.** Static HTML. Allowed: skip link to `main`, in-page `<details>`, hash links, Vega-Lite hover/download from already-bound specs. Forbidden: request-time producer fetch, live vintage switch, A/B, heatmap, client search.

**Preview chrome** is **serving**, not in the render tree. The preview host may inject a banner (`Preview · not published` plus `vintage_id` in IBM Plex Mono). Citizen HTML must not contain that banner. A leaked preview URL still sends `X-Robots-Tag: noindex, nofollow`.

**404.** Quiet sentence, links to `/` and sleeves, `noindex`. Do not invent a number to fill the page.

---

## Web layout design

Slice layout (hero, stat row, `--desk` column, chart wells) is [design-system.md](../design-system.md). This file only adds **site** frame:

| Region | Width | Notes |
|--------|-------|--------|
| Header / footer | `--desk` | Same column as the article; left-aligned; not a full-bleed marketing bar |
| Main | `--desk` | Home, hub, slice, and house pages share it |
| Sleeve nav | wrap | Text links, `--mark` + underline; 44px hit height |
| Preview banner | full viewport | Serving-only; `--card` on `--paper`; never on citizen |

Home, hub, and house pages use the same tokens (`--paper`, `--card`, `--ink`, `--muted`, `--mark`). They do not get a second palette or a larger marketing type scale. H1 on a slice remains the citizen question; H1 on home is the desk line, not a billboard.

Do not add a mega-menu, tabbed dashboard, or map that ranks states by default.

---

## SEO strategy and content

**Intent.** Kitchen-table questions official statistics can answer: prices, jobs, tax, school, hospital, ration — [topic-charters.md](../next/topic-charters.md) “How a topic got on this list” and the search-spike table. We do not chase news, bills of the week, exam portals, or filing how-tos.

**One question, one indexable URL.** The slice is the unit of search. Sub-questions stay on that URL. Sleeve hubs are indexes, not duplicates of the explainer. Fast facts on home quote published slots and link to the slice — they do not become a second canonical.

**Index only citizen-view.** Crawlers may see the citizen prefix. They must not see preview, signed URLs, or `/archive/{vintage_id}`.

**Stable title, bound snippet.** The citizen question (H1 / `<title>`) stays put across vintages. The meta description is the rendered fact-lede (number, unit, place, year, then definition). Refresh updates the snippet; it does not require a new slug.

**Cites are the trust signal.** Producer, series, date, geography vintage, caveat stay in the same view as the number. Do not write meta that a slot cannot support. Do not put `vintage_id`, annex codes, or `2024=100` in titles or descriptions ([editorial-guidelines.md](../editorial-guidelines.md)).

**Do not** keyword-stuff (“latest India inflation rate 2026 CPI food”); use judging words in titles; ship doorway state pages; `rel=canonical` from preview to live when the vintage differs; mark Prism as the statistical office in JSON-LD.

**`robots.txt` (citizen prefix only, not in the shared tree).**

```text
User-agent: *
Allow: /
Disallow: /archive/

Sitemap: {CITIZEN_ORIGIN}/sitemap.xml
```

Preview prefix: `Disallow: /` plus HTTP `X-Robots-Tag: noindex, nofollow`. Do not advertise a sitemap there.

**`sitemap.xml`.** Generated for the **citizen** pointer only (serve artifact, not this wave until a second slice is ready to publish): home, five sleeve hubs, catalog slices (and geography routes once they exist), house pages. Omit preview, omit `/archive/`, omit hashes, omit templates that did not bind, omit `/_astro/`, omit Vega JSON.

**Structured data** (bound text only; absolute `url` fields at citizen serve):

- Home: `WebSite` (`name`: Prism, `url`: `{CITIZEN_ORIGIN}`). No `SearchAction` (there is no search).
- Hub / slice: `BreadcrumbList`.
- Slice: `QAPage` whose `Question.name` is the citizen question and `acceptedAnswer.text` is the bound fact-lede. One answer. No “what this means.”

Do not emit `FAQPage` that repeats every section heading as a fake Q&A. Do not emit `Organization` as if Prism were MoSPI / RBI / Census.

---

## Page titles and meta

`{CITIZEN_ORIGIN}` is the public citizen host Platform sets at **serve**. It is not baked into shared or preview HTML.

| Page | `<title>` | `meta name="description"` |
|------|-----------|---------------------------|
| Home | `Prism — official numbers on India` | First sentence of [vision.md](../vision.md), truncated to ~160 characters |
| Sleeve hub | `{Hub H1} — official record · Prism` | “Official statistics on {Hub H1}, from the producing agencies.” No figures unless slotted |
| Slice | `{citizen_question}` | Plain-text fact-lede after bind. Fail render if the lede is empty while the H1 shows |
| Geography slice | `{citizen_question}` with the unit already in the words | Same rule; geography is in the question, not a suffix `\| Kerala` |
| House | `How this works · Prism` / `Sources · Prism` | One sentence, no figures unless slotted |
| 404 | `Page not found · Prism` | — |
| Retained | same as the slice title | same description as **that** vintage; see robots below |

**Shared HTML (every page).** Origin-agnostic. Path and type on the root element so serve can inject origin-bearing tags:

```html
<html lang="en" data-prism-path="/prices/retail-prices" data-prism-page="slice">
```

| `data-prism-page` | `data-prism-path` |
|-------------------|-------------------|
| `home` | `/` |
| `sleeve` | `/prices` (hub) |
| `slice` | `/prices/retail-prices` |
| `house` | `/how-this-works` or `/sources` |
| `notfound` | omit path |

Shared HTML includes `<title>`, description, `og:title`, `og:description`, `og:type`, `og:site_name`, `twitter:card`. It **omits** `<link rel="canonical">`, `og:url`, absolute JSON-LD `url` / `item` fields, and `<meta name="robots">` except 404 (`noindex`).

**Head contract (slice) after citizen serve:**

```html
<title>{citizen_question}</title>
<meta name="description" content="{bound fact-lede}" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<link rel="canonical" href="{CITIZEN_ORIGIN}{path}" />  <!-- citizen serve only -->
<meta property="og:title" content="{citizen_question}" />
<meta property="og:description" content="{bound fact-lede}" />
<meta property="og:type" content="website" />
<meta property="og:url" content="{CITIZEN_ORIGIN}{path}" />
<meta property="og:site_name" content="Prism" />
<meta name="twitter:card" content="summary" />
```

- `lang="en"` until a template ships another language ([design-system.md](../design-system.md)).
- No `og:image` until a named render of a bound chart PNG exists. Do not invent a marketing card.
- Visited links stay `--mark` (this is a record, not lore).
- Do not put `vintage_id` in `<title>`, description, or OG. Data vintage stays on the collapsed citation card.
- `article:published_time` is out (not a newsroom). Byline already shows release date (`Asia/Kolkata`) and next named release.

**Robots meta vs headers.** The two prefixes differ at **serve**:

| Prefix | HTML | HTTP | Canonical |
|--------|------|------|-----------|
| Citizen | title, description, OG, JSON-LD; inject absolute URLs from `data-prism-path` | none required on indexable pages | `{CITIZEN_ORIGIN}{path}` added at serve |
| Preview | same shared body; do not inject canonical or origin | `X-Robots-Tag: noindex, nofollow`; `Cache-Control: private, no-store` | omit (do not point a newer vintage at live numbers) |
| `/archive/{vintage_id}` | that vintage’s title/description | `X-Robots-Tag: noindex, nofollow` | `{CITIZEN_ORIGIN}{live path}` (the current slice, not the archive URL) |
| 404 | `<meta name="robots" content="noindex">` in shared HTML | optional `X-Robots-Tag: noindex` | omit |

A citizen route cannot read a non-published vintage. Preview never aliases `data/pointers/citizen`.

---

## Published vs preview

Two CMS modes. Same relative paths. Different pointer, different prefix, different catalog.

```text
data/renders/{vintage_id}/          complete tree for that pointer; not public by itself
data/pointers/preview               preview desk (cms_mode=preview)
data/pointers/citizen               published desk (cms_mode=citizen)
```

```text
Citizen GET  /prices/retail-prices
        → read citizen pointer → serve that tree’s matching file
        → inject canonical / og:url / JSON-LD origin
        → unpublished slice paths 404

Preview GET  {private prefix}/prices/retail-prices
        → read preview pointer → serve that tree’s matching file
        → X-Robots-Tag: noindex, nofollow
        → optional preview banner (serving chrome)
```

| | Preview | Published (citizen-view) |
|--|---------|---------------------------|
| Pointer | `data/pointers/preview` | `data/pointers/citizen` |
| Catalog | Every bound slice (C1–C3 when each can bind) | Slices on the citizen vintage only |
| Who | Editors, Trust, Charter | Citizens |
| Host | Private bucket / signed URL / local preview server | Public origin |
| Isolation | Different prefix + auth/`noindex`. A second *public* URL is not isolation | World-readable |
| Indexing | Disallow all; no sitemap | `Allow: /`; sitemap of live routes (when generated) |
| Banner | Serving chrome only | None |
| Flip | After a complete preview render; must not equal citizen in the same pass | Last step; nine tests pass; `COMPLETE` marker |
| On fail | Keep previous preview or none | Keep previous citizen vintage |
| Retained | Not preview | Prior citizen vintages at `/archive/{vintage_id}` |

Local preview today: `prism.preview_server` serves the preview tree with `PREVIEW_HEADERS` in `src/prism/serving.py`. Do not weaken those headers. Teach it the slashless → `index.html` map when the tree is nested.

**Tests this surface must keep.** Blueprint test 5: a citizen route cannot read a non-published vintage; preview is not world-readable. Test 4: do not move `citizen_pointer` if a required template failed. Test 6: one **page**, one `vintage_id` (the preview desk may hold several pages). After this tree ships, the required C1 file is `prices/retail-prices/index.html`, not root `index.html`.

---

## Template front matter

Front-end Architect sets `slug` (and the sleeve → path map). Content Editor already sets `template_id`, `sleeve`, `citizen_question`. UI/UX Developer fails the render if they disagree with this file. Do not pick a new slug in a UI/UX pass.

C1:

```yaml
template_id: c1-prices-people-pay
charter: C1
sleeve: prices-and-production
slug: retail-prices
citizen_question: How fast are retail prices rising in India, including food?
```

C3 (declared now; listed in the catalog only after this vintage binds it):

```yaml
template_id: c3-union-money
charter: C3
sleeve: money
slug: union
citizen_question: What does the Union collect, and what does it spend it on?
```

C2, when Content Editor adds the template: `sleeve: people`, `slug: population`, path `/people/population`.

---

## Out of scope

Visual tokens, chart form factor, presentation pass ([design-system.md](../design-system.md), UI/UX Developer). Tone ([design-philosophy.md](../design-philosophy.md)). Voice and scan path ([editorial-guidelines.md](../editorial-guidelines.md)). Pointer atomicity and `CITIZEN_ORIGIN` as infrastructure ([architectural-blueprint.md](../architectural-blueprint.md)). Dark mode, a mobile app, ISR, request-time fetch, engagement SDK.

---

## Next

```text
page_type:       home | sleeve | slice | house | notfound
path:            / · /{sleeve} · /{sleeve}/{slice} · /how-this-works · /sources
slug:            C1 retail-prices; C3 union; C2 population when the template exists
indexable:       citizen (home, hubs, catalog slices, house) · noindex-preview · 404 noindex
title_source:    vision purpose (home) · Hub H1 formula · citizen_question · house formula
next_persona:    ui-ux-developer
web_design:      docs/web-design.md
```

**UI/UX Developer** implements, without inventing a slug or a second public URL:

1. `SiteShell` on every page (skip link, lockup → `/`, five sleeve links, footer).
2. Astro files in [CMS tree](#cms-tree-one-vintage--one-site): `/` is desk home; C1 at `/prices/retail-prices`; five hubs; house routes; 404.
3. Bound `site.json`; `<title>` / description from this file; `data-prism-path` / `data-prism-page` on `<html>`.
4. On-disk directory `index.html` as specified. Do not leave C1 at `/`.

Do not implement geography routes, sitemap, `robots.txt` in the tree, or archive paths until a second slice is ready to publish. Do not paint the desk to resemble USAFacts.

**Platform Architect:** slashless URL → `{path}/index.html`; citizen-serve injection of canonical / `og:url` / JSON-LD origin from `data-prism-path`; COMPLETE required files include `prices/retail-prices/index.html` for C1; preview server must not weaken `PREVIEW_HEADERS`.

**Content Editor:** house body for `/how-this-works` and `/sources` (no figures unless slotted). Do not change C1/C3 citizen questions. C2 uses `slug: population` when that template is written.
