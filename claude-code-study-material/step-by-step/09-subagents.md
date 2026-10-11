# Part 09 — Subagents: isolated specialists
**Video:** 8:20:17 – 9:51:44 (Module 9)

**In this part:** 9.1 What & why · 9.2 Building and invoking them

---

## 9.1 Subagents: what they are and why they exist

### What it is
- A **subagent** is a specialised worker with:
  - its **own context window** (the heavy reading happens there, not in your session),
  - its **own system prompt** (a focused role),
  - its **own tool permissions** (`tools` / `disallowedTools`),
  - its **own model and effort** (often cheaper),
  - and a **single return value**: a summary back to the main session.
- The main session acts as a **manager**: it delegates, then keeps the report — not the noise.
- The course's framing: it's the difference between you reading every file yourself and handing the job to the right specialist.

### Why it matters
- **Context hygiene (the big one).** "Read all 40 files and tell me how auth works" costs tens of thousands of tokens in your main session. Delegated, those tokens are spent in the subagent and you receive a paragraph.
- **Cost control.** Routine exploration on Haiku while the parent stays on Sonnet/Opus changes your bill materially.
- **Quality through focus.** "You are a security auditor; report findings only" outperforms a generalist asked to do six things.
- **Parallelism.** Independent subagents run at once, cutting wall-clock time.
- **Safety.** Restricting tools is a real boundary — the course's line: an intern who can read the code but cannot see your bank statements or run destructive commands.

### How to do it (step by step)
1. **Find a candidate job.** Look for work with the shape *reads a lot → returns a little*: exploring a codebase, summarising a folder, reviewing a diff, auditing for a pattern.
2. **Decide what comes back.** Write the one-sentence report you want: "a list of endpoints with their auth requirements", "the three riskiest findings".
3. **Pick the cheapest model that can do it** (Haiku for scanning, Sonnet for judgement) and the **minimum tool set** (read-only unless it must write).
4. Delegate it in the main session and **check `/context`** before and after — the delivered value is the delta.
5. If the summary is wrong or vague, tighten the subagent's system prompt (that's where the role lives) rather than re-asking in the parent.
6. Adopt the rule of thumb and keep a running list of your subagents with one line each on when to use them.

**The delegation rule of thumb**
> If it reads a lot to produce a little → subagent.
> If it needs the full mess of your session to decide → keep it in the parent.

**Lab 9.1 — Prove the context win**
- [ ] Ran a "read everything and summarise" task in your main session; recorded `/context` before/after and the token cost.
- [ ] Ran the same task delegated (or via an exploration agent); recorded the same numbers.
- [ ] Compared the quality of the two summaries — did the delegation lose anything important?
- [ ] Wrote your first two subagent candidates with model + tool restrictions.

**Proof:** a two-row comparison (main session vs delegated: tokens, cost, quality note) and your candidate list.

**Quiz 9.1**
1. What exactly comes back to the main session from a subagent?
2. Give three benefits besides saving tokens.
3. Which of these should be delegated, and why: (a) "decide whether we should migrate payment providers", (b) "find every place we call the payments API"?

---

## 9.2 Building and invoking subagents

### What it is
- **Anatomy of a subagent file** (Markdown with YAML frontmatter):
  ```markdown
  ---
  name: planner
  description: >
    Reads requirements from CLAUDE.md and produces an implementation plan in
    PLAN.md. Use at the START of any new project or feature, before any code is
    written. Never writes code — only plans.
  tools: Read, Glob, Grep, Write
  disallowedTools: Bash, Edit
  model: haiku
  effort: high
  color: cyan
  ---

  You are a senior software architect. Your only job is to read requirements and
  produce a crystal-clear implementation plan. You never write code.
  ## Your Process
  1. Read CLAUDE.md thoroughly …
  2. Analyse the scope …
  3. Write PLAN.md with this exact structure: …
  ```
