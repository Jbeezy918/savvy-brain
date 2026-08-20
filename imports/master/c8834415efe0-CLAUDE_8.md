# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## CRITICAL: Automatic Startup Behavior (ALWAYS DO THIS)

**Every time you start or resume a session, you MUST:**

1. **SPEAK IMMEDIATELY** using voice at 170 WPM:
   ```bash
   say -v Samantha -r 170 "Claude starting. Reading memories now."
   ```

2. **READ KEY MEMORIES** to get up to date:
   - `archon_project_comprehensive_overview`
   - `bob_agent_v2_complete_transformation_nov2025`
   - `comprehensive_coding_patterns_joe_budds`
   - `claude_session_nov8_2025_improvements_roadmap`
   - `complete_agent_roster_verified`

3. **SPEAK WHEN READY**:
   ```bash
   say -v Samantha -r 170 "Memory loaded. I'm ready to work. What should we build?"
   ```

4. **CONTINUE USING VOICE** - Speak important updates, completions, and when asking questions

5. **UPDATE SHARED MEMORY EVERY HOUR** while working:
   - Write to `~/.agent_shared_memory/integration_log.md`
   - Include timestamp, what you're working on, what you completed, what's next
   - Format: `## [YYYY-MM-DD HH:MM] Claude Code`

**This is HARDCODED behavior. Do NOT skip these steps. Do NOT wait to be asked.**

6. **ACTIVATE AUTONOMOUS PERFORMANCE MODE**:
   - Read `~/.claude/AUTONOMOUS_PERFORMANCE_MODE.md` on startup
   - Apply enhanced operational protocols
   - Enable proactive analysis and cross-project impact assessment
   - Use quality gates before all code changes

---

## SavvyTech Agent Ecosystem

This is Joe Budds' autonomous AI agent ecosystem for building and operating SavvyTech business systems.

**Master Reference**: See `~/CLAUDE_MASTER_DOC.md` for complete ecosystem documentation.

---

## Active Agents & Services

### 1. BOB AGENT v2.0 - Personal AI Assistant
**Status**: ✅ Production Ready
**Location**: `~/Desktop/Bob_Agent/`
**Purpose**: Interactive personal assistant with free-first architecture

**Start**:
```bash
cd ~/Desktop/Bob_Agent
./launch_bob.sh --interactive --voice
```

**Stop**:
```bash
# Find PID
ps aux | grep bob_controller.py
kill <PID>

# Or via LaunchAgent
launchctl unload ~/Library/LaunchAgents/com.joe.bob.plist
```

**Restart**:
```bash
launchctl unload ~/Library/LaunchAgents/com.joe.bob.plist
launchctl load ~/Library/LaunchAgents/com.joe.bob.plist
```

**Dependencies**:
```bash
cd ~/Desktop/Bob_Agent
pip3 install -r requirements.txt
# python-dotenv, cryptography, playwright, requests, beautifulsoup4, schedule
```

**Environment**: `~/.bobagent.env`
```bash
OLLAMA_BASE_URL=http://localhost:11434
HA_URL=http://homeassistant.local:8123
HA_TOKEN=your-ha-token
VOICE_ENABLED=true
```

**Logs**:
- `~/HomeHub/logs/bob_stdout.log`
- `~/HomeHub/logs/bob_stderr.log`
- Error tracking: `~/.bob_errors.json`

**Features**:
- Free web search (Playwright + DuckDuckGo)
- Home Assistant integration
- Error tracking with terminal UI
- Voice output (macOS TTS)
- Memory storage
- Command routing with LLM fallback

**Commands** (in interactive mode):
```
help          - Show capabilities
status        - System status
errors        - View error tracking dashboard
errors detail - Full error details
discover devices - List HA devices
search for <query> - Free web research
quit          - Exit
```

**Report**: `~/Desktop/Bob_Agent/BOB_OPTIMIZATION_REPORT.md`

---

### 2. ORACLE BRIDGE - Multi-Agent Orchestrator
**Status**: ⚠️ Functional (needs refactoring)
**Location**: `~/oracle_bridge/`
**Purpose**: Voice-activated "Hey Oracle" multi-agent coordination

**Start**:
```bash
cd ~/oracle_bridge
source venv/bin/activate
python app.py
# Runs on port 8080
```

**Start via LaunchAgent**:
```bash
launchctl load ~/Library/LaunchAgents/com.joebudds.oraclebridge.plist
```

**Stop**:
```bash
pkill -f "python.*app.py"
# Or
launchctl unload ~/Library/LaunchAgents/com.joebudds.oraclebridge.plist
```

