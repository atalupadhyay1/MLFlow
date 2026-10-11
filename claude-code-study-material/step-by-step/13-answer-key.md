# Answer key — all quizzes

Answers for every quiz in the step-by-step guide (126 questions). **Take a quiz cold first**, then check here. For open questions the answer given is a *model answer*: if your version carries the same idea, you're right.

Scoring rule of thumb: below 80% on a part → re-read that part's **Why it matters** blocks before continuing. The later parts assume them.

---

## Part 01 — Foundations

### 1.1 Claude, Anthropic & the model family
1. **c — Haiku.** The task is narrow (read failing tests) and high-volume; speed and cost beat depth. Opus is for problems that require reasoning, not retrieval.
2. Because **capability is priced**: the strongest model burns more tokens, hits plan limits faster, and is slower for work that doesn't need it. "Most powerful" and "right for the job" are different things.
3. Costs: (i) dramatically higher token/cost burn and faster limit exhaustion, including on trivial edits; (ii) slower iterations and worse economics for high-volume mechanical work. Replacement policy: *default to the smallest model that passes the task; escalate to Opus only for planning, architecture and deep debugging.*

### 1.2 Chat vs Claude Code
1. **b** — the same models, with the ability to act on your machine through the terminal.
2. Because the "hands" can create, edit, delete and execute. Once an agent can act, the risk is no longer wrong answers — it's wrong *actions*, which is why permissions, hooks and review gates exist.
3. Any two of: create/modify/delete files in your project; run commands and tests; execute scripts; inspect the repository directly instead of you pasting it; iterate on real code until it runs.

### 1.3 The terminal
1. Because whoever can run commands in a shell can read, write, move and delete files and execute arbitrary programs — there is no narrower boundary. Terminal access *is* machine access.
2. `ls -la` (or `ls -a`). The `-a` flag shows dot-files, which plain `ls` hides.
3. `rm -rf` on your projects folder irreversibly deletes (recursively, without confirmation). You stop it with a **`PreToolUse` hook on `Bash` that exits 2** (Part 7), optionally plus a `deny` rule in `settings.json` (Part 3).

### 1.4 The agentic loop
1. **b** — ask → plan → act → observe → check → answer.
2. Because the loop **acts**: at each action point it crosses from thinking to doing something to your machine. The prompt is your opportunity to consent or refuse at exactly that boundary.
3. The weak stage is **observe/check** — it isn't verifying its work. Fix: add explicit **verification steps** to CLAUDE.md as commands (e.g. "after code changes run `npm test` and `npm run typecheck`; paste the output"). Verification instructions turn a guess into a checked fix.

---

## Part 02 — Install & authenticate

### 2.1 Installing
1. Because Claude Code needs to run on your machine to have hands. A web page cannot execute commands in your shell or touch your filesystem.
2. You installed for **one shell** and are running in the other. Each Windows shell has its own install command and PATH; either install for the shell you actually use or switch to the one you installed for (Windows Terminal is the smoothest route).
3. Most likely: (i) the shell session predates the install — **open a new terminal**; (ii) the install didn't complete or installed for a different shell/profile — **re-run the correct install command for your shell**, then verify with `claude --version`. Only reinstall after those two.

### 2.2 Authenticating
1. A **subscription** draws usage from your Claude plan's limits; an **API key** bills per token and is required for programmatic/headless work. Both authenticate Claude Code — they differ in billing, limits, and where they can be used.
2. Because your subscription authenticates **you** to Claude Code; an application needs its own programmatic credential. The app's usage is billed/limited separately — and must degrade gracefully when that key or quota fails.
3. Signals: (i) the error is an **auth/format** error rather than a stack trace in your code (e.g. "invalid key", "wrong format"); (ii) testing the key directly against the provider works or fails identically to the app. Also: "model not found" or quota errors are key/plan problems, not code bugs.