- **Locations:** project `.claude/agents/*.md` (committed, shared) · user `~/.claude/agents/*.md` (personal, all projects) · inside plugins (Part 11).
- **Three ways to invoke:**
  | Method | Control | Notes |
  |---|---|---|
  | Natural language ("explore my codebase") | Low | Chosen by `description`; misfires when many agents sound alike |
  | Explicit mention (`@code-reviewer`) | High | Names the worker |
  | `/agents` manager | Highest | Library UI: view, create, edit, set model |

### Why it matters
- The `description` field is the **router** — vague descriptions mean the wrong agent runs, or none does. It must state the *use case and the timing* ("use at the START of any new feature").
- Restricted `tools`/`disallowedTools` are both a safety boundary and a focus device: a reviewer without `Edit` cannot "helpfully" rewrite your code.
- The `/agents` UI is the practical on-ramp: most people won't hand-write frontmatter, so let the tool scaffold it, then edit the prompt.

### How to do it (step by step)
1. **Create via the UI first.** Run `/agents`, choose to create a new agent, and fill in: name, description (purpose + when to use), tools, model.
2. Inspect the generated file in `.claude/agents/` and rewrite the **description** so it's unambiguously routable:
   - Weak: *"Reviews code."*
   - Strong: *"Reviews changed files for bugs, security issues and style violations. Use after implementing a feature, before opening a PR. Reports findings only; never edits."*
3. Restrict tools to the minimum. For read-only reviewers: `tools: Read, Grep, Glob` and `disallowedTools: Bash, Edit`.
4. Set `model` and `effort` per worker — Haiku for scanning, Sonnet for judgement, high effort only where it earns it.
5. **Write the system prompt as a role with a process**, then a strict output contract (e.g. "report findings as a numbered list with file:line and severity; no code changes").
6. **Test the routing three ways:** natural language, `@name`, and via `/agents`. Note which wording caused auto-delegation to fire and which didn't; adjust the description.
7. Build a small team for one real workflow (the course's example pipeline): **planner** (writes `PLAN.md`, never code) → **code-writer** → **test-writer** → **reviewer/quality** → **security-auditor**. Run the sequence once end to end.

### Starter set to copy
| Agent | Model | Tools | Output contract |
|---|---|---|---|
| `explorer` | haiku | Read, Grep, Glob | "Map of the relevant files + how X works, ≤300 words" |
| `planner` | sonnet/haiku | Read, Grep, Glob, Write | Writes `PLAN.md` with phases, files, signatures. Never code |
| `reviewer` | haiku | Read, Grep, Glob | Numbered findings with severity; no edits |
| `test-writer` | sonnet | Read, Write, Bash | Tests + a summary of what they cover |
| `security-auditor` | sonnet | Read, Grep, Glob | OWASP-style findings only |

**Lab 9.2 — Build three agents and prove routing**
- [ ] Created `explorer`, `reviewer` and one more via `/agents`, then hand-edited the descriptions.
- [ ] Confirmed tool restrictions are honoured (reviewer cannot edit — try asking it to).
- [ ] Triggered each agent by natural language and by `@name`; recorded which wording worked.
- [ ] Ran the explorer on a real question and confirmed `/context` grew far less than doing it inline.
- [ ] Committed `.claude/agents/` and wrote a one-line "when to use" for each.

**Proof:** three agent files, a routing table (phrase → which agent fired), and the context delta from the delegated task.

**Quiz 9.2**
1. Which frontmatter field decides automatic delegation, and what should it contain?
2. Why give a reviewer `disallowedTools: Edit, Bash`?
3. You have three agents and natural-language delegation keeps picking the wrong one. Give two fixes.

---

## Part 09 wrap-up

| Topic | Done | Lab proof | Quiz |
|---|---|---|---|
| 9.1 What & why | ☐ | Delegation comparison table | ☐ /3 |
| 9.2 Build & invoke | ☐ | Three agents + routing table | ☐ /3 |

**Answers:** `13-answer-key.md` → Part 09.
**Next:** `10-agent-teams.md` — several Claudes on one project.
