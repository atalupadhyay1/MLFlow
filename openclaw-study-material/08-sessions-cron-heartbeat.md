# Chapter 8 — Sessions, Cron Jobs & the Heartbeat: An Agent That Works While You Sleep
*Course section: Scheduling & automated workflows · Time: ~75 min + Lab 8 (45 min)*

## Learning objectives
- Tune sessions (scope, resets) so context stays fresh and costs stay sane.
- Schedule work with **cron jobs** (exact times) and the **heartbeat** (periodic initiative) — and know which to use when.
- Write a `HEARTBEAT.md` that is useful, not expensive.
- Estimate and control the API cost of "always-on" behaviour.

---

## 8.1 Sessions, finished properly
From Ch 2: a session is one conversation's living context. Your three levers (in `session` config):
- **Scope** — `per-sender` gives each person their own thread (assistant-grade default).
- **Reset triggers** — `/new`, `/reset` on demand.
- **Automatic resets** — daily (e.g. 4 AM, when nobody's mid-thought) and/or idle timeout (e.g. a week of silence = archive it).

**Rule of thumb:** Fresh day, fresh session; same task, same session. Manually `/new` when switching from "plan my trip" to "debug my server" — mixed desks confuse agents exactly like they confuse humans.

Compaction sits beside sessions: when history grows, older turns compress into summary notes (`compaction: { mode: "safeguard" }`). Enable it; context explosions are the silent killer of long-running assistants.

## 8.2 Cron jobs — the alarm clock (exact, scheduled, reliable)
Use cron when timing is precise and the task is self-contained: *08:00 briefing, Sunday 20:00 report, every-6-hours job scan.*

Anatomy: **schedule** (cron expression or interval) + **payload** (the instruction the agent wakes up to) + **delivery** (which channel/chat gets the result). Managed via OpenClaw's cron tooling/CLI in your version — inspect with the dashboard/cron commands (`openclaw cron`-style tooling; confirm exact verbs with `openclaw --help` / docs, they evolve fastest here).

Example job (briefing — powered by your Ch 7 skill):
```json
{
  "name": "weekday-morning-brief",
  "schedule": "0 8 * * 1-5",
  "payload": "Run the daily-brief skill for my topics in USER.md. Send the brief to my Telegram. If nothing significant, reply with one line: 'Quiet morning — nothing needs you.'",
  "delivery": "telegram"
}
```
(Ready-to-adapt jobs: `templates/configs/cron-jobs.example.json`.)

**Cron craft guidelines (learned from everyone's mistakes):**
1. Payloads must be **self-sufficient** — the 8 AM agent hasn't read your midnight chat. Include sources, format, length, destination.
2. **Idempotent & quiet-by-default**: "if nothing found, say one line" beats a daily empty report you'll start ignoring (alert fatigue kills agents faster than bugs).
3. One job = one outcome. Briefing and job-scan are two jobs, two payloads, separately pausable.
4. Test-run a job **manually once** before trusting its schedule.

## 8.3 The heartbeat — initiative on a timer (periodic, judgement-based)
The heartbeat wakes the agent every N (e.g. `heartbeat: { every: "30m" }`) with its `HEARTBEAT.md` checklist. Unlike cron's fixed task, the heartbeat asks: *"Anything need attention?"* — email flags? calendar soon? server unhappy? Nothing? Then it stays silent (`HEARTBEAT_OK`-style no-op) and costs almost nothing.

```markdown
# HEARTBEAT.md
- Check server health skill; alert ONLY if disk >85% or a watched service is down.
- If a calendar event starts within 2h and I haven't been told, remind me.
- Otherwise reply HEARTBEAT_OK. Never send chatter.
```
**Heartbeat law:** Every item must have a *silence condition*. A heartbeat without "otherwise stay quiet" becomes a needy, expensive parrot. Also: empty/comment-only HEARTBEAT.md = heartbeats skip the API call entirely — the cheapest state, and the right default until you design yours.

## 8.4 Cron vs Heartbeat — decide in 5 seconds
| Ask yourself | Cron | Heartbeat |
|---|---|---|
| "Must happen *at 8:00 sharp*?" | ✅ | |
| "Self-contained known task?" | ✅ | |
| "Check periodically & use judgement?" | | ✅ |
| "Frequency: fixed schedule" | ✅ | "every 30m-ish, flexible" ✅ |
| Course mantra | **Cron = timing** | **Heartbeat = monitoring** |

## 8.5 The cost talk (have it now, not on invoice day)
Each wake-up = model call(s) + tool calls. Estimate: `wake-ups/day × round-trips × tokens`. A 30-min heartbeat = 48 potential calls/day; with strict silence conditions most return instantly cheap — but only if the design forces tiny outputs and minimal tool use. Tactics: cheap/fast model for heartbeat jobs, strong model for the weekly report; longer intervals (30–60m) unless urgency is real; logs review weekly (Ch 13's ops routine). Put a **spending cap/alert at your LLM provider** today. Yes, today.

## 8.6 🧪 Lab 8 — Schedule your morning (45 min)
1. Ensure the Ch 7 `daily-brief` (or equivalent) skill works on demand in Telegram.
2. Create a cron job for **tomorrow 08:00 your timezone** using the template; payload includes topics, 200-word cap, quiet-line rule.
3. Trigger it manually now (cron run/test facility in your version or ask the agent to "run the morning brief job now") — verify format on Telegram.
4. Write a minimal `HEARTBEAT.md` (server-check item only if you've done Ch 12; otherwise calendar/placeholder with silence rule), set `every: "30m"`, observe two cycles in logs.
5. Journal: cost per briefing run (provider dashboard), and your chosen heartbeat interval + why.
**✅ Expected:** One on-schedule brief received; heartbeat cycles visible and *silent* when nothing's wrong. Disable the heartbeat afterwards if you're not ready to run it — intentional off beats accidental bill.

## ⚠️ Traps
| Trap | Antidote |
|---|---|
| Job fires, does nothing useful | Payload leaned on chat context — rewrite self-sufficiently |
| Brief repeats yesterday's items | Payload must instruct memory-note dedupe (build it into the skill) |
| Heartbeat spams chat | Missing silence condition / HEARTBEAT_OK discipline |
| Jobs fire at wrong hour | VM timezone ≠ yours — set/assert timezone in payload & server (`timedatectl`) |

## 🎯 Self-check
1. Cron vs heartbeat in four words each? → *Exact-time task vs periodic judgement.*
2. The payload's #1 design rule? → *Self-sufficient (no chat context assumed).*
3. Cheapest heartbeat? → *Empty HEARTBEAT.md / disabled until designed.*

**→ Next: [Chapter 9 — Project 1: The Job-Search Agent](09-project-1-job-search-agent.md)**
