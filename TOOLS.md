# TOOLS.md - Local Notes

Skills define *how* tools work. This file is for *your* specifics — the stuff that's unique to your setup.

## Skill Sources

- **ClawdHub:** https://clawdhub.com/skills — Browse and download new skills here

## What Goes Here

Things like:
- Camera names and locations
- SSH hosts and aliases  
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Google Drive (gog)

**Account:** cachecabin@gmail.com
**Wingman Folder ID:** 1YYLYqXMlRuD3_iOPMUybM5lAenD2i4fH
**Rule:** ALL uploads go to Wingman folder automatically

Setup (already done):
```bash
export GOG_KEYRING_PASSWORD="wingman2026"
export GOG_ACCOUNT="cachecabin@gmail.com"
gog drive upload <file> --name "<name>" --parent 1YYLYqXMlRuD3_iOPMUybM5lAenD2i4fH
```

## Solar System Monitoring

**Huntsville Cabin** (off-grid, Utah)
- Location: https://www.opticsre.com/login
- Login: trentperry149@yahoo.com / AydenZP1109!
- Script: `/home/ubuntu/clawd/scripts/solar-check.py`
- Daily Report: 5:00 AM CST (11:00 AM UTC)
- Monitors:
  - Solar production (kW / kWh)
  - Generator status (running/off)
  - Generator production (kWh last 24hrs)
  - Battery voltage & temperature
  - Load consumption

## Examples

```markdown
### Cameras
- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH
- home-server → 192.168.1.100, user: admin

### TTS
- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
