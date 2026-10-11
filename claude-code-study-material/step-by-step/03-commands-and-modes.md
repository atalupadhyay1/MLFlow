# Part 03 — Commands, model control & permission modes
**Video:** 1:22:17 – 2:58:27 (Module 3)

**In this part:** 3.1 Slash commands · 3.2 Model, effort & cost · 3.3 Session commands · 3.4 Permission modes · 3.5 The `.claude` directory

> This is your daily control panel. Nothing here is exotic — but fluency here is the difference between fighting Claude Code and steering it.

---

## 3.1 Slash commands: the daily essentials

### What it is
- Commands typed as `/name` inside a session. The course demos 70+; you need ~15 fluently.
- Grouped by what they control:
  - **Session:** `/clear`, `/compact`, `/rewind`, `/branch`, `/resume`, `/status`
  - **Brain:** `/model`, `/effort`
  - **Money & capacity:** `/cost`, `/context`
  - **Setup:** `/init`, `/permissions`, `/login`, `/logout`, `/help`
  - **Extensions:** `/agents`, `/mcp`, `/plugins`, `/loop`
- **Custom commands** are Markdown files in `.claude/commands/` — the filename becomes the command (e.g. `pr-description.md` → `/pr-description`).

### Why it matters
- Two of them alone (`/clear` between tasks, `/context` when quality drops) prevent most "the AI got worse" experiences.
- Custom commands turn your repeated prompts into team assets — the cheapest automation in the whole course (before skills and hooks).
- Knowing the namespace means you look for an existing command before inventing a workflow.

### How to do it (step by step)
1. In a session, type `/` and read the list; then `/help` for descriptions.
2. Practise the five you'll use daily: `/status`, `/context`, `/cost`, `/compact`, `/clear`.
3. Create a custom command:
   1. Make `.claude/commands/` in a project (create it if missing).
   2. Add `pr-description.md` containing the prompt you'd otherwise retype — e.g. *"Look at the staged git diff and write a PR description: one-line title, what changed and why, how to test, any breaking changes."*
   3. Restart or reload the session, type `/pr-description`, and confirm it expands and runs.
4. Commit `.claude/commands/` so your team inherits it.

**Lab 3.1 — Build one custom command you'll reuse**
- [ ] Ran `/help` and located three commands you didn't know.
- [ ] Created `.claude/commands/pr-description.md` (or another workflow you repeat weekly).
- [ ] Invoked it successfully on real staged changes.
- [ ] Committed it and explained in one line why a command is cheaper than a skill or a hook for this job.

**Proof:** the committed command file plus its successful output.

**Quiz 3.1**
1. Where do custom slash commands live, and how does a file become a command?
2. Which command would you run immediately after a long research session you plan to continue?
3. You paste the same 6-line prompt every Monday. Rank your options (prompt, custom command, skill, hook) by effort and say which you'd pick first and why.

---

## 3.2 Controlling the model, effort and cost

### What it is
- `/model` — switch the model mid-session. Claude Code warns that the conversation is **cached for the current model**, so switching means the full history gets read again on your next message.
- `/effort` — sets how much thinking the model spends (low → medium → high → max). The course's framing: a *difficulty slider*, not a quality setting.
- `/cost` — session cost, tokens, duration, lines changed, and **plan usage** (e.g. *current session 2%, current week 18%*), often broken down per model.

### Why it matters
- **Model + effort are your two biggest cost levers** after context hygiene (Part 5). A hard task on Opus/high can be cheaper overall than five failed attempts on Haiku/low.
- The cache warning prevents a common waste: thrashing models every few messages, each switch re-reading the whole conversation.
- `/cost` is the only honest feedback loop you have. Without it, "context management" is theory.

