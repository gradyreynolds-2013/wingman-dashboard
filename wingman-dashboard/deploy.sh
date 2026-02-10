#!/bin/bash
# Deploy script for Wingman Dashboard
# Usage: ./deploy.sh [github_token]

set -e

echo "🐦‍🔥 Wingman Dashboard Deployment"
echo "================================"
echo ""

# Update usage stats
echo "📊 Updating usage statistics..."
cd /home/ubuntu/clawd
python3 scripts/update-usage-stats.py

# Check git status
echo ""
echo "📋 Current git status:"
git status --short

# Stage changes
echo ""
echo "➕ Staging dashboard files..."
git add wingman-dashboard/index.html wingman-dashboard/usage.json scripts/update-usage-stats.py

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo "✅ No changes to commit"
else
    # Commit
    echo ""
    echo "💾 Committing changes..."
    git commit -m "Update dashboard - $(date +'%Y-%m-%d %H:%M')"
    
    # Push
    echo ""
    echo "🚀 Pushing to GitHub..."
    
    if [ -n "$1" ]; then
        # Use provided token
        echo "   Using provided GitHub token..."
        git remote set-url origin "https://$1@github.com/gradyreynolds-2013/wingman-dashboard.git"
        git push origin master
        # Reset to HTTPS without token in URL
        git remote set-url origin "https://github.com/gradyreynolds-2013/wingman-dashboard.git"
    else
        # Try normal push (requires SSH or stored credentials)
        git push origin master || {
            echo ""
            echo "❌ Push failed!"
            echo ""
            echo "To push manually, you need GitHub authentication."
            echo ""
            echo "Option 1 - SSH Key:"
            echo "  1. Copy this public key:"
            echo "     cat ~/.ssh/github.pub"
            echo "  2. Add to GitHub.com → Settings → SSH Keys"
            echo "  3. Run: git remote set-url origin git@github.com:gradyreynolds-2013/wingman-dashboard.git"
            echo "  4. Run: git push origin master"
            echo ""
            echo "Option 2 - Personal Access Token:"
            echo "  1. Generate token at GitHub.com → Settings → Developer Settings"
            echo "  2. Run: ./deploy.sh YOUR_TOKEN_HERE"
            echo ""
            echo "Option 3 - Manual Deploy:"
            echo "  1. Go to https://app.netlify.com"
            echo "  2. Select wingmandash site"
            echo "  3. Drag and drop wingman-dashboard/ folder"
            echo ""
            exit 1
        }
    fi
    
    echo ""
    echo "✅ Deployment complete!"
    echo "🌐 Check site: https://wingmandash.netlify.app"
    echo "⏱️  Netlify will auto-build in ~1-2 minutes"
fi

echo ""
echo "Done! 🎉"
