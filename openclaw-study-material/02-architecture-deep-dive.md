# Chapter 2 — Architecture Deep-Dive: How a Message Becomes an Action
*Course section: Agents, Models, Tools, Skills, Channels, Gateway & Sessions · Time: ~75 min + Lab 3 preview*

## Learning objectives
- Trace one WhatsApp/Telegram message through every OpenClaw component until a reply comes back.
- Choose a model/provider sensibly (quality vs cost vs local).
- Explain sessions, context windows, and why agents "forget" mid-task — plus the three cures.
- Read an `openclaw.json` config and know which section does what.

---

## 2.1 The journey of one message (the most important diagram in the course)

You type on Telegram: *"Any disk issues on my server?"*

```
YOU (Telegram app)
   │  1. message leaves Telegram's servers
   ▼
CHANNEL PLUGIN (telegram)  ── checks: is this sender allowed? (allowFrom / pairing)
   │  2. normalised into an internal message
   ▼
GATEWAY (daemon, port 18789) ── routes to the right AGENT + SESSION
   │  3. assembles CONTEXT: system prompt + workspace files (AGENTS/SOUL/USER)
   │     + session history + available tools/skills
   ▼
MODEL (Claude/GPT/…) ── THINKS, then either replies or requests a TOOL CALL
   │  4a. plain reply ───────────────────────────────► back to you
   │  4b. tool call: exec("df -h") / web_search(…) / read(file)
   ▼
TOOL EXECUTION (sandboxed where configured) ── result returns to the model (OBSERVE)
   │  5. model may loop (another tool) or compose the final answer
   ▼
GATEWAY → CHANNEL → YOU:  "Disk at 61% — healthy. /var/log is growing though…"
```

**Key insight:** the model never touches your server directly. It *requests* tool calls; the Gateway executes them under rules you set. That separation is what makes agents securable at all (Ch 13 leans on it hard).

## 2.2 The Gateway — the always-on hub

- A **daemon** (background service) you install once: `openclaw gateway install` (launchd on macOS, systemd user unit on Linux/WSL2, Scheduled Task on Windows).
- Listens on **port 18789** by default; serves the **Control UI** (web dashboard), channel webhooks/polling, and the agent runtime.
- Foreground mode for debugging: `openclaw gateway --port 18789`. Background checks: `openclaw gateway status` / `restart` / `stop`.
- **Auth:** token-based. Never expose an unauthenticated Gateway to the internet — treat it like an admin panel, because it is one.
- **Config file:** `~/.openclaw/openclaw.json`. State directory overridable via `OPENCLAW_STATE_DIR` / `OPENCLAW_CONFIG_PATH` (useful on servers).

## 2.3 Models — choosing a brain without overpaying

| Provider style | Examples | Strengths | Watch out for |
|---|---|---|---|
| Premium hosted | Anthropic Claude, OpenAI GPT | Best reasoning & tool-use reliability | Cost per token; needs API key & billing |
| Value hosted | Gemini, DeepSeek, Kimi (Moonshot) | Cheap, fast, often "good enough" | Tool-calling quirks vary; test your skill |
| Router | OpenRouter | One key, many models, easy fallbacks | Extra hop; prices vary per model |
| Local | Ollama models on your machine | Free per call, private, offline | Needs decent RAM/GPU; weaker tool use |

**Rules of thumb used throughout this book:**
1. Learn on a mid-tier hosted model; only optimise cost once workflows work.
2. Use a **cheap/fast model for heartbeat & routine cron**, a stronger one for research/reports (model-per-job is a first-class idea — Ch 8).
3. Set `agents.defaults.model.primary` in config; keep a fallback if your provider supports it. Verify what's actually configured rather than assuming: `openclaw gateway status` and the dashboard show the live model.
4. Existing **Claude Code / Codex CLI logins** can be detected at onboarding — handy if you already pay for one.

## 2.4 Context — what the model "sees" on every turn

Each reply is generated from a freshly assembled context window:

1. **System instructions** — built from workspace files (`AGENTS.md` rules, `SOUL.md` personality, `IDENTITY.md`, `USER.md` context) — Ch 6.
2. **Session history** — the conversation so far (until reset/compaction).
3. **Tool & skill catalogue** — names + descriptions of what it may call.
4. **Your new message** (+ attachments).

