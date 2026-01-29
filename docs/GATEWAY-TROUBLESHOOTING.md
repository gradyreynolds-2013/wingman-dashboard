# 🔧 WINGMAN GATEWAY TROUBLESHOOTING

**When I stop responding, check this guide.**

---

## Quick Diagnosis

SSH into your server and run:
```
clawdbot gateway status
```

This tells you if I'm running or not.

---

## Common Problems & Fixes

### ❌ "Gateway not running"

**Fix:**
```
clawdbot gateway start
```

If that fails, try:
```
clawdbot gateway start --verbose
```
This shows what's wrong.

---

### ❌ Gateway starts but stops immediately

**Likely cause:** Bad config file

**Fix:**
```
clawdbot doctor
```
This checks for config problems.

If doctor finds issues:
```
clawdbot configure
```
Walk through the setup again.

---

### ❌ "Port already in use" error

**Likely cause:** Old process still running

**Fix:**
```
pkill -f clawdbot
clawdbot gateway start
```

---

### ❌ Bot responds in terminal but not Telegram

**Likely cause:** Telegram connection issue

**Fix:**
```
clawdbot gateway restart
```

If still broken:
```
clawdbot configure --section telegram
```
Re-enter your bot token.

---

### ❌ "API key invalid" or "Authentication failed"

**Likely cause:** Anthropic API key expired or wrong

**Fix:**
```
clawdbot configure --section anthropic
```
Enter a fresh API key from: https://console.anthropic.com/

---

### ❌ Responses are slow or timing out

**Likely cause:** Model overloaded or rate limited

**Quick check:**
```
clawdbot status
```

**Fix options:**
1. Wait a few minutes and try again
2. Check your API usage at console.anthropic.com

---

### ❌ "Config file corrupted" or JSON errors

**Likely cause:** Config got messed up during an edit

**Fix (restore config from backup):**
```
cp ~/.clawdbot/clawdbot.json.bak ~/.clawdbot/clawdbot.json
clawdbot gateway restart
```

If no backup exists, reconfigure:
```
clawdbot configure
```

---

### ❌ After update, everything broke

**Fix (rollback):**
```
npm install -g clawdbot@previous-version
clawdbot gateway restart
```

Or restore from your backup file.

---

## Nuclear Options (Last Resort)

### Full Reset (keeps your backup safe)
```
clawdbot gateway stop
rm -rf ~/.clawdbot
clawdbot configure
clawdbot gateway start
```
Then restore your workspace from backup.

### Complete Reinstall
```
npm uninstall -g clawdbot
npm install -g clawdbot
clawdbot configure
```

---

## Useful Commands Cheat Sheet

| What you want | Command |
|---------------|---------|
| Check status | `clawdbot gateway status` |
| Start | `clawdbot gateway start` |
| Stop | `clawdbot gateway stop` |
| Restart | `clawdbot gateway restart` |
| View logs | `clawdbot gateway logs` |
| Health check | `clawdbot doctor` |
| Reconfigure | `clawdbot configure` |

---

## When to Use Your Backup

If nothing above works:

1. Stop trying to fix it
2. Follow the EMERGENCY-RESTORE-GUIDE
3. Extract your backup
4. Start fresh

Your memories and config are in that backup. Don't waste hours debugging when you can restore in 15 minutes.

---

## Still Stuck?

- Clawdbot Discord: https://discord.com/invite/clawd
- Docs: https://docs.clawd.bot

---

*Last updated: January 29, 2026*
*Created by Wingman for Grady Reynolds*
