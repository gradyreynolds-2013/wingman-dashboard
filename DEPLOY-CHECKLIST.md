# ✅ Wingman Dashboard Deployment Checklist

## 🚀 Quick Deploy (5 minutes)

### Step 1: Add SSH Key to GitHub (2 min)
```bash
# 1. Copy this key:
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEK3Y711lZYjGJaUAatjUzXPfAtbfKWfJ8tZme9Dclx5 ubuntu@ip-172-31-4-241

# 2. Go to: https://github.com/settings/keys
# 3. Click "New SSH Key"
# 4. Title: "Wingman Dashboard Server"
# 5. Paste key above
# 6. Click "Add SSH Key"
```

### Step 2: Push to GitHub (30 sec)
```bash
cd /home/ubuntu/clawd
git remote set-url origin git@github.com:gradyreynolds-2013/wingman-dashboard.git
git push origin master
```

**Expected output:**
```
Enumerating objects: 9, done.
Counting objects: 100% (9/9), done.
...
To github.com:gradyreynolds-2013/wingman-dashboard.git
   abc1234..b9cb40c  master -> master
```

### Step 3: Wait for Netlify (1-2 min)
- Netlify auto-detects GitHub push
- Builds site automatically
- Deploys to https://wingmandash.netlify.app

**Track progress:**
https://app.netlify.com/sites/wingmandash/deploys

### Step 4: Test Live Site (2 min)
```bash
# Quick check:
curl https://wingmandash.netlify.app | grep "Model Usage Breakdown"

# Should return:
# <div class="section-title">Model Usage Breakdown</div>
```

**Manual check:**
1. Visit https://wingmandash.netlify.app
2. Scroll down past usage gauge
3. See "MODEL USAGE BREAKDOWN" section
4. Verify model cards and pie chart render
5. Test hover effects on cards

---

## 🔧 Alternative: Use Personal Access Token

If SSH doesn't work:

### Generate Token
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Name: "Wingman Dashboard Deploy"
4. Scopes: Check `repo`
5. Click "Generate token"
6. **Copy token immediately** (shown once!)

### Deploy with Token
```bash
cd /home/ubuntu/clawd/wingman-dashboard
./deploy.sh ghp_YOUR_TOKEN_HERE
```

---

## 📋 Pre-Flight Checklist

Before deploying, verify:

- [x] Python script tested and working
  ```bash
  cd /home/ubuntu/clawd
  python3 scripts/update-usage-stats.py
  # Should output: "✓ Usage stats updated: X models tracked"
  ```

- [x] usage.json contains model_breakdown
  ```bash
  cat wingman-dashboard/usage.json | jq '.model_breakdown[0].display_name'
  # Should output: "Claude Sonnet" or similar
  ```

- [x] HTML includes new section
  ```bash
  grep "Model Usage Breakdown" wingman-dashboard/index.html
  # Should find the section title
  ```

- [x] Git status clean
  ```bash
  git status
  # Should show: "Your branch is ahead of 'origin/master' by 1 commit."
  ```

- [x] Commit exists
  ```bash
  git log -1 --oneline
  # Should show: "b9cb40c Add comprehensive model breakdown..."
  ```

---

## 🧪 Post-Deploy Testing

After deployment, check:

### Visual Tests
- [ ] Model cards visible
- [ ] Pie chart renders
- [ ] Colors match (purple, gold, etc.)
- [ ] Emojis display (🎭, 🚀, etc.)
- [ ] Hover effects work
- [ ] Mobile responsive

### Data Tests
- [ ] Token counts accurate
- [ ] Costs are reasonable ($2-5/mo range)
- [ ] Percentages add to 100%
- [ ] Session counts correct

### Functional Tests
- [ ] No JavaScript errors in console
- [ ] Other sections still work (activity, wells, etc.)
- [ ] Page loads in <2 seconds
- [ ] Refresh button updates data

---

## 🚨 Troubleshooting

### Problem: SSH key rejected
**Error:** "Permission denied (publickey)"

**Solution:**
1. Verify key added to GitHub (check Settings → SSH Keys)
2. Test connection: `ssh -T git@github.com`
3. Should see: "Hi gradyreynolds-2013! You've successfully authenticated"
4. If still fails, use personal access token method

### Problem: Netlify not deploying
**Check:**
1. Go to https://app.netlify.com/sites/wingmandash/deploys
2. Look for build logs
3. Check for errors in build process

**Common issues:**
- Build timeout (increase in settings)
- Missing environment variables
- Wrong build command

### Problem: Model cards not showing
**Debug:**
```bash
# 1. Check data generation
python3 scripts/update-usage-stats.py
cat wingman-dashboard/usage.json | jq '.model_breakdown'

# 2. Check sessions exist
openclaw sessions --json | jq '.sessions | length'

# 3. Verify HTML uploaded
curl https://wingmandash.netlify.app/usage.json | jq '.model_breakdown'
```

### Problem: Pie chart blank
**Causes:**
- Canvas not supported (unlikely)
- No models with tokens > 0
- JavaScript error

**Fix:**
- Open browser console (F12)
- Look for red errors
- Verify `model_breakdown` array exists

---

## 📊 Success Criteria

Deployment is successful when:

✅ All Tests Pass:
- [ ] GitHub push successful
- [ ] Netlify build completes
- [ ] Site loads at wingmandash.netlify.app
- [ ] Model breakdown section visible
- [ ] Pie chart renders
- [ ] No console errors

✅ Data Accurate:
- [ ] Shows all active models
- [ ] Token counts match `openclaw sessions --json`
- [ ] Costs are reasonable
- [ ] Session counts correct

✅ Visual Quality:
- [ ] Colors look good
- [ ] Hover effects work
- [ ] Mobile responsive
- [ ] Consistent with rest of dashboard

---

## 📞 Quick Reference

**Dashboard:** https://wingmandash.netlify.app  
**GitHub Repo:** https://github.com/gradyreynolds-2013/wingman-dashboard  
**Netlify Admin:** https://app.netlify.com/sites/wingmandash  
**Commit:** b9cb40c  

**Files Changed:**
- `scripts/update-usage-stats.py`
- `wingman-dashboard/index.html`
- `wingman-dashboard/usage.json`

**Documentation:**
- `DASHBOARD-ENHANCEMENT-COMPLETE.md` - Full report
- `DEPLOYMENT.md` - Detailed guide
- `BEFORE-AFTER.md` - Visual comparison
- `deploy.sh` - Auto-deploy script
- This file - Quick checklist

---

## ⏱️ Time Estimates

| Task | Time |
|------|------|
| Add SSH key to GitHub | 2 min |
| Push to GitHub | 30 sec |
| Netlify build & deploy | 1-2 min |
| Test live site | 2 min |
| **TOTAL** | **~5 minutes** |

---

## 🎯 Ready to Deploy?

If all pre-flight checks pass, you're ready!

**Quick Command:**
```bash
cd /home/ubuntu/clawd
git push origin master && echo "✅ Pushed! Check Netlify in 2 min."
```

Then visit: https://wingmandash.netlify.app

---

**Created:** 2026-02-10 02:10 UTC  
**Status:** Ready for deployment  
**Estimated time to complete:** 5 minutes
