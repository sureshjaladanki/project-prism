"""C3 citation cards, caveat notes, and Union geography frames — attached, not rewritten."""

from __future__ import annotations

from datetime import date

from prism.ingest.c3 import (
    AFS_URL,
    ANNEX1_URL,
    BAG_URL,
    CAPITAL_URL,
    CGA_FA_URL,
    CGA_MONTHLY_URL,
    FRBM_URL,
    LIABILITIES_URL,
    NON_TAX_URL,
    STAT1_URL,
    TAX_URL,
)
from prism.refresh import (
    C3_FRAME_A_ID,
    C3_FRAME_B_ID,
    C3_FRAME_C_ID,
    C3_GEOGRAPHY_VINTAGE_2024,
    C3_GEOGRAPHY_VINTAGE_2026,
    C3_SERIES_BY_ID,
    CAVEAT_C3_CARD_1,
    CAVEAT_C3_CARD_2,
    CAVEAT_C3_CARD_3,
    CAVEAT_C3_CARD_4,
    CAVEAT_C3_CARD_5,
    CAVEAT_C3_CARD_6,
    CAVEAT_C3_CARD_7,
    CAVEAT_C3_CARD_8,
    CAVEAT_C3_CARD_9,
    CAVEAT_C3_CARD_10,
    CAVEAT_C3_CARD_11,
    CGA,
    CGA_LICENCE,
    CITE_C3_CARD_1,
    CITE_C3_CARD_2,
    CITE_C3_CARD_3,
    CITE_C3_CARD_4,
    CITE_C3_CARD_5,
    CITE_C3_CARD_6,
    CITE_C3_CARD_7,
    CITE_C3_CARD_8,
    CITE_C3_CARD_9,
    CITE_C3_CARD_10,
    CITE_C3_CARD_11,
    MOF_BUDGET,
    MOF_BUDGET_LICENCE,
    SERIES_BUDGET_2026_27_AFS,
    SERIES_BUDGET_2026_27_ANNEX1_TRENDS_RECEIPTS,
    SERIES_BUDGET_2026_27_CAPITAL_RECEIPTS,
    SERIES_BUDGET_2026_27_DEFICIT_STATISTICS,
    SERIES_BUDGET_2026_27_EXPENDITURE_STAT1,
    SERIES_BUDGET_2026_27_FRBM_STATEMENTS,
    SERIES_BUDGET_2026_27_LIABILITIES,
    SERIES_BUDGET_2026_27_NON_TAX_REVENUE,
    SERIES_BUDGET_2026_27_TAX_REVENUE,
    SERIES_CGA_FINANCE_ACCOUNTS_2024_25_STAT1,
    SERIES_CGA_MONTHLY_GLANCE_2026_07,
)
from prism.schema import (
    CaveatNote,
    Citation,
    CodeSystem,
    GeographyUnit,
    GeographyVintage,
)

BUDGET_LAID = date(2026, 2, 1)

UNITS_MISSING: tuple[str, ...] = (
    (
        "all States as own governments (C5): Andhra Pradesh; Arunachal Pradesh; Assam; "
        "Bihar; Chhattisgarh; Goa; Gujarat; Haryana; Himachal Pradesh; Jharkhand; "
        "Karnataka; Kerala; Madhya Pradesh; Maharashtra; Manipur; Meghalaya; Mizoram; "
        "Nagaland; Odisha; Punjab; Rajasthan; Sikkim; Tamil Nadu; Telangana; Tripura; "
        "Uttar Pradesh; Uttarakhand; West Bengal"
    ),
    (
        "all Union Territories as own governments (C5): Andaman and Nicobar Islands; "
        "Chandigarh; Dadra and Nagar Haveli and Daman and Diu; NCT of Delhi "
        "(legislature); Jammu and Kashmir (legislature); Ladakh; Lakshadweep; "
        "Puducherry (legislature)"
    ),
    "districts and below (parked)",
    "local-body accounts",
)


def _union_frame(
    *,
    frame_id: str,
    geography_vintage: str,
    code: str,
    name_en: str,
    breaks: str,
) -> GeographyVintage:
    return GeographyVintage(
        frame_id=frame_id,
        geography_vintage=geography_vintage,
        code_system=CodeSystem.none,
        frame="Union",
        units_included=(
            GeographyUnit(
                code=code, name_en=name_en, geography_vintage=geography_vintage
            ),
        ),
        units_missing=UNITS_MISSING,
        breaks=breaks,
        crosswalk="none",
    )


