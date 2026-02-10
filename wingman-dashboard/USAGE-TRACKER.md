# Usage Tracker & Cost Monitor

## Overview
Added usage meter and cost tracker to Wingman Dashboard showing real-time context usage, token consumption, and estimated costs.

## Features

### 1. Context Usage Gauge
- **Circular SVG gauge** displaying context percentage (0-100%)
- Animated fill with gradient styling
- Shows current tokens used vs. max tokens (e.g., "96k/131k")
- Displays current model in use

### 2. Cost Estimates
- **Daily cost** - Estimated based on current token usage × 20 sessions/day
- **Weekly cost** - Daily × 7
- **Monthly cost** - Daily × 30
- Uses model-specific pricing:
  - Claude Sonnet 4.5: $3/MTok avg
  - Grok 4.1 Fast Reasoning: $10/MTok avg
  - Claude Opus 4.5: $15/MTok avg

### 3. Compaction Counter
- Tracks number of context compaction events
- Updated from memory files

## Files

### `/home/ubuntu/clawd/scripts/update-usage-stats.py`
Python script that:
- Runs `openclaw sessions` to get current context usage
- Parses session data (tokens, percentage, model)
- Calculates cost estimates
- Counts compaction events from memory files
- Writes to `usage.json`

### `/home/ubuntu/clawd/wingman-dashboard/usage.json`
Data file containing:
```json
{
  "updated_at": "2026-02-10T01:42:32.408922Z",
  "context": {
    "percentage": 73,
    "used_tokens": 96000,
    "max_tokens": 131000,
    "tokens_display": "96k/131k"
  },
  "compaction": {
    "count": 0,
    "last_date": "2026-02-10"
  },
  "costs": {
    "daily": 19.2,
    "weekly": 134.4,
    "monthly": 576.0,
    "rate_per_mtok": 10.0
  },
  "model": "grok-4-1-fast-reasoning"
}
```

### `/home/ubuntu/clawd/wingman-dashboard/index.html`
Added:
- CSS for circular gauge, cost cards, and responsive layout
- HTML section with SVG gauge and cost display
- JavaScript `loadUsage()` function to fetch and render data

## Automation

### Cron Job
**Schedule:** Every 6 hours (`0 */6 * * *`)
**Command:** `python3 /home/ubuntu/clawd/scripts/update-usage-stats.py`
**Name:** `update-dashboard-usage`
**Target:** main session

**View status:**
```bash
openclaw cron list
```

**Manual update:**
```bash
python3 /home/ubuntu/clawd/scripts/update-usage-stats.py
```

## Deployment

### GitHub Repository
**Repo:** https://github.com/gradyreynolds-2013/wingman-dashboard
**Branch:** main

### Netlify
**URL:** https://wingmandash.netlify.app
**Auto-deploy:** Yes (connected to GitHub repo)

**To push updates:**
```bash
cd /home/ubuntu/clawd
git add wingman-dashboard/
git commit -m "Update dashboard"
git push origin master:main
```

Or use the cloned temp directory:
```bash
cd /tmp/wingman-dashboard-test
# Copy updated files
git add .
git commit -m "Update"
git push
```

## Current Stats (as of 2026-02-10 01:46 UTC)
- **Context:** 73% (96k/131k tokens)
- **Model:** Grok 4.1 Fast Reasoning
- **Daily Cost:** $19.20
- **Weekly Cost:** $134.40
- **Monthly Cost:** $576.00
- **Compactions:** 0

## Future Enhancements
- Historical cost tracking
- Context usage trends over time
- Alert when context exceeds 80%
- Compaction event log with timestamps
- Cost breakdown by model
