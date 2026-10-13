# Chapter 14 — Advanced: Sub-Agents, Multi-Agent Design & Scaling Your Automations
*Beyond-core course extension: multi-agent systems, APIs & messaging platforms at scale · Time: ~2 hrs*

## Learning objectives
- Spawn **sub-agents** for parallel work and know when parallelism helps (and when it's just parallel billing).
- Design a **multi-agent** setup on one Gateway: separate agents, workspaces, models, channels.
- Compose the four course projects into one personal automation *system*.
- Decide what *not* to automate — the most advanced skill in this book.

---

## 14.1 Sub-agents — delegation inside one conversation
A sub-agent is a temporary worker your main agent spawns for a bounded task ("research these 3 companies in parallel, report back"), after which the main agent synthesises. Config hints at the shape: `agents.defaults.subagents.maxConcurrent` (e.g. 8) and `maxConcurrent` for the main lane.

**Parallelism pays when:** tasks are independent (3 company dossiers), latency matters, and synthesis is cheap relative to gathering. **It wastes when:** tasks share context heavily, or the "research" is one quick search dressed as a programme. Rule: if you can't write each sub-task as a self-sufficient payload (Ch 8 rule returns), you're not ready to parallelise it.

**Worked pattern — the research fan-out:**
```
You: "Compare these 4 CRMs for a 10-person team."
Main agent: writes 4 sub-tasks (same skeleton: pricing/10 users, India support, API, migration)
  ├─ sub-agent A → CRM-1 dossier (file)
  ├─ sub-agent B → CRM-2 dossier (file)     (parallel)
  ├─ sub-agent C → CRM-3 dossier (file)
  └─ sub-agent D → CRM-4 dossier (file)
Main agent: reads 4 files → comparison table → recommendation (Ch 11 report skill)
```
Files as the hand-off medium (not chat) — auditable, resumable, cheap to re-synthesise. Note the cap discipline: maxConcurrent exists so enthusiasm doesn't become a fork-bomb of API calls.

## 14.2 Multi-agent on one Gateway — separate colleagues, separate desks
Grow from one agent when *trust boundaries or personalities* diverge:

| Agent | Workspace | Model | Channels | Tools | Why separate |
|---|---|---|---|---|---|
| `main` (assistant) | personal ws | strong | Telegram/WhatsApp (you only) | broad-ish, memory | Your chief of staff |
| `sysadmin` | ops ws | mid | Telegram (you only) | exec (read-first), files | Crown-jewel isolation (Ch 12) |
| `researcher` | research ws | strong | web chat / on demand | search/fetch/files | No channel exposure needed |
| `family`/`team` (later) | shared ws | cheap | group w/ mentions | narrow, no MEMORY.md of main | Other people never touch your private context |

Configured via `agents.entries` + per-agent workspace/model overrides and channel routing in `openclaw.json`; each workspace gets its own AGENTS/SOUL/USER files. **Design law:** separation is for *safety and context hygiene*, not novelty — one well-run agent beats four neglected ones.

## 14.3 Composition — your four projects as one system
```
        ┌──────────── 07:30 Sysadmin readiness (Ch 12) ──► Telegram (only on ⚠️ detail)
        ├──────────── 08:00 News brief (Ch 10) ──────────► Telegram
  YOU ◄─┤              Mon/Wed/Fri 09:00 Job shortlist (Ch 9) ► Telegram
        ├──────────── Fri 17:00 Business/research report (Ch 11) ► summary + file
        └──────────── Heartbeat (Ch 8): silent unless thresholds trip
```
Add on-demand: research fan-outs (§14.1), meeting prep, "note this" capture (Ch 7 skill). This is the *Automation Stack* the course title promises — notice it's ~80% the discipline of earlier chapters (payloads, guardrails, silence conditions) and ~20% new tech. That's true of most real systems, honestly.

## 14.4 Connecting more of your world (APIs, platforms, beyond the course)
- **Google Workspace / productivity suites** arrive as skills/plugins (docs, sheets, calendar patterns) — vet per Ch 13, scope permissions narrowly, calendar access is what makes heartbeat reminders genuinely useful.
- **Voice** (where supported): voice notes in/out turn the Telegram agent into something you use while walking — configure per current docs; keep transcripts to memory notes.
- **Browser automation** handles the sites without APIs (job boards, portals) — powerful and brittle; prefer feeds/APIs, use browser skills with approval on any submission.
- **Webhooks/API triggers:** scheduled + message triggers cover most needs; event-driven (CI failures pinging the sysadmin agent) is the natural next step for DevOps readers — same detect→report→approve pattern, new doorbell.

## 14.5 The advanced judgement chapter (short, career-long)
Automate the **frequent, the checkable, and the boring**. Keep humans on the **irreversible, the interpersonal, and the accountable**. Every automation proposal should answer: How will I know it failed? What does it cost per week? What breaks if it lies confidently? If those answers are crisp, build it; if fuzzy, it's a demo, not a system.

## ✅ Checkpoint / Advanced exercise
Design (on paper in your journal, build if ready) one fan-out: a 3-way parallel research with file hand-offs. State maxConcurrent, per-agent model choice, synthesis step, and weekly cost estimate. If any field is blank, the design isn't done.

## 🎯 Self-check
1. Hand-off medium for sub-agents? → *Files, not chat.*
2. When is a second agent justified? → *Different trust boundary, personality, or audience — not boredom.*
3. Automation-worthy = ___ + ___ + ___? → *Frequent, checkable, boring.*

**→ Next: [Chapter 15 — Troubleshooting, FAQ, Capstone & Interview Prep](15-troubleshooting-capstone.md)**
