# Chapter 12 — Project 4: Ubuntu Sysadmin & VM-Readiness Agent
*Course project: Ubuntu system administration, VM readiness reports, repetitive task automation · Time: ~2 hrs + Lab 12 (90 min)*
*Needs: Ch 3 cloud VM (this project is why we deployed one). Safety briefing in §12.1 is mandatory reading.*

## What "done" looks like
07:30 daily, Telegram: **"🖥️ VM readiness — web-vm-01: ✅ Ready. Disk 61%, RAM 48%, services up (nginx, openclaw), updates pending: 3 (0 security), cert expires in 41 days."** And on the bad day, *before* users notice: **"⚠️ Disk 89% and climbing — /var/log is 6.2 GB. Suggested action: rotate logs. Reply APPROVE to run cleanup, or IGNORE."** That second message is the difference between monitoring and an *agent*.

## 12.1 ⚠️ Safety briefing — shell access is the crown jewels
An agent with `exec` on your server can fix things at 3 AM and break them at 3:00:01 AM. Rules that keep this project a delight instead of an incident:
1. **Read-only first.** The readiness agent only *reads* (`df`, `free`, `systemctl status`, `ss`, log tails). Weeks of trust before any write action.
2. **Approval for actions.** Any mutating command (cleanup, restart, update) requires your explicit chat approval — design the skill that way, verify by test.
3. **Dedicated, least-privilege context** where your setup allows: agent workspace separate from your main assistant (Ch 14's second agent earns its keep here), sudo never passwordless-for-everything.
4. **No internet-open Gateway** (Ch 3's rule returns), token auth, allowlisted channel senders only — a sysadmin agent reachable by strangers is a breached server with extra steps.
5. **Log everything.** Commands run + outputs go to the daily memory note. If it isn't logged, it didn't happen; if it *did* happen unlogged, stop and investigate.

## 12.2 The readiness checklist (what "ready" means, concretely)
Adapt `templates/skills/sysadmin-check/SKILL.md`. A VM is READY when:
- Disk: every mount < 80% (warn 80–90, alert > 90); top-3 space consumers named.
- Memory/CPU: RAM < 85%, load average sane vs core count, no swap thrash.
- Services: watched list (e.g. nginx, docker, openclaw gateway) all `active`; failed units = 0 or explained.
- Network: expected ports listening (`ss -tlnp` vs your list); unexpected listener = alert.
- Security posture: pending updates counted, **security updates flagged separately**; SSH failed-login count (24h) reported; TLS cert days-remaining for your domains (> 14d ok).
- Backups: last backup timestamp found where your backup tool writes it (absence = alert).
- Uptime/restarts: uptime + "rebooted since yesterday?" (unexpected reboot = investigate).

Report = one line per check with ✅/⚠️/🔴 + the numbers. Verdict first line: READY / READY-WITH-WARNINGS / NOT-READY. (Full sample in the skill template.)

## 12.3 🧪 Lab 12 — From checks to trusted colleague (90 min)
1. **Baseline by hand (15 min):** SSH in and run the checks yourself: `df -h`, `free -h`, `uptime`, `systemctl --failed`, `ss -tlnp`, `apt list --upgradable 2>/dev/null | head`, `journalctl -u ssh --since "24h ago" | grep -ci failed` (adjust units to your VM). Note *your* verdict. The agent must learn to see what you just saw.
2. **Install the sysadmin-check skill** on the VM's agent (or your agent with exec scoped to the VM — be explicit about which machine commands run on; ambiguity here causes the classic "checked the wrong host" comedy).
3. **On-demand run via Telegram:** compare line-by-line with your baseline. Fix discrepancies in the skill (thresholds, service list, log paths). Two iterations is normal.
4. **Schedule it:** cron 07:30 daily → Telegram; plus a heartbeat variant only if you want intra-day alerts (disk check with silence condition — Ch 8 discipline).
5. **Approval-flow test:** ask it to "clean old logs" *without* the word approve — it must propose & wait. Then approve and watch it execute + log to memory note. If it acted without approval, stop: rewrite guardrails and retest before any scheduling.
6. **Break something safely:** create a big filler file (`fallocate -l 500M /tmp/filler`) to push a test mount over your warn threshold; next run must flag it. Remove the file. Chaos-testing your own monitor is how pros sleep.
**✅ Complete when:** agent verdict matches yours twice, alerts fire on the planted fault, and no mutating action ever ran unapproved.

## 12.4 Repetitive-task automation (the course's broader theme)
Once read + approved-action patterns are trusted, the same shape automates: log rotation reports, stale-file cleanup proposals, user/account audits, docker prune *proposals*, SSL renewal reminders, nightly config backups (to your private store). Pattern forever: **detect → report → propose → approve → act → log**. Automate the detecting and reporting fully; keep humans on the approving until a specific action has earned trust through repetition.

## ⚠️ Failure gallery
| Failure | Fix |
|---|---|
| Checked laptop instead of VM | Skill names the host; run a `hostname` line atop every report |
| Alert fatigue (daily ⚠️ for trivia) | Tune thresholds; warnings need "so-what" lines |
| Agent ran sudo rm "to help" | Approval guardrail + least privilege + restore from backup + incident journal entry (do all four) |
| Report says all ✅ during outage | It checked cached/yesterday's data — require live command outputs with timestamps |

## 🎯 Self-check
1. The six-word automation ethic? → *Detect, report, propose, approve, act, log.*
2. First capability level for any sysadmin agent? → *Read-only, until trust is earned.*
3. How do you know the monitor works? → *Plant a fault; watch it catch the fault.*

**→ Next: [Chapter 13 — Security, Cost & Production Hardening](13-security-cost-production.md)**
