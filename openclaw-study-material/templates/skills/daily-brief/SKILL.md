---
name: daily-brief
description: Use when the user asks for a morning briefing, daily digest, news update, or when the scheduled brief fires. Searches the user's USER.md topics from the last 24h, dedupes against recent briefs, and returns a short sourced brief.
---

# Daily Brief

## Steps
1. Topics = USER.md "Briefing topics" (phrases + ignore terms). None set → ask once, save there.
2. Per topic: web_search (last 24h; 48h on Mondays), web_fetch top 2–3 results. Primary sources preferred.
3. Dedupe by EVENT (not just URL) against yesterday's brief/headlines in memory notes.
4. Keep max 7 items overall. Each: `• <headline> — <one-line summary>. Why it matters: <tie to USER.md context>. <URL>`
5. Store today's headlines (title + URL) in today's memory note for tomorrow's dedupe.
6. Format: `☀️ Your brief (<date>)` headline, grouped bullets, close with `Watching: <1 pending thread>`.
7. Quiet day → exactly: `Quiet morning — nothing needs you.`

## Guardrails
- Summarise ONLY fetched text, never search snippets alone. No citation = not included.
- Under 200 words unless explicitly asked for more. No speculation presented as news.
