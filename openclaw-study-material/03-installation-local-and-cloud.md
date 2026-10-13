# Chapter 3 — Installation: Local Machine, Azure, GCP & AWS
*Course section: Install, configure & deploy OpenClaw · Time: ~60 min local · +60 min per cloud path (pick one first!)*

## Learning objectives
- Install OpenClaw locally and complete onboarding without fear.
- Deploy the same setup onto **Azure, GCP, or AWS** (the course covers all three — you only need one to follow along; read the others comparatively).
- Install the Gateway as a background service and verify it like a professional: `status`, `doctor`, `triage`, dashboard.

> 🛑 **Golden rule of this chapter:** Get it working on your laptop first, *then* lift the identical config to the cloud. Debugging on a VM over SSH while also learning OpenClaw doubles your pain for no benefit.

---

## 3.1 Prerequisites (check, don't assume)

| Need | Why | Check |
|---|---|---|
| Node.js **22+** (26 recommended by official docs; Node 24 also fine) | OpenClaw runtime | `node --version` |
| npm (comes with Node) | Installs the CLI | `npm --version` |
| An LLM route | The brain | API key (Anthropic/OpenAI/…) *or* existing Claude Code / Codex login |
| (Cloud labs) an Azure/GCP/AWS account | Your always-on home | Free-tier accounts work |

Install Node if missing: use your OS package manager, nvm, or simply let the official installer handle it (below).

## 3.2 Path A — Local install (everyone starts here) · 🧪 Lab 1

**Why this way:** The official installer detects your OS, installs Node if needed, installs the CLI, and launches onboarding.

```bash
# macOS / Linux — official one-liner
curl -fsSL https://openclaw.ai/install.sh | bash

# Windows (PowerShell) — official one-liner (or use the Windows Hub app / WSL2; WSL2 behaves like Linux)
iwr -useb https://openclaw.ai/install.ps1 | iex

# Alternative (any OS, if you prefer npm directly)
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

**Onboarding, question by question (what it's really asking):**
1. **Quick Start vs Custom setup** — Quick Start reuses detected AI access (Claude Code/Codex login or existing key) and opens the dashboard. Choose **Custom setup** the first time so you *see* every choice; you can't debug what the wizard hid from you.
2. **Model provider** — paste your API key when prompted (it verifies with a real completion — a failure here = key/billing issue, fix it now, not later).
3. **Gateway** — accept local mode, token auth, port **18789**.
4. **Daemon/service** — say yes (`--install-daemon`): LaunchAgent (macOS) / systemd user unit (Linux/WSL2) / Scheduled Task (Windows). This is what makes it "always-on".
5. **Channel** — skip for now; Chapter 5 does Telegram properly. Web chat is enough for Lab 1.

**Verify like you mean it:**
```bash
openclaw --version
openclaw gateway status     # expect: listening on 18789
openclaw dashboard          # opens the Control UI in your browser
```
Send "Hello! What can you do?" in the Control UI chat. **✅ Lab 1 checkpoint: you get a sensible AI reply.** Screenshot it — it's your "day one" memory; the Capstone asks for it.

**If onboarding gets messy:**
```bash
openclaw doctor   # read-only health checks you can read yourself
openclaw triage   # sanitised diagnosis; can hand findings to a coding agent — nothing leaves your machine until you choose
openclaw gateway --port 18789   # foreground mode: watch live logs while you retry
```

## 3.3 The cloud idea (read before touching any console)

Why deploy at all? Your laptop sleeps; an agent that briefs you at 8 AM cannot. A small always-on VM = your agent's home. The course deploys to **Azure, GCP and AWS**; all three follow the *same 6-step pattern* — only the console buttons differ:

```
1. Create small Linux VM (Ubuntu, 1–2 vCPU / 2–4 GB RAM to start)
2. Lock it down (SSH keys only, firewall: SSH from your IP; Gateway stays on loopback)
3. Install Node 22+ → install OpenClaw → onboard (or copy ~/.openclaw from laptop)
4. Install Gateway as service (systemd) so it survives reboot
5. Reach the dashboard safely (SSH tunnel — never open 18789 to the world)
6. Connect channels (Telegram needs no inbound port — perfect for VMs)
```

> 🔐 **Non-negotiable:** The Gateway dashboard is an admin panel. On every cloud: bind `loopback`, use token auth, and view it through an SSH tunnel:
> `ssh -L 18789:127.0.0.1:18789 user@YOUR_VM_IP` → then browse `http://127.0.0.1:18789` locally. Anyone who skips this eventually features in a security blog post.

