# Part 01 — Foundations
**Video:** 0:00:00 – 0:33:08 (Module 1)

**In this part:** 1.1 Claude, Anthropic & the model family · 1.2 Chat vs Claude Code · 1.3 The terminal · 1.4 The agentic loop

> This part has no install and no code. It exists because the rest of the course is confusing without it. Do not skip 1.3 and 1.4 — they are the two ideas every later module leans on.

---

## 1.1 Claude, Anthropic & the model family

### What it is
- **Anthropic** is the company; **Claude** is its AI model family. The relationship mirrors OpenAI → ChatGPT.
- Claude ships in **tiers**, not one model:
  | Tier | Character | Typical use |
  |---|---|---|
  | **Haiku** | Fastest, cheapest | Simple, high-volume, maintenance |
  | **Sonnet** | Balanced | Everyday coding and reasoning |
  | **Opus** | Most capable | Hard planning, architecture, deep reasoning |
- Some models offer **extended/adaptive thinking** (think longer before answering) and an **effort** setting — both are ways of spending more compute on a hard problem. ⚠️ Availability and version numbers (Haiku 4.5 / Sonnet 4.6 / Opus 4.7 at recording time) change; check the docs.

### Why it matters
- **Cost and limits are model-dependent.** Burning Opus on a rename wastes your plan; using Haiku to design an architecture gives you a shallow plan.
- The course's rule of thumb, reused everywhere later: **Opus plans → Sonnet builds → Haiku maintains.** It mirrors a senior/mid/junior team.
- Knowing the family lets you answer "which model should I use?" rationally instead of always picking the strongest.

### How to do it (step by step)
1. Open the model picker in whatever Claude surface you have (web, desktop, terminal) and read the available tiers and their descriptions.
2. Pick three real tasks from your own week: one trivial (rename/format), one normal (add a feature), one hard (design or debug something deep).
3. Assign a tier to each: trivial → Haiku, normal → Sonnet, hard → Opus. Write the mapping down; you'll reuse it in 3.2.
4. Note which models expose extended thinking and/or effort — you'll use both in 3.2.

**Lab 1.1 — Model mapping**
- [ ] List your three tasks and chosen tiers.
- [ ] For the "hard" task, write one sentence on why a faster model would fail at it.
- [ ] Sketch the senior/mid/junior analogy in your own words.

**Proof:** a written mapping of three tasks → three tiers with a one-line justification each.

**Quiz 1.1**
1. Which tier would you choose to investigate a failing test suite quickly, and why?
   a) Opus, because accuracy matters most  b) Sonnet, because everything should use one model  c) Haiku, because the task is narrow and high-volume  d) Whichever is newest
2. Explain why "always use the most powerful model" is a bad policy.
3. Your team says every task must use Opus "to be safe". Give two concrete costs of that rule and a one-line replacement policy.

---

## 1.2 Chat vs Claude Code: brain vs brain with hands

### What it is
- **Claude chat** (web/desktop) reasons and replies. It can read what you paste or share, but it **cannot touch your machine**.
- **Claude Code** is the *same* brain installed on your machine, able to **act**: create, edit and delete files and run commands.
- The course's analogy: chat is *a smart person on the phone*; Claude Code is **a brain with hands**.

### Why it matters
- It explains the course's whole shape: everything after this module is about **giving the hands better tools, rules and reflexes**.
- It stops the classic beginner error of expecting chat to change files, or expecting Claude Code to behave like a chatbot that only answers.
- It frames safety: hands can do damage, which is why permissions (3.4), hooks (7.4) and gating (12.4) exist.

### How to do it (step by step)
1. In Claude chat, ask for a small script — e.g. *"write a Python script that prints the Fibonacci sequence"*. Notice you get **text you must copy**.
2. Ask it to save the file for you. Notice it can't — there is no file in your project that changed.
3. Now install Claude Code (Part 2) or, if already installed, run `claude` in an empty folder and ask for the same script.
4. Watch the difference: it proposes a **file write** and asks your permission; approve it, then run the script from your terminal.
5. Write down the difference in one sentence, using the words *reason* and *act*.

**Lab 1.2 — Same request, two brains**
- [ ] Chat attempt done; note what you had to do manually (create file, paste, run).
- [ ] Claude Code attempt done; note what it did for you.
- [ ] One-sentence summary of the difference.

**Proof:** a working script file created by Claude Code in your folder, plus your one-sentence summary.

**Quiz 1.2**
1. Which statement is correct?
   a) Claude Code is Claude chat with a different theme  b) Claude Code is the same models with the ability to act on your machine  c) Claude Code is a separate, weaker model  d) Claude Code is a browser extension
2. Why does the "brain with hands" framing matter for safety?
3. A colleague says "I already use Claude in the browser, so installing Claude Code adds nothing." Give two things only Claude Code can do.

---

## 1.3 The terminal: how Claude gets hands

### What it is
- The **terminal** (shell) is a text interface where commands create, list, move and delete files and run programs. Everything the GUI does, the terminal can do — and more.
- Because Claude Code runs commands in your terminal, **terminal access *is* machine access**: whoever can run commands there can touch your files.
- Quick vocabulary the course demonstrates: `ls` (list), `mkdir` (make folder), `cd` (change folder), `touch` (create empty file), `rm` (delete). ⚠️ `rm` is destructive — never let a demo run it on anything you need.

