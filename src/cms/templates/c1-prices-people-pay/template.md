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
<p>Year-on-year inflation was {{slot:all-india-combined-general-inflation-latest-p}} percent as of {{period.latest_provisional.label}}, All India Combined. Food was {{slot:all-india-combined-cfpi-inflation-latest-p}} percent. CPI (General) is the headline retail price index of selected goods and services collected in sampled rural and urban markets.</p>
</div>

{{stat-row}}
{{stat:all-india-combined-general-inflation-latest-p|CPI (General), Combined}}
{{stat:all-india-combined-cfpi-inflation-latest-p|Food, Combined}}
{{/stat-row}}

{{chart:general-beside-food}}

<p class="source-line">NSO / MoSPI · CPI (General) and food · {{period.latest_provisional.label}} · released {{cite:cite-c1-cpi-general-base-2024-2026-08.release_date}}</p>

<p>The same release also prints {{period.latest_final.label}}: {{slot:all-india-combined-general-inflation-latest-f}} percent on CPI (General) Combined and {{slot:all-india-combined-cfpi-inflation-latest-f}} percent on food — a different month, not a revision of the figures above.</p>

<nav class="hottest-rail" aria-label="Further questions">
<a href="#food">How fast is food rising?</a>
<a href="#basket">What else in the basket is rising?</a>
<a href="#rural-urban">How fast are rural and urban prices rising?</a>
<a href="#states">How fast are prices rising in the States and Union Territories?</a>
<a href="#rate-over-time">How has this rate moved?</a>
</nav>
{{/hero}}

{{section}}
<h2 id="food">How fast is food rising?</h2>

Food and beverages — a wider basket that also includes drinks and food-processing services — was {{slot:all-india-combined-div01-inflation-latest-p}} percent All India Combined in {{period.latest_provisional.label}}. That is a different official series from the Consumer Food Price Index on the first screen; both are published in the same release.

On the Consumer Food Price Index alone, rural food was {{slot:all-india-rural-cfpi-inflation-latest-p}} percent and urban food was {{slot:all-india-urban-cfpi-inflation-latest-p}} percent in that month.

{{chart:cfpi-beside-division-01}}

<p class="source-line">NSO / MoSPI · Consumer Food Price Index and Food and beverages · {{period.latest_provisional.label}}</p>
{{/section}}

{{section}}
<h2 id="basket">What else in the basket is rising?</h2>

All India Combined, {{period.latest_provisional.label}}. These are the published groups of the retail basket, in the order the producer prints them.

{{chart:all-india-division-inflation-latest}}

<p class="source-line">NSO / MoSPI · CPI groups · {{period.latest_provisional.label}}</p>

Food and beverages on this chart is not the Consumer Food Price Index above.
{{/section}}

{{section}}
<h2 id="rural-urban">How fast are rural and urban prices rising?</h2>

In {{period.latest_provisional.label}}, All India rural year-on-year inflation was {{slot:all-india-rural-general-inflation-latest-p}} percent; urban was {{slot:all-india-urban-general-inflation-latest-p}} percent.

{{stat-row}}
{{stat:all-india-rural-general-inflation-latest-p|CPI (General), Rural}}
{{stat:all-india-urban-general-inflation-latest-p|CPI (General), Urban}}
{{/stat-row}}

{{chart:all-india-sectors-inflation-latest}}

<p class="source-line">NSO / MoSPI · CPI (General) · {{period.latest_provisional.label}} · released {{cite:cite-c1-cpi-general-base-2024-2026-08.release_date}}</p>

Combined is a published sector, not an average made here. All India Combined is the national unit, not every district.
{{/section}}

{{section}}
<h2 id="states">How fast are prices rising in the States and Union Territories?</h2>

In {{period.latest_provisional.label}}, CPI (General) Combined is printed for each State and Union Territory. They are listed alphabetically by official English name.

{{chart:state-ut-combined-inflation-latest}}

<p class="source-line">NSO / MoSPI · CPI (General) Combined · {{period.latest_provisional.label}}</p>

Chandigarh Rural this month: {{slot:chandigarh-rural-general-inflation-latest-p}}. Chandigarh Combined is on the chart.
{{/section}}

{{section}}
<h2 id="rate-over-time">How has this rate moved?</h2>

A longer All India Combined run of year-on-year inflation goes through December 2024. It does not include the compiled months in the figures above.

{{chart:all-india-linked-inflation-holes}}

<p class="source-line">NSO / MoSPI · CPI General inflation (All India) · 2013 unpublished</p>

Year-on-year inflation on this run is not published for 2013 — not zero. Filled months begin January 2014.
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

CPI here is a price index from a price-collection system, not a census of every shop and not a pump-price register.

{{slot:caveat-general-population}}

The index is on a 2024 base. Index points and year-on-year inflation (%) are separate observations. A blank inflation cell is not published, not zero.

The latest printed month on this page is still Provisional. The same monthly release also prints Final figures for a different month; those are not a revision of the Provisional month. Provisional and Final are different statuses for different months — not two readings of the same month.

Rural, Urban, and Combined are three published sectors. Combined is not a Rural–Urban average made on this page. All India Combined is the producer’s national unit, not a roll-up of State/UT Combined, and not every district.

The press date is the release, not the month the prices refer to.

Independently compiled indexes on this base run from January 2025. This page binds the latest Final month and the latest Provisional month only. Months in between that the compiled files do not carry stay not published. Those months are not filled from a longer All India run, and that run is not joined to these two months as one line.

Prices are grouped as the producer groups them on this base. An older six-group description on the MoSPI site is not the grouping of record for these numbers.

Chandigarh Rural is not published (no rural market in Chandigarh). On the printed Chandigarh row, Combined equals Urban. Districts are not on this page.

This page does not include forecasts; cheap or expensive verdicts; city rankings; press “top five States” or “top five items” tables as a ranking; petrol, diesel or LPG pump prices; district figures; item or subclass indexes; WPI; Labour Bureau CPI-IW, CPI-AL or CPI-RL; or CPI 2012=100 drawn as one line with Base 2024=100.
{{/how-this-is-measured}}