**Context window = the model's desk.** Everything must fit on the desk. Long chats push old papers off — that's "forgetting". Three cures, in order of preference:
- **Compaction/summarisation** (e.g. `compaction: { mode: "safeguard" }` in defaults) — old chat compressed into notes.
- **Memory files** — important facts written to `MEMORY.md`/daily notes, re-read next session (Ch 6).
- **Session resets** — `/new`, daily reset (e.g. 4 AM), or idle reset so stale context doesn't poison a fresh task (Ch 8).

## 2.5 Tools & plugins — the hands

Built-in families you'll meet: **exec/shell** (run commands), **file read/write/edit**, **web search & fetch**, **browser control**, **messaging**, **cron management**, plus plugin tools (e.g. WhatsApp login is itself an on-demand plugin). Principles:

- Grant **least privilege**: an agent that only briefs news needs search+fetch, not shell.
- Tool *descriptions* are prompts too — the model picks tools by reading them. Vague description → wrong tool. (You'll feel this when writing skills in Ch 7.)
- Dangerous tools (`exec`, file delete, browser purchases) deserve **approval gates** and sandboxing — configuration, not hope.

## 2.6 Reading a real config (demystified)

```json5
{
  env: { ANTHROPIC_API_KEY: "sk-ant-…" },        // secrets (prefer env vars on servers — Ch 13)
  agents: { defaults: {
      model: { primary: "anthropic/claude-sonnet-4-6" },
      workspace: "~/.openclaw/workspace",
      compaction: { mode: "safeguard" },
      heartbeat: { every: "30m" },               // "0m" = off; see Ch 8 before enabling!
      maxConcurrent: 4,
      subagents: { maxConcurrent: 8 }            // Ch 14
  }},
  channels: {
    telegram: { enabled: true, botToken: "123456:ABC-…", dmPolicy: "pairing" },
    whatsapp: { enabled: true, dmPolicy: "pairing", allowFrom: ["+919999999999"] }
  },
  gateway: { mode: "local", bind: "loopback", auth: { mode: "token" } },
  skills: { install: { nodeManager: "npm" } }
}
```
Read it as sentences: *"Default agent uses this model and workspace. Telegram and WhatsApp are on, strangers must pair first. Gateway stays on loopback with token auth."* If you can translate config → English, you can debug 80% of issues.

## 2.7 Sessions in one paragraph
A **session** is one continuous conversation with its own history. Scope can be per-sender (each person gets their own — recommended for assistants) and resets happen via `/new`, daily hour, or idle timeout. Sessions are why two people can talk to the same agent without it mixing up their requests — and why *you* saying "start fresh" actually works.

## ✅ Checkpoint — Lab 3 preview (do fully after Ch 4)
Once your Gateway runs (Ch 3–4), send one message and run `openclaw gateway status` + watch the dashboard/logs while it replies. Identify in the log: channel intake → model call → (tool call?) → reply. If you can narrate it using §2.1, this chapter is yours.

## ⚠️ "It broke, now what?"
| Symptom | Likely layer | First move |
|---|---|---|
| No reply at all | Gateway down / channel not connected | `openclaw gateway status`, then `openclaw doctor` |
| Reply, but dumb/generic | Wrong model or workspace files not loaded | Check dashboard model; verify workspace path in config |
| "It forgot everything" | Session reset / context overflow | `/new` intentionally; add MEMORY.md facts; enable compaction |
| Tool never gets used | Tool not enabled, or skill description unclear | List tools in dashboard; sharpen the skill (Ch 7) |

## 🎯 Self-check
1. Who executes a tool call — model or Gateway? → *Gateway (the model only requests it).*
2. Name the 4 things assembled into context each turn. → *System/workspace instructions, session history, tool/skill catalogue, new message.*
3. Cheapest cure for "agent forgets between days"? → *Write facts to memory files (and load them), not longer chat history.*

**→ Next: [Chapter 3 — Installation: Local, Azure, GCP & AWS](03-installation-local-and-cloud.md)**
