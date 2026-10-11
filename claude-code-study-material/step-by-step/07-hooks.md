# Part 07 — Hooks: background automation, zero tokens
**Video:** 5:40:13 – 6:49:12 (Module 7)

**In this part:** 7.1 What, why & the event list · 7.2 Configuration · 7.3 The contract (stdin, exit codes, structured output) · 7.4 Building four hooks that matter

---

## 7.1 Hooks: what they are and why they behave differently from prompts

### What it is
- A **hook** is a command (shell, Python, anything executable) that runs automatically when a **lifecycle event** fires in Claude Code — before/after tool use, session start/stop, notifications, and more.
- Hooks run **outside the model**: no prompt, no context, no tokens. They are ordinary software with deterministic behaviour.
- The full event list (course reference): `SessionStart`, `UserPromptSubmit`, prompt expansion, `PreToolUse`, permission request/denial, `PostToolUse`, `Notification`, subagent start/stop/failure, task created/completed, `Stop`, `SessionEnd`, pre-compact.
- Hooks receive **JSON on stdin** describing the event (which tool, what arguments), and return a result via **exit code** or structured JSON on stdout.

### Why it matters
- **Prompts are suggestions; hooks are guarantees.** "Please format the code after each edit" can be forgotten or argued with. A `PostToolUse` hook *always* runs.
- They cost nothing per invocation, so they're ideal for high-frequency chores: formatting, logging, notifications, small deterministic rewrites (e.g. normalising punctuation).
- They're your **hard safety layer**: a `PreToolUse` guard blocks destructive commands even when the session is in an auto or bypass mode where nothing else asks.

### How to do it (step by step)
1. **Choose the moment, not the tool.** Ask: should this run *before* an action (verify/block) or *after* it (fix/log/notify)?
   - Block/verify → `PreToolUse`
   - Fix/log after → `PostToolUse`
   - Around the session → `SessionStart` / `Stop` / `SessionEnd`
2. Make the *cheapest possible thing* that does the job: usually a shell one-liner, escalating to a Python script only when you need logic.
3. Write the script, then **test it by hand** before wiring it up:
   ```bash
   echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /"}}' | python .claude/hooks/guard.py; echo "exit=$?"
   ```
4. Wire it into settings (7.2), restart the session, and trigger the event deliberately.
5. Verify both branches: the path that should pass **and** the path that should block. A guard you never saw block is a guard you don't know works.
6. Keep a short list of hooks in your notes with their trigger and purpose — you'll accumulate them.

**Hook vs prompt vs skill — pick correctly**
| Need | Use | Why |
|---|---|---|
| Must happen every single time | **Hook** | Deterministic, zero tokens |
| A procedure with judgement | Skill | Instructions + scripts, invoked when relevant |
| A policy you want to block on | **Hook** (`PreToolUse`, exit 2) | Works even in bypass mode |
| A one-off instruction | Prompt | No permanence needed |

**Lab 7.1 — Map your first hook**
- [ ] Chose a real annoyance that happens on *every* edit or command.
- [ ] Decided the correct event and wrote one sentence on why before/after.
- [ ] Tested the raw script by hand with a fake JSON payload.
- [ ] Wrote the hook into your personal hooks list.

