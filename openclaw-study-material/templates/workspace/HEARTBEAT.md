# HEARTBEAT.md — Periodic Checks (template)
*Keep tiny. Every item needs a silence condition, or this file becomes an expensive parrot.*
*Tip: an empty/comment-only file = heartbeat makes no API call. Start there; grow deliberately.*

- Run the sysadmin-check skill for the main VM. Alert ONLY if any check is 🔴 or disk > 90%.
  Otherwise reply HEARTBEAT_OK.
- If a calendar event starts within 2 hours and the user hasn't been reminded, remind once.
  Otherwise reply HEARTBEAT_OK.
- Never send chatter, summaries, or "just checking in" messages.
