# Part 08 — MCP: connecting Claude to the outside world
**Video:** 6:49:12 – 8:20:17 (Module 8)

**In this part:** 8.1 What & why (connectors vs MCP) · 8.2 Connecting a server · 8.3 Building your own

---

## 8.1 MCP: what it is and why it exists

### What it is
- **MCP (Model Context Protocol)** is an **open standard** defining how AI agents communicate with external tools and data sources.
- Architecture in one line: **Claude Code is the client; an MCP server exposes tools; the protocol is the contract between them.**
- The course's mental model: **a toolbox you don't have to build or maintain.** Instead of writing and fixing custom glue for Gmail, Slack, GitHub, a database and a browser, you connect to a server that already exposes them.
- **Connectors vs MCP:**
  - *Connector* — a ready-made integration surfaced inside Claude products (turn on Gmail, done). Convenient, curated, limited.
  - *MCP* — the open protocol you configure yourself. More work, any server anyone publishes, works everywhere MCP is supported.

### Why it matters
- Without MCP, every integration is bespoke and every upstream API change breaks your code. With MCP, the **server maintainer** absorbs that.
- It's what turns "Claude knows about your tools" into "Claude *uses* your tools": read email, open PRs, query a database, drive a browser.
- ⚠️ **Every connected server has a context cost**: its tool descriptions go into the window on every request. More servers ≠ more capability; it can be *less*, because overlapping tools confuse selection (the course demonstrates exactly this with search vs research tools).

### How to do it (step by step)
1. **Inventory the integrations you actually need** (not "might be cool"): email, code host, chat, search, browser, database.
2. For each, decide **connector vs MCP**: if a curated connector exists in your Claude surface and covers the need, use it; use MCP for everything else or when you need it inside Claude Code.
3. Understand the shape you'll be configuring — a server exposes **tools** with names, descriptions, and JSON-schema parameters. Example (Tavily): `search`, `extract`, `crawl`, `map`, plus a heavier `research`.
4. Note the **cost profile** of each tool: `search` in the course's demo used ~1 credit; `research` burned ~250 credits on one query. Know before you fire.
5. Write your MCP policy in one line: *"Only servers I used this week stay enabled."*

**The toolbox analogy, precisely**
> You don't forge your own hammer for every job and fix it when it bends. You connect to a workshop that supplies hammers, and you spend your time building.

**Lab 8.1 — Choose, don't collect**
- [ ] Listed the integrations your real work needs.
- [ ] Marked each as connector-eligible or MCP-required.
- [ ] Picked exactly **one** to connect first, and wrote why.
- [ ] Noted its tools and their cost/quota profile from the provider's docs.

**Proof:** your inventory table with one chosen server and its tool/cost notes.

**Quiz 8.1**
1. Define MCP in one sentence and name the example the course uses for it.
2. What is the practical difference between a connector and an MCP server?
3. Why can adding more MCP servers make Claude *worse* at using tools?

---

## 8.2 Connecting a server, step by step

### What it is
- Servers come in two flavours:
  | | **Local (stdio)** | **Hosted / remote (HTTP·SSE)** |
  |---|---|---|
  | Runs on | your machine as a process | provider infrastructure |
  | Config | command + args | URL (+ headers/API key) |
  | Resources | your CPU/RAM (small VMs struggle) | theirs |
  | Great for | file access, browser automation, private tools | Gmail, Slack, Tavily, GitHub |
- Configuration lives in **`.mcp.json`** (project root) or `.claude/.mcp.json`, with **scopes**:
  - **project** — committed, shared with the team,
  - **user** — your account, all projects,
  - **local** — private, not committed (the place for personal keys).
- Secrets always come from **environment variables**, never literals.
- `/mcp` lists servers, shows tools, and handles authentication.

### Why it matters
- Scopes are a security boundary: a shared repo should not carry your personal credentials, and a team tool should not be trapped on one laptop.
- Local vs hosted determines where your resources and failure modes live — a local browser server on a small machine will crash; a hosted server will fail on auth/credits instead.
- Context cost again: enable in `settings.json` (`enabledMcpjsonServers`) only what you want loaded.

### How to do it (step by step)
1. Get the server's setup instructions from its provider and note whether it's local or hosted.
2. Create/verify the key as an environment variable:
   ```bash
   export TAVILY_API_KEY="…"     # add to your shell profile
   ```
3. Add the server to `.mcp.json`:
   ```json
   {
     "mcpServers": {
       "tavily-remote-mcp": {
         "type": "http",
         "url": "https://mcp.tavily.com/mcp/",
         "headers": { "X-API-Key": "${TAVILY_API_KEY}" }
       }
     }
   }
   ```
