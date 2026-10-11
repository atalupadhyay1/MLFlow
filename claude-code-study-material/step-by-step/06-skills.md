# Part 06 — Skills: reusable playbooks
**Video:** 4:31:35 – 5:40:13 (Module 6)

**In this part:** 6.1 What & why · 6.2 Anatomy of a skill · 6.3 Creating skills (and Skills 2.0)

---

## 6.1 Skills: what they are and why they're the best value in the course

### What it is
- A **skill** is a folder containing:
  - `SKILL.md` — YAML frontmatter (`name`, `description`, optional `trigger`, `argument-hint`, `effort`) + Markdown instructions,
  - and optionally `scripts/`, `references/`, `assets/`, even a `requirements.txt`.
- Invoked **explicitly** (via its trigger, e.g. `/expense-summary`) or **automatically** when a task matches its `description`.
- **Progressive disclosure:** only the *name and description* sit in context until the skill is invoked — the body and scripts load on demand. That's why installing many skills doesn't blow up your baseline.

### Why it matters
- Skills turn "the thing I re-explain every week" into a **one-command procedure** that produces identical results.
- They solve the thing chat users hate: retraining a conversation from scratch each time you start a new chat. Skills are the *portable* version of that training.
- They're the cheapest of the big three extensions to adopt: a hook needs a script, an MCP server needs infrastructure, a skill needs a Markdown file.
- The course's analogy: skills are learned routines — once you can drive, you can drive any car; and just as driving doesn't let you fly a plane, a skill applies to its own scope.

### How to do it (step by step)
1. **Find candidates.** List tasks you repeat with the same shape: release notes, weekly reports, data-file summaries, PR descriptions, code review of a diff, "summarise this CSV".
2. **Pick the one with the most steps** — the more procedure, the more a skill saves.
3. Decide **scope**: project (`./.claude/skills/…`, shared with the team) or personal (`~/.claude/skills/…`, everywhere).
4. Write down the procedure *in the order you actually perform it*, including the parts you always forget.
5. Ship it as a skill (6.2 for anatomy), run it, and refine it the first time it's not perfect. Note that the body only loads when invoked — so it can be as detailed as it needs to be.

**Skill vs the neighbours (so you pick the right tool)**
| | Slash command | **Skill** | Hook | Subagent |
|---|---|---|---|---|
| Is | saved prompt | procedure (+scripts/assets) | event-driven script | isolated worker |
| Context cost | loads when invoked | description only, body on demand | **zero** | summary back to you |
| Can run code | no | **yes** (bundled scripts) | yes | yes |
| Auto-invoked | no | **yes, via description** | yes, on events | yes, by description |

**Lab 6.1 — Pick your first skill**
- [ ] Listed five repeated tasks from your own work.
- [ ] Chose one and wrote its steps in the real order (including gotchas).
- [ ] Decided scope (project vs personal) and justified it.
- [ ] Named the skill (verb-ish, obvious: `release-notes`, `weekly-report`, `csv-summary`).

**Proof:** a named skill + a written procedure you could hand to a new teammate.

**Quiz 6.1**
1. Why doesn't installing thirty skills bloat your context?
2. What triggers automatic invocation of a skill?
3. Which fits each case — a saved prompt, a skill, or a hook: (a) reformat every file Claude writes; (b) the PR description you always write; (c) a five-step data analysis pipeline with bundled scripts?

---

## 6.2 Anatomy of a skill

