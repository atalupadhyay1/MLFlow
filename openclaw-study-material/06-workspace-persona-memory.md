# Chapter 6 — The Workspace: Personality, Identity, User Context & Memory
*Course section: Configure agent instructions, identity & user context · Time: ~75 min + Labs 5–6 (75 min)*

## Learning objectives
- Explain the job of each workspace file: **AGENTS.md, SOUL.md, IDENTITY.md, USER.md, MEMORY.md, HEARTBEAT.md**.
- Write workspace files that visibly change your agent's behaviour (Lab 5).
- Design memory that survives restarts: daily notes + curated long-term memory (Lab 6).
- Create/bootstrap a workspace cleanly (`openclaw setup --baseline` idea) and back it up.

---

## 6.1 The idea that makes OpenClaw feel different
Most chatbots have a hidden "system prompt" you can't see. OpenClaw puts the agent's *upbringing* in **plain Markdown files in a folder you own** — the **workspace** (default `~/.openclaw/workspace`). Open them, read them, edit them with any text editor. Your agent's personality is literally a document you can review in Notepad. That transparency is the feature.

Create/inspect a baseline workspace without the full wizard:
```bash
openclaw setup --baseline     # creates workspace + config folders without full onboarding
ls ~/.openclaw/workspace
```

## 6.2 The files, one by one (with excerpts you may steal)

### `AGENTS.md` — the employee handbook (rules of behaviour)
Operating instructions: how to work, what to check first, what never to do, how to use memory. Example spine (full template in `templates/workspace/AGENTS.md`):
```markdown
# AGENTS.md
## Every session
1. Read SOUL.md, USER.md, and today's + yesterday's memory notes.
2. If MEMORY.md exists and this is the main session, read it too.
## Safety
- Never exfiltrate private data. Never run destructive commands without asking.
- When in doubt, ask. `trash` > `rm`.
## Make it yours
- Write down what matters. Mental notes don't survive restarts — files do.
```

### `SOUL.md` — personality & values (how it *sounds*)
Not skills — character. "Be genuinely helpful, not performatively helpful. Have opinions. Be resourceful before asking. Remember you're a guest in someone's life." Two agents with identical tools but different `SOUL.md` feel like different colleagues. Keep it under a page; personality diluted over 5 pages becomes no personality.

### `IDENTITY.md` — name, creature, vibe, emoji
Filled during your "first real conversation": e.g. *Name: Clawdia · Creature: AI assistant in the machine · Vibe: sharp, warm, low-sycophancy · Emoji: 🦞.* Small file, outsized effect — named agents get treated (and configured) more thoughtfully.

### `USER.md` — context about *you*
Name, pronouns, timezone, how to address you, ongoing projects, preferences, pet peeves ("don't schedule before 10 AM", "summaries first, detail on request"). **Privacy law of the workspace:** this file is gold for the agent and sensitive for you — it lives on your machine; think before syncing it to random clouds (Ch 13).

### `MEMORY.md` + `memory/YYYY-MM-DD.md` — the diary system (see §6.3).

### `HEARTBEAT.md` — the agent's standing checklist for proactive checks (Ch 8)
A short list the agent works through on heartbeat polls: email? calendar? server health? Empty/comment-only file = heartbeats skip API calls = free. Power *and* peril — Ch 8 in full.

## 6.3 Memory, designed properly
**The two-tier system (learn this pattern, it recurs everywhere in agent design):**
- **Daily notes** `memory/2026-…-….md` — raw log: what happened, decisions, snippets. Append freely, low ceremony.
- **`MEMORY.md`** — curated long-term memory: only the distilled essentials (preferences, key decisions, lessons). Periodically "clean up" daily notes into it — like a human journaling, then writing a memoir.
- Load order each session (via AGENTS.md ritual): today's + yesterday's dailies always; `MEMORY.md` in main session. Security nuance worth copying: loading the full long-term memory only in *main* sessions reduces leaking your life into shared/group contexts.

**Why files beat "the model will remember":** model context wipes on reset; files don't. The agent that "remembered my dog's name after a restart" simply *read it in a file*. No magic — literacy.

## 6.4 🧪 Lab 5 — Give your agent a personality (45 min)
1. Back up: `cp -r ~/.openclaw/workspace ~/.openclaw/workspace.bak`
2. From `templates/workspace/`, copy our `SOUL.md`, `USER.md`, `IDENTITY.md`, `AGENTS.md` over yours (or merge by hand — merging teaches more).
3. Personalise brutally: your real name/timezone in `USER.md`; a name + emoji in `IDENTITY.md`; one strong opinion in `SOUL.md` (e.g. "answers start with the conclusion").
4. `openclaw gateway restart`, then DM your Telegram bot: `/new` (fresh session so files reload), then: *"Who are you, who am I, and how will you answer me?"*
**✅ Expected:** It answers with its name, *your* facts, and visibly in the style you dictated (conclusion-first, if you set that). Change one line in `SOUL.md`, restart, `/new`, ask again — watch the behaviour move. That tight loop *is* prompt engineering, minus the mystique.

## 6.5 🧪 Lab 6 — Memory that survives a restart (30 min)
1. Tell the agent a fact in chat: *"Remember: my manager's name is Priya, standup is 9:30, and I prefer briefings under 150 words."*
2. Ask: *"Write that to today's memory note."* (Well-behaved AGENTS.md makes it offer anyway.)
3. Open `~/.openclaw/workspace/memory/<today>.md` — see it in plain text. Also distil one line into `MEMORY.md`.
4. Restart the Gateway, `/new`, ask: *"What do you know about my standup and briefing preferences?"*
**✅ Expected:** Correct recall — sourced from files you can open. **If it fails:** check workspace path in config (Ch 4 trap!), confirm the file was actually written, confirm session ritual reads today's note.

## 6.6 Workspace hygiene & backup
- The workspace *is* your agent's brain-state: **back it up** (copy folder / private git repo *without* secrets & tokens). Recovery from "agent went weird" is often just "restore last week's workspace".
- Version it: `git init` inside the workspace (with a careful `.gitignore` for anything secret) gives you personality change-history. Delightful and practical.

## ⚠️ Common traps
| Trap | Antidote |
|---|---|
| Edited files, agent unchanged | Restart + `/new`; verify `agents.defaults.workspace` path |
| 4-page SOUL.md, generic behaviour | Cut to <1 page of *sharp* traits |
| USER.md full of secrets (passwords, keys) | Never. Secrets go in env/secret stores, not prompt files (Ch 13) |
| Agent "remembers" wrong facts | Read the memory files — correct the text, like editing notes. That you *can* is the point |

## 🎯 Self-check
1. AGENTS vs SOUL in one line each? → *Rules/handbook vs character/voice.*
2. Daily notes vs MEMORY.md? → *Raw log vs curated distillation.*
3. Why load MEMORY.md only in main sessions? → *Limit private-context exposure in shared/group sessions.*

**→ Next: [Chapter 7 — Tools, Skills & ClawHub](07-tools-skills-clawhub.md)**
