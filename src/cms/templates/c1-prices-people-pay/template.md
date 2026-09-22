---
template_id: c1-prices-people-pay
charter: C1
sleeve: prices-and-production
slug: retail-prices
citizen_question: How fast are retail prices rising in India, including food?
slots: ./slots.yaml
---

{{hero}}
<!-- cite-view: first-screen. CMS must show producer (linked), series, reference period, release date (Asia/Kolkata), and caveat in this same view as the numbers. A tooltip is not enough. Fail the render if any required card is missing. -->

<p class="sleeve">Prices and production</p>

# How fast are retail prices rising in India, including food?

<p class="byline">Updated {{cite:cite-c1-cpi-general-base-2024-2026-08.release_date}} (Asia/Kolkata). Next named release {{cite:cite-c1-cpi-general-base-2024-2026-08.next_release}}.</p>

<div class="fact-lede">
<p><span class="thesis-mark">Retail prices were {{slot:all-india-combined-general-inflation-latest-p}} percent higher in {{period.latest_provisional.label}} than a year earlier.</span> Food was {{slot:all-india-combined-cfpi-inflation-latest-p}} percent higher.</p>
<p>A month earlier, in {{period.latest_final.label}}, the general rate was {{slot:all-india-combined-general-inflation-latest-f}} percent; food was {{slot:all-india-combined-cfpi-inflation-latest-f}} percent.</p>
<p>It is the change in the prices households actually pay, measured on the same basket of goods and services each month.</p>
</div>

{{stat-row}}
{{stat:all-india-combined-general-inflation-latest-p|General, Combined · %}}
{{stat:all-india-combined-cfpi-inflation-latest-p|Food, Combined · %}}
{{stat:all-india-rural-general-inflation-latest-p|General, Rural · %}}
{{stat:all-india-urban-general-inflation-latest-p|General, Urban · %}}
{{/stat-row}}

{{chart:general-beside-food}}

<p class="source-line">NSO / MoSPI · CPI (General) and food · {{period.latest_provisional.label}} · released {{cite:cite-c1-cpi-general-base-2024-2026-08.release_date}}</p>

<nav class="hottest-rail" aria-label="Further questions">
<a href="#food">Is food rising faster than everything else?</a>
<a href="#rate-over-time">When was it last this high?</a>
<a href="#states">Where are prices rising fastest?</a>
<a href="#rural-urban">How fast are rural and urban prices rising?</a>
<a href="#basket">What else in the basket is rising?</a>
</nav>
{{/hero}}

{{section}}
<h2 id="food">Is food rising faster than everything else?</h2>

In {{period.latest_provisional.label}}, food was {{slot:all-india-combined-cfpi-inflation-latest-p}} percent and the general rate was {{slot:all-india-combined-general-inflation-latest-p}} percent — All India Combined. Rural food was {{slot:all-india-rural-cfpi-inflation-latest-p}} percent; urban food was {{slot:all-india-urban-cfpi-inflation-latest-p}} percent.

{{chart:cfpi-beside-division-01}}

<p class="source-line">NSO / MoSPI · Consumer Food Price Index and Food and beverages · {{period.latest_provisional.label}}</p>
{{/section}}

{{section}}
<h2 id="rate-over-time">When was it last this high?</h2>

Year-on-year inflation for All India Combined over the published run on this page:

{{chart:all-india-linked-inflation-holes}}

<p class="source-line">NSO / MoSPI · CPI General inflation (All India)</p>
{{/section}}

{{section}}
<h2 id="states">Where are prices rising fastest?</h2>

In {{period.latest_provisional.label}}, CPI (General) Combined for each State and Union Territory — ordered by the published rate on this chart.

{{chart:state-ut-combined-inflation-latest}}

<p class="source-line">NSO / MoSPI · CPI (General) Combined · {{period.latest_provisional.label}}</p>
{{/section}}

{{section}}
<h2 id="rural-urban">How fast are rural and urban prices rising?</h2>

In {{period.latest_provisional.label}}, All India rural year-on-year inflation was {{slot:all-india-rural-general-inflation-latest-p}} percent; urban was {{slot:all-india-urban-general-inflation-latest-p}} percent.

{{stat-row}}
{{stat:all-india-rural-general-inflation-latest-p|Rural · %}}
{{stat:all-india-urban-general-inflation-latest-p|Urban · %}}
{{/stat-row}}

{{chart:all-india-sectors-inflation-latest}}

<p class="source-line">NSO / MoSPI · CPI (General) · {{period.latest_provisional.label}} · released {{cite:cite-c1-cpi-general-base-2024-2026-08.release_date}}</p>
{{/section}}

{{section}}
<h2 id="basket">What else in the basket is rising?</h2>

All India Combined, {{period.latest_provisional.label}} — published groups of the retail basket, in the order the producer prints them.

{{chart:all-india-division-inflation-latest}}

<p class="source-line">NSO / MoSPI · CPI groups · {{period.latest_provisional.label}}</p>
{{/section}}

<div class="source-stack">
<p class="source-stack-label">Sources on this page</p>
{{cite-block:general-latest}}
{{cite-block:food-latest}}
{{cite-block:general-final}}
{{cite-block:food-final}}
{{cite-block:linked-back-series}}
{{caveat-block:caveat-c1-cpi-general-base-2024}}
</div>

{{how-this-is-measured}}
## Methodology

<!-- cite-view: how-this-is-measured. Prose only. Do not bind an observation here — a number in this view would require a second copy of the citation cards. -->

CPI (General) is the headline retail price index of selected goods and services collected in sampled rural and urban markets. The Consumer Food Price Index is food only — not the wider Food and beverages division. Combined is a published sector (rural and urban together), not an average made here.

The index is on a 2024 base. Index points and year-on-year inflation (%) are separate observations. A blank inflation cell is **not published**, not zero. Year-on-year inflation on the longer All India run is not published for 2013 — not zero.

The latest printed month on this page is still Provisional. The same monthly release also prints Final figures for a different month; those are not a revision of the Provisional month.

Rural, Urban, and Combined are three published sectors. All India Combined is the producer’s national unit, not a roll-up of State/UT Combined, and not every district. Chandigarh Rural is not published (no rural market in Chandigarh). Districts are not on this page.

Independently compiled indexes on this base run from January 2025. This page binds the latest Final month and the latest Provisional month only. Months in between that the compiled files do not carry stay not published. Those months are not filled from a longer All India run, and that run is not joined to these two months as one line.

This page does not include forecasts; cheap or expensive verdicts; city rankings; petrol, diesel or LPG pump prices; district figures; WPI; or CPI 2012=100 drawn as one line with Base 2024=100.
{{/how-this-is-measured}}
