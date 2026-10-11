# Hands-on Labs — Claude Code Course

Twelve labs (one per module) plus the capstone. Each lab lists **goal**, **steps**, and **proof of completion** — don't move on until you can show the proof. Labs assume you've installed Claude Code; Labs 1–2 can be done on any modern machine.

> **Safety.** Work in a scratch folder or a throwaway repo for Labs 3, 7, 10 and 11 — you'll be experimenting with permission modes, guards, and parallel agents. Never point bypass/auto modes or unattended schedules at a repo you can't restore from git.

---

## Lab 1 — Prove the difference between chat and Code
**Goal:** internalise "brain vs brain with hands".

1. In a scratch folder, ask Claude chat (web/desktop) to write a Python script that sorts an array with bubble sort and saves it as `sort.py`.
2. Now start `claude` in the empty folder and ask the same.
3. Watch what happens with permissions and file creation; then run the script.
4. Write three sentences: what chat could do, what Code could do, and what made the difference.

**Proof:** `sort.py` exists, runs, and you can explain that the terminal is the mechanism of action.

---

## Lab 2 — Install, authenticate, and survive the first error
**Goal:** a working installation on your OS + a mental checklist for breakage.

1. Install Claude Code natively for your OS (macOS/Linux one-liner; Windows: exact PowerShell or CMD command).
2. Authenticate (`/login`, subscription or API key — know which you're on).
3. Start a session, ask something trivial, then run `/status`.
4. Deliberately break something recoverable: open a *second* shell that doesn't know the command, or query a bad model, and fix it using the course's triage (PATH/new terminal, right shell, clean reinstall).
5. Find where your session history is written under `~/.claude/`.

**Proof:** a session runs, `/status` shows your model, and you wrote down the triage steps that worked.

---

## Lab 3 — Command and permission tour
**Goal:** fluency with the daily control panel.

1. In a scratch repo, run `/help`, `/status`, `/model` (note the cache warning), `/effort` (try low vs high on the same question).
2. Create two files with Claude, then run `/cost` and `/context` and read both carefully.
3. Hold a short conversation, then `/branch` it; change something in the branch; `/resume` the original and confirm it's untouched.
4. Do a long-ish conversation, then `/compact` passing explicit instructions about what to keep; compare `/context` before and after.
5. Test permission modes with `Shift+Tab`: in plan mode, ask for a change and confirm nothing is edited; in accept-edits, confirm edits apply without prompting.
6. Run `/init` to see the CLAUDE.md skeleton it generates.

**Proof:** your notes list what each mode allowed/denied, with the `/context` before/after numbers from `/compact`.

---

## Lab 4 — Write a CLAUDE.md that pays for itself
**Goal:** a project brain you'll actually keep.

1. Pick a real project of yours (any language).
2. Draft CLAUDE.md containing: one-paragraph overview, tech stack, **essential commands** (install/dev/test/lint), code standards, project structure (only key files), hard rules, and a verification checklist.
3. Add an import (`@docs/…`) to keep the core small; add one HTML comment as a human-only note.
4. Test the hierarchy: put "always answer in Portuguese" in the user-level `~/.claude/CLAUDE.md`, and a conflicting convention in the project file. Ask a mixed question and observe which wins; remove the experiment afterwards.
5. Ask Claude to "run the verification steps for the file I just changed" — it should use *your* commands.

**Proof:** Claude runs your documented test command without being told it, and your hierarchy experiment showed project scope winning.

---

## Lab 5 — Break your context on purpose, then fix it
**Goal:** feel context rot and master the recovery.

1. In a project with a decent codebase, ask Claude to "read every file and summarise the architecture". Note `/context` usage.
2. Keep going: paste a long document, ask three unrelated follow-ups, and watch the number climb. Ask Claude a question that requires an instruction from early in the session and see whether it drifts.
3. Now recover: `/context` → `/compact` with explicit instructions ("keep the architecture summary, the API surface, the file map") → `/context` again. Then try `/clear` + a short status file handover instead.
4. Compute the cost lesson: from `/cost`, compare the per-message spend before and after compaction.

**Proof:** a table of context usage and cost before/after, plus two sentences on when you'd use compact vs clear.

---

## Lab 6 — Build a skill you'll reuse this week
**Goal:** a working skill with progressive loading.

1. Pick a repetitive workflow (release notes, PR description, data-file summary, weekly report).
2. Create `.claude/skills/<name>/SKILL.md` with frontmatter (`name`, `description`, `trigger`, optionally `argument-hint`, `effort`) and body sections: Goal, Inputs, Steps, Rules/Output format, References.
3. If part of it is deterministic, move that into a bundled script (`scripts/…`) and reference it. Add `requirements.txt` if libraries are needed.
4. Run it by trigger, then ask for the same thing in natural language and confirm auto-invocation works from the description.
5. Add an argument (e.g. output directory) and run it twice with different values.
6. Bonus: use a skill-creator to generate a second skill and compare its structure with yours.

**Proof:** two successful invocations (explicit + automatic) and the skill folder listed in the repo.

---

## Lab 7 — Hooks: guard, format, log
**Goal:** automation that costs zero tokens.

1. In a scratch project, ask Claude Code to add a **PostToolUse** hook matching `Write|Edit` that runs a formatter appropriate to your language (black, prettier, gofmt…). Confirm it fires.
2. Add a **PreToolUse** hook on `Bash` that blocks a small blocklist (`rm -rf *`, `git reset --hard`, `curl … | bash`). Implement it as a script that exits **2** with an explanatory stderr message. Try to trigger it — verify it blocks and that Claude proposes an alternative.
3. Add a **SessionStart** or **Stop** hook that appends a timestamped line to a log file.
4. Test each hook by hand with a sample JSON payload before relying on it.

**Proof:** the block fires with a written reason, and the log file contains entries from two different sessions.

---

## Lab 8 — Connect one real MCP server (and build a tiny one)
**Goal:** the toolbox, end to end.

1. Configure a hosted MCP server you can legitimately test (a search provider is the course's example) in `.mcp.json`, with the API key referenced as `${ENV_VAR}`. Put it in **local** scope if it's personal.
2. Run `/mcp`, authenticate, and list its tools.
3. Ask a question that forces a tool call; observe the permission prompt and the raw-vs-summarised result.
4. Now build your own: ask Claude Code to create a small Python MCP server exposing 3–4 tools (e.g. unit conversions or arithmetic). Inspect the tool schemas it produces, register it, restart the session, and use it.
5. Try the same request twice: once letting Claude choose the tool, once naming it explicitly. Note the difference when multiple tools overlap.

**Proof:** your own server answers a question through its tool, and your notes explain the schema → tool-choice link.

---

## Lab 9 — Two subagents with restricted tools
**Goal:** delegate with boundaries.

1. Create `.claude/agents/explorer.md`: name, a precise `description` ("Use when asked to map or summarise a codebase"), `tools: Read, Grep, Glob`, no write tools.
2. Create `.claude/agents/reviewer.md`: `model: haiku`, `disallowedTools: Edit, Bash`, a system prompt that says "report findings only".
3. In a real repo: ask "explore this codebase and tell me how authentication works" — verify the explorer is chosen and that only a summary lands in your main context (check `/context`).
4. Then implement a small change and explicitly invoke the reviewer with `@reviewer`; evaluate its output.
5. Run two subagents on independent questions at once and compare wall-clock time with doing them sequentially.

**Proof:** `/agents` lists both, the auto-delegation worked, and your main context stayed small.

---

## Lab 10 — Agent teams on a toy feature
**Goal:** parallel instances with discipline.

1. In a scratch repo with git initialised, enable the experimental flag in `.claude/settings.json`. ⚠️ Skip this lab if the feature is unavailable in your version — the concepts still matter.
2. Write a short spec: a small feature with three workstreams (e.g. API endpoint, UI component, tests) and an explicit rule that all teammates must agree on the API contract first.
3. Ask for a team of three; watch the lead spawn teammates. Use `Shift+Down` to inspect views.
4. Let them finish, then review the branches/worktrees and perform the merge yourself, resolving conflicts deliberately.
5. Before/after: record token usage — this is the most expensive lab.

**Proof:** three workstreams merged in a working repo, and a note on where coordination helped vs. cost time.

---

## Lab 11 — Package your setup as a plugin
**Goal:** turn your config into something shareable.

1. In a project where you've built agents, skills, and hooks, ask Claude to "create a plugin from my `.claude` folder" (or hand-assemble `.claude-plugin/<name>/` with `plugin.json`).
2. Verify the manifest: name, version, description, and correct paths for agents/skills/hooks; check `${CLAUDE_PLUGIN_ROOT}` in hook commands.
3. Enable it in project settings, restart, and confirm agents/skills/hooks are active.
4. Commit the plugin directory, clone the repo into a second folder, and confirm the plugin travels.
5. Optional: browse a marketplace and read one community plugin's hooks before deciding whether to install it (and write down why you would or wouldn't).

**Proof:** a fresh clone gets your capabilities, and you documented one security judgement about a third-party bundle.

---

## Lab 12 — Schedule something harmless, then something useful
**Goal:** automation you can trust.

1. **Headless first:** run `claude -p "summarise today's git log into reports/daily.md"` by hand. Confirm it respects permissions and doesn't hang.
2. **Loop:** use `/loop 2m` to watch a file (e.g. a log) and report when a condition is met — with a stop condition. Interrupt and restart it to see the session dependency.
3. **Routine/desktop:** set up one recurring task. Start read-only (analyse and write a report to `reports/`), with a human gate for anything irreversible.
4. Write the safety checklist into the task's prompt itself: read-only scope, non-destructive output path, log file, and the exact condition under which it should stop.
5. Run it on three consecutive cycles manually before leaving it unattended.

**Proof:** a log showing three successful scheduled runs and a report file produced without your intervention.

---

## Lab 13 — Capstone: build DailyPulse (or your own full-stack app)
**Goal:** exercise modules 1–12 in one build, spec-first.

Follow the course's build order. Substitute your own app if you prefer — keep the *sequence*.

### Phase 0 — Factory setup (before any app code)
- [ ] Create the repo, initialise git, commit nothing but a README yet.
- [ ] Write `CLAUDE.md`: stack, ports, storage, standards, essential commands, hard rules, verification steps.
- [ ] Add hooks: PostToolUse auto-format for your language + a Stop/log hook.
- [ ] Write your prompts **in advance** in `prompts.md`, one per phase. (Optional but recommended: have a *different* AI act as "CTO" to draft these technical prompts from your product spec.)

### Phase 1 — Backend
- [ ] FastAPI (or equivalent) with a thin route layer over a services module.
- [ ] JSON-file storage in `data/`; endpoints for tasks, briefing, standup, insights.
- [ ] CORS middleware configured for the frontend origin; `requirements.txt`.
- [ ] Test every endpoint with curl/browser.

### Phase 2 — Frontend
- [ ] React + Vite (+ Tailwind) with components for briefing, tasks, standup, insights, header/weather.
- [ ] Loading and error states on every API call; `fetch` to the backend base URL.
- [ ] Add one skill for a repeating ritual (e.g. `morning-briefing`, `generate-standup`).

### Phase 3 — Polish and AI features
- [ ] Add a real AI feature via an **API key** (not your chat subscription) with graceful fallback when the provider fails or the quota is exhausted.
- [ ] Add a live data feed (news/weather) through an API or MCP server.
- [ ] `/compact` with explicit instructions before asking for large changes; compress screenshots before pasting them for UI bug fixes.

### Phase 4 — Automate
- [ ] Schedule the briefing generation (cron locally, or a routine/desktop task) — read-only, non-destructive output path, logged.
- [ ] Add a subagent (e.g. `reviewer`) and use it before finishing.

### Deliverable checklist
- [ ] Runs end to end from a clean clone (documented in README).
- [ ] `CLAUDE.md`, at least one skill, one hook, one subagent committed.
- [ ] A `logs/` or `reports/` artefact proving the automation ran.
- [ ] A short `RETRO.md`: what the AI got right fast, where the last 20% went, and which module's feature you'd add next (subagents? teams? scheduling?).

**Stretch goals (pick one):** deploy it (backend + frontend hosts), add authentication, replace JSON storage with a database, or convert your morning briefing into a scheduled routine that messages you.

---

## Progress tracker

| Lab | Done | Proof artefact |
|---|---|---|
| 1 Chat vs Code | ☐ | `sort.py` + 3 sentences |
| 2 Install & auth | ☐ | `/status` output + triage notes |
| 3 Commands & modes | ☐ | context before/after table |
| 4 CLAUDE.md | ☐ | committed CLAUDE.md + hierarchy experiment |
| 5 Context rot | ☐ | cost/context table |
| 6 Skill | ☐ | `.claude/skills/<name>/` |
| 7 Hooks | ☐ | block log + session log |
| 8 MCP | ☐ | `.mcp.json` + own server |
| 9 Subagents | ☐ | two agent files + delegation evidence |
| 10 Agent teams | ☐ | merged branches |
| 11 Plugin | ☐ | `.claude-plugin/<name>/` |
| 12 Scheduling | ☐ | 3 logged runs |
| 13 Capstone | ☐ | working app + RETRO.md |
