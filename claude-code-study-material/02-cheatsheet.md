# Claude Code — Cheat Sheet

Companion to the study guide. Everything here comes from the course (Mayank Aggarwal, *Claude Code Full Course*, 2026). Version-specific values are flagged ⚠️ — re-verify against current docs.

---

## 1. Getting started

```bash
# macOS / Linux — one-line native install (from the official quickstart)
# Windows: use the PowerShell command, or the CMD command — match your shell
# Then, inside a project folder:
claude                 # start an interactive session
claude -p "prompt"     # headless: no UI, never stops to ask
claude --allowedTools "Read,Grep"        # restrict tools in headless mode
claude --dangerously-skip-permissions    # ONLY in an isolated container/VM

/init      # bootstrap a CLAUDE.md for this project
/login     # sign in (Anthropic account)
/logout    # sign out
/help      # list commands
/status    # version, model, session facts
```

**Install triage:** new terminal if `command not found` · match shell (PowerShell vs CMD) · don't re-run a "frozen" installer · clean reinstall if exit code 1 · Windows users: install Windows Terminal for a Unix-like experience.

---

## 2. Slash commands worth memorising

| Command | What it does | Tip |
|---|---|---|
| `/model` | Switch model mid-session | Switching re-reads full history — don't thrash |
| `/effort` | low / medium / high / max thinking budget | high+ for hard problems |
| `/cost` | Tokens, cost, duration, lines changed, plan usage | Check after long runs |
| `/context` | Visual breakdown of the context window | Use when quality degrades |
| `/compact [instructions]` | Compress history | Always pass what to preserve |
| `/clear` | New session, empty context (old one stays on disk) | Between unrelated tasks |
| `/rewind` | Go back to an earlier message | Undo a bad direction |
| `/branch` (fork) | Continue in a new session with a new ID | Try experiments safely |
| `/resume` | Reopen a previous session | After a break |
| `/agents` | Subagent library/manager | Create, edit, set models |
| `/mcp` | List/auth/manage MCP servers | Check which tools are live |
| `/plugins` (+ marketplace) | Install capability bundles | Read before enabling |
| `/loop` | Repeat a task in this session | Min interval 1 minute ⚠️ |
| `/permissions` | Inspect/manage permission rules | Pre-approve safe tools |
| `/init` | Generate CLAUDE.md | Then edit ruthlessly |

**Keyboard:** `Shift+Tab` cycles permission modes (normal → accept edits → plan) · `Esc` interrupts · `Shift+Down` switches agent-team teammate views ⚠️.

**Custom commands:** put a Markdown file in `.claude/commands/` (e.g. `pr-description.md`) → it becomes `/pr-description`.

---

## 3. Permission modes

