# Web app execution plan

Front-end Architect. Remaining work to turn the civic CMS from a correct tree into a citizen-grade desk. Standing contract: [web-design.md](../web-design.md) — this plan does not replace it. Look is [design-system.md](../design-system.md) (UI/UX Developer). Copy is [editorial-guidelines.md](../editorial-guidelines.md) (Content Editor). Pointers, origin, and serve headers are [architectural-blueprint.md](../architectural-blueprint.md) (Platform Architect). Ship or block is Charter and Trust.

Three words, once. A **sleeve** is one of the five topic families (People, Work, Money, Prices, Delivery) and the first segment of a URL. A **slice** is one citizen question on one stable URL inside a sleeve. A **vintage** is one dated snapshot of observations, citations, and caveats; a page binds to exactly one.

## Verdict

The route layer is done. The desk is not.

Everything `web-design.md` asked for structurally now exists on the preview tree checked at `localhost:4321` on 2026-09-19: `/` is the desk home with the Purpose sentence as H1, C1 sits at `/prices/retail-prices`, C2 at `/people/population`, C3 at `/money/union`, all five sleeve hubs answer 200, both house pages and the 404 are in place, one shared `SiteShell` carries the skip link, lockup, sleeve nav, breadcrumb and footer, `site.json` is the only list of live pages, titles come from the citizen question or a house formula, shared HTML omits canonical and `og:url`, and both servers map a slashless path to `index.html` and 301 a trailing slash away. Preview sends `X-Robots-Tag: noindex, nofollow` and `Cache-Control: private, no-store` on every page.

What is left is not more routes. It is four things: the slice pages do not point at each other, the 404 is a dead end, the home and hub cards paste a whole paragraph where the contract asks for a one-liner, and the first screen of a slice shows big numbers before it shows who published them. None of those need a new URL, a new slug, or a second public host. Three of the four are handoffs to UI/UX Developer and Content Editor with the rule already written down here.

No new slugs are minted in this plan. C4–C8 paths are already declared in the contract and are not needed to finish this wave.

## How the IA serves the vision — and where it does not

The Purpose sentence in [vision.md](../vision.md) is "a shared, checkable picture of India that does not belong to a party, a ministry, or a news cycle." Four properties of the current IA carry that:

- **One question, one URL.** A citizen who is sent `/prices/retail-prices` sees the same question, the same H1, and the same `<title>` next month with new numbers. Nothing in the path names a party, a ministry, a charter id, or a vintage. Sub-questions stay hashes on that page, so there is no second canonical competing for the same answer.
- **The catalog is the site.** Home, hubs, footer and `/sources` all read `site.json`, so an unbindable template is silently absent rather than a dead link. A citizen cannot reach a page that this vintage could not fill.
- **Preview is not a second public address.** Isolation is the prefix plus headers, not a `/preview` segment. A leaked preview URL still tells crawlers to stay away, and the citizen pointer is never aliased.
- **Quiet empty is honest.** `/work` and `/delivery` return 200 with a heading and nothing else. The desk does not pretend to cover what it has not ingested.

Where the IA falls short of the vision today:

- **The desk does not feel shared yet, it feels like three unlinked pages.** A reader on C1 has no route to C2 or C3 except the header. The hottest-rail on each slice is in-page hashes only. The contract already says that rail is hashes *plus* catalog siblings; the templates never emit the siblings.
- **"Checkable" is below the fold.** Citation and caveat cards sit in a `.source-stack` at the bottom while three display figures lead. The design system requires cite chrome in the same view as the number. The numbers currently arrive before their provenance.
- **A wrong URL ends the visit.** The 404 body is an H1 and one link. Chrome carries the sleeves, but the page says nothing.

USAFacts is taken for **role**, not look. The role Prism keeps is the answer-page shape — question as H1, a bound fact-lede that actually answers it, evidence, then method — plus fast facts as bound one-liners and featured questions as rails. The live tree has that shape. The role Prism refuses stays refused, and this plan adds nothing from the other column: no `/answers/…/country/…` tree, no geography picker in the header, no search box, no newsletter field, no chat widget, no media desk, no "hottest topics" scoops, no magenta costume. The one place the live desk drifts toward their homepage is the fast-facts card pasting a full paragraph; the fix is to shorten it, not to restyle it.

## Replacement for "Now vs target" in `web-design.md`

