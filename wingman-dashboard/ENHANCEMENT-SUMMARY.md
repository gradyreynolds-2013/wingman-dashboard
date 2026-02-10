# 🎯 Wingman Dashboard Model Breakdown Enhancement

## ✅ COMPLETED WORK

### 1. Enhanced Backend Script ✅
**File:** `scripts/update-usage-stats.py`

**Enhancements:**
- ✅ Parse `openclaw sessions --json` to get ALL agent sessions
- ✅ Aggregate token usage by model (Claude Haiku/Sonnet/Opus, Grok, Gemini, GPT-4o, DALL-E)
- ✅ Calculate per-model costs using accurate pricing ($0.40/M for Haiku, $3/M for Sonnet, $10/M for Grok, etc.)
- ✅ Export comprehensive `model_breakdown` array to usage.json
- ✅ Track session count per model
- ✅ Provide display names and normalized model keys

**Output Format:**
```json
{
  "model_breakdown": [
    {
      "model": "claude-sonnet",
      "display_name": "Claude Sonnet",
      "total_tokens": 267279,
      "input_tokens": 57,
      "output_tokens": 4171,
      "session_count": 13,
      "cost_rate": 3.0,
      "costs": {
        "daily": 0.08,
        "weekly": 0.56,
        "monthly": 2.41
      }
    }
  ]
}
```

### 2. Enhanced Frontend Dashboard ✅
**File:** `wingman-dashboard/index.html`

**New Features:**

#### Model Cards Section
- ✅ Responsive grid layout showing all active models
- ✅ Color-coded cards with gradient hover effects
- ✅ Emoji indicators per model (🎭 Sonnet, 🚀 Grok, 💎 Gemini, etc.)
- ✅ Token count formatted as K/M (e.g., "267.3k")
- ✅ Monthly cost estimate prominently displayed
- ✅ Session count badge
- ✅ Per-model color scheme (purple for Sonnet, gold for Grok, etc.)

#### Interactive Pie Chart
- ✅ HTML5 Canvas-based visualization
- ✅ Donut-style rendering with center cutout
- ✅ Color-coded slices matching model cards
- ✅ Smooth borders between slices
- ✅ Dynamic legend showing percentage breakdown
- ✅ Responsive sizing (280x280px)

#### CSS Additions
- `.model-breakdown-section` - Main container with section styling
- `.model-breakdown-container` - Grid: cards left, chart right
- `.model-cards` - Responsive auto-fit grid (200px min per card)
- `.model-card` - Individual cards with hover effects and colored top border
- `.pie-chart-card` - Chart container with padding
- `.pie-legend` - Styled legend items with color swatches
- Responsive breakpoints for mobile (<900px)

#### JavaScript Functions
- `loadModelBreakdown(models)` - Main render function
- `renderPieChart(models)` - Canvas pie chart with proportional slices
- `getModelEmoji(modelKey)` - Returns emoji for each model
- `getModelColor(modelKey)` - Returns hex color for visual consistency
- `formatTokens(tokens)` - Human-readable number formatting

### 3. Documentation ✅
- ✅ `DEPLOYMENT.md` - Full deployment guide with troubleshooting
- ✅ `ENHANCEMENT-SUMMARY.md` - This file
- ✅ `deploy.sh` - Automated deployment script with fallback instructions

### 4. Git Commit ✅
```bash
Commit: b9cb40c
Message: "Add comprehensive model breakdown with cards and pie chart"
Files: 
  - wingman-dashboard/index.html (554 insertions, 93 deletions)
  - scripts/update-usage-stats.py (complete rewrite)
  - wingman-dashboard/usage.json (updated format)
```

### 5. Local Testing ✅
- ✅ Script generates correct model breakdown data
- ✅ Dashboard HTML includes new section
- ✅ JavaScript renders without errors
- ✅ Verified on http://localhost:8765

---

## 🔴 BLOCKED: GitHub Push

**Issue:** SSH key not registered with GitHub account

**Current state:**
- ✅ Code committed locally (commit b9cb40c)
- ❌ Not pushed to GitHub
- ❌ Netlify auto-deploy hasn't triggered
- 🌐 Live site still shows old version

**SSH Public Key (needs to be added to GitHub):**
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEK3Y711lZYjGJaUAatjUzXPfAtbfKWfJ8tZme9Dclx5 ubuntu@ip-172-31-4-241
```

---

## 📋 MANUAL DEPLOYMENT STEPS

### Option 1: Add SSH Key to GitHub (Recommended)
```bash
# 1. Copy the SSH public key (shown above)

# 2. Add to GitHub:
#    - Go to GitHub.com → Settings → SSH and GPG Keys
#    - Click "New SSH Key"
#    - Paste the key above
#    - Save

# 3. Push to GitHub:
cd /home/ubuntu/clawd
git remote set-url origin git@github.com:gradyreynolds-2013/wingman-dashboard.git
git push origin master

# 4. Wait ~1-2 minutes for Netlify auto-deploy
# 5. Verify at https://wingmandash.netlify.app
```

### Option 2: Use Personal Access Token
```bash
# 1. Generate token:
#    - Go to GitHub.com → Settings → Developer Settings → Personal Access Tokens
#    - Generate new token (classic)
#    - Select scope: "repo"
#    - Copy token

