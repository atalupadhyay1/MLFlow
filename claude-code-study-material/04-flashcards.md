# Flashcards — Claude Code Course

75 cards. Cover the answer, say it out loud, then check. Cards marked ⚠️ cover version-specific facts that may have changed.

**How to use:** front/back pairs below. For spaced repetition, do 15–20 a day: day 1 → day 3 → day 7 → day 21. Anything you miss, add to a "leech" list and re-read the matching study-guide section.

---

## Foundations

**1. Who builds Claude, and who builds ChatGPT?**
Anthropic builds Claude; OpenAI builds ChatGPT.

**2. Why does the course compare Claude to ChatGPT?**
Because everyone has used ChatGPT, so it's the fastest way to place Claude in a familiar frame — same category, different company and different emphasis (safety-first).

**3. Name the three Claude model tiers and their characters.**
Haiku (fast, cheap, simple), Sonnet (balanced, everyday work), Opus (most capable, complex reasoning). ⚠️ version numbers change.

**4. What is the course's rule of thumb for choosing a model?**
Match the model to the job: Opus for planning/architecture, Sonnet for building, Haiku for maintenance and simple tasks. More power = more cost and faster limits.

**5. What is extended thinking?**
A mode where the model deliberates longer before answering, for complex problems and debugging. Availability varies by model. ⚠️

**6. What exactly is "Claude Code" in the brain/hands model?**
The same Claude brain, but with hands: it's installed on your machine so it can run terminal commands, read/write/delete files, and execute code.

**7. What is "the hands"?**
The terminal (shell). Anything that can run commands in your terminal has access to your machine.

**8. What can Claude on the desktop app do that the web version can't?**
Small conveniences like capturing screenshots from your system — but it still cannot touch your files. Analogy: a smart person on the phone.

**9. Describe the agentic loop.**
Ask → plan → act (read files, run commands, search) → observe the result → check → retry if needed → answer. It's iteration at high speed, not magic.

**10. Why is the agentic loop worth understanding before learning features?**
Skills, hooks, MCP, and subagents are all ways of shaping that loop — better procedures, reflexes, tools, and workers.

## Installation & auth

**11. Which install path does the course recommend?**
The native terminal install. Download the desktop app and IDE extensions for convenience, but the terminal teaches the mechanics.

**12. What Windows-specific advice does the course give?**
Use the exact install command for your shell (PowerShell vs CMD), and consider installing Windows Terminal for the Unix-like experience most tutorials assume.

**13. What are you agreeing to at the "trust this workspace" prompt?**
That Claude Code may read, write, and execute files in that folder. It's the real security boundary — trust deliberately.

**14. Subscription vs API key for Claude Code?**
Subscription (Pro/Max) draws from plan limits; an API key bills per token and is needed for headless/programmatic use.

**15. Where is session history stored on disk?**
Under `~/.claude/` (per-project folders) — that's how `/resume` and rewind bring past conversations back.

**16. First three things to check when the CLI misbehaves after install?**
New terminal/PATH, correct shell (Windows), clean reinstall if versions mismatch.

## Commands, modes, `.claude`

**17. What does `/model` warn you about when switching?**
The conversation is cached for the current model — switching makes the full history get read again, which costs tokens. Don't switch constantly.

**18. What does `/effort` control?**
How much thinking budget the model spends (low → max). High for hard problems, low for chores.

**19. What does `/cost` show?**
Session cost, tokens, duration, lines changed, and how much of your plan's usage window is consumed, often per model.

**20. `/context` vs `/compact` vs `/clear`?**
`/context` = inspect what fills the window. `/compact` = summarise and continue. `/clear` = start a fresh session (old one stays on disk).

**21. What is `/branch` (fork) for?**
Continuing from a point in a *new* session with a new ID, leaving the original intact — safe experimentation.

**22. Name the common permission modes.**
Default (ask), accept-edits, plan (read-only), auto, don't-ask, bypass (isolated environments only). ⚠️ names shift over time.

**23. Which permission mode is read-only, and when is it most useful?**
Plan mode — exploring an unfamiliar codebase or a risky change before anything is edited.

**24. How do you cycle permission modes in a session?**
`Shift+Tab`.

**25. Why is `.claude` hidden, and how do you see it?**
It's a dot-directory, intentionally invisible to casual users; `ls -la` or enabling hidden files reveals it.

