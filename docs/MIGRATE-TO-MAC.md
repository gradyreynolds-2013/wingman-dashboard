# 🍎 MIGRATING WINGMAN TO YOUR MAC

**Move your Clawdbot setup from AWS EC2 to your Mac Desktop**

---

## What You'll Need

- Your Mac Desktop (running macOS)
- Your latest backup file (`wingman-backup-XXXXXXXX.tar.gz`)
- 30-45 minutes
- Telegram on your Mac (or phone nearby for testing)

---

## Step 1: Install Prerequisites on Mac

Open Terminal (Spotlight → search "Terminal"):

```bash
# Install Homebrew (if you don't have it)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Node.js via Homebrew
brew install node

# Verify installation
node --version  # Should show v18+ or v20+
npm --version
```

---

## Step 2: Install Clawdbot

```bash
npm install -g clawdbot
```

Verify:
```bash
clawdbot --version
```

---

## Step 3: Get Your Backup File

**Option A: Download from Telegram**
- Open Telegram on your Mac
- Find the backup file I sent you (search "wingman-backup")
- Click to download it
- Note where it saves (usually `~/Downloads/`)

**Option B: Transfer from your phone**
- AirDrop the backup file from your phone to your Mac
- Or email it to yourself and download on Mac

---

## Step 4: Extract the Backup

```bash
# Navigate to where the backup is (adjust path if needed)
cd ~/Downloads

# Extract it
tar -xzvf wingman-backup-20260129-140547.tar.gz

# This creates two folders:
# - .clawdbot (your config and data)
# - clawd (your workspace)

# Move them to the right locations
mv .clawdbot ~/
mv clawd ~/
```

---

## Step 5: Start Clawdbot

```bash
clawdbot gateway start
```

You should see:
```
✓ Gateway started on http://localhost:18789
✓ Telegram bot connected
```

---

## Step 6: Test It

Open Telegram and message your Wingman bot:

```
Hey, are you on my Mac now?
```

If I respond, you're good! ✅

---

## Step 7: Verify Everything Works

Check that your files are there:

```bash
# Check your workspace
ls ~/clawd

# You should see:
# - AGENTS.md
# - SOUL.md
# - USER.md
# - skills/
# - research/
# - docs/
# - etc.

# Check installed skills
cd ~/clawd
clawdhub list
```

---

## Step 8: Set Clawdbot to Auto-Start (Optional)

So Wingman starts automatically when your Mac boots:

```bash
clawdbot gateway install
```

This creates a LaunchAgent that starts Clawdbot on login.

To undo later:
```bash
clawdbot gateway uninstall
```

---

## Step 9: Update Backup Script Path (Optional)

The backup script currently points to `/home/ubuntu/` paths. Update it for Mac:

```bash
nano ~/clawd/scripts/backup.sh
```

Change:
- `/home/ubuntu/.clawdbot` → `~/.clawdbot`
- `/home/ubuntu/clawd` → `~/clawd`
- `/home/ubuntu/backups/wingman` → `~/backups/wingman`

Save and test:
```bash
~/clawd/scripts/backup.sh
```

---

## Step 10: Shut Down AWS Server (Once Everything Works)

**Only do this AFTER you've confirmed everything works on Mac!**

SSH into your AWS server one last time:

```bash
ssh ubuntu@YOUR-AWS-IP
```

Stop Clawdbot:
```bash
clawdbot gateway stop
```

Then in AWS Console:
1. Go to EC2
2. Select your instance
3. **Stop** the instance (to save money but keep it as backup)
4. Or **Terminate** it (to delete completely)

**Recommendation:** STOP it first, test Mac for a week, THEN terminate if all is well.

---

## Troubleshooting

### "Gateway won't start"

Check logs:
```bash
clawdbot gateway logs
```

Common issues:
- Port already in use → `lsof -ti:18789 | xargs kill -9`
- Missing dependencies → Reinstall node/npm
- Config corruption → Restore from `.clawdbot.json.bak`

### "Bot doesn't respond"

1. Check gateway status: `clawdbot gateway status`
2. Restart: `clawdbot gateway restart`
3. Check Telegram token is correct: `clawdbot config get channels.telegram.botToken`

### "Skills missing"

They're in `~/clawd/skills/` — if empty, they didn't extract properly.

Re-extract backup or reinstall:
```bash
cd ~/clawd
clawdhub install self-improving-agent
clawdhub install humanizer
# etc.
```

---

## Mac-Specific Tips

### Keep Your Mac Awake
Clawdbot needs to stay running. In System Preferences:
- **Energy Saver** → Prevent Mac from sleeping when display is off (desktop)
- Or use: `caffeinate -s` to keep system awake

### Firewall
macOS Firewall is usually fine. Clawdbot only listens on localhost by default (no external access).

### Updates
Clawdbot updates via npm:
```bash
npm update -g clawdbot
```

---

## Differences: AWS vs Mac

| Aspect | AWS EC2 | Your Mac |
|--------|---------|----------|
| **Always on** | 24/7 (cloud) | Only when Mac is on |
| **Access** | SSH from anywhere | Local only (unless VPN/Tailscale) |
| **Cost** | $10-30/month | Free (electricity) |
| **Speed** | Depends on instance | Fast (local) |
| **Backups** | Manual or S3 | Time Machine + manual |

**For your use case (2 weeks on/off):**
- Mac at home is perfect for off-weeks
- AWS might be better for on-hitch access (if you need remote)
- Or run both: Mac at home, lightweight AWS for hitch weeks

---

## Optional: Hybrid Setup (Best of Both Worlds)

**Idea:** 
- Use Mac when you're home (off-weeks)
- Spin up AWS only during hitch weeks for remote access

**How:**
1. Keep AWS instance **stopped** (not terminated)
2. When hitch starts, **start** the instance
3. Your most recent backup auto-syncs (via weekly Telegram sends)
4. When hitch ends, **stop** AWS, switch back to Mac

**Cost:** ~$3-5/month (storage only when stopped)

---

## Your Server Details (For Reference)

- **Provider:** AWS EC2
- **IP:** *(fill in when you need it)*
- **Instance Type:** *(fill in)*
- **Region:** us-east-2

---

*Last updated: January 29, 2026*  
*Created by Wingman for Grady Reynolds*