### What it is
- The **frontmatter** is the interface: `name` (invocation), `description` (when to auto-invoke — this is the most important line you'll write), optional `trigger`, `argument-hint`, `effort`.
- The **body** is the procedure: goal, inputs, numbered steps, rules, output format, references.
- **Bundled files** are the power feature: scripts (deterministic work that should run identically every time) and references (long knowledge that shouldn't sit in the body).

### Why it matters
- The `description` is effectively **prompt engineering for the router**: a vague description means the skill never fires automatically, or fires on the wrong tasks.
- Moving deterministic steps into **scripts** cuts cost and variance: no tokens spent regenerating the same code, no "it did it slightly differently this time".
- A literal **output format** (with a sample) is how you get consistent artefacts instead of a slightly different report every run.

### How to do it (step by step)
1. Create the folder: `.claude/skills/<skill-name>/`.
2. Write `SKILL.md` with frontmatter — and make the description say **what it does *and* when to use it**:
   ```markdown
   ---
   name: generate-report
   description: >
     Generates a daily project status report by reading all Python files in /src,
     summarising each module, collecting TODOs, and writing a markdown report to
     /reports/. Use when asked to generate a report, summarise the codebase, or
     create a status update.
   trigger: /generate-report
   argument-hint: "path/to/source (default /src)"
   effort: low
   ---
   ```
3. Write the body as a procedure: **Goal → Inputs → Steps (numbered) → Rules → Output format**.
4. If a step is deterministic, write it as a script in `scripts/` and reference it (e.g. `python scripts/01_eda.py --input titanic.csv`).
5. If you need exact output, include a **sample of the output** in the body (the course's `expense-summary` skill does exactly this, down to the ASCII layout and rounding rules).
6. Add `requirements.txt` / config templates when the script needs them, so runs are reproducible.
7. Invoke it by trigger, then in natural language, and fix the description if auto-invocation doesn't fire.

### Two shapes worth copying

**Shape A — deterministic formatter (no scripts, exact layout)**
```markdown
---
name: expense-summary
description: Shows a summary of all groups and expenses. Use for a quick overview of active groups, total spending and per-member contributions.
trigger: /expense-summary
effort: low
---
Read backend/data/groups.json and backend/data/expenses.json directly with the Read tool. Do not make HTTP calls.
Print a summary in EXACTLY this format: <layout…>
## Calculation rules
- amounts are stored in paise; divide by 100 for display
- percentages round to 1 dp; if total is 0 show 0.0%
- sort members by amount paid, highest first
- if groups.json is empty print: "No groups found."
```

**Shape B — scripted pipeline (partial determinism)**
```markdown
### Phase 1: Exploratory Data Analysis
**Script**: [01_eda.py](./scripts/01_eda.py)
```bash
python scripts/01_eda.py --input data.csv --output reports/eda.html
```
Run this first to get: shape, dtypes, missing values, distributions, correlations.
```

**Lab 6.2 — Ship a skill with a script**
- [ ] Created `.claude/skills/<name>/SKILL.md` with a description that names both purpose and trigger conditions.
- [ ] Body follows Goal → Inputs → Steps → Rules → Output format.
- [ ] Moved at least one deterministic step into `scripts/`.
- [ ] Included a literal output example.
- [ ] Ran it twice — by trigger and by natural language — and got the same artefact.

**Proof:** the skill folder (SKILL.md + script), two successful runs, and one refinement you made after the first run.

**Quiz 6.2**
1. Which frontmatter field decides auto-invocation, and what must it contain to work well?
2. Why put a step in a bundled script rather than describing it in the body?
3. Your skill runs, but the output format varies each time (different headings, sometimes a table, sometimes bullets). What's missing from the skill?

---

## 6.3 Creating skills fast (Skills 2.0 / skill creator)

### What it is
- A **skill that writes skills**: the course uses a "skill creator" skill where you describe what you want; it asks clarifying questions (scope, language, components), then generates `SKILL.md`, scripts, references, assets, and requirements.
- **Skills 2.0** refinements: pass **arguments** (dataset name, output dir), set **model/effort** per skill, and iterate on generated skills like normal code.
- The same skill concept works across Claude surfaces (Claude AI, co-work, Claude Code), so what you build is portable.

### Why it matters
- The blank page is the real barrier to writing skills; a generator removes it. You review and refine instead of authoring from scratch.
- Generated skills teach anatomy by example — you see good structure, then internalise it.
- It's how you scale: once you can produce a skill in ten minutes, you stop tolerating repeated work in any project.

### How to do it (step by step)
1. Install or open a skill-creator skill (official "skill creator" or equivalent).
2. Ask it for a skill you'll genuinely use, and describe the outcome rather than the implementation:
   > *"Create a skill that analyses a CSV in depth for Kaggle-style work. It should have scripts and subfolders, so it runs on the data and produces a thorough analysis."*
3. Answer its questions with real decisions: **scope** (project vs personal), **language** (Python etc.), **components** (which analyses matter).
4. Review the generated tree: `SKILL.md`, `scripts/`, `references/`, `assets/`, `requirements.txt`.
5. **Make it yours:** add an argument (`argument-hint: path/to/data.csv`), set `effort`, and tighten the description.
6. Run it end to end on a real dataset; fix what breaks; commit.
7. Record the time it took vs writing it by hand — that ratio is the reason to keep a skill-creator handy.

**Argument pattern to copy**
```markdown
---
name: generate-report-arg
description: Generates a report for a given source directory. Use when asked to report on a folder.
argument-hint: "src/ output/dir"
---
Read `$1` and write the report to `$2`.
```

**Lab 6.3 — Generate, refine, ship**
- [ ] Had a skill-creator produce a skill from a one-paragraph request.
- [ ] Reviewed the generated structure and understood each folder's role.
- [ ] Added at least one argument and set `effort`.
- [ ] Ran it on real data and fixed one issue.
- [ ] Committed it (or moved it to `~/.claude/skills/`).

**Proof:** the generated-then-refined skill tree, plus a note of what the generator got wrong that you fixed.

**Quiz 6.3**
1. What does a skill creator do, and what should you still review manually?
2. How do you make a skill accept an input like a file path or output directory?
3. You generate a skill and it "works" but ignores your project's conventions. Name two specific edits.

---

## Part 06 wrap-up

| Topic | Done | Lab proof | Quiz |
|---|---|---|---|
| 6.1 What & why | ☐ | Named skill + procedure | ☐ /3 |
| 6.2 Anatomy | ☐ | Skill with script + 2 runs | ☐ /3 |
| 6.3 Creating skills | ☐ | Generated + refined skill | ☐ /3 |

**Answers:** `13-answer-key.md` → Part 06.
**Next:** `07-hooks.md` — automation that costs zero tokens.