**26. Name six things that live in `.claude/`.**
CLAUDE.md, settings.json, rules/, skills/, agents/, commands/, hooks/, MCP config, plugins (any six).

**27. Where do custom slash commands come from?**
Markdown files in `.claude/commands/` — the filename becomes the command.

## CLAUDE.md

**28. What problem does CLAUDE.md solve?**
It gives Claude permanent knowledge of the project (stack, commands, standards, rules), so sessions don't start from zero and repeat the same mistakes.

**29. List the CLAUDE.md priority hierarchy, weakest → strongest.**
Enterprise/managed → user (`~/.claude/CLAUDE.md`) → project (`./CLAUDE.md` or `.claude/CLAUDE.md`) → `CLAUDE.local.md`.

**30. How does Claude find instruction files?**
It walks up the directory tree from the working directory, loading CLAUDE.md / CLAUDE.local.md along the way.

**31. What belongs in CLAUDE.md?**
Project overview, essential commands, code style/naming, structure, testing workflow, hard rules/guardrails, verification steps, pointers to other docs.

**32. Name three things that do NOT belong.**
Full API documentation, code snippets that will drift, task-specific instructions (and never secrets). ⚠️ Also: outdated info is worse than none.

**33. What trick keeps CLAUDE.md lean while still pointing at detail?**
Imports (`@path/to/file.md`) — modular brain, small always-loaded core.

**34. What happens to HTML comments in instruction files?**
They're stripped before the content is injected into context — useful for human-only notes.

**35. When should you add something to CLAUDE.md?**
The second time a mistake happens, when a review catches something Claude should have known, or whenever you re-explain the same convention.

**36. How do you bootstrap CLAUDE.md quickly?**
`/init` to draft it from the repo, then edit ruthlessly.

## Context management

**37. Why is every message expensive?**
LLMs are stateless: each turn re-sends the whole history plus system prompt, tools, MCP definitions, skills, and CLAUDE.md.

**38. What is context rot?**
Degradation in a long session — ignored instructions, repeated work, new mistakes — caused by context volume and the model's attention bias toward the start and end.

**39. Why does "the model got dumber" usually mean something else?**
Because the model didn't change — the context did. It's a resource-management problem on your side.

**40. Three tactics to fix a rotten context?**
Inspect `/context`; `/compact` with explicit instructions on what to keep; or `/clear` and start fresh (optionally handing over a status/changelog file).

**41. What's the right way to use `/compact`?**
Pass instructions for what must survive (file structure, endpoints, patterns) instead of letting it summarise blindly.

**42. Name four context costs under your control.**
CLAUDE.md size, number of enabled MCP servers, session length/hygiene, prompt specificity (also: skills, model/effort, pasting images and large files).

**43. Which context costs are not under your control?**
The platform system prompt and core tool definitions.

