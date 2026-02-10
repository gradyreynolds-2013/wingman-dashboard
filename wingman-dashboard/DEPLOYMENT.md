# Wingman Dashboard - Model Breakdown Enhancement

## ✅ Completed Work

### 1. Enhanced Python Stats Script
**File:** `/home/ubuntu/clawd/scripts/update-usage-stats.py`

**Changes:**
- Aggregates usage across ALL sessions (not just main)
- Groups by model: Claude (Haiku/Sonnet/Opus), Grok, Gemini, GPT-4o, DALL-E
- Calculates per-model costs with accurate pricing
- Exports model breakdown to `usage.json`

**Test:**
```bash
cd /home/ubuntu/clawd
python3 scripts/update-usage-stats.py
```

### 2. Enhanced Dashboard HTML
**File:** `/home/ubuntu/clawd/wingman-dashboard/index.html`

**New Features:**
- **Model Cards Section:** Visual cards for each model showing:
  - Total tokens (formatted as K/M)
  - Monthly cost estimate
  - Session count
  - Color-coded by model type
  - Emoji indicators
  
- **Interactive Pie Chart:** Canvas-based chart showing:
  - Token distribution across models
  - Color-coded slices
  - Donut-style rendering
  - Legend with percentages

**CSS Additions:**
- `.model-breakdown-section` - Main container
- `.model-cards` - Responsive grid layout
- `.model-card` - Individual model cards with hover effects
- `.pie-chart-card` - Chart container
- Color scheme per model (purple for Sonnet, gold for Grok, etc.)

**JavaScript Functions:**
- `loadModelBreakdown(models)` - Renders model cards
- `renderPieChart(models)` - Draws canvas pie chart
- `getModelEmoji(modelKey)` - Returns emoji for model
- `getModelColor(modelKey)` - Returns hex color for model
- `formatTokens(tokens)` - Formats numbers as K/M

### 3. Git Commit
```bash
cd /home/ubuntu/clawd
git add wingman-dashboard/index.html wingman-dashboard/usage.json scripts/update-usage-stats.py
git commit -m "Add comprehensive model breakdown with cards and pie chart"
```

**Commit hash:** `b9cb40c`

## 📋 Manual Deployment Steps

### GitHub Push
Currently blocked by SSH authentication. Options:

**Option A: Set up GitHub Personal Access Token**
1. Go to GitHub.com → Settings → Developer Settings → Personal Access Tokens
2. Generate new token (classic) with `repo` scope
3. Set up credentials:
```bash
cd /home/ubuntu/clawd
git remote set-url origin https://ghp_YOURTOKEN@github.com/gradyreynolds-2013/wingman-dashboard.git
git push origin master
```

**Option B: Use SSH Key**
1. Add the public key to GitHub account:
```bash
cat ~/.ssh/github.pub
```
2. Copy output to GitHub.com → Settings → SSH Keys
3. Test and push:
```bash
cd /home/ubuntu/clawd
git remote set-url origin git@github.com:gradyreynolds-2013/wingman-dashboard.git
git push origin master
```

### Netlify Deploy
If Netlify is configured for auto-deploy from GitHub (recommended):
1. Push to GitHub (see above)
2. Netlify will auto-build and deploy
3. Check build logs at netlify.com

If manual deploy is needed:
1. Install Netlify CLI: `npm install -g netlify-cli`
2. Authenticate: `netlify login`
3. Deploy:
```bash
cd /home/ubuntu/clawd/wingman-dashboard
netlify deploy --prod
```

### Alternative: Manual File Upload
1. Download files locally:
   - `wingman-dashboard/index.html`
   - `wingman-dashboard/usage.json`
   - `scripts/update-usage-stats.py`
2. Upload via Netlify drag-and-drop interface
3. Or use Netlify CLI: `netlify deploy --dir=wingman-dashboard --prod`

## 🧪 Testing

### Local Test
```bash
cd /home/ubuntu/clawd/wingman-dashboard
python3 -m http.server 8765
# Visit http://localhost:8765
```

**Expected Results:**
- ✅ Model Usage Breakdown section appears after usage gauge
- ✅ Model cards show Claude Sonnet, Grok, and any other active models
- ✅ Pie chart renders with colored slices
- ✅ Legend shows percentages
- ✅ Costs display monthly estimates per model
- ✅ Cards are color-coded (purple, gold, etc.)

### Live Site Test
Once deployed, verify:
1. Navigate to dashboard URL
2. Check "Model Usage Breakdown" section
3. Verify pie chart renders
4. Hover over model cards for effects
5. Check responsive layout on mobile

## 📦 Backup Created

Archive: `/home/ubuntu/clawd/wingman-dashboard-enhanced.tar.gz`

Contains:
- Enhanced index.html
- Updated usage.json
- New update-usage-stats.py

## 🎨 Model Color Scheme

- **Claude Sonnet:** Purple gradient (#7c3aed → #a855f7)
- **Claude Opus:** Pink gradient (#ec4899 → #f472b6)
- **Claude Haiku:** Cyan gradient (#06b6d4 → #22d3ee)
- **Grok:** Gold gradient (#f59e0b → #fbbf24)
- **Gemini:** Blue gradient (#3b82f6 → #60a5fa)
- **GPT-4o:** Green gradient (#10b981 → #34d399)
- **DALL-E:** Red gradient (#ef4444 → #f87171)

## 📊 Current Model Stats

As of deployment:
- **Claude Sonnet:** 267k tokens, $2.41/mo (13 sessions)
- **Grok:** 97k tokens, $2.91/mo (1 session)
- **Total:** $5.32/month estimated

## 🔄 Automated Updates

The dashboard auto-refreshes usage stats. To ensure model breakdown stays current:

1. Add to cron (if not already scheduled):
```bash
*/30 * * * * cd /home/ubuntu/clawd && python3 scripts/update-usage-stats.py
```

2. Or trigger manually when needed:
```bash
cd /home/ubuntu/clawd
python3 scripts/update-usage-stats.py
```

## 🚀 Next Steps

1. **Push to GitHub** (choose Option A or B above)
2. **Verify Netlify auto-deploy** or manually deploy
3. **Test live site** at dashboard URL
4. **Monitor usage stats** - model breakdown updates every 30 min
5. **Add more models** as they come online (GPT-o1, Gemini Pro, etc.)

## ❓ Troubleshooting

**Pie chart not rendering:**
- Check browser console for Canvas errors
- Verify usage.json has `model_breakdown` array
- Ensure models array has `total_tokens` > 0

**Model cards empty:**
- Run `python3 scripts/update-usage-stats.py`
- Check `usage.json` contains model_breakdown
- Verify sessions exist: `openclaw sessions --json`

**Cost estimates seem off:**
- Review cost rates in `update-usage-stats.py`
- Adjust `get_model_cost_rate()` if pricing changes
- Token-to-cost multiplier may need tuning

---

**Created:** 2026-02-10  
**Commit:** b9cb40c  
**Status:** ✅ Ready for deployment
