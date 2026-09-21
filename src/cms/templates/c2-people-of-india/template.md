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
<p>As on {{period.projection_2026.label}}, the official projection for India, Persons, is {{slot:india-projected-persons-2026}}. That is a National Commission on Population projection from the 2019 Technical Group report, not a census count. Census 2011 enumerated {{slot:india-total-persons-2011}} people in India, Total, as of {{period.census_2011.label}} — the latest published census Total.</p>
</div>

{{stat-row}}
{{stat:india-total-persons-2011|India, Total}}
{{stat:india-rural-persons-2011|India, Rural}}
{{stat:india-urban-persons-2011|India, Urban}}
{{/stat-row}}

<p class="source-line">National Commission on Population · projected population, 1 March · {{period.projection_2026.label}}</p>
<p class="source-line">Office of the Registrar General &amp; Census Commissioner, India · Census 2011 · {{period.census_2011.label}}</p>

<p>Rural, Urban, and Total are three published lines. Total is not an average made here. India is the national unit as printed, not every district. Telangana and Ladakh are not State or UT labels on this 2011 map.</p>

<nav class="hottest-rail" aria-label="Further questions">
<a href="#where">Where were people counted in 2011?</a>
<a href="#change">How did census counts change through 2011?</a>
<a href="#births-deaths">What do 2024 birth and death rates say?</a>
<a href="#fertility">What does the 2024 fertility report say?</a>
<a href="#projection">What does the official projection print?</a>
</nav>
{{/hero}}

{{section}}
<h2 id="where">Where were people counted in 2011?</h2>

Census 2011 prints a Total count for each State and Union Territory on that map. They are listed alphabetically. This is not a ranking.

{{chart:state-ut-total-2011}}

<p class="source-line">Office of the Registrar General &amp; Census Commissioner, India · Census 2011, Total · {{period.census_2011.label}}</p>

<p>India Total is the national unit above, not a bar here. Districts in the same workbook are not on this page. Telangana and Ladakh are not on this 2011 list. Daman &amp; Diu and Dadra &amp; Nagar Haveli are two rows.</p>
{{/section}}

{{section}}
<h2 id="change">How did census counts change through 2011?</h2>

India Total census counts are printed for census years from 1901 through 2011. That run stops at 2011. It is not joined to the projection below.

{{chart:india-census-years-1901-2011}}

<p class="source-line">Office of the Registrar General &amp; Census Commissioner, India · census years 1901–2011</p>

<p>A blank or not-available cell is a hole, not zero. This table is not a 2024 headcount and not a birth rate.</p>
{{/section}}

{{section}}
<h2 id="births-deaths">What do 2024 birth and death rates say?</h2>

These are Sample Registration System rates for {{period.srs_2024.label}}, not a census count. They are not multiplied by the 2011 headcount on this page.

<p>In that year, India’s Total birth rate was {{slot:india-birth-rate-2024}}. The death rate was {{slot:india-death-rate-2024}}. The infant mortality rate was {{slot:india-imr-2024}}.</p>

{{stat-row}}
{{stat:india-birth-rate-2024|Birth rate, Total}}
{{stat:india-death-rate-2024|Death rate, Total}}
{{stat:india-imr-2024|Infant mortality rate, Total}}
{{/stat-row}}

{{chart:india-srs-rates-2024}}

<p class="source-line">Office of the Registrar General of India, Vital Statistics Division · SRS Bulletin · {{period.srs_2024.label}}</p>

<p>Rates are not “how many people live in India.” This bulletin does not print total fertility. Manipur carries a sample footnote on the table of record.</p>
{{/section}}

{{section}}
<h2 id="fertility">What does the 2024 fertility report say?</h2>

<p>In {{period.srs_2024.label}}, India’s Total fertility rate was {{slot:india-tfr-2024}}. Rural was {{slot:india-tfr-rural-2024}}; urban was {{slot:india-tfr-urban-2024}}.</p>

{{stat-row}}
{{stat:india-tfr-2024|Total fertility rate, India}}
{{stat:india-tfr-rural-2024|Rural}}
{{stat:india-tfr-urban-2024|Urban}}
{{/stat-row}}

<p class="source-line">Office of the Registrar General &amp; Census Commissioner, India · SRS Statistical Report 2024 · {{period.srs_2024.label}}</p>

<p>This report’s main fertility table is India and bigger States and Union Territories as printed. Smaller States, most Union Territories, and districts are missing here. Do not fill those holes from the bulletin above.</p>
{{/section}}

{{section}}
<h2 id="projection">What does the official projection print?</h2>

A 2019 technical-group report prints projected population in thousands as on 1 March, 2011 to 2036. That is a projection, not a census. The 2011 column is not the Census 2011 count above.

On {{period.projection_2026.label}}, the official projection prints {{slot:india-projected-persons-2026}} people for India, Persons.

{{chart:india-projected-2011-2036}}

<p class="source-line">National Commission on Population, Ministry of Health &amp; Family Welfare · projected population, thousands, 1 March</p>

<p>A 2026 cell is still that 2019 report. It does not close the missing later census. The projection is not joined to the 1901–2011 census line.</p>
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

<!-- cite-view: how-this-is-measured. Prose only. Do not bind an observation here — a number in this view would require a second copy of the citation cards. -->

Census counts, Sample Registration System rates, and the 2011–2036 projection are three records. This page shows each as itself. It does not pick a winner or make one “India today” figure.

Census 2011 is the latest published census total. Census 2021 totals were not published. Census 2027 houselisting is not a count.

Census 2011 counts everyone enumerated on the published India and State or Union Territory rows. District rows in the same workbook are not on this page. This is not NPR, electoral rolls, or a count of who lives here now.

The 2011 Census map does not include Telangana or Ladakh as State or UT rows. Daman &amp; Diu and Dadra &amp; Nagar Haveli are separate.

Birth, death, and infant mortality rates on this page are 2024 survey estimates. They are not a headcount. Total fertility lives on the statistical report, whose main tables miss smaller States and Union Territories.

The official projection is from the 2019 Technical Group report, as on 1 March. The producer prints thousands of persons; compact display on this page uses the same scale as census person counts. That does not make the projection a census. Its 2011 column is a smoothed projected base, not the Census 2011 count. A later year on that table is not an enumeration.

This page does not include NPR or citizenship registers; electoral rolls; caste politics; district maps; ranks; forecasts; or international modelled stocks as the source of record.
{{/how-this-is-measured}}
