# Part 04 — CLAUDE.md: the project's permanent brain
**Video:** 2:58:27 – 3:43:48 (Module 4)

**In this part:** 4.1 What & why · 4.2 Hierarchy & loading · 4.3 Writing and maintaining it

---

## 4.1 CLAUDE.md: what it is and why it changes everything

### What it is
- A **Markdown file of standing instructions** that Claude Code loads automatically at the start of every session in that project.
- It holds what a new teammate would need on day one: what the project is, the stack, the exact commands, the conventions, the non-negotiables, and how to verify work.
- It has siblings: a user-level version (`~/.claude/CLAUDE.md`) for your personal defaults, and a private `CLAUDE.local.md` per project.

### Why it matters
- Without it, **every session starts from zero**: wrong test runner, wrong naming, "we don't use that library", the same correction five times a week.
- It converts your corrections from *repeated prompts* into *permanent context* — the single highest-leverage file in the whole course.
- It's also a **context cost** (Part 5): a bloated CLAUDE.md is paid on every request, so quality and economy point the same way: keep it tight.

### How to do it (step by step)
1. Run the "second time" test on your last week of work: which mistakes happened twice? Which convention did you re-explain? Each is a line that belongs in CLAUDE.md.
2. Open your project and run `/init` to let Claude draft a CLAUDE.md from the repo.
3. Read the draft critically: delete anything that is obvious, stale, or task-specific.
4. Add the four things Claude cannot infer reliably: **essential commands**, **verification steps**, **hard rules**, and **what the project is for**.
5. Commit it. From now on, every repeated correction gets *added here* instead of being retyped.

**The "add it to CLAUDE.md" reflex**
> Correction happens once → it goes in the file → it never happens again.

**Lab 4.1 — The second-time test**
- [ ] Listed three mistakes/corrections that repeated in your last week of work.
- [ ] Ran `/init` and kept a copy of the generated draft for comparison.
- [ ] Wrote the four non-inferable sections (commands, verification, hard rules, purpose) yourself.
- [ ] Committed CLAUDE.md.

**Proof:** your committed CLAUDE.md plus the list of three repeated problems it now prevents.

**Quiz 4.1**
1. What is CLAUDE.md for, in one sentence a teammate would understand?
2. Why is a *bloated* CLAUDE.md harmful even if every line is true?
3. Name three things that happened twice in your work this week that belong in the file (use your own examples).

---

## 4.2 Where it lives, how it loads, and who wins

### What it is
- **Priority hierarchy, weakest → strongest:**
  1. **Enterprise / managed policy** — org rules you can't override.
  2. **User** — `~/.claude/CLAUDE.md` — your defaults everywhere.
  3. **Project** — `./CLAUDE.md` or `./.claude/CLAUDE.md` — committed, shared.
  4. **`CLAUDE.local.md`** — private project overrides, strongest, not committed.
- **Loading:** Claude Code **walks up the directory tree** from your working directory, loading `CLAUDE.md` / `CLAUDE.local.md` from each level it passes. Running in `repo/backend/` loads `repo/backend/`, then `repo/`, then beyond.
- **Imports:** CLAUDE.md can pull in other files (e.g. `@docs/architecture.md`) so the always-loaded core stays small.
- **Two mechanical facts worth knowing:** HTML comments in these files are stripped before injection, and very large memory files get truncated (the course cites the first ~200 lines of bigger memory files loading ⚠️) — another argument for brevity.
- **Conflicts:** instructions closest to the project win. When two strong instructions genuinely clash, Claude will usually **ask** rather than guess.

### Why it matters
- It makes behaviour *predictable*: you can reason about which rule applies in which folder.
- It's the mechanism for team standards (project scope, committed) vs personal taste (user scope) vs secrets/local-only notes (`CLAUDE.local.md`).
- The "closest wins" rule means you never need to fight a global preference — you override it locally.

### How to do it (step by step)
1. **See the precedence live.** In `~/.claude/CLAUDE.md` add a preference: `Always give code examples in Python.`
2. In a scratch project, create `CLAUDE.md` with: `This project is C++. Give code examples in C++.` Ask for "a function that sorts a list". Observe which wins and note that Claude may flag the conflict.
3. Now add a **private** override: `CLAUDE.local.md` with `For this repo, everything in Java.` Ask again. Confirm the local file outranks the project file.
4. **Test the walk-up.** Create `repo/CLAUDE.md` and `repo/sub/CLAUDE.md` with different rules; start Claude Code in `repo/sub/` and confirm both are seen and the nearer one wins for conflicts.
5. **Test imports.** Move a long section of your project CLAUDE.md into `docs/architecture.md` and reference it with `@docs/architecture.md`. Confirm Claude still knows the content.
6. **Test the comment trick.** Add an HTML comment with a human-only note (`<!-- staging creds live in 1Password -->`) and confirm it doesn't appear in Claude's context while remaining visible to humans in the file.
7. Clean up your experiment files and write your team's scope policy: what goes global, project, local.

