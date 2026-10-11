# Claude Code Full Course — Complete Study Pack

Study material for the YouTube course **"CLAUDE CODE FULL COURSE 12 HOURS: Build Real AI Projects (2026)"** by **Mayank Aggarwal** (`@tech.mayankagg`).

| | |
|---|---|
| **Video** | <https://www.youtube.com/watch?v=05aY2LRIC3s> |
| **Length** | 13:53:46 (~14 hours, 13 modules + capstone) |
| **Published** | 3 May 2026 |
| **Course landing page (from the video)** | <https://claude-code-with-mayank.netlify.app> |
| **Course resources repo (from the video)** | <https://github.com/mayank953/Youtube/tree/main/Claude%20Code%20Crash%20Course> |
| **Level** | Beginner → Advanced; explicitly built for technical **and** non-technical people |

> **Note on version drift.** This course was recorded in early-to-mid 2026 and quotes model names, prices, limits, and command names current at that time (e.g. Haiku 4.5 / Sonnet 4.6 / Opus 4.7, Claude Routines, agent teams, plugin marketplaces). Treat those as *illustrations of a concept*, not permanent facts — the underlying ideas (context, hooks, MCP, subagents, CLAUDE.md) change far more slowly than the version numbers. Always re-check the official docs before relying on a specific price or flag.

---

## What's in this pack

| File | What it is | Best used for |
|---|---|---|
| `README.md` | This file: video map, study plans, how the pieces fit | Orientation |
| `01-study-guide.md` | **Core document.** Module-by-module guide (13 modules) with concepts, demos, configs, gotchas, and self-check questions | First read-through + revision |
| `02-cheatsheet.md` | One-page-per-topic quick reference: commands, modes, files, hooks, scheduling, templates | Daily use, during practice |
| `03-glossary.md` | Plain-English definitions of every term the course uses | When a word blocks you |
| `04-flashcards.md` | ~75 question/answer cards | Spaced repetition, commute review |
| `05-quiz-and-answers.md` | 20 multiple-choice + 10 short-answer questions with full answer key | Self-testing before/after watching |
| `06-labs.md` | 12 hands-on labs (one per module) + the DailyPulse capstone build plan | Actually learning it |
| `study-hub.html` | Interactive single-file study hub (tabs, flip cards, quiz reveal) | Browser-based revision |

**How to use it with the video:** skim the relevant module in `01-study-guide.md` *before* watching that chapter (so you know what to look for), watch at 1.25–1.5×, then do the matching lab in `06-labs.md` on your own machine, then self-test with the flashcards/quiz a day later.

---

## The one mental model the whole course hangs on

1. **Claude (chat/web/desktop) is a brain.** It can reason and answer. It cannot touch your machine.
2. **Claude Code is that same brain with hands.** The "hands" are your terminal: creating, editing, and deleting files and running commands — always asking permission unless you change the mode.
3. **The agentic loop is how the brain uses the hands:** ask → think/plan → act → observe result → check → retry or answer. Not magic — fast iteration.
4. **Context is the scarce resource.** Every single message re-sends the entire conversation plus system prompt, tools, MCP definitions, skills, and CLAUDE.md. This causes cost, limits, and "context rot".
5. **Everything else in the course is a lever on that model:** CLAUDE.md (permanent memory), skills (reusable procedures), hooks (zero-token automation), MCP (connections to the outside world), subagents (isolated cheap workers), agent teams (parallel instances), plugins (bundles), scheduling (work without you).

If you can explain points 1–4 to someone else, you understand the course. Everything in modules 3–12 is a lever; module 13 pulls them all.

---

## Full chapter map (timestamps from the video description)

