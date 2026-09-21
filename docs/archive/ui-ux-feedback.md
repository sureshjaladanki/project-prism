# UI/UX feedback

Principal. Recorded 2026-09-20 against the 2026-09-19 pass: [ui-ux-change-plan.md](ui-ux-change-plan.md) and the then-current contract, now [design-system-v1.md](design-system-v1.md). This file is the direction note. The ruling now lives in [design-system.md](../design-system.md) (**v2**).

```text
about:          preview desk look vs the 2026-09-19 change plan
wanted:         modern, welcoming, eye-pleasing
got:            quiet, measurable, austere — reads boring and non-intuitive
layout:         prose at --measure 40rem, charts at --desk 68rem — looks misaligned
keeps:          Phase A fit and contrast (3.2px labels, bleeding stats, hole AA)
forbids:        USAFacts costume (magenta, cream plot, Aeonik, wordmark, search, chat)
status:         folded into design-system.md v2; v1 archived
next_persona:   ui-ux-developer (Phase E on the change plan)
```

## What was wanted

The desk should look **modern, welcoming, and eye-pleasing**. Not a ministry PDF. A citizen should want to stay on the first screen. Type, stats, and charts should read as one layout.

USAFacts is the *role* (question → fact-lede → evidence → method). It is not the look to copy. The wanted delta is craft and welcome **inside** house tokens — navy `--mark`, stone paper, IBM Plex — not a magenta `span.answer`.

## What the 2026-09-19 plan did

It optimized for **readable and checkable**, and treated “appealing” as a preference it would not put in the contract. Success was: no 3.2px chart type, no bleeding stats, hole contrast at AA, producer on the first screen, prose not 124 characters wide. Tone stayed “quiet, corporate, professional, minimal.” Radius 0, no shadow, no gradient. “Prettier than the record” is an explicit fail.

That is the wrong direction for this feedback. Boredom was accepted as the cost of not looking like USAFacts. The principal did not ask for that trade.

The plan did use [usafacts-profile.md](../usafacts-profile.md) only for **role vs costume**. It did not take homepage craft (short, prominent facts) as a welcome problem until home was already a mission sentence over whispered grey cards. Theme labels (`corporate, professional, minimal, modern`) live in `design-system.md` front matter; the plan did not recategorize the look as welcoming.

## Failures named by the principal

1. **Boring.** Quiet chrome plus unfinished fit reads sparse, not calm. One navy accent and square cards are not enough of a designed moment on the answer.
2. **Non-intuitive.** Cite as a collapsed strip, charts that scroll instead of fitting the well, home not allowed to lead with a large welcome line, holes as small grey italic. Record path, not a welcome path.
3. **Text and graphs different widths — looks misaligned.** The rewritten system caps running prose, fact-lede, byline, and source-line at `--measure` **40rem**, and keeps stats, charts, cards, header, and footer at `--desk` **68rem**. On a wide screen the text column is much narrower than the chart well. Left edges may match; the **right edge does not**. The plan called this a reading fix (`--measure` had been unused). It reads as two templates glued together.

## What to keep from that plan

Fit and contrast were real. Do not roll them back to make the page prettier:

- Chart type must not render under 12px effective size (live desk: **3.2px** on 360px).
- Stat figures must fit their cell (live desk: ten-digit count **58px** out of the card at 768px).
- `--hole` must clear **4.5:1** (live desk: **3.09:1**).
- Producer name on the first screen.

## Correction to apply

Do not implement Phase A harder. Reopen [design-system.md](../design-system.md) for a welcome ruling, then amend the change plan.

1. **One width on the first screen.** Lede, stats, cite strip, and charts share one column. Keep `--measure` only for long method prose, not for the hero. Shared left **and** right edge.
2. **Welcome is scan path, not costume.** Fact in `--ink`, real card grid, cite next to the number, charts that fill the same well. A designed landing on the bound answer using house tokens (`.fact-lede`, `--mark` navy) — still not magenta, cream, Aeonik, or a wordmark.
3. **Tone.** Modern and welcoming are success criteria, not adjectives that lose to “quiet.” Minimal still means no gradient, no scorecard, no engagement SDK. It does not mean the page may look unfinished or misaligned.

Out of scope here: routes, slugs, citizen copy, pointer flips, USAFacts costume, dark mode.

## Done when

Folded into [design-system.md](../design-system.md) (**v2**). Previous contract: [design-system-v1.md](design-system-v1.md). Implementation is [ui-ux-change-plan.md](ui-ux-change-plan.md) Phase E. This file stays the direction note; do not treat the 2026-09-19 plan as the last word on first-screen width or tone.
