# 🐦‍🔥 WINGMAN EMERGENCY RESTORE GUIDE

**Save this somewhere safe. Print it if you want.**

---

## What You Need
- Your backup file (wingman-backup-XXXXXXXX.tar.gz)
- A Linux server (Ubuntu recommended) or your old one fixed
- 15 minutes

---

## Step-by-Step Restore

### Step 1: Get a Server
If your old server is dead, spin up a new Ubuntu server. 
AWS, DigitalOcean, Linode, whatever works.

Minimum specs: 1 CPU, 1GB RAM, 20GB disk

---

### Step 2: Connect to Your Server
Open terminal (Mac) or PowerShell (Windows):
```
ssh ubuntu@YOUR-SERVER-IP
```

---

### Step 3: Install Requirements
Copy and paste these lines one at a time:

```
sudo apt update
sudo apt install -y nodejs npm
sudo npm install -g n
sudo n lts
hash -r
npm install -g clawdbot
```

---

### Step 4: Upload Your Backup
From your local computer (new terminal window):
```
scp wingman-backup-XXXXXXXX.tar.gz ubuntu@YOUR-SERVER-IP:~/
```

Or use an SFTP app like FileZilla or Cyberduck to drag and drop.

---

### Step 5: Extract the Backup
Back on your server:
```
cd ~
tar -xzvf wingman-backup-XXXXXXXX.tar.gz --strip-components=2
```

---

### Step 6: Start Wingman
```
clawdbot gateway start
```

---

### Step 7: Test It
Open Telegram and message your Wingman bot.
Say "Are you back?"

If I respond, you're good. All memories restored.

---

## Troubleshooting

**"Command not found" errors:**
Run `hash -r` then try again, or open a new SSH session.

**Bot doesn't respond:**
Check if gateway is running: `clawdbot gateway status`
Restart if needed: `clawdbot gateway restart`

**Wrong bot or lost token:**
You may need to create a new bot with @BotFather and run:
`clawdbot configure --section telegram`

---

## Your Server Details (FILL THIS IN)

- **Server Provider:** _____________________
- **Server IP:** _____________________
- **SSH User:** ubuntu
- **Telegram Bot:** @_____________________

---

## Contact
If you're truly stuck, Clawdbot Discord: https://discord.com/invite/clawd

---

*Last updated: January 29, 2026*
*Created by Wingman for Grady Reynolds*