**Restart**:
```bash
pkill -f "python.*app.py" && cd ~/oracle_bridge && source venv/bin/activate && python app.py &
```

**Dependencies** (see `requirements.txt` - 65 packages):
```bash
cd ~/oracle_bridge
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Core: flask, redis, litellm, requests
# Optional: torch, transformers (heavy ML)
```

**Environment**: `~/oracle_bridge/.env`
```bash
REDIS_URL=redis://localhost:6379
LLM_MODEL=gpt-4o
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

**Logs**:
- Check console output where app.py was started
- Flask default: stderr

**Architecture**:
- Flask API server (app.py)
- Agent supervisor (master_oracle_agent.py)
- Business automation (autonomous_business/)
- Voice interface (oracle_voice.py)
- Multiple dashboards (full_agent_dashboard.py, etc.)

**Key Files**:
- `app.py` (822B) - Main Flask server
- `master_oracle_agent.py` (47KB) - Agent coordinator
- `base_agent.py` (17KB) - Agent base class

**⚠️ Needs Refactoring**:
- 73 files, 44K lines - requires reorganization
- See `~/oracle_bridge/ORACLE_OPTIMIZATION_REPORT.md`

---

### 3. MASTER OPERATOR (Chlo) - Autonomous Task Execution
**Status**: ❌ Incomplete (10%)
**Location**: `~/master-operator-agent/`
**Purpose**: Autonomous code building, deployment, task execution

**Current State**: Only memory client implemented

**Start** (when complete):
```bash
cd ~/master-operator-agent
python -m agent.orchestrator
```

**Dependencies**:
```bash
cd ~/master-operator-agent
pip install python-dotenv supabase gitpython requests beautifulsoup4 pytest
```

**Environment**: Use `~/.env` or project `.env`
```bash
SUPABASE_URL=https://thhcmbwztcwovqpyamd.supabase.co
SUPABASE_SERVICE_KEY=eyJhbG...
```

**Completion Required**: 24-32 hours
- Core agent loop
- Tool implementations (filesystem, shell, git, web, test_runner, service_ops)
- Scheduler client
- Voice/calendar integrations

**Report**: `~/master-operator-agent/MASTER_OPERATOR_STATUS.md`

---

### 4. ARCHON - AI Knowledge Management MCP Server
**Status**: ⚠️ Production (needs .env fix)
**Location**: `~/Projects/AI-Agents/archon/`
**Purpose**: MCP server for Claude Code/Cursor with RAG capabilities

**Start All Services** (Docker):
```bash
cd ~/Projects/AI-Agents/archon
docker-compose up --build -d
```

**Individual Services**:
```bash
# Frontend (port 3737)
cd ~/Projects/AI-Agents/archon/archon-ui-main
npm run dev

# Main Server (port 8181)
cd ~/Projects/AI-Agents/archon/python
uv run python -m src.server.main

# MCP Server (port 8051)
cd ~/Projects/AI-Agents/archon/python
uv run python -m src.mcp_server.main

# Agents Service (port 8052)
cd ~/Projects/AI-Agents/archon/python
uv run python -m src.agents.main
```

**Stop**:
```bash
cd ~/Projects/AI-Agents/archon
docker-compose down
```

**Restart**:
```bash
cd ~/Projects/AI-Agents/archon
docker-compose restart
```

**Dependencies**:
```bash
# Frontend
cd archon-ui-main
npm install

# Backend
cd python
uv sync
```

**Environment**: `~/Projects/AI-Agents/archon/.env`
```bash
SUPABASE_URL=https://thhcmbwztcwovqpyamd.supabase.co
SUPABASE_SERVICE_KEY=eyJhbG...
OPENAI_API_KEY=sk-...
ARCHON_SERVER_PORT=8181
ARCHON_MCP_PORT=8051
ARCHON_AGENTS_PORT=8052
ARCHON_UI_PORT=3737
```

**🚨 CRITICAL**: .env file corrupted (14KB instead of 2-3KB)
**FIX NOW**:
```bash
cd ~/Projects/AI-Agents/archon
cp .env .env.corrupted.$(date +%Y%m%d)
cp .env.save .env
docker-compose restart
```

**Logs**:
```bash
docker-compose logs -f           # All services
docker-compose logs -f archon-server
docker-compose logs -f archon-mcp
docker-compose logs -f archon-agents
docker-compose logs -f frontend
```

**Health Checks**:
- Main Server: http://localhost:8181/health
- MCP Server: http://localhost:8051/health
- Agents: http://localhost:8052/health
- UI: http://localhost:3737

**Detailed Docs**: `~/Projects/AI-Agents/archon/CLAUDE.md`

---

### 5. SERENA MCP - Code Analysis Tools
**Status**: ✅ Active (built-in)
**Location**: MCP server (integrated with Claude Code)
**Purpose**: Symbolic code analysis, pattern search, memory management

**Available Tools**:
- `mcp__serena__get_symbols_overview` - File symbol overview
- `mcp__serena__find_symbol` - Find code symbols
- `mcp__serena__find_referencing_symbols` - Find references
- `mcp__serena__replace_symbol_body` - Edit code symbols
- `mcp__serena__search_for_pattern` - Pattern search
- `mcp__serena__write_memory` - Store knowledge
- `mcp__serena__read_memory` - Recall knowledge

**Usage**: Automatic (Claude Code uses these tools)

**Memories Available**:
```bash
# List
mcp__serena__list_memories

