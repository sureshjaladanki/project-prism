---
template_id: c2-people-of-india
charter: C2
sleeve: people
slug: population
citizen_question: How many people live in India, where, and how is that changing?
slots: ./slots.yaml
---

{{hero}}
<!-- cite-view: first-screen. CMS must show producer (linked), series, reference period, release date (Asia/Kolkata), and caveat in this same view as the numbers. A tooltip is not enough. Fail the render if any required card is missing. Do not move citizen_pointer. -->

<p class="sleeve">People</p>

# How many people live in India, where, and how is that changing?

<p class="byline">Official projection as on {{period.projection_2026.label}}. Latest published census Total: {{period.census_2011.label}}.</p>

<div class="fact-lede">
<p><span class="thesis-mark">About {{slot:india-projected-persons-2026}} live in India in {{period.projection_2026.label}}, on the government's official projection.</span></p>
<p>The last time everyone was counted, in Census 2011, the total was {{slot:india-total-persons-2011}}; in 2001 it was {{slot:india-total-persons-2001}}.</p>
<p>A projection is the government's estimate of how many people there are now, carried forward from the last count.</p>
</div>

{{stat-row}}
{{stat:india-projected-persons-2026|Projection · persons}}
{{stat:india-total-persons-2011|Census 2011 Total · persons}}
{{stat:india-birth-rate-2024|Birth rate · per 1,000}}
{{stat:india-death-rate-2024|Death rate · per 1,000}}
{{/stat-row}}

{{chart:india-projected-2011-2036}}

<p class="source-line">National Commission on Population · projected population, 1 March · {{period.projection_2026.label}}</p>
<p class="source-line">Office of the Registrar General &amp; Census Commissioner, India · Census 2011 · {{period.census_2011.label}}</p>

<nav class="hottest-rail" aria-label="Further questions">
<a href="#where">Where do people live?</a>
<a href="#change">How fast is that changing?</a>
<a href="#births-deaths">Who is being born, and who is dying?</a>
<a href="#fertility">What does the fertility report say?</a>
<a href="#projection">What does the official projection print?</a>
</nav>
{{/hero}}

{{section}}
<h2 id="where">Where do people live?</h2>

Census 2011 prints a Total count for each State and Union Territory. They are listed alphabetically.

{{chart:state-ut-total-2011}}

<p class="source-line">Office of the Registrar General &amp; Census Commissioner, India · Census 2011, Total · {{period.census_2011.label}}</p>
{{/section}}

{{section}}
<h2 id="change">How fast is that changing?</h2>

India Total census counts from 1901 through 2011, with plain year ticks — then the projection path on the first screen, named as projection.

{{chart:india-census-years-1901-2011}}

<p class="source-line">Office of the Registrar General &amp; Census Commissioner, India · census years 1901–2011</p>
{{/section}}

{{section}}
<h2 id="births-deaths">Who is being born, and who is dying?</h2>

Sample Registration System rates for {{period.srs_2024.label}} — survey estimates for that year, each with its unit.

<p>India’s Total birth rate was {{slot:india-birth-rate-2024}}. The death rate was {{slot:india-death-rate-2024}}. The infant mortality rate was {{slot:india-imr-2024}}.</p>

{{stat-row}}
{{stat:india-birth-rate-2024|Birth rate · per 1,000}}
{{stat:india-death-rate-2024|Death rate · per 1,000}}
{{stat:india-imr-2024|Infant mortality · per 1,000}}
{{/stat-row}}

{{chart:india-srs-rates-2024}}

<p class="source-line">Office of the Registrar General of India, Vital Statistics Division · SRS Bulletin · {{period.srs_2024.label}}</p>
{{/section}}

{{section}}
<h2 id="fertility">What does the fertility report say?</h2>

<p>In {{period.srs_2024.label}}, India’s Total fertility rate was {{slot:india-tfr-2024}}. Rural was {{slot:india-tfr-rural-2024}}; urban was {{slot:india-tfr-urban-2024}}.</p>

{{stat-row}}
{{stat:india-tfr-2024|Total fertility rate}}
{{stat:india-tfr-rural-2024|Rural}}
{{stat:india-tfr-urban-2024|Urban}}
{{/stat-row}}

<p class="source-line">Office of the Registrar General &amp; Census Commissioner, India · SRS Statistical Report 2024 · {{period.srs_2024.label}}</p>
{{/section}}

{{section}}
<h2 id="projection">What does the official projection print?</h2>

On {{period.projection_2026.label}}, the official projection for India, Persons, is {{slot:india-projected-persons-2026}}. The chart on the first screen shows the full projection path beside the census years under “How fast is that changing?”.
{{/section}}

<div class="source-stack">
<p class="source-stack-label">Sources on this page</p>
{{cite-block:census-pca}}
{{cite-block:census-a02}}
{{cite-block:srs-bulletin}}
{{cite-block:srs-stat}}
{{cite-block:ncp-table8}}
{{caveat-block:caveat-c2-census-2011-pca-sd}}
</div>

{{how-this-is-measured}}
## Methodology

<!-- cite-view: how-this-is-measured. Prose only. -->

A projection is not a census enumeration. Census 2011 counted persons on 1 March 2011 — the latest published census Total. The National Commission on Population Table 8 projection is printed in thousands of persons; Census PCA is persons. After canonical conversion they share the persons ladder on this page; they remain different records and are not joined as one continuous headcount line.

The 2011 column on the projection table is a smoothed projected base, not the Census 2011 count. A later year on that table is still the 2019 Technical Group report — not an enumeration.

SRS birth, death, infant mortality, and fertility rates are survey rates, not headcounts. Do not multiply them by the 2011 headcount on this page. Blank or not-available census cells are **not published**, not zero. Telangana and Ladakh are not State or UT labels on the 2011 map. Districts are not on this page. Smaller States and most Union Territories are not on the main fertility table.
{{/how-this-is-measured}}
