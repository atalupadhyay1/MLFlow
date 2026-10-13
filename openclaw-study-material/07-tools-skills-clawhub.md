# Chapter 7 — Tools, Skills & ClawHub: Teaching the Agent New Tricks
*Course section: Skills & plugins · Time: ~90 min + Lab 7 (60 min)*

## Learning objectives
- Distinguish tools, plugins, and skills crisply (and explain it to someone else).
- Install & vet a skill from **ClawHub** without installing a security incident.
- Write your own skill: a `SKILL.md` with YAML frontmatter + instructions an agent can actually follow (Lab 7).
- Debug "the agent won't use my skill" systematically.

---

## 7.1 Three words, finally untangled
- **Tool** — one callable action (`web_search`, `read`, `exec`, browser…). Verbs.
- **Plugin** — a packaged extension that *adds* tools/channels (WhatsApp support is a plugin that installs on demand).
- **Skill** — a *folder* teaching the agent a procedure: `SKILL.md` (frontmatter + Markdown instructions) plus optional scripts/references. Skills combine tools into judgement: not just "you have a knife" but "here's how we make the salad".

Skills live in the workspace (e.g. `~/.openclaw/workspace/skills/<name>/`) — *your* skills override/shared-next-to bundled and ClawHub-installed ones, and they're discovered by description matching: the agent reads skill descriptions and loads the relevant one for a task. Write descriptions like you're writing the world's most important one-line job ad.

## 7.2 Anatomy of a SKILL.md (annotated)

```markdown
---
name: daily-brief
description: Use when the user asks for a morning briefing or daily digest of news and updates on their chosen topics. Searches the web, deduplicates, and returns a short structured brief.
---

# Daily Brief

## When to use
User asks for a briefing/digest, or a scheduled brief fires.

## Steps
1. Read topics from USER.md (or ask, if empty).
2. web_search each topic, limit to the last 24h.
3. web_fetch the top 2–3 results per topic; ignore duplicates of yesterday's brief (check memory notes).
4. Summarise each item in ONE line + link. Max 7 items total.
5. Format: headline line, bullets, "watching:" last line. Under 200 words unless asked.

## Guardrails
- Never invent headlines; if search fails, say so.
- No paywalled full text; link instead.
```
Frontmatter `name` + `description` is the *trigger*; the body is the *method*. Most bad skills fail in the description (agent never selects it) or in missing guardrails (agent freelances). Copy-ready skills live in `templates/skills/`.

## 7.3 ClawHub — the skill marketplace, with adult supervision
**ClawHub** is the community registry for skills: discover, inspect, install into your workspace. The workflow that keeps you safe:

1. **Discover** — browse/search ClawHub (via its site/CLI as your version provides) for the capability (e.g. "google workspace", "pdf summarise").
2. **Inspect before installing** — read the full `SKILL.md`, every script, and what tools it demands. Ask: *would I run these shell commands myself, sight unseen?* If a "weather skill" wants your email password, it's not a weather skill.
3. **Install** into your workspace skills folder (per ClawHub/your version's install flow; `skills.install.nodeManager: "npm"` governs script deps where relevant).
4. **Enable narrowly, test in web chat first** (not on your production Telegram agent with shell access), watch tool calls in logs (Lab 3 skill!).
5. **Review community signals** — downloads, maintainer, update recency — as *hints*, never as proof.

> 🚨 **Security framing (non-negotiable):** A skill is *code + instructions that an AI will follow*. The 2025–26 wave of malicious agent skills across ecosystems is exactly why this book makes you read before installing. Ch 13 formalises a vetting checklist; Lab 7 makes you practise it.

## 7.4 🧪 Lab 7 — Install one, then write your own (60 min)
**Part A — Vet & install (25 min):**
1. Pick a harmless capability (e.g. weather or pdf-summary) on ClawHub.
2. Fill the vetting checklist in `labs/LAB-MANUAL.md` (tools demanded? scripts? network calls? secrets asked?).
3. Install, then test in **web chat**: trigger it with a matching prompt; confirm in logs it loaded and which tools it called.

**Part B — Write your own (35 min):** Build `note-to-self` exactly (then make it yours):
```bash
mkdir -p ~/.openclaw/workspace/skills/note-to-self
cat > ~/.openclaw/workspace/skills/note-to-self/SKILL.md <<'EOF'
---
name: note-to-self
description: Use when the user says "note this", "remember this", or asks to save a quick note. Appends a timestamped entry to today's memory note.
---
# Note to Self
1. Take the user's exact point; do not embellish.
2. Append `- [HH:MM] <note>` to memory/<today>.md (create the file if needed).
3. Reply with only: "Noted ✅" plus a 3-word echo of the topic.
EOF
openclaw gateway restart
```
Then DM: *"Note this: renew the domain in March."* → check today's memory file. **✅ Expected:** entry present; reply terse. **Then iterate once:** change reply style in the skill, restart, retest. Congratulations — prompt/tool engineering is now a thing you've *done*, not watched.

## 7.5 Why won't it trigger? (the debugging ladder)
1. **Description mismatch** — your prompt's words vs description's words. Broaden the description with synonyms ("briefing/digest/morning update").
2. **Not discovered** — wrong folder/name (folder name ↔ `name` frontmatter), Gateway not restarted.
3. **Tool missing** — skill instructs a tool the agent doesn't have/enabled. Logs show refusal; enable the tool or rewrite the step.
4. **Model too weak** — small/local models miss subtle triggers; test on your stronger model to isolate.
5. **Conflicting skills** — two similar descriptions; make each description claim its distinct territory.

## ✅ Checkpoint
- [ ] One ClawHub skill vetted with the written checklist and tested in web chat.
- [ ] `note-to-self` works and one iteration visibly changed behaviour.
- [ ] You can debug a non-triggering skill in the 5-step order above.

## 🎯 Self-check
1. Tool vs skill, knife analogy? → *Knife = tool; recipe = skill.*
2. The two places bad skills usually fail? → *Triggering description; missing guardrails.*
3. First test environment for any new skill? → *Web chat, narrow tools, logs open — not production channels.*

**→ Next: [Chapter 8 — Sessions, Cron Jobs & the Heartbeat](08-sessions-cron-heartbeat.md)**
