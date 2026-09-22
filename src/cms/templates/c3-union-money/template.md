---
template_id: c3-union-money
charter: C3
sleeve: money
slug: union
citizen_question: What does the Union collect, and what does it spend it on?
slots: ./slots.yaml
---

{{hero}}
<!-- cite-view: first-screen. CMS must show producer (linked), series, reference period, release date (Asia/Kolkata), and caveat in this same view as the numbers. A tooltip is not enough. Fail the render if any required card is missing. Do not move citizen_pointer. -->

<p class="sleeve">Money</p>

# What does the Union collect, and what does it spend it on?

<p class="byline">Updated {{cite:cite-c3-budget-2026-27-annex1-trends-receipts.release_date}} (Asia/Kolkata). Next named release {{cite:cite-c3-budget-2026-27-annex1-trends-receipts.next_release}}.</p>

<div class="fact-lede">
<p><span class="thesis-mark">The Union government plans to collect {{slot:annex1-revenue-receipts-be}} and spend {{slot:stat1-total-expenditure-be}} in {{period.budget_estimates_2026_27.year_label}}.</span></p>
<p>The last year with final accounts, {{period.actuals_2024_25.year_label}}, it collected {{slot:annex1-revenue-receipts-actuals-2024-25}}.</p>
<p>These are Budget Estimates — the plan printed in this year's Budget.</p>
</div>

{{stat-row}}
{{stat:annex1-revenue-receipts-be|Revenue receipts}}
{{stat:stat1-total-expenditure-be|Total expenditure}}
{{stat:liabilities-total-end-2024-25|Total liabilities}}
{{stat:ntr-non-tax-be|Non-tax revenue}}
{{/stat-row}}

{{chart:collect-beside-spend}}

<p class="source-line">Ministry of Finance, Budget Division · Union Budget 2026-27 · {{period.budget_estimates_2026_27.label}} · laid {{cite:cite-c3-budget-2026-27-annex1-trends-receipts.release_date}}</p>

<nav class="hottest-rail" aria-label="Further questions">
<a href="#collect">Where does the money come from?</a>
<a href="#spend">Where does it go?</a>
<a href="#liabilities">What does the Union owe?</a>
<a href="#three-records">Plan, revised plan, final accounts</a>
<a href="#deficit">What deficits does the Budget print?</a>
<a href="#receipts-over-time">How have receipts moved in this Budget book?</a>
</nav>
{{/hero}}

{{section}}
<h2 id="collect">Where does the money come from?</h2>

In {{period.budget_estimates_2026_27.label}}, tax is printed by major head — each against the last published Actuals where the book prints them. These are gross tax heads.

{{chart:tax-heads-be}}

<p class="source-line">Ministry of Finance, Budget Division · Receipt Budget, tax revenue · {{period.budget_estimates_2026_27.label}} · {{cite:cite-c3-budget-2026-27-tax-revenue.release_date}}</p>

{{stat-row}}
{{stat:ntr-non-tax-be|Non-tax revenue}}
{{stat:capital-non-debt-be|Non-debt capital receipts}}
{{stat:capital-debt-be|Debt receipts}}
{{/stat-row}}
{{/section}}

{{section}}
<h2 id="spend">Where does it go?</h2>

The Budget’s summary splits spending into central expenditure and transfers to States and Union Territories — Budget Estimates for {{period.budget_estimates_2026_27.label}}.

{{chart:spend-blocks-be}}

<p class="source-line">Ministry of Finance, Budget Division · Expenditure Profile, Statement 1 · {{period.budget_estimates_2026_27.label}} · {{cite:cite-c3-budget-2026-27-expenditure-stat1.release_date}}</p>

<p>Central expenditure was {{slot:stat1-central-expenditure-be}}. Transfers were {{slot:stat1-transfers-be}}.</p>
{{/section}}

{{section}}
<h2 id="liabilities">What does the Union owe?</h2>

Outstanding liabilities are a stock at year-end. At end of {{period.actuals_2024_25.year_label}}, total liabilities were {{slot:liabilities-total-end-2024-25}}.

{{stat-row}}
{{stat:liabilities-public-debt-end-2024-25|Public debt}}
{{stat:liabilities-other-end-2024-25|Other liabilities}}
{{stat:liabilities-total-end-2024-25|Total liabilities}}
{{/stat-row}}

