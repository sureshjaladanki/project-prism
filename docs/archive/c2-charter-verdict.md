# C2 charter verdict

Charter Editor after Trust Auditor (**pass**, [Trust Auditor](1d8bbfab-8c17-45e8-b278-cff46c501c3c)). Preview was `data/pointers/preview` → `dv-20260919-87b702f1fd66`. C2 in/out/source_class unchanged. This is **not** a ship of the published pointer.

```text
slice:          How many people live in India, where, and how is that changing?
in:             Census population at national and state/UT as published; Sample Registration System births, deaths, infant mortality, fertility as published; official NCP/MoHFW Table 8 projection as itself. Fetch from official government agencies that can source that dependency (producing office first preference, not the only host). Quote producer, series, date, and fetch source in the sources of the page view.
out:            treating 2011 as current without saying so; a blended “India today” figure; NPR / citizenship registers; electoral rolls; caste politics; district tables (parked); World Bank / UN as source of record; NITI scorecards as the record
source_class:   allow — requirement → producing office → official government fetch (producer first, any government office that can source the dependency) → cite on the page
next_persona:   platform-architect
block_reason:   Honour Trust on the record: the C2 preview is inside the vision. Do not flip citizen_pointer. A C2 vintage tree does not include C1 (`prices/retail-prices`). Publishing this vintage as citizen would unpublish the shipped C1 slice. Keep citizen on dv-20260916-234e263c8588. Intended holes remain (no later census total; Frame A/B 2011 map; Frame D smaller States/UTs; districts parked). Platform names how more than one slice shares a published pointer before any C2 citizen ship.
```

## Decision

**Keep C2 on preview. Do not unpublish C1.**

Trust passed the bound page: three records stay separate; lag and holes are stated; official ORGI and NCP/MoHFW cards only.

Citizen HTTP still reads only `dv-20260916-234e263c8588`. Render for C2 is `data/renders/dv-20260919-87b702f1fd66/` (`/people/population`). UI/UX Developer does not flip `citizen_pointer` in this close.

## Next

Platform Architect: two CMS modes are named. Preview binds every complete slice; citizen-view lists only slices on `citizen_pointer` (C1 today). Do not start C4–C20 in this close. Do not recode geography frames. Do not pull district files.