FRAME_A_GOI = _union_frame(
    frame_id=C3_FRAME_A_ID,
    geography_vintage=C3_GEOGRAPHY_VINTAGE_2026,
    code="government-of-india",
    name_en="Government of India",
    breaks=(
        "Union accounts for Budget 2026-27 as laid 1 February 2026. "
        "Not a state Finance Accounts vintage. Not CGA monthly (Frame B) "
        "and not Finance Accounts 2024-25 (Frame C)."
    ),
)
FRAME_A_HEADS = _union_frame(
    frame_id=C3_FRAME_A_ID,
    geography_vintage=C3_GEOGRAPHY_VINTAGE_2026,
    code="union-budget-heads",
    name_en="Union budget heads",
    breaks=FRAME_A_GOI.breaks,
)
FRAME_A_CENTRAL = _union_frame(
    frame_id=C3_FRAME_A_ID,
    geography_vintage=C3_GEOGRAPHY_VINTAGE_2026,
    code="central-government",
    name_en="Central Government",
    breaks=FRAME_A_GOI.breaks,
)
FRAME_B_UNION = _union_frame(
    frame_id=C3_FRAME_B_ID,
    geography_vintage=C3_GEOGRAPHY_VINTAGE_2026,
    code="union-government",
    name_en="Union Government",
    breaks=(
        "Intra-year unaudited Union accounts for FY 2026-27 up to July 2026. "
        "Not Budget BE/RE/Actuals (Frame A) and not Finance Accounts 2024-25 "
        "Actuals (Frame C). Do not recode onto Frame A labels."
    ),
)
FRAME_C_UNION = _union_frame(
    frame_id=C3_FRAME_C_ID,
    geography_vintage=C3_GEOGRAPHY_VINTAGE_2024,
    code="union-government",
    name_en="Union Government",
    breaks=(
        "Annual Actuals for FY 2024-25. Not Budget 2026-27 (Frame A) and "
        "not July 2026 monthly (Frame B). Do not recode proceeds assigned "
        "to States into a state finance row."
    ),
)


def _cite(
    series_id: str,
    citation_id: str,
    *,
    producer: str,
    artefact_id: str,
    reference_period: str,
    release_date: date | str,
    url: str,
    geography_as_published: str,
    frequency: str,
    licence: str,
    caveat_one_line: str,
) -> Citation:
    return Citation(
        citation_id=citation_id,
        producer=producer,
        series=C3_SERIES_BY_ID[series_id].name,
        id=artefact_id,
        reference_period=reference_period,
        release_date=release_date,
        url=url,
        geography_as_published=geography_as_published,
        frequency=frequency,
        licence=licence,
        next_release="unknown",
        caveat_one_line=caveat_one_line,
    )