### Why it matters
- You cannot judge Claude Code's risk profile without understanding what a shell can do. "It can read, write and execute" means *all of it* — including deleting.
- It demystifies the permission prompts you'll approve hundreds of times: each one is Claude asking to use the hands.
- It makes you a better operator: you'll recognise when a command is dangerous, and you'll write better hooks (7.4) because you know what you're blocking.

### How to do it (step by step)
1. Open a terminal: **Terminal** on macOS/Linux; **Windows Terminal**, **PowerShell** or **CMD** on Windows.
2. Make a scratch folder and enter it: `mkdir ~/claude-sandbox && cd ~/claude-sandbox`.
3. List what's there: `ls` (macOS/Linux) or `dir` (Windows CMD/PowerShell).
4. Create and verify: `touch hello.txt`, then `ls` — the file appears. On Windows PowerShell: `New-Item hello.txt`.
5. Make a subfolder: `mkdir notes`, then `ls` again; open your file manager side-by-side and watch the same folders appear there.
6. Optional but instructive: create a hidden file `touch .hidden`, then compare `ls` (doesn't show it) with `ls -la` (shows it). This is exactly the `.claude` behaviour from 3.5.
7. Do **not** run `rm` on anything yet — you'll do it deliberately in a lab in Part 7, guarded by a hook.

**Lab 1.3 — Terminal fluency basics**
- [ ] Created `~/claude-sandbox` and moved into it.
- [ ] Created `hello.txt` and `notes/`, confirmed with `ls`, and saw them in the GUI file manager.
- [ ] Demonstrated hidden files with `.hidden`, `ls` vs `ls -la`.
- [ ] Wrote down the five commands you used and what each does.

**Proof:** the sandbox folder containing `hello.txt`, `notes/` and `.hidden`, plus your five-line command glossary.

**Quiz 1.3**
1. Why is "Claude Code has terminal access" effectively the same as "Claude Code has access to my machine"?
2. Which command shows files that a plain `ls` hides?
3. You watch Claude propose `rm -rf ~/projects`. What is the risk, and where in the course do you learn to stop this automatically?

---

## 1.4 The agentic loop

### What it is
- The cycle Claude runs on **every** request:
  **ask → plan → act (read files, search, run commands) → observe the result → check → retry if needed → answer.**
- It is not a single question/answer exchange; it's an iteration loop, and that iteration is what makes Claude Code feel like it "understands" your project.
- The course's line: it isn't magic, it's iteration at very high speed.

### Why it matters
- Everything later is a **lever on this loop**: skills give it better procedures, hooks give it reflexes, MCP gives it more tools, subagents give it helpers, permissions control what it may do.
- It explains the permission prompts: the loop *acts*, so at each action point it can ask you.
- It explains failures too: if the loop can't observe what happened (no logs, no tests), it can't self-correct — which is why verification steps in CLAUDE.md matter so much.

### How to do it (step by step)
1. Start a session in a real project folder: `claude`.
2. Give a task that forces iteration, e.g. *"find every place we handle errors from the payments API and summarise the patterns you see."*
3. Watch the tool lines: reading files, searching, possibly running `grep`. That's the *act → observe* half.
4. Follow up with something that requires verification: *"now add a test for the missing case you found."* Watch it read the test conventions, write a test, run it, and fix it if it fails.
5. Note where you had to **approve** an action. Each approval is a loop step crossing from "think" to "do".
6. Write the loop out in your own words, then map each arrow to a course feature: plan→? act→? observe→? check→?

**Lab 1.4 — Watch one full loop**
- [ ] Ran an exploration task and observed at least three file reads.
- [ ] Ran a task that wrote code and executed something (test or script).
- [ ] Recorded each time you were asked for permission, and what it was for.
- [ ] Mapped loop stages to features: skills (procedure), hooks (reflex), MCP (tools), subagents (helpers).

**Proof:** a short log of one complete loop — task → actions taken → result → any retry — with one line per stage.

**Quiz 1.4**
1. Which sequence describes the agentic loop?
   a) ask → answer  b) ask → plan → act → observe → check → answer  c) plan → deploy → rollback  d) prompt → cache → respond
2. Why does the loop make permission prompts necessary?
3. Claude repeatedly "fixes" a bug but never verifies its fix. Based on the loop, name the weak stage and one change to CLAUDE.md that would strengthen it.

---

## Part 01 wrap-up

| Topic | Done | Lab proof | Quiz |
|---|---|---|---|
| 1.1 Model family | ☐ | Tier mapping | ☐ /3 |
| 1.2 Chat vs Code | ☐ | Script + summary | ☐ /3 |
| 1.3 Terminal | ☐ | Sandbox folder + glossary | ☐ /3 |
| 1.4 Agentic loop | ☐ | Loop log | ☐ /3 |

**Answers:** `13-answer-key.md` → Part 01.
**Next:** `02-install-and-auth.md` — get the hands installed and authenticated.
