# SavvyTech Automations - Complete Business & Technical Documentation
**For: Claude AI Context Transfer**
**Generated**: October 6, 2025
**Owner**: Joe Budds
**Company**: SavvyTech Automations

---

# TABLE OF CONTENTS

1. [Business Overview](#1-business-overview)
2. [Current Agent Inventory](#2-current-agent-inventory)
3. [Technical Environment](#3-technical-environment)
4. [Home Assistant Project](#4-home-assistant-project)
5. [Priority Capabilities Needed](#5-priority-capabilities-needed)
6. [Current Workflows](#6-current-workflows)
7. [Immediate Priorities](#7-immediate-priorities)
8. [File Structure & Locations](#8-file-structure--locations)

---

# 1. BUSINESS OVERVIEW

## 1.1 Business Model & Vision

**Company Name**: SavvyTech Automations
**Website**: https://savvytechautomations.com
**Business Type**: AI Agent Services Company
**Launch Status**: Pre-launch (launching ASAP)

### Core Business Model
- **AI-powered automation services** for businesses and individuals
- **Multi-department AI agent workforce** operating autonomously
- **Revenue-first focus**: Every decision prioritizes money-making capabilities
- **Target**: $500/month minimum to unlock advanced tools, scaling to $10K+/month

### Value Proposition
"We automate everything that can be automated using AI agents that think, learn, and execute autonomously."

## 1.2 Revenue Urgency & Monetization Strategy

### Critical Timeline
- **IMMEDIATE NEED**: Generate first revenue within 1-2 weeks
- **Short-term Goal**: $500/month (unlocks premium API access)
- **Medium-term Goal**: $2,000/month (sustainable operations)
- **Long-term Goal**: $10,000+/month (scale team and infrastructure)

### Revenue Streams (Priority Order)

#### 1. **LocalBook** - Local Service Booking App (TOP PRIORITY)
- **Target Market**: Local service businesses (salons, mechanics, contractors)
- **Pricing**: $79/month per business
- **Goal**: 5 customers = $395/month
- **Tech Stack**: 100% free (React, Supabase, Vercel, Stripe)
- **Status**: React project initialized, needs completion THIS WEEK
- **Path**: `~/archon/autonomous-agents/apps/booking-app/`

#### 2. **Home Assistant Hub Product**
- **Target Market**: Smart home enthusiasts, property managers
- **Pricing**: $199 one-time + optional $9.99/month for cloud features
- **Value**: Auto-discover 100+ devices, zero-config setup
- **Status**: Core HA setup complete, needs product packaging
- **Competitive Edge**: Simplest setup on market

#### 3. **Guardian Multi-Care Monitoring Platform**
- **Target Market**: Elder care facilities, childcare centers, healthcare
- **Products**: Smart cameras, GPS trackers, vital sign wearables
- **Business Stage**: Business plan development (Lexi + Trent agents)
- **Patent Opportunity**: Magnetic mounting, multi-generational monitoring
- **Revenue Potential**: High (hardware + subscription)

#### 4. **AI Agent Consulting Services**
- **Target Market**: Small businesses needing automation
- **Pricing**: $500-2,000 per project
- **Services**: Form automation, data entry, API integration, web scraping
- **Status**: Ready to launch, need first client

#### 5. **White-Label AI Solutions**
- **Target Market**: Agencies, SaaS companies
- **Pricing**: Custom (starting $1,000/month)
- **Offering**: Pre-built agent systems, custom integrations

## 1.3 Department Structure

### Department 1: **PRODUCTION** (Building & Development)
**Mission**: Build apps, software, databases, and automation systems for clients

**Agents**:
- **Product Engineer Agent** (`archon/autonomous-agents/src/agents/product_engineer.py`)
  - Designs features and writes production code
  - Manages deployments and version control
  - Tech stack: React, Python, Node.js, FastAPI

- **Bob the Builder Agent** (`Desktop/AI_Agents/Bob/`)
  - Specializes in coded automations and technical implementations
  - Home Assistant automation expert
  - Infrastructure and DevOps tasks

**Capabilities**:
- Full-stack web development
- Database design and optimization
- API development and integration
- DevOps and deployment automation
- Code review and quality assurance

**Tech Stack**:
- **Frontend**: React 18, TypeScript, Vite, TailwindCSS
- **Backend**: Python 3.13, FastAPI, Node.js 22.12
- **Databases**: Supabase (PostgreSQL + pgvector), Pinecone (vector DB)
- **Deployment**: Vercel (frontend), Railway/Heroku (backend), Docker

### Department 2: **CREATIVE** (Content & Ideation)
**Mission**: Generate content, ideate products, create marketing materials

**Agents**:
- **Jenny** (`Desktop/AI_Agents/Jenny/`)
  - Primary creative director
  - Content generation (blogs, social media, emails)
  - Marketing copy and ad campaigns

- **Luna** (`Desktop/AI_Agents/Luna/`)
  - Visual concept development
  - Brand strategy and positioning
  - Customer persona development

- **Ava** (`Desktop/AI_Agents/Ava/`)
  - Customer success specialist
  - Support documentation and FAQs
  - User onboarding flows

- **Lexi** (`Desktop/AI_Agents/Lexi/`)
  - Business plan writer
  - Product documentation specialist
  - Patent and legal documentation

**Capabilities**:
- Blog posts, articles, case studies
- Social media content (Twitter, LinkedIn, Instagram)
- Email marketing campaigns
- Product descriptions and landing pages
- Business plans and pitch decks
- Brand voice and messaging
- Visual mockups and wireframes

**Tech Stack**:
- **AI Models**: Claude (Anthropic), GPT-4 (OpenAI), Gemini
- **Design**: Figma, Canva (via automation)
- **Content Mgmt**: Markdown, Git, Notion

### Department 3: **RESEARCH** (Data & Intelligence)
**Mission**: Web scraping, data gathering, market research, competitive analysis

**Agents**:
- **Sales Director Agent** (`archon/autonomous-agents/src/agents/sales_director.py`)
  - Market research and lead generation
  - Competitive analysis
  - Sales strategy development

- **Trent** (`Desktop/AI_Agents/Trent/`)
  - Financial modeling and projections
  - Market analysis and research
  - Data analysis specialist

- **Demo** (`Desktop/AI_Agents/Demo/`)
  - Web scraping and data extraction
  - API exploration and testing
  - Research automation

**Capabilities**:
- Web scraping (Selenium, Playwright, BeautifulSoup)
- Data extraction from websites and APIs
- Competitive intelligence gathering
- Market trend analysis
- Lead generation and qualification
- Financial data modeling
- Research report generation

**Tech Stack**:
- **Scraping**: Crawl4AI, Selenium, Playwright, BeautifulSoup
- **Data Processing**: Pandas, NumPy
- **APIs**: Serp API, Perplexity API, custom REST APIs
- **Storage**: PostgreSQL, JSON, CSV exports

## 1.4 Connected Brain System Architecture

### Shared Knowledge Base
All agents access a unified knowledge repository powered by **Archon** platform.

**Components**:
1. **Supabase PostgreSQL Database**
   - URL: `https://thhccnbwztcwovqpyamd.supabase.co`
   - Stores: Projects, tasks, documents, code examples
   - Features: Real-time subscriptions, row-level security

2. **Pinecone Vector Database**
   - API Key: `pcsk_6r3bz1_P8rL37gjnagN4aVsi57iWVvxyGvqPTf4oCeWP1AyhFmiAQL1NN1QchP3X8seWBG`
   - Stores: Embeddings for semantic search
   - Use Case: Find similar code, documentation, patterns

3. **Archon Knowledge Management System**
   - Location: `~/archon/`
   - Frontend: React UI on port 3737
   - Backend: FastAPI server on port 8181
   - MCP Server: port 8051 (Model Context Protocol)
   - Agents Service: port 8052

### How Agents Share Knowledge

**Real-time Communication**:
- Socket.IO events for instant updates
- WebSocket connections for live progress tracking
- Shared task queues in Supabase

**Knowledge Flow**:
```
Agent Observation → Store in Supabase → Create Embedding → Index in Pinecone
                                ↓
                        Other Agents Query
                                ↓
                    Relevant Knowledge Returned
```

**Example Use Cases**:
- Product Engineer learns API pattern → All agents can use it
- Research agent finds market data → Creative agents use for content
- Bob solves HA automation → Knowledge indexed for future similar tasks

## 1.5 Market Gap Prediction Database

### Concept
**Algorithmic Market Intelligence System** that predicts opportunities before competitors.

**Current Status**: Design phase, not yet implemented

**Planned Architecture**:

1. **Data Collection Layer**
   - Scrape 100+ startup databases (Product Hunt, Indie Hackers, Hacker News)
   - Monitor trending GitHub repos
   - Track funding announcements (Crunchbase, AngelList)
   - Social media sentiment analysis (Twitter, Reddit, LinkedIn)

2. **Pattern Recognition Engine**
   - Identify gaps: "People want X but no one offers Y"
   - Detect dying products: "Complaints increasing, no updates"
   - Spot emerging trends: "Sudden spike in searches for Z"
   - Cross-reference with capabilities: "We can build this NOW"

3. **Opportunity Scoring Algorithm**
   ```python
   score = (
       market_demand * 0.3 +
       competition_weakness * 0.25 +
       buildability_score * 0.20 +
       time_to_market * 0.15 +
       revenue_potential * 0.10
   )
   ```

4. **Automated Validation**
   - Test demand: Run micro-ads, landing pages
   - Check feasibility: Agent capability assessment
   - Estimate effort: Break down into tasks
   - Project revenue: Financial modeling (Trent agent)

**Implementation Priority**: HIGH (after first revenue)

**Tech Stack**:
- Python for data pipeline
- Supabase for storage
- Pinecone for pattern matching
- GPT-4 for opportunity analysis
- Scheduled jobs (cron) for continuous monitoring

---

# 2. CURRENT AGENT INVENTORY

## 2.1 Agent Registry (40+ Agents)

### **OPERATIONAL AGENTS** (Ready for Production)

#### **Archon Platform Agents** (`~/archon/python/src/agents/`)

| Agent Name | Provider | Primary Function | API Keys Used | Status |
|-----------|----------|------------------|---------------|---------|
| **Oracle** | Claude (Anthropic) | Master orchestrator, strategic planning | ANTHROPIC_API_KEY | ✅ Operational |
| **Omni** | Claude | Universal problem solver, general tasks | ANTHROPIC_API_KEY | ✅ Operational |
| **Product Engineer** | Claude | Full-stack development, code generation | ANTHROPIC_API_KEY | ✅ Operational |
| **Sales Director** | Claude | Market research, sales strategy | ANTHROPIC_API_KEY | ✅ Operational |
| **Communication Director** | Claude | SMS, email, notifications, coordination | ANTHROPIC_API_KEY, TWILIO | ✅ Operational |
| **Bob the Builder** | Claude | Automation specialist, HA integrations | ANTHROPIC_API_KEY | ✅ Operational |
| **Home Assistant Specialist** | Claude | HA device management, automations | ANTHROPIC_API_KEY | ✅ Operational |
| **Browser Navigator** | Claude | Web automation, form filling | ANTHROPIC_API_KEY | ✅ Operational |
| **Account Setup Agent** | Claude | Account creation, onboarding automation | ANTHROPIC_API_KEY | ✅ Operational |
| **Plaid Setup Agent** | Claude | Financial API integration | ANTHROPIC_API_KEY | ✅ Operational |
| **Universal Automation Agent** | Claude | General automation tasks | ANTHROPIC_API_KEY | ✅ Operational |

#### **Revenue-Focused Agents** (`~/archon/python/src/agents/`)

| Agent Name | Provider | Primary Function | API Keys Used | Status |
|-----------|----------|------------------|---------------|---------|
| **Website Affiliate Analyzer** | GPT-4 | Analyze sites for monetization | OPENAI_API_KEY | ✅ Operational |
| **Content Marketing Specialist** | GPT-4 | SEO content, blog posts | OPENAI_API_KEY | ✅ Operational |
| **SEO Content Factory** | GPT-4 | Mass content generation | OPENAI_API_KEY | ✅ Operational |
| **Amazon Affiliate Optimizer** | GPT-4 | Product recommendations, links | OPENAI_API_KEY | ✅ Operational |
| **Micro SaaS Builder** | GPT-4 | Build small products fast | OPENAI_API_KEY | ✅ Operational |
| **Social Media Amplifier** | GPT-4 | Multi-platform content distribution | OPENAI_API_KEY | ✅ Operational |
| **Ad Performance Optimizer** | GPT-4 | Analyze and optimize ad campaigns | OPENAI_API_KEY | ✅ Operational |

#### **Desktop AI Agents** (`~/Desktop/AI_Agents/`)

| Agent Name | Provider | Primary Function | Tech Stack | Status |
|-----------|----------|------------------|------------|---------|
| **Jenny** | Claude/GPT | Creative director, content generation | Python, GUI | ✅ Operational |
| **Luna** | Gemini | Visual concepts, brand strategy | Python, GUI | ✅ Operational |
| **Ava** | Claude | Customer success, support | Python, SQLite | ✅ Operational |
| **Trent** | GPT-4 | Financial modeling, analysis | Python, Pandas | ✅ Operational |
| **Lexi** | Claude | Business plans, documentation | Python, Markdown | ✅ Operational |
| **Demo** | Mixed | Research, web scraping | Python, Selenium | ✅ Operational |
| **Razor** | Claude | Security, code auditing | Python | 🔧 In Dev |
| **Cannon** | GPT | Rapid prototyping | Python | 🔧 In Dev |
| **The Key Butler** | Custom | API key management | Python | 🔧 In Dev |

### **IN DEVELOPMENT** (Not Yet Deployed)

| Agent Name | Provider | Purpose | Blocker |
|-----------|----------|---------|---------|
| **Nexus Intelligence Router** | Claude | Route tasks to best agent | Integration needed |
| **Quantum Readiness Analyzer** | GPT | Future tech assessment | Scope definition |
| **Agent Deployer** | System | Auto-deploy new agents | Testing phase |
| **Guardian Data Access** | Custom | Healthcare data platform | Compliance review |

## 2.2 Agent Communication Architecture

### Current Communication Methods

**Method 1: Shared Database (Primary)**
- All agents read/write to Supabase
- Real-time updates via subscriptions
- Task queue system for coordination

**Method 2: File-Based (Secondary)**
- Agents write to shared folders
- JSON files for data exchange
- Used for logs and batch processing

**Method 3: API Calls (For External)**
- RESTful APIs between services
- WebSocket for real-time events
- MCP protocol for Cursor/Windsurf integration

### Agent Coordination Workflow

**Example: LocalBook App Development**
```
1. User Request → Claude Code (you)
2. Claude Code → Creates Archon tasks
3. Oracle Agent → Reviews tasks, assigns to Product Engineer
4. Product Engineer → Writes code, logs progress
5. Bob Agent → Sets up infrastructure, deployment
6. Jenny Agent → Creates landing page copy
7. Trent Agent → Builds financial projections
8. Communication Director → Sends SMS update to Joe
```

**Coordination File**: `~/archon/autonomous-agents/src/utils/coordinator.py`

## 2.3 Tech Stack by Department

### Production Department
- **Languages**: Python 3.13, TypeScript, JavaScript
- **Frontend**: React 18, Vite, TailwindCSS, shadcn/ui
- **Backend**: FastAPI, Express.js, Node.js
- **Databases**: Supabase (PostgreSQL), Pinecone (vectors)
- **Package Managers**: `uv` (Python), npm (Node)
- **Testing**: pytest, Vitest
- **Deployment**: Vercel, Railway, Docker

### Creative Department
- **AI APIs**: OpenAI, Anthropic, Google Gemini
- **Content Tools**: Markdown, Notion API
- **Design**: Figma API (planned), Canva automation
- **Image Gen**: DALL-E, Midjourney API (planned)

### Research Department
- **Scraping**: Crawl4AI, Playwright, Selenium, BeautifulSoup
- **Data Processing**: Pandas, NumPy, SciPy
- **APIs**: Serp API, Perplexity API, sports odds API
- **Storage**: CSV, JSON, PostgreSQL

---

# 3. TECHNICAL ENVIRONMENT

## 3.1 Operating System & Hardware

**Computer**: MacBook Pro (Apple Silicon M2)
**OS**: macOS 15.6.1 (Sequoia)
**Kernel**: Darwin 24.6.0
**Architecture**: ARM64

**Specs**:
- **Processor**: Apple M2 chip
- **Memory**: 16GB+ unified memory
- **Storage**: 512GB+ SSD
- **Network**: WiFi 6, Ethernet available

## 3.2 Development Tools Installed

| Tool | Version | Location | Purpose |
|------|---------|----------|---------|
| **Python** | 3.13.1 | `/usr/local/bin/python3` | Primary backend language |
| **Node.js** | 22.12.0 | `/usr/local/bin/node` | Frontend & server tools |
| **npm** | 10.9.0 | `/usr/local/bin/npm` | Node package manager |
| **uv** | Latest | `~/.local/bin/uv` | Fast Python package manager |
| **Git** | 2.x | `/usr/bin/git` | Version control |
| **nmap** | 7.98 | `/usr/local/bin/nmap` | Network scanning |
| **curl** | Latest | `/usr/bin/curl` | HTTP requests |
| **PostgreSQL** | via Supabase | Cloud | Database |
| **Docker** | Not installed | - | Planned installation |

**IDEs & Editors**:
- Cursor (primary AI coding tool)
- VS Code (secondary)
- Claude Code CLI (command-line AI)
- Windsurf (AI coding, MCP enabled)

## 3.3 Current File Structure

```
/Users/joebudds/
├── api_keys/
│   └── keys.env                          # Master API key vault (28 keys)
│
├── archon/                                # Main AI knowledge platform
│   ├── python/                           # Backend services
│   │   ├── src/
│   │   │   ├── server/                  # FastAPI server (port 8181)
│   │   │   ├── mcp_server/              # MCP server (port 8051)
│   │   │   ├── agents/                  # PydanticAI agents (port 8052)
│   │   │   │   ├── oracle/              # Master orchestrator
│   │   │   │   ├── omni/                # Universal solver
│   │   │   │   ├── product_engineer/    # Full-stack dev
│   │   │   │   ├── browser_navigator/   # Web automation
│   │   │   │   └── [40+ other agents]
│   │   │   ├── registry/                # Agent coordination
│   │   │   └── models/                  # Database schemas
│   │   ├── tests/                       # Backend tests
│   │   ├── pyproject.toml               # Python dependencies (uv)
│   │   └── .env                         # Environment variables
│   │
│   ├── archon-ui-main/                  # Frontend (port 3737)
│   │   ├── src/
│   │   │   ├── components/              # React components
│   │   │   ├── pages/                   # App pages
│   │   │   ├── services/                # API clients
│   │   │   └── contexts/                # React contexts
│   │   ├── package.json                 # Frontend dependencies
│   │   └── vite.config.ts               # Vite config
│   │
│   ├── autonomous-agents/               # Standalone agent system
│   │   ├── src/agents/                  # Agent implementations
│   │   │   ├── communication_director.py
│   │   │   ├── product_engineer.py
│   │   │   ├── sales_director.py
│   │   │   ├── bob_the_builder.py
│   │   │   └── home_assistant_specialist.py
│   │   ├── apps/
│   │   │   └── booking-app/             # LocalBook app (IN PROGRESS)
│   │   ├── .env                         # Agent API keys
│   │   └── check_status.sh              # System status dashboard
│   │
│   ├── docker-compose.yml               # Service orchestration
│   ├── CLAUDE.md                        # Archon development guide
│   └── CLAUDE-ARCHON.md                 # Archon workflow guide
│
├── Desktop/
│   └── AI_Agents/                       # Desktop GUI agents
│       ├── Jenny/                       # Creative director
│       ├── Luna/                        # Visual concepts
│       ├── Ava/                         # Customer success
│       ├── Trent/                       # Financial analyst
│       ├── Lexi/                        # Business writer
│       ├── Demo/                        # Research & scraping
│       ├── Bob/                         # Automation specialist
│       ├── Razor/                       # Security auditor
│       ├── Cannon/                      # Rapid prototyping
│       └── The Key Butler/              # API key manager
│
├── HomeHub/                             # Home Assistant integration
│   ├── homehub_builder.py               # Device auto-assignment
│   ├── ha_inspector.py                  # System inspection
│   ├── ha_complete_setup.py             # Dashboard builder
│   ├── ha_advanced_setup.py             # Add-on installer
│   ├── .env                             # HA credentials
│   ├── requirements.txt                 # Python dependencies
│   └── HA_SETUP_REPORT.md               # Complete HA documentation
│
├── AI-Relay/                            # Multi-agent orchestration
│   ├── orchestrator.py                  # Agent coordinator
│   └── requirements.txt                 # Dependencies
│
├── Dev/                                 # Development projects
│   ├── Spark/                           # Delivery tracking app
│   └── Dictation/                       # Voice-to-text tools
│
├── Delivery_Tracking/                   # Spark project work
├── Agents/                              # Agent experiments
└── CLAUDE.md                            # Root development guide
```

## 3.4 API Keys Vault

**Location**: `/Users/joebudds/api_keys/keys.env`
**Format**: Environment variable file
**Security**: Local only, not in Git
**Total Keys**: 28

**Categories**:
- **AI/LLM**: OpenAI, Anthropic, Gemini, Perplexity, DeepSeek
- **Voice/Audio**: ElevenLabs, Porcupine
- **Search/Data**: Serp API, Sports Odds API
- **Payment**: Stripe, PayPal
- **Home Automation**: Home Assistant, Homey Pro
- **Communication**: Twilio (SMS), Netlify
- **Cloud Infrastructure**: Supabase, Pinecone, Heroku

**Access**:
- All agents load from this vault
- Agents use `python-dotenv` to read
- Keys are injected via environment variables

## 3.5 Database Setup

### Supabase (Primary Database)
- **URL**: `https://thhccnbwztcwovqpyamd.supabase.co`
- **Type**: PostgreSQL with pgvector extension
- **Tables**:
  - `sources` - Crawled websites, uploaded documents
  - `documents` - Chunked content with embeddings
  - `projects` - Project management
  - `tasks` - Task tracking and assignment
  - `code_examples` - Indexed code snippets

- **Features**:
  - Real-time subscriptions (WebSocket)
  - Row-level security
  - Automatic backups
  - REST API auto-generated

**Schema Location**: Managed via Supabase dashboard

### Pinecone (Vector Database)
- **API Key**: `pcsk_6r3bz1_...`
- **Purpose**: Semantic search for knowledge base
- **Index**: `archon-knowledge`
- **Dimensions**: 1536 (OpenAI embeddings)
- **Use Cases**:
  - Find similar code examples
  - Semantic documentation search
  - Pattern matching across projects

### SQLite (Local Databases)
- **Location**: Various agent folders
- **Examples**:
  - `~/Desktop/AI_Agents/Ava/ava_customer_support.db`
  - Used for agent-specific data
  - Not shared between agents

## 3.6 Network Configuration

**Local Network**: 192.168.68.0/24
**Gateway**: 192.168.68.1
**Mac IP Addresses**: 192.168.68.115, 192.168.68.75

**Raspberry Pi (Home Assistant)**:
- **IP**: 192.168.68.129
- **Port**: 8123
- **Purpose**: Home automation server
- **Version**: Home Assistant 2025.10.1

**Other Network Devices**: 40+ smart home devices (see Section 4)

**Remote Access**:
- **Tailscale VPN**: Installed
- **Tailscale IP**: 100.126.192.34
- **SSH**: Available via Tailscale
- **Purpose**: Access Mac from anywhere (iPhone, tablet)

---

# 4. HOME ASSISTANT PROJECT

## 4.1 Current Setup Status

**System**: Home Assistant OS on Raspberry Pi
**IP Address**: 192.168.68.129:8123
**Version**: 2025.10.1
**Status**: ✅ Fully Operational

### Completed Setup (75% Done)
- ✅ Raspberry Pi configured and running
- ✅ API authentication with long-lived token
- ✅ 4 essential add-ons installed (MQTT, File Editor, VS Code, Samba)
- ✅ MQTT broker configured for IoT devices
- ✅ Network discovery enabled (Zeroconf, DHCP, Bluetooth)
- ✅ HomeHub dashboard created with area organization
- ✅ 2 automations created (Welcome Home, Good Night)
- ✅ 10 devices registered
- ✅ 48 entities available
- ✅ 3 areas configured (Living Room, Kitchen, Bedroom)

### Pending Setup (25% Remaining)
- ⏳ HomeKit Bridge QR code pairing
- ⏳ Alexa account linking (Cloud integration ready)
- ⏳ Add remaining 90+ smart devices
- ⏳ Configure device-specific integrations
- ⏳ Build room-specific dashboards
- ⏳ Create advanced automations

**Full Documentation**: `~/HomeHub/HA_SETUP_REPORT.md`

## 4.2 Device Inventory (100+ Devices)

### **Smart Lighting** (30+ devices)
- **Philips Hue**: Bridge + 12 bulbs (color, white)
- **TP-Link Kasa**: 8 smart bulbs, 4 light strips
- **Govee**: 6 LED strips (RGB, addressable)
- **Lutron Caseta**: Dimmer switches, bridge

### **Switches & Plugs** (20+ devices)
- **TP-Link Kasa**: 10 smart plugs (energy monitoring)
- **Wemo**: 6 smart plugs
- **Zigbee Switches**: 4 wall switches

### **Climate Control** (5 devices)
- **Nest**: 2 thermostats
- **Smart Fans**: 3 ceiling fans with remote control

### **Security & Cameras** (15+ devices)
- **Ring**: Doorbell camera, 2 spotlight cameras
- **Wyze**: 8 indoor cameras, 2 outdoor cameras
- **Smart Locks**: 2 door locks (August, Schlage)
- **Motion Sensors**: 3 indoor sensors

### **Media & Entertainment** (12+ devices)
- **Chromecast**: 4 devices (TVs, displays)
- **Roku**: 3 streaming devices
- **Smart TVs**: 2 (Samsung, LG)
- **Sonos**: 3 speakers

### **Hubs & Controllers** (5 devices)
- **Homey Pro**: Central hub (API integrated)
- **Philips Hue Bridge**: Zigbee controller
- **Lutron Bridge**: Caseta controller
- **SmartThings Hub**: Samsung devices

### **Sensors** (15+ devices)
- **Temperature/Humidity**: 6 sensors
- **Door/Window**: 5 contact sensors
- **Water Leak**: 2 sensors
- **Motion**: 2 sensors

### **Appliances** (8 devices)
- **Smart Vacuum**: Robot vacuum (Roomba/similar)
- **Smart Plugs on Appliances**: Coffee maker, lamps, etc.

### **Other** (10+ devices)
- **Smart Garage Door**: Opener with sensor
- **Smart Blinds**: 2 motorized blinds
- **Smart Sprinklers**: 2 zones
- **Voice Assistants**: Alexa Echo devices (4)

## 4.3 Protocols & Technologies

| Protocol | Device Count | Use Case |
|----------|--------------|----------|
| **WiFi** | 60+ | Most smart devices |
| **Zigbee** | 20+ | Lights, sensors, switches |
| **Z-Wave** | 5+ | Door locks, sensors |
| **Bluetooth** | 10+ | Sensors, trackers |
| **Lutron Clear Connect** | 4 | Caseta dimmers |
| **Proprietary (Homey, etc.)** | 10+ | Various |

## 4.4 Integration Goals

### Auto-Discovery Vision
**Goal**: Plug in ANY smart device → HA automatically detects, configures, and adds to dashboard

**Current vs. Target**:
- **Current**: Manual integration via UI (30+ clicks per device)
- **Target**: Zero-config, automatic room assignment, instant dashboard
- **Challenge**: 50+ different integration methods/APIs

### Voice Control
**Goal**: Control everything via Alexa and Siri/HomeKit

**Status**:
- ✅ Alexa Cloud integration enabled (needs account linking)
- ✅ HomeKit Bridge ready (needs QR code pairing)
- ⏳ Custom voice commands and routines

### Automation Wishlist
1. **Morning Routine**: Gradual lights, coffee maker, thermostat up
2. **Evening Routine**: Sunset lights, lock doors, security cameras active
3. **Away Mode**: Randomize lights, monitor cameras, alert on motion
4. **Movie Mode**: Dim lights, close blinds, start streaming
5. **Sleep Mode**: All lights off, doors locked, optimal temperature
6. **Energy Saver**: Turn off idle devices, optimize HVAC
7. **Security Alerts**: SMS on door/window open when away
8. **Weather Response**: Adjust thermostat, close blinds on hot days

## 4.5 Hub Product Vision

### Product Name: **HomeHub**
**Tagline**: "Smart Home Setup in 5 Minutes, Not 5 Hours"

### Unique Selling Points
1. **Auto-Discovery**: Finds all devices on network automatically
2. **Zero-Config**: No manual integration, no YAML editing
3. **Voice Control**: Works with Alexa, Google, Siri out of box
4. **Beautiful Dashboard**: Auto-organized by room
5. **Pre-Built Automations**: 20+ common automations included
6. **One-Click Install**: Raspberry Pi image, flash and go

### Target Market
- **DIY Smart Home Enthusiasts**: Tired of complex setup
- **Property Managers**: Manage multiple properties remotely
- **Tech-Savvy Homeowners**: Want automation without hassle
- **Seniors**: Simple voice control for accessibility

### Competitive Advantage
| Feature | HomeHub | Home Assistant Raw | SmartThings | Google Home |
|---------|---------|-------------------|-------------|-------------|
| **Auto-Discovery** | ✅ All protocols | ❌ Manual | ⚠️ Limited | ⚠️ WiFi only |
| **Voice Control** | ✅ All assistants | ⚠️ Complex | ✅ Google only | ✅ Google only |
| **Dashboard** | ✅ Auto-generated | ❌ Manual YAML | ⚠️ Basic | ⚠️ Basic |
| **Price** | $199 one-time | Free (DIY) | Free (limited) | Free (limited) |
| **Privacy** | ✅ Local | ✅ Local | ❌ Cloud | ❌ Cloud |

### Revenue Model
- **Hardware**: $199 (Raspberry Pi + custom image)
- **Cloud Features**: $9.99/month (optional, remote access, backups)
- **Licensing**: $29 (software-only, BYOD Raspberry Pi)
- **Support**: $49/year (priority support, custom automations)

**Target Revenue**: 50 units/month = $10K/month (hardware + software)

---

# 5. PRIORITY CAPABILITIES NEEDED

## 5.1 Form Filling Automation

### Use Cases

#### **Account Creation** (High Priority)
**Target Sites**:
- **Stripe Account**: Business banking setup
- **PayPal Business**: Payment processing
- **Google Business Profile**: Local SEO
- **Facebook Business Manager**: Ad accounts
- **LinkedIn Company Page**: B2B presence
- **GitHub Organization**: Code hosting
- **AWS/Azure/GCP**: Cloud infrastructure
- **Domain Registrars**: Namecheap, GoDaddy
- **Email Marketing**: Mailchimp, ConvertKit
- **Analytics**: Google Analytics, Mixpanel

**Current Pain Point**: 30-60 minutes per account, 50+ fields, verification steps

**Desired Solution**:
- Agent reads form fields
- Auto-fills from business profile database
- Handles CAPTCHA (2Captcha API integration)
- Completes email verification
- Saves credentials to vault
- Reports completion status

**Implementation**:
- Use `Browser Navigator Agent` (`~/archon/python/src/agents/browser_navigator/`)
- Playwright for browser automation
- Stealth mode to avoid detection
- Screenshot on errors for debugging

#### **Payment & Financial Forms**
**Target Sites**:
- **Plaid Connection**: Bank account linking
- **Stripe Onboarding**: Identity verification, tax forms
- **IRS W-9**: Tax information
- **State Business Registration**: LLC, sales tax
- **Merchant Accounts**: Square, Clover

**Special Considerations**:
- Financial data security (encrypted storage)
- Manual review before submission
- Compliance with regulations

#### **Client Onboarding Forms**
**Target Sites**:
- **Freelance Platforms**: Upwork, Fiverr, Toptal
- **Client Questionnaires**: Custom forms on websites
- **Project Briefs**: Scope, timeline, budget
- **NDA/Contract Signing**: DocuSign, HelloSign

## 5.2 API Key Retrieval & Storage Workflow

### Current Manual Process (30-60 min per service)
1. Navigate to service website (e.g., stripe.com)
2. Log in or create account
3. Navigate to "Developers" or "API" section
4. Click "Create API Key" or "Get API Key"
5. Copy key
6. Paste into `~/api_keys/keys.env`
7. Update agent `.env` files
8. Test API connection
9. Document key usage

**Services Needing Keys** (Priority Order):
1. **Stripe** (payments) - DONE ✅
2. **Plaid** (banking) - TODO
3. **Twilio** (SMS) - DONE ✅
4. **SendGrid** (email) - TODO
5. **Cloudflare** (CDN) - TODO
6. **Google Maps** (location) - TODO
7. **Firebase** (backend) - TODO
8. **Auth0** (authentication) - TODO
9. **Algolia** (search) - TODO
10. **Sentry** (error tracking) - TODO

### Desired Automated Flow
```
Agent → Navigate to service API page
      → Create developer account (if needed)
      → Generate API key
      → Copy key to clipboard
      → Append to ~/api_keys/keys.env with proper formatting
      → Update all agent .env files that need this key
      → Test API connection with simple call
      → Log success/failure
      → Report to user via SMS
```

**Challenges**:
- Each service has different UI/flow
- Some require phone verification
- Some require identity verification (tax forms)
- Rate limiting on account creation

**Solution**:
- `Account Setup Agent` with Playwright
- Service-specific scripts (`~/archon/python/src/agents/accountsetupagent/`)
- Manual verification step when needed
- Store credentials securely (encrypted)

## 5.3 Voice Command Interface

### Requirements

**Input Methods**:
- **Wake Word**: "Hey Jarvis" or "Hey SavvyTech"
- **Push-to-Talk**: Button or keyboard shortcut
- **Continuous Listening**: Background monitoring (privacy mode)

**Commands Needed**:

#### **Agent Management**
- "Deploy Product Engineer agent"
- "What are all agents working on?"
- "Pause Demo agent"
- "Show me Jenny's last output"

#### **Project Management**
- "Create new project: [name]"
- "What's the status of LocalBook?"
- "Show me all pending tasks"
- "Mark task [ID] as complete"

#### **Information Retrieval**
- "Search knowledge base for [topic]"
- "Find code example for [functionality]"
- "What's our current revenue?"
- "How many API keys do we have?"

#### **Home Automation** (via Home Assistant)
- "Turn on living room lights"
- "Set bedroom temperature to 68"
- "Show me front door camera"
- "Lock all doors"

#### **System Control**
- "Open Archon dashboard"
- "Run HomeHub sync"
- "Check Raspberry Pi status"
- "Show me system logs"

### Implementation Plan

**Tech Stack**:
- **Speech-to-Text**: OpenAI Whisper (local or API)
- **Wake Word Detection**: Porcupine (API key: `2weFSr...`)
- **Natural Language Understanding**: GPT-4 or Claude
- **Text-to-Speech**: ElevenLabs (API key: `sk_5086...`)

**Architecture**:
```
Microphone → Wake Word Detection → STT (Whisper)
                                      ↓
                              NLU (GPT-4) → Intent & Entities
                                      ↓
                              Command Router
                                      ↓
                    ┌─────────────────┼─────────────────┐
                    ↓                 ↓                 ↓
              Agent Control    Home Assistant    System Control
                    ↓                 ↓                 ↓
              TTS Response ← Combine Results ← TTS Response
```

**Priority**: MEDIUM (after first revenue)

## 5.4 Computer Control (Clicking, Typing, Navigation)

### Use Cases

#### **Automated Testing**
- Click through web app flows
- Fill forms and submit
- Verify success/error messages
- Screenshot bugs automatically

#### **Browser Automation**
- Open websites in specific browser
- Navigate multi-step workflows
- Download files from sites
- Extract data from web pages

#### **Desktop Automation**
- Open applications
- Navigate menus (File → Save, etc.)
- Type keyboard shortcuts
- Move/resize windows

#### **Cross-Application Workflows**
- Copy from Figma → Paste into code editor
- Export from Excel → Upload to website
- Screenshot from browser → Send via Slack

### Implementation

**Tools**:
- **PyAutoGUI**: Mouse/keyboard control (Python)
- **Playwright**: Browser automation (JavaScript/Python)
- **AppleScript**: Mac-specific automation
- **Accessibility API**: UI element detection

**Safety Measures**:
- Require explicit permission for each action
- Screen recording during automation (for debugging)
- Emergency stop hotkey (Cmd+Shift+Esc)
- Sandbox mode for testing

**Example Script** (PyAutoGUI):
```python
import pyautogui
import time

# Safety: Enable fail-safe (move mouse to corner to abort)
pyautogui.FAILSAFE = True

# Open Spotlight
pyautogui.hotkey('command', 'space')
time.sleep(0.5)

# Type application name
pyautogui.write('Terminal')
pyautogui.press('enter')
time.sleep(1)

# Type command
pyautogui.write('cd ~/archon && uv run pytest')
pyautogui.press('enter')
```

**Location**: `~/archon/autonomous-agents/src/utils/computer_control.py`

## 5.5 Network Device Configuration Automation

### Use Cases

#### **Smart Home Devices**
- Auto-connect devices to WiFi (QR code or WPS)
- Configure device settings (name, room, behavior)
- Update firmware automatically
- Backup device configurations

#### **Network Equipment**
- Configure routers (port forwarding, DHCP reservations)
- Set up VLANs for IoT devices (security)
- Monitor network health (speed tests, uptime)
- Alert on offline devices

### Challenges
- 50+ different device APIs
- Some devices have no API (only mobile app)
- Some require physical button presses
- Security concerns (network access)

### Solution Approach

**Phase 1: API-Based Devices**
- Philips Hue, TP-Link Kasa, Nest, etc.
- Use official APIs where available
- Store device credentials securely

**Phase 2: App Reverse-Engineering**
- Intercept mobile app traffic (mitmproxy)
- Identify API endpoints
- Replicate authentication flow
- Build custom API wrappers

**Phase 3: Physical Automation**
- QR code generation for WiFi credentials
- Robotic button presser (for devices requiring physical interaction)
- OCR for screen reading

**Location**: `~/archon/python/src/agents/home_assistant_specialist/`

---

# 6. CURRENT WORKFLOWS

## 6.1 API Key Retrieval Process

### Current Manual Workflow (Example: Stripe)

**Steps** (20-30 minutes):
1. Open browser → Navigate to stripe.com
2. Click "Sign In" → Enter credentials
3. If no account: "Create Account" → Fill 20+ fields
4. Navigate to "Developers" → Click "API Keys"
5. Click "Create API Key" → Name it → Select permissions
6. Copy "Secret Key" (starts with `sk_`)
7. Open `~/api_keys/keys.env` in editor
8. Add line: `STRIPE_SECRET_KEY=sk_...`
9. Save file
10. Open `~/archon/python/.env`
11. Add line: `STRIPE_SECRET_KEY=sk_...`
12. Save file
13. Open `~/archon/autonomous-agents/.env`
14. Add line: `STRIPE_SECRET_KEY=sk_...`
15. Save file
16. Test API: `curl -u sk_...: https://api.stripe.com/v1/customers`
17. If success, done. If error, debug.

**Pain Points**:
- Repetitive across 50+ services
- Easy to make typos
- Forget to update all .env files
- No validation until later
- Manual tracking of which agents need which keys

### Desired Automated Workflow

**Command**: `hey jarvis, get me a stripe api key`

**Agent Actions** (5 minutes, unattended):
1. Browser Navigator Agent opens stripe.com
2. Checks if logged in (cookie stored)
3. If not: Retrieves credentials from vault, logs in
4. Navigates to Developers → API Keys
5. Clicks "Create New Key"
6. Names it: `SavvyTech_Production_${DATE}`
7. Copies key to clipboard
8. Appends to `~/api_keys/keys.env`:
   ```bash
   # === Payment APIs ===
   STRIPE_SECRET_KEY=sk_live_51...
   ```
9. Updates all agent `.env` files automatically:
   - `~/archon/python/.env`
   - `~/archon/autonomous-agents/.env`
   - `~/HomeHub/.env` (if needed)
10. Tests API connection:
    ```bash
    curl -u ${STRIPE_SECRET_KEY}: https://api.stripe.com/v1/customers?limit=1
    ```
11. Logs result to database
12. Sends SMS: "✅ Stripe API key configured and tested"

**Implementation**:
- Agent: `Account Setup Agent` + `Browser Navigator Agent`
- Location: `~/archon/python/src/agents/accountsetupagent/`
- Tech: Playwright (browser automation)
- Status: 50% implemented, needs testing

## 6.2 Agent Deployment Workflow

### Current Process

**Scenario**: Need to create a new agent for [specific task]

**Manual Steps** (2-4 hours):
1. Open `~/archon/python/src/agents/` folder
2. Create new folder: `mkdir mynewagent`
3. Create `agent.py` file
4. Copy boilerplate from similar agent
5. Modify: name, capabilities, prompts
6. Add to `~/archon/python/src/registry/agents.py`
7. Update `pyproject.toml` if new dependencies
8. Run `uv sync` to install dependencies
9. Create test file: `tests/test_mynewagent.py`
10. Write basic tests
11. Run tests: `uv run pytest`
12. Update documentation
13. Deploy to agents service (restart container)
14. Test via Archon UI
15. Monitor logs for errors

**Pain Points**:
- Lots of boilerplate code
- Easy to forget steps (e.g., update registry)
- Testing is manual
- No template system

### Desired Automated Workflow

**Command**: `create agent: [name], purpose: [description]`

**System Actions**:
1. Agent Deployer Agent reads request
2. Generates agent code using template:
   ```python
   # Auto-generated by Agent Deployer
   # Date: 2025-10-06
   # Purpose: [description]

   from pydantic_ai import Agent, RunContext
   ...
   ```
3. Adds to registry automatically
4. Creates test file with basic tests
5. Runs tests, reports results
6. If pass: Deploys to agents service
7. If fail: Reports errors, suggests fixes
8. Updates documentation automatically

**Implementation Status**: 70% complete
- Location: `~/archon/python/agent_deployer.py`
- Needs: Better template system, automated testing

## 6.3 Claude Code vs. Other AI Usage

### When to Use Claude Code (This Session)
**Use Cases**:
- **Code writing and editing**: Full file manipulation, refactoring
- **System administration**: File system operations, network config
- **Debugging**: Run tests, check logs, investigate errors
- **Documentation**: Create comprehensive docs with code examples
- **Automation**: Write scripts, set up workflows
- **Integration**: Connect multiple systems, configure APIs

**Strengths**:
- Full file system access
- Can run commands (bash, python, etc.)
- Multi-file editing and refactoring
- Persistent context across session
- Tool use (Read, Write, Edit, Bash, Glob, Grep)

### When to Use Archon Agents
**Use Cases**:
- **Ongoing tasks**: Multi-hour/multi-day projects
- **Specialized work**: SEO content, financial modeling, web scraping
- **Autonomous operation**: Run without supervision
- **Parallel work**: Multiple agents working simultaneously
- **Knowledge base queries**: RAG search, code examples

**Strengths**:
- Always available (no context limits)
- Specialized skills per agent
- Shared knowledge base
- Task queue system
- Real-time notifications (SMS, email)

### When to Use Other AI (ChatGPT, Gemini)
**Use Cases**:
- **Quick questions**: No file access needed
- **Brainstorming**: Ideas, strategies, approaches
- **Learning**: Explain concepts, tutorials
- **Mobile use**: When away from computer

**Strengths**:
- Fast response times
- Conversational interface
- Mobile apps available
- Free tiers available

### Workflow Example: Building LocalBook App

**Week 1** (Current):
- **Claude Code**: Set up project structure, configure Supabase, write initial code
- **Product Engineer Agent**: Build React components, API routes
- **Bob Agent**: Set up Vercel deployment, configure environment
- **Jenny Agent**: Write landing page copy, value propositions
- **Trent Agent**: Create pricing calculator, financial projections

**Week 2** (After Launch):
- **Claude Code**: Debug issues, add features based on feedback
- **Sales Director Agent**: Research target customers, create outreach list
- **Communication Director**: Send SMS when new user signs up
- **Archon MCP**: Log all development decisions for future reference

---

# 7. IMMEDIATE PRIORITIES

## 7.1 THIS WEEK (Must Complete)

### Priority 1: **LocalBook App MVP** (CRITICAL PATH TO REVENUE)

**Deadline**: Friday, October 11, 2025
**Goal**: Fully functional booking app ready for first customer

#### Tasks Breakdown

**Day 1 (Monday) - Frontend Core**
- [ ] Complete React component library
  - Booking form with date/time picker
  - Service selection with images
  - Customer info capture
  - Confirmation screen
- [ ] Implement Supabase auth (email/password)
- [ ] Connect frontend to Supabase API
- [ ] Mobile-responsive design (TailwindCSS)

**Day 2 (Tuesday) - Backend & Business Logic**
- [ ] Supabase database schema:
  - `businesses` table (salon/mechanic info)
  - `services` table (haircut, oil change, etc.)
  - `bookings` table (appointments)
  - `customers` table (user data)
- [ ] Row-level security policies
- [ ] Email confirmation triggers (Supabase functions)
- [ ] Calendar availability logic

**Day 3 (Wednesday) - Payment Integration**
- [ ] Stripe Connect integration
  - Business onboarding flow
  - Payment collection
  - Automatic payouts (minus 3% fee)
- [ ] Test transactions (sandbox mode)
- [ ] Receipt generation

**Day 4 (Thursday) - Polish & Testing**
- [ ] UI/UX improvements
- [ ] Error handling (network failures, validation)
- [ ] Loading states and animations
- [ ] Cross-browser testing (Chrome, Safari, Firefox)
- [ ] Mobile testing (iOS, Android)

**Day 5 (Friday) - Deploy & Marketing**
- [ ] Deploy to Vercel (production)
- [ ] Custom domain setup (localbook.app or similar)
- [ ] SSL certificate (automatic via Vercel)
- [ ] Landing page with demo video
- [ ] Create first pitch deck for local businesses

**Agents Assigned**:
- **Product Engineer**: Lead development
- **Bob**: Deployment and infrastructure
- **Jenny**: Landing page copy, email templates
- **Trent**: Pricing strategy, financial projections
- **Claude Code (you)**: Coordination, code review, debugging

**Success Metric**: One paying business customer by end of week ($79/month = $948/year)

### Priority 2: **Revenue Generation Tasks**

#### Task 2A: **Outreach to First 20 Customers**
**Target**: Local service businesses in Dallas/Fort Worth

**List**:
- 5 hair salons
- 5 auto mechanics
- 5 HVAC companies
- 5 cleaning services

**Outreach Method**:
- Phone call (warm intro)
- Email with demo video
- Offer: First month free ($79 value)

**Agent**: Sales Director + Jenny (email copy)

#### Task 2B: **Create Demo Video** (2-3 minutes)
- Show business owner dashboard
- Demonstrate booking flow (customer perspective)
- Highlight key features: calendar, payments, confirmations
- End with pricing and CTA

**Tools**: Loom or ScreenFlow
**Agent**: Jenny (script)

### Priority 3: **Home Assistant Hub Productization**

**Goal**: Create sellable "HomeHub" product by end of week

**Tasks**:
- [ ] Create Raspberry Pi disk image with pre-configured HA
- [ ] Build web-based setup wizard
- [ ] Design packaging and branding
- [ ] Create installation guide (5 minutes or less)
- [ ] Set up Stripe product page
- [ ] Launch on Product Hunt

**Agents**: Bob (technical), Jenny (marketing), Lexi (documentation)

**Revenue Target**: 5 sales @ $199 = $995

### Priority 4: **Guardian Business Plan Completion**

**Goal**: Investor-ready pitch deck for Guardian platform

**Tasks**:
- [ ] Complete market analysis (Trent)
- [ ] Finalize product specifications (Lexi)
- [ ] Create financial projections (Trent)
- [ ] Design product sketches (Luna)
- [ ] Write patent strategy document (Lexi)
- [ ] Assemble pitch deck (Jenny + Lexi)

**Timeline**: 2 weeks (not blocking revenue)

## 7.2 First Product/Service to Market

**WINNER**: LocalBook (Local Service Booking App)

**Reasoning**:
1. **Fastest to build**: 5 days vs. weeks/months
2. **Zero infrastructure cost**: Supabase free tier, Vercel free tier
3. **Proven demand**: Every local business needs booking
4. **Recurring revenue**: $79/month subscription
5. **Low barrier to entry**: No hardware, no inventory
6. **Scale potential**: 100,000+ local businesses in DFW

**Alternative**: Home Assistant Hub (longer timeline, one-time revenue)

## 7.3 Quick Wins (Revenue This Week)

### Win 1: **Freelance Automation Project**
**Opportunity**: Post on Upwork/Fiverr offering form automation services

**Service**: "I'll automate any repetitive web task (form filling, data entry, scraping)"

**Pricing**: $500-1,000 per project

**Delivery Time**: 3-5 days

**Effort**: 5-10 hours (Browser Navigator Agent does heavy lifting)

**Expected Revenue**: $500-1,000 (one project)

**Agent**: Browser Navigator + Product Engineer

### Win 2: **AI Agent Consulting Call**
**Opportunity**: Offer free 30-minute "AI Audit" to local businesses

**Pitch**: "I'll show you 3 ways AI can save you 10+ hours per week"

**Conversion**: Sell $2,000 automation package

**Expected Revenue**: $2,000 (one client)

**Agent**: Sales Director (research), Jenny (follow-up email)

### Win 3: **Content Creation Service**
**Opportunity**: SEO blog posts for SaaS companies

**Pricing**: $300 per 2,000-word article

**Delivery**: Same day (Jenny + SEO Content Factory agents)

**Market**: Reach out to 50 SaaS companies on LinkedIn

**Expected Revenue**: $300-900 (1-3 articles)

**Agent**: Jenny (writing), Sales Director (outreach)

### Win 4: **HomeHub Beta Sales**
**Opportunity**: Sell 3 beta units at discount ($99 instead of $199)

**Target**: Post in Home Assistant subreddit, Discord servers

**Pitch**: "Beta testers wanted - setup in 5 minutes, auto-discovers all devices"

**Expected Revenue**: $297 (3 units)

**Agent**: Bob (technical support), Jenny (marketing post)

### Win 5: **Guardian Pre-Orders**
**Opportunity**: Gauge interest with landing page, collect $50 deposits

**Target**: Elder care facilities, daycare centers

**Goal**: 10 deposits = $500

**Agent**: Lexi (landing page copy), Trent (pricing), Luna (mockups)

---

# 8. FILE STRUCTURE & LOCATIONS

## 8.1 Critical File Paths

### API Keys & Credentials
```
~/api_keys/keys.env                    # Master vault (28 API keys)
~/archon/python/.env                   # Archon backend environment
~/archon/autonomous-agents/.env        # Standalone agents environment
~/HomeHub/.env                         # Home Assistant credentials
```

### Agent Code
```
# Archon Platform Agents
~/archon/python/src/agents/            # All PydanticAI agents
  ├── oracle/agent.py                  # Master orchestrator
  ├── omni/agent.py                    # Universal solver
  ├── browser_navigator/agent.py       # Web automation
  ├── accountsetupagent/agent.py       # Account creation
  └── [30+ other agents]

# Desktop GUI Agents
~/Desktop/AI_Agents/                   # Python GUI agents
  ├── Jenny/                           # Creative director
  ├── Luna/                            # Visual concepts
  ├── Ava/                             # Customer success
  ├── Trent/                           # Financial analyst
  └── [10+ other agents]

# Autonomous Agent System
~/archon/autonomous-agents/src/agents/
  ├── communication_director.py        # SMS, email, coordination
  ├── product_engineer.py              # Full-stack development
  ├── sales_director.py                # Market research, sales
  ├── bob_the_builder.py               # Automation specialist
  └── home_assistant_specialist.py     # HA integrations
```

### Projects
```
# LocalBook App (TOP PRIORITY)
~/archon/autonomous-agents/apps/booking-app/
  ├── src/                             # React frontend
  ├── api/                             # Backend API (if needed)
  └── README.md                        # Project overview

# Home Assistant Integration
~/HomeHub/
  ├── homehub_builder.py               # Device auto-assignment
  ├── ha_inspector.py                  # System inspection
  ├── ha_complete_setup.py             # Dashboard builder
  ├── ha_advanced_setup.py             # Add-on installer
  └── HA_SETUP_REPORT.md               # Complete documentation

# Archon Platform
~/archon/
  ├── python/                          # Backend services
  ├── archon-ui-main/                  # React frontend
  ├── docker-compose.yml               # Service orchestration
  └── CLAUDE.md                        # Development guide
```

### Configuration
```
~/archon/python/pyproject.toml         # Python dependencies (uv)
~/archon/archon-ui-main/package.json   # Frontend dependencies (npm)
~/archon/docker-compose.yml            # Service configuration
```

### Documentation
```
~/CLAUDE.md                            # Root development guide
~/archon/CLAUDE.md                     # Archon-specific guide
~/archon/CLAUDE-ARCHON.md              # Archon workflow guide
~/HomeHub/HA_SETUP_REPORT.md           # Home Assistant documentation
~/SAVVYTECH_COMPLETE_BUSINESS_TECHNICAL_DOCUMENTATION.md  # THIS FILE
```

### Databases
```
# Supabase (cloud)
https://thhccnbwztcwovqpyamd.supabase.co

# Pinecone (cloud)
https://app.pinecone.io/

# SQLite (local)
~/Desktop/AI_Agents/Ava/ava_customer_support.db
```

### Scripts & Utilities
```
~/archon/autonomous-agents/check_status.sh        # System status dashboard
~/HomeHub/run.sh                                  # HA builder execution script
```

## 8.2 Network Locations

```
# Home Assistant (Raspberry Pi)
http://192.168.68.129:8123

# Archon Services (Local Development)
http://localhost:3737    # Frontend UI
http://localhost:8181    # Main FastAPI server
http://localhost:8051    # MCP server
http://localhost:8052    # Agents service

# Remote Access
Tailscale IP: 100.126.192.34
SSH: ssh joebudds@100.126.192.34
```

## 8.3 Cloud Services

```
# Websites
SavvyTech: https://savvytechautomations.com
Netlify: https://app.netlify.com/sites/a29eed52-517c-488f-9b91-84b838c8c4ab

# Development Platforms
GitHub: (need repo URLs)
Vercel: (need project URL)
Supabase: https://supabase.com/dashboard/project/thhccnbwztcwovqpyamd

# APIs
Stripe Dashboard: https://dashboard.stripe.com
Twilio Console: https://console.twilio.com
OpenAI Platform: https://platform.openai.com
Anthropic Console: https://console.anthropic.com
```

---

# APPENDIX A: Quick Start Commands

```bash
# Check system status
cd ~/archon/autonomous-agents && ./check_status.sh

# Start Archon services (all at once)
cd ~/archon && docker-compose up -d

# Start Archon frontend (development)
cd ~/archon/archon-ui-main && npm run dev

# Start Archon backend (development)
cd ~/archon/python && uv run python -m src.server.main

# Run Home Assistant sync
cd ~/HomeHub && source .venv/bin/activate && python homehub_builder.py

# Deploy an agent
cd ~/archon/python && uv run python agent_deployer.py --agent [name]

# Run tests
cd ~/archon/python && uv run pytest
cd ~/archon/archon-ui-main && npm run test

# Check Raspberry Pi
ping 192.168.68.129
curl http://192.168.68.129:8123

# View logs
cd ~/archon && docker-compose logs -f
tail -f ~/HomeHub/homehub.log
```

---

# APPENDIX B: Contact & Communication

**Owner**: Joe Budds
**Phone**: +1 (918) 916-0017
**Business Phone**: +1 (844) 907-4050 (Twilio)
**Email**: [from Twilio or Netlify tokens]

**Notification Preferences**:
- SMS for critical updates (deployments, errors, revenue)
- Email for daily summaries
- Dashboard for detailed progress

**Communication Director Agent** sends SMS notifications automatically for:
- New revenue/customers
- System errors/downtime
- Task completions
- Deployment successes/failures

---

# APPENDIX C: Success Metrics

**Week 1 Goals** (October 6-13):
- [ ] LocalBook MVP deployed
- [ ] 1-5 paying customers ($79-395/month)
- [ ] $500+ one-time revenue (freelance/quick wins)
- [ ] Home Assistant 100% complete
- [ ] Guardian business plan 50% complete

**Month 1 Goals** (October):
- [ ] $2,000/month recurring revenue
- [ ] 20+ customers across all products
- [ ] All 40+ agents operational
- [ ] Market gap database launched
- [ ] 100% automation of key workflows

**Quarter 1 Goals** (Q4 2025):
- [ ] $10,000/month recurring revenue
- [ ] 100+ customers
- [ ] Guardian platform launched (hardware)
- [ ] 10+ employee-level agents
- [ ] Full voice control system operational

---

**END OF DOCUMENTATION**

*Generated: October 6, 2025*
*For: Claude AI Context Transfer*
*Next Update: After first revenue milestone*