C3_CITATIONS: dict[str, Citation] = {
    SERIES_BUDGET_2026_27_TAX_REVENUE: _cite(
        SERIES_BUDGET_2026_27_TAX_REVENUE,
        CITE_C3_CARD_1,
        producer=MOF_BUDGET,
        artefact_id=(
            "Receipt Budget Part A; fetch tr.xlsx sheet ReceiptReport123 "
            "(printed book tr.pdf)"
        ),
        reference_period="Actuals 2024-2025, Budget 2025-2026, Revised 2025-2026, Budget 2026-2027",
        release_date=BUDGET_LAID,
        url=TAX_URL,
        geography_as_published="Government of India / Union as published. Not a state Finance Accounts table. Not districts.",
        frequency="annual budget document",
        licence=MOF_BUDGET_LICENCE,
        caveat_one_line="BE / RE / Actuals are different vintages in the same table — do not collapse them. Gross tax is not Centre’s net tax.",
    ),
    SERIES_BUDGET_2026_27_NON_TAX_REVENUE: _cite(
        SERIES_BUDGET_2026_27_NON_TAX_REVENUE,
        CITE_C3_CARD_2,
        producer=MOF_BUDGET,
        artefact_id="Receipt Budget Part A; fetch ntr.xlsx sheet ReceiptReport123 (printed book ntr.pdf)",
        reference_period="Actuals 2024-2025, Budget 2025-2026, Revised 2025-2026, Budget 2026-2027",
        release_date=BUDGET_LAID,
        url=NON_TAX_URL,
        geography_as_published="Government of India / Union as published. Receipts of Union Territories is a Union budget head, not C5.",
        frequency="annual budget document",
        licence=MOF_BUDGET_LICENCE,
        caveat_one_line="Separate from tax revenue and from capital/debt receipts. Do not add Cards 1–3 into a Prism collections total.",
    ),
    SERIES_BUDGET_2026_27_CAPITAL_RECEIPTS: _cite(
        SERIES_BUDGET_2026_27_CAPITAL_RECEIPTS,
        CITE_C3_CARD_3,
        producer=MOF_BUDGET,
        artefact_id="Receipt Budget Part A; fetch ctr.xlsx sheet ReceiptReport123 (printed book cr.pdf). Workbook is ctr.xlsx, not cr.xlsx.",
        reference_period="Actuals 2024-2025, Budget 2025-2026, Revised 2025-2026, Budget 2026-2027",
        release_date=BUDGET_LAID,
        url=CAPITAL_URL,
        geography_as_published="Government of India / Union as published. Not state borrowings.",
        frequency="annual budget document",
        licence=MOF_BUDGET_LICENCE,
        caveat_one_line="Debt receipts are printed net of repayments on many lines. Market loans (net) is not gross market borrowings.",
    ),
    SERIES_BUDGET_2026_27_ANNEX1_TRENDS_RECEIPTS: _cite(
        SERIES_BUDGET_2026_27_ANNEX1_TRENDS_RECEIPTS,
        CITE_C3_CARD_4,
        producer=MOF_BUDGET,
        artefact_id="Annex-1; file doc/rec/annex1.pdf. Reconstructed PDF word-to-column; annex1.xlsx 404.",
        reference_period="Actual 2017-18 through 2024-25, RE 2025-26, BE 2026-27",
        release_date=BUDGET_LAID,
        url=ANNEX1_URL,
        geography_as_published="Government of India as published. Not states.",
        frequency="annual annex",
        licence=MOF_BUDGET_LICENCE,
        caveat_one_line="PDF reconstruction (ambiguous=0). Tax revenue here is net of States’ share. Last two columns are RE and BE, not Actuals.",
    ),
    SERIES_BUDGET_2026_27_EXPENDITURE_STAT1: _cite(
        SERIES_BUDGET_2026_27_EXPENDITURE_STAT1,
        CITE_C3_CARD_5,
        producer=MOF_BUDGET,
        artefact_id="Expenditure Profile Statement 1; fetch stat1.xlsx sheet Statement1 (printed book stat1.pdf)",
        reference_period="Actuals 2024-2025, BE 2025-2026, RE 2025-2026, BE 2026-2027",
        release_date=BUDGET_LAID,
        url=STAT1_URL,
        geography_as_published="Union budget heads. Transfers to States/UTs are Union outgo as printed — not C5.",
        frequency="annual budget document",
        licence=MOF_BUDGET_LICENCE,
        caveat_one_line="Two printed totals (with / without public-enterprise resources). Do not treat Transfers as C5.",
    ),
    SERIES_BUDGET_2026_27_DEFICIT_STATISTICS: _cite(
        SERIES_BUDGET_2026_27_DEFICIT_STATISTICS,
        CITE_C3_CARD_6,
        producer=MOF_BUDGET,
        artefact_id="BAG table Deficit Statistics; fetch budget_at_a_glance.xlsx sheet Deficit Statistics (printed book bag2.pdf)",
        reference_period="Actuals 2024-2025, BE 2025-2026, RE 2025-2026, BE 2026-2027",
        release_date=BUDGET_LAID,
        url=BAG_URL,
        geography_as_published="Government of India as published",
        frequency="annual budget document",
        licence=MOF_BUDGET_LICENCE,
        caveat_one_line="Use producer labels (FD, RD, ERD, PD) — not a Prism score. Parentheses are % of GDP as printed. Do not ingest other BAG sheets.",
    ),
    SERIES_BUDGET_2026_27_LIABILITIES: _cite(
        SERIES_BUDGET_2026_27_LIABILITIES,
        CITE_C3_CARD_7,
        producer=MOF_BUDGET,
        artefact_id="Annex 1(i); file doc/rec/annex91.pdf. Reconstructed PDF word-to-column; annex91.xlsx 404.",
        reference_period="Outstanding at year-end as labelled, including 1950-51 and RE/BE columns",
        release_date=BUDGET_LAID,
        url=LIABILITIES_URL,
        geography_as_published="Central Government / Government of India as published",
        frequency="annual budget document",
        licence=MOF_BUDGET_LICENCE,
        caveat_one_line="Statement of Liabilities is not FRBM-defined debt. PDF reconstruction (ambiguous=0). Stock, not a year’s deficit.",
    ),
    SERIES_BUDGET_2026_27_FRBM_STATEMENTS: _cite(
        SERIES_BUDGET_2026_27_FRBM_STATEMENTS,
        CITE_C3_CARD_8,
        producer=MOF_BUDGET,
        artefact_id="Combined PDF doc/frbm1.pdf. Named hole: statutory FRBM prose, not a reconstructable receipts/expenditure/deficit/debt grid. frbm2.pdf 404.",
        reference_period="Budget 2026-27 / RE 2025-26 as discussed in the Preface",
        release_date=BUDGET_LAID,
        url=FRBM_URL,
        geography_as_published="Central Government as in the FRBM statements",
        frequency="annual with the Union Budget",
        licence=MOF_BUDGET_LICENCE,
        caveat_one_line="Named hole. Do not print a reconstructed FRBM table. Deficit/debt figures remain on Cards 6–7. Do not turn 3%/40%/60% into a Prism grade.",
    ),
    SERIES_BUDGET_2026_27_AFS: _cite(
        SERIES_BUDGET_2026_27_AFS,
        CITE_C3_CARD_9,
        producer=MOF_BUDGET,
        artefact_id="Constitutional AFS; file doc/AFS/allafs.pdf. Do not ingest allafs.xlsx (stale year headers). PDF reconstruction.",
        reference_period="Statement I columns Actuals 2024-2025, BE 2025-2026, RE 2025-2026, BE 2026-2027",
        release_date=BUDGET_LAID,
        url=AFS_URL,
        geography_as_published="Central Government / Consolidated Fund of India, Contingency Fund, Public Account. UT-without-legislature lines are still Union accounts, not C5.",
        frequency="annual (Article 112)",
        licence=MOF_BUDGET_LICENCE,
        caveat_one_line="PDF of record; companion xlsx is a different year. Estimates net of refunds and recoveries. PDF reconstruction (ambiguous=0).",
    ),
    SERIES_CGA_MONTHLY_GLANCE_2026_07: _cite(
        SERIES_CGA_MONTHLY_GLANCE_2026_07,
        CITE_C3_CARD_10,
        producer=CGA,
        artefact_id="CGA Monthly Accounts month=07 year=2026-2027; DATA2627.htm. HTML table expand, not a spreadsheet.",
        reference_period="April–July 2026 of FY 2026-2027 vs BE 2026-2027",
        release_date="unknown",
        url=CGA_MONTHLY_URL,
        geography_as_published="Government of India / Union Government as printed. Not states, not districts.",
        frequency="monthly during the year",
        licence=CGA_LICENCE,
        caveat_one_line="Actuals are unaudited provisional (@). Fiscal deficit in the monthly file is not necessarily the year-end deficit. HTML reconstruction.",
    ),
    SERIES_CGA_FINANCE_ACCOUNTS_2024_25_STAT1: _cite(
        SERIES_CGA_FINANCE_ACCOUNTS_2024_25_STAT1,
        CITE_C3_CARD_11,
        producer=CGA,
        artefact_id="CGA FinanceReport 2024-2025; Fin20242025Statement1.pdf. PDF reconstruction. CGA remains the accounts publisher.",
        reference_period="financial year 2024-2025 (with 2023-2024 comparatives)",
        release_date="unknown",
        url=CGA_FA_URL,
        geography_as_published="Union Government as printed. Statement 1 annexure proceeds assigned to States is Union tax assignment, not C5.",
        frequency="annual audited-year accounts",
        licence=CGA_LICENCE,
        caveat_one_line="Annual Actuals, not BE/RE. PDF reconstruction (ambiguous=0). Do not silent-substitute monthly accounts.",
    ),
}