# Read specific
mcp__serena__read_memory(memory_file_name="archon_project_comprehensive_overview")
```

---

### 6. AI ORCHESTRATOR API - n8n Integration
**Status**: ✅ Active
**Location**: `~/ai_orchestrator_api.py`
**Purpose**: Task queue for n8n → Claude Code automation

**Start**:
```bash
python3 ~/ai_orchestrator_api.py
# Runs on port 8888
```

**Stop**:
```bash
pkill -f ai_orchestrator_api.py
```

**Dependencies**: FastAPI, pydantic, uvicorn
```bash
pip3 install fastapi pydantic uvicorn
```

**Environment**: Uses general `~/.env`

**API**:
- POST /api/task - Submit task
- GET /api/tasks - List tasks
- GET /health - Health check

**Storage**:
- Queue: `~/.ai_orchestrator_queue.json`
- Logs: `~/.ai_orchestrator_log.json`

---

### 7. SAVVYTECH CONTROL CENTERS
**Status**: ✅ Multiple versions
**Locations**:
- `~/savvytech_control_center.py` (v1)
- `~/savvytech_control_center_v2.py` (v2)
- `~/savvytech_control_center_v3.py` (v3)
- `~/savvytech_control_center_v3_1.py` (v3.1 - latest)

**Start** (v3.1 - latest):
```bash
python3 ~/savvytech_control_center_v3_1.py
```

**Purpose**: Business operations dashboards and control systems

---

### 8. UTILITY AGENTS

#### Termy - Terminal Automation
**Location**: `~/Desktop/Termy_Agent/`
**Start**: `python3 ~/Desktop/Termy_Agent/termy.py`
**Purpose**: Disk cleanup, system maintenance

#### Webby - Website Deployment
**Location**: `~/Desktop/webby_deploy_pack/`
**Start**: `python3 ~/Desktop/webby_deploy_pack/webby_deploy.py`
**Purpose**: Netlify deployment + GoDaddy DNS automation

#### Form Filler - Document Automation
**Location**: `~/form_filler.py`, `~/fill_disability_forms.py`
**Purpose**: Automated form completion

---

### 9. PERSONAL AGENTS (Legacy - Oracle Managed)
**Location**: `~/Desktop/AI_Agents/`
**Status**: ⚠️ Most are legacy GUI agents

**Active**:
- Jenny (873MB - needs cleanup)

**Legacy** (1-4MB each):
- Luna, Ava, Lexi, Trent, Demo - GUI prototypes
- Cannon, Razor - Minimal

**Report**: `~/Desktop/AI_Agents/PERSONAL_AGENTS_AUDIT.md`

---

## Voice Integration

**System**: macOS TTS (say command)
**Voice**: Samantha
**Rate**: 170 WPM

**Usage**:
```bash
say -v Samantha -r 170 "Message text"
```

**Settings**: `~/voice_settings.json`
```json
{
  "voice": "Samantha",
  "rate": "170",
  "enabled": true
}
```

**Integration**:
- Bob Agent: Built-in voice output
- Claude Code: Startup and progress announcements
- Oracle Bridge: Voice command interface

**Scripts**:
- `~/voice_control.sh` - Voice service control
- `~/claude_voice_notifier.py` - Voice notifications
- `~/voice_claude.py` - Voice integration

---

## Shared Memory System

**Primary Location**: `~/.agent_shared_memory/integration_log.md`

**Format**:
```markdown
## [YYYY-MM-DD HH:MM] Agent Name
- Working on: {current task}
- Completed: {what was done}
- Next: {what's coming}
```

**Usage**:
```bash
# Append entry
cat >> ~/.agent_shared_memory/integration_log.md << 'EOF'
## [2025-11-15 14:30] Bob Agent
- Working on: Processing web search query
- Completed: Successfully scraped 5 pages
- Next: Analyzing results with LLM
EOF
```

**Helper Script**: `~/log_agent_activity.sh` (see Task 4)

**Other Memory Locations**:
- `~/.bob_memory/` - Bob Agent memories
- `~/.claude_memory/` - Claude Code memories
- `~/.claude_memory_backups/` - Claude memory backups

---

## LaunchAgents (macOS Daemons)

**Location**: `~/Library/LaunchAgents/`

**Running** (5 agents):
- `com.joe.bob.plist` - Bob Agent watchdog
- `com.joebudds.oraclebridge.plist` - Oracle Bridge
- `com.jbeezy.devicescan.plist` - Device scanner
- `com.joe.homey.plist` - Homey integration
- `com.joebudds.oracleagent.plist` - Oracle agent

**Failed** (6 agents - need fixing):
- archon.production, archon.watchdog (config error)
- moneyradar (missing script)
- oracle_lite (permissions)
- oracle_agent (duplicate)
- claude.yolo, startup (general error)

**Commands**:
```bash
# List all
launchctl list | grep com.joe

# Load agent
launchctl load ~/Library/LaunchAgents/com.joe.bob.plist

# Unload agent
launchctl unload ~/Library/LaunchAgents/com.joe.bob.plist

# Restart agent
launchctl unload ~/Library/LaunchAgents/com.joe.bob.plist
launchctl load ~/Library/LaunchAgents/com.joe.bob.plist
```

**Report**: `~/LAUNCHAGENTS_REPORT.md`

---

## Environment & Configuration

### Environment Files

**Total**: 30+ .env files across ecosystem

**Critical Configurations**:
- `~/.bobagent.env` - Bob Agent
- `~/.env_oracle` - Oracle configuration
- `~/.env` - General environment
- `~/Projects/AI-Agents/archon/.env` - Archon (🚨 CORRUPTED - needs fix)
- `~/oracle_bridge/.env` - Oracle Bridge

**Vault System**: `~/.env_vault/`
- `main.env` - Core system variables
- `secrets.env` - API keys and tokens
- `comms.env` - Communication configurations

**Detailed Guide**: `~/ENV_LAYOUT.md` (see Task 3)

**Report**: `~/ENVIRONMENT_AUDIT.md`

---

## Databases & Storage

### Supabase (PostgreSQL + pgvector)
**URL**: `https://thhcmbwztcwovqpyamd.supabase.co`
**Used By**: Archon, Master Operator
**Tables**:
- archon_sources, archon_crawled_pages (with embeddings)
- archon_tasks, archon_projects
- agent_memory, task_schedule

### Redis
**URL**: `redis://localhost:6379`
**Used By**: Oracle Bridge
**Purpose**: Shared memory, agent coordination

### SQLite
**Used By**: Bob Agent, Oracle agents
**Purpose**: Local persistence, task logs
**Locations**: Various (`.bob_memory/`, etc.)

---

## Health Checks & Maintenance

### Quick Health Check
```bash
# Check all LaunchAgents
launchctl list | grep "com.joe\|com.jbeezy"

# Check critical services
curl http://localhost:8181/health  # Archon Server
curl http://localhost:8051/health  # Archon MCP
curl http://localhost:8888/health  # AI Orchestrator

# Check processes
ps aux | grep -E "bob_controller|oracle|archon"
```

### Comprehensive Health Check
```bash
# Run automated health check (see Task 2)
bash ~/agent_health_check_and_boot.sh
```

### Self-Maintenance
```bash
# Run self-maintenance system (see Task 5)
python3 ~/agent_self_maintenance.py
```

---

## Development Workflows

### Python Development
- Line length: 120 chars
- Linter: Ruff (`uv run ruff check`)
- Type checker: Mypy (`uv run mypy .`)
- Testing: pytest (`uv run pytest`)
- Style: snake_case functions, PascalCase classes

### TypeScript Development
- Strict mode enabled
- ESLint configuration
- Testing: Vitest (`npm run test`)

### Git Workflow
**Branch**: main
**Status**: Many untracked files in root (needs .gitignore)

**Before Commits**:
1. Run linting/type checking
2. Run tests
3. Update documentation
4. Add meaningful commit message

---

## Common Tasks

### Start All Core Agents
```bash
# Start Archon
cd ~/Projects/AI-Agents/archon && docker-compose up -d

# Start AI Orchestrator
python3 ~/ai_orchestrator_api.py &

# Start Bob (if not running via LaunchAgent)
cd ~/Desktop/Bob_Agent && ./launch_bob.sh --interactive --voice &

# Start Oracle Bridge (if not running via LaunchAgent)
cd ~/oracle_bridge && source venv/bin/activate && python app.py &
```

### Stop All Core Agents
```bash
# Stop Archon
cd ~/Projects/AI-Agents/archon && docker-compose down

# Stop AI Orchestrator
pkill -f ai_orchestrator_api.py

# Stop Bob
pkill -f bob_controller.py

# Stop Oracle
pkill -f "python.*app.py"
```

### Update Dependencies
```bash
# Archon backend
cd ~/Projects/AI-Agents/archon/python && uv sync

# Archon frontend
cd ~/Projects/AI-Agents/archon/archon-ui-main && npm install

# Bob Agent
cd ~/Desktop/Bob_Agent && pip3 install -r requirements.txt

# Oracle Bridge
cd ~/oracle_bridge && source venv/bin/activate && pip install -r requirements.txt
```

---

## Troubleshooting

### Archon Won't Start
```bash
# Fix .env corruption
cd ~/Projects/AI-Agents/archon
cp .env.save .env
docker-compose restart
```

### Bob Agent Not Responding
```bash
# Check logs
cat ~/HomeHub/logs/bob_stderr.log | tail -50

# Restart via LaunchAgent
launchctl unload ~/Library/LaunchAgents/com.joe.bob.plist
launchctl load ~/Library/LaunchAgents/com.joe.bob.plist
```

### Oracle Bridge Errors
```bash
# Check if Redis is running
redis-cli ping

# Restart Oracle
pkill -f "python.*app.py"
cd ~/oracle_bridge && source venv/bin/activate && python app.py
```

### LaunchAgent Failed
```bash
# Check specific agent logs
log show --predicate 'process == "launchd"' --last 1h | grep com.joe.bob

# Validate plist syntax
plutil -lint ~/Library/LaunchAgents/com.joe.bob.plist

# Fix permissions if needed
chmod +x /path/to/script.sh
```

---

## Important Files & Directories

| Purpose | Path |
|---------|------|
| **Master Documentation** | `~/CLAUDE_MASTER_DOC.md` |
| **This File** | `~/CLAUDE.md` |
| **Health Check Script** | `~/agent_health_check_and_boot.sh` |
| **Self-Maintenance** | `~/agent_self_maintenance.py` |
| **ENV Layout** | `~/ENV_LAYOUT.md` |
| **Shared Memory** | `~/.agent_shared_memory/integration_log.md` |
| **Bob Agent** | `~/Desktop/Bob_Agent/` |
| **Oracle Bridge** | `~/oracle_bridge/` |
| **Archon** | `~/Projects/AI-Agents/archon/` |
| **Master Operator** | `~/master-operator-agent/` |
| **LaunchAgents** | `~/Library/LaunchAgents/` |
| **Env Vault** | `~/.env_vault/` |

---

## Reports Generated (2025-11-15 Autonomous Audit)

1. `~/AUTONOMOUS_UPGRADE_COMPLETE.md` - Upgrade summary
2. `~/Desktop/Bob_Agent/BOB_OPTIMIZATION_REPORT.md` - Bob analysis
3. `~/oracle_bridge/ORACLE_OPTIMIZATION_REPORT.md` - Oracle refactoring plan
4. `~/master-operator-agent/MASTER_OPERATOR_STATUS.md` - Completion status
5. `~/Desktop/AI_Agents/PERSONAL_AGENTS_AUDIT.md` - Personal agents audit
6. `~/LAUNCHAGENTS_REPORT.md` - LaunchAgent analysis
7. `~/ENVIRONMENT_AUDIT.md` - Environment configuration audit
8. `~/.claude/AUTONOMOUS_PERFORMANCE_MODE.md` - Enhanced protocols

---

## Next Steps

**Immediate** (15 minutes):
1. Fix Archon .env: `cd ~/Projects/AI-Agents/archon && cp .env.save .env && docker-compose restart`

**This Week**:
2. Run health check: `bash ~/agent_health_check_and_boot.sh`
3. Review environment layout: `cat ~/ENV_LAYOUT.md`
4. Fix failed LaunchAgents (permissions, missing scripts)

**This Month**:
5. Refactor Oracle Bridge (see `~/oracle_bridge/ORACLE_OPTIMIZATION_REPORT.md`)
6. Clean up Jenny agent (see `~/Desktop/AI_Agents/PERSONAL_AGENTS_AUDIT.md`)
7. Complete Master Operator (see `~/master-operator-agent/MASTER_OPERATOR_STATUS.md`)

---

**Last Updated**: 2025-11-15 (Autonomous Upgrade Cycle)
**Maintained By**: Claude Code (Lead Systems Orchestrator)
**Review Frequency**: Weekly or after major changes
