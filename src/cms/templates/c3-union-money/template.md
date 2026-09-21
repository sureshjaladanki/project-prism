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
<p>In {{period.budget_estimates_2026_27.label}}, Government of India revenue receipts were {{slot:annex1-revenue-receipts-be}}. Total expenditure through the Budget was {{slot:stat1-total-expenditure-be}}. Budget Estimates are the printed plan for that year, not Actuals. Revenue receipts on this line are the Budget’s printed receipts total, not a sum of the tax, non-tax, and capital statements below.</p>
</div>

{{stat-row}}
{{stat:annex1-revenue-receipts-be|Revenue receipts}}
{{stat:stat1-total-expenditure-be|Total expenditure through the Budget}}
{{/stat-row}}

{{chart:collect-beside-spend}}

<p class="source-line">Ministry of Finance, Budget Division · Union Budget 2026-27 · {{period.budget_estimates_2026_27.label}} · laid {{cite:cite-c3-budget-2026-27-annex1-trends-receipts.release_date}}</p>

<p>These are Union accounts. They are not the accounts of the States, of Union Territories as own governments, or of districts.</p>

<nav class="hottest-rail" aria-label="Further questions">
<a href="#collect">What does the Union collect?</a>
<a href="#spend">What does it spend it on?</a>
<a href="#deficit">What deficits does the Budget print?</a>
<a href="#liabilities">What liabilities are outstanding?</a>
<a href="#receipts-over-time">How have receipts moved in this Budget book?</a>
<a href="#three-records">How do the monthly accounts and Finance Accounts sit beside the Budget?</a>
</nav>
{{/hero}}

{{section}}
<h2 id="collect">What does the Union collect?</h2>

Tax, non-tax, and capital receipts are three statements in the same Budget book. They are not one collections total made on this page.

In {{period.budget_estimates_2026_27.label}}, tax is printed by major head. These are gross tax heads. They are not tax after States’ share — that net figure sits in the receipts total above.

{{chart:tax-heads-be}}

<p class="source-line">Ministry of Finance, Budget Division · Receipt Budget, tax revenue · {{period.budget_estimates_2026_27.label}}</p>

<p>GST Compensation Cess on this chart is a hole where the statement prints a blank, not zero.</p>

{{stat-row}}
{{stat:ntr-non-tax-be|Non-tax revenue}}
{{stat:capital-non-debt-be|Non-debt capital receipts}}
{{stat:capital-debt-be|Debt receipts}}
{{/stat-row}}

<p>Debt receipts on many lines are printed net of repayments. Market loans (net) is not gross market borrowing. Receipts of Union Territories on the non-tax statement are a Union budget head, not the accounts of a Union Territory government.</p>
{{/section}}

{{section}}
<h2 id="spend">What does it spend it on?</h2>

The Budget’s own summary splits spending into central expenditure and transfers. Transfers to States and Union Territories here are Union outgo, not those governments’ own accounts.

In {{period.budget_estimates_2026_27.label}}, central expenditure was {{slot:stat1-central-expenditure-be}}. Transfers were {{slot:stat1-transfers-be}}. Both numbers are the printed Total column.

{{chart:spend-blocks-be}}

<p class="source-line">Ministry of Finance, Budget Division · Expenditure Profile, Statement 1 · {{period.budget_estimates_2026_27.label}}</p>

<p>Central expenditure is printed as establishment, central sector schemes, and other central expenditure. Transfers are printed as centrally sponsored schemes, Finance Commission transfers, and other transfers.</p>

<p>A second printed total, total expenditure through the Budget and resources of public enterprises, was {{slot:stat1-total-with-psu-be}} in the same column. That is a different line from total expenditure through the Budget above.</p>
{{/section}}

{{section}}
<h2 id="deficit">What deficits does the Budget print?</h2>

In {{period.budget_estimates_2026_27.label}}, the Budget at a Glance prints fiscal deficit, revenue deficit, effective revenue deficit, and primary deficit as labelled. These are the producer’s lines, not a grade.

{{chart:deficit-be}}

<p class="source-line">Ministry of Finance, Budget Division · Budget at a Glance, Deficit Statistics · {{period.budget_estimates_2026_27.label}}</p>

<p>The same table also prints Actuals {{period.actuals_2024_25.year_label}} and Revised Estimates {{period.revised_2025_26.year_label}}. Those columns are not this chart.</p>

<p>The FRBM statutory packet for this Budget is {{slot:frbm-not-a-table}}. Deficit statistics and outstanding liabilities remain the Budget tables on this page. This page does not turn the Act’s printed wording into a pass or fail.</p>
{{/section}}

{{section}}
<h2 id="liabilities">What liabilities are outstanding?</h2>

Outstanding liabilities are a stock at year-end, not the year’s deficit and not the year’s net debt receipts.

