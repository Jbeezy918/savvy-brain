# SOP Sync — Project Status, Recovery, and Build Brief

**Updated:** July 22, 2026  
**Owner:** SavvyTech Consulting LLC  
**Product:** SOP Sync  
**Backend:** SOP_Sync-Backend  
**Supabase project ID:** `shzaxjsflzpntgefuzko`  
**Current backend status:** **Paused**

## Immediate Action Required

The Supabase backend was paused on July 22, 2026 after more than seven days of insufficient activity.

1. Sign in to Supabase and open the [SOP_Sync-Backend project](https://supabase.com/dashboard/project/shzaxjsflzpntgefuzko).
2. Select **Restore project** or **Unpause project**, whichever the dashboard displays.
3. Wait until the project reports a healthy/active status.
4. Verify the database, authentication, storage, API, and application connection before resuming development.
5. Back up/export critical project data after access is restored.

The project must be restored **within 90 days of July 22, 2026**—approximately **October 20, 2026**. Supabase states that after that window the project cannot be restored, although its data will remain available for download.

## How to Keep It Active

Supabase automatically pauses inactive free-tier projects after seven days of insufficient activity.

Choose one:

- **Free plan:** use the project regularly and do not allow another seven-day inactivity period. Confirm real application/database activity in Supabase; do not rely on an unverified artificial ping.
- **Pro plan:** upgrade through the [organization billing settings](https://supabase.com/dashboard/org/oiveeyzpqbinbpqyqzpu/billing?panel=subscriptionPlan) to prevent inactivity-based pausing.

Upgrading is optional. Restoring the project is the urgent requirement.

## Post-Restore Verification Checklist

- [ ] Project status is active/healthy.
- [ ] Database tables and records are present.
- [ ] Authentication configuration and users are intact.
- [ ] Storage buckets and files are accessible.
- [ ] API URL and required keys are available in project settings.
- [ ] Local environment variables point to this project.
- [ ] Backend health check succeeds.
- [ ] SOP Sync can create, read, update, and retrieve a test record.
- [ ] Critical data has been exported/backed up.
- [ ] A recurring activity review is scheduled if remaining on the free plan.

## Confirmed Product Purpose

SOP Sync is a process-intelligence application for observing, recording, auditing, standardizing, and improving real-world work processes. It is not merely a document repository.

Core intended workflow:

1. Record approved user activity and capture screenshots at meaningful steps.
2. Convert captured activity into an ordered process map.
3. Generate a standard operating procedure or work instruction.
4. Compare later executions against the approved process.
5. Identify deviations, timing differences, and training needs.
6. Produce reviewable reports and improvement recommendations.

## Confirmed Local Project Locations

Two SOP Sync source locations have appeared in prior project records and must be reconciled before code changes:

- `/Users/joebudds/Desktop/CoWork_Pipeline/SOPsync`
- `/Users/joebudds/Desktop/SOP_Syncv2`

The Savvy Suite control-center record uses:

- Tool link: `/Users/joebudds/Desktop/Savvy_Suite/Tools/Business Products/SOP Sync`
- Launcher: `Launch_SOPSync.command`
- Dashboard candidate: `sopsync_dashboard.py`
- UI framework identified: Tkinter
- Environment: no separate environment recorded

Do not assume both source folders contain the same version. Compare modification dates and version-control state before merging or deleting anything.

## Known Project Components

The previously reported `CoWork_Pipeline/SOPsync` folder included:

- `CLAUDE.md`
- `requirements.txt`
- `SOPsync.spec`
- `sop_pipeline.py`
- `sop_sync_mvp.py`
- `sopsync_api.py`
- `sopsync_dashboard.py`
- `sopsync_recorder.py`
- `sopsync_viewer.py`
- `sopsync_status.py`
- `sop_output/`
- `sop_sync_data/`
- `SESSION_LOGS/`
- `logs/`
- `build/`
- `dist/`

Generated outputs, logs, screenshots, databases, build artifacts, and session history should not be loaded automatically into an AI coding context. Start with the core project instructions, current-state documents, and only the source files needed for the active task.

## Backend Configuration Previously Associated With This Project

Prior records associate `SOP_Sync-Backend` with an Archon-related setup at:

- Repository: `/Users/joebudds/archon`
- Environment file: `/Users/joebudds/archon/.env`
- Expected variables: `SUPABASE_URL` and `SUPABASE_SERVICE_KEY`
- Prior diagnostic log: `backend_no_docker.log`
- Constraint at that time: no-Docker startup path

These details are historical and must be verified against the current SOP Sync source before reuse. Never copy secret values into this Markdown file or commit them to source control.

## Recommended Recovery Order

1. Restore the Supabase project.
2. Export a backup.
3. Verify the current Supabase URL and keys locally without exposing their values.
4. Identify the authoritative SOP Sync source folder.
5. Launch the current dashboard and run a controlled end-to-end test.
6. Repair backend connectivity or data migrations only after the source and database versions are confirmed.
7. Update the project documentation with verified architecture, schema, and deployment details.

## Branding Direction

- Product name: **SOP Sync**
- Parent/master brand direction previously discussed: **Savvy Sync**
- Positioning: process observation, intelligence, auditing, and improvement
- Preferred visual language: workflow nodes and process intelligence
- Avoid: generic clipboard/checklist branding
- Tagline direction: **Observe. Optimize. Standardize.**

## Items Still Requiring Verification

- Which local source folder is authoritative.
- Whether `/Users/joebudds/archon` is still the active backend repository.
- Current database schema and migrations.
- Current deployment target and public application URL.
- Whether authentication and storage are used in the current build.
- Exact production health-check endpoint.
- Backup/restore procedure for SOP Sync application data.
- Whether real weekly usage is sufficient to keep the free project active.

## Source Evidence

- Supabase email received July 22, 2026: “Your Supabase Project SOP_Sync-Backend has been paused.”
- Supabase email received July 21, 2026: “Your Supabase Project SOP_Sync-Backend is going to be paused.”
- Prior SOP Sync project conversations and Savvy Suite audit/control-center records.