### Precedence cheat-line
> Enterprise < User < Project < `CLAUDE.local.md` — *closest to the work wins; conflicts get asked about, not silently guessed.*

**Lab 4.2 — Precedence lab**
- [ ] Reproduced a user-vs-project conflict and observed the project win (and any clarifying question).
- [ ] Added `CLAUDE.local.md` and confirmed it outranks the project file.
- [ ] Verified the walk-up behaviour with a nested folder.
- [ ] Converted a section to an import with `@…`.
- [ ] Wrote your scope policy (global / project / local).

**Proof:** a filled-in precedence table with what you actually observed, plus your scope policy.

**Quiz 4.2**
1. Order the four scopes by priority, strongest first.
2. From which directories does Claude Code load instruction files when started in `repo/backend/`?
3. You have a global rule "never use tabs", a project rule "this repo uses tabs", and a local file saying nothing. Which applies, and what will Claude likely do if the clash is real?

---

## 4.3 Writing a CLAUDE.md that earns its tokens (and keeping it alive)

### What it is
- A **short, structured, high-signal document**. The course's structure: overview → commands → conventions → structure → rules → verification.
- A living file: every repeated correction is a line to add; every stale line is a line to delete.

### Why it matters
- Anthropic's own guidance (quoted in the course) is to include **bash commands, code style and workflow rules** — precisely the things that make the agent *verify* instead of guess.
- Verification lines change behaviour measurably: "run pytest after changes" is the difference between a fix and a guess.
- Stale instructions are worse than missing ones: they make Claude confidently wrong.

### How to do it (step by step)
1. Copy this skeleton and fill it in — nothing more unless you can justify it:
   ```markdown
   # <Project name>
   One paragraph: what this is, for whom, and the goal.

   ## Tech stack
   - Backend: <framework, port, storage, env vars>
   - Frontend: <framework, port, data fetching, state rules>

   ## Essential commands
   - install:   <cmd>
   - dev:       <cmd>
   - test:      <cmd>
   - lint/type: <cmd>

   ## Code standards
   - <naming, typing, formatting, error handling, component rules>

   ## Project structure
   - <path> — <responsibility>   (only what matters)

   ## Hard rules
   - Never commit directly to main. Never hardcode credentials.
   - No silent failures — handle errors explicitly. Ask instead of assuming.

   ## Verification (run after changes)
   - Code: run typecheck + tests.
   - UI: screenshot and compare against the requirement.
   - Data: verify with a test query.
   ```
2. **Fill the commands by stealing them from reality**: open `package.json` / `Makefile` / CI config and copy the exact invocations. Wrong commands are worse than none.
3. **Write verification as commands, not vibes.** "Tests pass" is a vibe; `npm test` is a command.
4. **Trim to fit one screen.** Anything longer than ~1 page should probably be an imported file or a skill.
5. **Set the maintenance rhythm:** whenever you correct Claude, ask "is this a one-off or a rule?" One-off → not in the file. Rule → add it, keep it short, commit.
6. **Delete ruthlessly at the end of each project phase:** remove instructions about code you no longer have.

### The belong / don't belong table

| Belongs | Doesn't belong |
|---|---|
| Project overview and goal | Full API documentation |
| Exact build/test/lint commands | Code snippets that will drift |
| Conventions and naming | Task-specific instructions ("add the button on line 42") |
| Key file map | Anything stale |
| Hard rules / guardrails | Secrets, keys, credentials |
| Verification checklist | A diary of past decisions (use docs/ for that) |

**Lab 4.3 — Ship a one-screen CLAUDE.md**
- [ ] Wrote the six sections with real, copied command strings.
- [ ] Added at least three verification steps phrased as commands.
- [ ] Made Claude run your verification steps: ask it to "make a small change, then run the verification steps" and confirm it uses *your* commands.
- [ ] Trimmed the file to fit one screen and committed it.
- [ ] Added a maintenance note to your own workflow (when corrections become rules).

**Proof:** the one-screen committed file, plus a transcript line showing Claude running your verification command unprompted.

**Quiz 4.3**
1. Which one belongs in CLAUDE.md: the full Stripe API reference, or "run `npm run typecheck` before finishing"? Why?
2. Why should verification steps be written as commands rather than outcomes?
3. Your CLAUDE.md is 400 lines and sessions feel slow. Name two moves that keep the knowledge but shrink the always-loaded file.

---

## Part 04 wrap-up

| Topic | Done | Lab proof | Quiz |
|---|---|---|---|
| 4.1 What & why | ☐ | Committed file + repeated-problem list | ☐ /3 |
| 4.2 Hierarchy & loading | ☐ | Precedence table + scope policy | ☐ /3 |
| 4.3 Writing it | ☐ | One-screen file + verification run | ☐ /3 |

**Answers:** `13-answer-key.md` → Part 04.
**Next:** `05-context.md` — the resource that decides your bill and your quality.
