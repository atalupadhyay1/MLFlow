# Chapter 15 — Troubleshooting Playbook, FAQ, Capstone & Interview Prep
*Course wrap-up: keep it running, prove you learned it · Time: ~90 min + Capstone (half day, gloriously)*

## 15.1 The troubleshooting method (memorise the order)
```
1. REPRODUCE   make it fail again, on purpose, watching logs (foreground gateway)
2. LOCATE      which layer? channel → gateway → session/context → model → tool/skill → payload data
3. ONE CHANGE  fix the smallest thing; restart; retest
4. RECORD      journal: symptom, cause, fix. Your future incidents are 70% repeats.
```
Golden commands: `openclaw gateway status` · `openclaw doctor` · `openclaw triage` · `openclaw gateway --port 18789` (live logs) · `openclaw configure` · dashboard (Channels status first).

## 15.2 Master symptom table (every pain in this book, one page)
| Symptom | Layer | Go to |
|---|---|---|
| Dashboard won't open (local) | Gateway | gateway status → foreground logs → port conflict? |
| Dashboard won't open (VM) | Access | Tunnel up? bind loopback is *why* tunnel is needed; firewall SSH ok? |
| No reply on Telegram/WhatsApp | Channel | Channels status → pairing approved? → allowFrom? → token/login fresh? (Ch 5 table) |
| Replies but generic/wrong personality | Context | Workspace path; files edited? restart + `/new` (Ch 6) |
| Forgot yesterday | Memory/session | Daily note written? MEMORY.md curated? session reset too aggressive? (Ch 6/8) |
| Skill never triggers | Skill | Debugging ladder: description → discovery → tools → model → conflicts (Ch 7) |
| Tool errors in logs | Tool | Tool enabled? permissions/sandbox? run the command yourself via SSH to compare |
| Cron silent / wrong hour | Schedule | Job enabled? payload self-sufficient? VM timezone; manual-fire test (Ch 8) |
| Heartbeat expensive/noisy | Schedule | Silence conditions; interval; cheap model; log review (Ch 8/13) |
| Costs spiking, no culprit | Ops | Provider usage by day vs job list; kill zombie jobs (Ch 13) |
| Agent did something unapproved | Safety | Stop gateway; logs; tighten guardrails/least-privilege; incident journal (Ch 12/13) |
| "It just feels haunted" | Meta | `doctor` → `triage` → read slowly. Then journal. Then fix ONE thing |

## 15.3 FAQ (the questions every learner asks)
**Q: Local or cloud — if I can only pick one?** Local to learn, cloud to *run on schedule*. Most graduates end with both (same config, Ch 3.7).
**Q: Which model should I start with?** A mid-tier hosted model with reliable tool-calling (mainstream Claude/GPT class or equivalent), a provider cap set. Optimise later with data (your weekly cost review), not vibes.
**Q: Do I need to code?** You need terminal comfort and Markdown. Scripts appear inside skills optionally; every lab here works without writing application code.
**Q: My agent is smart but inconsistent. Normal?** Yes — narrow the skill, cap outputs, add examples to SKILL.md. Consistency comes from instructions + files, not hope.
**Q: Can my team share one agent?** Yes with per-sender sessions + mention-only groups + a shared-workspace agent that never loads your private MEMORY.md (Ch 14).
**Q: How do I keep up as OpenClaw changes?** Release notes + `docs.openclaw.ai` + updating laptop-first (Ch 13). Your workspace files and skills are portable Markdown — your investment survives version bumps.
**Q: Is my Udemy certificate + this enough for jobs/freelancing?** Certificate proves attendance; a *running system* proves skill. The Capstone below is the portfolio piece — demo the Telegram morning stack live and watch the room change.

## 15.4 🏆 The Capstone — "One Morning in My Automated Life" (half day)
**Brief:** Assemble your best version of the Ch 14 morning stack and run it for real, once, end-to-end, on schedule:
1. Sysadmin readiness (VM) — 07:30 slot.
2. News brief (your topics) — 08:00 slot.
3. One more of: job shortlist / business report / research radar.
4. Heartbeat with a silence condition, observed for ≥ 2 cycles.
5. A one-page **run-book** in your journal: architecture diagram (Ch 2 style), jobs table (schedule/payload/model/cost), hardening checklist status, backup-restore proof, incident drill result (plant a fault; show the catch — Ch 12 style).
**Pass bar:** A friend watching your phone at 08:05 understands what happened and why; your run-book convinces a sceptical engineer it's safe and costed; the planted fault was caught without you touching anything.
**Portfolio move:** 3-minute screen-record: phone receiving the morning stack → VM dashboard → one skill file open. Narrate with Chapter 1's language (loop, gateway, skill, session). This beats ten certificates in interviews. Tag it to your Lab 1 "day one" screenshot. Progress, documented, is the credential.

## 15.5 Interview & viva prep (likely questions, strong answer shapes)
1. *"Agent vs chatbot?"* → Loop + tools + memory + channels; OpenClaw's Gateway executes tool calls under rules (§1.2, §2.1).
2. *"How does the agent remember?"* → Files: daily notes distilled to MEMORY.md, loaded per session; context limits handled by compaction/resets (Ch 6/8).
3. *"Cron or heartbeat for X?"* → Timing vs monitoring framing + a cost sentence (Ch 8).
4. *"Biggest security risks?"* → Open access, injection, malicious skills, secret leakage — each with its countermeasure (Ch 13).
5. *"It hallucinated in production. Your response?"* → Evidence-first skills (fetch-before-claim, citations, UNKNOWN labels), approval gates, incident method (§15.1).
6. *"Cost control?"* → Per-job models, caps/alerts, verbosity caps, weekly kill-the-zombies review (Ch 13).

## 15.6 Your next 30 days (so this doesn't evaporate)
- **Week 1:** Re-run any shaky lab; write two more personal skills (capture, summarise-link).
- **Week 2:** Harden for real (Ch 13 ticked), cloud deployment if still local-only.
- **Week 3:** One fan-out or Workspace-integration skill, vetted properly.
- **Week 4:** Capstone polish + demo recorded; teach one friend (teaching is the final lab — you'll find your own knowledge gaps at minute three, guaranteed).
Keep the weekly 10-minute ops review forever. Systems stay alive through rituals, not enthusiasm.

## 🎓 Graduation checkpoint
- [ ] Capstone run-book complete, planted fault caught.
- [ ] Journal contains: Lab 1 screenshot, cost numbers, two incident entries, demo link.
- [ ] Re-read your Ch 1 journal prompt ("first task I'd trust…"). Rewrite it now. Notice the difference. *That's* the course, learned.

> 💬 **Last word, human to human:** You didn't just learn a tool; you learned a way of delegating to software that talks back. Use it to remove drudgery, never to remove your judgement. Build agents that make you calmer and more informed — and keep the approval button close. Good luck, and good building. 🦞

**← Back to [README / Course Map](README.md) · [Lab Manual](labs/LAB-MANUAL.md) · [Cheat Sheet](cheatsheets/commands.md)**
