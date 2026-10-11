# Claude Code Full Course — Study Guide

Module-by-module notes for **"CLAUDE CODE FULL COURSE 12 HOURS: Build Real AI Projects (2026)"** by Mayank Aggarwal.
Each module: **why it matters → key ideas → the demo → configs/commands → gotchas → check yourself.**

Timestamps refer to the video. Version-specific facts (model names, prices, limits) are marked where they matter.

---

## Module 1 — Foundations: what Claude Code actually is
**Video:** 0:00:00 – 0:33:08 · **Why it matters:** every later module is easier once the brain/hands model is clear.

### 1.1 Anthropic, and how Claude relates to ChatGPT
- OpenAI builds **ChatGPT**; **Anthropic** builds **Claude**. Different companies, same category of product.
- Anthropic was founded by people who left OpenAI and positions itself as safety-first ("AI research and products that put safety at the frontier").
- Pedagogically the course anchors Claude against ChatGPT because everyone has used ChatGPT — "ChatGPT is the Google of AI" is the course's framing.
- Practical takeaway: when documentation or a tutorial says "the model", it means an Anthropic model behind the Claude product family.

### 1.2 The Claude model family
| Tier | Character | Best for | Trade-off |
|---|---|---|---|
| **Haiku** | Fastest, cheapest | Simple, quick, high-volume tasks; maintenance | Least deep reasoning |
| **Sonnet** | Balanced | Everyday work, most coding/reasoning | Middle ground |
| **Opus** | Most capable | Complex planning, architecture, hard reasoning | Slowest, highest token/cost burn |

- Models as shown in the video: Haiku 4.5, Sonnet 4.6, Opus 4.7 (older versions remain selectable).
- Some models expose **extended thinking** (think longer before answering) or **adaptive thinking**; availability varies by tier.
- Context windows quoted in the course: ~200K tokens for Haiku; up to ~1M for larger surfaces — treat exact numbers as version-specific and check docs.
- **The course's rule of thumb — match model to job, don't always pick the strongest:**
  - **Opus → plan / architect** (like a senior engineer writing the plan)
  - **Sonnet → build** the main components (mid-level engineer)
  - **Haiku → maintain**, find errors, do simple edits (junior/maintenance work)
- Picking the right model is a *cost and context* decision, not an ego decision. More power = more tokens = faster limit burn.

### 1.3 Claude on web & desktop vs Claude Code
- Web/desktop Claude is a **chat interface**. It can answer, explain, write code *for you to copy*, and read screenshots you hand it. **It cannot touch your files.**
- Analogy used in the course: **Claude on desktop is a smart person on the phone** — great advice, no hands.
- **Claude Code is the same brain with hands.** The hands are your **terminal**: the terminal is what can create/delete files and run commands, and anything that can run commands on your machine *has access to your machine*.
- Demo that proves it: from a terminal, `mkdir` creates a folder that instantly appears in Finder; `touch` creates files; `ls` lists them. Claude Code is installed on your machine precisely so it can do this class of thing.
- Demo contrast: ask chat Claude for a bubble-sort script → it prints code you must copy, save, and run yourself. Ask Claude Code the same thing → it writes the file, pastes the code, and runs it.
- **Why "for developers":** Claude Code needs installation and shell access — that's the mechanism by which the brain gets hands.

### 1.4 The agentic loop (the most important idea in the course)
When you ask Claude something, it doesn't answer in one shot. It runs a loop:

```
ask → plan → act (read files / search / run commands) → observe result → check
   ↘ if not good enough ── retry with what it learned ──┐
   ↘ if good enough ── answer ──────────────────────────┘
```

- Demo in the course: asking chat Claude for a PDF makes it read a "PDF skill", choose a library, install it, write a script, run it, and return the finished PDF — visibly iterating. The course's line: it isn't magic, it's iteration at very high speed.
- Claude Code runs the same loop but with file writes and shell commands as its actions, which is why it asks for permission at action points.
- **Why this matters for the rest of the course:** skills, hooks, MCP, and subagents are all ways of *shaping* this loop — giving it better procedures, better reflexes, better tools, and better workers.

### Check yourself
1. Why is "Claude Code = Claude with a different UI" wrong?
2. Which model would you pick to plan a large refactor, and why not the same one for maintenance?
3. What does the terminal have to do with Claude Code's abilities?

---

## Module 2 — Installation, authentication, and IDEs
**Video:** 0:33:08 – 1:22:17 · **Why it matters:** most people quit here when an install error appears; the course deliberately troubleshoots as it goes.