{{chart:liabilities-stock}}

<p class="source-line">Ministry of Finance, Budget Division · Statement of Liabilities of the Central Government · year-end as labelled · {{cite:cite-c3-budget-2026-27-liabilities.release_date}}</p>
{{/section}}

{{section}}
<h2 id="three-records">Plan, revised plan, final accounts</h2>

Budget Estimates, Revised Estimates, and Actuals are three records — one cite control per observation.

{{stat-row}}
{{stat:annex1-revenue-receipts-be|Budget Estimates 2026-27}}
{{stat:annex1-revenue-receipts-actuals-2024-25|Budget book, Actuals 2024-25}}
{{stat:fa-revenue-receipts-actuals-2024-25|Finance Accounts, Actuals 2024-25}}
{{stat:cga-monthly-revenue-receipts-upto-july-2026|Monthly accounts, up to July 2026}}
{{/stat-row}}

<p class="source-line">Ministry of Finance, Budget Division · Receipt Budget, Annex-1 · Budget Estimates 2026-27 and Actuals 2024-25 · {{cite:cite-c3-budget-2026-27-annex1-trends-receipts.release_date}}</p>
<p class="source-line">Controller General of Accounts · Finance Accounts · Actuals 2024-25 · {{cite:cite-c3-cga-finance-accounts-2024-25-stat1.release_date}}</p>
<p class="source-line">Controller General of Accounts · Monthly accounts · up to July 2026 · {{cite:cite-c3-cga-monthly-glance-2026-07.release_date}}</p>
{{/section}}

{{section}}
<h2 id="deficit">What deficits does the Budget print?</h2>

In {{period.budget_estimates_2026_27.label}}, the Budget at a Glance prints fiscal deficit, revenue deficit, effective revenue deficit, and primary deficit as labelled.

{{chart:deficit-be}}

<p class="source-line">Ministry of Finance, Budget Division · Budget at a Glance, Deficit Statistics · {{period.budget_estimates_2026_27.label}} · {{cite:cite-c3-budget-2026-27-deficit-statistics.release_date}}</p>
{{/section}}

{{section}}
<h2 id="receipts-over-time">How have receipts moved in this Budget book?</h2>

Filled Actuals run from {{period.annex1_actuals_from.label}} through {{period.annex1_actuals_to.label}}. The last columns are Revised Estimates and Budget Estimates — not Actuals.

{{chart:receipts-run}}

<p class="source-line">Ministry of Finance, Budget Division · Receipt Budget, Annex-1 · years as labelled · {{cite:cite-c3-budget-2026-27-annex1-trends-receipts.release_date}}</p>
{{/section}}

<div class="source-stack">
<p class="source-stack-label">Sources on this page</p>
{{cite-block:annex1}}
{{cite-block:tax}}
{{cite-block:non-tax}}
{{cite-block:capital}}
{{cite-block:expenditure}}
{{cite-block:deficit}}
{{cite-block:liabilities}}
{{cite-block:frbm-hole}}
{{cite-block:afs}}
{{cite-block:cga-monthly}}
{{cite-block:finance-accounts}}
{{caveat-block:caveat-c3-budget-2026-27-annex1-trends-receipts}}
</div>

{{how-this-is-measured}}
## Methodology

<!-- cite-view: how-this-is-measured. Prose only. -->

Budget Estimates are the plan printed in this year's Budget — not Actuals and not Revised Estimates. The three are separate records; do not read them as one continuous change.

The headline revenue-receipts figure is the Budget’s printed receipts total, not a sum of the tax, non-tax, and capital statements below. Tax heads on the receipts chart are gross; Annex-1 tax revenue is often net of States’ share.

GST Compensation Cess is **not published** where the statement prints a blank. Integrated GST (IGST) may be a published **zero** — say both plainly; never plot the cess gap as zero.

These are Union accounts. They are not the accounts of the States, of Union Territories as own governments, or of districts. Outstanding liabilities on this page are Central Government as printed — not general government including states. Debt receipts on many lines are printed net of repayments. Monthly CGA figures for April–July are unaudited intra-year accounts, not a year-end actual.
{{/how-this-is-measured}}
