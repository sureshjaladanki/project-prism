---
template_id: c1-prices-people-pay
charter: C1
sleeve: prices-and-production
citizen_question: How fast are retail prices rising in India, including food?
bound_vintage_id: dv-20260916-234e263c8588
slots: ./slots.yaml
---

{{hero}}
<!-- cite-view: first-screen. CMS must show producer, series, reference period, release date (Asia/Kolkata), geography vintage, data vintage, and caveat in this same view as the numbers. A tooltip is not enough. Fail the render if any required card is missing. -->

<p class="sleeve">Prices and production</p>

# How fast are retail prices rising in India, including food?

<p class="byline">Updated {{cite:cite-c1-cpi-general-base-2024-2026-08.release_date}} (Asia/Kolkata). Next named release {{cite:cite-c1-cpi-general-base-2024-2026-08.next_release}}. Data vintage {{data_vintage_id}}.</p>

Year-on-year inflation (%) on **CPI (General)**, Base 2024=100, {{period.latest_provisional.label}}. Combined is a published sector in the same tables, not a Rural–Urban average made on this page.

{{stat-row}}
{{stat:all-india-combined-general-inflation-latest-p|All India Combined}}
{{stat:all-india-rural-general-inflation-latest-p|Rural}}
{{stat:all-india-urban-general-inflation-latest-p|Urban}}
{{/stat-row}}

All India (`00`) is the producer’s national unit. It is not a roll-up of State/UT Combined, and it is not every district. **Districts are not in this series** (parked). **Chandigarh Rural is not published** (the producer prints no rural market in Chandigarh). On the printed Chandigarh row, Combined equals Urban.

{{cite-block:general-latest}}
{{caveat-block:caveat-c1-cpi-general-base-2024}}

{{chart:all-india-sectors-inflation-latest}}
{{/hero}}

## Food, same month

The named food index is the **Consumer Food Price Index (CFPI)**. It is the same series as CPI Group “Food”, Group code **01.1**. It is **not** Division 01 “Food and beverages”.

{{stat-row}}
{{stat:all-india-combined-cfpi-inflation-latest-p|All India Combined, CFPI}}
{{stat:all-india-rural-cfpi-inflation-latest-p|Rural}}
{{stat:all-india-urban-cfpi-inflation-latest-p|Urban}}
{{/stat-row}}

Division 01 “Food and beverages” is a wider published basket (food plus beverages and services for processing primary goods for food). In the same month, All India Combined year-on-year inflation on Division 01 was {{slot:all-india-combined-div01-inflation-latest-p}} percent.

CFPI and Division 01 are two official numbers for the same place and month. This page does not choose between them.

{{cite-block:food-latest}}
{{caveat-block:caveat-c1-cpi-cfpi-base-2024}}
{{caveat-block:caveat-c1-cpi-division-group-base-2024}}

{{chart:cfpi-beside-division-01}}

## Provisional and Final

<!-- cite-view: provisional-and-final. CMS must show producer, series, reference period, release date (Asia/Kolkata), geography vintage, data vintage, and caveat in this same view as the July Final Combined numbers. A tooltip is not enough. Fail the render if any required card is missing. -->

{{period.latest_provisional.label}} and {{period.latest_final.label}} are printed in the same release. They are different observations. This page does not replace one with the other or blend them.

{{stat-row}}
{{stat:all-india-combined-general-inflation-latest-f|All India Combined, CPI (General)}}
{{stat:all-india-combined-cfpi-inflation-latest-f|All India Combined, CFPI}}
{{/stat-row}}

{{period.latest_final.label}}. Release date of this monthly book: {{cite:cite-c1-cpi-general-base-2024-2026-08.release_date}} (display in Asia/Kolkata). That date is not the reference month.

{{cite-block:general-final}}
{{cite-block:food-final}}
{{caveat-block:caveat-c1-cpi-general-base-2024}}
{{caveat-block:caveat-c1-cpi-cfpi-base-2024}}

## States and Union Territories

CPI (General) **Combined** year-on-year inflation (%), {{period.latest_provisional.label}}, as published. Units are listed in **alphabetical order of the official English State Name**. This is not a ranking. The axis is not sorted by the inflation measure.

