# Quiz — Claude Code Full Course

30 questions: 20 multiple-choice, 10 short-answer. Answers and explanations at the end. Take it cold first; anything below 24/30 means re-read those study-guide sections.

---

## Part A — Multiple choice (1 point each)

**1. In the course's core analogy, what does the terminal represent for Claude Code?**
a) A cheaper interface b) The "hands" that let the brain act on your machine c) A backup for the web app d) A permission-mode setting

**2. Which task best fits the course's model-selection rule?**
a) Opus for renaming a variable b) Haiku for architecture planning c) Opus for planning, Sonnet for building, Haiku for maintenance d) Always Opus — quality first

**3. Claude on the web or desktop cannot do which of these?**
a) Explain code you paste b) Read a screenshot you share c) Edit files directly in your project folder d) Answer follow-up questions

**4. The agentic loop is best described as…**
a) A prompt template b) plan → act → observe → check → retry/answer c) A model training process d) A caching layer

**5. Which is the strongest scope in the CLAUDE.md hierarchy?**
a) User `~/.claude/CLAUDE.md` b) Enterprise policy c) `CLAUDE.local.md` d) Project `.claude/CLAUDE.md`

**6. Which item does NOT belong in a CLAUDE.md?**
a) Essential build/test commands b) Naming conventions c) The entire third-party API reference d) Verification checklist

**7. Why is the same conversation history billed again on every message?**
a) Caching is disabled b) LLMs are stateless, so history is re-sent each call c) It's a bug in Claude Code d) Only if you use /compact

**8. Which command starts a brand-new session with empty context while leaving the old session on disk?**
a) `/compact` b) `/rewind` c) `/clear` d) `/branch`

**9. Which command is read-only and presents a plan before editing?**
a) Auto mode b) Plan mode c) Accept-edits mode d) Bypass permissions

**10. Which statement about skills is TRUE?**
a) All installed skills load fully into context at session start b) Only name and description sit in context until the skill is used c) Skills cannot contain scripts d) Skills only exist in Claude Code

**11. A skill should contain a bundled script when…**
a) The instructions are vague b) The steps are deterministic and repeatable c) You want auto-invocation d) You need arguments

**12. What does hook exit code 2 do?**
a) Retries the tool b) Blocks the action and returns stderr to Claude as the reason c) Logs a warning only d) Disables the hook

**13. Why are hooks described as "zero tokens"?**
a) They use a smaller model b) They run outside the model on lifecycle events c) They cache the response d) They only run at session end

**14. The most reliable hook configuration practice the course recommends is…**
a) Hand-edit settings.json while Claude runs b) Let Claude add the first hook, then inspect c) Only use bash hooks d) Never use timeouts

**15. MCP is best summarised as…**
a) A model tier b) An open standard for connecting AI agents to external tools and data c) Anthropic's plugin marketplace d) A prompt technique

**16. Which is the biggest hidden cost of enabling many MCP servers?**
a) Disk space b) Their tool descriptions consume context on every request c) Slower installation d) More permissions prompts

**17. What distinguishes an agent team from subagents?**
a) Teams use cheaper models b) Teammates coordinate with each other in separate sessions, often via git worktrees c) Subagents cannot run in parallel d) Teams don't use tools

**18. A plugin can bundle all of the following EXCEPT…**
a) Agents and skills b) Hooks and MCP servers c) Settings and CLAUDE.md d) Your personal API subscription credentials, safely shared

**19. Which scheduling option keeps working when your laptop is closed?**
a) `/loop` b) Desktop scheduled task c) Claude routine d) Foreground session

**20. Which is a safe automation, per the course's rules?**
a) "Every night, fix failing tests and push to main" b) "On PR open, post a review comment and flag auth/payment changes" c) "Deploy when tests pass" d) "Clean up the repo, delete what isn't needed"

---

## Part B — Short answer (2 points each)

**21.** Explain, in two sentences, why Claude Code asks for permissions at all.

**22.** Your session has become slow, expensive, and forgetful after four hours of work, but you still need to continue the same task. Give the two-step recovery and what to include in it.

**23.** Name three context costs you directly control and one you can't.

**24.** What is the difference between a connector and an MCP server?

**25.** Give two reasons a subagent is preferable to having the main session read 40 files.

**26.** Why does the course insist that your *application's* AI features need an API key rather than your Claude subscription?

**27.** List the five safety rules for unattended scheduled agents.

**28.** You need a workflow that formats every Python file Claude writes, logs every session, and blocks `rm -rf`. Which mechanism do you use for each of the three, and why not prompts?

**29.** What does `/context` tell you that `/cost` doesn't, and vice versa?

**30.** Why does the course recommend writing CLAUDE.md and hooks *before* generating application code?

---