The old table described a single-page build with C1 at `/`. That is no longer true. The table below has been written into [web-design.md](../web-design.md); nothing else in that file changed.

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
| Hottest-rail | In-page hashes only | Hashes **plus** catalog sibling slices |
| 404 body | H1 and a link to `/` | Quiet sentence, links to `/` and the five sleeves |

## Rulings

These settle the open questions so the next persona does not have to guess. Where a ruling should later become contract text in `web-design.md`, it is marked **fold-in**; that edit is a separate Front-end pass, not part of the implementation.

**R1 — Hottest-rail siblings are injected from the catalog, never typed into a template.** A slice's `.hottest-rail` renders its author-written in-page hashes first, in template order, then up to three sibling links taken from `site.json`. Siblings are catalog order (charter order, already how `cms_site.py` sorts), the current slice excluded, link text is the sibling's `citizen_question` verbatim. If the catalog has no sibling — the citizen desk today holds C1 only — the rail is hashes alone and no empty group, heading, or placeholder appears. `filter_hottest_rail` already drops any `href` that is not a hash or a catalog path; injection happens on the same pass so that invariant holds. No template gains a hardcoded question. **Fold-in.**

**R2 — The 404 gets a quiet sentence and the five sleeves in `main`.** One sentence, no figure, no apology, no search box, and no list of catalog questions (that would make the 404 a second index). Links: `/` and the five sleeve hubs, read from `site.json` sleeves. The page keeps `data-prism-page="notfound"`, keeps `<meta name="robots" content="noindex">`, and keeps no `data-prism-path` so citizen serve never injects a canonical for it. Repeating the sleeve links inside `main` is allowed **here only** — home still must not.

**R3 — Fast facts and hub cards use the first sentence of the bound lede.** The contract says a bound one-liner; the live cards paste the lede including its definition sentence. Rule: `site.json` slices carry a `fact_lede_one_line` derived at bind as the first sentence of the plain-text fact-lede. Home `.fast-facts` and hub `.sleeve-index` use it; the slice `<title>`, `meta description`, and `QAPage` `acceptedAnswer` keep the full `fact_lede` unchanged. The one-liner is never a link — the `citizen_question` remains the only link on the card. Fail the render if the derived sentence is empty while the card shows. A Content-Editor-authored `fast_fact` in front matter is the later alternative; it is not this wave, because a second authored sentence is a second claim to check. **Fold-in.**

**R4 — Home and hub cards carry the vintage of the slice they quote, not the tree.** On the preview desk, home shows C1, C2 and C3 cards while `<html data-vintage-id>` is the tree vintage. That reads as one vintage covering three differently dated facts. Each `.fast-facts` and `.sleeve-index` card gets `data-vintage-id` from its own catalog entry, which `site.json` already stores per slice. The root attribute stays as the tree vintage. Blueprint test 6 (one page, one `vintage_id`) is about bound pages; home and hubs are catalog indexes and must say which snapshot each quoted fact came from. **Fold-in.**

**R5 — The preview banner stays optional and stays at serve.** Isolation is already carried by the headers, so the banner does not block anything. When Platform adds it: injected by `preview_server` into HTML responses only, text `Preview · not published` plus the tree `vintage_id` in IBM Plex Mono, no link and no control inside it so the skip link remains the first focusable element, and never emitted by `citizen_server` or written into the render tree. A test asserts the citizen response body does not contain the banner marker.

**R6 — `robots.txt` before sitemap; both only when a public citizen origin exists.** Not this wave. The citizen pointer still holds C1 alone and there is no public host. When a second slice is ready to publish, Platform serves `robots.txt` from the citizen prefix as written in the contract, and adds the `Sitemap:` line only once `sitemap.xml` exists — do not advertise a sitemap that 404s. Preview serves `Disallow: /` and never a sitemap. Nothing about robots or sitemap goes into the render tree.

**R7 — Cite chrome moves up the page; it does not get a URL.** Fixing the scan path is a UI/UX and Content Editor job against the design system. The Front-end constraints on that work: no per-slice `/sources` route, no `#sources` fragment promoted as the citation home, `/sources` stays a house index of catalog questions and does not become a cite dump, and the compact first-screen byline must not remove the full cards from the page — a crawler and a citizen must both still find producer, series, period and release date on the same URL as the number.

