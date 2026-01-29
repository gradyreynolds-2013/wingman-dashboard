# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice
**Areas**: frontend | backend | infra | tests | docs | config
**Statuses**: pending | in_progress | resolved | wont_fix | promoted | promoted_to_skill

## Status Definitions

| Status | Meaning |
|--------|---------|
| `pending` | Not yet addressed |
| `in_progress` | Actively being worked on |
| `resolved` | Issue fixed or knowledge integrated |
| `wont_fix` | Decided not to address (reason in Resolution) |
| `promoted` | Elevated to CLAUDE.md, AGENTS.md, or copilot-instructions.md |
| `promoted_to_skill` | Extracted as a reusable skill |

## Skill Extraction Fields

When a learning is promoted to a skill, add these fields:

```markdown
**Status**: promoted_to_skill
**Skill-Path**: skills/skill-name
```

Example:
```markdown
## [LRN-20250115-001] best_practice

**Logged**: 2025-01-15T10:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/docker-m1-fixes
**Area**: infra

### Summary
Docker build fails on Apple Silicon due to platform mismatch
...
```

---

## [LRN-20260129-001] correction

**Logged**: 2026-01-29T14:15:00Z
**Priority**: critical
**Status**: resolved
**Area**: config

### Summary
Model name changes require full version identifiers, not short names

### Details
Grady's previous bot was asked to "switch to Sonnet" and used `anthropic/claude-sonnet-4` instead of the correct `anthropic/claude-sonnet-4-20250514`. This crashed the gateway with "Unknown model" error and locked him out completely, losing the bot.

### Correct Behavior
Before changing any model in config:
1. Run `clawdbot models list` to verify exact model name
2. Use the full identifier with version date
3. Never guess or use shorthand names in config

### Resolution
- Created MODEL-CHANGES-GUIDE.md for Grady
- Will always verify model names before applying config changes

---
