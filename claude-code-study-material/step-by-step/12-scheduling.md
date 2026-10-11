# Part 12 — Scheduling & automation
**Video:** 11:07:28 – 11:56:47 (Module 12)

**In this part:** 12.1 Why + the three ways · 12.2 `/loop` & headless mode · 12.3 Routines & desktop tasks · 12.4 The safety playbook

---

## 12.1 Why schedule, and the three ways to do it

### What it is
- **The scenario.** Picture A: every morning you spend 30 minutes doing the same ritual — check failing tests, scan error logs, review open PRs, check the build, then post a status to Slack. Picture B: you arrive to a written standup, diagnosed failures, flagged risky PRs, and a briefing already in your inbox.
- The gap between the pictures is **scheduling**. Claude Code offers three ways:
  | | `/loop` | Desktop scheduled task | **Claude routine** |
  |---|---|---|---|
  | Runs on | your machine, current session | your machine | Anthropic's cloud |
  | Machine on? | yes | yes | **no** |
  | Session open? | yes | app running | no |
  | Persistence | until expiry (~3 days) ⚠️ | yes | yes |
  | Local files | yes | yes | fresh clone of your repo |
  | Triggers | interval / cron (min 1 min ⚠️) | time | schedule, API, **GitHub events** |
  | Best for | watching something now | local dashboards/processes | unattended recurring work |
- And the conceptual difference from classic cron: a cron script **executes blindly** — if the API errors, the script exits, and you find out hours later by reading logs. A scheduled Claude task **reasons**: it reads the error, tries an alternative, documents both failures, and sends a notification with a diagnosis.

### Why it matters
- This is the module that converts Claude Code from "a better autocomplete" into **leverage**: work that happens while you sleep, not work you must babysit.
- The three-way table answers the only question that matters operationally: *what must be true for this to run?* (machine on / session open / nothing).
- The reasoning-vs-execution difference is why this beats the cron jobs most engineers already have.

### How to do it (step by step)
1. **Find your own Picture A ritual**: list everything you do at the same time every day/week that is *checking, summarising or reporting*.
2. For each item, note whether it needs **local files** (→ machine-based) or only **remote data** (→ routine).
3. Pick one item to automate first; choose the mechanism from the table using two questions:
   - Must it survive my laptop closing? → **routine**
   - Is it a short-lived "watch until X happens"? → **`/loop`**
   - Is it local and recurring on a schedule? → **desktop task**
4. Write the run's **output contract** now (a file? a Slack message? a report path?) — you'll implement it in 12.2–12.3.
5. Local cron syntax refresher (still useful): `minute hour day-of-month month day-of-week`, e.g. "MWF at 8am". Generate it with an AI rather than memorising it.

**Lab 12.1 — Choose your first automation**
- [ ] Wrote your Picture A ritual as a list.
- [ ] Classified each item: local-only vs remote-ok.
- [ ] Chose one and the mechanism, with a one-line justification.
- [ ] Wrote the output contract (where the result lands).

**Proof:** the ritual list + your chosen automation + its mechanism + output contract.

**Quiz 12.1**
1. Give the three scheduling options and whether your laptop must be on for each.
2. What does a scheduled Claude task do that a cron script doesn't?
3. Which mechanism would you choose to "check every 5 minutes whether the deploy log says success, then stop"? Why?

---

## 12.2 `/loop` and headless mode

### What it is
- **`/loop`** — repeats a prompt or slash command on an interval **inside the current session**. It inherits the session's MCP servers and permissions, can access local files, supports intervals down to 1 minute, and stops when you close the session (or after its expiry, ~3 days ⚠️).
  ```
  /loop 2m check if deploy.log exists. If so, read its last 20 lines and tell me whether
           the deployment succeeded, failed, or is still in progress. If it succeeded, stop
           watching. If it failed, explain the error.
  ```
- **Headless mode** — `claude -p "<prompt>"` runs with **no interface** and **never blocks waiting for input**. Options like `--allowedTools` restrict what it may do; `--dangerously-skip-permissions` exists but belongs **only** in isolated containers/VMs.
- The crucial nuance: **headless is not a permission override.** It still enforces permissions — it simply has no UI to ask through. Without it, a scheduled run would hang forever on the first permission prompt.

### Why it matters
- `/loop` is the fast, local watchdog: perfect for "tell me when this finishes" with a stop condition.
- Headless is what makes **any** schedule trustworthy: cron, systemd, CI, routines — all need a run that can't stall on a prompt.
- The permission nuance prevents two opposite mistakes: expecting headless to bypass safety, or wiring a schedule that dies silently because it *needed* an approval.