### 2.3 Running your way
1. Permission for Claude Code to **read, write and execute** within that folder. It's a security decision because a folder can contain credentials, client data or irreplaceable files — and "execute" means running code you may not read line-by-line.
2. On disk under **`~/.claude/`** (per-project session history, e.g. under `~/.claude/projects/…`). **`/resume`** uses it (as do rewind/branch flows).
3. The **desktop app (or IDE panel)** — it runs the same engine while bypassing a broken CLI path, so you keep working and can diagnose in parallel. It's a legitimate surface, not a workaround; you just have fewer knobs.

---

## Part 03 — Commands, model control & permission modes

### 3.1 Slash commands
1. In **`.claude/commands/`** (project) or `~/.claude/commands/` (user). The **filename becomes the command** (`pr-description.md` → `/pr-description`), and the file's content is the prompt it expands into.
2. `/compact` — ideally with explicit instructions about what to keep, since you intend to continue the same task.
3. Effort ranking, lowest to highest: **prompt (retype every time) < custom command (write once, reuse) < skill (procedure + scripts, auto-invocable) < hook (runs itself, zero tokens)**. Pick the **custom command** first: it's minutes of work and removes the retyping immediately. If the task also needs deterministic steps or auto-invocation, promote it to a skill later; only reach for a hook if it must happen without you asking.

### 3.2 Model, effort and cost
1. Because the conversation is **cached for the current model**; a different model can't reuse that cache, so the **full history is read again** on the next message — you pay to re-establish context. Claude Code warns you exactly when you attempt it.
2. `/model` chooses **which brain** (capability tier/version); `/effort` chooses **how hard that brain thinks** on the request (low → max). One changes the engine, the other changes the throttle.
3. Any two: **compact/clear** to shrink the history being resent; reduce **effort** for routine steps; **narrow your prompts** so fewer files get read; disable **unused MCP servers**; trim **CLAUDE.md**; delegate bulk reading to **subagents**; take **smaller tasks per session**.

### 3.3 Session commands
1. `/compact` **summarises the existing conversation and continues in the same session**. `/clear` **abandons the conversation and starts a fresh session with empty context** — the old one remains on disk.
2. When you want to **try something without risking the working session**: a fork keeps the original intact and gives the experiment its own session ID. `/rewind` moves you *backwards* in the same conversation; it doesn't preserve the current state as a separate thread.
3. **`/compact` with explicit instructions** — keep the file structure, API surface, established patterns, open TODOs. Not `/clear` (you'd lose a working session's context and have to rebuild it) and not `/rewind` (it doesn't reduce context; it moves you to an earlier point and discards the work since).

### 3.4 Permission modes
1. **Plan mode** is read-only. It still allows **reading files, searching, and exploring** the codebase so it can present a plan — it just can't edit or execute.
2. Because **prompt fatigue causes mistakes**: approving dozens of trivial actions trains you to approve without reading. Auto mode keeps a background safety check while running, so you keep momentum *and* a safety net; bypass removes the checks entirely, which is only acceptable where damage is contained (isolated containers/VMs).
3. Objection: bypass removes every guard on a repository where a mistake is unrecoverable — a wrong command can delete work or leak credentials, and there is no undo. Alternative: keep **auto mode + deny rules in `settings.json` + a `PreToolUse` guard hook**, or run bypass only inside a throwaway container with the repo mounted read-only.

### 3.5 The `.claude` directory
1. It's a **dot-directory** (hidden by convention on Unix-like systems). See it with `ls -la`, or enable hidden files in Finder/Explorer.
2. Most likely: (i) the **hook is in the wrong scope or file** — e.g. user settings vs project settings, or the project has its own `settings.json` that doesn't include it; (ii) **settings were not re-read** — hooks load at session start, so a restart is needed (also check the session's cwd is inside the project).
3. *Personal review agent* → **user scope** (you want it everywhere). *Deploy command for this repo* → **project scope** (it only makes sense here, and the team should have it — though anything sensitive about it should be parameterised). *API keys* → **neither**: environment variables or a secrets manager; never in either scope, and especially never committed.

---

## Part 04 — CLAUDE.md

