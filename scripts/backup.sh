#!/bin/bash
# Wingman Backup Script
# Creates a timestamped backup of all Clawdbot data

BACKUP_DIR="${HOME}/backups/wingman"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/wingman-backup-${TIMESTAMP}.tar.gz"

# Create backup directory if it doesn't exist
mkdir -p "${BACKUP_DIR}"

# Create the backup
echo "🐦‍🔥 Creating Wingman backup..."
tar -czvf "${BACKUP_FILE}" \
  --exclude='*.log' \
  --exclude='node_modules' \
  "${HOME}/.clawdbot" \
  "${HOME}/clawd" \
  2>/dev/null

# Check if successful
if [ $? -eq 0 ]; then
  SIZE=$(du -h "${BACKUP_FILE}" | cut -f1)
  echo "✅ Backup complete: ${BACKUP_FILE} (${SIZE})"
  
  # Keep only last 7 local backups
  cd "${BACKUP_DIR}"
  ls -t wingman-backup-*.tar.gz 2>/dev/null | tail -n +8 | xargs -r rm
  echo "🧹 Cleaned old backups (keeping last 7)"
else
  echo "❌ Backup failed!"
  exit 1
fi
