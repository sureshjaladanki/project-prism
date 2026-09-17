# Product

A civic **CMS** for the portrait in [vision.md](vision.md). Not a folder of static pages. Not a live scrape of ministry sites.

- **Template** — Portrait Editor’s copy and chart spec, with slots that only accept cited observations.
- **Data vintage** — an immutable snapshot of observations, citations, geography, and caveats after one pipeline run. That is **data-in-time**: the page is true as of that vintage.
- **Render** — `template + vintage → page`. Same inputs, same page.
- **Refresh** — when an official source updates, or an editor asks, Ingest lands the new artifact, Pipeline writes a **new** vintage, CMS re-renders, Platform publishes. Periodic or on-demand. Citizen-view moves only to a complete published vintage.

Do not hand-author a citizen page of numbers. Do not fetch a producer website at request time to fill a chart.

The machine is [architectural-blueprint.md](architectural-blueprint.md). Landing official files is [ingestion-blueprint.md](ingestion-blueprint.md). Who does the work is [team.md](team.md).
