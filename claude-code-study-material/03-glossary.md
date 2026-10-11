# Glossary — Claude Code course terms in plain English

**Agent team** — Several Claude instances (a team lead plus teammates) working on the same project at the same time, in separate sessions, messaging each other. Teammates typically work in their own git worktree; the lead merges. Experimental. ⚠️

**Agentic loop** — The core cycle Claude runs: plan → act (read/write/run) → observe → check → retry or answer. The "secret" behind why Claude Code feels smart: fast iteration, not magic.

**Anthropic** — The company that builds Claude. Founded by former OpenAI people; positions itself as safety-first.

**API key** — A credential for pay-per-token access to a model. Separate from a Claude subscription: your *app* needs an API key; your *Claude Code session* can run on a subscription. Different billing, different limits.

**Auto mode (permission mode)** — Runs actions with a background safety check instead of asking every time. The course's recommended default once you're comfortable.

**Auto-compact buffer** — Context space reserved so Claude can automatically summarise a long conversation before hitting the hard limit. Visible in `/context`.

**Bypass permissions** — Permission mode where nearly everything runs without asking. Only appropriate in isolated containers/VMs. ⚠️

**Chat vs Code (the brain/hands model)** — Claude chat (web/desktop) is a brain: it can advise, not act. Claude Code is the same brain *with hands* — the terminal, which can create/edit/delete files and run commands.

**Claude Code** — Anthropic's terminal-based coding agent. Installs on your machine so it can act on your files; powered by the same Claude models as the chat products.

**`CLAUDE.local.md`** — Private, per-project instruction file with the **highest** priority in the CLAUDE.md hierarchy. Typically git-ignored.

**`CLAUDE.md`** — The "project brain": a Markdown file of instructions (stack, commands, conventions, guardrails) that Claude Code loads automatically at session start. Lives at project root or in `.claude/`; a user-level version (`~/.claude/CLAUDE.md`) applies everywhere.

**`/clear` vs `/compact`** — `/clear` throws the conversation away and starts a fresh session (old one stays on disk). `/compact` summarises the current conversation in place so you can continue with less context.

**Command (custom slash command)** — A saved prompt stored as a Markdown file in `.claude/commands/`; typing its name expands it. (Different from a skill: no scripts/resources, no progressive loading.)

**Connector** — A ready-made, vendor-provided integration surfaced inside Claude products (e.g. Gmail). Easier than MCP; less extensible. MCP is the open standard underneath the broader ecosystem.

**Context rot** — Degradation as a session fills up: ignored instructions, repeated work, new mistakes. Caused by context volume plus models' tendency to weight the beginning and end of a long context more heavily (primacy/recency bias).

**Context window** — The token budget available for one request. Every turn re-sends system prompt + tools + MCP + skills + CLAUDE.md + message history. Fixed size; shared by everything.

**Cron** — Classic Unix time-based scheduler: `minute hour day-of-month month day-of-week`. Runs scripts blindly (fails silently). Scheduled Claude tasks are "cron with judgement" because they can reason about failures.

**`.claude` directory** — The hidden configuration folder that controls Claude Code: settings, CLAUDE.md, rules, skills, agents, commands, hooks, MCP config, plugins. Exists per project and per user (`~/.claude`).

**Desktop scheduled task** — A recurring Claude task run by your machine (e.g. the desktop app), so it needs the machine on; good for local files/processes.

**Effort** — `/effort` setting (low → max) controlling how much thinking budget the model spends on a request. A "difficulty slider".

**Extended / adaptive thinking** — Model features that let Claude deliberate longer before answering complex problems. Availability varies by model tier. ⚠️

**Git worktree** — A plain git feature allowing multiple working directories (branches) from one repository. Used by agent teams so each teammate edits its own copy without collisions.

**Haiku / Sonnet / Opus** — The three Claude model tiers: fast-and-cheap, balanced, most-capable. Course rule: Opus to plan, Sonnet to build, Haiku to maintain. ⚠️ versions change.

**Headless mode** — Running Claude Code with no interactive UI (`claude -p "…"`). Never blocks on a permission prompt, which is what makes cron/CI scheduling viable. It still enforces permissions — it simply has no interface.

**Hook** — A shell command/script that fires on lifecycle events (before/after tool use, session start/stop, notifications…). Runs outside the model: zero tokens, deterministic, and able to block actions (exit code 2).

