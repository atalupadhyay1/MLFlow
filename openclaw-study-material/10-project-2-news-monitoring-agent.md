# Chapter 10 — Project 2: The News-Monitoring & Daily Briefing Agent
*Course project: Daily news monitoring, research & reporting · Time: ~90 min + Lab 10 (75 min)*

## What "done" looks like
08:00. Telegram: **"☀️ Your brief — AI infra: [3 items]. Cloud policy: [2]. Nothing new in: startups."** Each item: one-line summary + why it matters *to you* + link. Under 200 words. You are informed before your first meeting without opening six apps. On quiet days: one line. The agent respects your attention like a good chief of staff.

## 10.1 Design decisions that make-or-break briefs
1. **Topics are a USER.md contract:** 3–5 topics, each with 2–3 search phrases and "ignore" terms. More topics = shallower brief = deleted unread by week two.
2. **Freshness window:** last 24h (48h Mondays). Enforced in the skill's search instructions, verified by fetched page dates where available.
3. **Dedupe across days:** yesterday's brief headlines are stored in the daily memory note; the skill checks before including. (Same pattern as Ch 9 — notice the reuse.)
4. **"Why it matters" line:** generic summaries are RSS with extra steps. Forced relevance ("relates to your Azure migration project in USER.md") is the entire value.
5. **Source hygiene:** prefer primary sources (official blogs, regulators, papers) over content farms; never summarise what wasn't fetched; link everything.

## 10.2 Reuse & extend the Chapter 7 skill
Ch 7's `daily-brief` becomes production here: add topic blocks from `templates/skills/daily-brief/SKILL.md`, the dedupe step, the relevance line, and the quiet-day rule. Set the Ch 8 cron (`0 8 * * 1-5` weekdays — adjust to your life), cheap/fast model if your setup allows per-job models, delivery to Telegram.

## 10.3 🧪 Lab 10 — Ship your 8 AM chief of staff (75 min)
1. Write topics into USER.md (3 max for the lab). Include one "ignore" term per topic.
2. Finalise the brief skill (merge template upgrades), restart, test on demand in Telegram.
3. **Adversarial check:** ask afterwards, *"Did any item repeat from yesterday's brief? Show me your sources."* Inspect: every claim must trace to a fetched URL. Delete/tighten any step that summarised from search snippets alone.
4. Add a "weekly themes" cron (Sun 19:00): reads the week's daily notes, outputs 5 bullets — patterns, not headlines. (This one impresses people disproportionately.)
5. Schedule the weekday brief; manually fire once from cron; check phone delivery & length with a stopwatch mindset: could you read it in 90 seconds?
**✅ Complete when:** 3 consecutive test briefs contain zero repeats, zero unverifiable claims, and each item earns its "why it matters" line.

## 10.4 Variants the course gestures at (build one as homework)
- **Competitor watcher:** topics = competitor names; Friday digest of launches/pricing.
- **Research radar:** arXiv/paper queries weekly; "one paper worth your Saturday" format.
- **Policy/regulatory monitor:** official gazette/regulator sources only; alert-immediately on keyword hit (heartbeat candidate, strict silence otherwise).
- **Multilingual brief:** sources in two languages, brief in yours — models are good at this; keep the link-everything rule.

## 10.5 Failure gallery
| Failure | Fix |
|---|---|
| Brief = search snippets, shallow | Force fetch-before-summarise in skill |
| Same story, 4 outlets | Dedupe by *event*, not URL (skill instruction) |
| "Huge if true" rumours included | Source tiering: primary > reputable > aggregator(never alone) |
| You stopped reading by day 4 | Too long/too many topics. Cut ruthlessly. Attention is the KPI |

## 🎯 Self-check
1. The two anti-noise mechanisms? → *Dedupe vs memory notes; quiet-day one-liner.*
2. Why fetch full pages when snippets exist? → *Snippets invite hallucination; fetched text is evidence.*
3. The brief's real KPI? → *Still read on day 10.*

**→ Next: [Chapter 11 — Project 3: Research, Business Reporting & Marketing Agent](11-project-3-research-and-business-reporting.md)**
