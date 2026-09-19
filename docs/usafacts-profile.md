# USAFacts live profile

Observation of [usafacts.org](https://usafacts.org/) on **2026-09-17**. What the site is, in their words and on the pages checked. **Not a Prism contract.** Contrast with Prism only at the end.

```text
check:     2026-09-17, live pages
org:       not-for-profit, nonpartisan civic initiative (not a 501(c)(3))
founder:   Steve Ballmer (2017); privately funded by him
shape:     question → magenta fact-lede → stats/charts → method/sources
```

## What it is

USAFacts is a **not-for-profit, nonpartisan civic initiative** that makes US government data easier to access and understand. About: “We turn public data into public knowledge” / “USAFacts exists to make government data easier to access and understand.” FAQ: “USAFacts is a not-for-profit, nonpartisan civic initiative making government data easy for all Americans to access and understand.” ([about-usafacts](https://usafacts.org/about-usafacts/)). Homepage H1: “Free unbiased public data for everyone.” ([home](https://usafacts.org/)).

Founder, as they tell it: “When former Microsoft CEO Steve Ballmer retired, he wanted to know how the government spends our tax dollars. … So, in 2017, he built USAFacts.” Leadership listed on About: Ballmer (Founder), Lauren Woodman (President), Megan Winfield (CTO), Richard Coffin (Chief of Advocacy and Research), Kari D'Elia (CPO). Their [AI info](https://usafacts.org/ai-info-page/) page adds founded **24 April 2017**, headquarters **Bellevue, WA**.

Funding FAQ: privately funded by Ballmer; no external donors; **not a 501(c)(3)** and no tax exemption under revenue tax laws; no advertising; free, “No paywalls, period.” ([about-usafacts](https://usafacts.org/about-usafacts/)).

## Who it is for

They say **all Americans** / everyone. In practice the site also pitches:

- **Citizens and voters** — answer pages, topic hubs, state pages such as [Maine](https://usafacts.org/me/) (“whether you’re a Mainer deciding how to vote”).
- **Congress and policy staff** — “Data Skills for Congress,” America in Facts, [government-and-policy](https://usafacts.org/government-and-policy/).
- **Journalists** — [press-partners](https://usafacts.org/press-partners/): “Free, citable government data, ready for your next story.” Creative Commons; cite USAFacts.
- **Teachers** — [Crash Course](https://usafacts.org/crash-course/) classroom materials.
- **Technologists / AI products** — [AI and tech](https://usafacts.org/ai-and-tech/), MCP beta, connectors.

## What they publish

| Product | Live URL | Notes |
|---------|----------|--------|
| Answer pages | `/answers/…` (no index) | Citizen questions; see below |
| Articles | `/articles/…` | Hub **`/articles/` 301 →** [guides-and-reports](https://usafacts.org/guides-and-reports/) |
| Data guides | e.g. [housing affordability](https://usafacts.org/guides/housing-affordability/) | Hub [guides-and-reports](https://usafacts.org/guides-and-reports/): “Data guides break down a curated set of government data…” Individual `/guides/` pages 200; **`/guides/` index 404** |
| Reports | [research reports](https://usafacts.org/research-and-initiatives/reports/) | **2026 Government 10-K** still live ([government-10-k](https://usafacts.org/government-10-k/)); State of the Union in Numbers; America in Facts; State of the Facts (polling) |
| Just the Facts | [just-the-facts](https://usafacts.org/just-the-facts/) | Video/explainer hub (Ballmer and others). **`/the-facts/` 404** |
| The Viz Lab | [the-viz-lab](https://usafacts.org/the-viz-lab/) | Experimental charts. **`/labs/` 404** |
| Analyst Notes | [analyst-notes](https://usafacts.org/analyst-notes/) | Behind-the-scenes notes |
| Newsletter | forms on many pages | “unbiased, data-driven insights” weekly. **`/newsletter/` 404** |
| Ask the data | site-wide chat widget | “We use AI to summarize the data, charts, and analysis we have on USAFacts.” **`/ask-the-data/` 404** |
| Download | chart **download** buttons on answers | No public `/download/` hub (404) |
| Data / MCP | [mcp](https://usafacts.org/mcp/), [data-sources](https://usafacts.org/data-sources/) | MCP beta: live server, no API key |

Topic browse (footer): Crime, Defense & security, Economy, Education, Environment, Government, Immigration, Health, Population. Also Crash Course, Research and initiatives, Government and policy, Press and media → [press-partners](https://usafacts.org/press-partners/).

## How an answer page is built

`https://usafacts.org/answers/` is **404**. Deep answers are live. Markup: `builder-model="answer-page"`. Shape on the pages checked:

1. **Question** as H1 (geography picker, e.g. “US”).
2. **Highlighted fact-lede** — magenta `<span class="answer">` (JSON-LD uses `class='answer'`). Repeated as FAQPage / QAPage `acceptedAnswer`. Then giant display figures.
3. **Evidence** — charts, maps, sub-questions, related articles.
4. **Methodology / sources** — “USAFacts standardizes data, in areas such as time and demographics…”. Source panels: agency + “Additional Contributors: **Data analysis and processing by USAFacts**.” Accordion: “Our approach to AI for this analysis.”

Checked ledes:

| Page | Highlighted answer |
|------|--------------------|
| [Jobs](https://usafacts.org/answers/how-many-jobs-were-added-in-the-us-last-month/country/united-states/) | “In August 2026, about 162,000 jobs were gained.” |
| [Crime](https://usafacts.org/answers/what-is-the-crime-rate-in-the-us/country/united-states/) | “In 2024, for every 100,000 people, the violent crime rate was 359 and the property crime rate was 1,760.” Then **359** / **1,760** |
| [Inflation](https://usafacts.org/answers/what-is-the-current-inflation-rate/country/united-states/) | “The inflation rate was 3.4%, as of August 2026.” |

## Voice and stance

**Claim.** About: “We don’t tell you what to think. We give you what you need to make informed decisions.” Politics FAQ (About and [our-data](https://usafacts.org/our-data/)): “Neither. USAFacts is nonpartisan; our data comes exclusively from government sources, and our analysis is reliable and credible by design.” Homepage articles rail: “We break down complex issues using real data, not opinions.” Newsletter: “No spin, just the facts.” They cite Ad Fontes (May 2026 chart: highest reliability, lowest bias — their wording).

They do **not** use the slogan “no opinion.” Closest: “A stat without context is no better than an opinion.” ([about](https://usafacts.org/about-usafacts/)). [our-data](https://usafacts.org/our-data/): “Supporting and trusting government data does not equate to supporting polices of an administration.” (their spelling).

**Practice.** Nonpartisan as *no party-as-cause copy* on the pages checked. They still rank places, highlight a thesis sentence, interpret (“insights,” “Now what?”), and advocate for public data (homepage open letter to Congress; Coffin’s title is advocacy). Press page: “sharp analysis, and compelling narratives.” Viz Lab: charts that make “the takeaway hard to miss.”

## Data practice

- **Government sources only** (as they define it). About: hundreds of federal, state, and local databases. [our-data](https://usafacts.org/our-data/): “over 90 at last count.” [data-sources](https://usafacts.org/data-sources/): “over 70 at last count” — both pages live; they do not reconcile the count here.
- **Not think tanks / universities** as the record: “unlike information from think tanks or universities, which may carry viewpoints.” ([our-data](https://usafacts.org/our-data/), [ai-info](https://usafacts.org/ai-info-page/)).
- **Original analysis:** “Beyond republishing government figures directly, we conduct original analysis on select government sources…” ([our-data](https://usafacts.org/our-data/)). Answer bylines: “Data analysis and processing by USAFacts.”
- **Standardization** on answer pages (time, demographics).
- **AI (they say so):** human analysts “conduct data analysis, identify findings, and write them up”; AI fills state/region templates from pre-selected points and updates wording (“decreased” → “increased”); “All content is reviewed by USAFacts… before publication.” Site chat: “We use AI to summarize…” MCP and ChatGPT/Claude connectors on [AI and tech](https://usafacts.org/ai-and-tech/).
- They **advocate** when series disappear (Billion Dollar Disasters, Food Security Survey — [our-data](https://usafacts.org/our-data/) FAQ).

## Ranks, league tables, highlighted takeaway, verdicts

Not a rare flourish. Answer copy, numbered state lists, and article headlines.

**Ranks — yes**

1. Crime answer — “What state has the highest crime rate? What state has the lowest?” / “Among states, Alaska had the highest violent crime rate and New Mexico had the highest property crime rate.” ([crime answer](https://usafacts.org/answers/what-is-the-crime-rate-in-the-us/country/united-states/)). Related article: [Which states have the highest and lowest crime rates?](https://usafacts.org/articles/which-states-have-the-least-and-most-crime/).
2. Jobs answer — “Which states had the best and worst job growth in July 2026? Maryland led all states… The two lowest-performing supersectors…” ([jobs answer](https://usafacts.org/answers/how-many-jobs-were-added-in-the-us-last-month/country/united-states/)).
3. Income answer — “Massachusetts had the highest median household income and Mississippi had the lowest.” Numbered league: “1. Washington, DC $109,700 2. Massachusetts…” ([income answer](https://usafacts.org/answers/what-is-the-income-of-a-us-household/country/united-states/)).
4. Population answer — “Vermont ranked last, with a 0.29% decline.” ([population answer](https://usafacts.org/answers/is-the-population-growing-or-shrinking/country/united-states/)). Articles: “Of the top 10 most educated states…” ([most educated](https://usafacts.org/articles/which-states-are-the-most-educated/)); “Airlines ranked best to worst… The top five were:” ([airports and airlines](https://usafacts.org/articles/what-are-the-best-and-worst-airlines-for-on-time-performance/)).

Not seen on the pages fetched: “eighth-most,” “laggard,” “scorecard.”

**League tables / maps.** Crime answer: choropleth “Property and violent crimes per 100,000 people, 2024,” then “Crime rate per 100,000 people, by state (2024)” with Violent / Property toggles and **See all (51)** in measure order (Washington, DC → Alaska → New Mexico…), not A–Z. Income: numbered top ten. Maps are JS-drawn; SVG fills were not in the HTML snapshot, so **red–green performance colour was not confirmed**. Crime hero is teal with a magenta header rail, not a choropleth.

**Verdicts — sometimes**

- **(a) Policy / moral judgment.** Sparse as party-causal copy. Present as performance nicknames and some advocacy. Air quality lede: “The average air quality in Arizona is considered unhealthy, while Hawaii has the country’s best air quality.” ([best/worst air](https://usafacts.org/articles/which-states-have-the-best-and-worst-air-quality/)). Jobs: “lowest-performing supersectors,” “best and worst job growth.” Teen article title: “The CDC says teen mental health is in crisis…” ([teen article](https://usafacts.org/articles/the-cdc-says-teen-mental-health-is-in-crisis-who-is-most-at-risk/)) — nickname attributed to CDC. Homepage open letter: America’s data infrastructure is “outdated.” Phrase hunt on fetched HTML: no “impressive,” “thanks to,” “miracle.”
- **(b) “What this means.”** Exact string **not** on the pages downloaded. Closest: “America’s public data has a trust problem. Now what?” ([trust article](https://usafacts.org/articles/americas-data-has-a-trust-problem-now-what/)). About: they “turn the numbers into insights.”
- **(c) Highlighted answer as thesis.** **Yes.** Magenta `span.answer` is the product, not a sidebar.

## Look / chrome (product facts, not a design spec)

- Magenta top bar (`border-t-magenta-500`); magenta highlight on the fact-lede.
- Homepage **Featured**: “hottest topics”; **Fast facts** (one-line answers, same numbers as the jobs/inflation/crime answers).
- Cream/off-white hero fields on marketing pages; crime answer hero is dark teal.
- Site-wide **Ask the data** chat; search; newsletter fields.

## What it is not

- **Not a 501(c)(3)** and not donor-funded, on their FAQ.
- **Not a live newsroom URL.** `/newsroom/` is **404**. They still run an article desk, press partnerships, and “Trendlines behind the headlines.”
- **Not a reprint bureau.** They standardize, analyze, rank, highlight a takeaway, and write insights. A second producer of summaries sitting on government series — not the producing agency.
- **Labs is not `/labs/`.** Ask the Data is a widget; Viz Lab is `/the-viz-lab/`.

## Failed fetches / gaps (do not invent)

| URL | Result |
|-----|--------|
| https://usafacts.org/answers/ | 404 (no index; deep answers 200) |
| https://usafacts.org/guides/ | 404 (individual guides 200) |
| https://usafacts.org/labs/ | 404 (live: [the-viz-lab](https://usafacts.org/the-viz-lab/)) |
| https://usafacts.org/ask-the-data/ | 404 (widget only) |
| https://usafacts.org/about-our-data/ | 404 (footer label; live: [our-data](https://usafacts.org/our-data/)) |
| https://usafacts.org/newsroom/ | 404 |
| https://usafacts.org/the-facts/ | 404 (live: [just-the-facts](https://usafacts.org/just-the-facts/)) |
| https://usafacts.org/10k/ and `/10-k/` | 404 (live: [government-10-k](https://usafacts.org/government-10-k/)) |
| https://usafacts.org/press/ and `/press-and-media/` | 404 (live: [press-partners](https://usafacts.org/press-partners/)) |
| https://usafacts.org/answers/which-states-have-the-highest-and-lowest-crime-rates/ | 404 (that story is an **article**) |
| https://usafacts.org/newsletter/, `/download/`, `/team/`, `/leadership/` | 404 |

Agency count disagrees between [our-data](https://usafacts.org/our-data/) (90+) and [data-sources](https://usafacts.org/data-sources/) (70+). Map colour scale not confirmed from HTML.

## Date of check

**2026-09-17.** Live HTML + browser on homepage, About, our-data, guides-and-reports, Viz Lab, Crash Course, Analyst Notes, research/reports, 10-K, MCP, press-partners, AI pages, housing guide, and the answer/article URLs above.

## Gray zone vs Prism (contrast only)

Prism takes the **question → fact-lede → evidence → method** shape. It allows bound ranks, a house-highlighted fact-lede, fast-facts / featured-slice rails, and a named analysis byline — in Prism tokens, with the agency still the producer. USAFacts does the shape **and** those moves in magenta costume, often as a second producer of summaries.

| Prism (this contract) | USAFacts live |
|-----------------------|----------------|
| Bound rank of a published measure; no judging words; no red–green | Rank talk including best/worst; measure-sorted league tables |
| `.fact-lede` house highlight (`--mark` navy, `--card`, `--paper`) | Magenta `span.answer` + FAQPage |
| Fast facts as slot-bound one-liners; hottest rails as featured citizen questions | Homepage “hottest topics”; Fast facts; articles + Just the Facts |
| “Analysis by Prism” beside the producer cite; agency remains the producer | “Data analysis and processing by USAFacts”; original analysis / insights |
| Still out: magenta/cream/Aeonik look; partisan report card; newsroom scoops; “get notified”; invented figures | Media desk, insights, “Now what?” |

Gray zone: extrema of one series (“highest annual increase”) vs a 51-row league table; EPA “unhealthy” vs “best air quality”; technical “cost-burdened” vs a civic nickname.

**Bottom line.** USAFacts is a Ballmer-funded civic data publisher: answers, articles, guides, videos, a government 10-K, labs, and AI tooling, all on US government sources plus their own analysis. The gap with Prism is the look (magenta, cream plot, Aeonik, wordmark), newsroom-adjacent articles, and a partisan / government scorecard — not the existence of ranks, a highlighted lede, a facts rail, or a named analysis byline.
