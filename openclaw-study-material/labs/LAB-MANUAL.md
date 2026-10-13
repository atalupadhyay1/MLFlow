# Hands-On Lab Manual — OpenClaw: AI Agent Automation Stack
*Print this. Tick boxes with a real pen if you can. Every lab: Goal → Needs → Steps → Expected output → Prove it → If it breaks.*

General setup for all labs: terminal open, journal open (`../templates/learning-journal.md`), Gateway commands from Ch 4 at hand. Times are honest medians for a first attempt.

---

### Lab 1 — "Hello, Agent" (Ch 3) · 30 min
**Goal:** Local install + first dashboard chat. **Needs:** Node 22+ or installer, one LLM key/login.
**Steps:** installer one-liner (your OS, Ch 3.2) → Custom setup onboarding → daemon yes → `openclaw gateway status` → `openclaw dashboard` → chat "Hello! What can you do?"
**Expected:** Gateway on 18789; AI reply naming capabilities. **Prove it:** screenshot saved; journal row written.
**If it breaks:** model test fail → key/billing; port busy → stray gateway (Ch 4 traps).

### Lab 2 — Cloud deployment (Ch 3) · 60 min
**Goal:** Same agent on Azure *or* GCP *or* AWS VM. **Needs:** one cloud account, SSH key.
**Steps:** VM (Ubuntu, small) → firewall SSH-only (your IP) → SSH in → install → onboard → `openclaw gateway install` → SSH tunnel `-L 18789:127.0.0.1:18789` → dashboard → chat test → billing/budget alert set.
**Expected:** Dashboard via tunnel only; service survives `gateway restart`. **Prove it:** close tunnel → dashboard unreachable (that's a pass!); reopen → works.
**If it breaks:** service dies at logout → `sudo loginctl enable-linger $USER`.

### Lab 3 — Gateway detective (Ch 4) · 30 min
**Goal:** Trace one message. **Steps:** foreground gateway (or dashboard logs) → tool-forcing prompt → label channel/session/model/tool/reply in logs.
**Expected:** journal lists model, tool, round-trip count (usually 2–3). **Prove it:** narrate it aloud using §2.1 vocabulary.
**If it breaks:** ask the agent "which tools do you have?" and compare.

### Lab 4 — Telegram agent (Ch 5) · 45 min
**Goal:** BotFather → paired, allowlisted Telegram agent. **Steps:** `/newbot` → token → config `dmPolicy: pairing` → restart → DM → approve pairing → test reply → second-account rejection test.
**Expected:** You get replies; stranger gets gate, not answers. **Prove it:** one-sentence trust model in journal.
**If it breaks:** Ch 5 troubleshooting table, top to bottom.

### Lab 5 — Personality transplant (Ch 6) · 45 min
**Goal:** Workspace files visibly change behaviour. **Steps:** backup workspace → copy templates → personalise USER/IDENTITY/SOUL → restart + `/new` → identity interview → one-line edit → retest.
**Expected:** answers reflect your facts + dictated style, twice (before/after edit). **Prove it:** paste both answers in journal; the difference is your evidence.
**If it breaks:** workspace path in config (Ch 4 trap).

### Lab 6 — Immortal memory (Ch 6) · 30 min
**Goal:** Fact survives restart. **Steps:** teach fact → agent writes daily note → verify file → distil to MEMORY.md → restart + `/new` → quiz agent.
**Expected:** correct recall with files open beside you showing the source. **Prove it:** highlight the exact file lines.
**If it breaks:** file written? read at session start? path right?

### Lab 7 — Skills: vet, install, author (Ch 7) · 60 min
**Goal:** One ClawHub skill vetted + `note-to-self` authored and iterated.
**Vetting checklist (fill for the installed skill):**
```
Skill: __________  Source/maintainer: __________  Date: ____
□ Full SKILL.md read   □ All scripts read   □ Tools demanded: __________
□ Network calls explained: __________  □ Secrets requested: none / __________
□ Web-chat test passed; tool calls in logs matched description: □
Verdict: INSTALL / REJECT (why): __________
```
**Expected:** "Note this: …" appends timestamped line to today's memory file; one style iteration visible. **Prove it:** memory file diff.
**If it breaks:** Ch 7 debugging ladder, in order.

### Lab 8 — Scheduling (Ch 8) · 45 min
**Goal:** Cron brief + disciplined heartbeat. **Steps:** brief skill on-demand ✓ → cron job (tomorrow 08:00) → manual-fire → HEARTBEAT.md with silence rule, `every: 30m` → watch 2 cycles.
**Expected:** on-schedule delivery; silent healthy heartbeats. **Prove it:** cost-per-brief from provider dashboard, journalled.
**If it breaks:** payload self-sufficiency; VM timezone.

### Lab 9 — Job-search agent (Ch 9) · 90 min
**Goal:** Deduped, reasoned shortlist on a schedule. **Steps:** USER.md criteria → template skill → dry run → interrogate rejects → rerun (dedupe ✓) → skill fix → cron + cron-path test.
**Expected:** 0 duplicates across runs; every reject reasoned; ≤5 items formatted. **Prove it:** job-search-log.md contents.
**If it breaks:** Ch 9 failure gallery.

### Lab 10 — News brief (Ch 10) · 75 min
**Goal:** 90-second, sourced, deduped morning brief. **Steps:** ≤3 topics in USER.md → brief skill upgrade → adversarial source check → weekly-themes cron → scheduled brief.
**Expected:** 3 briefs, 0 repeats, 0 unverifiable claims, relevance line per item. **Prove it:** click every link yourself once.
**If it breaks:** fetch-before-summarise; dedupe by event.

### Lab 11 — Research report (Ch 11) · 90 min
**Goal:** A forwardable report file. **Steps:** real question → sources-file-first verified → skeleton grading → single-source interrogation → one recurring cron report.
**Expected:** citations, assumptions, unknowns, confidence stated. **Prove it:** you actually forward/send it somewhere.
**If it breaks:** Ch 11 failure gallery.

### Lab 12 — Sysadmin readiness + hardening (Ch 12–13) · 90 min
**Goal:** Trusted read-only monitor with approval-gated actions. **Steps:** manual baseline → skill → two comparison iterations → schedule → unapproved-action test (must refuse/ask) → planted-fault test (filler file) → Ch 13 checklist on this deployment.
**Expected:** verdicts match yours; planted fault caught; nothing mutates unapproved. **Prove it:** memory-note log of the approved action + your checklist ticks.
**If it breaks:** hostname line; thresholds; approval guardrail rewrite + full retest.

---

## Capstone lab (Ch 15) — pass bar recap
Morning stack live on schedule + run-book (diagram, jobs table with costs, hardening status, backup-restore proof, planted-fault catch) + 3-minute demo recording. See Ch 15 §15.4.

## Lab safety oath (sign it in your journal)
*I will keep gateways loopback + token, channels allowlisted, skills vetted, actions approval-gated, backups tested, and billing capped — before I make anything clever.* Signature: ______ Date: ______