C3_GEOGRAPHIES: dict[str, GeographyVintage] = {
    SERIES_BUDGET_2026_27_TAX_REVENUE: FRAME_A_GOI,
    SERIES_BUDGET_2026_27_NON_TAX_REVENUE: FRAME_A_GOI,
    SERIES_BUDGET_2026_27_CAPITAL_RECEIPTS: FRAME_A_GOI,
    SERIES_BUDGET_2026_27_ANNEX1_TRENDS_RECEIPTS: FRAME_A_GOI,
    SERIES_BUDGET_2026_27_EXPENDITURE_STAT1: FRAME_A_HEADS,
    SERIES_BUDGET_2026_27_DEFICIT_STATISTICS: FRAME_A_GOI,
    SERIES_BUDGET_2026_27_LIABILITIES: FRAME_A_CENTRAL,
    SERIES_BUDGET_2026_27_FRBM_STATEMENTS: FRAME_A_CENTRAL,
    SERIES_BUDGET_2026_27_AFS: FRAME_A_CENTRAL,
    SERIES_CGA_MONTHLY_GLANCE_2026_07: FRAME_B_UNION,
    SERIES_CGA_FINANCE_ACCOUNTS_2024_25_STAT1: FRAME_C_UNION,
}


def _note(caveat_id: str, **fields: str) -> CaveatNote:
    return CaveatNote(caveat_id=caveat_id, **fields)


