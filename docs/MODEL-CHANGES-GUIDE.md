# 🧠 CHANGING MODELS SAFELY

**This guide exists because wrong model names can break everything.**

---

## The Problem

When you set an invalid model name like `anthropic/claude-sonnet-4`, the gateway crashes because that model doesn't exist. Your bot stops responding and you're locked out.

---

## Valid Model Names (As of January 2026)

### Anthropic Models
```
anthropic/claude-opus-4-5          ← Current best (you're using this)
anthropic/claude-sonnet-4-20250514 ← Fast, cheaper
anthropic/claude-haiku-3-5-20241022 ← Fastest, cheapest
```

### Important!
- Model names include version dates
- `claude-sonnet-4` alone is WRONG
- `claude-sonnet-4-20250514` is CORRECT
- These change over time — always verify first

---

## How to Check Available Models

Before changing anything, run:
```
clawdbot models list
```

This shows all valid models you can use.

---

## Safe Way to Change Models

### Option 1: Use the CLI (Safest)
```
clawdbot config set agents.defaults.model.primary "anthropic/claude-sonnet-4-20250514"
clawdbot gateway restart
```

### Option 2: Ask Me to Do It
Just tell me: "Switch to Sonnet" or "Use a cheaper model"
I'll handle it correctly.

---

## If You Already Broke It

### Symptoms:
- Bot won't respond
- Logs show: "Unknown model: anthropic/claude-whatever"
- Gateway keeps crashing

### Fix (from SSH):

**Step 1: Stop the broken gateway**
```
clawdbot gateway stop
```

**Step 2: Fix the config file manually**
```
nano ~/.clawdbot/clawdbot.json
```

Find the line that looks like:
```
"primary": "anthropic/claude-sonnet-4"
```

Change it to a valid model:
```
"primary": "anthropic/claude-opus-4-5"
```

Save: `Ctrl+O`, `Enter`, `Ctrl+X`

**Step 3: Restart**
```
clawdbot gateway start
```

### Alternative: Restore from Backup
If editing JSON scares you:
```
tar -xzvf wingman-backup-XXXXXXXX.tar.gz -C / --strip-components=2
clawdbot gateway start
```

---

## Recovery Cheat Sheet

| Problem | Command |
|---------|---------|
| See valid models | `clawdbot models list` |
| Check current model | `clawdbot config get agents.defaults.model.primary` |
| Change model safely | `clawdbot config set agents.defaults.model.primary "MODEL_NAME"` |
| Fix bad config | Edit `~/.clawdbot/clawdbot.json` manually |
| Nuclear option | Restore from backup |

---

## Pro Tips

1. **Always verify the model name** before changing it
2. **Keep a backup** before making config changes
3. **Ask me first** — I can change my own model safely
4. **When in doubt**, stick with `anthropic/claude-opus-4-5`

---

## Quick Reference: Model Nicknames

If you want to switch models, just tell me using these simple names:

| Say this | I'll use |
|----------|----------|
| "Use Opus" | anthropic/claude-opus-4-5 |
| "Use Sonnet" | anthropic/claude-sonnet-4-20250514 |
| "Use Haiku" | anthropic/claude-haiku-3-5-20241022 |
| "Use something cheaper" | I'll pick appropriately |

I'll handle the technical names so you don't have to.

---

*Last updated: January 29, 2026*
*Created by Wingman for Grady Reynolds*
