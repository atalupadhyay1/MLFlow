# Chapter 5 — Channels: Telegram, WhatsApp & Messaging Your Agent Like a Colleague
*Course section: Configure Telegram & connect with AI agents · Time: ~60 min + Lab 4 (45 min)*

## Learning objectives
- Create a Telegram bot with BotFather and wire it to OpenClaw end-to-end (Lab 4).
- Connect WhatsApp safely (linked-device QR, allowlists) and understand the "two-phone" recommendation.
- Control *who* may talk to your agent: pairing, `allowFrom`, group mention rules.
- Know what other channels exist (Slack, Discord, Signal, iMessage, Teams, Matrix, Zalo, Google Chat) and when you'd pick each.

---

## 5.1 Why channels are a bigger deal than they look
A channel is not "just chat". It's **identity + reachability + trust**: whoever can message the agent can (within its tools) ask it to do things. So this chapter is half *plumbing*, half *bouncers at the door*. Both halves matter equally.

**Channel selection shortcut:**
| Channel | Setup effort | Best for | Note |
|---|---|---|---|
| **Telegram** | Low (bot token) | Learning, personal agents, VM agents (no inbound port!) | Start here — the course does too |
| **WhatsApp** | Medium (QR link) | Personal assistant on your real number's ecosystem | Use a dedicated number if possible |
| Web chat (Control UI) | Zero | Testing | Already used in Labs 1–3 |
| Slack / Discord | Medium (app/bot) | Teams, communities | Group mention rules shine here |
| Signal / iMessage / Teams / Matrix / Zalo / Google Chat | Varies | Specific audiences | Same pairing/allowlist concepts apply |

## 5.2 🧪 Lab 4 — Telegram, from BotFather to "it replies!"
**Time:** 45 min · **Needs:** Gateway running (Ch 3–4), a Telegram account.

**Step 1 — Create the bot (in Telegram):**
1. Open Telegram, search **@BotFather** (verify the blue tick — impostors exist).
2. Send `/newbot`, give it a display name (e.g. "My OpenClaw Assistant"), then a username ending in `bot` (e.g. `my_openclaw_assistant_bot`).
3. BotFather replies with a **token** like `123456789:ABC-…`. Treat it like a password: it *is* full control of your bot. Never post it in screenshots/GitHub (Ch 13 will haunt you otherwise).

**Step 2 — Connect it to OpenClaw.** Either via onboarding/configure, or config:
```json5
channels: {
  telegram: { enabled: true, botToken: "123456789:ABC-…", dmPolicy: "pairing" }
}
```
Prefer storing the token via environment variable / `openclaw configure` prompts over committing it to files you might share. Then:
```bash
openclaw gateway restart
openclaw gateway status
```

**Step 3 — Pair (the bouncer does his job):**
1. Open your new bot in Telegram, send `/start` or any hello.
2. With `dmPolicy: "pairing"`, the first message from an unknown sender creates a **pairing request** rather than letting them in.
3. Approve it (dashboard Channels area, or the pairing approval flow shown in your version's UI/logs — check `docs.openclaw.ai/channels/pairing` for the exact click path in your build).
4. Message again: *"Hello! Introduce yourself in one line."*

**✅ Lab 4 checkpoint:** Your phone now holds a conversation with an agent running on your machine/VM. That little buzz in your pocket is the whole course in miniature — everything else is making that agent more capable, more scheduled, and safer.

**Step 4 — Groups (optional, do it consciously):** Add the bot to a group only with **mention rules** (e.g. respond when `@botname` or a mention pattern matches). An agent that answers *every* group message is annoying within an hour and expensive within a day. In config this lives under the agent/channel group settings (e.g. `requireMention: true` for groups).

## 5.3 WhatsApp — the personal-assistant classic
OpenClaw's WhatsApp is an on-demand plugin using WhatsApp Web-style linking:

```bash
openclaw channels login            # shows QR (choose WhatsApp if prompted)
openclaw gateway --port 18789      # if gateway not already running
```
Scan with WhatsApp → Settings → Linked Devices → Link a Device.

**The two-phone setup (recommended, from official guidance):** Your personal number messages a **dedicated assistant number** (second SIM/eSIM/old phone). Why? Clean separation, the agent never impersonates *you* from your own number, and you can cut access instantly. Then lock it down:

```json5
channels: { whatsapp: {
  allowFrom: ["+919999999999"],        // ONLY your number may DM the agent — never run open-to-the-world
  groups: { "*": { requireMention: true } }
}}
```
(`+91…` is just an example — use your own international format.) Rules: `allowFrom` always set; groups mention-only; test by messaging from a non-listed number and confirming *no* reply.

## 5.4 Sessions per channel (connecting back to Ch 2)
With `session.scope: "per-sender"`, your Telegram-you and WhatsApp-you can hold separate threads unless you design otherwise. Reset triggers (`/new`, `/reset`), daily reset hour, and idle timeout live under `session` config — tune them deliberately in Ch 8 rather than inheriting mystery behaviour.

## 5.5 Channel troubleshooting field guide
| Symptom | Check first |
|---|---|
| BotFather token rejected | Copied with spaces? Bot created by the *real* BotFather? Token revoked via `/revoke`? |
| Telegram bot silent | Gateway up? Channels status green? Pairing approved? Token in *this* config (not your laptop's, if agent is on VM)? |
| WhatsApp disconnected | Linked device removed on phone / plugin needs re-login: `openclaw channels login` |
| Agent replies to everyone in group | Mention rule missing — set `requireMention` for groups |
| Stranger got a reply | `dmPolicy` too open — set `pairing` + `allowFrom`, restart, re-test |

## ✅ Checkpoint
- [ ] Telegram bot replies to *you*, ignores (or pairing-gates) a second account/friend test.
- [ ] (If doing WhatsApp) QR linked, `allowFrom` set, non-listed number test passed.
- [ ] You can state your channel trust model in one sentence: *"Only ___ can DM; groups need ___."*

## 🎯 Self-check
1. Why is Telegram ideal for a cloud VM? → *Bot polls outbound — no inbound port to open.*
2. What does `dmPolicy: "pairing"` actually buy you? → *Unknown senders request access instead of getting it.*
3. WhatsApp's single most important safety setting? → *`allowFrom` with only your number(s).*

**→ Next: [Chapter 6 — The Workspace: Personality, Identity & Memory](06-workspace-persona-memory.md)**