### How to do it (step by step)
1. Run `/model` and read the warning text carefully. Switch to a cheaper model once; send a message; then `/cost` and note the difference.
2. Set effort deliberately: `/effort high` before a complex debugging or design task; `/effort low` for mechanical edits. Compare `/cost` after each.
3. Establish your working pattern (the course's): **plan on the strongest model, build on the balanced one, maintain on the cheap one.**
4. Build a small experiment: same task, twice.
   - Attempt A: cheap model + low effort on something genuinely hard.
   - Attempt B: strong model + high effort on the same task.
   - Record tokens, cost and whether the result actually worked.
5. Save your personal rule in CLAUDE.md or notes: *"Plan with ___, build with ___, maintain with ___; effort ___ for routine, ___ for hard."*
6. Check `/cost` after any heavy run as a habit — especially before a subscription limit surprises you.

**Lab 3.2 — Cost experiment**
- [ ] Read the `/model` cache warning and reproduced it (switch, then `/cost`).
- [ ] Ran the A/B experiment on one hard task; recorded cost and success for each arm.
- [ ] Wrote your personal model/effort policy.
- [ ] Captured a `/cost` screenshot or note before and after a heavy task.

**Proof:** a two-row experiment table (model, effort, tokens, cost, worked?) and your written policy.

**Quiz 3.2**
1. Why is switching models mid-session expensive, and what does Claude Code do to compensate?
2. What is the difference between `/model` and `/effort` conceptually?
3. Your session shows 18% of the weekly window used after one day and costs are climbing, but you can't switch models mid-task. Name two things you'd change besides the model.

---

## 3.3 Session commands: `/compact`, `/clear`, `/rewind`, `/branch`, `/resume`

### What it is
- `/compact` — summarise the conversation into less context and **continue in the same session**. You can (and should) pass instructions about what to keep.
- `/clear` — start a **new session with empty context**; the previous session stays on disk.
- `/rewind` — go back to an earlier point in the conversation.
- `/branch` (fork) — continue from the current point in a **new session with its own ID**, leaving the original intact.
- `/resume` — reopen a previous session.

### Why it matters
- These five are the *actual* mechanism of context hygiene from Part 5. "Manage your context" is meaningless without them.
- `/branch` is the unsung one: it lets you try a risky direction ("what if we added this feature?") without contaminating a working session.
- `/compact` with instructions is the difference between losing your architecture notes and keeping them.

### How to do it (step by step)
1. Hold a short conversation in a scratch project; send 6–8 messages.
2. `/rewind` to an earlier message; notice the conversation re-anchors there.
3. From that point, `/branch` and confirm you're in a **new session with a different ID** (the original is untouched).
4. Back in a session, run `/compact` with no instructions once, then `/context` — observe the shrink.
5. Repeat with **explicit instructions**: `/compact keep the file structure, API endpoints, the React component layout and the coding patterns established`. Compare what survives.
6. Run `/clear`, confirm the counter resets to a near-empty baseline, then `/resume` the earlier session and confirm it's still on disk and intact.

### The instruction you should memorise for `/compact`
> "Keep: the file structure, the API surface, the naming/patterns we established, and any open TODOs. Drop: exploration we already resolved."

**Lab 3.3 — Session surgery**
- [ ] Rewound, branched, and verified the two sessions have different IDs.
- [ ] Compacted once without instructions and once with; recorded `/context` after each.
- [ ] Cleared and resumed; confirmed nothing was lost from disk.
- [ ] Wrote your standard `/compact` sentence.

**Proof:** a table of `/context` numbers for *before*, *compact-blind*, *compact-with-instructions*, and *after clear*.

**Quiz 3.3**
1. `/compact` vs `/clear` — what happens to the conversation in each case?
2. When is `/branch` better than `/rewind`?
3. Claude is 40 messages deep, working well, but drifting on conventions. Which command, with what instruction, and why not the others?

---

## 3.4 Permission modes

### What it is
The control over how much autonomy Claude Code has. The course calls this the most important safety concept — and the most misunderstood.

| Mode | Behaviour | Use for |
|---|---|---|
| **Default** | Asks before edits/commands; reads are free | Learning, sensitive repos |
| **Accept edits** | Auto-approves file edits + common FS commands (mkdir/touch/move/copy) | Iterating on code you're reviewing |
| **Plan** | Read-only; explores and presents a plan before editing | Unfamiliar codebases, big changes |
| **Auto** | Runs actions with a background safety check | Long tasks; avoids "yes fatigue" (course's recommended default once comfortable) |
| **Don't ask** | Only pre-approved tools run | Locked-down CI/scripts |
| **Bypass permissions** | Nearly everything runs | **Only** isolated containers/VMs ⚠️ |

- **Shift+Tab** cycles the common ones in-session (normal → accept edits → plan).
- Permission *rules* in `settings.json` (allow/deny lists) layer on top — mode is the policy, rules are the exceptions.

### Why it matters
- It is the primary defence between an agent and your filesystem. Everything else (hooks, gating, read-only schedules) is defence in depth.
- Choosing the wrong mode is how people get burned: bypass on a real repo, or accept-edits on a repo with production credentials.
- Understanding modes lets you be *fast* safely — auto mode exists precisely because prompting for every `mkdir` destroys flow.

### How to do it (step by step)
1. In a **throwaway** repo, create a file with Claude in default mode. Watch the prompt; read every option it offers (yes / allow all edits this session / no).
2. Press **Shift+Tab** to **plan mode**. Ask for a change. Confirm Claude explores and *presents a plan* without editing — then approve or reject the plan.
3. Shift+Tab to **accept edits**. Ask for two file edits; confirm they apply without prompts. Note which non-edit commands still prompt.
4. Shift+Tab to **auto**. Ask for a small multi-step task and observe that it runs with background checks instead of asking constantly.
5. Add a permission rule to `.claude/settings.json` and confirm it works:
   ```json
   {
     "permissions": {
       "allow": ["Bash(git commit*)", "Bash(python -m pytest*)"],
       "deny":  ["Bash(rm -rf*)", "Bash(sudo*)", "Bash(curl* | bash*)"]
     }
   }
   ```
6. Attempt a denied action and confirm it's blocked. Then write your **mode policy**: which mode for (a) learning, (b) my own repo, (c) a repo with secrets, (d) automation.

### Mode policy worksheet
- Learning / a new codebase → ______
- Daily work on a trusted repo → ______
- Anything with credentials or client data → ______
- Unattended / scheduled work → ______ (see 12.4)

**Lab 3.4 — Feel the difference**
- [ ] Tested all four practical modes on a throwaway repo.
- [ ] Verified one allow rule and one deny rule from `settings.json`.
- [ ] Wrote your four-line mode policy.
- [ ] Explained in one line why bypass is *not* a productivity setting.

**Proof:** the settings file with allow/deny rules, plus a note showing a blocked action and your mode policy.

**Quiz 3.4**
1. Which mode is read-only, and what does it still allow?
2. Why does the course recommend auto mode once you're comfortable rather than bypass?
3. A teammate sets bypass on the production repo "for speed". Give the two-sentence objection and the alternative you'd propose.

---

## 3.5 The `.claude` directory

### What it is
- The hidden control folder for Claude Code. Two instances matter:
  - **Project:** `./.claude/` — travels with the repo, shared with the team.
  - **User:** `~/.claude/` — your machine-wide settings, agents, preferences.
  - (Enterprise/managed scope also exists for organisations.)
- Typical contents: `CLAUDE.md`, `settings.json`, `settings.local.json`, `rules/`, `skills/`, `agents/`, `commands/`, `hooks/`, MCP config (`/.mcp.json`), plugins, plus logs.
- Hidden by design (dot-prefix): `ls` won't show it, `ls -la` will. Finder/Explorer need hidden files enabled.

### Why it matters
- **Everything you configure lives here or is referenced here.** Skills, agents, hooks, MCP, permissions — if it's not in a recognised `.claude` location, Claude Code doesn't see it.
- The split between project and user scope *is* the sharing model: what the team gets vs what only you get.
- Scope confusion causes the classic "I added an agent and it isn't showing up" problem. Knowing the map fixes it in seconds.

### How to do it (step by step)
1. In a project, create the folder if it doesn't exist: `mkdir -p .claude` (project) — and inspect `ls -la ~/.claude` (user).
2. Compare the two: list both trees and note which files exist where. (`ls -la .claude ~/.claude`)
3. Confirm the hidden behaviour: plain `ls` misses it; `ls -la` shows it; your file manager shows it only with hidden files enabled.
4. Create one artefact in **each scope** and observe the sharing difference:
   - Project: `.claude/commands/hello-project.md` (committed, team-wide).
   - User: `~/.claude/commands/hello-me.md` (personal, all projects).
   - Invoke both with `/` and confirm they exist in different worlds.
5. Add a `settings.local.json` override and note in one line how it differs from `settings.json` (personal, should not be committed).
6. Sketch the map in your notes:
   ```
   project/.claude/   CLAUDE.md · settings.json · settings.local.json
                      rules/ · skills/ · agents/ · commands/ · hooks/ · .mcp.json
   ~/.claude/         same idea, all projects · projects/ (session history)
   ```

**Lab 3.5 — Two-scope proof**
- [ ] Both scopes inspected and compared.
- [ ] One command created in project scope, one in user scope; both invoked.
- [ ] `settings.local.json` created and explained.
- [ ] Map drawn in your notes with one line on what each scope is *for*.

**Proof:** two working custom commands from different scopes, plus your annotated map.

**Quiz 3.5**
1. Why doesn't `ls` show `.claude`, and how do you see it?
2. You add a hook to `~/.claude/settings.json` and it doesn't fire in a project. What are the two most likely reasons?
3. Which of these belongs in project scope rather than user scope, and why: a personal code-review agent you use everywhere; a deploy command specific to this repo; your API keys?

---

## Part 03 wrap-up

| Topic | Done | Lab proof | Quiz |
|---|---|---|---|
| 3.1 Slash commands | ☐ | Committed custom command | ☐ /3 |
| 3.2 Model, effort, cost | ☐ | A/B cost table + policy | ☐ /3 |
| 3.3 Session commands | ☐ | `/context` comparison table | ☐ /3 |
| 3.4 Permission modes | ☐ | Settings rules + mode policy | ☐ /3 |
| 3.5 `.claude` directory | ☐ | Two-scope commands + map | ☐ /3 |

**Answers:** `13-answer-key.md` → Part 03.
**Next:** `04-claudemd.md` — give the project a permanent brain.
