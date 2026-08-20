# CLAUDE MASTER DOCUMENTATION
**Joe Budds' Complete AI Ecosystem**

**Generated**: 2025-11-15 (Autonomous Upgrade Cycle)
**Version**: 1.0.0
**Last Audit**: Full autonomous system scan

---

## 📋 Table of Contents

1. [Executive Summary](#executive-summary)
2. [System Architecture](#system-architecture)
3. [Active Projects](#active-projects)
4. [Agent Ecosystem](#agent-ecosystem)
5. [Infrastructure](#infrastructure)
6. [Configuration Management](#configuration-management)
7. [Development Workflows](#development-workflows)
8. [Maintenance & Operations](#maintenance--operations)
9. [Optimization Roadmap](#optimization-roadmap)
10. [Quick Reference](#quick-reference)

---

## Executive Summary

### System Overview

This is Joe Budds' personal AI development environment containing **15+ active projects**, **12+ AI agents**, and complete automation infrastructure for building autonomous business systems.

**Core Focus**: AI-powered automation, multi-agent orchestration, and autonomous business operations

### Health Status (2025-11-15)

| Component | Status | Priority |
|-----------|--------|----------|
| **Bob Agent v2.0** | ✅ Production Ready | - |
| **Archon (MCP Server)** | ⚠️ Needs .env fix | HIGH |
| **Oracle Bridge** | ⚠️ Needs refactoring | HIGH |
| **Master Operator** | ❌ Incomplete (10%) | MEDIUM |
| **Personal Agents** | ⚠️ Legacy/Mixed | MEDIUM |
| **LaunchAgents** | ⚠️ 5 running, 6 failed | HIGH |
| **Environment Configs** | ⚠️ Needs cleanup | HIGH |

### Critical Actions Needed

1. 🚨 **Fix Archon .env** - Corrupted with Guardian text (restore from backup)
2. 🚨 **Refactor Oracle Bridge** - 44K lines, 60+ files, needs reorganization
3. ⚠️ **Consolidate Jenny Agent** - 873MB, multiple versions, cleanup needed
4. ⚠️ **Fix Failed LaunchAgents** - 6 agents failing (permissions, missing scripts)
5. ⚠️ **Remove Duplicate Configs** - 30+ .env files, consolidation needed

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE LAYER                      │
│  Voice (macOS TTS) │ CLI │ Web UI │ n8n Workflows           │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────┴────────────────────────────────────────────┐
│              ORCHESTRATION LAYER                            │
│  Claude Code │ Oracle Bridge │ AI Orchestrator API          │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────┴────────────────────────────────────────────┐
│                 AGENT LAYER                                  │
│  Bob │ Jenny │ Master Operator │ Luna │ Ava │ Others        │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────┴────────────────────────────────────────────┐
│              CAPABILITY LAYER                                │
│  Archon MCP │ Voice │ Browser │ Home Assistant │ Tools      │
└────────────────┬────────────────────────────────────────────┘
                 │
┌────────────────┴────────────────────────────────────────────┐
│               INFRASTRUCTURE LAYER                           │
│  Supabase │ Redis │ SQLite │ File System │ macOS Services  │
└─────────────────────────────────────────────────────────────┘
```

### Core Philosophy

1. **Free-First**: Use open-source, local-first solutions (Ollama, Playwright, etc.)
2. **Self-Healing**: Agents restart automatically, memory persists across crashes
3. **Voice-Enabled**: macOS TTS integration throughout (170 WPM, Samantha)
4. **Memory-Centric**: Shared memory via Redis, Supabase, and file system
5. **Microservices**: Clean separation of concerns, Docker where appropriate

---

## Active Projects

### Tier 1: Production Systems

#### 1. **Archon** - AI Knowledge Management MCP Server
- **Location**: `~/Projects/AI-Agents/archon/`
- **Status**: ✅ Production (⚠️ .env corrupted)
- **Purpose**: MCP server for Claude Code/Cursor/Windsurf with RAG capabilities
- **Tech**: FastAPI + React + PydanticAI + Supabase + pgvector
- **Services**: 4 microservices (Server 8181, MCP 8051, Agents 8052, UI 3737)
- **Launch**: `docker-compose up --build -d`
- **Docs**: See `archon/CLAUDE.md` and memory `archon_project_comprehensive_overview`
- **Critical Issue**: `.env` file corrupted (14KB instead of 2-3KB)
  - **Fix**: `cd ~/Projects/AI-Agents/archon && cp .env.save .env`

#### 2. **Bob Agent v2.0** - Personal AI Assistant
- **Location**: `~/Desktop/Bob_Agent/`
- **Status**: ✅ Production Ready (Excellent)
- **Purpose**: Interactive personal assistant with error tracking
- **Tech**: Python + Playwright + Ollama + Home Assistant
- **Features**: Free web search, voice output, HA control, error tracking
- **Launch**: `cd ~/Desktop/Bob_Agent && ./launch_bob.sh --interactive --voice`
- **Architecture**: 2,545 lines, 19 modules, clean design
- **Report**: See `Desktop/Bob_Agent/BOB_OPTIMIZATION_REPORT.md`

#### 3. **Oracle Bridge** - Multi-Agent Orchestrator
- **Location**: `~/oracle_bridge/`
- **Status**: ⚠️ Functional but needs refactoring
- **Purpose**: Voice-activated "Hey Oracle" agent orchestration
- **Tech**: Flask + FastAPI + Streamlit + Redis + LiteLLM
- **Features**: ReAct loop, voice interface, agent supervisor, business automation
- **Architecture**: 44,179 lines, 73 files (⚠️ NEEDS CLEANUP)
- **Launch**: `cd ~/oracle_bridge && python app.py`
- **Report**: See `oracle_bridge/ORACLE_OPTIMIZATION_REPORT.md`
- **Critical**: Needs 48-76 hours of refactoring (file reorganization, dependency reduction)

### Tier 2: Active Development

#### 4. **AI Orchestrator API** - n8n Integration
- **Location**: `~/ai_orchestrator_api.py`
- **Status**: ✅ Active
- **Purpose**: Task queue for n8n → Claude Code automation
- **Tech**: FastAPI + JSON storage
- **Port**: 8888
- **Launch**: `python3 ai_orchestrator_api.py`

#### 5. **Master Operator Agent** - Autonomous Task Execution
- **Location**: `~/master-operator-agent/`
- **Status**: ❌ Incomplete (10%)
- **Purpose**: Autonomous code building, deployment, task execution
- **Tech**: Python + Supabase + planned tool integrations
- **Completed**: Memory client (130 lines)
- **Remaining**: Core agent loop, tools (filesystem, git, shell, etc.)
- **Effort**: 24-32 hours to complete
- **Report**: See `master-operator-agent/MASTER_OPERATOR_STATUS.md`

#### 6. **AI-Relay** - Multi-AI Orchestration
- **Location**: `~/Projects/RelayApp/AI-Relay/`
- **Status**: ✅ Active
- **Purpose**: Streamlit-based multi-agent orchestration
- **Tech**: Streamlit + Python
- **Launch**: `cd AI-Relay && python orchestrator.py`

### Tier 3: Utilities & Support

#### 7. **SavvyTech Control Centers** (v1-v3.1)
- **Location**: `~/savvytech_control_center*.py`
- **Purpose**: Business operations dashboards
- **Versions**: 4 iterations (v3.1 latest)

#### 8. **Webby** - Website Deployment Agent
- **Location**: `~/Desktop/webby_deploy_pack/`
- **Purpose**: Automated Netlify deployment + GoDaddy DNS
- **Status**: ✅ Production ready

#### 9. **Termy** - Terminal Automation
- **Location**: `~/Desktop/Termy_Agent/`
- **Purpose**: Disk cleanup, system maintenance
- **Status**: ✅ Active

#### 10. **Form Filler** - Document Automation
- **Location**: `~/{form_filler.py, fill_disability_forms.py}`
- **Purpose**: Automated form completion

### Archived/Legacy

- **OrderBot**: VAPI.ai phone agent for restaurants (ready for outreach)
- **Lead Generator**: Business lead discovery and outreach
- **Network Automation**: WiFi optimization, HA device discovery
- **HomeHub**: Smart home integration suite

---

## Agent Ecosystem

### Production Agents

#### **Bob Agent v2.0** 🤖 (Best-in-Class)
- **Role**: Personal assistant
- **Features**: Web search, voice, HA, error tracking
- **Status**: ✅ Production ready
- **Files**: 19 Python modules, 2,545 lines
- **Quality**: Excellent (no TODOs, clean architecture)
- **Dependencies**: 7 packages (lightweight)

#### **Oracle Master** 🔮
- **Role**: Multi-agent coordinator
- **Features**: Voice activation, ReAct loop, agent supervision
- **Status**: ⚠️ Functional, needs refactor
- **Files**: 73 Python files, 44,179 lines
- **Quality**: Feature-rich but disorganized
- **Dependencies**: 65 packages (⚠️ HEAVY)

### Personal Agents (Oracle-Managed)

| Agent | Size | Status | Purpose |
|-------|------|--------|---------|
| **Jenny** | 873MB | ⚠️ Active, needs cleanup | Task management, email campaigns |
| **Luna** | 1.2MB | Legacy GUI | Creative inspiration |
| **Ava** | 4.1MB | Legacy GUI | Data analysis, strategic planning |
| **Lexi** | 1.8MB | Legacy GUI | Social media, marketing |
| **Trent** | 2.7MB | Legacy GUI | Life coaching, guidance |
| **Demo** | 4.0MB | Legacy GUI | Education, tutorials |
| **Cannon** | Small | Minimal | Specialized (TBD) |
| **Razor** | Small | Minimal | Specialized (TBD) |

**Recommendation**: Consolidate into Bob v2.0 or archive most. Jenny is the only active non-Bob agent.

### Special Purpose Agents

- **Termy**: Terminal operations and cleanup
- **Webby**: Website deployment automation
- **Key Butler**: Credential management

**Report**: See `Desktop/AI_Agents/PERSONAL_AGENTS_AUDIT.md`

---

## Infrastructure

### Services & Ports

| Service | Port | Status | Purpose |
|---------|------|--------|---------|
| Archon Server | 8181 | ⚠️ Needs restart | Main FastAPI server |
| Archon MCP | 8051 | ⚠️ Needs restart | MCP protocol server |
| Archon Agents | 8052 | ⚠️ Needs restart | PydanticAI agents |
| Archon UI | 3737 | ⚠️ Needs restart | React frontend |
| AI Orchestrator | 8888 | ✅ Active | n8n integration |
| Oracle Bridge | 8080 | ✅ Active | Main Oracle server |
| Bob Agent | N/A | ✅ Active | CLI/daemon |

### Databases

#### **Supabase** (PostgreSQL + pgvector)
- **URL**: `https://thhcmbwztcwovqpyamd.supabase.co`
- **Used By**: Archon, Master Operator
- **Tables**: archon_sources, archon_crawled_pages (with embeddings), archon_tasks, archon_projects, agent_memory, task_schedule
- **Extensions**: pgvector for semantic search

#### **Redis**
- **Used By**: Oracle Bridge
- **Purpose**: Shared memory, agent coordination

#### **SQLite**
- **Used By**: Bob Agent, Oracle agents
- **Purpose**: Local persistence, task logs, memory

### File System

#### **Shared Memory**
- `~/.agent_shared_memory/integration_log.md` - Cross-agent coordination
- `~/.bob_memory/` - Bob Agent memories
- `~/.claude_memory/` - Claude Code memories

#### **Logs**
- `~/HomeHub/logs/` - Bob watchdog logs
- Various agent-specific log files

#### **Credentials**
- `~/.env_vault/` - Centralized vault (main, secrets, comms)
- `~/.bobagent.env` - Bob configuration
- `~/.env_oracle` - Oracle configuration
- Project-specific `.env` files (30+)

### LaunchAgents (macOS Daemons)

**Total Installed**: 27 plist files

**Running** (5):
- com.joe.bob - Bob Agent watchdog
- com.joebudds.oraclebridge - Oracle Bridge
- com.jbeezy.devicescan - Device scanner
- com.joe.homey - Homey integration
- com.joebudds.oracleagent - Oracle agent

**Failed** (6):
- archon.production, archon.watchdog (config error)
- moneyradar (missing script)
- oracle_lite (permissions)
- oracle_agent (duplicate)
- claude.yolo, startup (general error)

**Inactive** (11): jenny.watchdog, client.boot, homehub, toolscheatsheet, patent boards, etc.

**Report**: See `LAUNCHAGENTS_REPORT.md`

---

## Configuration Management

### Environment Variables

**Total .env Files**: 30+ across ecosystem

#### **Critical Configurations**

**Archon** (`~/Projects/AI-Agents/archon/.env`):
```bash
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=eyJhbG...
OPENAI_API_KEY=sk-...
ARCHON_SERVER_PORT=8181
ARCHON_MCP_PORT=8051
ARCHON_AGENTS_PORT=8052
ARCHON_UI_PORT=3737
```
🚨 **CORRUPTED** - 14KB file, restore from .env.save

**Bob Agent** (`~/.bobagent.env`):
```bash
OLLAMA_BASE_URL=http://localhost:11434
HA_URL=http://homeassistant.local:8123
HA_TOKEN=your-token
VOICE_ENABLED=true
```

**Oracle Bridge** (`~/oracle_bridge/.env`):
```bash
REDIS_URL=redis://localhost:6379
LLM_MODEL=gpt-4o
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
```

#### **Vault System** (`~/.env_vault/`)
- `main.env` - Core system variables
- `secrets.env` - API keys and tokens
- `comms.env` - Communication configurations

**Report**: See `ENVIRONMENT_AUDIT.md`

### Git Status (2025-11-15)

**Branch**: main
**Untracked**: 100+ files in root directory (agents, scripts, docs)
**Recommendation**: Create `.gitignore`, organize into directories

---

## Development Workflows

### Common Commands

#### **Archon Development**
```bash
# Frontend
cd ~/Projects/AI-Agents/archon/archon-ui-main
npm run dev              # Development server
npm run build            # Production build
npm run test             # Run tests
npm run lint             # Lint code

# Backend
cd ~/Projects/AI-Agents/archon/python
uv sync                  # Install dependencies
uv run pytest            # Run tests
uv run ruff check        # Lint
uv run mypy .            # Type check
uv run python -m src.server.main      # Run server
uv run python -m src.mcp_server.main  # Run MCP

# Docker
cd ~/Projects/AI-Agents/archon
docker-compose up --build -d    # Start all
docker-compose logs -f          # View logs
docker-compose down             # Stop all
```

#### **Bob Agent**
```bash
cd ~/Desktop/Bob_Agent
./launch_bob.sh --interactive --voice   # Interactive mode
python3 bob_controller.py status        # Check status
python3 bob_controller.py errors        # View errors
```

#### **Oracle Bridge**
```bash
cd ~/oracle_bridge
source venv/bin/activate
python app.py                    # Start server
python master_oracle_agent.py    # Run Oracle
```

### Coding Standards

**Python**:
- Line length: 120 chars
- Linter: Ruff
- Type checker: Mypy
- Style: snake_case functions, PascalCase classes
- Dataclasses for data structures
- Async/await for I/O operations

**TypeScript**:
- Strict mode enabled
- ESLint configuration
- camelCase for functions, PascalCase for components

### Testing

**Python**: pytest
```bash
uv run pytest                    # All tests
uv run pytest tests/test_foo.py  # Single file
uv run pytest -v                 # Verbose
uv run pytest --cov              # Coverage
```

**TypeScript**: Vitest
```bash
npm run test                     # All tests
npm run test:coverage            # With coverage
```

---

## Maintenance & Operations

### Daily Operations

**Morning Startup**:
1. Check LaunchAgent status: `launchctl list | grep com.joe`
2. Verify critical services: Archon, Bob, Oracle
3. Review logs for overnight errors
4. Update shared memory with day's plan

**Evening Shutdown**:
1. Commit any code changes
2. Update shared memory with accomplishments
3. Back up critical .env files
4. Review error logs from Bob Agent

### Weekly Maintenance

**Monday**:
- Review all agent error logs
- Clear resolved errors from Bob Agent
- Check disk space (Termy Agent)
- Update dependencies if needed

**Friday**:
- Full system health check
- Back up Supabase data
- Rotate API keys if scheduled
- Plan next week's priorities

### Monthly Maintenance

- **Update all dependencies** (uv sync, npm update)
- **Security audit** of .env files
- **Performance profiling** of agents
- **Clean up temp files and logs**
- **Review and archive old projects**
- **Update CLAUDE_MASTER_DOC.md**

### Emergency Procedures

**If Archon Fails**:
```bash
cd ~/Projects/AI-Agents/archon
docker-compose down
cp .env.save .env  # Restore config
docker-compose up --build -d
```

**If Bob Agent Fails**:
```bash
launchctl unload ~/Library/LaunchAgents/com.joe.bob.plist
# Fix issue
launchctl load ~/Library/LaunchAgents/com.joe.bob.plist
```

**If Oracle Bridge Fails**:
```bash
pkill -f oracle_bridge
cd ~/oracle_bridge
python app.py
```

---

## Optimization Roadmap

### Immediate (This Week)

#### Priority 1: Archon .env Restoration
**Effort**: 15 minutes
**Impact**: HIGH (unblocks Archon development)
```bash
cd ~/Projects/AI-Agents/archon
cp .env .env.corrupted.$(date +%Y%m%d)
cp .env.save .env
docker-compose restart
```

#### Priority 2: Fix Failed LaunchAgents
**Effort**: 1-2 hours
**Impact**: HIGH (system stability)
- Fix permissions on oracle_lite script
- Remove duplicate Oracle agents
- Investigate missing scripts
- Update Archon LaunchAgent configs

#### Priority 3: Oracle Bridge File Reorganization
**Effort**: 4-6 hours
**Impact**: HIGH (maintainability)
- Create src/ directory structure
- Move 60+ files into organized folders
- Remove duplicates
- Document entry points

### Short-term (This Month)

#### Priority 4: Jenny Agent Consolidation
**Effort**: 3-4 hours
**Impact**: MEDIUM (873MB → ~200MB)
- Identify active version
- Archive old versions
- Clean up dependencies
- Document functionality

#### Priority 5: Environment Centralization
**Effort**: 4-6 hours
**Impact**: MEDIUM (security & organization)
- Expand ~/.env_vault/ pattern
- Remove duplicate .env files
- Create secret rotation schedule

#### Priority 6: Complete Master Operator
**Effort**: 24-32 hours
**Impact**: MEDIUM (new capability)
- Implement core agent loop
- Build tool implementations
- Add scheduler client
- Create tests

### Long-term (This Quarter)

#### Priority 7: Personal Agent Migration
**Effort**: 16-24 hours
**Impact**: LOW-MEDIUM
- Migrate Luna/Ava/Lexi/Trent to Bob v2.0 or archive
- Update Oracle Bridge registry
- Document retirement decisions

#### Priority 8: Oracle Bridge Dependency Reduction
**Effort**: 12-16 hours
**Impact**: MEDIUM (performance & size)
- Split requirements into core/optional
- Remove heavy ML dependencies if unused
- Implement lazy loading
- Reduce Docker image size

#### Priority 9: Testing Infrastructure
**Effort**: 20-30 hours
**Impact**: HIGH (quality & confidence)
- Add pytest tests for Bob Agent
- Integration tests for Archon
- E2E tests for Oracle coordination
- CI/CD pipeline setup

---

## Quick Reference

### Key File Locations

| Purpose | Path |
|---------|------|
| **Archon MCP Server** | `~/Projects/AI-Agents/archon/` |
| **Bob Agent** | `~/Desktop/Bob_Agent/` |
| **Oracle Bridge** | `~/oracle_bridge/` |
| **Master Operator** | `~/master-operator-agent/` |
| **Personal Agents** | `~/Desktop/AI_Agents/` |
| **Claude Code Settings** | `~/.claude/settings.json` |
| **Claude Code Hooks** | `~/.claude/hooks/` |
| **Shared Memory** | `~/.agent_shared_memory/` |
| **Environment Vault** | `~/.env_vault/` |
| **LaunchAgents** | `~/Library/LaunchAgents/` |

### Key Commands

| Task | Command |
|------|---------|
| **Start Archon** | `cd ~/Projects/AI-Agents/archon && docker-compose up -d` |
| **Start Bob** | `cd ~/Desktop/Bob_Agent && ./launch_bob.sh --interactive --voice` |
| **Check LaunchAgents** | `launchctl list \| grep com.joe` |
| **View Bob Errors** | Bob interactive mode: `errors` |
| **Health Check** | Run scripts in reports (various locations) |

### Critical Passwords & Keys

**Stored In**:
- `~/.env_vault/secrets.env` - Primary secrets
- Project-specific `.env` files - Service credentials
- `~/.bobagent.env` - Bob configuration
- Archon `.env` - Supabase, OpenAI keys

**Never Commit**: Any .env file to git

### Emergency Contacts

- **Supabase Dashboard**: https://supabase.com/dashboard
- **Claude Code Docs**: https://docs.claude.com/claude-code
- **Archon Repo**: https://github.com/coleam00/archon

---

## Appendices

### Generated Reports (2025-11-15)

1. **Bob Agent Optimization**: `~/Desktop/Bob_Agent/BOB_OPTIMIZATION_REPORT.md`
2. **Oracle Bridge Optimization**: `~/oracle_bridge/ORACLE_OPTIMIZATION_REPORT.md`
3. **Master Operator Status**: `~/master-operator-agent/MASTER_OPERATOR_STATUS.md`
4. **Personal Agents Audit**: `~/Desktop/AI_Agents/PERSONAL_AGENTS_AUDIT.md`
5. **LaunchAgents Report**: `~/LAUNCHAGENTS_REPORT.md`
6. **Environment Audit**: `~/ENVIRONMENT_AUDIT.md`
7. **Autonomous Performance Mode**: `~/.claude/AUTONOMOUS_PERFORMANCE_MODE.md`

### Memory Files (Serena MCP)

- `archon_project_comprehensive_overview` - Archon architecture & Supabase
- `bob_agent_v2_complete_transformation_nov2025` - Bob v2.0 details
- `comprehensive_coding_patterns_joe_budds` - Coding standards
- `claude_session_nov8_2025_improvements_roadmap` - Improvement plans
- `complete_agent_roster_verified` - All agents cataloged
- `serena_capability_upgrades_needed` - Serena upgrade roadmap

---

**Document Version**: 1.0.0
**Last Updated**: 2025-11-15
**Generated By**: Claude Code (Autonomous Upgrade Cycle)
**Next Review**: Weekly or after major changes

**This is a living document. Update after significant system changes.**
