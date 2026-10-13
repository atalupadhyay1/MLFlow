# Chapter 9 — Project 1: The Job-Search Agent
*Course project: Automating job searches & repetitive online tasks · Time: ~2 hrs + Lab 9 (90 min)*
*Needs: Ch 5 (Telegram), 6 (USER.md), 7 (skills), 8 (cron) all done. This is where the stack clicks.*

## What "done" looks like
Every morning (or twice weekly), your phone buzzes: *"3 new roles match you: [title, company, why-you-fit in one line, link]. 11 scanned, 8 rejected (reasons logged)."* You tap a link. That's it. No portals, no doom-scrolling, no FOMO.

## 9.1 Design before building (the professional order)
**1. Define the target (in USER.md — the agent reads it every run):**
```markdown
## Job search (for agents)
- Target titles: DevOps Engineer, Cloud Engineer (not: helpdesk, sales)
- Must-haves: remote or Bengaluru hybrid; Linux + AWS/Azure; ₹/salary band if listed
- Nice: Kubernetes, Terraform. Deal-breakers: on-call without pay note, 6-day weeks
- Sources: company career pages I list + web search. Apply: NEVER auto-apply — shortlist only.
```
That last line is ethics *and* design: agents shortlist, humans apply. Auto-applying with a hallucinating agent is how you get rejected by a robot for a job you never saw.

**2. Workflow (the skill we'll write):**
```
fetch/search sources → dedupe vs memory/job-search-log.md → score vs criteria →
reject with reason (log it — auditable!) → shortlist top 5 → format → deliver (Telegram)
```
**3. Cadence:** cron Mon/Wed/Fri 09:00 beats daily for most job boards (less noise, same coverage).

## 9.2 The skill (adapt `templates/skills/job-search/SKILL.md`)
Key instructions it encodes: read criteria from USER.md; search queries per title; fetch postings; extract title/company/location/salary/must-haves; compare line-by-line; maintain `memory/job-search-log.md` (seen URLs + verdict + date — your dedupe memory); output format strictly:
```
🎯 <Title> — <Company> (<location>)
Why you: <one line tied to USER.md skills>
Watch: <one risk/gap, honestly>
<URL>
```
Guardrails: never invent salary/requirements; if fetch fails, list link with "couldn't verify details"; max 5; if zero matches, the Ch 8 quiet-line.

## 9.3 🧪 Lab 9 — Build & run it (90 min)
1. Add the "Job search" block to `USER.md` with *your* real criteria (15 min — vagueness here = garbage forever).
2. Install the template skill into `workspace/skills/job-search/`, restart Gateway.
3. Dry run in Telegram: *"Run job search now, sources: web search only."* Watch logs: searches → fetches → shortlist. **Interrogate the rejects:** ask "why did you reject role X?" — a good skill answers from its log. (20 min + fixes)
4. Inspect `memory/job-search-log.md`; confirm URLs recorded. Run again immediately: **✅ dedupe check — no repeats.**
5. Fix your top frustration by editing the *skill* (not by arguing in chat) — e.g. tighten title matching. Restart, rerun. This edit-test loop is the real skill being taught.
6. Schedule the cron job (template in `templates/configs/cron-jobs.example.json`); delivery to Telegram; manual-trigger once from cron to prove the scheduled path, not just chat path.
**✅ Lab complete when:** two consecutive runs give zero duplicates, rejects have reasons, and the shortlist format is stable enough to read half-asleep.

## 9.4 Quality upgrades (pick after core works)
- **Scoring transparency:** append `Score: 8/10 (missing: Terraform depth)` — teaches you your own gaps over weeks.
- **Company-page watching:** add 5 dream-company career pages to sources; fetch beats search for these.
- **Weekly digest mode:** daily silent logging + Friday summary cron. Noise ↓, signal ↑.
- **Interview-prep hook:** replying "prep <company>" triggers Ch 11's research skill scoped to that company. Projects compose — that's the stack mindset.

## 9.5 Ethics & platform rules (read, genuinely)
Respect sites' terms/robots, rate-limit fetches, prefer official APIs/feeds where offered, never auto-submit applications or mass-message recruiters, and keep a human as the applicant of record. A shortlist agent is a research assistant; keep it one.

## ⚠️ Failure gallery
| Failure | Root cause | Fix location |
|---|---|---|
| Same jobs daily | Log not written/read | skill steps (memory file) |
| Irrelevant titles | USER.md criteria mushy | USER.md, not chat complaints |
| Hallucinated salaries | Fetch skipped, model guessed | guardrail: "link-only if unverified" |
| 40-item dumps | No cap/ranking | skill output rules (max 5) |

## 🎯 Self-check
1. Why must the agent never auto-apply? → *Accuracy, consent, platform rules — human stays applicant.*
2. Dedupe lives in ___ not ___? → *Memory file, not chat history.*
3. First fix when results are irrelevant? → *Sharpen USER.md criteria.*

**→ Next: [Chapter 10 — Project 2: News-Monitoring & Daily Briefing Agent](10-project-2-news-monitoring-agent.md)**