**Hook matcher** — The pattern in settings.json that decides which tool events a hook fires on, e.g. `"Bash"` or `"Write|Edit"`.

**Hook exit code 2** — The "hard stop": the action is blocked and stderr is returned to Claude as the reason. Exit 0 allows; other non-zero codes are non-fatal errors. Mnemonic from the course: *you shall not pass*.

**Local MCP server** — An MCP server process running on your machine (stdio). Best for file access and browser automation; consumes your RAM (the course notes small machines struggling).

**Marketplace (plugins)** — A git-based catalogue of plugin bundles that Claude Code can browse and install from. Anthropic runs an official one; community ones are unreviewed → due diligence required.

**MCP (Model Context Protocol)** — Open standard defining how AI agents talk to external tools and data sources. The course's analogy: a toolbox you don't have to build or maintain — connect to the supplier instead of forging your own hammer.

**MCP scope** — Where an MCP server's config lives and who sees it: **project** (committed, whole team), **user** (all your projects), **local** (private, uncommitted, e.g. for secrets).

**Model Context / MCP tool definition** — The name, description, and JSON-schema parameters a server exposes. This is what the model reads when deciding which tool to call — so descriptions are effectively prompt engineering, and every connected server's list costs context.

**Permission mode** — How much autonomy Claude Code has: default (ask), accept-edits, plan (read-only), auto, don't-ask, bypass. Cycle common ones with `Shift+Tab`.

**Plan mode** — Read-only mode where Claude explores and presents a plan before being allowed to edit anything. Ideal for unfamiliar codebases and large changes.

**Plugin** — A versioned bundle containing agents, skills, commands, hooks, MCP servers, settings, and CLAUDE.md, installable in one step and shareable via git. Manifest lives at `.claude-plugin/<name>/plugin.json`.

**Progressive disclosure (skills)** — Only a skill's name and description occupy context until the skill is actually invoked; the full instructions and bundled scripts load on demand. Why you can install many skills cheaply.

**`/loop`** — Command that re-runs a prompt or slash command on an interval inside the current session (minimum interval ~1 minute, expires after ~3 days unless persistent ⚠️). Needs the machine on and the session open.

**Recency / primacy bias** — Models attending more strongly to the start and end of a long context; the middle gets "fuzzier". The mechanism behind context rot.

**Routine (Claude routine)** — Cloud-hosted scheduled automation: triggered by time, API, or GitHub events; spins up a fresh clone of your repo with your tools/MCP servers; runs even when your laptop is closed.

**Rules (`rules/`)** — Small Markdown files in `.claude/` holding focused policies (code style, security, testing) that complement CLAUDE.md.

**Settings.json** — The configuration file (project `.claude/settings.json`, or user-level) holding permissions, hooks, env vars, enabled plugins, and pre-approved MCP servers. `settings.local.json` for private overrides.

**Skill** — A reusable playbook: a folder with `SKILL.md` (frontmatter + instructions) plus optional scripts, references, and assets. Invoked by trigger or automatically by matching its description.

**Skill creator** — A skill whose job is to write other skills: asks clarifying questions, then scaffolds SKILL.md, scripts, references, and requirements.

**Slash command** — Any `/command` typed in a session: built-in (`/compact`, `/model`, `/context`…) or custom from `.claude/commands/`.

**Stateless (LLMs)** — Models remember nothing between calls. Continuity exists only because the entire conversation is re-sent each time — the reason context management *is* cost management.

**Subagent** — A specialised worker with its own context window, prompt, tool permissions, and (optionally) cheaper model. Delegated to from the main session and returns only a summary. Defined in `.claude/agents/*.md`.

**System prompt** — Fixed instructions Claude Code sends every turn (rules, product behaviour). Consumes context you can't edit, roughly 3% in the course's `/context` demo.

**Token** — The unit of text models read and bill for. More tokens = more cost, both input (re-sent every turn) and output. Output tokens are usually priced higher.

**Trust workspace prompt** — The one-time consent when opening a folder: Claude may read, write, and execute files there. Read it — this is the actual security boundary.

**Work tree (git)** — See *Git worktree*.

**`.mcp.json`** — Project file defining MCP servers (`mcpServers` object with type, url/command, headers). Secrets should reference environment variables (`${TAVILY_API_KEY}`), never literals.

**`enabledMcpjsonServers` / `enabledPlugins`** — settings.json keys that pre-approve project MCP servers and turn plugins on for everyone who shares the repo.
