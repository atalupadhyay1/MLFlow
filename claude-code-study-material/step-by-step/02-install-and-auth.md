# Part 02 — Install & authenticate
**Video:** 0:33:08 – 1:22:17 (Module 2)

**In this part:** 2.1 Installing on macOS/Linux/Windows · 2.2 Authenticating · 2.3 Running your way (desktop, IDE, trust, sessions)

> The course spends a lot of time here on purpose: most people quit at their first install error. Treat this part as *"install, then prove you can recover when it breaks."*

---

## 2.1 Installing Claude Code on macOS, Linux and Windows

### What it is
- Claude Code is installed by running a **command in your terminal**, not by double-clicking a setup file. The installer fetches a script, downloads what it needs, and registers the `claude` command.
- Three ways exist in practice:
  1. **Native terminal install** — the recommended, universal path.
  2. **Inside Claude Desktop** — a Claude Code tab appears for paid plans; pick a folder and go. GUI, but it hides the mechanics.
  3. **Inside an IDE** (VS Code and forks) — Claude Code in a panel with editor context.

### Why it matters
- Claude Code needs to live *on your machine* to have hands. A web page cannot run your shell.
- The Windows story is where most people stumble: **the install command differs by shell** (PowerShell vs CMD), and tutorials usually assume Unix-like behaviour.
- Knowing the three routes means you always have a fallback: if the CLI misbehaves, the desktop app can still get you working while you diagnose.

### How to do it (step by step)
1. Open the **official quickstart/installation docs** and find the section for your OS. Do not copy install commands from random blogs — versions drift. ⚠️
2. **macOS / Linux:** open Terminal and run the provided install command. Let it finish; it may look idle while downloading.
3. **Windows:** decide your shell first.
   - PowerShell route: run the PowerShell command exactly as documented.
   - CMD route: run the CMD command exactly as documented.
   - If you want the Unix-like experience most tutorials assume, install **Windows Terminal** from the Microsoft Store first and use that from now on.
4. Close and reopen your terminal so the new `claude` command is on your PATH.
5. Verify: run `claude --version` (or start `claude` and check `/status`).
6. If you hit an error, work the triage list in the Lab before reinstalling.

### Common failure modes (use this as your checklist)
| Symptom | First move |
|---|---|
| `claude: command not found` | New terminal; PATH not refreshed |
| Install seems frozen | It's downloading — wait; don't run it twice in parallel |
| Works in PowerShell, not CMD (or vice versa) | You installed for one shell and opened the other — match them |
| Exit code 1 immediately after install | Stale/mismatched install — perform a clean reinstall |
| Auth loop | See 2.2 |

**Lab 2.1 — Install on your OS (and break it once)**
- [ ] Installed Claude Code natively for your OS using the official command.
- [ ] Confirmed with `claude --version` / `/status` in a **new** terminal.
- [ ] Deliberately triggered (or simulated) one failure above and fixed it using the table.
- [ ] Wrote your personal install notes: OS, shell, exact command used, error seen, fix.

**Proof:** your install notes, plus Claude Code starting successfully in a fresh terminal.

**Quiz 2.1**
1. Why does Claude Code need to be installed rather than used purely from the web?
2. Your Windows install works in PowerShell but not CMD. What happened?
3. After installing, your new terminal still can't find `claude`. Give the two most likely causes and the fix order.

---

## 2.2 Authenticating: subscription, API key, third-party platforms

### What it is
- Two mainstream ways to pay for Claude Code usage:
  - **Subscription** (Claude Pro/Max): Claude Code draws from your plan's usage limits. `/login` with your account; `/logout` signs out.
  - **API key**: pay-per-token against console credentials. Required if you want usage outside a subscription and for programmatic/headless runs (Part 12).
- **Third-party platforms** exist as resellers/alternatives for model access. The course demonstrates one: cheaper or alternative access, but more moving parts and different failure modes.
- ⚠️ Prices, limits and plan names at recording time: Pro ≈ $20/month tier, Max ≈ $100/month tier.

### Why it matters
- It determines **what you can do when limits hit**: subscription users wait or top up; API users pay and continue.
- **Your app is not your session.** A subscription authenticates *you* to Claude Code; an application you build needs its own **API key**, billed separately. The capstone (13.4) hits this wall live.
- Third-party platforms are a real option but a real risk: key format mistakes, decommissioned models, quota surprises. You want to learn to isolate "key problem" from "code problem" fast.

### How to do it (step by step)
1. Decide your billing path:
   - *Learning and daily use, already on a plan?* Use **subscription**: `claude` → `/login` → complete browser auth → `/status` to confirm.
   - *Need headless/automation or no subscription?* Create an **API key** in your console and authenticate with it (the CLI offers an API-key login path).