| # | Module | Timestamp | In this pack |
|---|---|---|---|
| 1 | Introduction, Anthropic vs OpenAI, model family, desktop vs Code, terminal, **agentic loop** | 0:00:00 | Study Guide §1 |
| 2 | Installation & setup (Mac/Linux/Windows), API key auth, third-party platforms, VS Code/IDEs | 0:33:08 | Study Guide §2 |
| 3 | Slash commands (70+), /cost, /compact, /clear, permission modes, the `.claude` folder | 1:22:17 | Study Guide §3 |
| 4 | CLAUDE.md — why it's the most important file, hierarchy, what belongs | 2:58:27 | Study Guide §4 |
| 5 | Context management — context window, context rot, token budgeting | 3:43:48 | Study Guide §5 |
| 6 | Skills — reusable playbooks, anatomy, Skills 2.0 / skill creator | 4:31:35 | Study Guide §6 |
| 7 | Hooks — zero-token background automation, event reference, guardrails | 5:40:13 | Study Guide §7 |
| 8 | MCP — connectors vs MCP, Gmail/Tavily demos, local vs hosted, custom server | 6:49:12 | Study Guide §8 |
| 9 | Subagents — isolated specialists, parallelism, /agents | 8:20:17 | Study Guide §9 |
| 10 | Agent teams — multiple Claude instances coordinating | 9:51:44 | Study Guide §10 |
| 11 | Plugins & marketplace — one-command capability bundles | 10:35:46 | Study Guide §11 |
| 12 | Scheduling — /loop, routines, desktop tasks, headless mode, safety | 11:07:28 | Study Guide §12 |
| 13 | **Capstone: DailyPulse** — full-stack app built live from a spec | 11:56:47 | Study Guide §13 + Lab 13 |

---

## Suggested study plans

**A. 10-day steady plan (~1.5–2 h/day)** — best retention

| Day | Do this |
|---|---|
| 1 | Watch 0:00–1:22 (modules 1–2). Install Claude Code. Lab 1–2. |
| 2 | Watch 1:22–2:58 (module 3). Lab 3. Skim the full slash-command list. |
| 3 | Watch 2:58–3:43 (module 4). Lab 4 — write a real CLAUDE.md for one of your projects. |
| 4 | Watch 3:43–4:31 (module 5). Lab 5. Deliberately blow up a context and fix it. |
| 5 | Watch 4:31–5:40 (module 6). Lab 6. Build one skill you'll actually reuse. |
| 6 | Watch 5:40–6:49 (module 7). Lab 7. Add a safety hook + auto-format hook. |
| 7 | Watch 6:49–8:20 (module 8). Lab 8. Connect one real MCP server. |
| 8 | Watch 8:20–9:51 (module 9). Lab 9. Build two subagents. |
| 9 | Watch 9:51–11:56 (modules 10–12). Labs 10–12. Schedule one read-only task. |
| 10 | Watch 11:56–13:53 (module 13) while building along. Do Lab 13 yourself. |
| +1 | Take `05-quiz-and-answers.md` cold. Review every wrong answer. |

**B. Weekend sprint** — watch all 13 modules over 2 days at 1.5×, then spend a third day doing labs 3–8 only. The capstone is optional in this plan; substitute your own project.

**C. Reference mode** — if you already use Claude Code, skip to modules 4, 5, 7, 9, 12 (the highest-leverage ones) and use `02-cheatsheet.md` as the index.

---

## The single most valuable habits the course teaches

1. **Write a real CLAUDE.md before writing code** — commands, stack, conventions, guardrails, verification steps.
2. **One task = one session.** `/clear` between unrelated tasks; `/compact` *with explicit instructions* when you must continue.
3. **Delegate anything that would dump a big file into your main context** to a subagent.
4. **Prefer hooks over prompting** for anything that must happen every time (formatting, logging, blocking dangerous commands) — hooks cost zero tokens.
5. **Match the model to the job** — plan with the strongest model, build with the balanced one, maintain with the cheap fast one.
6. **Start automations read-only**, write outputs to non-destructive paths, add human review gates for irreversible actions, log everything, and test for days before trusting a schedule.
7. **Never copy-paste a stranger's plugin/hook/marketplace repo without reading it.** Community bundles run with your permissions.

---

## Attribution & scope

This pack is a *study aid*: it summarises and restructures the ideas taught in the video so you can learn faster and revise. It is not a transcript and reproduces no substantial portion of the course. The concepts, demos, and file examples referenced come from the course and its public resources repo, linked above. Go watch the video — especially the live demos, which are what this pack deliberately compresses into prose.
