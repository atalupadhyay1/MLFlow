# Chapter 4 — The Gateway & Web Interface (Control UI) in Depth
*Course section: Master the OpenClaw web interface · Time: ~60 min + Lab 3 (30 min)*

## Learning objectives
- Operate the Gateway confidently: start/stop/status/logs, foreground vs service.
- Use every important area of the **Control UI** (dashboard): chat, agents, channels, skills, sessions, config.
- Trace one message through the UI/logs (Lab 3) and read config without fear.

---

## 4.1 Gateway operations — your daily verbs

```bash
openclaw gateway status     # is it up? which port? which config?
openclaw gateway install    # (re)register as OS service (launchd / systemd / Scheduled Task)
openclaw gateway restart    # after config changes
openclaw gateway stop
openclaw gateway --port 18789   # foreground: live logs, Ctrl+C stops (debugging gold)
openclaw dashboard          # open Control UI
openclaw doctor             # health checks
openclaw configure          # revisit onboarding settings later — kinder than editing JSON cold
```

**Foreground vs daemon — when each?** Daemon for real life (survives reboots/logouts). Foreground when something's wrong: the logs stream right in front of you while you reproduce the issue. Professionals alternate without thinking; now you will too.

## 4.2 Control UI tour (open `openclaw dashboard` and click along)

| Area | What it's for | Beginner mission |
|---|---|---|
| **Chat** | Talk to the agent (web channel) | Send a message; try `/new`, then ask "what did we discuss before?" — feel the session reset |
| **Agents** | Your agent(s): model, workspace, identity | Confirm which model is *actually* live (never assume) |
| **Channels** | WhatsApp/Telegram/Discord… connection status | Note statuses are red/green truth — check here first when "it doesn't reply" |
| **Sessions** | Active conversation sessions & resets | Find your chat session; note its key/scope |
| **Skills** | Installed skills & enable/disable | Just look today; Ch 7 makes it home |
| **Config** | View/edit gateway config | Find `channels`, `gateway.auth`, `agents.defaults` — match them to Ch 2 §2.6 |
| **Logs** (where exposed) | What the Gateway saw & did | Lab 3 below lives here + foreground mode |

> 💡 **Habit that separates pros:** When anything misbehaves, the order is **Channels status → Logs → Config → Doctor**. UI first, terminal second, guessing never.

## 4.3 🧪 Lab 3 — Gateway detective (trace one message)
**Goal:** See §2.1's diagram happen live. **Time:** 30 min. **Needs:** Ch 3 complete.

1. Terminal 1: stop the daemon copy and run foreground so logs stream:
   ```bash
   openclaw gateway stop; openclaw gateway --port 18789
   ```
   *(If your install resists stopping the service, just open the dashboard logs instead — the observations matter, not the method.)*
2. In the Control UI chat, send: `Search the web for today's date and tell me one headline.` (any prompt that forces a tool).
3. In the logs, hunt for the sequence: **channel intake → session → model request → tool call (web search) → tool result → final reply.**
4. Write in your journal: the model's name, the tool name, and roughly how many model round-trips it took. (Most first-timers are surprised it's 2–3, not 1 — that's the agent loop, and that's your API bill. Remember this in Ch 13.)
5. Restart properly: Ctrl+C, then `openclaw gateway install` (if needed) + `openclaw gateway status`.

**Expected outcome:** You can narrate your own screenshot of logs using the words *channel, gateway, session, model, tool*. **If stuck:** ask the agent itself in chat: "Which tools do you have?" — its answer reveals the tool catalogue it was given.

## 4.4 Config editing without tears

- Prefer `openclaw configure` or the dashboard's config editor for guided changes.
- Hand-editing `~/.openclaw/openclaw.json`: **back it up first** (`cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak`), change ONE thing, `openclaw gateway restart`, verify. One change at a time is the difference between "configuration" and "archaeology".
- JSON5 is tolerated in docs examples (comments, trailing commas) — real files should stay clean JSON unless your version documents otherwise. When in doubt, validate by restarting and reading the first error line; it names the field.

## 4.5 Multi-agent awareness (preview of Ch 14)
One Gateway can host several agents (e.g. `main` assistant + a `sysadmin` agent) each with its own workspace, model, and channel routing. Today just notice `agents.entries` exists in config. We build a second agent properly in Chapter 14 — mentioning it now so the config never looks alien.

## ✅ Checkpoint
- [ ] You can start/stop/status the Gateway both ways (service + foreground).
- [ ] Lab 3 done; journal has model + tool + round-trip count.
- [ ] You located model, channels, and auth settings in the Control UI.

## ⚠️ Common traps
| Trap | Antidote |
|---|---|
| Edited config, "nothing changed" | You didn't restart: `openclaw gateway restart` |
| Dashboard opens, chat errors | Check provider key/billing (Ch 3) and Agents → model |
| Two Gateways fighting (port in use) | `openclaw gateway status`; stop the stray foreground one (Ctrl+C its terminal) |
| Changed workspace path, agent "lost personality" | Personality lives in workspace files — point config back or copy files (Ch 6) |

## 🎯 Self-check
1. Fastest path when the agent goes silent? → *Channels status → logs → config → doctor.*
2. Why run foreground mode at all? → *Live logs while reproducing a bug.*
3. One config change at a time + restart + verify — why? → *So you always know which change caused which effect.*

**→ Next: [Chapter 5 — Channels: Telegram, WhatsApp & Messaging Your Agent](05-channels-telegram-whatsapp.md)**
