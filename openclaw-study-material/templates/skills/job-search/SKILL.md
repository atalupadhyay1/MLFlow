---
name: job-search
description: Use when the user asks to search jobs, find roles, run the job scan, or when the scheduled job-search fires. Searches listings against USER.md criteria, dedupes against the job log, and delivers a short reasoned shortlist. Shortlist only — never auto-apply.
---

# Job Search

## Inputs
- Criteria: USER.md "Job search" block (titles, must-haves, deal-breakers, sources). If missing, ask once and save answers there.
- Dedupe memory: memory/job-search-log.md (create if absent).

## Steps
1. Build 3–5 search queries from target titles + must-haves.
2. web_search, then web_fetch each promising posting (max ~12 fetched/run).
3. Extract: title, company, location, salary (only if stated), must-haves, URL.
4. Skip any URL already in the job log. Score the rest vs criteria.
5. Append EVERY fetched posting to the log: `YYYY-MM-DD | verdict(shortlist/reject: reason) | title | company | URL`.
6. Deliver top 5 max:
   `🎯 <Title> — <Company> (<location>)` / `Why you: <one line vs USER.md skills>` / `Watch: <one honest gap>` / `<URL>`
7. Zero matches → exactly: `No new matching roles today. <n> scanned, log updated.`

## Guardrails
- NEVER submit applications, forms, or messages to recruiters.
- Never invent salary, requirements, or deadlines. Unverifiable → list link + "details unverified".
- Respect source sites' terms; prefer official career pages/APIs/feeds where listed in USER.md.