**Proof:** the tested script output (`exit=0` and the blocked case's `exit=2`), plus your hooks list entry.

**Quiz 7.1**
1. Why do hooks cost no tokens, and what does that have to do with the agentic loop?
2. Which event would you use to stop a command before it runs?
3. Name one thing that should be a hook and one that should be a prompt, and why.

---

## 7.2 Configuring hooks

### What it is
- Hooks are declared in **`settings.json`** (project `.claude/settings.json`, or user `~/.claude/settings.json`) under the `hooks` key. The scripts themselves usually live in `.claude/hooks/`.
- Anatomy of an entry:
  - **event name** (`PreToolUse`, `PostToolUse`, `SessionStart`, `Stop`, …) — the key,
  - **`matcher`** — which events/tools it applies to (e.g. `"Bash"`, `"Write|Edit"`, a regex),
  - **`hooks`** — a list of commands, each with `type: "command"`, the `command` string, and optional **`timeout`** and **`async`**.
- `async: true` lets Claude continue while the hook runs in the background — right for logging and notifications, wrong for anything Claude must see the result of.

### Why it matters
- `matcher` is where hook bugs usually live: a hook that never fires, or fires everywhere, is nearly always a matcher mistake.
- `timeout` protects your workflow from a hanging script (a hook that never returns blocks the action).
- Getting the file location and scope right is the difference between a personal convenience and a team standard.

### How to do it (step by step)
1. **Let Claude write the first one.** Ask: *"Add a PostToolUse hook matching Write|Edit that runs our formatter on the file — add it to this project's settings."* Reason: writing settings while the tool is initialising can lead to your hand-written file being overwritten and the hook lost. Let Claude merge it, then inspect.
2. Read the resulting JSON and confirm the three parts: event, `matcher`, `command`.
3. Add `timeout` and, where appropriate, `async`:
   ```json
   {
     "hooks": {
       "PostToolUse": [
         { "matcher": "Write|Edit",
           "hooks": [
             { "type": "command", "command": "python .claude/hooks/auto_format.py", "timeout": 30 },
             { "type": "command", "command": "python .claude/hooks/session_logger.py", "async": true }
           ] } ]
     }
   }
   ```
4. Restart the session (or start a new one) — settings are read at start.
5. **Trigger it and prove it fired**: edit a file and check your hook's side effect (formatted code, new log line, notification).
6. Decide scope: personal convenience → user scope; team guarantee → project scope and commit it.

**Lab 7.2 — Wire and prove one hook**
- [ ] Had Claude add a hook to project `settings.json` (not hand-written).
- [ ] Confirmed event + matcher + command in the file.
- [ ] Added a `timeout`, and `async: true` where it made sense.
- [ ] Restarted and proved the hook fired with a visible side effect.
- [ ] Committed it and wrote one line on why project scope was right.

**Proof:** the settings block, the side effect (log line / formatted file), and your commit.

**Quiz 7.2**
1. What are the three parts of a hook entry, and which one decides when it fires?
2. Why is `async: true` wrong for a hook that must block an action?
3. Your hook never fires on file writes. Give two matcher-level causes and one settings-level cause.

---

## 7.3 The contract: stdin JSON, exit codes, structured output

### What it is
- **Input:** your hook receives JSON on **stdin**. For tool events that includes fields like `tool_name` (e.g. `"Bash"`, `"Write"`) and `tool_input` (e.g. the exact `command`, the `file_path`). Always parse defensively — if stdin isn't valid JSON, exit cleanly (0) rather than crashing the session.
- **Exit codes** are the decision:
  | Code | Meaning |
  |---|---|
  | `0` | allow / continue normally |
  | `2` | **block the action**; stderr is sent back to Claude as the reason |
  | other non-zero | non-blocking error (logged, doesn't stop Claude) |
- **Structured output (advanced):** instead of an exit code you may print JSON with `hookSpecificOutput`, e.g.
  ```json
  { "hookSpecificOutput": {
      "hookEventName": "PreToolUse",
      "permissionDecision": "deny",
      "permissionDecisionReason": "Destructive command blocked by hook" } }
  ```
  This lets a hook *decide* (allow / deny / ask) rather than just pass or fail.
- **Why exit 2 is the emergency brake:** in auto or bypass modes nothing else is asking you. Exit 2 stops the tool anyway — the course's mnemonic: *"you shall not pass."*

### Why it matters
- Most hook debugging is contract debugging: wrong field name, unparsed stdin, wrong exit code. Knowing the contract means fixing it in minutes.
- `exit 2` plus a *useful stderr message* is what makes a guard teachable: Claude receives the reason and proposes a safer alternative instead of blindly retrying.
- Using `permissionDecision: "ask"` gives you a middle path: flagging suspicious-but-not-certain actions for human attention.

### How to do it (step by step)
1. Write a minimal inspector hook to see what a real event looks like:
   ```bash
   #!/usr/bin/env bash
   cat > /tmp/hook-input.json     # dump stdin for inspection
   echo "[hook] event captured" >&2
   exit 0
   ```
2. Trigger the event, then read `/tmp/hook-input.json` and note the actual field names (`tool_name`, `tool_input.command`, `tool_input.file_path`).
3. Build a guard using those fields, and always keep an **allow path**:
   ```python
   import json, sys, re
   BLOCKED = [r"rm\s+-rf\s+[/~.]", r"git\s+reset\s+--hard", r"curl\s+.*\|\s*bash"]
   try:
       event = json.load(sys.stdin)
   except json.JSONDecodeError:
       sys.exit(0)                      # never crash the session
   if event.get("tool_name") != "Bash":
       sys.exit(0)
   cmd = event.get("tool_input", {}).get("command", "")
   for pat in BLOCKED:
       if re.search(pat, cmd, re.I):
           print(f"BLOCKED by security hook: matched {pat}\nCommand was: {cmd}\nUse a safer alternative.",
                 file=sys.stderr)
           sys.exit(2)                  # the emergency brake
   sys.exit(0)
   ```
4. Prove **both** branches by hand: a harmless command (`ls`) → `exit=0`; a destructive one → `exit=2` with your message on stderr.
5. Wire it as `PreToolUse` on `Bash`, then ask Claude to do something destructive and confirm it is blocked *and* that Claude explains the block and suggests an alternative.
6. Add the JSON-decision variant to your notes for cases where you want "ask" instead of a hard deny.

### Quick reference
```
stdin  → {"tool_name": "Bash", "tool_input": {"command": "…"}}
exit 0 → allow        exit 2 → BLOCK (stderr → Claude)        other → non-fatal error
stdout → {"hookSpecificOutput": {"hookEventName":"PreToolUse",
          "permissionDecision":"allow|deny|ask", "permissionDecisionReason":"…"}}
```

**Lab 7.3 — Build and prove a guard**
- [ ] Captured a real event payload to a file and identified the fields.
- [ ] Built a guard with a proper allow path and defensive JSON parsing.
- [ ] Proved `exit=0` and `exit=2` by hand.
- [ ] Blocked a real destructive request through Claude Code and captured Claude's explanation.
- [ ] Noted when you'd use `"ask"` instead of `"deny"`.

**Proof:** the guard script, the two exit codes from your own terminal, and the transcript of the blocked request.

**Quiz 7.3**
1. What are the three exit outcomes in a hook, and what does each do?
2. Why does a blocked hook produce a *better* outcome than a silently failed permission?
3. Your guard returns exit 1 "to be safe". What actually happens, and why is that wrong?

---

## 7.4 Four hooks worth building (with testing discipline)

### What it is
The course's working set — each one earns its place immediately:
1. **Notification hook** — tell you when Claude needs input (macOS `osascript`; Linux/Windows equivalents). Copy the snippet from the official hooks guide.
2. **Security guard** (`PreToolUse` on `Bash`) — regex blocklist: `rm -rf /`, `rm -rf *`, `rm -r *`, `git reset --hard`, `DROP TABLE/DATABASE`, `chmod 777`, `curl … | bash`, `wget … | sh`.
3. **Auto-format** (`PostToolUse` on `Write|Edit`) — run `black` for `.py`, `prettier` for JS/TS/JSON/CSS; log the result; keep it fast.
4. **Session logger** (`SessionStart` / `Stop` / on `Bash`) — append timestamped lines to a log file so you can reconstruct what happened while you were away.

### Why it matters
- Together they cover the three hook jobs: **notify me**, **protect me**, **tidy up after me**.
- The auto-format demo proves the value viscerally: ask for deliberately messy code and watch it become clean seconds later, without a prompt and without tokens.
- The guard demo proves that exit 2 survives auto/bypass modes — the course deliberately tries to `rm -rf` a folder and gets a refusal with a safer suggestion.

### How to do it (step by step)
1. **Notification:** paste the official snippet into `settings.json`, then trigger it — walk away mid-task and confirm you're pinged when Claude waits for input.
2. **Guard:** wire the script from 7.3, then attempt a destructive action. Confirm: block + explanation + alternative. Then verify the allow path still works for normal commands.
3. **Auto-format:** create `messy.py` with bad spacing and no blank lines, ask Claude to write it, and watch the formatter fix it after the write. Log each formatting event to a file.
4. **Logger:** add a logger to `SessionStart` and `Stop` (async). Start a session, do something, exit, then read the log file.
5. **Test everything by hand first.** For each hook: craft a sample payload, run the script, check the exit code. Never debug a hook through Claude.
6. **Tune the noise.** If the formatter slows every edit, cut its scope (only `.py`) or move slow work to `async`. A hook that degrades the workflow gets deleted — correctly.
7. Commit the set (project scope) and add a line to CLAUDE.md: *"Formatting and guard hooks run automatically; don't re-ask for them."*

### The five hook gotchas
1. Hooks are **code running with your permissions** — a buggy one can break every edit. Test in isolation.
2. Keep them **fast**; use `timeout` and `async`.
3. **Matcher mistakes** are the #1 cause of "my hook doesn't fire".
4. Settings are read at **session start** — restart after editing.
5. Prefer hooks for **policy and hygiene**, not judgement calls.

**Lab 7.4 — The starter hook pack**
- [ ] Notification hook working (you were actually pinged).
- [ ] Security guard blocking a real destructive attempt, with Claude explaining it.
- [ ] Auto-format cleaning a messy file within seconds of writing it.
- [ ] Session log capturing at least two session boundaries.
- [ ] All four tested by hand first; the set committed to the project and noted in CLAUDE.md.

**Proof:** log file with formatting + session entries, the blocked-command transcript, and the committed settings.

**Quiz 7.4**
1. Why does the course insist you test hooks by hand instead of through Claude?
2. Your formatter hook adds 4 seconds to every edit on a large repo. Name two fixes.
3. Which of the four hooks would still work correctly in bypass-permission mode, and why does that matter?

---

## Part 07 wrap-up

| Topic | Done | Lab proof | Quiz |
|---|---|---|---|
| 7.1 What, why, events | ☐ | Tested script + hooks list | ☐ /3 |
| 7.2 Configuration | ☐ | Settings block + fired hook | ☐ /3 |
| 7.3 The contract | ☐ | Guard + exit codes + block transcript | ☐ /3 |
| 7.4 Four hooks | ☐ | Logs + blocked transcript + commit | ☐ /3 |

**Answers:** `13-answer-key.md` → Part 07.
**Next:** `08-mcp.md` — connect Claude to the outside world.