| Mode | Behaviour | Use for |
|---|---|---|
| Default | Ask every time | Learning, sensitive repos |
| Accept edits | Auto-approve file edits + common FS commands | Iterating on code |
| Plan | Read-only; presents a plan first | Unfamiliar codebases |
| Auto | Runs with background safety checks | Long tasks (course's recommendation) |
| Don't ask | Only pre-approved tools | Locked-down CI/scripts |
| Bypass permissions ⚠️ | Everything except protected paths | Isolated containers/VMs only |

Defence in depth = mode + `permissions` rules in settings + hooks.

```json
{
  "permissions": {
    "allow": ["Bash(git commit*)", "Bash(npm install*)", "Write(.claude/*)"],
    "deny":  ["Bash(rm -rf*)", "Bash(sudo*)", "Bash(curl* | bash*)"]
  }
}
```

---

## 4. The `.claude` directory

```
project/.claude/            # committed, shared with the team
├── CLAUDE.md               # project brain
├── settings.json           # permissions, hooks, env, enabled plugins/MCP
├── settings.local.json     # personal overrides (not committed)
├── rules/                  # extra rule files (code-style.md, security.md, testing.md)
├── commands/               # custom slash commands (*.md)
├── skills/<name>/SKILL.md  # skills (scripts/, references/, assets/)
├── agents/*.md             # subagents
├── hooks/                  # hook scripts
└── .mcp.json / mcp config  # MCP servers

~/.claude/                  # user scope: same idea, applies to all projects
~/.claude/projects/...      # on-disk session history (what /resume reads)
```

Invisible to `ls`; visible with `ls -la` or hidden-files enabled in Finder/Explorer.

---

## 5. CLAUDE.md

**Priority (weakest → strongest):** enterprise/managed → user (`~/.claude/CLAUDE.md`) → project (`./CLAUDE.md` or `./.claude/CLAUDE.md`) → `CLAUDE.local.md`.

**Loading:** Claude walks up the directory tree from the cwd, loading CLAUDE.md/CLAUDE.local.md along the way. Supports imports (`@docs/architecture.md`). HTML comments are stripped before injection.

**Template:**

```markdown
# <Project name>
One-paragraph description, users, and goal.

## Tech stack
- Backend: <framework, port, storage, env vars>
- Frontend: <framework, port, data fetching, state rules>

## Essential commands
- install: <cmd>   - dev: <cmd>   - test: <cmd>   - lint/typecheck: <cmd>

## Code standards
- <naming, typing, formatting, error handling, component rules>

## Project structure
- <path> — <responsibility>   (only the files that matter)

## Hard rules
- Never commit directly to main. Never hardcode credentials.
- No silent failures — handle errors explicitly. Ask instead of assuming.

## Verification (run after changes)
- After code changes: run typecheck + tests.
- After UI changes: screenshot and compare to the requirement.
- After DB changes: verify with a test query.
```

**Belongs:** overview, commands, standards, structure, testing workflow, guardrails, verification steps, pointers.
**Does NOT belong:** full API docs, code snippets, stale instructions, task-specific instructions, secrets.

---

## 6. Context management

**Every turn resends:** system prompt + tool definitions + MCP tool descriptions + skill descriptions + CLAUDE.md/memory + full message history + reserved auto-compact buffer.

| Symptom | Fix |
|---|---|
| Instructions ignored, repeated work, dumb mistakes | `/context` → `/compact` (with instructions) or `/clear` |
| New topic in an old session | `/clear` |
| Must continue a long task | `/compact` telling it exactly what to keep |
| Returning to work later | New session + point it at a `CHANGELOG.md`/status file |
| Big files / long exploration | Delegate to a subagent |

**Budget levers you control:** CLAUDE.md size · number of MCP servers enabled · skills installed · model & effort · prompt specificity · session length · pasted images/files.
**Not controllable:** platform system prompt, core tools.

**Cost intuition ⚠️ (prices change):** billing is per-million input tokens *per call*, and history is resent each call. Course example: ~200K context × 5 messages ≈ $3 on Sonnet; a bloated single message ≈ $0.10.

---

## 7. Skills

```markdown
---
name: my-skill
description: What it does and WHEN to use it (this drives auto-invocation).
trigger: /my-skill
argument-hint: "path/to/file.csv"
effort: low            # optional
---

# Goal
# Inputs
# Steps (numbered, explicit)
# Rules / output format (specify literally if format matters)
# References: ./scripts/01_eda.py, ./references/toolkit.md
```
- Locations: `.claude/skills/<name>/SKILL.md` (project) · `~/.claude/skills/` (personal) · plugins.
- Only name+description sit in context until invoked → cheap at rest.
- Put deterministic work in **scripts** (reproducible, no generation cost) and pin `requirements.txt`.
- Let a **skill-creator** skill scaffold new ones, then refine arguments/model/effort.

---

## 8. Hooks

```json
{
  "hooks": {
    "PreToolUse":  [ { "matcher": "Bash",
        "hooks": [ { "type": "command", "command": "python .claude/hooks/security_guard.py", "timeout": 10 } ] } ],
    "PostToolUse": [ { "matcher": "Write|Edit",
        "hooks": [ { "type": "command", "command": "python .claude/hooks/auto_format.py", "timeout": 30 },
                   { "type": "command", "command": "python .claude/hooks/session_logger.py", "async": true } ] } ],
    "SessionStart": [ { "hooks": [ { "type": "command", "command": "python .claude/hooks/session_logger.py", "async": true } ] } ],
    "Stop":         [ { "hooks": [ { "type": "command", "command": "echo 'done' >&2", "async": true } ] } ]
  }
}
```

**Events:** SessionStart · UserPromptSubmit · prompt expansion · PreToolUse · permission request/denied · PostToolUse · Notification · subagent start/stop/failure · task created/completed · Stop · SessionEnd · pre-compact.

**Contract:** JSON on stdin (`tool_name`, `tool_input`, …) → **exit 0 = allow**, **exit 2 = block (stderr goes to Claude)**, other non-zero = non-blocking error. Or print `hookSpecificOutput` JSON with `permissionDecision: "allow"|"deny"|"ask"` + reason.

```bash
# Minimal blocking hook (jq-based)
COMMAND=$(jq -r '.tool_input.command')
echo "$COMMAND" | grep -q 'rm' && jq -n '{hookSpecificOutput:{hookEventName:"PreToolUse",
  permissionDecision:"deny", permissionDecisionReason:"Destructive command blocked"}}' || exit 0
```

**Golden rules:** let Claude write the first hook (avoids settings.json clobbering) · test hooks by hand · keep them fast · use `timeout`/`async` · prefer hooks for policy and hygiene, prompts for thinking.

---

## 9. MCP

```json
// .mcp.json (project root) or .claude/.mcp.json
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
- Secrets via `${ENV_VAR}` — never hardcode.
- Scopes: **project** (committed, team) → **user** (all your projects) → **local** (private, not committed).
- `/mcp` to list/authenticate; `enabledMcpjsonServers` to pre-approve; tool permissions look like `mcp__<server>__<tool>`.
- Local (stdio) vs hosted (HTTP/SSE): local for file/browser tools, hosted for SaaS. Local servers consume your RAM.
- Each server's tool list costs context every request → enable only what you need.
- Building your own server = expose functions with name/description/JSON-schema parameters. Registers like any other server.

---

## 10. Subagents

```markdown
---
name: code-reviewer
description: Reviews changes for bugs, security issues, and style violations. Use after implementing a feature.
tools: Read, Grep, Glob
disallowedTools: Bash, Edit
model: haiku
effort: high
color: blue
---

You are a senior reviewer. Report findings only; never modify files.
```
- Locations: `.claude/agents/*.md` · `~/.claude/agents/*.md` · plugins.
- Invoke by natural language (auto), `@name` (explicit), or `/agents` (library UI).
- Returns a summary only; work happens in its own context → main session stays lean.
- Use restricted tools + cheaper models for focused jobs. Run several in parallel.

---

## 11. Agent teams

```json
// .claude/settings.json
{ "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" } }
```
- Shape: team lead + teammates (e.g. backend / frontend / QA) in their own sessions, messaging each other.
- Teammates work in **git worktrees** (separate branches/checkouts); lead merges.
- `Shift+Down` switches views; in-process or split-pane display.
- ⚠️ Experimental — expect rough edges; high token burn; supervise and review merges.
- vs subagents: hierarchy/report-back vs peer coordination; stable vs experimental.

---

## 12. Plugins

```
.claude-plugin/<plugin-name>/
├── plugin.json      # {"name","version","description","author","keywords",
│                     #  "agents":"./agents/","skills":"./skills/","hooks":"./hooks.json"}
├── hooks.json       # commands using ${CLAUDE_PLUGIN_ROOT}
├── agents/  skills/  hooks/
├── settings.json.template
└── README.md
```
- `/plugins` → installed tab + marketplace tab; add a marketplace by GitHub URL; install/enable/disable/refresh.
- Community plugins are **not reviewed by Anthropic** → read the code, check reputation.
- Share with a team by committing the plugin directory + enabling it in project settings → teammates get it on `git pull`.

---

## 13. Scheduling & headless

| Option | Where it runs | Laptop on? | Session open? | Triggers |
|---|---|---|---|---|
| `/loop <interval> <task>` | Your machine, this session | Yes | Yes | Interval / cron (min 1 min ⚠️, expires ~3 days) |
| Desktop scheduled task | Your machine | Yes | App running | Time |
| **Claude routine** | Anthropic cloud | **No** | No | Schedule / API / GitHub events |
| `claude -p "…"` | Wherever you run it | — (host must run) | No | Your cron/systemd/CI |

- `/loop` inherits the session's MCP servers and permissions; good for watchers with a stop condition.
- Headless **still respects permissions** — it just has no UI and won't block on prompts. Test by hand before scheduling.
- Routine triggers include GitHub events with filters (PR opened/merged, release, issue; author/title/body/regex).

**Unattended-work safety checklist**
1. Read-only first. 2. Write to non-destructive paths. 3. Human gate for irreversible actions. 4. Log everything. 5. Test for days before trusting it.

```
BAD : "when tests pass, deploy to production"
GOOD: "when tests pass, write READY-TO-DEPLOY.md and ask a human in Slack to deploy"

BAD : "fix all lint errors in the codebase"
GOOD: "identify lint errors, write them to reports/lint-issues.md, do not modify source files"
```

---

## 14. Troubleshooting index

| Symptom | Likely cause / first move |
|---|---|
| `command not found` | New terminal / PATH |
| Wrong behaviour in one shell (Windows) | Installed for the wrong shell |
| Claude asks permission constantly | Switch to accept-edits/auto, or add `permissions.allow` rules |
| Same mistake twice | Add it to CLAUDE.md (Module 4) |
| Instructions ignored late in a session | Context rot → `/context`, `/compact` with instructions, or `/clear` |
| Costs spiking | Bloat: too many MCP servers, huge CLAUDE.md, long session, pasted images |
| Claude "dumber" than usual | Check context and model; restart fresh session |
| Hook not firing | Matcher string, settings location, hook file executable, test by hand |
| MCP tools missing | `/mcp`, server scope, API key env var, restart session |
| 401/auth errors in your app | It's your app's key, not your subscription — API keys are separate |
| Agent team features absent | Experimental flag not set; feature may have changed ⚠️ |

---

## 15. The 10 rules to keep on your desk

1. CLAUDE.md before code.
2. One task, one session; `/clear` freely.
3. `/compact` with explicit instructions when you must continue.
4. Delegate bulk reading to subagents.
5. Hooks for anything that must happen every time.
6. Match model to job (plan strong, build balanced, maintain cheap).
7. Only connect the MCP servers you actually use.
8. Read any plugin/hook you install.
9. Start automations read-only, gate the irreversible, log everything.
10. Verify with commands, not vibes — put the commands in CLAUDE.md.
