# Part 13 — Capstone: DailyPulse, spec-first full-stack build
**Video:** 11:56:47 – 13:53:46 (Module 13)

**In this part:** 13.1 Factory setup (spec, CLAUDE.md, hooks, prompts) · 13.2 Backend · 13.3 Frontend & debugging · 13.4 AI features, scheduling, go-live

> This is the revision exercise for Parts 1–12. You can build DailyPulse exactly as the course does, or substitute your own app — **keep the sequence**, because the sequence is the lesson.
>
> **What DailyPulse is:** a personal productivity web app — morning briefing, smart tasks (AI breaks a task into subtasks), a standup generator from today's completed tasks, daily insights, plus weather and a live AI news feed.

---

## 13.1 Factory setup: spec, CLAUDE.md, hooks, prompts

### What it is
Everything *before* the first application line of code:
1. a **spec** (what you're building, for whom, what "done" means),
2. a **CLAUDE.md** (stack, ports, storage, standards, commands, verification),
3. **hooks** (at minimum auto-format; ideally a session logger),
4. a **prompts file** — the build prompts written in advance, one per phase.

### Why it matters
- The course's explicit advice: **behave like a tech lead, not a prompt tourist.** If you don't specify architecture, the model invents one — and you spend the rest of the build paying for that decision.
- Hooks and CLAUDE.md before code means hygiene is automatic from the first file; retrofitting them after 40 files is wasted effort.
- Pre-written prompts keep you in control of *sequence and scope* — the AI executes, it doesn't wander.
- **The two-AI pattern:** use a different AI as "CTO" to draft technical prompts from your product spec, then give those prompts to Claude Code. Two roles, better output.

### How to do it (step by step)
1. **Write the spec** in plain English (the course builds from exactly such a document): features, users, data, and what you will *not* build. Include the tech stack and ports.
2. **Create the repo** and initialise git. Commit the spec.
3. **Write CLAUDE.md** using the Part 4 template, filled with *this* project's reality:
   - Backend: FastAPI on port 8000, JSON files in `backend/data/` (tasks.json, briefing.json), python-dotenv for env vars.
   - Frontend: React + Vite + Tailwind on port 5173, `fetch()` to `http://localhost:8000`, `useState`/`useEffect` only.
   - Standards: type hints + docstrings + black for Python; functional components + loading/error states for React.
   - Commands: how to install, run and test each side.
4. **Add hooks** before writing app code:
   ```json
   { "hooks": {
       "PostToolUse": [ { "matcher": "Write|Edit",
         "hooks": [ { "type": "command",
                      "command": "jq -r '.tool_input.file_path' | { read -r f; [[ \"$f\" == *.py ]] && python -m black \"$f\" --quiet; } 2>/dev/null || true" } ] } ],
       "Stop": [ { "hooks": [ { "type": "command",
                    "command": "echo '[DailyPulse] Claude finished — review output above' >&2", "async": true } ] } ] } }
   ```
   (Simplest reliable version: a small Python formatter script — the course's DailyPulse settings use exactly that pattern.)
5. **Write `prompts.md`** — one prompt per phase: backend, test endpoints, frontend, fix CORS, add live news, schedule it. Review them as a sequence *before* running any.
6. Optional but recommended: hand the spec to ChatGPT/Claude-as-CTO and ask it to produce those technical prompts. Paste them into `prompts.md`.

**Lab 13.1 — Factory, then nothing else**
- [ ] Spec committed (features, stack, ports, non-goals).
- [ ] CLAUDE.md written from the template with real commands and verification steps.
- [ ] Auto-format hook proven (write a messy `.py` file, watch it clean up).
- [ ] `prompts.md` written with all phases, reviewed as a sequence.
- [ ] (Stretch) A second AI produced the prompt set from your spec.

**Proof:** the committed spec + CLAUDE.md + a formatting event in your log + `prompts.md`.

**Quiz 13.1**
1. Why set up CLAUDE.md and hooks *before* generating application code?
2. What is the two-AI pattern, and what problem does it solve?
3. Your prompts file has one giant prompt: "build the whole app". Give two reasons to split it by phase.

---

## 13.2 Backend: FastAPI, storage, endpoints

### What it is
- A **FastAPI** service with a **thin route layer** over a services module:
  - `backend/main.py` — routes only (plus CORS middleware),
  - `backend/services.py` — business logic and AI calls,
  - `backend/data/` — JSON storage (`tasks.json`, `briefing.json`),
  - `backend/requirements.txt` — dependencies.
- Endpoints that mirror the features: tasks (list/create/complete), smart-task breakdown (AI → subtasks), briefing, standup, insights.

### Why it matters
- The **thin-routes/services split** is what keeps the build maintainable and gives the AI a clear place for each kind of change. Ask for a route, get a route; ask for logic, get logic — not both tangled in one file.
- **JSON storage** keeps the capstone dependency-free while teaching the shape of real persistence. Swapping in a database later is a contained change.
- **Explicit endpoint contracts** in your prompt ("POST /tasks with this schema, calling the AI to split the title into 3–5 subtasks") prevent the model from inventing its own API — the single most common cause of frontend/backend mismatch.
- The course's own lesson: give the AI *schemas*, not vibes.

### How to do it (step by step)
1. Paste the **backend prompt** from `prompts.md` (adjust to your spec). Include, explicitly:
   - files to create and their responsibilities,
   - each endpoint with method, path, request and response shape,
   - storage format and file locations,
   - the AI call and what it returns (and a **fallback** if the AI fails),
   - CORS middleware for the frontend origin.
2. Let it build; then **read the diff** — don't accept blindly. Check the routes are thin and logic lives in services.
3. Install and run:
   ```bash
   cd backend && python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn main:app --reload --port 8000
   ```
4. **Test every endpoint before touching the UI** (the course does exactly this):
   ```bash
   curl -s localhost:8000/tasks | jq
   curl -s -X POST localhost:8000/tasks -H 'content-type: application/json' -d '{"title":"Write lab notes"}'
   curl -s localhost:8000/briefing | jq
   ```
5. Verify the **data files** appear/update in `backend/data/` after writes.
6. Ask Claude to fix anything that doesn't match the contract — one endpoint at a time, with the failing curl output pasted in.

**Lab 13.2 — Backend, tested by hand**
- [ ] `main.py` routes are thin; logic lives in `services.py`.
- [ ] Data files created in `backend/data/`.
- [ ] Every endpoint tested with curl and returning the documented shape.
- [ ] CORS middleware present for the frontend origin.
- [ ] One AI-backed endpoint has an explicit fallback path when the provider fails.

**Proof:** curl outputs for each endpoint (saved to a file) and the data files on disk.

**Quiz 13.2**
1. Why keep routes thin and logic in a services module?
2. What goes wrong when your prompt omits request/response schemas?
3. Testing endpoints with curl before building the UI saves time. Explain why in terms of debugging surface area.

---

## 13.3 Frontend, screenshots and CORS debugging

### What it is
- A **React + Vite** frontend (+ Tailwind) with components for the briefing, task manager, standup generator, insights, weather and header.
- The inevitable first-run problems: **CORS**, port mismatches, wrong API base URL, missing loading/error states.
- The course's debugging method: **take a screenshot of the broken page, compress it, paste it with "fix this"** — and iterate.

### Why it matters
- The frontend is where the AI's output and reality collide: browser security (CORS), timing (loading states), and UX details. This phase is normal engineering, not failure.
- **Images consume context**, so compressing a screenshot before pasting is a genuinely cost-relevant habit, not a nicety.
- It teaches the loop that matters in real work: observe → paste evidence → fix → verify.

### How to do it (step by step)
1. Paste the **frontend prompt** from `prompts.md`: components, the API base URL, `fetch` usage, and the rule "loading and error states on every API call".
2. Run it:
   ```bash
   cd frontend && npm install && npm run dev
   ```
3. Open the app. Expect failures. **Capture evidence:** take a screenshot, compress it, and paste it with the observed behaviour ("generate standup returns a red error banner; console shows CORS").
4. **Fix CORS properly, not by accident.** Two acceptable shapes:
   - Backend middleware allowing the frontend origin (`http://localhost:5173`), or
   - A dev proxy in Vite config.
   Confirm with the browser network tab — a 200 with the right `Access-Control-Allow-Origin`, not just "it works now".
5. **Fix the AI-failure UX:** when the AI provider is down or out of quota, the button must degrade gracefully (disabled + clear message), not crash. Test by removing the API key temporarily.
6. Re-verify each component after each fix: briefing renders, tasks add/complete, standup generates, insights show.
7. Add a `/compact` checkpoint before large changes now (see 13.4) — this app's context grows fast.

**Lab 13.3 — From broken to working**
- [ ] All components render with real backend data.
- [ ] Screenshot-driven fix documented (before/after).
- [ ] CORS explained and verified in the network tab (not just "works now").
- [ ] Loading and error states present on every API call.
- [ ] AI-unavailable path tested deliberately.

**Proof:** before/after screenshots, the network-tab header evidence, and the graceful-failure screenshot.

**Quiz 13.3**
1. Why compress a screenshot before pasting it, in context terms?
2. What is the difference between "CORS is fixed" and "the page stopped showing an error"?
3. Your app's AI feature throws a 500 when the provider quota is exhausted. What's the correct behaviour and which Part taught it?

---

## 13.4 AI features, scheduling, and going live

### What it is
- **Real AI in the app:** a provider API key (Gemini, OpenRouter, Claude API…), a model choice, and graceful fallback.
- **Live data:** a news/weather feed (the course wires Tavily; MCP optional).
- **Scheduling:** the app refreshes itself (briefing generation) via cron or a routine.
- **Go-live:** deploy backend and frontend, or push to GitHub ready to deploy.
- Plus the meta-lessons the course hits live: session limits, compacting before big asks, and the 80/20 reality of AI-assisted builds.

### Why it matters
- **The API-key distinction:** your Claude *subscription* authenticates you to Claude Code; an **application** needs its own key, billed separately. Apps must degrade gracefully when that key or quota fails. The course hits this wall live (Gemini quota → OpenRouter fallback → a typo'd key).
- **Scheduling closes the loop** from Part 12: the app stops needing you to click "generate".
- **The 80/20 truth:** AI gets you to ~80% fast; the last 20% — polish, error states, logging, tests — is where the product actually becomes usable.

### How to do it (step by step)
1. **Add the AI feature properly:** put the key in `.env` (never in code), read it via `python-dotenv`, and write the **fallback path first** (deterministic behaviour when the model is unavailable).
2. **Isolate key vs code fast** when it fails (the Part 2 triage): test the key against the provider directly, check the model name exists on that key, check quota, *then* debug code. The course's failure was a single missing character in the key — a "wrong format" error, not a bug.
3. **Wire live data** (e.g. Tavily news search) behind the same fallback discipline; cache or degrade when it fails.
4. **Compact before big asks.** After a long build, `/compact keep the file structure, all API endpoints, the React component structure and the established patterns`. The course's warning shot: one message with a bloated context cost ~$0.10 ⚠️.
5. **Schedule the refresh:** a headless `claude -p` call wrapped in cron, *or* a routine. Apply the Part 12 safety rules — start read-only, write to non-destructive paths, gate anything irreversible, log every run.
6. **Fix the last defects honestly:** mark tasks complete, generate a standup, check the insights page. If something doesn't work (the course leaves a couple of rough edges live), write it into `RETRO.md` rather than pretending.
7. **Write `RETRO.md`:** what the AI got right fast, where the last 20% went, which Part's feature you'd add next (subagents? routines? team review?), and the cost/limit lessons from this build.
8. **Optional go-live:** push to GitHub, deploy backend (e.g. Render) and frontend (e.g. Vercel), and re-check CORS/env vars in the deployed environment.

**Lab 13.4 — Make it live, then schedule it**
- [ ] AI feature works with a real key from `.env`.
- [ ] Graceful fallback verified by removing/breaking the key.
- [ ] Live data feed wired with a failure path.
- [ ] Ran one explicit `/compact` before a large change and noted the cost difference in `/cost`.
- [ ] Scheduled the refresh (cron or routine) with the Part 12 safety checklist applied.
- [ ] `RETRO.md` written.
- [ ] (Stretch) Deployed and verified in production.

**Proof:** the working app with fallback screenshots, the scheduled run's log/output, and `RETRO.md`.

**Quiz 13.4**
1. Why does your app need an API key when you already pay for a Claude subscription?
2. Name three Part 12 safety rules you'd apply to the app's scheduled refresh.
3. The build hit a session limit mid-feature. Give two preventive habits from Parts 5 and 12.

---

## Part 13 wrap-up

| Topic | Done | Lab proof | Quiz |
|---|---|---|---|
| 13.1 Factory setup | ☐ | Spec + CLAUDE.md + prompts | ☐ /3 |
| 13.2 Backend | ☐ | curl evidence per endpoint | ☐ /3 |
| 13.3 Frontend & debugging | ☐ | Screenshots + CORS evidence | ☐ /3 |
| 13.4 AI, scheduling, go-live | ☐ | Fallback + scheduled run + RETRO | ☐ /3 |

**Answers:** `13-answer-key.md` → Part 13.

---

## Course complete — the twelve levers you now own

| Lever | Part | One line |
|---|---|---|
| Model choice | 1, 3 | Match intelligence and cost to the job |
| Terminal access | 1 | The hands that make action possible |
| Agentic loop | 1 | Plan → act → observe → check → retry |
| Permission modes | 3 | How much autonomy, and where |
| CLAUDE.md | 4 | The project's permanent brain |
| Context hygiene | 5 | Keep quality high and cost low |
| Skills | 6 | Reusable procedures, cheap at rest |
| Hooks | 7 | Guaranteed, zero-token automation |
| MCP | 8 | Connections to real tools and data |
| Subagents | 9 | Isolated, focused, cheap workers |
| Agent teams | 10 | Parallel instances that coordinate |
| Plugins | 11 | Package and share the whole setup |
| Scheduling | 12 | Work that happens without you |

**The honest caveat the course ends on:** no project needs all of them. Knowing they exist is the edge — the failure mode is spending hours doing by hand what a hook, skill or subagent would have done automatically.