C3_CAVEATS: dict[str, CaveatNote] = {
    SERIES_BUDGET_2026_27_TAX_REVENUE: _note(
        CAVEAT_C3_CARD_1,
        concept="Union tax revenue by major heads as printed in Receipt Budget 2026-27 Part A (I. Tax Revenue). Gross tax is not Centre’s net tax.",
        unit="Rupees as labelled on the statement (typically crore). Blank / dotted cells are not zero.",
        population="Government of India / Union tax receipts as published. Not state tax. Not districts. Not a per-person tax.",
        reference_period="Column label on the cell: Actuals 2024-2025, BE 2025-2026, RE 2025-2026, or BE 2026-2027. Not the 1 February 2026 laying date.",
        producer_definition="Receipt Budget, 2026-2027 — I. Tax Revenue; fetch tr.xlsx sheet ReceiptReport123. Tidy table: openpyxl cells (ingest flag sheet=ReceiptReport123) — not reconstructed from tr.pdf.",
        comparable_from="The four columns in this file. A longer run of receipts lives on Card 4 (net of States’ share) — not this gross-head table.",
        breaks="BE vs RE vs Actuals: four vintages, not one line. Spreadsheet cell map of the same Budget statement — not a PDF scrape. Do not recode onto Frame B or C.",
        lags="Budget laid 1 February 2026. next_release unknown (Budget 2027-28 not dated on these artifacts).",
        disagrees_with="Card 4 tax revenue net of States’ share. Card 9 AFS revenue receipts. Card 10 monthly actuals vs BE. Card 11 Finance Accounts Actuals 2024-25.",
        do_not="Do not collapse BE/RE/Actuals. Do not treat gross tax as Centre’s net tax. Do not add Cards 1–3 into a Prism collections total. Do not chart blank cess as 0. Do not present Union tax as all-India public receipts. Do not rank, forecast, or per-person.",
    ),
    SERIES_BUDGET_2026_27_NON_TAX_REVENUE: _note(
        CAVEAT_C3_CARD_2,
        concept="Union non-tax revenue as printed (II. Non-Tax Revenue), including receipts of Union Territories as a Union head.",
        unit="Rupees as labelled. Blank is not zero.",
        population="Government of India / Union. Receipts of Union Territories here is a Union budget head, not UT Finance Accounts (C5).",
        reference_period="Actuals 2024-2025, BE 2025-2026, RE 2025-2026, BE 2026-2027 as column labels. Not 1 February 2026.",
        producer_definition="Receipt Budget, 2026-2027 — II. Non-Tax Revenue; fetch ntr.xlsx sheet ReceiptReport123. openpyxl cells — not reconstructed from ntr.pdf.",
        comparable_from="The four columns in this file. Card 4 Annex-1 has a Non-Tax Revenue row in its own run — still a different table.",
        breaks="BE vs RE vs Actuals. Do not add to Card 1 as one revenue unless the producer prints that total. Spreadsheet cell map — not a PDF scrape.",
        lags="Same Budget 2026-27 lag as Card 1. next_release unknown.",
        disagrees_with="Card 1 (tax). Card 3 (capital/debt). Card 4 multi-year non-tax row. Cards 9–11.",
        do_not="Do not treat UT receipts on this statement as C5. Do not merge tax and non-tax. Do not rank, forecast, or per-person.",
    ),
    SERIES_BUDGET_2026_27_CAPITAL_RECEIPTS: _note(
        CAVEAT_C3_CARD_3,
        concept="Union capital receipts as printed: Non-Debt Receipts and Debt Receipts / borrowings as labelled.",
        unit="Rupees as labelled. Many debt lines are printed net of repayments.",
        population="Government of India / Union. Not state borrowings.",
        reference_period="Actuals 2024-2025, BE 2025-2026, RE 2025-2026, BE 2026-2027. Not 1 February 2026.",
        producer_definition="Receipt Budget, 2026-2027 — III. Capital Receipts; fetch ctr.xlsx sheet ReceiptReport123. Workbook is ctr.xlsx, not cr.xlsx (404).",
        comparable_from="The four columns in this file. Card 4 Annex-1 capital-receipt rows are a different annex.",
        breaks="BE vs RE vs Actuals. Market loans (net) is not gross market borrowings. Spreadsheet cell map — not a PDF scrape.",
        lags="Same Budget 2026-27 lag. next_release unknown.",
        disagrees_with="Card 7 outstanding liabilities (stock). Card 6 deficit. Cards 10–11.",
        do_not="Do not treat net debt receipts as gross borrowings. Do not use this card as the debt stock (Card 7). Do not chart as C5 state debt.",
    ),
    SERIES_BUDGET_2026_27_ANNEX1_TRENDS_RECEIPTS: _note(
        CAVEAT_C3_CARD_4,
        concept="Multi-year Union receipts table as printed in Receipt Budget Annex-1, including printed deficit lines in the same annex.",
        unit="Rupees as labelled. Deficit lines are the producer’s printed lines, not a Prism blend.",
        population="Government of India as published. Not states.",
        reference_period="Financial-year column on the cell: Actual 2017-18 through 2024-25, RE 2025-26, BE 2026-27 as labelled.",
        producer_definition="Receipt Budget, 2026-2027 — Annex-1 Trends in Receipts (annex1.pdf). PDF word-to-column; ingest flag pdfplumber words; ambiguous=0. annex1.xlsx 404.",
        comparable_from="Columns the producer prints. Do not extend with RBI or IMF. Last two columns are RE and BE, not Actuals.",
        breaks="Reconstructed from PDF, not a spreadsheet cell map. Tax revenue here is net of States’ share — break vs Card 1. Actual vs RE vs BE in one row: never one continuous Actuals line.",
        lags="Same Budget laying. next_release unknown. Reconstruction is not a later release.",
        disagrees_with="Card 1 (gross tax heads). Card 6 BAG Deficit Statistics. Card 11 Actuals 2024-25.",
        do_not="Do not hide PDF reconstruction. Do not guess an ambiguous amount into a year column. Do not name years the file does not contain. Do not chart RE/BE as Actuals.",
    ),
    SERIES_BUDGET_2026_27_EXPENDITURE_STAT1: _note(
        CAVEAT_C3_CARD_5,
        concept="Union expenditure summary as printed: Central Expenditure; Transfers; Total Expenditure through Budget; Resources of Public Enterprises — each split Revenue / Capital / Total where printed.",
        unit="Rupees as labelled.",
        population="Union budget heads. Transfers to States/UTs are Union outgo as printed — not state Finance Accounts.",
        reference_period="Actuals 2024-2025, BE 2025-2026, RE 2025-2026, BE 2026-2027. Not 1 February 2026.",
        producer_definition="Expenditure Profile 2026-2027 — Statement 1; fetch stat1.xlsx sheet Statement1. openpyxl cells. BE 2026-27 Total sits one empty column after Capital.",
        comparable_from="The four year-status columns in this statement.",
        breaks="BE vs RE vs Actuals. Two printed totals (with / without public-enterprise resources): do not swap labels. Spreadsheet cell map — not a PDF scrape.",
        lags="Same Budget 2026-27 lag. next_release unknown.",
        disagrees_with="Card 9 AFS disbursements. Card 10 monthly expenditure vs BE. Card 11 Finance Accounts.",
        do_not="Do not use scheme MIS as this series. Do not treat Transfers as C5. Do not chart the two printed totals as one. Do not issue waste/welfare verdicts.",
    ),
    SERIES_BUDGET_2026_27_DEFICIT_STATISTICS: _note(
        CAVEAT_C3_CARD_6,
        concept="Union deficit statistics as printed: Fiscal Deficit, Revenue Deficit, Effective Revenue Deficit, Primary Deficit, and Sources of Financing Fiscal Deficit. Parentheses are % of GDP as printed.",
        unit="Rupees as labelled, and percent of GDP where the producer prints parentheses.",
        population="Government of India as published.",
        reference_period="Actuals 2024-2025, BE 2025-2026, RE 2025-2026, BE 2026-2027 on the statistics table.",
        producer_definition="Budget at a Glance 2026-2027 — Deficit Statistics; fetch budget_at_a_glance.xlsx sheet Deficit Statistics. Do not ingest other BAG sheets.",
        comparable_from="Columns on this table. Card 4 annex deficit lines are a different printed table. Card 10 monthly fiscal deficit is intra-year unaudited.",
        breaks="BE vs RE vs Actuals. % of GDP uses the Budget’s cited GDP. Spreadsheet cell map — not a PDF scrape.",
        lags="PDF CreationDate 1 February 2026. next_release unknown.",
        disagrees_with="Card 4 printed deficit lines. Card 8 FRBM prose percentages. Card 10 monthly fiscal deficit. Card 11 year-end Actuals.",
        do_not="Do not grade FRBM targets from this table. Do not blend monthly Card 10 into this year-status table. Do not invent one Union money number.",
    ),
    SERIES_BUDGET_2026_27_LIABILITIES: _note(
        CAVEAT_C3_CARD_7,
        concept="Outstanding liabilities of the Central Government as printed: Public Debt; Other Liabilities; Total / Net Liabilities. Stock at year-end, not a year’s deficit.",
        unit="Rupees as labelled. External debt footnote: book value / historical rate as printed.",
        population="Central Government / Government of India. Not state debt.",
        reference_period="Outstanding at year-end as labelled: end of 1950-51; 2021-2022 through 2024-25; Revised 2025-26; Budget 2026-27.",
        producer_definition="Receipt Budget, 2026-2027 — Part B: 1 (i) Statement of Liabilities (annex91.pdf). PDF word-to-column; ambiguous=0.",
        comparable_from="Columns on this statement. 1950-51 is a printed historical column, not a continuous series to splice without the producer’s notes.",
        breaks="Reconstructed from PDF. Two debt concepts: this Statement of Liabilities vs FRBM-defined debt. Revised vs Budget vs year-end Actuals columns.",
        lags="Same Budget laying. next_release unknown.",
        disagrees_with="FRBM-defined debt on BAG charts. Card 3 net debt receipts (flow, not stock). Card 6 deficit.",
        do_not="Do not hide PDF reconstruction. Do not merge FRBM-defined debt into this stock. Do not present Union liabilities as general government including states.",
    ),
    SERIES_BUDGET_2026_27_FRBM_STATEMENTS: _note(
        CAVEAT_C3_CARD_8,
        concept="Statements of Fiscal Policy required under the FRBM Act, 2003, as bound for Budget 2026-27. Named hole: statutory packet, not a reconstructable receipts/expenditure/deficit/debt grid.",
        unit="Not a table. Percent of GDP and other figures remain producer prose. Not a Prism grade against 3% / 40% / 60% wording.",
        population="Central Government as in the FRBM statements.",
        reference_period="Budget 2026-27 / RE 2025-26 as discussed in the Preface. Not a reconstructable year grid.",
        producer_definition="Combined PDF frbm1.pdf. Ingest flag: statutory FRBM prose, not a reconstructable grid; do not ingest page 9 Economic Performance at a Glance as this card. lineage_ok: no.",
        comparable_from="Not comparable as a table. Deficit and debt figures of record remain Cards 6–7.",
        breaks="Not a reconstructable grid. Missing: Macro-Economic Framework; Medium-term Fiscal Policy / Fiscal Policy Strategy; deviation statement; FRBM labels as printed.",
        lags="Presented with Budget 2026-27. next_release unknown.",
        disagrees_with="Cards 6–7 remain the Budget tables of record for deficit and outstanding liabilities. Do not merge.",
        do_not="Do not print a fake FRBM table. Do not ingest page 9 Economic Performance at a Glance as this card. Do not turn 3% / 40% / 60% into a Prism grade.",
    ),
    SERIES_BUDGET_2026_27_AFS: _note(
        CAVEAT_C3_CARD_9,
        concept="Annual Financial Statement of the Central Government for 2026-2027 as laid: Consolidated Fund, Contingency Fund, Public Account.",
        unit="Rupees as labelled. Estimates are net of refunds and recoveries (Key to Budget Documents).",
        population="Central Government / Consolidated Fund of India, Contingency Fund, Public Account. UT-without-legislature AFS lines are still Union accounts, not C5.",
        reference_period="Statement I columns Actuals 2024-2025, BE 2025-2026, RE 2025-2026, BE 2026-2027.",
        producer_definition="AFS allafs.pdf. PDF word-to-column; ambiguous=0. allafs.xlsx headers are a different year — do not ingest as this vintage.",
        comparable_from="Columns on Statement I of this PDF.",
        breaks="Reconstructed from PDF, not a spreadsheet cell map. BE vs RE vs Actuals. Do not ingest the stale companion xlsx.",
        lags="Cover New Delhi, February 1, 2026. next_release unknown.",
        disagrees_with="Cards 1–5 Receipt/Expenditure statements (same Budget family, different books). Card 11 Finance Accounts Actuals.",
        do_not="Do not hide PDF reconstruction. Do not ingest allafs.xlsx as 2026-27. Do not treat UT-without-legislature AFS lines as C5.",
    ),
    SERIES_CGA_MONTHLY_GLANCE_2026_07: _note(
        CAVEAT_C3_CARD_10,
        concept="Union Government Accounts at a Glance as at the end of July 2026: intra-year unaudited provisional actuals versus Budget Estimates 2026-2027.",
        unit="Rupees as labelled, and percent of BE where printed. @ marks unaudited provisional.",
        population="Government of India / Union Government as printed. Not states, not districts.",
        reference_period="April–July 2026 of FY 2026-2027 vs BE 2026-2027. Not a year-end actual.",
        producer_definition="DATA2627.htm. HTML table 0; colspan/rowspan expanded. Not a spreadsheet export (xlsx 404).",
        comparable_from="This month’s glance table. Prior months in the same FY are different source_vintages.",
        breaks="HTML reconstruction. Actuals are @ unaudited. Fiscal deficit here is not necessarily the year-end deficit. Do not recode onto Frame A.",
        lags="News dated 1 September 2026 for upto July 2026. next_release unknown.",
        disagrees_with="Card 6 year-status deficit. Card 11 Finance Accounts Actuals. Budget BE 2026-27 on Cards 1–9.",
        do_not="Do not hide HTML reconstruction. Do not annualise April–July as a year-end actual. Do not replace @ actuals with Budget Actuals. Do not use www.cga.gov.in.",
    ),
    SERIES_CGA_FINANCE_ACCOUNTS_2024_25_STAT1: _note(
        CAVEAT_C3_CARD_11,
        concept="Union Finance Accounts 2024-2025 No. 1 Summary of Transactions: receipts and disbursements, Actuals, with 2023-2024 comparatives.",
        unit="Crores of rupees as printed.",
        population="Union Government as printed. Annexure proceeds assigned to States is Union tax assignment, not C5.",
        reference_period="Financial year 2024-2025 (with 2023-2024 comparatives). Annual Actuals, not BE/RE.",
        producer_definition="Fin20242025Statement1.pdf. PDF word-to-column; ambiguous=0. Ingest drops 1–2 digit column-index rows; they are not crores.",
        comparable_from="The two Actuals columns on Statement No. 1.",
        breaks="Reconstructed from PDF. Annual Actuals, not Budget BE/RE. Do not recode the States annexure into C5.",
        lags="PDF CreationDate 20 December 2025. Finance Accounts 2025-26 not on the CGA dropdown as of 18 September 2026.",
        disagrees_with="Budget printed Actuals 2024-25 (Card 1–9). Card 10 monthly actuals.",
        do_not="Do not hide PDF reconstruction. Do not treat 1–2 digit column-index rows as crores. Do not silent-substitute this file for monthly accounts or Budget BE.",
    ),
}