**R8 — Number grouping is one convention, chosen once, applied at bind.** `1210854977` and `5347314.81` are unreadable and overflow the `--desk` stat cells. This persona does not pick Indian versus Western grouping. What is fixed here: whichever convention is chosen is applied at bind, so the figure in the fact-lede, the stat cell, and the `meta description` are identical strings — the description is the plain-text lede and ends up in search results. No `vintage_id`, annex code, or `2024=100` enters the head. UI/UX owns the cell overflow (`tabular-nums` is already in `desk.css`); Content Editor and bind own the convention.

**R9 — Empty hubs stay empty and are not advertised.** `/work` and `/delivery` return 200 with the hub H1. Do not 301 them, do not 404 them, do not drop them from header or footer, and above all do not list C4 or C8 as "coming soon" — that advertises a URL that does not resolve. Content Editor may add one sentence with no figure in it saying the sleeve has no published question yet. That is a copy decision, not a route.

**R10 — `how-this-is-measured` renders as a section, not a comment.** `LAYOUT_BLOCKS` in `template_bind.py` maps the token to `<section class="how-measured">` and `desk.css` styles that class, but the templates carry it as an HTML comment and the live pages had no such section. That is a bind and template fix, not a route. No `/how-it-is-measured` page exists or is wanted; method stays on the slice.

**R11 — Not Front-end.** The C2 "not printed" byline is a citation and copy question for Content Editor and the Methodologist. `.analysis-byline` is allowed chrome that Content Editor names and UI/UX styles; it is not required to ship this wave and it never replaces the producer cite.

## Phases

Each item names one owner persona. Nothing here waits on C4–C8 templates, and nothing here publishes C2 or C3 — moving the citizen pointer is Charter and Trust.

### Phase 0 — Contract (Front-end Architect)

1. Replace the stale "Now vs target" table in `web-design.md`. **Done in this pass.**
2. Fold R1, R3, and R4 into `web-design.md` as contract text — one edit to the hottest-rail paragraph, one to the `site.json` field list, one to the desk-home section. Do this before or alongside Phase 1 so UI/UX implements against the file, not against this plan.

Acceptance: `web-design.md` describes the tree that exists, plus the rail, the one-liner, and the per-card vintage. No second IA memo survives.

### Phase 1 — Make the desk a desk (UI/UX Developer, with one Content Editor line)

3. **Hottest-rail siblings** per R1, injected in `src/prism/cms_site.py` alongside `filter_hottest_rail` and consumed unchanged by the slice route. *(UI/UX Developer)*
4. **404 body** per R2: sentence plus `/` plus five sleeve links. The sentence is one line of copy. *(Content Editor writes the sentence; UI/UX Developer implements the page)*
5. **Fast-facts and hub one-liner** per R3, plus per-card `data-vintage-id` per R4. *(UI/UX Developer)*
6. **`how-measured` section** per R10. *(UI/UX Developer)*

Acceptance: on the preview desk, C1 links to C2 and C3 by their citizen questions and to nothing outside the catalog; the citizen desk's C1 rail shows hashes only with no empty group; home and hub cards show one sentence each and name their own vintage; an unknown path returns a 404 that explains itself and offers five sleeves; a rendered slice contains `<section class="how-measured">`. No new path, slug, `<title>`, or `data-prism-page` value appears anywhere.

### Phase 2 — Make the first screen checkable (UI/UX Developer + Content Editor)

7. **Presentation pass on the first screen** against the design system scan path, within the R7 constraints: compact source byline beside the numbers, full cards still on the page. *(UI/UX Developer)*
8. **Figure grouping and stat-cell fit** per R8. *(Content Editor and bind choose the convention; UI/UX Developer fixes the cells)*
9. **Optional `.analysis-byline` and the C2 "not printed" byline wording** per R11. Not blocking. *(Content Editor, then UI/UX Developer)*

Acceptance: every figure above the fold has producer, series, reference period and release date in the same view; no stat cell overflows at `--desk` on a 360px viewport; the `meta description` string matches the on-page lede character for character.

### Phase 3 — Serving polish (Platform Architect)

10. **Preview banner** per R5 — optional, do not block the wave.
11. **Citizen serve rehearsal:** run `prism serve --origin …` against the citizen pointer and confirm canonical, `og:url`, and absolute JSON-LD `item` paths are injected, that 404 gets neither, and that no preview marker is present. The injection code already exists; this is a check, not a build.

Acceptance: preview HTML carries the banner and the citizen response does not; a citizen slice response has exactly one canonical and one `og:url`, both absolute on the configured origin.

### Phase 4 — Only when a second slice is ready to publish (Platform Architect, then Trust Auditor)

