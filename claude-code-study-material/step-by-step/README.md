# Step-by-Step Guide — Claude Code Full Course

A procedural companion to **"CLAUDE CODE FULL COURSE 12 HOURS: Build Real AI Projects (2026)"** by Mayank Aggarwal
(<https://www.youtube.com/watch?v=05aY2LRIC3s>).

**Every topic follows the same five blocks:**

| Block | What it gives you |
|---|---|
| **What it is** | The concept in a few lines — the definition you could repeat to someone else |
| **Why it matters** | What it changes in practice; what breaks if you ignore it |
| **How to do it** | Numbered, copy-able steps with real commands and configs |
| **Lab** | A checkbox exercise with a *proof of completion* (don't skip) |
| **Quiz** | 3 questions per topic — answers in `13-answer-key.md` so you can self-test honestly |

> **How this differs from the rest of the pack.** `01-study-guide.md` is a *reading* document (concepts, demos, gotchas). This guide is a *doing* document: it assumes you'll sit at a terminal with the video paused, and it ends every topic with practice and a check. Use the study guide to understand a module, this guide to master it.

---

## How to work through it

1. **Pick one part** (= one module of the video). Skim its "What it is" blocks to see the shape.
2. **Watch that chapter of the video** at 1.25–1.5× with this file open beside it.
3. **Do the How steps** on your own machine as they come up. Don't batch them — muscle memory is the point.
4. **Do the Lab.** It is deliberately small and always ends with an artefact (a file, a log line, a screenshot, a score).
5. **Answer the Quiz without looking.** Then check `13-answer-key.md`.
6. Tick the topic in the progress table at the bottom of each part. Move on.

**Scale:** 42 topics, 42 labs, 126 quiz questions with a full answer key. One part a day for 13 days is comfortable; three topics a day is the sprint.

**Conventions used throughout**
- `code` = something you type or a filename.
- ⚠️ = version-specific detail from the recording (model names, prices, limits, experimental flags). Verify against current docs before depending on it.
- Every Lab has a **Proof** line. If you can't point at the artefact, the lab isn't done.
- Quizzes mix *recall*, *application*, and *diagnosis* questions. The diagnosis ones are the ones that matter in real work.

---

## Topic index

| Part | Topics | Video |
|---|---|---|
| [01 — Foundations](01-foundations.md) | 1.1 Claude, Anthropic & the model family · 1.2 Chat vs Claude Code (brain vs brain with hands) · 1.3 The terminal · 1.4 The agentic loop | 0:00:00 |
| [02 — Install & authenticate](02-install-and-auth.md) | 2.1 Installing on macOS/Linux/Windows · 2.2 Authenticating (subscription, API key, third parties) · 2.3 Running your way (desktop, IDE, trust, sessions) | 0:33:08 |
| [03 — Commands & modes](03-commands-and-modes.md) | 3.1 Slash commands · 3.2 Model, effort & cost · 3.3 Session commands · 3.4 Permission modes · 3.5 The `.claude` directory | 1:22:17 |
| [04 — CLAUDE.md](04-claudemd.md) | 4.1 What & why · 4.2 Hierarchy & loading · 4.3 Writing and maintaining it | 2:58:27 |
| [05 — Context management](05-context.md) | 5.1 The context window · 5.2 Context rot · 5.3 Budgeting & the recovery playbook | 3:43:48 |
| [06 — Skills](06-skills.md) | 6.1 What & why · 6.2 Anatomy · 6.3 Creating skills (and Skills 2.0) | 4:31:35 |
| [07 — Hooks](07-hooks.md) | 7.1 What, why & events · 7.2 Configuration · 7.3 The contract · 7.4 Building four hooks | 5:40:13 |
| [08 — MCP](08-mcp.md) | 8.1 What & why (connectors vs MCP) · 8.2 Connecting a server · 8.3 Building your own | 6:49:12 |
| [09 — Subagents](09-subagents.md) | 9.1 What & why · 9.2 Building and invoking them | 8:20:17 |
| [10 — Agent teams](10-agent-teams.md) | 10.1 What & why (vs subagents) · 10.2 Running a team safely | 9:51:44 |
| [11 — Plugins](11-plugins.md) | 11.1 What & anatomy · 11.2 Installing safely and creating your own | 10:35:46 |
| [12 — Scheduling](12-scheduling.md) | 12.1 Why + the three ways · 12.2 `/loop` & headless · 12.3 Routines & desktop tasks · 12.4 Safety playbook | 11:07:28 |
| [13 — Capstone: DailyPulse](13-capstone.md) | 13.1 Factory setup · 13.2 Backend · 13.3 Frontend & CORS · 13.4 AI features, scheduling, go-live | 11:56:47 |
| [Answer key](13-answer-key.md) | All quiz answers with one-line explanations | — |

---

## Progress table

Copy this into your notes and tick as you go.

| Part | Watched | How steps done | Lab done | Quiz scored |
|---|---|---|---|---|
| 01 Foundations | ☐ | ☐ | ☐ | ☐ /12 |
| 02 Install & auth | ☐ | ☐ | ☐ | ☐ /9 |
| 03 Commands & modes | ☐ | ☐ | ☐ | ☐ /15 |
| 04 CLAUDE.md | ☐ | ☐ | ☐ | ☐ /9 |
| 05 Context | ☐ | ☐ | ☐ | ☐ /9 |
| 06 Skills | ☐ | ☐ | ☐ | ☐ /9 |
| 07 Hooks | ☐ | ☐ | ☐ | ☐ /12 |
| 08 MCP | ☐ | ☐ | ☐ | ☐ /9 |
| 09 Subagents | ☐ | ☐ | ☐ | ☐ /6 |
| 10 Agent teams | ☐ | ☐ | ☐ | ☐ /6 |
| 11 Plugins | ☐ | ☐ | ☐ | ☐ /6 |
| 12 Scheduling | ☐ | ☐ | ☐ | ☐ /12 |
| 13 Capstone | ☐ | ☐ | ☐ | ☐ /12 |
| **Total** | | | | **☐ /126** |

**Scoring rule of thumb:** below 80% on any part, re-read that part's *Why* blocks before continuing — the later modules assume them.

---

*This guide summarises and restructures the course's teaching; it is not a transcript. Concepts and demos belong to the course and its public resources repo (github.com/mayank953/Youtube → Claude Code Crash Course).*