2. Verify you're authenticated correctly: `/status` shows account/plan; ask one question to confirm a working model call.
3. Test sign-out/sign-in once, so you know the flow: `/logout`, then `/login`.
4. **If you use a third-party platform:** create the key, check the provider's **model list** first, confirm the model you intend to use is available on that key, and only then wire it up.
5. Keep keys in an environment variable (e.g. `export MY_PROVIDER_KEY=...`) rather than typing them into files you might commit.
6. Write down where your usage comes from and what happens at the limit — you'll need both facts in Part 12.

### Diagnosing auth errors (the 90-second triage)
1. Is it a **key** problem or a **code** problem? Test the key against the provider's own endpoint/model list first.
2. Check **key format** (providers validate prefixes; a single missing character gives an auth error, not a code error).
3. Check **model availability** on that key — "model not found" is not "code broken".
4. Check **quota/credits** before assuming a bug.
5. Only then debug your code.

**Lab 2.2 — Authenticate and prove recovery**
- [ ] Authenticated with your chosen method; `/status` confirms it.
- [ ] Asked one question and got an answer (proves the model call path works).
- [ ] If using a provider key: verified the model exists on your key's model list.
- [ ] Recorded your usage source + what happens at the limit + your 5-step triage.

**Proof:** `/status` output, plus your triage notes.

**Quiz 2.2**
1. What's the practical difference between a subscription and an API key for Claude Code?
2. Your app returns an authentication error to users. Why is "top up my Claude subscription" the wrong instinct?
3. Give two signals that an error is a *key* problem rather than a *code* problem.

---

## 2.3 Running your way: desktop app, IDEs, trust and where sessions live

### What it is
- **Claude Desktop** can host Claude Code for paid accounts: open a folder, click the Claude Code tab, accept the trust prompt, chat. A GUI over the same engine.
- **IDEs** (VS Code/forks) run Claude Code in a panel with editor context — convenient when you're editing anyway.
- **The trust prompt** is the real security boundary: proceeding means Claude Code may **read, write and execute** in that folder.
- **Sessions live on disk** under `~/.claude/` (per-project folders). That's what makes `/resume` and rewind possible — and what you'd inspect when something looks lost.

### Why it matters
- Trusting a folder is a real decision, not a formality: a folder containing bank statements and credentials is now readable by an agent that can also execute code.
- Knowing sessions are on disk removes the fear of "losing my context" and enables the Part 5 hygiene tactics (status files, resuming deliberately).
- The desktop/IDE routes are your fallbacks when the terminal install is unhappy — and they teach the same concepts.

### How to do it (step by step)
1. **Try the desktop route:** open Claude Desktop → Claude Code tab → choose a *throwaway* folder (e.g. `~/claude-sandbox`) → read the trust prompt carefully → proceed.
2. Ask it to do something small ("create hello.txt with a greeting"), then find `hello.txt` in your file manager. The GUI is doing exactly what the CLI does.
3. **Try the IDE route** if you have VS Code: open the sandbox folder, start Claude Code from the panel, and notice the editor context it has (open file, selection).
4. **Find your sessions:** open a terminal and explore `~/.claude/` (`ls -la ~/.claude`, then look for `projects/`). Open one project's session folder and note how conversations are stored.
5. Resume something: in Claude Code, `/resume`, pick an earlier session, confirm it comes back.
6. Decide (and write down) which surface you'll use for what — e.g. CLI for real work, desktop for quick lookups.

### Trust checklist (run this before clicking "trust")
- What is in this folder? Any secrets, keys, `.env`, client data?
- Is it under git, so damage is recoverable?
- Which permission mode will I use here (see 3.4)?
- Do I understand that "execute" means running code I may not read line-by-line?

**Lab 2.3 — Trust, GUI vs CLI, and session archaeology**
- [ ] Ran a task in the desktop or IDE surface in a throwaway folder.
- [ ] Inspected `~/.claude/` and located a session for one project.
- [ ] Used `/resume` to reopen a past session.
- [ ] Wrote your personal rule for which folders you trust and which you don't.

**Proof:** the GUI-created file, a described session folder path, and your trust rule in one or two lines.

**Quiz 2.3**
1. What are you actually granting when you accept the trust prompt, and why is it a security decision?
2. Where does Claude Code keep session history, and which command uses it?
3. Which surface would you use while debugging a broken CLI install, and why is that a legitimate path rather than a workaround?

---

## Part 02 wrap-up

| Topic | Done | Lab proof | Quiz |
|---|---|---|---|
| 2.1 Install | ☐ | Install notes + working CLI | ☐ /3 |
| 2.2 Authenticate | ☐ | `/status` + triage notes | ☐ /3 |
| 2.3 Running your way | ☐ | GUI file + session path + trust rule | ☐ /3 |

**Answers:** `13-answer-key.md` → Part 02.
**Next:** `03-commands-and-modes.md` — the daily control panel.