12. `robots.txt` on the citizen prefix, then `sitemap.xml`, in that order, per R6.
13. Archive paths, geography routes, and `og:image` remain unopened. They are named in the contract and are not this wave.

Acceptance: not evaluated until Charter opens a second publish.

### Gate — Trust Auditor

Before anything a citizen sees. Trust runs after Phase 1 and Phase 2 on the **preview** tree. Front-end evidence to hand over: no route, slug, or title changed; the rail emits only catalog paths and hashes; the 404 stays `noindex`; preview headers are unweakened; the citizen pointer was not touched by any item in this plan.

## Routes, titles, indexability

Complete surface. Nothing in this plan adds a row.

| Path | `data-prism-page` | `<title>` source | Indexable | Status |
|------|-------------------|------------------|-----------|--------|
| `/` | `home` | `Prism — official numbers on India` | citizen | Ships; cards change in Phase 1 |
| `/people` | `sleeve` | Hub H1 formula — `People — official record · Prism` | citizen | Ships |
| `/work` | `sleeve` | `Work — official record · Prism` | citizen | Ships, quiet empty |
| `/money` | `sleeve` | `Money — official record · Prism` | citizen | Ships |
| `/prices` | `sleeve` | `Prices and production — official record · Prism` | citizen | Ships |
| `/delivery` | `sleeve` | `Delivery — official record · Prism` | citizen | Ships, quiet empty |
| `/prices/retail-prices` | `slice` | `citizen_question` (C1) | citizen | Ships; published vintage |
| `/people/population` | `slice` | `citizen_question` (C2) | noindex-preview | Preview only; Charter owns publish |
| `/money/union` | `slice` | `citizen_question` (C3) | noindex-preview | Preview only; Charter owns publish |
| `/how-this-works` | `house` | `How this works · Prism` | citizen | Ships |
| `/sources` | `house` | `Sources · Prism` | citizen | Ships |
| unknown | `notfound` | `Page not found · Prism` | noindex | Body changes in Phase 1 |
| `/work/labour`, `/money/states`, `/people/school`, `/people/health`, `/delivery/food-and-farm` | `slice` | `citizen_question` | later | Slugs already declared; no template yet |

Every citizen path above is served from the tree at the citizen pointer, with canonical and `og:url` injected at serve from `data-prism-path`. Every preview path is the same relative path on a private prefix with `noindex, nofollow`. There is no third address for any of them.

## Out of scope

Search or any client filter over the catalog. `/answers/` or any other question-tree prefix. Geography routes and geography pickers. `/archive/{vintage_id}`. Sitemap and `robots.txt` this wave. Newsletter, subscribe, chat, "Ask the data", social row, press kit, download hub, most-viewed. A newsroom or article desk. Magenta, cream, Aeonik, a wordmark beyond the text lockup, or any other part of the USAFacts costume. ISR, Next.js, request-time producer fetch, engagement SDK. Tokens, type scale, chart chrome, and the presentation pass itself — those are UI/UX Developer against `design-system.md`. Citizen questions, fact-ledes, and house copy — Content Editor. Pointer flips and `CITIZEN_ORIGIN` — Platform Architect. Ship or block — Charter and Trust.

## Suggested order

Phase 0 item 2, then Phase 1 in the order 3, 5, 4, 6, then Trust on preview, then Phase 2, then Trust again, then Phase 3. Phase 4 waits for Charter.

Item 3 is first in Phase 1 because the rail is the one gap that changes how the desk reads as a whole; item 5 is next because it is the same `site.json` pass; the 404 and the `how-measured` section are independent and can run in parallel with either. Phase 2 is deliberately after the rail, because moving cite chrome up the first screen is a presentation pass and should be run once, against a page whose structure has stopped moving. Nothing in Phases 0–3 requires a C4–C8 template to exist, and nothing in them moves `data/pointers/citizen`.

```text
page_type:       home | sleeve | slice | house | notfound
path:            / · /people · /work · /money · /prices · /delivery · /prices/retail-prices · /people/population · /money/union · /how-this-works · /sources
slug:            C1 retail-prices · C2 population · C3 union (no new slug in this plan)
indexable:       citizen (home, five hubs, house, C1) · noindex-preview (C2, C3) · noindex (404)
title_source:    vision purpose (home) · Hub H1 formula · citizen_question · house formula
next_persona:    ui-ux-developer
web_design:      docs/web-design.md
```
