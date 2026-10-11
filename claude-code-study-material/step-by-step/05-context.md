# Part 05 — Context management
**Video:** 3:43:48 – 4:31:35 (Module 5)

**In this part:** 5.1 The context window · 5.2 Context rot · 5.3 Budgeting & the recovery playbook

> This is the part most tutorials skip and the one that decides your bill, your speed, and whether Claude feels smart or stupid. It is also the part that makes `/compact` and `/clear` feel like tools rather than buttons.

---

## 5.1 The context window and why statelessness matters

### What it is
- The **context window** is the fixed budget of tokens a request can carry. **LLMs are stateless** — they remember nothing between calls. Continuity exists only because Claude Code **re-sends everything, every turn**:
  - the **system prompt** (product rules),
  - **tool definitions**,
  - **MCP server tool descriptions**,
  - **skill descriptions**,
  - **CLAUDE.md / memory**,
  - the **entire message history**,
  - and a reserved **auto-compact buffer**.
- `/context` visualises exactly this split — you'll see files being read, tokens accumulating, and free space shrinking.
- In the course's demo, a fresh session already carried several thousand tokens **before any typing**; even a trivial "hi" in a real project sat at ~29.5K/200K with the system prompt alone at ~6.2K. ⚠️

### Why it matters
- **Cost is per call, and history is part of every call.** A 200K-token context charges you again for those 200K tokens on your next message — the course's example: five more messages ≈ $3 on Sonnet ⚠️.
- **Limits are context-driven**: subscriptions run out faster when every message carries a huge history.
- It explains why "just keep chatting" is the wrong instinct for long projects, and why the session commands in 3.3 exist.

### How to do it (step by step)
1. Open a fresh session in a real project and run `/context` **before typing anything**. Note the fixed overhead (system prompt, tools, MCP, skills, CLAUDE.md).
2. Type a one-word message (`hi`) and run `/context` again. Note that the baseline was never "zero" — it's the floor you pay on every message.
3. Ask it to read a large file, then `/context` again; watch the messages/tools portion jump.
4. Note which parts are **your** choices (CLAUDE.md size, MCP servers, skills) and which are not (system prompt, core tools). Put the controllable ones in a list — that list is your budget.
5. Sanity-check the cost model with `/cost` after a few exchanges: the same context is billed repeatedly.

**The statelessness sentence to remember**
> Nothing is remembered between calls; everything is re-sent. Managing context *is* managing cost and quality.

**Lab 5.1 — Make the invisible visible**
- [ ] Captured `/context` at three moments: fresh session, after `hi`, after a file read.
- [ ] Listed the controllable vs non-controllable components from the breakdown.
- [ ] Recorded the "floor" (fixed overhead) for your project and the top two contributors.
- [ ] Compared `/cost` across those three points.

**Proof:** a three-row table (moment → tokens used → main contributor) plus your controllable/non-controllable list.

**Quiz 5.1**
1. Why does a session already use thousands of tokens before you type anything?
2. Which of these can you shrink: system prompt, tool definitions, MCP descriptions, CLAUDE.md, message history? (Pick all you control.)
3. A teammate says "context is free until you hit the limit". Correct them in two sentences using the cost model.

---

## 5.2 Context rot: the failure everyone misdiagnoses

### What it is
- **Context rot** = quality decay in a long session: instructions from early on get ignored, the same work gets redone, mistakes appear that wouldn't have happened 20 messages ago.
- Causes: sheer volume, plus **primacy/recency bias** — models attend most to the beginning and end of a long context and "fuzzy" in the middle. The course's visual: top and bottom remembered, middle blurred.
- Symptoms to watch for: CLAUDE.md rules silently violated; repeated questions; Claude re-asking for info it already has; drift in conventions; rising cost per message.

### Why it matters
- The near-universal mistake is blaming the model. **The model didn't change; the context did.** Fixing the resource fixes the behaviour.
- Recognising rot early saves hours: you compact or clear *before* twenty messages of drift, instead of after.
- It reframes "the AI is dumb today" into a checklist you can actually run.

### How to do it (step by step)
1. **Reproduce it on purpose.** In a scratch project: ask for a rule early ("use snake_case everywhere"), then do 15–20 messages of unrelated work (paste a document, ask several side questions, read files).
2. Now ask for a small function. Check whether the early rule survives. Note the drift.
3. Run `/context` — record the percentage used.
4. **Run the symptom checklist** at that moment:
   - Are instructions from the start still respected?
   - Am I repeating explanations?
   - Is cost per message climbing?
   - Has the model started asking for facts it was given?
5. Recover using 5.3, then repeat step 2 and observe the behaviour return.
6. Write your own **rot tripwire**: the specific signal (e.g. "Claude asks for something I already pasted") that makes you immediately run `/context`.