## 3.4 Path B — Azure (course path 1)

1. **Create VM:** Azure Portal → Virtual machines → Create. Ubuntu Server LTS, size B1s/B2s-class (free-tier eligible where available), authentication = **SSH public key**, username noted.
2. **Networking:** Inbound rules: allow SSH (22) **from your IP only**. Do *not* add 18789.
3. **Connect:** `ssh -i yourkey.pem azureuser@VM_PUBLIC_IP`
4. **Install:**
   ```bash
   curl -fsSL https://openclaw.ai/install.sh | bash
   openclaw onboard --install-daemon     # or the classic wizard: openclaw onboard --classic
   openclaw gateway install              # ensure service registration
   openclaw gateway status
   ```
5. **Dashboard:** SSH-tunnel per §3.3, open the Control UI, confirm model + workspace.
6. **Make it survive:** `systemctl --user status openclaw*` (verify the user service), enable lingering if your VM needs the user service after logout: `sudo loginctl enable-linger $USER`.

## 3.5 Path C — Google Cloud Platform (course path 2)

1. **Create VM:** Compute Engine → Create instance. `e2-micro`/`e2-small`, Ubuntu LTS boot disk, your region.
2. **Firewall:** default VPC rules already restrict; add/verify SSH only; never create a rule for 18789.
3. **Connect:** `gcloud compute ssh INSTANCE --zone=ZONE` (or SSH button in console).
4. **Install & verify:** identical commands to Azure §3.4 steps 4–6.
5. **Costs:** `e2-micro` free tier exists in specific US regions — check current terms; set a **billing alert** (Billing → Budgets) before you fall in love with the VM.

## 3.6 Path D — AWS EC2 (course path 3)

1. **Launch:** EC2 → Launch instance. Ubuntu Server LTS, `t3.micro`/`t2.micro`, create/select **key pair** (download the `.pem`, `chmod 400` it).
2. **Security group:** SSH 22 from *My IP* only. Nothing else inbound.
3. **Connect:** `ssh -i key.pem ubuntu@PUBLIC_DNS`
4. **Install & verify:** same as §3.4 steps 4–6. Dashboard via SSH tunnel.
5. **Costs:** free-tier hours are finite and per-account; stop (not just close laptop!) test instances, set an AWS Budgets alert.

## 3.7 Copying your laptop setup to the cloud (the satisfying shortcut)

Once local works, replicate instead of re-onboarding:
```bash
# from laptop (contains config + workspace + memory — contains secrets too, transfer carefully!)
scp -r ~/.openclaw user@VM_IP:~/
ssh user@VM_IP "openclaw gateway restart && openclaw gateway status"
```
Then re-check channel logins (WhatsApp may need a fresh QR — Ch 5) and rotate any key you wouldn't want on a server (Ch 13).

## ✅ Chapter checkpoint (Lab 2)
- [ ] Local: `openclaw gateway status` healthy, dashboard chat replies.
- [ ] Cloud (one provider): VM created with SSH-only firewall; OpenClaw installed; service running; dashboard reached ** via tunnel only**.
- [ ] You can explain *why* 18789 is never opened publicly, in one sentence.

## ⚠️ "It broke, now what?"
| Symptom | Fix order |
|---|---|
| `node: command not found` / wrong version | Re-run installer, or install Node 22+ via nvm: `nvm install 22 && nvm use 22` |
| Onboarding model test fails | Wrong/expired key, no billing, or region block — test the key with the provider directly |
| Dashboard won't load on VM | Gateway status → tunnel command correct? → `bind: loopback` means *tunnel is the way*, that's expected |
| Service dies on logout (VM) | `sudo loginctl enable-linger $USER`, then `openclaw gateway restart` |
| Everything's on fire | `openclaw doctor` → `openclaw triage` → read output slowly. In that order. |

## 🎯 Self-check
1. Quick Start vs Custom setup — which for a first-timer and why? → *Custom: you see every decision you'll later debug.*
2. Your friend opened port 18789 publicly "to use the dashboard from anywhere". Your one-sentence reply? → *(Something like) "You've published an admin panel that can run shell commands — tunnel instead."*
3. Which 3 commands verify any install? → *`gateway status`, `doctor`, dashboard chat.*

**→ Next: [Chapter 4 — Gateway & the Web Interface (Control UI)](04-gateway-web-ui-and-config.md)**