# 2. Deploy with script:
cd /home/ubuntu/clawd/wingman-dashboard
./deploy.sh YOUR_TOKEN_HERE
```

### Option 3: Manual Netlify Upload
```bash
# 1. Download these files locally:
#    - wingman-dashboard/index.html
#    - wingman-dashboard/usage.json
#    - wingman-dashboard/actions.json
#    - wingman-dashboard/activity.json
#    - wingman-dashboard/tasks.json
#    - wingman-dashboard/scheduled-tasks.json
#    - wingman-dashboard/wells.json

# 2. Go to https://app.netlify.com
# 3. Select "wingmandash" site
# 4. Drag and drop the wingman-dashboard folder
# 5. Confirm deployment
```

---

## 🧪 TESTING CHECKLIST

Once deployed:

### Visual Elements
- [ ] "Model Usage Breakdown" section appears after usage gauge
- [ ] Model cards display for active models (Claude Sonnet, Grok, etc.)
- [ ] Each card shows: emoji, model name, token count, monthly cost, sessions
- [ ] Cards have colored top borders (purple, gold, blue, etc.)
- [ ] Pie chart renders in circular/donut shape
- [ ] Pie chart colors match model cards
- [ ] Legend shows model names with percentages

### Responsiveness
- [ ] Desktop: Cards grid + pie chart side-by-side
- [ ] Tablet/Mobile: Cards stack, chart below
- [ ] Cards wrap gracefully (min 200px per card)
- [ ] Text remains legible at all sizes

### Data Accuracy
- [ ] Token counts match `openclaw sessions --json` output
- [ ] Cost estimates are reasonable (check pricing rates)
- [ ] Session counts are accurate
- [ ] Percentages in legend add up to 100%

### Interactions
- [ ] Hover effects work on model cards (lift up, brighter border)
- [ ] No JavaScript console errors
- [ ] Page loads without flickering
- [ ] Other sections (activity feed, wells, etc.) still work

---

## 📊 CURRENT STATS (as of 2026-02-10)

**Active Models:**
- Claude Sonnet: 267k tokens, $2.41/mo, 13 sessions (73.4%)
- Grok: 97k tokens, $2.91/mo, 1 session (26.6%)

**Total:** 364k tokens, $5.32/month, 14 sessions

---

## 🎨 MODEL COLOR PALETTE

| Model | Emoji | Color | Gradient |
|-------|-------|-------|----------|
| Claude Sonnet | 🎭 | Purple | #7c3aed → #a855f7 |
| Claude Opus | 👑 | Pink | #ec4899 → #f472b6 |
| Claude Haiku | ✨ | Cyan | #06b6d4 → #22d3ee |
| Grok | 🚀 | Gold | #f59e0b → #fbbf24 |
| Gemini | 💎 | Blue | #3b82f6 → #60a5fa |
| GPT-4o | 🤖 | Green | #10b981 → #34d399 |
| DALL-E | 🎨 | Red | #ef4444 → #f87171 |

---

## 🔄 AUTOMATED UPDATES

The `update-usage-stats.py` script should run on a schedule to keep data fresh.

**Check if scheduled:**
```bash
crontab -l | grep update-usage-stats
```

**Add to cron if not present:**
```bash
crontab -e
# Add this line:
*/30 * * * * cd /home/ubuntu/clawd && python3 scripts/update-usage-stats.py
```

---

## 📦 FILES CHANGED

| File | Lines Changed | Status |
|------|---------------|--------|
| `scripts/update-usage-stats.py` | +221 / -127 | ✅ Complete rewrite |
| `wingman-dashboard/index.html` | +554 / -93 | ✅ Enhanced |
| `wingman-dashboard/usage.json` | New format | ✅ Updated |
| `wingman-dashboard/DEPLOYMENT.md` | +150 | ✅ Created |
| `wingman-dashboard/deploy.sh` | +75 | ✅ Created |

**Total additions:** ~1,000 lines of code/docs

---

## 🚀 NEXT STEPS

### Immediate (required for live deployment):
1. **Add SSH key to GitHub** OR use personal access token
2. **Run:** `cd /home/ubuntu/clawd && git push origin master`
3. **Wait 1-2 minutes** for Netlify auto-deploy
4. **Test live site:** https://wingmandash.netlify.app
5. **Verify** model breakdown section renders correctly

### Future Enhancements (optional):
- Add model comparison trends (week-over-week)
- Show input vs output token ratio per model
- Add cost alerts when exceeding budget thresholds
- Track model switching patterns
- Export model usage report as CSV
- Add filtering/sorting to model cards

---

## 📞 SUPPORT

**Dashboard URL:** https://wingmandash.netlify.app  
**GitHub Repo:** https://github.com/gradyreynolds-2013/wingman-dashboard  
**Netlify App:** https://app.netlify.com/sites/wingmandash  

**Backup Archive:** `/home/ubuntu/clawd/wingman-dashboard-enhanced.tar.gz`

---

## ✨ SUCCESS CRITERIA

This enhancement is considered **COMPLETE** when:

- ✅ Backend aggregates all models correctly
- ✅ Frontend displays model cards with accurate data
- ✅ Pie chart renders proportionally
- ✅ Code is committed to git
- ⏳ Code is pushed to GitHub (PENDING)
- ⏳ Netlify site shows new features (PENDING)
- ⏳ Live site tested and verified (PENDING)

**Current Status:** 🟡 85% Complete (awaiting GitHub push)

---

**Created:** 2026-02-10 02:07 UTC  
**Commit:** b9cb40c  
**By:** Wingman (Sub-agent)