### The rot triage flow
```
Something feels wrong
   ↓
/context      → is the window crowded?
   ↓ yes
/compact with instructions  → can you continue cheaply?
   ↓ still off / task changed
/clear (+ status file handover)  → start clean
```

**Lab 5.2 — Trigger rot deliberately**
- [ ] Caused a rule to be forgotten by filling context.
- [ ] Recorded the `/context` number at the moment of failure.
- [ ] Completed the four-question symptom checklist with answers.
- [ ] Defined your personal tripwire signal.

**Proof:** the before/after evidence of the forgotten rule, the context number, and your tripwire.

**Quiz 5.2**
1. What is context rot, in one sentence?
2. Name the two attention-related causes the course highlights.
3. Your session is long and Claude starts ignoring CLAUDE.md. Name the wrong diagnosis and the right one.

---

## 5.3 Token budgeting and the recovery playbook

### What it is
- **Budgeting:** deliberately spending context where it earns its keep — and refusing to spend it elsewhere.
- Levers you control:
  | Lever | Cheap setting | Expensive setting |
  |---|---|---|
  | CLAUDE.md | One screen | 400-line essay |
  | MCP servers | Only what you use | Everything you've ever installed |
  | Skills | Descriptions only until invoked | (no baseline cost) |
  | Model & effort | Haiku/low for chores | Opus/max for everything |
  | Prompts | Specific scope, few files | "look at everything" |
  | Session | `/clear` between tasks | One 12-hour mega-session |
  | Images/files | Compressed, cropped | Full-page screenshots |
- Levers you don't control: the platform system prompt and core tool definitions.
- **The recovery playbook** for a bloated session:
  1. `/context` — diagnose.
  2. `/compact` **with explicit instructions** — continue with the same task.
  3. `/clear` + a **status file handover** — when the task changed or quality is still off.
  4. **Delegate** heavy reading to subagents (Part 9) instead of loading it yourself.

### Why it matters
- Budgeting is the difference between a $3 conversation and a $30 one, and between a subscription that lasts the month and one that dies mid-week.
- The recovery playbook turns "my session is ruined" into a two-minute routine with no lost work: the old session stays on disk, and a status file makes the new one smart fast.
- Delegation is the structural fix — you stop paying for bulk reading in your main context at all.

### How to do it (step by step)
1. **Audit your baseline.** In a real project: `/context`. List the top three contributors. Fix or remove the biggest controllable one (usually an unused MCP server or a fat CLAUDE.md).
2. **Practise the handover.** Write a `STATUS.md` in your repo:
   ```markdown
   ## Where we are
   - Feature X implemented; tests green.
   ## Key decisions
   - Uses Redis for caching; JSON storage for tasks.
   ## Open items
   - CORS issue on /standup; needs AI fallback when quota is hit.
   ## How to verify
   - `npm test`, `pytest -q`
   ```
3. `/clear`, then start the new session with: *"Read STATUS.md, then continue with the open items."* Note how little context that costs versus resuming a monster session.
4. **Practise compact-with-intent** on a long session: `/compact keep the file structure, API surface, patterns and open TODOs`. Then `/context` to confirm the shrink.
5. **Practise delegation:** instead of asking your main session to read 30 files, ask a subagent (or an exploration agent) to summarise them — the reading happens elsewhere.
6. **Write your budget policy** — a short list of rules you'll actually follow, e.g.:
   - Clear between unrelated tasks.
   - One status file per project phase.
   - No new MCP server without deleting one.
   - Compress screenshots before pasting.
   - Big reads → subagents.

**Lab 5.3 — Budget and recover**
- [ ] Audited your baseline and fixed the largest controllable contributor.
- [ ] Wrote a real `STATUS.md` for a project you're working on.
- [ ] Did a clear-and-handover; confirmed the new session picked up cheaply.
- [ ] Ran a compact-with-instructions and recorded the context delta.
- [ ] Wrote your budget policy (5 lines max).

**Proof:** baseline before/after numbers, the committed `STATUS.md`, and your policy.

**Quiz 5.3**
1. Name three context costs you control and one you don't.
2. When is a status file + `/clear` better than `/compact`?
3. Your main session has 40K tokens of file reads from exploring a codebase, and you still need to implement a fix. What's the structural change that prevents this next time?

---

## Part 05 wrap-up

| Topic | Done | Lab proof | Quiz |
|---|---|---|---|
| 5.1 Context window | ☐ | Three-moment context table | ☐ /3 |
| 5.2 Context rot | ☐ | Drift reproduction + tripwire | ☐ /3 |
| 5.3 Budget & recovery | ☐ | `STATUS.md` + policy | ☐ /3 |

**Answers:** `13-answer-key.md` → Part 05.
**Next:** `06-skills.md` — turn repeated workflows into reusable playbooks.
