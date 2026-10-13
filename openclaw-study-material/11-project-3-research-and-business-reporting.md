# Chapter 11 — Project 3: Research, Business-Reporting & Marketing Agent
*Course project: Technical research, business reporting & marketing automation · Time: ~2 hrs + Lab 11 (90 min)*

## What "done" looks like
You ask on Telegram: *"Research: should our 5-person startup use Azure or GCP for a customer-data workload in India? Budget-sensitive, compliance-aware. Report by evening."* By evening: a structured, sourced report in your workspace — options, comparison table, costs with assumptions stated, risks, recommendation with confidence level — plus a 5-line executive summary on Telegram. Not a blob of chat text: a *document*.

## 11.1 The research pattern (teach it once, reuse everywhere)
```
1. CLARIFY   restate the question; list sub-questions; state assumptions
2. PLAN      sources per sub-question (docs > analysts > blogs); note search phrases
3. GATHER    search + fetch; save source notes (URL, date, key claims) to workspace file FIRST
4. SYNTHESISE cross-check claims (2 sources for anything load-bearing); flag disagreements
5. REPORT    fixed structure (below); every key claim cited; unknowns labelled UNKNOWN
6. DELIVER   summary on channel; full report as file in workspace/reports/
```
Saving source notes to a file *before* writing is the step novices skip and professionals don't: it makes the work auditable, resumable across sessions, and cheaper (no re-fetching).

**Report skeleton (from `templates/skills/research-report/SKILL.md`):**
```markdown
# <Question> — <date>
## Executive summary (5 lines max)
## Method & sources (counts, types, dates)
## Findings (per sub-question, cited)
## Comparison table (if options)
## Costs & assumptions (explicit!)
## Risks & unknowns
## Recommendation (with confidence: low/med/high + what would change it)
## Sources
```

## 11.2 Business & marketing variants (same engine, different payload)
- **Weekly business report cron:** Fri 17:00 — reads the week's memory notes + any metrics files you drop in workspace (CSV exports), produces "wins / numbers / blockers / next week" for your manager or clients. Human reviews before sending. Always.
- **Marketing assistant:** content calendar drafts from your briefs, post drafts in *your* SOUL-defined voice, competitor-post roundup. Guardrail: drafts only, human posts — brand voice + platform rules demand a human click.
- **Meeting prep on demand:** "prep me for <company/person>" → research skill scoped narrow, 1-page output, 30-min cron-before-calendar as the advanced move (heartbeat checking calendar — Ch 8 pattern again).

## 11.3 🧪 Lab 11 — A report you'd actually forward (90 min)
1. Install/adapt the `research-report` skill; create `workspace/reports/`.
2. Ask a *real* question you care about (tool choice, market, course-vs-course — real stakes expose fake rigour).
3. Watch the method: confirm a sources file appears in the workspace *before* the final report. If the agent jumps to writing, your skill's step order needs teeth ("Do not draft until sources file exists").
4. Grade the output against the skeleton: Are costs' assumptions explicit? Are unknowns labelled? Is confidence stated? Interview it: *"Which claim has only one source?"* — then fix the skill, not just the report.
5. Schedule ONE recurring report (business weekly or research radar) via cron with delivery = summary + file path.
**✅ Complete when:** you'd forward the report to a colleague with only light edits, and every load-bearing claim clicks through to a source.

## 11.4 Cost & quality levers
- Strong model for synthesis, cheap model for gathering cron pre-work.
- Cap sources (e.g. 8–12) — unbounded research is unbounded billing.
- Cache via files: source notes mean next week's update only fetches *new* material.

## ⚠️ Failure gallery
| Failure | Fix |
|---|---|
| Confident, uncited claims | Skill: "no citation = label UNKNOWN or delete" |
| Both-sides mush, no recommendation | Require recommendation + confidence + reversal condition |
| Report lives only in chat, lost | Deliverable = workspace file; chat gets summary + path |
| Stale pricing presented as fact | Date-stamp every cost; "verify before acting" footer |

## 🎯 Self-check
1. The professional step novices skip? → *Saving sourced notes to a file before synthesising.*
2. Every recommendation needs which trio? → *Confidence level, assumptions, what-would-change-it.*
3. Marketing agent's bright line? → *Drafts, human sends.*

**→ Next: [Chapter 12 — Project 4: Ubuntu Sysadmin & VM-Readiness Agent](12-project-4-ubuntu-sysadmin-vm-readiness.md)**