### 4.1 What & why
1. It's the project's standing instruction file: what the project is, its stack, exact commands, conventions, hard rules and how to verify work — loaded automatically so every session starts informed instead of blank.
2. Because it is **re-sent in every request**, so its length is a permanent tax on cost, speed and usable context — and long files get truncated, meaning some "true" lines are never even read.
3. Any three genuinely repeated problems (e.g. wrong test runner used repeatedly; inconsistent naming in new files; Claude re-creating a helper that already exists; forgetting the migration step; not running the type check). Each becomes one short line under the right heading.

### 4.2 Hierarchy & loading
1. **`CLAUDE.local.md` → project (`./CLAUDE.md` or `.claude/CLAUDE.md`) → user (`~/.claude/CLAUDE.md`) → enterprise/managed policy.** (Strongest first; enterprise is enforced above all.)
2. It walks up the tree: `repo/backend/`, then `repo/`, then any parent directories, loading `CLAUDE.md` and `CLAUDE.local.md` from each level it passes.
3. The **project rule** ("this repo uses tabs") applies — it's closer to the work than your global preference. If the clash is genuine and consequential, Claude will typically **ask** rather than silently pick; you can also make the intent explicit ("this project overrides any personal preference about indentation").

### 4.3 Writing it
1. **"Run `npm run typecheck` before finishing."** It's a command Claude can execute and verify against; the Stripe reference is bulk that inflates every request and goes stale. Document the API elsewhere and link/import it if needed.
2. Because an outcome ("tests pass") is unverifiable and arguable — the model can claim it. A command produces **observable output** the model can read, so the agentic loop's *observe* and *check* stages actually work.
3. (i) Move detail into **imported files** (`@docs/…`) so the always-loaded core stays small; (ii) **delete stale/obvious lines** and move anything procedural into a **skill** (loaded only when invoked). Optionally (iii) check whether the file is being truncated and prioritise the top of the file accordingly.

---

## Part 05 — Context management

