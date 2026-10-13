# OpenClaw Cheat Sheet — Commands & Concepts (one page, keep open)

## Install & onboard
```bash
curl -fsSL https://openclaw.ai/install.sh | bash        # macOS/Linux
iwr -useb https://openclaw.ai/install.ps1 | iex         # Windows PowerShell
npm install -g openclaw@latest                          # alternative
openclaw onboard --install-daemon                       # guided setup + service
openclaw setup --baseline                               # workspace/config folders only
openclaw configure                                      # revisit settings later
```

## Gateway daily verbs (port 18789)
```bash
openclaw gateway status | install | restart | stop
openclaw gateway --port 18789     # foreground + live logs (debug mode)
openclaw dashboard                # Control UI
openclaw doctor                   # health checks (read yourself)
openclaw triage                   # sanitised diagnosis, agent handoff (opt-in)
openclaw --version
```
Cloud dashboard, the safe way: `ssh -L 18789:127.0.0.1:18789 user@VM_IP` → browse `127.0.0.1:18789`. Never expose 18789 publicly.

## Files that are the agent (workspace, default `~/.openclaw/workspace`)
`AGENTS.md` rules handbook · `SOUL.md` personality · `IDENTITY.md` name/vibe · `USER.md` about you · `MEMORY.md` curated long-term · `memory/YYYY-MM-DD.md` daily diary · `HEARTBEAT.md` heartbeat checklist · `skills/<name>/SKILL.md` taught procedures. Config: `~/.openclaw/openclaw.json`. After edits: `openclaw gateway restart` + `/new` in chat.

## Channels
```bash
openclaw channels login           # e.g. WhatsApp QR linking
```
Telegram: BotFather `/newbot` → token → `channels.telegram { enabled, botToken, dmPolicy: "pairing" }` → approve pairing. WhatsApp: `allowFrom: ["+<your number>"]` always; groups `requireMention: true`. Chat resets: `/new`, `/reset`.

## Concepts in one breath
Model=brain · Agent=worker · Tool=one action (verb) · Skill=recipe (SKILL.md: description triggers, body instructs, guardrails restrain) · Channel=doorway (WhatsApp/Telegram/…) · Gateway=always-on hub executing tool calls under your rules · Session=one conversation's context (scope per-sender; daily/idle resets; compaction summarises) · Cron=exact-time job (self-sufficient payload!) · Heartbeat=periodic judgement with silence conditions (`HEARTBEAT_OK`; empty HEARTBEAT.md = off/cheap) · Sub-agent=temporary parallel worker, hands off via files.

## Decide fast
Cron vs Heartbeat → timing vs monitoring. Fix order → Channels status → logs → config → doctor. Skill won't fire → description → folder/discovery → tools enabled → model strength → conflicts. Irrelevant results → fix USER.md criteria / skill, not chat arguments. Expensive agent → caps, per-job cheap models, longer intervals, output caps, kill zombie jobs weekly.

## Safety non-negotiables
Loopback+token gateway · pairing/allowFrom everywhere · vet skills (read SKILL.md + scripts) · read-only before write, approval before mutation · secrets in env, never workspace/git · backups tested · provider + cloud billing caps set. Incident: stop → preserve logs → rotate tokens → restore → journal.