### How to do it (step by step)
1. **Loop with a stop condition.** Create a file that changes (e.g. append to `deploy.log`), then run the `/loop` command above. Observe: it reports "still in progress", then "succeeded", then stops.
2. **Loop over something real**: `/loop 10m check for new PRs via the GitHub MCP; summarise the titles and authors; flag any touching auth or payment files`.
3. **Headless smoke test.** In your project:
   ```bash
   claude -p "summarise today's git log into reports/daily.md"
   ```
   Confirm: no UI, no questions, file written, exit cleanly.
4. **Headless with restricted tools:**
   ```bash
   claude -p "review the code for obvious issues" --allowedTools "Read,Grep,Glob"
   ```
   Confirm it can read but not write — and note that a request needing a write will simply not happen (it can't ask).
5. **Make a cron entry** that calls your headless command (or use the platform scheduler), then run it manually once first — never schedule something you haven't run by hand.
6. Write down the three failure modes you now understand: session closed (`/loop`), prompt that needed permission (headless), and expiry (~3 days ⚠️).

**Lab 12.2 — Loop and headless**
- [ ] Ran a `/loop` with an explicit **stop condition** and saw it stop.
- [ ] Ran a headless command by hand and got a written output file.
- [ ] Ran a headless command with `--allowedTools` and confirmed the restriction held.
- [ ] Created (and manually tested) one cron/scheduler entry that calls the headless command.
- [ ] Wrote your three failure modes with mitigations.

**Proof:** the loop output showing the stop, the headless output file, and the scheduler entry with its manual test result.

**Quiz 12.2**
1. What does headless mode change about permission handling, and what does it *not* change?
2. Why does a `/loop` stop working when you close your terminal?
3. Your scheduled headless job produced no output and no error. Give the two most likely causes.

---

## 12.3 Routines and desktop tasks

### What it is
- **Claude routines** — cloud-hosted scheduled automation:
  - triggers: **schedule**, **API call**, or **GitHub events** (PR opened/merged, release published, issue opened) with **filters** (author, title, body, regex),
  - execution: Anthropic's infrastructure spins up a **fresh clone** of your repo with your tools/MCP servers (GitHub, Slack, etc.),
  - results: files written, PRs opened, messages sent, reports generated — **while your laptop is closed**.
- **Desktop scheduled tasks** — recurring Claude work driven by your machine: good for local files, local processes, daily dashboards.

### Why it matters
- Routines remove the two constraints that make local scheduling fragile (machine on, session open) and add an event-driven mode that local cron can't do cleanly.
- GitHub-event triggers are how agentic work plugs into a real team workflow: PR opened → first-pass review comment, before a human even looks.
- Knowing both means you place each automation where it belongs: **cloud for unattended and event-driven, desktop for local and stateful**.

### How to do it (step by step)
1. **Design the run before creating it:** trigger → inputs → actions → output path → stop/abort condition → who reviews.
2. **Create a routine** in the UI: choose the trigger (schedule or GitHub event), add filters (e.g. ignore anything whose title contains "bug" if you only want feature reviews), and confirm the repo/credentials/agent settings.
3. **Start read-only.** First version analyses and reports; no writes to source. (12.4 covers the rest.)
4. **Test the trigger manually** (fire the event or run the routine once), read the logs, and check the output landed where you said.
5. **Create one desktop task** for something local (e.g. "read today's data, generate a dashboard, email it").
6. **Add a human gate** to anything irreversible, then watch the first few cycles before trusting it.

### Recipes worth stealing
| Recipe | Mechanism | Trigger | Action |
|---|---|---|---|
| PR first-pass review | Routine | GitHub: PR opened | Comment with a review + flag auth/payment files |
| Daily data quality | Routine | Schedule 6am | Run the data-quality skill, write output, post errors to Slack |
| Weekly code quality | Routine | Schedule Sun 11pm | Run tests, coverage, security scan |
| Monday planning | Routine | Schedule Mon 8am | Read last night's report → prioritised task list → assign via GitHub |
| Continuous docs | Routine | GitHub: push to main | Read changed files, update docs |
| Daily dashboard | Desktop task | Schedule | Read/process local data, generate dashboard, email via MCP |

**Lab 12.3 — One routine, one desktop task**
- [ ] Designed a run (trigger → inputs → actions → output → review).
- [ ] Created a routine with the correct trigger and filters.
- [ ] Ran it once, read the logs, verified the output.
- [ ] Created a desktop task for something local.
- [ ] Wrote the review gate for each.

**Proof:** the routine's log + output artefact, the desktop task definition, and your review-gate note.

**Quiz 12.3**
1. Name three trigger types for a routine and one filter example.
2. Why does a routine keep working when your laptop is closed, and what does it get instead of your local files?
3. Your routine runs on every PR — including dependency bumps. Give the filter you'd add and why.

---

## 12.4 The safety playbook for unattended work

### What it is
- What you're actually creating: a system that can read and write files, run bash, call external APIs, commit code, open PRs and send messages — **with nobody watching**. The course is blunt: these are not permissions you'd casually hand to anything.
- The five rules:
  1. **Start read-only.**
  2. **Write to non-destructive paths.**
  3. **Human review gates for irreversible actions.**
  4. **Log everything.**
  5. **Test for days before trusting it.**
- The rewrite pattern — *same goal, safe phrasing*:
  | ❌ Bad | ✅ Good |
  |---|---|
  | "Deploy when tests pass" | "When tests pass, write READY-TO-DEPLOY.md and ask a human in Slack to deploy" |
  | "Fix all lint errors in the codebase" | "Identify lint errors, write the list to reports/lint-issues.md, do not modify source files" |
- Also worth knowing: settings escape hatches exist (e.g. disabling automatic repo cloning for routines) and unattended runs consume plan limits fast — monitor usage and the extra-usage toggle.

### Why it matters
- Unattended mistakes are the expensive kind: nobody is there to say "stop". A wrong `rm`, a force push, or a bad deploy at 3am is exactly the failure this playbook prevents.
- The bad/good rewrite is a *thinking tool*: it forces you to separate **judgement** (AI can do) from **irreversible action** (a human should approve).
- Logging is not bureaucracy — it's the only way to debug something that ran while you slept.

### How to do it (step by step)
1. **Take your chosen automation and write its blast radius**: what can it read, write, execute, send, spend?
2. **Apply rule 1:** reduce the first version to analysis + a report file. Nothing else.
3. **Apply rule 2:** point all outputs at a non-destructive path (`reports/`, `logs/`, a Slack channel) — never at source files or your database.
4. **Apply rule 3:** for each irreversible step (deploy, push, delete, send to customers), insert a human gate: the agent writes a recommendation and asks; a person performs the action.
5. **Apply rule 4:** make sure a log exists per run (a hook, the routine's own logs, or an appended file) and that you know where to look.
6. **Apply rule 5:** run it manually for three consecutive cycles — same time, same conditions — and diff the outputs. Only then let it run unattended.
7. **Add the permissions layer:** deny rules in settings for destructive commands (`rm -rf`, `sudo`, `curl | bash`) and a `PreToolUse` guard hook (Part 7) so the guarantee holds even in auto modes.
8. **Write your automation charter** — 5 lines you'll apply to every future schedule:
   - read-only first; writes only to reports/
   - nothing irreversible without a human
   - every run logged
   - tested for 3 cycles before unattended
   - monthly review: is it still earning its tokens?

**Lab 12.4 — Harden your automation**
- [ ] Wrote the blast radius (read/write/execute/send/spend) of your automation.
- [ ] Converted it to read-only + report output.
- [ ] Inserted a human gate for each irreversible step and wrote the exact phrasing.
- [ ] Confirmed logging exists and you can find the log.
- [ ] Ran 3 manual cycles and compared outputs.
- [ ] Added deny rules + a guard hook, and wrote your automation charter.

**Proof:** the read-only version's outputs from three runs, your gate phrasings, and the charter.

**Quiz 12.4**
1. List the five safety rules for unattended agents.
2. Rewrite safely: "Every night, fix failing tests and push to main."
3. A colleague says logging is unnecessary because "the summary tells us what happened". Give two reasons they're wrong.

---

## Part 12 wrap-up

| Topic | Done | Lab proof | Quiz |
|---|---|---|---|
| 12.1 Three ways | ☐ | Ritual list + mechanism choice | ☐ /3 |
| 12.2 `/loop` & headless | ☐ | Loop stop + headless output + cron entry | ☐ /3 |
| 12.3 Routines & desktop | ☐ | Routine log + desktop task | ☐ /3 |
| 12.4 Safety playbook | ☐ | 3 read-only runs + charter | ☐ /3 |

**Answers:** `13-answer-key.md` → Part 12.
**Next:** `13-capstone.md` — put every lever to work in one build.