### 5.1 The context window
1. Because every request carries fixed overhead: the **system prompt**, **tool definitions**, **MCP server tool descriptions**, **skill descriptions**, and **CLAUDE.md/memory**. That floor is paid before you type a word.
2. **You control:** MCP descriptions (enable fewer servers), CLAUDE.md (write tighter), message history (clear/compact), skills installed (though they're cheap at rest). **You don't control:** the system prompt and core tool definitions.
3. Two sentences: "History is re-sent and billed on **every** call, so a 200K-token context charges you again for those 200K tokens on your next message — cost scales with session length, not just new words. It's also why long sessions get slower and forgetful: the window fills, and attention spreads thinner." (Course's illustration: ~200K × 5 messages ≈ $3 on Sonnet ⚠️.)

### 5.2 Context rot
1. Quality decay in long sessions — ignored instructions, repeated work, new mistakes — caused by how much context the model is juggling, not by the model getting worse.
2. **Primacy and recency bias**: models attend more strongly to the beginning and end of a long context; the middle gets "fuzzy".
3. Wrong diagnosis: "the model got dumber / is having a bad day." Right diagnosis: **the context is bloated** — run `/context`, then `/compact` with instructions (or `/clear` + status file) to restore behaviour.

### 5.3 Budgeting & recovery
1. **Controlled:** CLAUDE.md size, number of enabled MCP servers, session hygiene (`/clear` between tasks), prompt specificity, model & effort, whether you paste images/large files, use of subagents. **Not controlled:** the platform system prompt and core tool definitions.
2. When the **task has changed or quality is still poor after compacting** — a status file + clean session gives a smaller, cleaner baseline than a summarised monster. `/compact` is better when you must continue the *same* task with continuity.
3. **Delegate exploration to subagents** (and/or a status-file handover): let the isolated worker do the 40K tokens of reading and return a summary, so your main context never absorbs the file dumps.

---

## Part 06 — Skills

### 6.1 What & why
1. Because of **progressive disclosure**: only each skill's name and description sit in context; the body and bundled scripts load only when the skill is invoked.
2. The **`description`** field — when it matches the current request's intent, the model can invoke the skill automatically.
3. (a) **Hook** — reformatting must happen every time, deterministically, at zero token cost. (b) **Slash command** — a saved prompt you invoke deliberately (promote to a skill if it grows steps/scripts). (c) **Skill** — a five-step pipeline with bundled scripts is exactly what skills are for.

### 6.2 Anatomy
1. **`description`** — it must state *what the skill does* and *when to use it* (the trigger conditions), because that's the text the model uses to route.
2. Because a script is **deterministic and free**: it runs identically every time with no tokens spent regenerating the same code, and no run-to-run variation in the mechanics.
3. The **output format specification** — a literal template and/or a sample of the exact expected output, plus rules for edge cases (empty input, rounding, ordering). Without it, the model improvises the presentation each run.

### 6.3 Creating skills
1. A skill creator **generates a skill from a description** — clarifying scope/components first, then producing `SKILL.md`, scripts, references, assets and requirements. You must still review: the **description** (routing), the **output contract**, argument handling, and whether the scripts match your project's conventions.
2. Add frontmatter fields (e.g. `argument-hint: "path/to/data.csv out/dir"`) and reference the arguments in the body (`$1`, `$2`) — the course's `generate-report-arg` pattern.
3. Any two: rewrite the **description** to include project-specific triggers; **point the steps at your project's real commands/paths** (e.g. your test runner, your folder layout); add your output format; set `effort`/model; restrict what it does when invoked.

---

## Part 07 — Hooks

### 7.1 What, why & events
1. Because they run **outside the model** on lifecycle events — pure software reacting to an event, with no prompt and no generation. Relative to the loop, they don't participate in it; they attach to its edges (before an action, after an action, at session boundaries).
2. **`PreToolUse`** — it fires before the tool runs, and with `exit 2` (or a `permissionDecision: deny`) it prevents the action outright.
3. Hook: *format every Python file after it's written* (must be guaranteed, costs nothing). Prompt: *"focus on readability rather than cleverness in this module"* (a judgement/context-sensitive instruction for this task). Prompts are for judgement; hooks are for guarantees.

### 7.2 Configuration
1. **Event name**, **`matcher`** (which tool/event it applies to), and the **`hooks` array** containing the command (+ optional `timeout`/`async`). The **matcher** decides when it fires (with the event key).
2. Because an async hook returns control immediately — Claude proceeds without waiting, so the hook cannot **block** the action it was supposed to prevent. Blocking requires a synchronous hook whose exit code is read.
3. Matcher-level: the matcher doesn't match the tool name you assumed (e.g. `Write` vs `Write|Edit`, or wrong case); the matcher regex/target is so specific it never matches in practice. Settings-level: the hook is in a **different scope/file** than the session reads (user vs project, or a `.local` file), or the session wasn't restarted after editing.

### 7.3 The contract
1. **`0`** = allow/continue. **`2`** = block the action, with stderr passed back to Claude as the explanation. **Other non-zero** = non-blocking error (logged, doesn't stop Claude).
2. Because a silent failure teaches nothing: the model doesn't know why, so it may retry the same thing or thrash. `exit 2` plus a clear stderr message gives Claude the *reason*, so it explains the block and proposes a safer alternative — the block becomes a conversation instead of a wall.
3. **Exit 1 is a non-blocking error** — the tool still runs. That is exactly wrong for a guard: it looks like protection while providing none. Destructive actions must exit **2** (or return `permissionDecision: "deny"`).

### 7.4 Four hooks worth building
1. Because a hook is **code running with your permissions** — a bug can break every edit, and Claude-mediated testing is slow and confusing. Crafting a sample JSON payload and checking the exit code takes seconds and isolates the bug.
2. Any two: narrow the matcher (only `.py`, not every write); make it **`async: true`** if Claude needn't see the result; run the formatter only on **changed files** rather than the whole project; swap the formatter for a faster one; move heavy logging out of the synchronous path.
3. The **security guard** (and any `PreToolUse` blocker) — because exit 2 overrides auto/bypass modes where nothing else is asking for permission. That's what makes it the guarantee that survives a "convenience" mode.

---

## Part 08 — MCP

### 8.1 What & why
1. An **open standard** defining how AI agents communicate with external tools and data sources. The course's example: **a toolbox you don't have to build or maintain** (you connect instead of forging your own hammer).
2. A **connector** is a ready-made, curated integration surfaced inside Claude products; an **MCP server** is any implementation of the open protocol that you add and configure yourself — more work, far more extensible, and reusable across MCP-compatible clients.
3. Because every server's **tool descriptions occupy context on every request**, and **overlapping tools confuse selection** — the course demonstrates a model choosing the wrong search tool when two similar ones existed. More servers can mean worse tool choice and a fatter, pricier prompt.

### 8.2 Connecting a server
1. **Local** when the tool must touch your machine or your private files (filesystem access, Playwright browser automation) — those need your resources and your data. **Hosted** when the capability belongs to a provider (Gmail, Slack, Tavily, GitHub) — no local process to maintain, but auth/credits become your failure modes.
2. In **environment variables**, referenced from the config as `${VAR_NAME}`. Never as a literal string in a committed config file, and never anywhere in the repository.
3. (i) Is the server declared in the file the session actually reads, and in the correct **scope** (project vs user vs local)? (ii) Is the JSON valid, and has the session been **restarted** since you added it? (iii) If it is host-dependent, is the **env var set** in this shell/session (and is the key valid)?

### 8.3 Building your own
1. **Name**, **description**, and **JSON-schema parameters** (types + required fields). The **description** is effectively a prompt: it is what the model reads when deciding whether and how to call the tool.
2. Because tool selection happens **before** execution, driven by names and descriptions rather than code. Two plausible-looking descriptions make the choice ambiguous, so the model picks wrongly — the code never gets a chance to be right.
3. (i) Write a small MCP server that exposes the balance API as 2–3 tools with clear names, descriptions and parameter schemas; (ii) test it locally and register it in `.mcp.json` (local scope for credentials); (iii) get the API key into an environment variable and confirm the tools appear in `/mcp`; (iv) share it with the team — commit the server repo, use **project scope** for the server definition and keep the key personal.

---

## Part 09 — Subagents

### 9.1 What & why
1. A **summary/report** — the subagent's reading, exploration and dead ends stay in its own context window; only its final output returns to the main session.
2. Any two: **cost control** (cheaper model for routine work), **focus/quality** (a specialist prompt beats a generalist), **parallelism** (independent jobs at once), **safety** (restricted tools create a real boundary).
3. **(b)** should be delegated — it's bulk reading producing a small answer. (a) is a **decision with architectural and business consequences** that needs your full context and accountability; keep it in the main session (a subagent may *gather* the evidence for it).

### 9.2 Building & invoking
1. **`description`** — and it should state purpose *and* timing/conditions ("use at the START of any new feature, before any code is written"), because that's the routing text.
2. Because the reviewer's job is to **report, not repair**: without `Edit` it cannot quietly rewrite your code (hiding problems), and without `Bash` it cannot run or mutate anything — findings stay observations you decide on. It also keeps the review cheap and focused.
3. (i) **Rewrite the descriptions** so each states a distinct purpose and when to use it — ambiguity is the usual cause; (ii) **invoke explicitly** with `@agent-name` for the work that matters, treating natural language as a convenience; optionally reduce the number of overlapping agents or give each a distinct, narrow scope.

---

## Part 10 — Agent teams

### 10.1 What & why
1. **Subagents report back to one parent** (a hierarchy, results returning upward). **Agent teams are peers** — separate concurrent sessions that message each other, coordinated by a lead, with git worktrees providing isolation.
2. Git worktree lets each teammate have its own **branch/checkout** of the repository, so parallel edits don't collide in one working directory. Without it, simultaneous writers would trample each other's files and uncommitted changes.
3. A **small, tightly coupled change** — e.g. "rename this function and update its three callers, then run the tests". It doesn't split along an interface, so spawning three sessions adds coordination overhead and merge risk for no parallelism gain.

### 10.2 Running a team
1. The rule that **teammates agree the interface contract (request/response schema, shared types) before writing code** — without it, each workstream invents its own assumptions and the pieces don't fit, which is the dominant failure mode.
2. Because a summary is a *claim*, not a verification. Merging is where conflicts, silent overwrites and scope creep surface; you are the one accountable for the result, so review each diff and merge deliberately — then run the tests on the merged tree.
3. (i) **Assign file/directory ownership** per teammate in the brief so their edit surfaces are disjoint (e.g. `backend/`, `frontend/`, `tests/`); (ii) **stop and re-brief**: have them agree the shared interface first (or serialise the overlapping part so only one writer touches that file).

---

## Part 11 — Plugins

### 11.1 What & anatomy
1. Any five of: agents (subagents), skills, commands, hooks, MCP server definitions, settings templates, CLAUDE.md, README/manifest metadata.
2. So hook commands resolve to the plugin's own files **wherever the plugin is installed** — otherwise absolute or relative paths break on a teammate's machine and the hook silently fails.
3. **Credentials and secrets** (API keys, tokens) and anything machine-specific/personal (absolute paths, personal preferences). Secrets belong in **environment variables or a secrets manager**; personal preferences belong in **user scope** outside the shared bundle.

### 11.2 Install & create
1. That you **read the code before enabling it** — specifically its **hooks and commands**, since those execute with your permissions — check reputation (stars, forks, activity), and test it in a **scratch repository**. Community plugins are not reviewed by Anthropic.
2. You **commit the plugin directory** and **enable it in project settings** — when a teammate pulls the repo, the plugin (and the switch that turns it on) arrives with it.
3. **A hard-coded path** (absolute path to your home directory, or a relative path that assumed your layout) instead of `${CLAUDE_PLUGIN_ROOT}` — the most common portability failure in hand-assembled plugins.

---

## Part 12 — Scheduling

### 12.1 Why & the three ways
1. **`/loop`** — machine on *and* session open. **Desktop scheduled task** — machine on. **Claude routine** — neither; it runs in the cloud.
2. It **reasons about the outcome**: reads an error, tries an alternative, documents the failure, and notifies with a diagnosis and a suggested fix. A cron script just exits and leaves you to discover the silence hours later.
3. **`/loop`** — it's a short-lived local watch with a stop condition, running in the session that has your local file access; the routine/desktop route is for recurring schedules, not "watch until this one thing finishes".

### 12.2 `/loop` & headless
1. It changes the **interface, not the policy**: headless still **enforces permissions**, but it cannot stop to ask — so anything requiring approval simply doesn't happen. What it removes is the blocking prompt, which is exactly why schedules don't stall. (It is *not* a permission bypass.)
2. Because `/loop` runs **inside the current session on your machine** — closing the terminal ends the session, and the loop with it (also subject to its expiry).
3. Most likely: (i) the run **needed a permission** it couldn't obtain and therefore did nothing (no UI to ask through); (ii) it **errored early or wrote somewhere else** — the working directory/paths differed under the scheduler, or the command wasn't on the scheduler's PATH. Also possible: the output went to a file you didn't check.

### 12.3 Routines & desktop tasks
1. Triggers: **schedule**, **API call**, **GitHub events** (PR opened/merged, release published, issue opened). Filter example: author/title/body/`regex` — e.g. ignore anything whose title contains "chore" or "deps".
2. Because it runs on **Anthropic's cloud infrastructure**, not your machine. Instead of your local files it gets a **fresh clone of your repository** (with your tools/MCP servers available).
3. Add a **title filter** (e.g. "skip if the title matches `^(chore|build|deps)`" or "only review PRs whose body mentions a feature flag/label"). Reason: every run costs tokens and attention, and automated dependency bumps add noise rather than review value — you want the routine looking at changes a human should actually scrutinise.

### 12.4 Safety playbook
1. **Start read-only. Write to non-destructive paths. Human review gates for irreversible actions. Log everything. Test for days before trusting it.**
2. Safe rewrite: *"Every night, run the tests, diagnose any failures, and write a report to `reports/test-diagnosis.md` (including suggested patches as proposals, not applied changes); open a PR with the proposed fixes for human review — never push directly to main."* (The point: diagnose and propose; a human merges.)
3. (i) A summary is a **claim** — the log is the raw evidence, and you need it to reconstruct what actually happened when the run misbehaves. (ii) Logs are your **only debugging surface**: nobody watched the run live, so without a trail you cannot tell what it read, decided, or did — nor prove it *didn't* do something.

---

## Part 13 — Capstone

### 13.1 Factory setup
1. Because CLAUDE.md and hooks **shape every subsequent action**: the brain knows the stack, commands and verification steps from the first file, and formatting/logging happen automatically. Retrofitting them means correcting conventions across a codebase that was built without them.
2. You use a **second AI as "CTO"** — give it the product spec and have it draft the technical prompts/architecture, then hand those prompts to Claude Code to execute. It separates **decision-making from execution**, so the build follows a considered plan instead of whatever the executor improvises.
3. Any two: (i) you lose control of **sequence and scope** — one prompt produces an architecture you never reviewed, and mismatches surface late; (ii) **debugging becomes guesswork** — with everything changed at once you can't isolate what broke; (iii) it **blows context** on one huge generation rather than letting you verify each layer.

### 13.2 Backend
1. Because **route handlers stay about transport** (parse request, call logic, shape response) while **business logic lives in one testable place**. It keeps changes local — new logic doesn't require touching routes — and stops validation, storage and AI calls tangling into a single unreviewable file.
2. The model **invents its own API** — different field names, different shapes, different status codes — which the frontend then codes against, producing mismatches you debug later. Schemas pin the contract so both sides agree by construction.
3. Because you **remove a whole layer of variables**: with curl you're testing the backend alone, so any failure is backend-only. Once the UI is involved, a failure could be the backend, the frontend, CORS, the browser, or the data — and you'd be debugging all of them at once.

### 13.3 Frontend & debugging
1. Because **images consume context** like anything else — a full-page screenshot can cost thousands of tokens per paste, and it's re-sent on every subsequent turn in that session. Compressing (and cropping to the relevant region) keeps the cost proportional to the information.
2. "The page stopped showing an error" might mean the request succeeded, the error was swallowed, a fallback rendered, or a cached response was used. "CORS is fixed" means you verified the actual mechanism: a **200 response with the expected `Access-Control-Allow-Origin`** in the network tab, from the real request to the real origin.
3. Correct behaviour: **degrade gracefully** — catch the provider failure, disable or clearly mark the AI-backed feature, show a helpful message (and any deterministic fallback result), and leave the rest of the app working. This is the **Part 13 / Part 2** lesson about app keys (and Part 5's context hygiene doesn't apply here — the fallback is the point).

### 13.4 AI features, scheduling, go-live
1. Because a subscription authenticates **you** to Claude Code's session. An application calling a model at runtime needs its own **programmatic credential** (API key), with its own billing and limits — the two are not interchangeable.
2. Any three from Part 12: **read-only first**; **write outputs to a non-destructive path** (`reports/`); **human gate for anything irreversible**; **log every run**; **test for days/manual cycles before trusting it**; plus deny rules/guard hooks and monitoring usage.
3. Any two sensible habits: (i) **`/compact` with explicit instructions before big asks** and `/clear` between phases, instead of dragging a bloated history through the whole build (Part 5); (ii) **match model/effort to the work** — cheaper models for mechanical edits, saving the strong model for planning (Parts 3–5); (iii) **delegate bulk reading** to subagents; (iv) **schedule work to run unattended** (routines) instead of holding one long session (Part 12); (v) monitor `/cost` and plan usage as you go rather than discovering the limit mid-feature.

---

## If you got a lot wrong in one part

Don't re-read the whole part — go straight to its **Why it matters** blocks and then redo the **Lab**. These quizzes test whether you've internalised the reasoning, not whether you memorised a command list; a missed answer almost always means a *why* you skimmed.