4. **Choose the scope deliberately**: team tools → project `.mcp.json`, committed; personal keys → local/private file (not committed). Confirm `.gitignore` covers anything sensitive.
5. Pre-approve in settings if you're confident:
   ```json
   { "enabledMcpjsonServers": ["tavily-remote-mcp"] }
   ```
6. Restart the session, then `/mcp` → authenticate → confirm the tool list appears.
7. **Use it and watch the difference:** ask a question that forces a tool call, and compare the raw result with Claude's summarised answer. The raw JSON is ugly; the model's rewrite is the product.
8. If a request fails, run the triage: is it auth, credits/quota, model/tool availability, or network? (Same discipline as 2.2.)

### Troubleshooting table
| Symptom | Likely cause |
|---|---|
| Server doesn't appear in `/mcp` | Wrong file/scope, malformed JSON, session not restarted |
| Tools appear but calls fail | Missing/invalid API key env var |
| Only some tools work | Provider quota/plan limits specific tools |
| Claude picks the wrong tool | Overlapping tools (search vs research) — name the tool explicitly |
| Machine slows to a crawl | A local server (e.g. browser automation) is resource-heavy |

**Lab 8.2 — Connect one real server**
- [ ] Created the API key as an environment variable.
- [ ] Added the server to `.mcp.json` in the correct scope.
- [ ] Confirmed it with `/mcp` and listed its tools.
- [ ] Ran one real query through it and captured the raw-vs-summarised difference.
- [ ] Wrote your troubleshooting one-liner for "server not showing up".

**Proof:** the config file (with `${ENV_VAR}` placeholder, no secrets), the `/mcp` tool list, and one successful call.

**Quiz 8.2**
1. When would you choose a local server over a hosted one? Give one example of each.
2. Where do API keys belong in an MCP config, and where should they never appear?
3. Your teammate's server works; yours doesn't appear in `/mcp`. List three checks in order.

---

## 8.3 Building your own MCP server

### What it is
- A server exposes **tools**: functions with a **name**, a **description**, and a **JSON-schema parameter list** (types, required fields).
- The course builds a small **calculator server** live: `add`, `subtract`, `multiply`, `divide`, `power`, `square_root`, `average`, plus `list_tools` / `call_tool` plumbing.
- Registration is the same as any other server — add it to `.mcp.json`, restart, and it appears.
- Functions can be arbitrarily complex, including calling an LLM inside. The protocol doesn't care.

### Why it matters
- **The description is the prompt for tool selection.** The model reads names, descriptions and schemas to decide whether and how to call a tool — writing them well is prompt engineering.
- Building one demystifies the whole ecosystem: after ten minutes of building a calculator, every hosted server's behaviour makes sense.
- It's how you expose *internal* capabilities — your own APIs, data stores, or company systems — to any MCP-compatible agent.

### How to do it (step by step)
1. Ask Claude Code to scaffold a minimal server, or write it yourself:
   > *"Create a simple Python MCP server that exposes arithmetic tools: add, subtract, multiply, divide, power, square_root, average."*
2. Read the generated code and identify the three parts of each tool: **name**, **description**, **parameter schema**.
3. **Improve the descriptions** — add units, constraints, and when to use each tool (e.g. "use `average` for a list of numbers; requires at least one value").
4. Register it in `.mcp.json` (local scope is fine for a private tool), restart the session, and confirm the tools appear in `/mcp`.
5. Test through Claude: *"use the calculator MCP to compute 5 + 9"* → observe the tool call and the result.
6. Test the **description effect**: make two tools sound ambiguous ("calculate" and "compute"), then try a request and see the confusion. Fix the descriptions. This lesson is the whole point.
7. Decide where it lives long-term: personal `~/.claude` scope for yourself, or a small repo + project scope for the team.

**Lab 8.3 — Ship a tiny server you understand**
- [ ] Scaffolded a server with at least four tools.
- [ ] Reviewed and improved every tool description.
- [ ] Registered it and called one tool through Claude.
- [ ] Reproduced and fixed one tool-selection ambiguity.
- [ ] Decided its scope and documented how to start it.

**Proof:** the server file, the `/mcp` tool list including your tools, and a successful computed answer.

**Quiz 8.3**
1. What three pieces of information does a tool expose to the model, and which is effectively a prompt?
2. Why does a badly described tool cause wrong tool selection even when the code is perfect?
3. You want your team to use your internal "leave balance" API from Claude Code. Outline the four steps.

---

## Part 08 wrap-up

| Topic | Done | Lab proof | Quiz |
|---|---|---|---|
| 8.1 What & why | ☐ | Inventory + one chosen server | ☐ /3 |
| 8.2 Connecting | ☐ | Config + tool list + call | ☐ /3 |
| 8.3 Building your own | ☐ | Working server + computed result | ☐ /3 |

**Answers:** `13-answer-key.md` → Part 08.
**Next:** `09-subagents.md` — isolated specialists that keep your context clean.