**44. What's the cost pattern that surprises people?**
The *same* history is billed as input tokens on every call; a 200K-token context makes each subsequent message expensive (~$3 for five messages in the course's example ⚠️).

**45. Best practice when starting a new topic mid-session?**
`/clear` (or a new session) — don't drag the old context along.

## Skills

**46. What is a skill?**
A reusable playbook: `SKILL.md` with frontmatter (name, description, trigger) plus instructions, and optionally scripts, references, and assets.

**47. Why don't 20 skills blow up your context?**
Progressive disclosure: only name and description sit in context until a skill is actually invoked.

**48. Which frontmatter field makes a skill get invoked automatically?**
`description` — it tells the model when the skill applies.

**49. When should a skill contain a script rather than instructions?**
When the steps are deterministic and repeatable — scripts run identically every time and cost no generation tokens.

**50. Where do skills live?**
Project: `.claude/skills/<name>/SKILL.md`. Personal: `~/.claude/skills/`. Also bundled inside plugins.

**51. What did the course's `expense-summary` skill do that's worth copying?**
Specified the output format literally, documented calculation rules and edge cases, and gave a sample output.

**52. How do you create skills fast?**
Use a skill-creator skill: describe what you want, answer its clarifying questions, then refine arguments/model/effort.

**53. Skill vs custom slash command?**
A command is a saved prompt; a skill is procedural knowledge that may include scripts and assets and is auto-invocable.

## Hooks

**54. Why are hooks "zero token"?**
They run outside the model, triggered by lifecycle events — no prompt, no context, no generation cost.

**55. Name five hook events.**
SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, Stop (also: Notification, SessionEnd, subagent/task events, pre-compact).

**56. What does exit code 2 do in a hook?**
Blocks the action and sends stderr back to Claude as the reason. This is the emergency brake (exit 0 = allow; other codes = non-fatal error).

**57. What is a hook matcher?**
The pattern selecting which events/tools a hook fires for, e.g. `"Bash"` or `"Write|Edit"`.

**58. Where are hooks configured?**
In `settings.json` (project or user scope), under the `hooks` key; the scripts themselves usually live in `.claude/hooks/`.

**59. Why does the course say to let Claude add your first hook?**
Hand-editing settings while the tool initialises can lead to the file being overwritten and the hook lost. Let Claude write it, then inspect.

**60. Give three classic hook uses.**
Auto-format after writes, block dangerous bash commands (security guard), notify/log around sessions.

**61. What should you always do before trusting a hook?**
Test it by hand with a sample JSON payload and confirm its exit code.

## MCP

**62. Define MCP in one sentence.**
An open standard for how AI agents communicate with external tools and data sources — a maintained toolbox instead of custom glue code.

**63. Connectors vs MCP?**
Connectors are ready-made vendor integrations inside Claude; MCP is the open protocol you configure yourself (local or hosted servers).

**64. Local vs hosted MCP server — pick one example each.**
Local: Playwright browser automation / filesystem tools (uses your RAM). Hosted: Gmail, Slack, Tavily (URL + API key).

**65. How are MCP secrets handled?**
Environment variables referenced in config (`${TAVILY_API_KEY}`) — never committed literals.

**66. Name the three MCP config scopes.**
Project (committed, team), user (all your projects), local (private, not committed).

**67. Which command inspects MCP servers and their tools?**
`/mcp`.

**68. Why can too many MCP servers make Claude worse?**
Every server's tool descriptions consume context on every request, and overlapping tools confuse tool selection.

**69. What makes a custom MCP server's tool usable by the model?**
Its name, description, and JSON-schema parameters — the description is effectively the prompt for when to call it.

## Subagents

**70. What defines a subagent?**
An isolated worker with its own context window, system prompt, tool permissions, and optionally a cheaper model — the main session gets back only a summary.

**71. Give three reasons to use subagents.**
Keep the main context clean, cut cost with cheaper models on routine work, and parallelise/focus work with restricted tools.

**72. How are subagents invoked?**
Natural language (auto by description), explicit `@name` mention, or the `/agents` manager.

**73. Why restrict `tools` / `disallowedTools` on a subagent?**
Safety and focus — like an intern who can read the code but can't touch your email or run destructive commands.

**74. Rule of thumb for when work should be a subagent?**
When it requires reading a lot to produce a little.

## Agent teams, plugins, scheduling

**75. What's the structural difference between subagents and agent teams?**
Subagents report back to one parent (hierarchy); agent teammates coordinate with each other (peers) in separate sessions, using git worktrees for isolation.

**76. What enables agent teams, and what's the caveat?**
An experimental settings flag (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` ⚠️); the feature is unstable and burns tokens fast.

**77. What does a plugin bundle?**
Agents, skills, commands, hooks, MCP servers, settings, and CLAUDE.md — installable in one step and shareable via git.

**78. Why use `${CLAUDE_PLUGIN_ROOT}` in plugin hooks?**
So hook paths resolve correctly wherever the plugin is installed.

**79. What due diligence is required for community plugins?**
They aren't reviewed by Anthropic and run with your permissions — read the hooks/commands and check reputation before installing.

**80. Name the three scheduling options and their laptop requirements.**
`/loop` (machine on, session open), desktop scheduled task (machine on), Claude routine (cloud — laptop can be closed). Headless `claude -p` is the scriptable form.

**81. Why is headless mode essential for schedules?**
A scheduled run that stops to ask for permission is a broken schedule; `claude -p` never blocks on prompts (it still enforces permissions — it just has no UI).

**82. The five safety rules for unattended automation?**
Start read-only; write to non-destructive paths; human review gates for irreversible actions; log everything; test for days before trusting it.

**83. Rewrite the bad automation: "when tests pass, deploy."**
"Write a READY-TO-DEPLOY file and ask a human in Slack to deploy" — keep the irreversible step behind a person.

**84. Why is a scheduled Claude task better than a cron script?**
Reasoning, not just execution: it can read an error, try an alternative, document the failure, and notify with a diagnosis.
