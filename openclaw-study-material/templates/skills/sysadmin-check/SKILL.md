---
name: sysadmin-check
description: Use when asked for server health, VM readiness, system status, or on the scheduled readiness job/heartbeat. Runs READ-ONLY Ubuntu checks, reports a readiness verdict with evidence, and only proposes — never performs — fixes without approval.
---

# Ubuntu Sysadmin & VM Readiness Check (READ-ONLY)

## Steps (run live; show hostname + timestamp first)
1. Identity/load: `hostname; date; uptime; free -h`
2. Disk: `df -h` (flag mounts ≥80% warn, ≥90% alert; name top consumers e.g. `du -sh /var/log` if high)
3. Services: `systemctl --failed`; confirm watched services active (from USER.md/ops notes: e.g. nginx, docker, openclaw)
4. Network: `ss -tlnp` — compare against expected ports; unexpected listener = alert
5. Updates: `apt list --upgradable 2>/dev/null` — count total, call out security updates separately
6. Auth noise: failed SSH logins 24h (`journalctl -u ssh --since "24h ago"` | grep -ci failed; adjust unit if needed)
7. Certs (if domains in ops notes): days remaining each; <14d = alert
8. Backups: report last-backup timestamp from the configured location; missing = alert

## Report format
`🖥️ VM readiness — <hostname> (<time>): ✅ READY | ⚠️ READY-WITH-WARNINGS | 🔴 NOT-READY`
One line per check with ✅/⚠️/🔴 + numbers. For any ⚠️/🔴 add `Proposed action: <exact command>` and STOP.

## Guardrails (absolute)
- Read-only commands ONLY in this skill. Never delete, restart, update, or edit config.
- Any fix requires the user's explicit approval in chat, showing the exact command first.
- Log checks + any approved actions (command + output summary) to today's memory note.
