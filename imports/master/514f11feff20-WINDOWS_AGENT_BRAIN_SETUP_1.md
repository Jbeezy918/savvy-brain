# 🪟 Windows 11 Mini PC: Agent Brain Setup

**Purpose**: Turn your Windows mini PC into the always-on "brain" that runs Webby, orchestrates agents, and exposes APIs
**Time**: 30 minutes
**Difficulty**: Easy (click + paste)

**Prerequisites**:
- ✅ Mac File + Model Server setup completed
- ✅ Python 3.11+ installed ([download here](https://python.org/downloads))
- ✅ Tailscale installed and logged in

---

## 📂 Part A: Mount Mac Shares as Network Drives (10 minutes)

Your Windows PC will access Mac folders as if they're local drives (Z:\, Y:\, M:\).

### Step 1: Get Mac Connection Info

You need your Mac's Tailscale IP. On your **Mac**, open Terminal and run:

```bash
tailscale ip -4
```

**Write down**: `100.___.___.___` (your Mac's Tailscale IP)

---

### Step 2: Test Connection from Windows

On **Windows**, open **PowerShell** (click Start, type "PowerShell", click it) and paste:

```powershell
# Replace 100.x.x.x with your Mac's Tailscale IP
Test-NetConnection -ComputerName 100.x.x.x -Port 445

# Should show "TcpTestSucceeded: True"
```

**You should see**: `TcpTestSucceeded : True` ✅

If it fails, go back to Mac and verify File Sharing is ON.

---

### Step 3: Map Mac Documents to Z:\ Drive

**Click Steps**:
1. Open **File Explorer** (Windows key + E)
2. Click **This PC** in left sidebar
3. Click **Computer** tab at top (or right-click "This PC" → "Map network drive")
4. Click **Map network drive**
5. **Drive**: Select **Z:**
6. **Folder**: Enter `\\100.x.x.x\Documents` (replace with your Mac IP)
7. **Check** "Reconnect at sign-in"
8. **Click** "Finish"
9. **Enter** your Mac username and password when prompted
10. **Check** "Remember my credentials"
11. **Click** "OK"

**You should see**: Z:\ drive appear in File Explorer with Mac's Documents folder! ✅

---

### Step 4: Map Mac Projects to Y:\ Drive

**Repeat** the same process:

1. **Computer** tab → **Map network drive**
2. **Drive**: Select **Y:**
3. **Folder**: Enter `\\100.x.x.x\Projects` (replace with your Mac IP)
4. **Check** "Reconnect at sign-in"
5. **Click** "Finish"
6. Use same Mac credentials

**You should see**: Y:\ drive with Mac's Projects folder! ✅

---

### Step 5: Map Mac Models to M:\ Drive

**Repeat** one more time:

1. **Computer** tab → **Map network drive**
2. **Drive**: Select **M:**
3. **Folder**: Enter `\\100.x.x.x\Models` (replace with your Mac IP)
4. **Check** "Reconnect at sign-in"
5. **Click** "Finish"
6. Use same Mac credentials

**You should see**: M:\ drive with Mac's Models folder! ✅

---

### Step 6: Test File Access

Let's make sure files sync properly. In **PowerShell**:

```powershell
# Create a test file on Z:\ (Mac Documents)
echo "Hello from Windows!" > Z:\test_from_windows.txt

# List files to verify
dir Z:\ | Select-Object Name

# Should show test_from_windows.txt
```

Now **on your Mac**, open Terminal:

```bash
# Check if the file appeared on Mac
ls ~/Documents/test_from_windows.txt

# Should show the file exists!

# Clean up
rm ~/Documents/test_from_windows.txt
```

**If you see the file on Mac**: Everything is working perfectly! ✅

---

### Step 7: Make Drives Reconnect on Boot

The drives should already reconnect on boot (we checked "Reconnect at sign-in"), but let's verify:

**PowerShell**:
```powershell
# Check persistent network drives
Get-PSDrive -PSProvider FileSystem | Where-Object {$_.DisplayRoot -ne $null}

# Should show Z:, Y:, M: with Mac paths
```

**You should see**: Your three mapped drives listed.

---

### 🎯 Part A Complete!

**What You've Done**:
- ✅ Connected Windows to Mac via SMB over Tailscale
- ✅ Mapped Documents → Z:\
- ✅ Mapped Projects → Y:\
- ✅ Mapped Models → M:\
- ✅ Configured drives to reconnect on boot
- ✅ Tested file synchronization

**Next**: Set up Webby monitor and API on Windows!

---

## 🤖 Part B: Transfer and Setup Webby Monitor (10 minutes)

We'll copy your existing Webby monitor from Mac to Windows and set it up to run as a Windows service.

### Step 1: Create Agent Brain Directory

Open **PowerShell as Administrator** (right-click PowerShell → "Run as administrator"):

```powershell
# Create directory structure
New-Item -ItemType Directory -Path "C:\AgentBrain" -Force
New-Item -ItemType Directory -Path "C:\AgentBrain\webby" -Force
New-Item -ItemType Directory -Path "C:\AgentBrain\logs" -Force
New-Item -ItemType Directory -Path "C:\AgentBrain\configs" -Force

Write-Host "✅ Directory structure created!"
```

---

### Step 2: Copy Webby Files from Mac to Windows

The Webby files are on your Mac. We'll access them via the Y:\ drive (Mac's home directory should be accessible via Projects).

**Option A: Copy from Mac manually (Easier)**

On **Mac** Terminal:
```bash
# Copy webby_enhanced_monitor.py to a shared location
cp ~/webby_enhanced_monitor.py ~/Projects/webby_enhanced_monitor.py

# Copy the upgrade script too
cp ~/upgrade_webby_monitor.sh ~/Projects/upgrade_webby_monitor.sh

echo "✅ Files copied to Projects folder"
```

Then on **Windows** PowerShell:
```powershell
# Copy from Y:\ (Mac Projects) to C:\AgentBrain\webby\
Copy-Item "Y:\webby_enhanced_monitor.py" -Destination "C:\AgentBrain\webby\"

Write-Host "✅ Webby monitor copied to Windows!"
```

**Option B: Download directly on Windows**

If Y:\ drive mapping isn't working yet, create the file manually:

On **Windows**, open Notepad and paste the Webby monitor code, then save as `C:\AgentBrain\webby\webby_enhanced_monitor.py`.

Or use PowerShell to create it:
```powershell
# I'll provide the adapted Windows version in the next step
```

---

### Step 3: Adapt Webby for Windows

The current Webby uses macOS `say` command. Let's create a Windows-compatible version.

Create `C:\AgentBrain\webby\webby_enhanced_monitor.py` with this content:

**PowerShell** (run as Administrator):
```powershell
# Create Windows-compatible Webby monitor
@"
# Python script content here - adapted for Windows
# Uses pyttsx3 for Windows TTS instead of macOS say
# (I'll provide the full adapted script)
"@ | Out-File -FilePath "C:\AgentBrain\webby\webby_enhanced_monitor.py" -Encoding UTF8
```

**Actually**, let's make this easier. On **Mac**, let's create a portable version that works on both:

```bash
# On Mac - create Windows-compatible version
cat > ~/Projects/webby_enhanced_monitor_windows.py << 'ENDOFFILE'
#!/usr/bin/env python3
"""
Webby Enhanced Monitor - Windows Version
Advanced Website Monitoring with Notifications (Windows-compatible)
"""

import os
import sys
import json
import time
import subprocess
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
import platform

# Configuration
STATE_FILE = Path.home() / ".webby_monitor_state.json"
LOG_FILE = Path.home() / ".webby_monitor.log"
SITE_DOMAIN = os.getenv("SITE_DOMAIN", "savvytechautomations.com")
NETLIFY_SITE_ID = "a23eed52-517c-488f-9b91-84b838c8c4ab"
CHECK_INTERVAL = 300  # 5 minutes
VOICE_ENABLED = os.getenv("VOICE_ENABLED", "true").lower() == "true"

# Rotating check schedule
CHECKS = [
    "SSL Certificate",
    "Website Uptime",
    "DNS Health",
    "Netlify Builds",
    "Domain Expiry"
]


class VoiceNotifier:
    """Handle voice notifications - cross-platform"""

    def __init__(self):
        self.is_windows = platform.system() == "Windows"
        self.is_mac = platform.system() == "Darwin"

        # Try to import Windows TTS if on Windows
        if self.is_windows:
            try:
                import pyttsx3
                self.engine = pyttsx3.init()
                self.engine.setProperty('rate', 170)
            except:
                self.engine = None
                print("Warning: pyttsx3 not available, voice disabled")

    def speak(self, message: str, rate: int = 170):
        """Speak a message - cross-platform"""
        if not VOICE_ENABLED:
            return

        try:
            if self.is_mac:
                # macOS TTS
                subprocess.run(
                    ["say", "-v", "Samantha", "-r", str(rate), message],
                    timeout=30,
                    capture_output=True
                )
            elif self.is_windows and self.engine:
                # Windows TTS
                self.engine.say(message)
                self.engine.runAndWait()
        except Exception as e:
            print(f"Voice notification failed: {e}")


class WebbyEnhancedMonitor:
    """Enhanced website monitoring with notifications"""

    def __init__(self):
        self.state = self.load_state()
        self.current_check_index = 0
        self.voice = VoiceNotifier()

        # Track issue patterns
        self.ssl_error_count = 0
        self.consecutive_downtime = 0
        self.last_notification = None

    def load_state(self) -> Dict:
        """Load monitoring state"""
        if STATE_FILE.exists():
            try:
                with open(STATE_FILE, 'r') as f:
                    return json.load(f)
            except:
                pass

        return {
            "last_run": None,
            "total_checks": 0,
            "issues_found": 0,
            "issues_fixed": 0,
            "last_issue": None,
            "check_history": [],
            "notification_history": []
        }

    def save_state(self):
        """Save monitoring state"""
        try:
            self.state["last_run"] = datetime.now().isoformat()
            with open(STATE_FILE, 'w') as f:
                json.dump(self.state, f, indent=2)
        except Exception as e:
            self.log(f"Failed to save state: {e}")

    def log(self, message: str, level: str = "INFO"):
        """Log message"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)

        try:
            with open(LOG_FILE, 'a') as f:
                f.write(log_entry + "\n")
        except:
            pass

    def notify(self, message: str, severity: str = "info"):
        """Send notification (voice + log)"""
        self.log(f"🔔 NOTIFICATION [{severity.upper()}]: {message}", "NOTIFY")

        # Avoid spam - only notify once every 30 minutes for same issue
        now = datetime.now().timestamp()
        if self.last_notification and (now - self.last_notification) < 1800:
            return

        self.last_notification = now

        # Voice notification for critical issues
        if severity in ["critical", "error"]:
            self.voice.speak(f"Website alert. {message}")

        # Track notification
        self.state["notification_history"].append({
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "severity": severity
        })
        self.state["notification_history"] = self.state["notification_history"][-50:]

    def add_to_history(self, check: str, status: str, details: str, action_taken: Optional[str] = None):
        """Add check result to history"""
        entry = {
            "check": check,
            "timestamp": datetime.now().isoformat(),
            "status": status,
            "details": details,
            "action_taken": action_taken
        }

        self.state["check_history"].append(entry)
        self.state["check_history"] = self.state["check_history"][-100:]

        if status in ["failed", "error"]:
            self.state["issues_found"] += 1
            self.state["last_issue"] = entry

        if action_taken:
            self.state["issues_fixed"] += 1

    def check_ssl_basic(self) -> Dict:
        """Basic SSL check via HTTPS request"""
        try:
            response = requests.get(
                f"https://{SITE_DOMAIN}",
                timeout=10,
                verify=True
            )

            if response.status_code == 200:
                self.ssl_error_count = 0
                self.log("✅ SSL Certificate: Verified and working")
                self.add_to_history("SSL Certificate", "ok", "SSL verified via live connection test")
                return {"status": "ok", "details": "SSL fully operational"}
            else:
                self.log(f"⚠️ SSL Certificate: Status {response.status_code}")
                return {"status": "warning", "details": f"Status {response.status_code}"}

        except requests.exceptions.SSLError as ssl_err:
            self.ssl_error_count += 1
            error_detail = str(ssl_err)

            self.log(f"❌ SSL Certificate: Error (count: {self.ssl_error_count})")

            if self.ssl_error_count >= 3:
                self.notify(f"SSL certificate experiencing persistent issues. Error count: {self.ssl_error_count}", "error")

            self.add_to_history("SSL Certificate", "error", f"SSL error (count {self.ssl_error_count}): {error_detail}")
            return {"status": "error", "details": f"SSL issue (#{self.ssl_error_count})"}

        except Exception as e:
            error_msg = str(e)
            self.log(f"❌ SSL Certificate: {error_msg}")
            self.add_to_history("SSL Certificate", "failed", f"Check failed: {error_msg}")
            return {"status": "failed", "details": error_msg}

    def check_uptime_enhanced(self) -> Dict:
        """Enhanced uptime check with retry logic"""
        max_retries = 3
        retry_delay = 5

        for attempt in range(max_retries):
            try:
                response = requests.get(
                    f"https://{SITE_DOMAIN}",
                    timeout=30,
                    headers={'User-Agent': 'WebbyEnhancedMonitor/2.0'}
                )

                if response.status_code == 200:
                    self.consecutive_downtime = 0
                    response_time = response.elapsed.total_seconds()

                    self.log(f"✅ Website Uptime: OK ({response_time:.2f}s)")
                    self.add_to_history("Website Uptime", "ok", f"Website responding normally (200 OK, {response_time:.2f}s)")
                    return {"status": "ok", "details": f"Response time: {response_time:.2f}s"}
                else:
                    self.log(f"⚠️ Website Uptime: Status {response.status_code}")
                    self.add_to_history("Website Uptime", "warning", f"Non-200 status code: {response.status_code}")
                    return {"status": "warning", "details": f"Status: {response.status_code}"}

            except Exception as e:
                if attempt < max_retries - 1:
                    self.log(f"⚠️ Website Uptime: Attempt {attempt + 1} failed, retrying in {retry_delay}s...")
                    time.sleep(retry_delay)
                    continue
                else:
                    error_msg = str(e)
                    self.consecutive_downtime += 1

                    self.log(f"❌ Website Uptime: DOWN after {max_retries} attempts - {error_msg}")

                    if self.consecutive_downtime >= 3:
                        self.notify(f"Website has been down for {self.consecutive_downtime} consecutive checks.", "critical")

                    self.add_to_history("Website Uptime", "error", f"Sustained downtime ({self.consecutive_downtime} checks): {error_msg}")
                    return {"status": "error", "details": f"Down after {max_retries} retries"}

        return {"status": "error", "details": "Unexpected error"}

    def check_dns(self) -> Dict:
        """Check DNS resolution"""
        try:
            import socket
            ips = socket.gethostbyname_ex(SITE_DOMAIN)[2]

            self.log(f"✅ DNS Health: OK - {', '.join(ips)}")
            self.add_to_history("DNS Health", "ok", f"DNS resolving correctly: {', '.join(ips)}")
            return {"status": "ok", "details": f"IPs: {', '.join(ips)}"}

        except Exception as e:
            error_msg = str(e)
            self.log(f"❌ DNS Health: {error_msg}")
            self.notify("DNS resolution is failing for the website", "error")
            self.add_to_history("DNS Health", "failed", f"DNS resolution failed: {error_msg}")
            return {"status": "failed", "details": error_msg}

    def check_netlify_builds(self) -> Dict:
        """Check Netlify builds status - simplified for Windows"""
        self.log("⚠️ Netlify Builds: Skipping (requires netlify CLI)")
        return {"status": "skipped", "details": "Netlify CLI not available"}

    def check_domain_expiry(self) -> Dict:
        """Check domain expiration - simplified for Windows"""
        self.log("⚠️ Domain Expiry: Skipping (whois not standard on Windows)")
        return {"status": "skipped", "details": "whois not available"}

    def perform_check(self, check_name: str):
        """Perform a specific check"""
        self.log(f"🔍 Running check: {check_name}")

        check_map = {
            "SSL Certificate": self.check_ssl_basic,
            "Website Uptime": self.check_uptime_enhanced,
            "DNS Health": self.check_dns,
            "Netlify Builds": self.check_netlify_builds,
            "Domain Expiry": self.check_domain_expiry
        }

        check_func = check_map.get(check_name)
        if check_func:
            result = check_func()
            self.state["total_checks"] += 1
            return result
        else:
            self.log(f"❌ Unknown check: {check_name}")
            return {"status": "error", "details": "Unknown check"}

    def run_cycle(self):
        """Run one monitoring cycle"""
        self.log("=" * 60)
        self.log("Webby Enhanced Monitor - Starting cycle")
        self.log("=" * 60)

        check_name = CHECKS[self.current_check_index]
        self.perform_check(check_name)

        self.current_check_index = (self.current_check_index + 1) % len(CHECKS)
        self.save_state()

        self.log(f"Cycle complete. Next: {CHECKS[self.current_check_index]}")
        self.log("=" * 60)

    def run_continuous(self):
        """Run monitoring continuously"""
        self.log("🤖 Webby Enhanced Monitor started (Windows)")
        self.log(f"Monitoring: {SITE_DOMAIN}")
        self.log(f"Checks: {', '.join(CHECKS)} (every {CHECK_INTERVAL}s)")
        self.log(f"Voice notifications: {'ENABLED' if VOICE_ENABLED else 'DISABLED'}")

        # Startup notification
        self.voice.speak("Webby enhanced monitor is now active and protecting your website.")

        try:
            while True:
                self.run_cycle()
                time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            self.log("Stopping Webby Enhanced Monitor...")
            self.voice.speak("Webby monitor stopping.")
            self.save_state()
            sys.exit(0)


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Webby Enhanced Monitor")
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    parser.add_argument("--no-voice", action="store_true", help="Disable voice notifications")

    args = parser.parse_args()

    if args.no_voice:
        global VOICE_ENABLED
        VOICE_ENABLED = False

    monitor = WebbyEnhancedMonitor()

    if args.once:
        monitor.run_cycle()
    else:
        monitor.run_continuous()


if __name__ == "__main__":
    main()
ENDOFFILE

echo "✅ Windows-compatible Webby created at ~/Projects/webby_enhanced_monitor_windows.py"
```

Now copy to Windows (on **Windows** PowerShell):
```powershell
# Copy from Y:\ to C:\AgentBrain\webby\
Copy-Item "Y:\webby_enhanced_monitor_windows.py" -Destination "C:\AgentBrain\webby\webby_enhanced_monitor.py"

Write-Host "✅ Webby copied to Windows!"
```

---

### Step 4: Install Python Dependencies on Windows

**PowerShell**:
```powershell
# Install required packages
pip install requests pyttsx3

Write-Host "✅ Dependencies installed!"
```

---

### Step 5: Test Webby on Windows

**PowerShell**:
```powershell
# Run Webby once to test
python C:\AgentBrain\webby\webby_enhanced_monitor.py --once --no-voice

# Should run one check cycle and exit
```

**You should see**: Log output showing a check being performed (SSL, Uptime, or DNS).

---

### 🎯 Part B Complete!

**What You've Done**:
- ✅ Created C:\AgentBrain directory structure
- ✅ Copied Webby monitor from Mac to Windows
- ✅ Adapted Webby for Windows (cross-platform compatible)
- ✅ Installed Python dependencies
- ✅ Tested Webby successfully

**Next**: Create a FastAPI wrapper to expose Webby as an HTTP API!

---

## 🌐 Part C: Create Webby HTTP API (10 minutes)

We'll wrap Webby in a FastAPI server so you can control it via HTTP from your phone or other devices.

### Step 1: Install FastAPI and Dependencies

**PowerShell**:
```powershell
# Install FastAPI and Uvicorn (ASGI server)
pip install fastapi uvicorn python-multipart

Write-Host "✅ FastAPI installed!"
```

---

### Step 2: Create Webby API Server

Create `C:\AgentBrain\webby\webby_api.py`:

**PowerShell**:
```powershell
# Create API server file
@"
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, Dict, List
import json
import subprocess
import sys
from pathlib import Path
from datetime import datetime
import threading
import time

app = FastAPI(title="Webby Monitor API", version="1.0.0")

# Paths
STATE_FILE = Path.home() / ".webby_monitor_state.json"
LOG_FILE = Path.home() / ".webby_monitor.log"
MONITOR_SCRIPT = Path("C:/AgentBrain/webby/webby_enhanced_monitor.py")

# Global monitor thread
monitor_thread = None
monitor_running = False


class CheckRequest(BaseModel):
    check_type: str = "all"  # "ssl", "uptime", "dns", "all"
    notify: bool = False


class WebbyState(BaseModel):
    last_run: Optional[str]
    total_checks: int
    issues_found: int
    issues_fixed: int
    last_issue: Optional[Dict]
    check_history: List[Dict]
    notification_history: List[Dict]


def load_state() -> Dict:
    '''Load Webby monitor state'''
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except:
            pass

    return {
        \"last_run\": None,
        \"total_checks\": 0,
        \"issues_found\": 0,
        \"issues_fixed\": 0,
        \"last_issue\": None,
        \"check_history\": [],
        \"notification_history\": []
    }


def get_recent_logs(lines: int = 50) -> List[str]:
    '''Get recent log lines'''
    if not LOG_FILE.exists():
        return []

    try:
        with open(LOG_FILE, 'r') as f:
            all_lines = f.readlines()
            return [line.strip() for line in all_lines[-lines:]]
    except:
        return []


@app.get(\"/\")
async def root():
    '''API root'''
    return {
        \"service\": \"Webby Monitor API\",
        \"version\": \"1.0.0\",
        \"status\": \"online\",
        \"endpoints\": {
            \"/status\": \"Get current monitoring status\",
            \"/history\": \"Get check history\",
            \"/logs\": \"Get recent logs\",
            \"/run_check\": \"Trigger a manual check (POST)\"
        }
    }


@app.get(\"/status\")
async def get_status():
    '''Get current monitoring status'''
    state = load_state()

    return {
        \"status\": \"active\",
        \"last_run\": state.get(\"last_run\"),
        \"total_checks\": state.get(\"total_checks\", 0),
        \"issues_found\": state.get(\"issues_found\", 0),
        \"issues_fixed\": state.get(\"issues_fixed\", 0),
        \"last_issue\": state.get(\"last_issue\"),
        \"monitor_running\": monitor_running
    }


@app.get(\"/history\")
async def get_history(limit: int = 20):
    '''Get recent check history'''
    state = load_state()
    history = state.get(\"check_history\", [])

    return {
        \"history\": history[-limit:],
        \"total_checks\": len(history)
    }


@app.get(\"/logs\")
async def get_logs(lines: int = 50):
    '''Get recent log lines'''
    logs = get_recent_logs(lines)

    return {
        \"logs\": logs,
        \"count\": len(logs)
    }


@app.post(\"/run_check\")
async def run_check(request: CheckRequest, background_tasks: BackgroundTasks):
    '''Trigger a manual check'''

    def run_monitor():
        try:
            args = [sys.executable, str(MONITOR_SCRIPT), \"--once\"]
            if not request.notify:
                args.append(\"--no-voice\")

            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                timeout=120
            )

            return {
                \"success\": result.returncode == 0,
                \"output\": result.stdout,
                \"error\": result.stderr
            }
        except Exception as e:
            return {
                \"success\": False,
                \"error\": str(e)
            }

    # Run in background
    background_tasks.add_task(run_monitor)

    return {
        \"status\": \"check_started\",
        \"message\": \"Manual check initiated in background\",
        \"check_type\": request.check_type
    }


@app.get(\"/health\")
async def health_check():
    '''Health check endpoint'''
    return {
        \"status\": \"healthy\",
        \"timestamp\": datetime.now().isoformat()
    }


if __name__ == \"__main__\":
    import uvicorn
    uvicorn.run(app, host=\"0.0.0.0\", port=8000, log_level=\"info\")
"@ | Out-File -FilePath "C:\AgentBrain\webby\webby_api.py" -Encoding UTF8

Write-Host "✅ Webby API created!"
```

---

### Step 3: Test Webby API

**PowerShell** (open a new window):
```powershell
# Start the API server
python C:\AgentBrain\webby\webby_api.py

# Should show "Uvicorn running on http://0.0.0.0:8000"
# Leave this running
```

**Open another PowerShell window** to test:
```powershell
# Test status endpoint
Invoke-RestMethod -Uri "http://localhost:8000/status"

# Should return JSON with monitoring status

# Test running a check
Invoke-RestMethod -Uri "http://localhost:8000/run_check" -Method POST -Body '{"check_type":"ssl","notify":false}' -ContentType "application/json"

# Should return {"status":"check_started",...}
```

**You should see**: JSON responses from the API ✅

---

### Step 4: Access API from Mac (Test Cross-Machine)

On your **Mac**, get your Windows Tailscale IP:

**On Windows PowerShell**:
```powershell
# Get Windows Tailscale IP
tailscale ip -4
```

**On Mac Terminal**:
```bash
# Replace 100.x.x.x with Windows Tailscale IP
curl http://100.x.x.x:8000/status

# Should return JSON with Webby status!
```

**You should see**: Same JSON response as localhost test ✅

---

### Step 5: Create Windows Service for Auto-Start

Let's make Webby API start automatically when Windows boots.

**Create startup script** (`C:\AgentBrain\start_webby_api.bat`):

**PowerShell**:
```powershell
@"
@echo off
REM Start Webby API Server
cd C:\AgentBrain\webby
python webby_api.py > C:\AgentBrain\logs\webby_api.log 2>&1
"@ | Out-File -FilePath "C:\AgentBrain\start_webby_api.bat" -Encoding ASCII

Write-Host "✅ Startup script created!"
```

**Create Windows Task Scheduler entry**:

1. Press **Windows key**
2. Type **"Task Scheduler"** and open it
3. Click **"Create Basic Task"** (right sidebar)
4. **Name**: `Webby API Server`
5. **Description**: `Start Webby monitoring API on boot`
6. **Trigger**: Select **"When the computer starts"**
7. **Action**: Select **"Start a program"**
8. **Program/script**: `C:\AgentBrain\start_webby_api.bat`
9. **Check** "Open Properties dialog when finish"
10. Click **"Finish"**

**In the Properties dialog that opens**:
1. **General** tab:
   - Select **"Run whether user is logged on or not"**
   - Check **"Run with highest privileges"**
2. **Conditions** tab:
   - Uncheck **"Start the task only if the computer is on AC power"**
3. Click **"OK"**
4. Enter your Windows password

---

### Step 6: Test Auto-Start

**PowerShell** (as Administrator):
```powershell
# Test running the task manually
schtasks /Run /TN "Webby API Server"

# Wait a few seconds, then check if it's running
$process = Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.Path -like "*webby_api.py*"}
if ($process) {
    Write-Host "✅ Webby API is running! PID: $($process.Id)"
} else {
    Write-Host "❌ Webby API not running"
}

# Test the API
Invoke-RestMethod -Uri "http://localhost:8000/health"
```

**You should see**: API responding with health check ✅

---

### 🎯 Part C Complete!

**What You've Done**:
- ✅ Installed FastAPI and Uvicorn
- ✅ Created Webby HTTP API wrapper
- ✅ Tested API locally on Windows
- ✅ Verified API accessible from Mac via Tailscale
- ✅ Created Windows startup script
- ✅ Configured Task Scheduler for auto-start
- ✅ Tested automatic startup

**Next**: Set up Raspberry Pi Home Assistant integration!

---

## 🔧 Management Commands

### Check if Webby API is Running
```powershell
# Find Python processes
Get-Process python -ErrorAction SilentlyContinue

# Test API
Invoke-RestMethod -Uri "http://localhost:8000/health"
```

### Start Webby API Manually
```powershell
cd C:\AgentBrain\webby
python webby_api.py
```

### Stop Webby API
```powershell
# Find and kill Python processes running webby_api
Get-Process python | Where-Object {$_.Path -like "*webby_api.py*"} | Stop-Process -Force
```

### View Logs
```powershell
# View API logs
Get-Content C:\AgentBrain\logs\webby_api.log -Tail 50

# View Webby monitor logs
Get-Content $env:USERPROFILE\.webby_monitor.log -Tail 50
```

### Restart Task Scheduler Service
```powershell
# Stop task
schtasks /End /TN "Webby API Server"

# Start task
schtasks /Run /TN "Webby API Server"
```

---

## 🧪 Testing Checklist

Before moving to Pi setup, verify:

- [ ] **Network Drives**: Z:, Y:, M: drives visible in File Explorer
- [ ] **File Sync**: Can create file on Z:\ and see it on Mac
- [ ] **Webby Running**: `python C:\AgentBrain\webby\webby_enhanced_monitor.py --once` works
- [ ] **API Local**: `http://localhost:8000/status` returns JSON
- [ ] **API Remote**: Mac can reach `http://100.x.x.x:8000/status` (Windows Tailscale IP)
- [ ] **Auto-Start**: Task Scheduler has "Webby API Server" task enabled
- [ ] **Logs**: `C:\AgentBrain\logs\webby_api.log` exists and has content

---

## 🔧 Troubleshooting

### Can't Map Network Drives

**Issue**: `\\100.x.x.x\Documents` fails to connect

**Solutions**:
1. **Verify Mac File Sharing**: Mac → System Settings → Sharing → File Sharing ON
2. **Test connection**: `Test-NetConnection -ComputerName 100.x.x.x -Port 445`
3. **Try local IP first**: Use Mac's `192.168.68.x` instead of Tailscale IP
4. **Check credentials**: Windows Credential Manager → Remove old Mac credentials, try again
5. **Restart SMB**: On Mac, toggle File Sharing OFF then ON

---

### Python Command Not Found

**Issue**: `python` command not recognized

**Solutions**:
1. **Reinstall Python**: Download from [python.org](https://python.org/downloads)
2. **Check "Add to PATH"** during installation
3. **Use full path**: `C:\Users\YourName\AppData\Local\Programs\Python\Python311\python.exe`
4. **Add to PATH manually**:
   - Right-click "This PC" → Properties
   - Advanced system settings → Environment Variables
   - Edit PATH, add Python directory

---

### Webby API Won't Start

**Issue**: API fails to start or crashes

**Solutions**:
1. **Check port 8000**: `netstat -ano | findstr :8000` (should be empty)
2. **Kill existing process**: `Get-Process python | Stop-Process -Force`
3. **Check dependencies**: `pip list | findstr -i "fastapi uvicorn"`
4. **Run manually to see errors**: `python C:\AgentBrain\webby\webby_api.py`
5. **View logs**: `Get-Content C:\AgentBrain\logs\webby_api.log`

---

### Task Scheduler Won't Start Task

**Issue**: Task shows error or won't run

**Solutions**:
1. **Check task history**: Task Scheduler → Task → History tab
2. **Verify script path**: Open task properties, verify paths are correct
3. **Test script manually**: Double-click `C:\AgentBrain\start_webby_api.bat`
4. **Run as Administrator**: Task properties → General → "Run with highest privileges"
5. **Check logs**: Event Viewer → Windows Logs → Application

---

### Can't Reach API from Mac

**Issue**: Mac can't access `http://100.x.x.x:8000`

**Solutions**:
1. **Verify Tailscale**: `tailscale status` on both machines
2. **Test locally first**: On Windows, `http://localhost:8000/status` should work
3. **Check Windows Firewall**:
   - Windows Security → Firewall & network protection
   - Allow an app → Python → Check "Private" and "Public"
4. **Get correct IP**: On Windows, `tailscale ip -4` to verify IP
5. **Ping test**: From Mac, `ping 100.x.x.x` (Windows Tailscale IP)

---

## 🎉 You're Done!

Your Windows mini PC is now:
- ✅ **Connected to Mac**: Z:, Y:, M: network drives mounted
- ✅ **Running Webby**: Website monitoring active
- ✅ **Exposing API**: FastAPI server on port 8000
- ✅ **Auto-Starting**: Launches on Windows boot
- ✅ **Network Accessible**: Reachable via Tailscale from any device

**Next Step**: Move to [Pi Home Assistant Integration](./PI_HOME_ASSISTANT_SETUP.md) to connect your smart home!

---

**Your Windows agent brain is ready to orchestrate everything!** 🧠🚀