At end of {{period.actuals_2024_25.year_label}}, Central Government public debt was {{slot:liabilities-public-debt-end-2024-25}}. Other liabilities were {{slot:liabilities-other-end-2024-25}}. Total liabilities were {{slot:liabilities-total-end-2024-25}}.

{{stat-row}}
{{stat:liabilities-public-debt-end-2024-25|Public debt}}
{{stat:liabilities-other-end-2024-25|Other liabilities}}
{{stat:liabilities-total-end-2024-25|Total liabilities}}
{{/stat-row}}

{{chart:liabilities-stock}}

<p class="source-line">Ministry of Finance, Budget Division · Statement of Liabilities of the Central Government · year-end as labelled</p>

<p>Revised Estimates {{period.revised_2025_26.year_label}} and Budget Estimates {{period.budget_estimates_2026_27.year_label}} on this chart are not year-end Actuals. They are not joined to the Actuals years as one line. This statement is not debt as defined in the FRBM Act.</p>
{{/section}}

{{section}}
<h2 id="receipts-over-time">How have receipts moved in this Budget book?</h2>

The Budget’s multi-year receipts table prints revenue receipts for the years in that file. Tax revenue in this table is net of States’ share — not the gross tax heads above.

Filled Actuals run from {{period.annex1_actuals_from.label}} through {{period.annex1_actuals_to.label}}. The last two columns are Revised Estimates {{period.revised_2025_26.year_label}} and Budget Estimates {{period.budget_estimates_2026_27.year_label}}. They are not Actuals.

{{chart:receipts-run}}

<p class="source-line">Ministry of Finance, Budget Division · Receipt Budget, Annex-1 · years as labelled in that table</p>

<p>This run does not continue past the years in the file.</p>
{{/section}}

{{section}}
<h2 id="three-records">How do the monthly accounts and Finance Accounts sit beside the Budget?</h2>

The Budget book, the monthly accounts, and the Finance Accounts are three records. They are not one Union-money figure.

{{stat-row}}
{{stat:annex1-revenue-receipts-actuals-2024-25|Budget book, Actuals 2024-25}}
{{stat:cga-monthly-revenue-receipts-upto-july-2026|Monthly accounts, up to July 2026}}
{{stat:fa-revenue-receipts-actuals-2024-25|Finance Accounts, Actuals 2024-25}}
{{/stat-row}}

<p>Budget-book Actuals {{period.actuals_2024_25.year_label}} are the Budget’s printed Actuals, not the Finance Accounts. Monthly actuals are unaudited figures for April–July 2026 of financial year 2026-27, against Budget Estimates 2026-27 — not a year-end actual. Finance Accounts {{period.finance_accounts_2024_25.label}} are annual Actuals from the Controller General of Accounts.</p>

<p>The Annual Financial Statement laid with this Budget is a fourth constitutional statement of the same Union accounts family, not a replacement for the Receipt Budget or Expenditure Profile. In {{period.budget_estimates_2026_27.label}} it prints corporation tax as {{slot:afs-corporation-tax-be}}. That is the Annual Financial Statement line, not the Receipt Budget tax-head line above.</p>

<p class="source-line">Ministry of Finance, Budget Division · Controller General of Accounts · each record as labelled</p>
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

<!-- cite-view: how-this-is-measured. Prose only. Do not bind an observation here — a number in this view would require a second copy of the citation cards. -->

This page is Union accounts only. States as own governments, Union Territories as own governments, and districts are missing.

Budget Estimates, Revised Estimates, and Actuals in the same Budget table are different columns. They are not one continuous collect or spend.

Gross tax heads and tax net of States’ share are two concepts. Two printed expenditure totals stay two totals. Outstanding liabilities and debt as defined in the FRBM Act stay two concepts.

Tax, non-tax, capital receipts, the expenditure summary, and deficit statistics are taken from the producing-office workbooks. Multi-year receipts, outstanding liabilities, the Annual Financial Statement, and Finance Accounts were read from the printed tables. Line labels can wrap or truncate; a truncated label is not a different series.

Monthly accounts are unaudited figures for the months in that snapshot. A later month is not this snapshot.

The FRBM statutory packet is not published as a grid. Macro-economic framework, medium-term fiscal policy, the deviation statement, and the Act’s printed 3 percent, 40 percent, and 60 percent labels are missing as a table — not the collect, spend, deficit, or liabilities figures above.

Release dates are the laying or news dates. They are not the financial year on the row. Next named release is not printed on these artifacts.

This page does not include state or Union Territory finances; local-body accounts; district tables; scheme report cards; waste or welfare verdicts; per-person figures; forecasts; a government 10-K or listing-disclosure frame; Economic Survey narrative; or RBI, IMF, or credit-rating tables as the source of record.
{{/how-this-is-measured}}