All India is the national unit above; it is not a bar on this chart.

Chandigarh Rural (unit `04`, Rural) for this month: {{slot:chandigarh-rural-general-inflation-latest-p}}. Combined for Chandigarh is included on the chart.

{{cite-block:state-ut-latest}}
{{caveat-block:caveat-c1-cpi-general-base-2024}}

{{chart:state-ut-combined-inflation-latest}}

## A longer All India run, with a break

The producer publishes a **linked** CPI General back series expressed on Base 2024=100, All India only, from January 2013 through December 2024. Those months are not independently compiled 2024-basket observations.

Independently compiled Base 2024=100 General **starts January 2025**. This vintage does **not** include compiled General rows for January 2025 through June 2026. The compiled months present here are {{period.latest_final.label}} and {{period.latest_provisional.label}}.

The chart draws the linked series and the compiled months as separate encodings. It does not stitch them into one line. A break is marked at January 2025. The gap is months this vintage does not carry — not a dip to zero.

This linked file has **no State/UT rows**. Districts are missing here as well. Do not read it as the whole country at every administrative level.

The linked file’s own release date is **not printed**. Do not use the monthly press date for it. Next update for that file is unknown.

Year-on-year inflation (%) on the linked file is **not published for 2013**. That hole is not zero. The first filled linked inflation months begin January 2014.

{{cite-block:linked-back-series}}
{{caveat-block:caveat-c1-cpi-back-series-linked-base-2024}}

{{chart:all-india-linked-index-break}}
{{chart:all-india-linked-inflation-holes}}

## What the groups are (All India Combined)

CPI Divisions follow COICOP 2018 as printed on the live 2024=100 annexes (not the older six-group metadata PDF). Bars are in **producer annex order** (codes 01–11, then 13). There is no Division 12 on this slice. This is not a ranking, and colour does not mean better or worse.

**Food** on this page remains CFPI / Group 01.1, above. Division 01 on this chart is labelled **Food and beverages**.

{{cite-block:divisions-latest}}
{{caveat-block:caveat-c1-cpi-division-group-base-2024}}

{{chart:all-india-division-inflation-latest}}

## How this is measured

<!-- cite-view: how-this-is-measured. CMS must show producer, series, reference period, release date (Asia/Kolkata), geography vintage, data vintage, and caveat in this same view as the Combined General index. A tooltip is not enough. Fail the render if any required card is missing. -->

CPI here is a price index from a price-collection system, not a census of every shop and not a pump-price register.

{{slot:caveat-general-population}}

**Index** (Base 2024=100) and **year-on-year inflation (%)** are stored as separate observations. A blank inflation cell is a hole (`unknown`), not zero.

All India Combined CPI (General) **index**, {{period.latest_provisional.label}}: {{slot:all-india-combined-general-index-latest-p}}.

{{cite-block:general-latest}}
{{caveat-block:caveat-c1-cpi-general-base-2024}}

Rural, Urban, and Combined are three published sectors. This page does not average Rural and Urban to invent Combined.

Independently compiled indexes on this base run from January 2025 in the producer’s time-series workbooks. **This vintage’s compiled series files contain {{period.latest_final.reference_period}} and {{period.latest_provisional.reference_period}} only.** Year-on-year inflation on this base needs a prior year on this base; do not fill 2025 inflation blanks from the linked file.

Live grouping is COICOP 2018. A National Metadata Structure PDF on the MoSPI site still describes older six-group weights; that PDF is not the grouping of record for these numbers.

Published indexes are rounded to two decimal places. This page does not recompute higher-level indexes from rounded figures.

{{slot:caveat-general-do-not}}

Next monthly CPI release named on the citation card: {{cite:cite-c1-cpi-general-base-2024-2026-08.next_release}}.

## Not on this page

Forecasts; cheap or expensive verdicts; city rankings; press “top five States” or “top five items” tables as a ranking; petrol, diesel or LPG pump prices; district figures; item or subclass indexes; WPI; Labour Bureau CPI-IW, CPI-AL or CPI-RL; CPI 2012=100 drawn as one line with Base 2024=100.