### 2.1 Three ways to run Claude Code
1. **Native install via terminal** (the course's recommended default)
   - macOS / Linux: a single install command from the official quickstart, run in Terminal.
   - Windows: a separate PowerShell command and a CMD command — use the exact one for your shell. If you want the Unix-like experience most tutorials assume, install **Windows Terminal** (Microsoft's) instead of fighting CMD.
   - The installer downloads a script, then additional pieces, then finishes — it takes a minute and looks "stuck" only because it's fetching.
2. **Inside Claude Desktop** — with a paid Pro/Max plan, a Claude Code tab appears in the desktop app: pick a folder, type a request, approve "trust this workspace". It's a GUI, but the course recommends learning the terminal path.
3. **Inside an IDE** (VS Code or a fork), where Claude Code runs in a panel with the editor's context. Useful, but the underlying mechanics are the same.

### 2.2 The trust prompt — read it
Before it works in a folder, Claude Code asks you to **trust the workspace**, warning that it may **read, write, or execute** files there. That's not boilerplate: after trusting, it can read a folder containing your bank statements, edit or delete files, and run Python you ask it to run. Trust folders deliberately.

### 2.3 Authentication
- `/login` signs in with your Anthropic account; `/logout` signs out (and forces re-authorisation next start).
- Two billing paths:
  - **Subscription** (Pro/Max) — Claude Code usage is drawn from your plan's limits.
  - **API key** — pay-per-token via console credentials; required if you want usage without a subscription, and required for headless/programmatic use.
- Third-party platforms exist for accessing models (pros: cheaper/alternative access; cons: extra moving parts, token/credit quirks) — the course demonstrates one and shows the failure modes: mysterious quota errors, key format errors, models being decommissioned. Budget time for troubleshooting.
- Practical tip from the demos: when a "model doesn't have access" error appears, test the key against the provider's model list rather than guessing in code.

### 2.4 Where your sessions actually live
- Sessions, history, and per-project state are written to **`~/.claude/projects/...`** on your machine (that's how `/resume` and rewind can bring a past conversation back).
- This is your first hint that `.claude` is the control plane of the whole tool (Module 3).

### 2.5 Common install/run problems the course hits
| Symptom | Cause / fix |
|---|---|
| `claude: command not found` after install | Shell PATH not reloaded — open a new terminal |
| Installer seems frozen | It's downloading; wait, don't re-run in parallel |
| Works in one shell, not another (Windows) | You installed for PowerShell but opened CMD (or vice versa) |
| Exit code 1 right after install | Stale/mismatched install (e.g. uninstalled then reinstalled unclearly) — reinstall cleanly, or use the desktop/IDE path to diagnose |
| Auth loops | Log out and back in, or switch between subscription and API key |

### Check yourself
1. Which install path does the course recommend, and why does it warn about Windows shells specifically?
2. What exactly are you granting when you "trust this workspace"?
3. Where does the on-disk session history live, and which command uses it?

---

## Module 3 — Commands, permission modes, and the `.claude` directory
**Video:** 1:22:17 – 2:58:27 · **Why it matters:** this is your daily control panel.

### 3.1 Slash commands (the course demos 70+)
Commands are typed as `/name` inside a session. Categories with the ones that actually matter:

**Model & effort**
- `/model` — switch model mid-session. Warning shown: *"this conversation is cached for the current model — switching means full history gets read on your next message."* Switching is expensive; don't thrash between models.
- `/effort` (low / medium / high / max) — a "difficulty slider" for how much thinking the model does. High/max for complex work; low for quick chores.

**Cost, context, session**
- `/cost` (a.k.a. usage) — tokens, cost, duration, lines changed, plus how much of your subscription window you've used, broken down per model.
- `/context` — a visual breakdown of what's filling your context window (see Module 5).
- `/compact` — compress the conversation; you can (and should) pass instructions for what to preserve.
- `/clear` — start a **new session with empty context**; the previous session stays on disk.
- `/rewind` — jump back to an earlier point in the conversation.
- `/branch` (fork) — continue from the current point in a **new session with a new ID**, leaving the original intact. Perfect for "let's try an experiment without risking my working session".
- `/resume` — reopen a previous session.
- `/status` — version, model, and other session facts.

**Setup & integrations**
- `/init` — bootstrap a CLAUDE.md for the project (see Module 4).
- `/agents` — subagent library and manager (Module 9).
- `/mcp` — list, authenticate, and manage MCP servers (Module 8).
- `/plugins` (+ marketplace) — install capability bundles (Module 11).
- `/loop` — schedule a repeating task in the session (Module 12).
- `/login`, `/logout`, `/help`, `/permissions`, and **custom commands** you author in `.claude/commands/*.md`.

### 3.2 Permission modes — the safety model
The course calls this the most important — and most misunderstood — safety concept.

| Mode | Behaviour | Use when |
|---|---|---|
| **Default (standard)** | Asks before every edit/command; read-only actions run freely | Learning, sensitive repos |
| **Accept edits** | File edits + common FS commands (touch/mkdir/move/copy) auto-approved | Iterating on code you're reviewing |
| **Plan mode** | Read-only: explores and presents a plan *before* editing anything | Unfamiliar codebase, big change |
| **Auto** | Everything runs with a background safety check | Long tasks, avoiding "yes-fatigue" (course's recommended default once comfortable) |
| **Don't ask** | Only pre-approved tools can run | Locked-down CI/scripts |
| **Bypass permissions** | Everything runs except protected paths | **Only** isolated containers/VMs |

- **Shift+Tab** cycles the common modes in-session (normal → accept edits → plan).
- The "allow all edits in this session" option in a permission prompt is a shortcut to accept-edits-style behaviour — use it consciously.
- Whatever mode you're in, the goal is: *worst case, Claude should not delete anything or run a destructive command.* Combine modes with hooks (Module 7) and permission rules in `settings.json` for defence in depth.

### 3.3 The `.claude` directory
- It's a **hidden** directory (files starting with a dot). `ls` won't show it; `ls -la` will. Finder/Explorer hide it until you enable hidden files — intentionally, because most users never need it, but professionals do.
- Two important instances:
  - **Project scope** — `./.claude/` (travels with the repo, shareable with your team)
  - **User/global scope** — `~/.claude/` (your machine-wide config, preferences, agents)
  - (Enterprise/managed and local scopes also exist — see the CLAUDE.md hierarchy in Module 4.)
- Typical contents seen in the course and its resources:
  - `CLAUDE.md`, `CLAUDE.local.md`
  - `settings.json`, `settings.local.json`
  - `rules/` (e.g. `code-style.md`, `security.md`, `testing.md`)
  - `skills/`, `agents/`, `commands/`
  - `hooks/` (scripts) and hook config inside `settings.json`
  - `.mcp.json` (MCP server definitions)
  - `plugins/`, logs and session data
- **Precedence intuition:** the closer the config is to the project, the stronger it applies. Claude also reads its config *only* from these locations — files scattered elsewhere aren't picked up.
- Demo: the course creates a `.claude` folder from scratch, shows it invisible to `ls`, then walks the official "explore the .claude directory" docs page to map every part.

### Check yourself
1. Difference between `/compact`, `/clear`, and `/branch`?
2. Which permission mode is *read-only*, and when would you use bypass?
3. Why does `ls` not show `.claude`.

---

## Module 4 — CLAUDE.md: the project's permanent brain
**Video:** 2:58:27 – 3:43:48 · **Why it matters:** one file that removes 80% of repeated instructions.

### 4.1 The problem it solves
Without it, every session re-learns your project: wrong conventions, repeated mistakes, "why didn't you know we use pytest", instructions from three conversations ago forgotten. With it, Claude Code starts every session already knowing the stack, the commands, the rules, and how you verify work.

Add to CLAUDE.md when: the same mistake happens twice; a review catches something Claude should have known; you re-explain the same convention.

### 4.2 Where it lives — the priority hierarchy
From weakest to strongest (closest to the project wins):

1. **Enterprise / managed policy** (org-wide rules you can't override)
2. **User** — `~/.claude/CLAUDE.md` (your personal preferences across all projects)
3. **Project** — `./CLAUDE.md` or `./.claude/CLAUDE.md` (checked into the repo)
4. **Local** — `./CLAUDE.local.md` (your private project overrides, not committed)

Mechanics worth knowing:
- Claude Code **walks up the directory tree** from your working directory, loading CLAUDE.md and CLAUDE.local.md found along the way.
- You can **import** other files from CLAUDE.md (e.g. `@docs/architecture.md`), so the brain can be modular instead of one giant file.
- Memory/instruction files are injected into context (the course notes documented limits such as only the first ~200 lines of larger memory files loading — keep it tight).
- **HTML comments are stripped** before injection — use them for human notes that shouldn't cost context.

### 4.3 The conflict demo (understand precedence viscerally)
The instructor sets a global preference ("always give me Python") and then a project instruction ("I work and learn DSA in C++"). Asking for a bubble sort makes Claude surface the conflict and follow the project-level instruction — because it's closer to the work. Stated directly in the project ("give me all code in Java"), Claude obeys for the rest of the session. Lesson: **nearest scope wins; vague layering gets clarified, not silently guessed.**

### 4.4 What belongs in CLAUDE.md
| Belongs | Why |
|---|---|
| Project overview (what this is, for whom) | Frames every decision |
| **Essential commands** (build, test, lint, run, deploy) | Claude verifies instead of guessing — Anthropic's own guidance highlights this |
| Code style & naming conventions | Fewer review nitpicks |
| Project structure (key directories & files) | Faster navigation, fewer blind reads |
| Testing workflow | "Run tests right after implementing" |
| Hard rules / guardrails | e.g. never commit to main, never hardcode credentials, no silent failures, prefer explicit over clever |
| Verification checklist | e.g. run typecheck + tests after changes; screenshot UI and compare to the requirement; verify DB changes with a query; ask rather than assume |
| Pointers to further docs | Keep the file small |

| Does **not** belong | Why |
|---|---|
| Entire API documentation | Bloats every single request |
| Code snippets that will drift | They go stale silently |
| Outdated instructions | Worse than none |
| Task-specific instructions | Belongs in the prompt, not the permanent brain |
| Secrets | Never |

### 4.5 Bootstrap it fast
- Run `/init` and let Claude draft it from the repository, then edit ruthlessly.
- The course's own trick: copy the official Anthropic memory/best-practices pages, hand them to an AI, and ask it to draft a CLAUDE.md for *your* project. (Their resources repo includes a `CLAUDE_md_best_practices.ipynb` doing exactly this.)
- Keep it a living file: every repeated correction is a line that belongs in CLAUDE.md.

### Check yourself
1. Order the scopes by priority, strongest first.
2. Give two examples of content that should *not* be in CLAUDE.md, and the reason.
3. How does a fresh session discover instructions in a parent directory?

---

## Module 5 — Context management: the skill that decides your bill and your quality
**Video:** 3:43:48 – 4:31:35 · **Why it matters:** most "the AI got dumber" stories are context stories.

### 5.1 What's actually being sent
- LLMs are **stateless**. Each turn, the entire conversation so far is re-sent, plus a fixed overhead:
  - **System prompt** (rules, product instructions)
  - **Tools** (definitions of what the agent can do)
  - **MCP servers/tools** (every connected server's capability list)
  - **Skills** (name/description until invoked)
  - **CLAUDE.md** and memory
  - **Messages** (your whole conversation) and a reserved **auto-compact buffer**
- The course demonstrates the official context visualiser: before you type anything, ~7–8K tokens are already used (system + memory + MCP + skills + CLAUDE.md). Just sending "hi" in a real session showed ~29.5K/200K used with the system prompt alone at ~3.1% (6.2K tokens) — the breakdown differs slightly between terminal and VS Code because tool sets differ.

### 5.2 Why bigger isn't better: context rot
- Models show **primacy/recency bias**: they attend more to the beginning and the end of a long context and can lose the middle.
- Symptoms as context fills:
  - Instructions from CLAUDE.md get ignored
  - Repeated work / re-explaining
  - Mistakes it wouldn't have made 20 messages ago
  - More expensive and slower **every** message
- Key reframing from the course: it isn't Claude getting worse, it's **you not managing the resource**. Context is a limited desk — the course's analogy is a fixed-width port.

### 5.3 The cost maths (why hygiene is money)
- Input tokens are billed **per million, per call** — and the whole history goes in every call.
- The course's worked example: at ~200K tokens of context, the next **five** messages cost roughly **$3** on Sonnet; the following 5–10 messages another $3–5. Same information, repeatedly paid for.
- During the capstone the instructor demonstrates a single message sent with a bloated context costing about **$0.10** — a visceral way to remember to compact *before* a big ask.
- Subscription users aren't immune: it's a rate limit and a quality problem instead of a bill.

### 5.4 The toolkit
| Tool | What it does | When |
|---|---|---|
| `/context` | Shows the breakdown (system/tools/MCP/skills/CLAUDE.md/messages/free space/buffer) | Whenever things feel off |
| `/compact` | Compresses history into a summary; **you can pass instructions** ("keep the file structure, all API endpoints, the React component structure and the established Python patterns") | Long session you must continue |
| `/clear` | Brand new session, empty context; old session remains on disk | New task / changed topic |
| New session + status file | Re-open a fresh session and point it at a `CHANGELOG.md`/status doc so it can catch up cheaply | Between work phases |
| Specific prompts | Narrow scope = fewer file reads = less context & cost | Always |

### 5.5 Token budgeting: what you can and cannot control
**Can control:** CLAUDE.md size, which MCP servers are enabled (each description costs context), skills you install, session length, model & effort, how specific your prompts are, whether you paste whole files/screenshots.
**Cannot control:** platform system prompt, core tool definitions.
**Therefore:** keep permanent files tight; enable only the MCP servers you need; start fresh per task; compact with intent instead of letting auto-compact decide; and never re-paste a 50K-token codebase "just so it knows" — use subagents (Module 9) instead.

### Check yourself
1. Why does a 20-message-old instruction often get ignored even under the limit?
2. When should you `/compact` versus `/clear`?
3. Name three context costs you directly control.

---

## Module 6 — Skills: reusable playbooks
**Video:** 4:31:35 – 5:40:13 · **Why it matters:** turns "I keep re-explaining a workflow" into a two-word command.

### 6.1 The idea
A **skill** is a folder containing a Markdown instruction file plus optional scripts, references, and assets. It's procedural knowledge Claude can invoke:
- **On demand** via its trigger/slash name (`/morning-briefing`), or
- **Automatically** when the task matches the description.
- Crucially, a skill's full body is **not** loaded into context until it's used — only its name/description sits in context as an index. This is progressive disclosure, and it's why skills don't cost you tokens at rest.

The course's driving analogy: skills are the AI equivalent of a learned routine. Once you can drive, you can drive any car — the skill transfers; and just as your driving skill doesn't let you fly a plane, a skill applies to its intended scope.

### 6.2 Anatomy of a skill
```markdown
---
name: generate-report                # invocation name
description: Generates a daily project status report ... Use when asked to
  generate a report, summarise the codebase, or create a status update.   # ← this drives auto-invocation
trigger: /generate-report            # explicit slash trigger
argument-hint: "path/to/data.csv"
effort: low                          # optional: cheaper thinking for routine work
---

# Goal
...
# Inputs
...
# Steps
1. ...
2. ...
# Rules / references
See ./scripts/01_eda.py and ./references/toolkit.md
```
- Folder conventions seen in the course's resources: `SKILL.md`, `scripts/`, `references/`, `assets/`, plus `requirements.txt` / config templates so results are reproducible.
- Write for a **new teammate**: sequencing, exact commands, expected output format, and edge cases.

### 6.3 Where skills live
- Project: `.claude/skills/<skill-name>/SKILL.md` (shared via git)
- Personal: `~/.claude/skills/...` (available across projects)
- Plugins: shipped inside a plugin bundle (Module 11)
- The concept is shared across Claude surfaces (Claude AI, co-work, Claude Code) — a skill you build is portable.

### 6.4 Three examples worth imitating
1. **Deterministic output skill** (`expense-summary`): reads two JSON files directly (explicitly *not* via HTTP), then prints a summary in an **exact layout**, with documented calculation rules (units, rounding, sorting, empty-data behaviour) and a sample output. Lesson: when the *format* matters, specify it literally.
2. **Scripted skill** (`morning-briefing`): contains a bash script that curls your local API, parses with `jq`, and prints a briefing + task stats. Lesson: move deterministic work into a script — it runs the same way every time and costs no generation tokens.
3. **Pipeline skill** (`kaggle-data-analysis`): a 5-phase workflow (EDA → preprocessing → feature engineering → statistics → reporting) where each phase points at a numbered script with concrete CLI examples. Lesson: multi-file skills make Claude a *guide* to a process rather than a code generator.

### 6.5 Skills 2.0 — let Claude write the skill
- The course uses a **skill-creator** skill: you describe what you want, it asks clarifying questions (project/personal scope, language, components), then generates `SKILL.md` + scripts + references + assets + requirements.
- Then refine: add **arguments** (e.g. dataset name, output directory), set `model`/`effort` per skill, and iterate. The instructor's summary: skills are the simplest concept with the highest leverage — and because they're invoked only when needed, they don't inflate your baseline context.

### 6.6 Skills vs the neighbours
| Thing | What it is | Context cost | Runs where |
|---|---|---|---|
| Slash command (custom) | A saved prompt/expansion | Loaded when invoked | Main session |
| Skill | Procedure + optional scripts/assets | Description only until invoked | Main session |
| Hook | Event-triggered script | **Zero** | Outside the model |
| Subagent | Separate worker with own context | Summary returned only | Its own context window |

### Check yourself
1. Why does adding 20 skills not blow up your context?
2. When should a skill include a script rather than instructions?
3. What does the `description` field control that the body doesn't?

---

## Module 7 — Hooks: background automation with zero tokens
**Video:** 5:40:13 – 6:49:12 · **Why it matters:** guarantees, not suggestions. Hooks always run; prompts can be forgotten.

### 7.1 What hooks are
Shell commands (or Python/bash scripts) fired by **lifecycle events** in Claude Code. They run **outside the model**: no tokens, no prompting, deterministic, and fast. Typical uses from the course: auto-formatting, security guardrails, session logging, notifications, and small deterministic edits (e.g. rewriting an em dash style — a job you'd otherwise spend a prompt on every time).

### 7.2 Events you can hook
`SessionStart` · `UserPromptSubmit` · prompt expansion · `PreToolUse` · permission request / denial · `PostToolUse` · `Notification` · subagent start/stop/failure · task created/completed · `Stop` (Claude finished responding) · `SessionEnd` · pre-compact and similar.

The naming tells you the moment; design rule: **block/verify before (`PreToolUse`), fix/log after (`PostToolUse`), announce around the session (`SessionStart`/`Stop`).**

### 7.3 Configuration shape
```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash",
        "hooks": [ { "type": "command",
                     "command": "python .claude/hooks/security_guard.py",
                     "timeout": 10 } ] }
    ],
    "PostToolUse": [
      { "matcher": "Write|Edit",
        "hooks": [ { "type": "command",
                     "command": "python .claude/hooks/auto_format.py",
                     "timeout": 30 },
                   { "type": "command",
                     "command": "python ${CLAUDE_PLUGIN_ROOT}/hooks/session_logger.py",
                     "async": true } ] }
    ]
  }
}
```
- `matcher` selects events by tool name (`Bash`, `Write|Edit`, regex).
- `timeout` guards against a hanging script; `async: true` lets Claude continue while the hook runs.
- Hooks live in `settings.json` — and the course strongly advises: **let Claude Code add the first hook for you**, because hand-writing settings while the tool is initialising can get it overwritten. Inspect and extend afterwards.

### 7.4 The contract: input, exit codes, output
- **Input:** JSON on stdin, including `tool_name` and `tool_input` (e.g. the exact bash command, the file path).
- **Exit code 0** → allow / continue.
- **Exit code 2** → **block the action**; stderr is sent back to Claude as the reason. This is the emergency brake — the instructor's mnemonic: *"you shall not pass"*. Other non-zero codes are non-blocking errors.
- **Advanced output:** print JSON instead, e.g. a `hookSpecificOutput` with `permissionDecision: "deny"` and a reason — used in the course's `block-rm.sh` (jq-based) example.
- Why exit 2 matters: in bypass/auto modes nothing else is asking you. A hook that exits 2 stops the action even then.

### 7.5 Four demos to copy
1. **Notification hook** — macOS `osascript` (with Linux/Windows equivalents) that pings you when Claude needs input. Solves the "I walked away and it's been waiting 20 minutes" problem.
2. **Security guard (`PreToolUse` on Bash)** — Python script matching a regex blocklist (`rm -rf /`, `rm -rf *`, `git reset --hard`, `DROP TABLE/DATABASE`, `chmod 777`, `curl … | bash`, `wget … | sh`), printing the reason and `exit(2)`. Then demonstrate: asking Claude to `rm -rf output/` gets **blocked with an explanation**, and Claude proposes a safer alternative. The instructor deliberately tests the guard rather than trusting it.
3. **Auto-format (`PostToolUse` on `Write|Edit`)** — after every write, run `black` for `.py` and `prettier` for JS/TS/JSON/CSS, log the result, optionally `async`. Demo: ask for a deliberately messy `messy.py` and watch it become clean seconds later. Note the course's demo sleep/log line is a teaching crutch — keep hooks fast.
4. **Session logging (`SessionStart` / `Stop` / on `Bash`)** — append structured lines to a log file so you can reconstruct what happened while you were away.

### 7.6 Gotchas
- Hooks are **code with your permissions** — a buggy hook can break every edit. Test by hand first (`echo '{...}' | python hook.py; echo $?`).
- Keep them fast and side-effect-light; use `timeout` and `async` where appropriate.
- Prefer hooks for *policy* (block dangerous things) and *hygiene* (format/log); don't abuse them to make decisions that need reasoning.

### Check yourself
1. Why are hooks cheaper than asking Claude to do the same thing?
2. What is the difference between exit code 1 and exit code 2 from a hook?
3. Where does the hook configuration live, and why let Claude write the first one?

---

## Module 8 — MCP: connecting Claude to the outside world
**Video:** 6:49:12 – 8:20:17 · **Why it matters:** it's the difference between an assistant that knows about your tools and one that can use them.

### 8.1 The problem MCP solves
Without a standard, connecting Claude to Gmail, Slack, GitHub, a database, or a browser means writing and **maintaining** custom integrations for each. Every change in the target API breaks your glue code — and millions of people would be writing the same glue.

**MCP (Model Context Protocol)** is an open standard defining how AI agents talk to external tools and data sources. The course's mental model: **MCP is a toolbox — or a tool library — you don't have to maintain.** Instead of building and fixing your own hammer and screwdriver, you ask to be connected to the workshop that supplies them.

### 8.2 Connectors vs MCP
- **Connectors**: vendor-provided, ready-made integrations surfaced inside Claude products (turn on Gmail in Claude and it's connected).
- **MCP**: the open protocol — you (or a provider) run/point at an MCP **server**; Claude Code is the **client**. More work to set up, far more extensible, works with any server anyone publishes.

### 8.3 Local vs hosted servers
| | Local (stdio) | Hosted / remote (HTTP/SSE) |
|---|---|---|
| Runs on | Your machine, as a process | Provider's infrastructure |
| Setup | Command + args in config | URL (+ headers/API key) |
| Resource use | Your CPU/RAM (course notes small VMs/RAM limits as a real constraint) | Theirs |
| Ideal for | File access, Playwright/browser automation, private tools | Gmail, Slack, Tavily, GitHub — anything vendor-run |
| Failure mode | Crashing process, missing runtime, RAM | Auth/credits/network |

### 8.4 Configuring MCP in Claude Code
Project-root `.mcp.json` (or `.claude/.mcp.json`):
```json
{
  "mcpServers": {
    "tavily-remote-mcp": {
      "type": "http",
      "url": "https://mcp.tavily.com/mcp/",
      "headers": { "X-API-Key": "${TAVILY_API_KEY}" }
    }
  }
}
```
- Use **environment variables** for secrets — never commit keys.
- **Scopes** (the course highlights this table): project-shared (committed, whole team) → user (your account, all projects) → local (private, e.g. `*.local.json`, not committed). Choose per server: team tooling in project scope, personal credentials in local scope.
- `settings.json` can pre-approve servers (`enabledMcpjsonServers`) and grant tool permissions (e.g. `mcp__plugin_playwright_playwright__browser_*`).
- `/mcp` lists servers, shows their tools, and handles authentication.
- **Remember the context cost:** every connected server's tool descriptions go into context on every request. Enable what you need; disable the rest.

### 8.5 What it looks like in practice
- **Gmail via MCP** — once connected, "read my email", "create a draft reply", "search threads" become plain-language instructions; under the hood MCP calls the Gmail API (the course points at `create draft`, `list labels`, `search threads`).
- **Tavily (search/research)** — exposes `search`, `extract`, `crawl`, `map` plus a heavier `research` tool. Demo shows Claude choosing tools, asking permission, returning results it then *rewrites* into readable form — the raw tool JSON is ugly, the model's summary is the product. Caution shown live: `research` burned ~250 credits on one query — know your tools' costs.
- **Browser automation (Playwright MCP)** — Claude drives a real browser, takes screenshots, reads results, closes the browser. Heavy for small machines.
- A recurring lesson: **if you don't know your tools, the model picks badly** (it mixed up built-in web search and Tavily's research tool until told which to use).

### 8.6 Building your own MCP server
The course asks Claude Code to build a small **calculator server** from scratch — a perfect anatomy lesson:
- A server exposes **tools** (functions): `add`, `subtract`, `multiply`, `divide`, `power`, `square_root`, `average`, plus `list_tools`/`call_tool` plumbing.
- Each tool has a **name, description, and JSON-schema parameters** (types, required fields). That description is *exactly* what the model reads when deciding whether/how to call it — so tool descriptions are prompt engineering.
- Register the server locally (in `.mcp.json` / local scope), restart, and it appears as an available tool. Then "what is 5 + 9" routes through your server.
- Any function can be arbitrarily complex — including calling an LLM inside — the protocol doesn't care.

### Check yourself
1. Give the one-sentence definition of MCP and the toolbox analogy.
2. When do you want a local server, and when a hosted one?
3. Why do too many MCP servers make Claude *worse*?

---

## Module 9 — Subagents: isolated specialists
**Video:** 8:20:17 – 9:51:44 · **Why it matters:** the cleanest solution to context bloat and to repetitive delegation.

### 9.1 The concept
A **subagent** is a specialised worker with **its own context window**, its own system prompt, its own tool permissions, and (optionally) its own cheaper model. Your main session delegates a job; the subagent does the heavy reading/exploring in *its* context; only a **summary** comes back. The main session stays clean.

The course's framing: you're a manager. You don't read every file yourself — you hand the task to the right specialist and get a report.

### 9.2 Why use them
| Benefit | Explanation |
|---|---|
| **Context hygiene** | The 50K tokens of file reads happen in the subagent, not in your main thread |
| **Cost control** | Routine work can run on Haiku while the parent stays on Sonnet/Opus |
| **Focus** | A specialist prompt ("you are a security auditor, report only findings") outperforms a generalist asked to do it all |
| **Parallelism** | Several subagents can run at once, each isolated |
| **Safety** | Tools can be restricted (`tools` / `disallowedTools`) — "an intern who can't see your bank statements" |

### 9.3 Anatomy of a subagent file
```markdown
---
name: planner
description: >
  Reads requirements from CLAUDE.md and produces a detailed implementation
  plan in PLAN.md. Use at the START of any new project or feature, before any
  code is written. Never writes code — only plans.        # drives auto-delegation
tools: Read, Glob, Grep, Write
disallowedTools: Bash, Edit
model: haiku
effort: high
color: cyan
---

You are a senior software architect. Your only job is to read requirements and
produce a crystal-clear implementation plan. You never write code.
## Your Process
1. Read CLAUDE.md thoroughly ...
2. Analyse the scope ...
3. Write PLAN.md with this exact structure: ...
```
- `description` is critical: it's how the main agent decides **when** to delegate.
- Restrict `tools` ruthlessly; that's your safety and quality boundary.
- Model choice per worker is a running-cost decision.

### 9.4 Where they live
- Project: `.claude/agents/*.md` (committed, shared)
- User: `~/.claude/agents/*.md` (personal, all projects)
- Inside plugins.
The course demonstrates both a project agent (`code-quality-reviewer-project`) and a global one (`code-reviewer-agent`).

### 9.5 Three ways to invoke
| Method | Control | Notes |
|---|---|---|
| Natural language ("explore my codebase") | Low | Claude picks a matching agent by description; can misfire with many agents |
| Explicit mention (`@code-reviewer …`) | Medium–high | Names the worker |
| `/agents` manager / slash invocation | Highest | Library UI: view, create, edit, set model |

`/agents` is also the creation UI — useful when you'd rather not hand-write frontmatter. The course builds one from scratch, sets its model, and watches it appear in the library (colour-coded in the UI).

### 9.6 Demos & patterns from the course
- Ask the main session to "go through the complete code, each and every file" → Claude delegates to an **explore** agent, reading in parallel batches instead of stuffing everything into the main context.
- A **planner** agent that never writes code, only writes `PLAN.md`.
- A **pipeline** of agents in the course's Task-Manager resources: planner → code-writer → service-writer → test-writer → quality-improver → security-auditor, each with restricted tools and a single responsibility.
- Rule of thumb to adopt: **if the work involves reading a lot to produce a little, make it a subagent.**

### Check yourself
1. What comes back to the main session from a subagent, and what doesn't?
2. Which frontmatter field decides automatic delegation?
3. Why would you give a subagent `disallowedTools: Bash, Edit`?

---

## Module 10 — Agent teams: multiple Claude instances on one project
**Video:** 9:51:44 – 10:35:46 · **Why it matters:** the frontier of parallel agentic work — powerful, still experimental, needs discipline.

### 10.1 The concept
If subagents are workers **reporting to one manager**, an **agent team** is several Claude instances **coordinating with each other** on the same project: a **team lead** plus **teammates**, each with its own context, working simultaneously and messaging each other (e.g. the backend teammate publishing the API contract so frontend and QA can build against it).

### 10.2 Subagents vs agent teams
| | Subagents | Agent teams |
|---|---|---|
| Topology | Parent → worker(s), report back | Peer-to-peer coordination + lead |
| Communication | Return value to parent | Teammates message each other |
| Context | Isolated per subagent | Isolated per teammate (sessions) |
| Concurrency | Parallel, fire-and-forget | Persistent, simultaneous sessions |
| Control | Manage via `/agents` | Shift+Down to switch views; display modes (in-process / split panes) |
| Maturity | Stable, everyday tool | **Experimental** (some things will not work) |
| Cost | Low–moderate | High — multiple live contexts |

### 10.3 How the course enables and runs it
- Project settings need the experimental flag:
  ```json
  { "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" } }
  ```
- Team shape: **team lead** (plans, spawns, merges) + **teammates** (backend, frontend, QA).
- With the demo prompt, teammates are told to coordinate on the API contract **before** writing code, then merge branches and report.
- **Git worktrees are the mechanism** that makes this safe: each teammate works on its own branch/checkout of the repo, so parallel edits don't trample each other; the lead merges at the end. (Worktrees are a plain git feature, not an AI feature — the course explains them as "multiple versions of the code, like version history in a docs editor".)
- Practical notes from the demo: switching teammate views is `Shift+Down`; some UI states show queued tasks; the instructor confirms the feature was Opus-only at launch on some surfaces and later relaxed — i.e. **expect this area to change**, and check the docs.

### 10.4 When to use it (and when not)
- **Use** for genuinely separable workstreams with a clean interface (API contract, shared schema) and for long builds you're happy to supervise.
- **Don't** for small changes (coordination overhead exceeds the benefit), or when you can't tolerate merge/conflict review.
- Always: one source of truth for interfaces, branch discipline, and a final human review.

### Check yourself
1. State the structural difference between a subagent and a team mate.
2. What does git worktree contribute, and why is it necessary here?
3. Name one risk that doesn't exist with a single session.

---

## Module 11 — Plugins & marketplace: bundle and share your setup
**Video:** 10:35:46 – 11:07:28 · **Why it matters:** the difference between "my clever config" and "my team's standard".

### 11.1 What a plugin is
A versioned bundle that can contain **agents + skills + commands + hooks + MCP servers + settings + CLAUDE.md**, installable in one step and shareable via git or a marketplace. Instead of emailing config files, you point someone at a plugin.

### 11.2 Anatomy
```
.claude-plugin/quicktask/
├── plugin.json            # name, version, description, author, keywords,
│                          # agents: ./agents/, skills: ./skills/, hooks: ./hooks.json
├── hooks.json             # event → matcher → command (${CLAUDE_PLUGIN_ROOT}/hooks/…)
├── hooks/                 # auto_format.py, session_logger.py
├── agents/                # planner.md, code-writer.md, test-writer.md, security-auditor.md …
├── skills/build-app/SKILL.md
├── settings.json.template
└── README.md              # what's inside, how to enable, standards
```
- `plugin.json` is the manifest that makes Claude Code recognise the directory.
- Hook commands use `${CLAUDE_PLUGIN_ROOT}` so they work wherever the plugin is installed.
- Note the symmetry with the resources repo: the same content that lives in `.claude/` (agents, skills, hooks, settings) is exactly what gets packaged.

### 11.3 Installing and using
- `/plugins` opens the manager: **installed plugins**, **marketplaces**, install/enable/disable, refresh, uninstall.
- **Add a marketplace**: point it at a GitHub repo URL (or path). Then browse and install plugins from it. Anthropic runs an **official** marketplace; community marketplaces exist too.
- **Security note the course makes explicitly:** community plugins are **not reviewed by Anthropic** — check stars/forks, read the hooks and commands (they execute with your permissions), and treat installation as running someone else's code.
- Enablement is recorded in settings (`enabledPlugins`), so a team can share a plugin *and* the switch that turns it on.

### 11.4 Creating / sharing your own
Two routes, both demoed:
1. **Ask Claude** — "create a plugin from my `.claude` folder in this project" → it scaffolds the manifest, copies agents/skills/hooks, and can enable it for you.
2. **Hand-roll** — create `.claude-plugin/<name>/`, write `plugin.json`, move content in, test.
Then: commit the plugin directory to the repo and add it to project settings — **team members get it automatically when they pull**, which is the whole point.

### Check yourself
1. Name five things a plugin can bundle.
2. Why is `${CLAUDE_PLUGIN_ROOT}` used in plugin hook paths?
3. What due diligence does the course insist on before installing a community plugin?

---

## Module 12 — Scheduling & automation: making Claude work without you
**Video:** 11:07:28 – 11:56:47 · **Why it matters:** the payoff module — automation that survives you closing the laptop.

### 12.1 The framing: cron with judgement
- A **cron job** runs a script on a schedule and fails silently: if the API errors, the script exits, nobody knows, and you debug by reading logs hours later.
- A **scheduled Claude task** reads the error, tries an alternative, documents both failures, sends a notification with a diagnosis, and suggests a fix. The course's summary: **reasoning, not just execution.**
- Cron syntax refresher (still worth knowing, still used): `minute hour day-of-month month day-of-week` — e.g. "MWF at 8am". Generate it with an AI rather than memorising.

### 12.2 The three ways to schedule
| | `/loop` | Desktop scheduled task | **Claude routine** |
|---|---|---|---|
| Runs on | Your machine, current session | Your machine | Anthropic's cloud |
| Machine must be on | Yes | Yes | **No** |
| Session must be open | Yes | Task app running | No |
| Persistence | Until expiry (~3 days) unless persistent | Yes | Yes |
| Local file access | Yes | Yes | Fresh clone of your repo |
| MCP/permissions | Inherited from session | Configured | Configured (GitHub, Slack, etc.) |
| Minimum interval | 1 minute | — | Cron schedule |
| Best for | Watching something now (deploys, logs, PRs) | Local dashboards/processes | Unattended recurring work, event-driven CI-style jobs |
| Triggers | Interval/cron | Time | Schedule, API, **GitHub events** |

**`/loop` details:** `/loop <interval> <prompt or /command>`; runs in the current session, inherits MCP servers and permissions, and stops when you close the session or after its expiry. Classic demo: watch `deploy.log` every 2 minutes and report/stop when the deployment finishes — including the failure branch.

**Headless mode:** `claude -p "<prompt>"` (optionally with `--allowedTools`, or `--dangerously-skip-permissions` **only** in an isolated environment) runs with no UI and **never stops to ask** — the missing piece for cron/systemd/CI, because a scheduled run that halts for a permission prompt is a broken schedule. Important nuance from the course: headless isn't a permission bypass — it still respects permissions; it's just *without an interface*.

**Claude routines:** cloud infrastructure, triggered by a schedule, an API call, or **GitHub events** (PR opened/merged, release published, issue opened) with filters on author/title/body/regex. A fresh clone of your repo is spun up with your tools/MCP servers, the work happens (files written, PRs opened, messages sent, reports generated), and **it runs while your laptop is closed**. The course walks the UI (schedule API, credentials, agent spin-up, results).

### 12.3 Recipes worth stealing
- **PR review bot** — on PR open: read the diff, post an initial review comment (routine + GitHub event).
- **Daily data pipeline** — 6am: run the data-quality skill, write output, post errors to Slack (routine).
- **Weekly code quality** — Sunday 11pm: test results, coverage, security scan (routine).
- **Monday planning** — 8am: read last night's report, produce a prioritised task list, assign via GitHub (routine).
- **Continuous docs** — on push to main: read changed files, update docs (routine).
- **Local dashboard** — read/process data, generate a daily dashboard, email stakeholders via MCP (desktop task).
- **Deploy watcher** — `/loop` every 2 minutes over `deploy.log` until success/failure.

### 12.4 Safety — the part you must not skip
A scheduled agent can read and write files, run bash, call external APIs, commit code, open PRs, and send messages — with no one watching. The course's five rules:

1. **Start read-only.** Schedule analysis before action.
2. **Write to non-destructive paths.** Reports to a folder, or out to Slack/MCP, so a bad run can't destroy the source of truth.
3. **Human review gates for irreversible actions.** *Bad:* "deploy when tests pass." *Good:* "when tests pass, write `READY-TO-DEPLOY.md` and ask a human on Slack to deploy." Same for linting: *bad* "fix all lint errors" → *good* "identify lint errors, write the list to `reports/lint-issues.md`, do not modify source".
4. **Log everything.** You won't be watching the terminal; structured logs are your only forensic trail.
5. **Test for days before trusting it.** Run the headless command by hand first; watch it for several cycles before letting it run unattended.

Also mentioned: a settings escape hatch (e.g. disabling automatic repo cloning) and awareness of usage limits/extra-usage toggles — scheduled agents can burn sessions fast.

### Check yourself
1. Give the three scheduling options with their "does my laptop need to be on" answers.
2. Why is headless mode necessary for trustworthy schedules?
3. Rewrite this bad automation as a safe one: "every night, fix any failing tests and push."

---

## Module 13 — Capstone: DailyPulse (full-stack, spec-first build)
**Video:** 11:56:47 – 13:53:46 · **Why it matters:** every concept from modules 1–12 is used, unforced, in one build.

### 13.1 What gets built
**DailyPulse** — a personal productivity web app:
- **Morning briefing** (fetched/generated each day)
- **Smart tasks** — the AI breaks a task title into 3–5 subtasks
- **Standup generator** — turns today's completed tasks into a standup summary
- **Daily insights** — patterns in your completed tasks
- Plus: weather widget, real-time AI news feed, confetti/UI polish.

### 13.2 The build order (copy this sequence)
1. **Spec & structure first.** Create the project, then write **CLAUDE.md** describing the stack, standards, key files, commands, and data models. Prepare a **prompts file** — the course writes the build prompts ahead of time and pastes them one by one.
2. **Hooks before code.** Add a `PostToolUse` auto-format hook (black on Python after Write/Edit) and a `Stop` hook message — set the guardrails before generating files.
3. **Backend** — FastAPI, thin route layer over a services module, JSON-file storage, endpoints for tasks/briefing/standup/insights, CORS middleware, `requirements.txt`.
4. **Test the endpoints** — curl/browser the API before touching the UI.
5. **Frontend** — React + Vite (+ Tailwind), components for briefing, tasks, standup, insights, header/weather; `fetch` to the backend.
6. **Fix bugs & CORS** — the classic full-stack moment: browser blocked by CORS, ports mismatched, etc. Course method: take a (compressed) screenshot of the broken page and paste it with "fix this".
7. **Real-time news via Tavily** — an MCP-backed/news API integration so the app shows current AI news.
8. **Schedule it with cron** — the app updates itself (briefing generation) on a schedule.
9. **Recap** — map each feature back to the module that taught it.

### 13.3 The teaching moments (more valuable than the app)
| Moment | Lesson |
|---|---|
| Prompts written in advance, one at a time | Behave like a tech lead: specify *what* and *where*, don't let the model invent your architecture |
| Using a second AI (ChatGPT/Claude chat) as "CTO" to draft the technical prompts | Two-AI pattern: one for decisions, one for execution |
| Hooks and CLAUDE.md created before code | Set up your factory before manufacturing |
| `/compact` with explicit instructions mid-build | "Keep the file structure, all API endpoints, the React component structure and the established patterns" — never let auto-compact choose what to forget |
| Screenshot + "fix this" for UI bugs; compress images first | Images consume context → compress before pasting |
| Gemini quota → OpenRouter fallback; a typo in the key → auth error | App-level AI needs its own API key (a subscription doesn't power your app); when debugging, isolate key vs code |
| "Fix it so it only creates tasks that way when AI isn't available" | Graceful degradation: the app must work when the AI provider fails |
| A single message after heavy context cost ~$0.10 | Compacting *before* a big request is explicitly cheaper |
| Session limits hit mid-build; extra-usage toggle appears | Budget limits are part of the workflow — plan model/context usage |
| The last 20% (polish, logging, error states, tests) takes real human effort | AI gets you ~80% fast; the remainder is where quality lives |

### 13.4 The completed project shape (from the course's resources)
```
DailyPulse/
├── .claude/
│   ├── CLAUDE.md                 # project brain: stack, standards, key files
│   ├── settings.json             # hooks: black on .py, Stop message
│   └── skills/
│       ├── morning-briefing/skill.md
│       └── generate-standup/skill.md
├── backend/
│   ├── main.py                   # FastAPI routes
│   ├── services.py               # business logic + AI calls
│   ├── generate_briefing.py
│   ├── requirements.txt
│   └── data/{tasks.json,briefing.json}
└── frontend/                     # React + Vite
    └── src/components/{MorningBriefing,TaskManager,StandupGenerator,
                        DailyInsights,WeatherWidget,Header,…}.jsx
```

### 13.5 Where to take it next
Deploy (backend on Render, frontend on Vercel), add auth, replace JSON with a database, add tests, turn the briefing into a scheduled routine that messages you each morning — i.e. re-apply modules 7, 9 and 12 to your own product.

### Check yourself
1. Why write CLAUDE.md and hooks *before* generating application code?
2. What did the instructor do wrong that cost $0.10 on one message?
3. Which modules does the capstone exercise, and where?

---

## Big-picture recap: the twelve levers

| Lever | Module | One-line purpose |
|---|---|---|
| Model choice | 1 | Match intelligence/cost to the job |
| Terminal access | 1 | The "hands" — what makes action possible |
| Agentic loop | 1 | Plan → act → observe → retry |
| Permissions | 3 | Decide how much autonomy to grant |
| CLAUDE.md | 4 | Permanent project memory |
| Context hygiene | 5 | Keep quality high and costs low |
| Skills | 6 | Reusable procedures, no at-rest cost |
| Hooks | 7 | Guaranteed, zero-token automation |
| MCP | 8 | Connect to real tools and data |
| Subagents | 9 | Isolated, cheap, specialised workers |
| Agent teams | 10 | Parallel instances with coordination |
| Plugins | 11 | Bundle and share the whole setup |
| Scheduling | 12 | Work that happens without you |

**And the honest caveat the course ends on:** not every project needs all of them. Knowing they exist is the edge — the failure mode is people spending hours doing by hand what a hook, skill, or subagent would have done automatically.
