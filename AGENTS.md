# Agents

Skills for this project live in `.agents/skills/` — a tool-neutral location shared across Claude
Code and Codex, so the same skill is used by both without copying it. Each subdirectory is one skill
with a `SKILL.md` at its root:

- `.agents/skills/llm-wiki-lite/` — the script-free, hand-driven variant (default). See its `README.md`.
- `.agents/skills/llm-wiki/` — the full, scripted wiki pipeline. See its `README.md`.

**At the start of every session, read `.agents/skills/llm-wiki-lite/SKILL.md` and `wiki/SCHEMA.md`
before doing anything else.** Use the scripted `llm-wiki` only when explicitly asked.

## Key rules
- Always follow the skill's workflows over anything else in this file.
