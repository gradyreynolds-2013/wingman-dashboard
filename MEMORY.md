# MEMORY.md - Wingman's Long-Term Memory

## Core Infrastructure

### Wingman Mission Control Dashboard
- **Live at:** https://wingmandash.netlify.app (also at http://18.118.31.236:8080)
- **Hosting:** Netlify (production-grade, zero crashes)
- **GitHub Repo:** https://github.com/gradyreynolds-2013/wingman-dashboard
- **Purpose:** Real-time activity tracking, task management, rig file inventory, project status
- **Status:** ✅ Deployed and operational with auto-deploy pipeline
- **Features:**
  - Task management (sort by due/priority/status/name, clear completed)
  - Activity feed (all actions logged + status dropdowns)
  - Calendar/schedule view (weekly upcoming tasks)
  - Global search (across tasks, actions, schedule)
  - Well files (36 documents, 5 wells, click-to-open modal)
  - Auto-sync from Google Drive daily at 5 AM UTC
- **Files Location:** `/home/ubuntu/clawd/wingman-dashboard/`
  - `index.html` - Full UI with all features
  - `activity.json` - Activity feed data (auto-updated)
  - `tasks.json` - Quick tasks (sortable, clearable)
  - `wells.json` - Rig files (36 documents from Google Drive)
  - `sync-rig-files.sh` - Daily Google Drive sync script (5 AM UTC)
- **Deployment:** GitHub push → Netlify auto-deploys in ~30 seconds

### Google Workspace Integration
- **Service Account Email:** wingman-bot-service-account@wingman-bot.iam.gserviceaccount.com
- **Service Account ID:** 107568506848093825308
- **Credentials Path:** `/home/ubuntu/.config/wingman-service-account.json`
- **Google Cloud Project:** wingman-bot (GCP)
- **APIs Enabled:** Drive, Sheets, Calendar, Docs
- **Folder Access:** Wingman folder (ID: 1YYLYqXMlRuD3_iOPMUybM5lAenD2i4fH)
- **Folder Organization:**
  - OZ Fund/ (pro formas, guides, investor scripts)
  - Marketing/ (content calendar, social media)
  - Sales Tools/ (investor pitches, objection scripts)
  - Resources/ (NEPQ PDFs, reference materials)
  - System/ (backups, archives, well files)
- **Status:** ✅ Service account created; ⏳ Awaiting Wingman folder share (Editor access)
- **Capabilities:**
  - ✅ Read/write Google Drive files (once folder shared)
  - ✅ Create/update Google Sheets
  - ✅ Read/update Google Docs
  - ✅ Pull calendar events
  - ⚠️ Create NEW files (quota exceeded; workaround: user creates, I update)
- **gog CLI Status:** Not yet configured with service account
- **Security:** No personal login; pure service account access

### Google Drive Organization
**Wingman folder structure:**
```
Wingman/
├── OZ Fund/ (pro formas, guides, investor scripts)
├── Marketing/ (content calendar, social media)
├── Sales Tools/ (investor pitches, objection scripts)
├── Resources/ (NEPQ PDFs, reference materials)
└── System/ (backups, archives)
```
**Total:** 36 files, 5 organized folders, all content preserved

### AI Models Available
- **Anthropic:** Sonnet 4.5 (primary), Opus 4.5 (heavy thinking), Haiku 4.5 (lightweight)
- **Google:** Gemini 3 Flash Preview
- **xAI:** Grok 4.1 (fast reasoning)
- **OpenAI:** GPT-4o, DALL-E 3 (image generation)
- **Image Generation:** DALLE-3 working (API key configured)

### Rig Well Documents
**All 36 documents indexed and tracked:**
- 204H: 7 documents
- 205H: 7 documents
- 504H: 8 documents
- 801H: 9 documents
- 901H: 6 documents

## Agent Status

### Sulla (Gym Accountability Bot)
- **Status:** ✅ LIVE and responding
- **Workspace:** `/home/ubuntu/andy/`
- **Binding:** Telegram `sulla` account → `sulla` agent
- **Function:** Gym tracking, nutrition, discipline accountability (Andy Frisella personality)

### Atlas (OZ Business Consultant)
- **Status:** ✅ LIVE and responding
- **Workspace:** `/home/ubuntu/atlas/`
- **Binding:** Telegram `atlas` account → `atlas` agent
- **Function:** OZ fund strategy, property analysis, investor relations

## Grady's Current Priorities

### Current Status: Off Hitch (since 2026-02-03)

**Dashboard Priorities (Feb 8-12):**
- ✅ Build Wingman Activity Dashboard (DONE)
- ✅ Deploy to Netlify with auto-deploy (DONE)
- ✅ Set up service account Google Drive access (DONE)
- ✅ Enable autonomous task management (DONE)
- ✅ Rig files auto-sync from Google Drive (DONE - daily 5 AM)

**Business Focus (Feb 15+):**
- Set up CREXI automation (due Feb 10)
- Research first OZ property target (apartments in Opportunity Zones)
- Finalize OZ fund website (positioning + copy + deployment)
- Create investor outreach list (LP identification)

**Business Model:** Vertically integrated real estate company in Opportunity Zones (QOZ strategy)

## Key Decisions & Setup

### Architecture Choices
- **Service Account Access:** wingman-bot-service-account (direct, no user interaction required)
- **Dashboard Hosting:** Self-hosted on EC2 (user preference; fragility risk mitigated by keep-alive script)
- **Google File Creation:** Limited by quota; pattern = user creates file, Wingman updates content
- **Task Management:** JSON-based quick tasks (auto-synced to dashboard, ordered by due date)
- **Well Files:** Centralized in System folder for drilling consultant work
- **Model Strategy:** Haiku for lightweight automation (cost efficiency)

### Current Blockers
1. **Service Account Folder Access:** Awaiting Grady to share Wingman folder with service account (Editor access)
2. **Dashboard Persistence:** Keep-alive script created but not yet deployed to systemd
3. **gog CLI Configuration:** Need to configure with service account credentials

## Next Architecture Steps (Ordered by Dependency)

**Phase 1: Unblock Google Access**
1. Share Wingman folder with service account (Editor access) ← **BLOCKER**
2. Configure gog CLI with service account credentials
3. Test Drive/Sheets/Calendar access via `gog` commands

**Phase 2: Dashboard Resilience**
4. Deploy keep-alive script to systemd for persistence
5. Add health checks and auto-restart logic

**Phase 3: Automation & Intelligence**
6. Enable autonomous Quick Tasks management (read/write to tasks.json)
7. Implement CREXI automation (due Feb 10)
8. Build "Today's Focus" dashboard section (AI-generated daily briefing)
9. Calendar Sync - Pull hitch dates, deadline tracking
10. Investor Tracking Sheet - LP pipeline management

---

**Last Updated:** 2026-02-10 (Dashboard Usage/Cost Tracker + Model Breakdown + Daily X OZ Brief Cron) (Session: Infrastructure Recovery & Production Deployment - Server Recovery, Netlify Migration, Auto-Sync Setup, Agent Recovery)