## Answer key

### Part A

1. **b** — Claude Code is the brain with hands; the terminal is the mechanism for acting on your machine.
2. **c** — Plan strong, build balanced, maintain cheap. Always-Opus burns cost and limits.
3. **c** — Chat products can't touch your files; they can only advise. (Claude Code is what edits files.)
4. **b** — Plan, act, observe, check, retry or answer. The "magic" is fast iteration.
5. **c** — `CLAUDE.local.md` sits closest to the project and outranks user, project, and enterprise scopes.
6. **c** — Full API docs bloat every request and go stale; point to them instead.
7. **b** — Models are stateless; each call re-sends the full history plus system prompt, tools, MCP, skills, and CLAUDE.md.
8. **c** — `/clear`. `/compact` keeps the same session by summarising; `/branch` forks a copy.
9. **b** — Plan mode is read-only and plan-first.
10. **b** — Progressive disclosure: only name/description are in context at rest.
11. **b** — Deterministic steps belong in scripts: identical every run, no generation cost.
12. **b** — Exit 2 blocks and routes stderr to Claude; exit 0 allows; other codes are non-blocking errors.
13. **b** — Hooks fire on lifecycle events outside the model.
14. **b** — Let Claude write the first hook so settings merge correctly, then inspect/test it.
15. **b** — An open standard (the "toolbox you don't maintain").
16. **b** — Tool definitions occupy context on every request; overlapping tools also confuse selection.
17. **b** — Peers in separate sessions coordinating (git worktrees for isolation) vs workers reporting to one parent.
18. **d** — Never bundle or share credentials; plugins are shared code, not secrets.
19. **c** — Claude routines run on Anthropic's cloud infrastructure.
20. **b** — Read-and-report with human review; the others include irreversible or unsupervised actions.

### Part B — model answers

**21.** Claude Code can write, edit, delete, and execute — actions with real consequences on your machine. Permission modes exist so you decide how much autonomy to grant, and hooks/rules add a second layer of defence. *(Key idea: power requires consent; the mode is the dial.)*

**22.** `/context` to see what's filling the window, then `/compact` with explicit instructions — naming the file structure, endpoints, component layout, and patterns to preserve. If quality is still poor, `/clear` and resume with a short status/CHANGELOG file describing where you are. *(If the task changed, `/clear` should be the first move, not the second.)*

**23.** **Control:** CLAUDE.md size, number of MCP servers enabled, session length/hygiene, prompt specificity, model/effort, skills installed, whether you paste images or big files. **Can't control:** the platform system prompt and core tool definitions.

**24.** A connector is a ready-made vendor integration surfaced inside Claude's products; an MCP server is any implementation of the open protocol — local or hosted — that you configure yourself. Connectors are convenience; MCP is extensibility and the shared standard.

**25.** The reading happens in the subagent's own context, so your main session stays lean (and cheaper — it receives only a summary); and the subagent can run a restricted tool set on a cheaper model, in parallel with other work. *(Also acceptable: focus — a specialist prompt beats a generalist.)*

**26.** A subscription authenticates *you* to Claude Code; an application needs its own programmatic credential (an API key) to call a model at runtime, and that usage is billed/limited separately. This is also why apps must degrade gracefully when the provider is unavailable.

**27.** (1) Start read-only; (2) write outputs to non-destructive paths; (3) put human review gates in front of irreversible actions; (4) log everything; (5) test the automation for days before trusting it.

**28.** All three are **hooks**: a `PostToolUse` hook matching `Write|Edit` for formatting, `SessionStart`/`Stop` hooks (or a shared logger) for logging, and a `PreToolUse` hook on `Bash` that exits 2 for dangerous commands. Prompts are unreliable here: they cost tokens, can be forgotten or argued with, and don't fire deterministically — exactly what hooks guarantee.

**29.** `/context` shows *composition* — how much of the window is system prompt, tools, MCP, skills, CLAUDE.md, messages, free space, and buffer — which is what you need to fix quality problems. `/cost` shows *consumption* — tokens, currency cost, duration, lines changed, and plan-window usage — which is what you need to fix spend and rate-limit problems.

**30.** CLAUDE.md gives the project a stable brain (stack, standards, commands, guardrails) before any file exists to infer it from, and hooks make hygiene automatic from the first write. Set up the factory before manufacturing — otherwise you spend the build correcting conventions instead of building.

---

## Scoring

| Score | Verdict | Next step |
|---|---|---|
| 27–30 | You can teach this | Do the labs; build the capstone |
| 22–26 | Solid | Re-read weak modules, redo those labs |
| 16–21 | Shaky | Re-watch modules 3–7, redo the quiz in two days |
| < 16 | Start over from the study guide | Watch the relevant video segments actively, lab after each module |
