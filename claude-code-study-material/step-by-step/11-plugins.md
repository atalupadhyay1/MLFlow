# Part 11 — Plugins & marketplaces
**Video:** 10:35:46 – 11:07:28 (Module 11)

**In this part:** 11.1 What & anatomy · 11.2 Installing safely and creating your own

---

## 11.1 Plugins: what they are and what's inside

### What it is
- A **plugin** is a **versioned bundle** that can contain:
  - **agents** (subagents), **skills**, **commands**, **hooks**,
  - **MCP server** definitions,
  - **settings** (templates), and a **CLAUDE.md**,
  - plus a manifest and README.
- Manifest layout:
  ```
  .claude-plugin/<plugin-name>/
  ├── plugin.json          # {"name","version","description","author","keywords",
  │                        #  "agents":"./agents/","skills":"./skills/","hooks":"./hooks.json"}
  ├── hooks.json           # event → matcher → command (using ${CLAUDE_PLUGIN_ROOT})
  ├── hooks/               # e.g. auto_format.py, session_logger.py
  ├── agents/              # planner.md, code-writer.md, test-writer.md, …
  ├── skills/build-app/SKILL.md
  ├── settings.json.template
  └── README.md
  ```
- Installed and managed via `/plugins`: an **Installed** tab and a **Marketplace** tab (Anthropic runs an official marketplace; community ones can be added by URL).

### Why it matters
- A plugin is the difference between *"my clever config"* and *"my team's standard"*: one install gives a teammate your agents, hooks, skills and MCP setup instead of a zip of instructions.
- It's the distribution format for everything you built in Parts 6–9. Without it, your work stays on your laptop.
- It's also how you **consume** other people's work — which is precisely where the security conversation starts.

### How to do it (step by step)
1. Inventory what you already have: list your agents, skills, commands and hooks with one line each.
2. Read a real manifest (the course's `quicktask` plugin is a good model) and map each key to a folder you already own.
3. Notice the one non-obvious convention: **hook commands reference `${CLAUDE_PLUGIN_ROOT}`** so paths resolve wherever the plugin is installed:
   ```json
   { "hooks": { "PostToolUse": [ { "matcher": "Write|Edit",
       "hooks": [ { "type": "command",
                    "command": "python \"${CLAUDE_PLUGIN_ROOT}/hooks/auto_format.py\"",
                    "timeout": 30 } ] } ] } }
   ```
4. Decide your first bundle's purpose in one sentence (e.g. "our Python project conventions: formatter hook + reviewer agents + build skill").
5. Write the README *first* — what's inside, how to enable, what standards it enforces. It doubles as your checklist.

**What can go in a bundle (checklist)**
- [ ] Agents (`.md` with frontmatter)
- [ ] Skills (`<name>/SKILL.md` + scripts/assets)
- [ ] Commands (`.md` prompt files)
- [ ] Hooks (`hooks.json` + scripts)
- [ ] MCP servers (definitions, *no secrets*)
- [ ] Settings template + CLAUDE.md

**Lab 11.1 — Inventory and plan**
- [ ] Listed your existing agents/skills/commands/hooks.
- [ ] Wrote a one-sentence purpose for the bundle you'll create.
- [ ] Drafted the README structure (what's inside, how to enable, standards).
- [ ] Flagged anything that must **not** travel (personal paths, API keys).

**Proof:** the inventory + purpose sentence + the "must not travel" list.

**Quiz 11.1**
1. Name five things a plugin can bundle.
2. Why do plugin hook commands use `${CLAUDE_PLUGIN_ROOT}`?
3. What must never travel inside a shared plugin, and where should it live instead?

---

## 11.2 Installing safely, and creating/sharing your own

### What it is
- **Installing:** add a marketplace (e.g. a GitHub repo URL) in `/plugins` → browse → install → enable. Enablement is recorded in settings, so it can be shared with a team.
- **Creating:** two routes the course demonstrates —
  1. **Ask Claude:** *"create a plugin from my `.claude` folder in this project"* — it scaffolds the manifest and copies content in.
  2. **Hand-roll:** create `.claude-plugin/<name>/`, write `plugin.json`, move content in, test, commit.
- **Sharing:** commit the plugin directory and enable it in **project settings** — teammates get it when they pull the repo.

### Why it matters
- **Community plugins are not reviewed by Anthropic.** They contain hooks and commands that execute with your permissions. The course is explicit: check stars/forks, read the hooks, treat installation as running someone else's code.
- The create-and-commit flow is how a team standardises without meetings: one person's working setup becomes everyone's default.
- It closes the loop of the whole course: CLAUDE.md (memory) + skills (procedures) + hooks (reflexes) + agents (workers) + MCP (tools) — **packaged, versioned, shareable**.

### How to do it (step by step)
1. **Install practice (safely):**
   1. `/plugins` → Marketplaces → add a marketplace by URL.
   2. Browse it and pick a plugin whose README you actually read.
   3. Before enabling: open its `hooks/` and commands and read them. Ask: *what does this run, when, on what?*
   4. Install, enable, **test on a throwaway repo**, then decide whether it stays.
   5. Remove the marketplace afterwards if you were only exploring.
2. **Create your own:**
   1. In a project with agents/skills/hooks you like, ask Claude to create a plugin from `.claude`.
   2. Review `.claude-plugin/<name>/plugin.json`: name, version, description, and correct paths for `agents`, `skills`, `hooks`.
   3. Verify hook commands use `${CLAUDE_PLUGIN_ROOT}`; replace any absolute personal paths.
   4. Enable it (locally first), restart, and confirm agents/skills/hooks are live.
   5. **Prove portability:** commit the plugin, clone the repo into a fresh folder, and confirm the capabilities appear there.
   6. Version it sensibly (`1.0.0`) and note in the README how teammates enable it.
3. **Write your security rule for third-party bundles** in one line, e.g.: *"I read hooks and commands before enabling, and I test new plugins in a scratch repo."*

### Pre-install audit for any community plugin
| Check | Why |
|---|---|
| Reputation: stars, forks, last commit | Abandoned or unknown code is a liability |
| Read every **hook** | Hooks run automatically, with your permissions |
| Read **commands/skills** | They shape what the agent will do |
| Look for secrets or network calls | Data exfiltration is the worst case |
| Test in a scratch repo | Bounded investigation |

**Lab 11.2 — Bundle it and prove it travels**
- [ ] Installed (and read) one community plugin, or documented why you skipped it.
- [ ] Created your own plugin with a valid `plugin.json`.
- [ ] Replaced absolute paths with `${CLAUDE_PLUGIN_ROOT}`; verified no secrets are included.
- [ ] Enabled it and confirmed agents/skills/hooks work.
- [ ] Cloned the repo fresh and confirmed the capabilities came with it.
- [ ] Wrote your one-line third-party plugin rule.

**Proof:** the plugin directory (manifest + README), the fresh-clone confirmation, and your security rule.

**Quiz 11.2**
1. What due diligence does the course insist on before installing a community plugin?
2. How do teammates get your plugin automatically?
3. Your plugin works for you but fails for a teammate with a path error. What's the most likely cause?

---

## Part 11 wrap-up

| Topic | Done | Lab proof | Quiz |
|---|---|---|---|
| 11.1 What & anatomy | ☐ | Inventory + README draft | ☐ /3 |
| 11.2 Install & create | ☐ | Plugin + fresh-clone proof | ☐ /3 |

**Answers:** `13-answer-key.md` → Part 11.
**Next:** `12-scheduling.md` — make Claude work while you don't.
