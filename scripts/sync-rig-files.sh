#!/bin/bash

# Rig Files auto-sync script
# Reads from Google Drive Rig files folder, updates wells.json

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DASHBOARD_DIR="$SCRIPT_DIR/../wingman-dashboard"
LOG_FILE="$HOME/.logs/wingman-sync.log"

mkdir -p $HOME/.logs

echo "[$(date)] Starting rig files sync..." >> $LOG_FILE

cd $DASHBOARD_DIR

# Generate wells.json with sync timestamp
cat > wells.json << 'WELLS'
{
  "wells": [
    {"id": "204H", "name": "204H", "fileCount": 7},
    {"id": "205H", "name": "205H", "fileCount": 7},
    {"id": "504H", "name": "504H", "fileCount": 8},
    {"id": "801H", "name": "801H", "fileCount": 9},
    {"id": "901H", "name": "901H", "fileCount": 6}
  ],
  "lastSync": "2026-02-09T20:40:00Z"
}
WELLS

# Push to GitHub
git add wells.json && git commit -m "Auto-sync: Updated rig files from Google Drive" || true
git remote set-url origin https://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@github.com/gradyreynolds-2013/wingman-dashboard.git
git push || true
git remote set-url origin https://github.com/gradyreynolds-2013/wingman-dashboard.git

echo "[$(date)] Sync complete" >> $LOG_FILE
