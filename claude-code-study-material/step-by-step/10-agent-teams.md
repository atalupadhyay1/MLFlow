# Part 10 — Agent teams
**Video:** 9:51:44 – 10:35:46 (Module 10)

**In this part:** 10.1 What & why (and how it differs from subagents) · 10.2 Running a team safely

> ⚠️ Agent teams were **experimental** at recording time. Expect rough edges, changing flags, and possible differences on your version. The *concepts* (parallel isolated sessions, worktree isolation, a lead who merges) are what matter here.

---

## 10.1 Agent teams: what they are and why they're different

### What it is
- An **agent team** = multiple Claude instances working on the **same project at the same time**:
  - one **team lead** (plans, spawns, coordinates, merges),
  - several **teammates** (e.g. backend, frontend, QA), each in its own session with its own context,
  - who **message each other** directly — e.g. the backend teammate publishes the API contract so frontend and QA can build against the same spec.
- **Isolation mechanism: git worktrees.** Each teammate works on its own branch/checkout of the repo, so parallel edits don't trample each other. Worktrees are a plain git feature, not an AI feature — the course explains them with a version-history analogy.
- Enabled with a settings flag:
  ```json
  // .claude/settings.json
  { "env": { "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1" } }
  ```
- Interaction: a display mode (in-process or split panes) and `Shift+Down` to switch between teammates ⚠️.

### Why it matters
- It's the difference between **delegation** and **collaboration**: subagents report to one parent; teammates negotiate with each other. Real work often has that shape (contract-first parallel development).
- It's the current frontier of agentic work — knowing the pattern puts you ahead of people still prompting one agent at a time.
- It's also the most expensive and most fragile mode. Understanding it prevents you from reaching for it when a single session (or two subagents) would do.

### How to do it (step by step)
1. Understand the topology before enabling anything:
   ```
   Subagents:   Parent ──▶ worker A        (report back)
                        └▶ worker B
   Agent team:  Lead ──▶ teammate 1 ◀──▶ teammate 2 ◀──▶ teammate 3
                       (own sessions, own worktrees, peer messaging)
   ```
2. Read the current official docs for team setup on your version (flag name, display modes, invocation) — this area changes. ⚠️
3. Write a **spec with an interface** before spawning: what is being built, which workstreams exist, and the exact contract they must agree on (API request/response schema, shared types).
4. Team sizing: **three** is the sweet spot in the course's demo (backend, frontend, QA). More adds coordination cost.
5. Before you start, confirm: repo is git-initialised, you're willing to review merges, and the task genuinely splits along the interfaces.

**When teams help / when they don't**
| Use teams | Don't |
|---|---|
| Multiple genuinely separable workstreams | One small change |
| A clean interface exists (API contract, schema) | Interfaces are still being discovered |
| You can supervise and review merges | You want unattended, unreviewed output |
| The build is long and parallelisable | Context/limit budget is tight |

**Lab 10.1 — Decide, then prepare**
- [ ] Found or invented a feature with three separable workstreams.
- [ ] Wrote the **interface contract** they must share (schemas, endpoints, types).
- [ ] Wrote the team brief: roles, deliverables, and the "agree on the contract first" rule.
- [ ] Justified in two lines why this beats a single session — or concluded it doesn't, and said why.

**Proof:** the spec + contract + team brief, and your one-paragraph judgement on whether a team is warranted.

**Quiz 10.1**
1. State the structural difference between subagents and agent teams.
2. What does git worktree contribute, and why is it necessary here?
3. Name one task shape where a team is clearly wrong, and why.

---

## 10.2 Running a team (and keeping it sane)

### What it is
- The workflow: **write the brief → enable the flag → ask for a team → watch → let them coordinate → review branches → merge yourself.**
- The course's demo brief instructs teammates to: build their component, **share the API contract before coding**, then merge and report.
- Observability is limited and evolving: display modes, queued-task views, `Shift+Down` to switch. Expect some UI jank and features that don't do anything yet. ⚠️

### Why it matters
- **Coordination failures are the dominant risk**, not model quality: two teammates inventing incompatible interfaces, merge conflicts, duplicated work.
- The token burn is real — several live contexts at once. A failed team run can cost the same as a long solo session.
- Reviewing worktrees and merging *yourself* is what converts "three agents did things" into "a working feature".

### How to do it (step by step)
1. **Repo hygiene first:** clean working tree, everything committed, you understand how worktrees map to branches (`git worktree list`).
2. Enable the flag in **project** settings (not global) so it doesn't surprise you in other repos.
3. Write the brief as a file (`prompt.txt` or inline) with: goal, the three workstreams, the **contract-first rule**, and the merge/report requirement.
4. Spawn the team and **watch for the coordination step**: did teammate 1 actually publish the contract before the others started? If not, stop and fix the brief.
5. Let them work. Periodically check each teammate's view (`Shift+Down`) and record token usage as you go.
6. When they finish: list the worktrees/branches, **review each diff**, then merge deliberately — resolving conflicts yourself rather than trusting a summary.
7. Run the project's tests on the merged result. This is the acceptance criterion, not the teammates' reports.
8. Retro: was coordination worth the cost? What would you change in the brief next time?

### Catches you should expect
| Symptom | What's happening | Move |
|---|---|---|
| Teammates build incompatible interfaces | Contract wasn't agreed first | Kill, rewrite the brief with the contract explicit |
| Nothing appears in the UI | Display mode / version quirk ⚠️ | Try another display mode or the CLI, don't fight it |
| Merge conflicts everywhere | Overlapping file ownership | Assign file/dir ownership per teammate in the brief |
| Token usage explodes | Several live contexts | Smaller scope, fewer teammates, cheaper models |
| Feature missing/absent in your version | Experimental flag/rollout | Check docs; skip the lab and keep the concepts |

**Lab 10.2 — Run one team on a toy feature**
- [ ] Clean repo with a written brief and explicit contract-first rule.
- [ ] Flag enabled in project settings only.
- [ ] Observed the contract-sharing step (or intervened when it was skipped).
- [ ] Reviewed each teammate's diff and merged manually.
- [ ] Ran the tests on the merged result and recorded token usage.
- [ ] Wrote a 3-line retro (worth it? what would you change?).

**Proof:** the merged, tested feature and your retro. If your version lacks teams, write the brief and the merge plan instead and note that in the retro.

**Quiz 10.2**
1. What is the single most important instruction in a team brief, and why?
2. Why should *you* do the merging rather than accepting a teammate's summary?
3. Halfway through, two teammates are editing the same file and creating conflicts. Give two interventions.

---

## Part 10 wrap-up

| Topic | Done | Lab proof | Quiz |
|---|---|---|---|
| 10.1 What & why | ☐ | Spec + contract + judgement | ☐ /3 |
| 10.2 Running a team | ☐ | Merged feature + retro | ☐ /3 |

**Answers:** `13-answer-key.md` → Part 10.
**Next:** `11-plugins.md` — package and share everything you've built.
