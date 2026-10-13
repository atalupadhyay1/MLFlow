# OpenClaw: AI Agent Automation Stack — Complete Study Material
### Beginner → Advanced | Concept + Hands-On Lab Edition (Humanised, Step-by-Step)

> **Course this follows:** *OpenClaw : AI Agent Automation Stack* — Udemy (by TechLatest.Net)
> Lecture link you shared: `lecture/57634443`
>
> **Honest note before we start:** Udemy lecture videos sit behind a login, so nobody outside your account can watch them. This study pack therefore **preserves the course's public structure and learning outcomes** (Understand OpenClaw → Install on Local/Azure/GCP/AWS → Web Interface & Telegram → Workspace/Identity/Memory → Tools & Skills → 4 Real-World Projects → Production) and rebuilds every topic **in original words**, cross-checked against the official OpenClaw docs at `docs.openclaw.ai`. Think of it as your companion notebook + lab manual for the course — watch a lecture, then come here to *actually do it* and understand *why* it worked.
>
> ⚠️ OpenClaw moves fast. Commands here reflect the official docs at the time of writing. If a command ever disagrees with `docs.openclaw.ai`, trust the docs — and see Chapter 15 on how to diagnose instead of guessing.

---

## Who this is for

| You are… | Start at | You'll get to |
|---|---|---|
| A complete beginner ("what even *is* an agent?") | Chapter 1 | Running your own Telegram AI assistant |
| A developer / DevOps engineer | Chapter 2, skim Ch.1 | Deployed, hardened, scheduled agents on a cloud VM |
| An IT / cloud professional | Chapters 3–4, 12–13 | Ubuntu sysadmin agents, VM readiness reports, production ops |
| A freelancer / builder | Chapters 9–11, 14 | Job-search, news, research & business-reporting agents you can demo/sell |

**No prior OpenClaw experience needed.** Basic comfort with a terminal helps; every command is explained before you run it.

## How to use this material (read this — it will save you hours)

1. **Go in order the first time.** Each chapter builds on the last. Skipping to the projects without Chapters 4–8 is the #1 reason beginners get stuck.
2. **Type the commands, don't copy-paste blindly.** Read the "Why are we doing this?" box first. If you can explain a command to a friend, you own it.
3. **Every chapter ends with 4 things:** ✅ Checkpoint (prove it worked) · 🧪 Lab (build something) · ⚠️ "It broke, now what?" · 🎯 Self-check quiz.
4. **Keep a learning journal.** Copy `templates/learning-journal.md` and fill one row per study session. Agents reward people who iterate.
5. **Budget:** ~18–25 hours total at a comfortable pace (or 5 days × 4 hours). Labs say how long they take.

## Course structure — preserved map

This table is your syllabus. The middle column is the course flow; the right column is where it lives here.

| Course flow (Udemy public outline) | Here |
|---|---|
| Introduction: What is OpenClaw & why agents? | **Ch 1** Foundations: LLMs vs Agents |
| Architecture: agents, models, tools, skills, channels, gateway, sessions | **Ch 2** Architecture Deep-Dive |
| Install & deploy: Local, Azure, GCP, AWS | **Ch 3** Installation (all 4 paths) |
| Gateway, Web Interface (Control UI), request lifecycle | **Ch 4** Gateway & Web UI |
| Telegram integration; other channels | **Ch 5** Channels: Telegram, WhatsApp & more |
| Configure agent instructions, identity, user context | **Ch 6** Workspace: AGENTS / SOUL / USER / IDENTITY |
| Memory, sessions, context | **Ch 6–8** Memory, Sessions, Cron & Heartbeat |
| Skills & plugins (ClawHub) | **Ch 7** Tools, Skills & ClawHub |
| **Project 1:** Automate job searching | **Ch 9** Job-Search Agent |
| **Project 2:** Daily news monitoring & briefing | **Ch 10** News-Monitoring Agent |
| **Project 3:** Technical research, business reporting, marketing automation | **Ch 11** Research & Business-Reporting Agent |
| **Project 4:** Ubuntu sysadmin, VM readiness reports, repetitive online tasks | **Ch 12** Ubuntu Sysadmin & VM-Readiness Agent |
| Secure, scalable, production operation | **Ch 13** Security, Cost & Production Hardening |
| Beyond the course: multi-agent & advanced automation | **Ch 14** Advanced: Sub-agents & Multi-Agent |
| Troubleshooting, revision, capstone | **Ch 15** Troubleshooting, FAQ, Capstone & Interview Prep |

## The 12 hands-on labs (at a glance)

Detailed lab sheets are in [`labs/LAB-MANUAL.md`](labs/LAB-MANUAL.md) and woven into chapters.

| # | Lab | Time | Chapter |
|---|---|---|---|
| 1 | "Hello, Agent" — install locally & first chat | 30 min | 3 |
| 2 | Deploy OpenClaw on a cloud VM (pick Azure/GCP/AWS) | 60 min | 3 |
| 3 | Gateway detective — trace one message end-to-end | 30 min | 4 |
| 4 | Telegram bot from BotFather to "it replies!" | 45 min | 5 |
| 5 | Give your agent a personality (workspace files) | 45 min | 6 |
| 6 | Memory that survives a restart | 30 min | 6/8 |
| 7 | Install a skill from ClawHub + write your own SKILL.md | 60 min | 7 |
| 8 | Cron vs Heartbeat — schedule a morning briefing | 45 min | 8 |
| 9 | Job-search agent (Project 1) | 90 min | 9 |
| 10 | News-monitoring agent (Project 2) | 75 min | 10 |
| 11 | Research → report agent (Project 3) | 90 min | 11 |
| 12 | Ubuntu sysadmin & VM-readiness agent (Project 4) + hardening | 90 min | 12/13 |

## Folder map

```
openclaw-study-material/
├── README.md                  ← you are here
├── 01-foundations.md … 15-troubleshooting-capstone.md   ← the textbook
├── labs/LAB-MANUAL.md         ← printable lab sheets with expected outputs
├── templates/
│   ├── workspace/             ← copy-paste AGENTS.md, SOUL.md, USER.md, IDENTITY.md, MEMORY.md, HEARTBEAT.md
│   ├── skills/                ← ready-to-edit example skills (job-search, daily-brief, sysadmin-check)
│   ├── configs/               ← openclaw.example.json, cron-jobs.example.json, .env.example
│   └── learning-journal.md
└── cheatsheets/commands.md    ← one-page command & concept cheat sheet
```

## Before Chapter 1 — set up your study environment

You need only three things to begin; cloud accounts come in Chapter 3 and are optional on day one.

```bash
# 1) A terminal: Terminal (macOS) / PowerShell or WSL2 (Windows) / any Linux shell
# 2) Node.js 22+ (OpenClaw's runtime — Chapter 3 checks this properly)
node --version    # want: v22.x or higher
# 3) One LLM API key OR an existing Claude Code / Codex login
#    (Anthropic Claude and OpenAI are the most common; OpenRouter/Gemini/Ollama also work — Ch. 2 explains the trade-offs)
```

> 💬 **A human word of encouragement:** Everyone's first agent feels a bit magical and a bit broken at the same time. That's normal — it's literally everyone's experience, including professionals'. The difference between people who "did the course" and people who *can do this* is just: they finished the labs and debugged two or three real errors. This book will walk you through exactly that. Let's begin.

**→ Next: [Chapter 1 — Foundations: From Chatbots to Agents](01-foundations.md)**
