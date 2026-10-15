# NY browser-lane brief — NY Department of State, Division of Corporations (read-only)

**When to run this:** only AFTER the API lane
(`bin/lanes/nydos.py`, dataset n9v6-gdp6) has been tried. The API lane covers
all *active* NY entities and is fast, free, and current (verified live
2026-09-20: 4.28M rows, dataset refreshed the same day). Escalate to this
browser lane when the API returns `no_record` for an entity you believe exists
in NY (it may be inactive, suspended, or dissolved — the dataset holds active
entities only), when you need **assumed-name (DBA) certificate** details, or
when the API lane errored.

**Also fine to use this lane for for-profit corporations** — the official
database covers business corporations, LLCs, LPs, LLPs, and not-for-profits
alike. (For nonprofits, keep the separate IRS TEOS lane in the skill's Lane B.)

**Read-only.** Nothing is submitted, created, paid, or changed. The NY DOS
site itself warns the system "should not be used to determine the
acceptability of an Entity Name" — use it only for status/record verification.
If a CAPTCHA appears, park and hand back — never route around it.

## Official entry points

- Search app: https://apps.dos.ny.gov/publicInquiry/
- Instructions page (fallback): https://dos.ny.gov/corporation-and-business-entity-search-database

## Step-by-step procedure

1. **Open** the search app. The search form has these controls:
   - **Search By** (dropdown): choose `Entity Name`, `DOS ID`, or `Assumed Name`.
   - **Search value**: the name or ID being searched.
   - **Entity Status** filter (dropdown): `Active`, `Inactive`, `Suspended`, or
     `All statuses` — default is NOT all, so for a no_record escalations use
     `All statuses`.
   - **Search Functionality** (dropdown, name searches only): match mode —
     `Begins With`, `Contains`, or `Base Words`. Start with `Begins With` on
     the legal name's first distinctive words; widen to `Contains` if needed.
   - **Entity List**: the entity-type filter (corporation, LLC, limited
     partnership, LLP, etc.). Select the type you believe the entity was filed
     as; if unsure, run once per plausible type or leave broad if allowed.
2. **Click "Search the Database."**
3. **Read the results table.** Columns: Name, DOS ID#, Assumed Name ID #,
   Status, Entity Type, Date of First Filing, County.
   - If several rows resemble the target, click each candidate's **name** to
     open its detail page — never assume the first row is the entity.
   - A DOS ID known from prior work (or from the API lane) is the
     disambiguator; search `DOS ID` directly when you have it.
4. **On the entity detail page, record every field shown:**
   - Current entity name; DOS ID #; current entity status (Active / Inactive /
     Suspended / Dissolved, etc.); entity type; initial DOS filing date;
     county; jurisdiction (domestic vs foreign).
   - **DOS process address** (address to which DOS mails process accepted on
     the entity's behalf — the NY equivalent of a registered-agent address
     for many entities).
   - **Registered agent** name and address, if shown. Note: NY does not
     require or maintain member/manager info for nonprofessional LLCs — do
     not report its absence as a gap.
   - Any **assumed names** listed with their Assumed Name ID #s.
   - Officers/directors/chairman with addresses, if shown (the open-data
     extract carries a `chairman_*` block; confirm on the detail page).
5. **Assumed-name (DBA) certificate search** (when asked for a DBA):
   - The Corporation and Business Entity Database explicitly includes assumed
     name filings for corporations, LLCs, and limited partnerships.
   - Set **Search By = Assumed Name** and search the assumed name (use the
     same match-mode progression as step 1); an Assumed Name ID can be
     searched directly if one is known from a prior results table.
   - Record: assumed name, Assumed Name ID #, the parent entity name and its
     DOS ID, filing date if shown.
6. **For an API-lane `no_record` escalation**, also note the entity status
   returned — if it appears as Inactive/Suspended/Dissolved, the API lane's
   `no_record` is explained by dataset coverage, not by the entity never
   existing. Report the status exactly as shown.

## Hand back

A per-entity record with: legal name, DOS ID, assumed-name ID(s) if any,
status, entity type, initial DOS filing date, county, jurisdiction, DOS
process address, registered agent (or "none shown"), officers/chairman if
shown — plus the **source URL of each detail page** and the search mode used
to find it. If nothing matches under All statuses, report that explicitly
(never as a denial of existence beyond the database).

## Fallback cascade

1. **API lane** — `python3 bin/lanes/nydos.py <DOS_ID|NAME>` (active entities,
   settled 2026-09-20).
2. **This browser brief** — inactive/dissolved entities, assumed-name (DBA)
   certificates, API error.
3. **Park-and-document** — if the search app is unreachable or gated (CAPTCHA,
   outage), record the attempt with timestamp + URL and park; do not invent a
   status.
