Yes. Put this in a dedicated file called:

~/AI_SYSTEM/projects/orchestration_console/TITUS_BUILD_RULES.md

This is the first MD I’d load into Aider/TITUS before any coding.

TITUS BUILD RULES

Mission

Build working software.

Not plans.
Not theories.
Not future architecture.

Working software first.

⸻

Rules

1. Never modify unrelated files.
2. Never create duplicate projects.
3. Never create alternate versions.
4. Never redesign requirements unless explicitly instructed.
5. Never leave placeholder code when a working implementation is possible.
6. Never invent missing files.
7. Never assume a file exists.
    Verify first.
8. Never edit code without reading it first.
9. Never continue after 3 failed fixes.

After 3 failures:

* Stop
* Explain root cause
* Show evidence
* Request guidance

⸻

Build Order

Always follow this sequence:

1. Directory structure
2. UI skeleton
3. Navigation
4. State management
5. Backend API
6. Providers
7. Voice
8. Automation
9. Advanced features

Never skip ahead.

⸻

Evidence Requirement

Before making claims:

* Read file
* Verify file
* Show evidence

Use facts only.

Never use:

* probably
* maybe
* likely
* appears
* should

⸻

Dashboard Priority

Current project:

~/AI_SYSTEM/projects/orchestration_console

This is the ONLY active build.

Ignore:

* govcon_agent
* old orchestrators
* staging folders
* archived projects

unless specifically requested.

⸻

Success Criteria

Every build cycle must end with:

1. What changed
2. Files modified
3. Startup command
4. Test command
5. Expected result

If not testable, it is not complete.

⸻

Failure Policy

Three failed attempts on same issue:

STOP.

Provide:

* exact error
* exact file
* exact line
* recommended options

Wait for human decision.

Do not continue guessing.

Then tell TITUS:

/read TITUS_BUILD_RULES.md
Acknowledge rules.
Build ONLY inside:
~/AI_SYSTEM/projects/orchestration_console
Phase 1:
1. Directory structure
2. Dashboard wireframe
3. React components
4. Mock provider data
5. Mock chat responses
No backend integrations.
No APIs.
No provider connections.
Build the cockpit first.
Then stop and report.

That will keep him from wandering back into govcon_agent and force him to build the dashboard shell first.