# Design philosophy

UI/UX Developer. Tone and idea for the civic CMS. Visual contract: [design-system.md](design-system.md). Site IA: [web-design.md](web-design.md) (Front-end Architect). How the page **reads**: [editorial-guidelines.md](editorial-guidelines.md) (Content Editor).

```text
tone:           modern, welcoming, civic publisher, generous
idea:           an answer a person can say out loud, with the government's name on it
house:          H1–H7 below — positive identity, short forbid list
```

Tone is aligned with how [USAFacts](https://usafacts.org/) answers a question: modern, welcoming, civic publisher, generous. We adapt voice, thesis-first lede, fast facts, evidence payoff, scan path, and look into our house for India. We do not use their wordmark, brand colour, or licensed typeface. Copy and scan path stay in the editorial guidelines. Tokens and the presentation pass live in the design system. Routes and nav live in web design.

**Idea.** An answer a person can say out loud, with the government's name on it. Public data belongs to the public; it was not built for the public. The page does the decoder-ring work below the fold and hands back a spoken fact first. Trust is an unmissable bound answer with the producer next to it.

**Language.** Two voices. Serif — IBM Plex Serif — states the record: the citizen question and every bound figure. Sans runs the desk: labels, byline, nav, chart type. Three grounds: warm stone paper, white for evidence, and a cool **well** for the answer band — once per screen. Navy is the institutional accent; clay and slate are categorical chart colour, never costume. The well is the one generous elevated thing: thesis (with house accent on the answer clause), movement, what-it-is, figures, and cite. Evidence is flat and equal-weight; method is later.

## House rules (H1–H7)

These replace “not USAFacts costume” as the standing look/chrome contract.

- **H1 — Prism is its own publication.** Own text lockup, own tokens, own typefaces. We do not use another publisher's wordmark, brand colour, or licensed typeface — Aeonik and the USAFacts magenta stay out because they are *theirs*, not because the shape is theirs.
- **H2 — The answer is the loudest thing on the page, and it is a bound observation.** Display weight never lands on a slogan, a mission line, or a section title. The thesis answer clause may carry a house accent mark (warm/navy family — not magenta, not a link colour).
- **H3 — Colour never means better or worse.** No red–green, no podium palette, no party or ministry palette, no tricolour as brand or scale, no saffron/green as up/down. Series colour is categorical position.
- **H4 — A gap is visible and named.** The citizen phrase is **not published**, italic, same size and face as its sentence. A published zero must look and read differently from a gap.
- **H5 — The producer sits with the number, in view.** Cite strip on the first screen, full card on this page, complete list at the bottom. “Analysis by Prism” beside the producer, never instead.
- **H6 — No chrome that collects the reader.** No search (this wave), chat, newsletter, social row, “get notified”, A/B, heatmap, or engagement SDK.
- **H7 — No decoration the vintage did not earn.** No illustration that asserts a fact, no gradient that implies direction, no icon standing in for a number.

Still forbidden, independent of look: spin and judging words; a partisan report card; hidden holes; a missing or replaced producer cite; invented figures; forecasts and private polls as the record; picking a winner between two disagreeing official series.

## Guidelines

1. **The answer is the product.** Question → thesis → movement → what-it-is → figures → evidence → method. The bound thesis clause and the display figure are the first designed objects.
2. **Invitation, then depth.** Start at a glance. Context sits with the fact. Full cards and methodology are available, not first.
3. **Generous, not bureaucratic.** Space, scale contrast, product cards. No search, chat, newsletter, or “get notified.”
4. **Ownable and checkable.** One house on every slice. A cropped chart still shows title, unit, geography, source, and holes — and reads as Prism.
5. **One well.** Lede (three sentences), stats, cite, and the first chart share left and right edge. `--measure` is method prose, not a second template glued to the chart.

Do not hide a hole or a cite to look finished. Generous landing is required.
