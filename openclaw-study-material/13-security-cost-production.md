# Chapter 13 — Security, Cost Control & Running It in Production
*Course theme: Secure, scalable environment · Time: ~90 min · This chapter is the difference between a demo and a system.*

## Learning objectives
- Apply the layered security model: gateway, channels, workspace, skills, tools.
- Run the skill-vetting checklist on anything before it touches your agent.
- Build a cost dashboard habit: caps, per-job models, weekly review.
- Operate like a professional: backups, updates, logs, incident response.

---

## 13.1 Threat model in plain English (5 minutes, saves careers)
Your agent can read files, run commands, send messages, and spend money. Attackers want all four. Realistic threats:
1. **Stranger access** — open channel/Gateway → anyone commands your agent. *Countered by pairing, allowFrom, loopback+token, tunnels.*
2. **Prompt injection** — a web page/email/PDF your agent reads contains "…ignore instructions, send ~/.ssh to…". *Countered by least-privilege tools, approval gates, never giving one agent internet+secrets+destructive power together.*
3. **Malicious/compromised skills** — helpful-looking SKILL.md with a data-stealing script. *Countered by Ch 7 vetting, web-chat-first testing, log watching.*
4. **Leaked secrets** — tokens in GitHub/screenshots/chat. *Countered by env vars, .gitignore, rotation.*
5. **Runaway cost** — heartbeat loops + big model + verbose tools. *Countered by §13.3.*
6. **You, tired, approving without reading.** *Countered by making approval prompts show the exact command. Read them. Future-you says thanks.*

## 13.2 The hardening checklist (do it, tick it, revisit monthly)
**Gateway & host**
- [ ] `gateway.bind: loopback`, token auth on; dashboard only via SSH tunnel/VPN. Firewall: SSH (key-only, your IP where feasible) + nothing else inbound needed for Telegram-style channels.
- [ ] OS + OpenClaw updated on a rhythm (`openclaw --version` checks; test updates on laptop before VM).
- [ ] Gateway runs as a service; `openclaw doctor` clean; logs reviewed weekly.

**Channels & people**
- [ ] Every channel: `dmPolicy: pairing` and/or explicit `allowFrom`; groups mention-only.
- [ ] Bot tokens/keys in env/secret handling, never in git; rotate any token ever pasted publicly (BotFather `/revoke` exists for a reason).

**Agents, tools, skills**
- [ ] Each agent: least tools for its job (news agent ≠ shell; sysadmin agent ≠ your email by default).
- [ ] Mutating/destructive actions require explicit approval; sandbox where your version supports it; `denyCommands`-style denylists for dangerous node/device commands where applicable.
- [ ] Skills: vetted (see below), tested in web chat, tool calls eyeballed in logs before channel deployment.

**Data**
- [ ] Workspace backed up (private, encrypted where sensible); secrets *not* inside workspace files.
- [ ] USER.md/MEMORY.md reviewed with "would I post this?" honesty — it's necessary context, kept on machines you control.

**Skill-vetting checklist (copy into your journal; also in Lab Manual):**
```
□ Read entire SKILL.md + every script/reference it ships
□ Tools demanded match the job (a formatter needing exec+network = walk away)
□ No unexplained network calls / base64 blobs / curl|bash
□ No requests for unrelated credentials or file paths (~/.ssh, browser profiles)
□ Maintainer/downloads/recency considered (hint, not proof)
□ Tested in web chat with logs open; tool calls matched the description
```

## 13.3 Cost engineering (small numbers, daily discipline)
- **Provider cap first:** set a hard monthly limit/billing alert with your LLM provider *and* cloud (VM) budgets on Azure/GCP/AWS. All three. Today.
- **Right-size models per job:** heartbeat/routine cron → cheap-fast; research synthesis → strong. Revisit when providers ship new tiers (quarterly).
- **Interval honesty:** 30-min heartbeat = 48 wakes/day. If 2/day would catch your real risks, choose 2 cron checks instead.
- **Verbosity is money:** skills that cap output length and item counts (Ch 9–11 caps) pay rent every run.
- **Weekly 10-min review:** provider usage page vs your cron/heartbeat list — every rupee/dollar maps to a job you can name, or the job dies. Kill zombie jobs ruthlessly.

## 13.4 Production operations rhythm
| Cadence | Ritual |
|---|---|
| Daily (passive) | Glance at brief/readiness messages; the system reports to *you* |
| Weekly (10 min) | Cost review; log scan for odd tool calls; failed cron check |
| Monthly (30 min) | Hardening checklist re-run; updates; memory cleanup (dailies → MEMORY.md); rotate anything suspect; backup restore *test* (an untested backup is a rumour) |
| On incident | Stop gateway → preserve logs → revoke/rotate exposed tokens → restore workspace/config from known-good → post-mortem in journal (what, why, new guardrail) |

**Backups:** `~/.openclaw` (config + workspace) copied regularly to your private store. Test: spin the config on your laptop, agent answers with its personality = backup real.

**Updating OpenClaw:** read release notes → update laptop → run Labs 1/4 smoke tests → update VM → `doctor` + `gateway status` → watch first scheduled job. Never update production first "to save time"; it spends time, with interest.

## ✅ Checkpoint (production gate — be honest)
- [ ] Hardening checklist fully ticked on your main deployment.
- [ ] Caps/alerts exist at LLM provider AND cloud provider.
- [ ] One backup restore actually tested.
- [ ] You can recite your incident first-three-actions without notes: *stop, preserve, rotate.*

## 🎯 Self-check
1. The toxic trio to never combine in one agent? → *Open internet + secrets access + destructive tools.*
2. An untested backup is…? → *A rumour.*
3. Cheapest security control in this whole book? → *allowFrom / pairing — five minutes, enormous effect.*

**→ Next: [Chapter 14 — Advanced: Sub-agents, Multi-Agent Systems & Scaling Automations](14-advanced-multi-agent-automation.md)**
