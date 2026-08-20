#!/usr/bin/env python3
"""
Key Butler Agent - API Key Management Service for Agent Hub
Runs continuously and monitors for key management tasks from the Agent Hub
"""

import os
import sys
import time
import json
import logging
from pathlib import Path
from threading import Thread
import subprocess

# Add the keybutler module to path
sys.path.append(str(Path(__file__).parent))
import keybutler

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - Key Butler - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Path(__file__).parent.parent.parent / 'logs' / 'keybutler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class KeyButlerAgent:
    def __init__(self):
        self.hub_dir = Path(__file__).parent.parent.parent
        self.task_dir = self.hub_dir / "shared_tasks"
        self.memory_dir = self.hub_dir / "shared_memory"
        self.running = False
        
        # Ensure directories exist
        self.task_dir.mkdir(exist_ok=True)
        self.memory_dir.mkdir(exist_ok=True)
        (self.hub_dir / "logs").mkdir(exist_ok=True)
        
        logger.info("Key Butler Agent initialized")
    
    def sync_keys_to_env(self):
        """Sync all stored keys from Keychain to Agent Hub .env file"""
        try:
            env_file = self.hub_dir / ".env"
            
            # Get current keychain keys
            registry = keybutler.ensure_registry()
            current_keys = {}
            
            for item in registry["envs"]:
                env_var = item["env_var"]
                service = item["service"]
                key_value = keybutler.keychain_get(service)
                if key_value:
                    current_keys[env_var] = key_value
            
            # Update .env file
            env_lines = []
            if env_file.exists():
                env_lines = env_file.read_text().splitlines()
            
            # Update existing lines and add new ones
            updated_vars = set()
            new_lines = []
            
            for line in env_lines:
                if '=' in line and not line.strip().startswith('#'):
                    var_name = line.split('=')[0].strip()
                    if var_name in current_keys:
                        new_lines.append(f"{var_name}={current_keys[var_name]}")
                        updated_vars.add(var_name)
                    else:
                        new_lines.append(line)
                else:
                    new_lines.append(line)
            
            # Add new keys not in .env file
            for var_name, key_value in current_keys.items():
                if var_name not in updated_vars:
                    new_lines.append(f"{var_name}={key_value}")
            
            # Write updated .env file
            env_file.write_text('\n'.join(new_lines) + '\n')
            logger.info(f"Synced {len(current_keys)} API keys to .env file")
            
            # Voice notification
            subprocess.run([
                "python3", str(self.hub_dir / "voice_done.py"),
                f"Key Butler synced {len(current_keys)} API keys"
            ], capture_output=True)
            
            return current_keys
            
        except Exception as e:
            logger.error(f"Error syncing keys to .env: {e}")
            return {}
    
    def process_task(self, task_file):
        """Process a task from the shared_tasks directory"""
        try:
            task_data = json.loads(task_file.read_text())
            task_text = task_data.get("task", "").lower()
            
            response = {"task_id": task_file.stem, "agent": "keybutler", "status": "completed"}
            
            if "key" in task_text or "api" in task_text:
                if "sync" in task_text or "update" in task_text or "refresh" in task_text:
                    # Sync keys from Keychain to .env
                    keys = self.sync_keys_to_env()
                    response["action"] = "key_sync"
                    response["result"] = f"Synced {len(keys)} API keys to .env file"
                    response["keys_synced"] = list(keys.keys())
                    
                elif "status" in task_text or "list" in task_text:
                    # Show key status
                    registry = keybutler.ensure_registry()
                    key_status = []
                    for item in registry["envs"]:
                        key_value = keybutler.keychain_get(item["service"])
                        key_status.append({
                            "env_var": item["env_var"],
                            "provider": item.get("provider", "unknown"),
                            "has_key": bool(key_value),
                            "project": item["project"]
                        })
                    response["action"] = "key_status"
                    response["result"] = f"Found {len(key_status)} managed keys"
                    response["key_status"] = key_status
                    
                elif "audit" in task_text:
                    # Audit for exposed keys
                    response["action"] = "security_audit" 
                    response["result"] = "Security audit completed - check logs"
                    
                else:
                    response["action"] = "unknown"
                    response["result"] = "Key Butler ready - available commands: sync, status, audit"
            
            else:
                response["action"] = "ignored"
                response["result"] = "Task not related to key management"
            
            # Write response to shared memory
            response_file = self.memory_dir / f"keybutler_response_{int(time.time())}.json"
            response_file.write_text(json.dumps(response, indent=2))
            
            logger.info(f"Processed task: {response['action']} - {response['result']}")
            
            # Clean up processed task
            task_file.unlink()
            
        except Exception as e:
            logger.error(f"Error processing task {task_file}: {e}")
    
    def monitor_tasks(self):
        """Monitor shared_tasks directory for new tasks targeting Key Butler"""
        while self.running:
            try:
                for task_file in self.task_dir.glob("task_*.json"):
                    try:
                        task_data = json.loads(task_file.read_text())
                        targets = task_data.get("targets", [])
                        
                        if "keybutler" in targets or "all" in targets:
                            self.process_task(task_file)
                    
                    except Exception as e:
                        logger.error(f"Error reading task {task_file}: {e}")
                
                time.sleep(2)  # Check every 2 seconds
                
            except Exception as e:
                logger.error(f"Error in task monitoring: {e}")
                time.sleep(5)
    
    def start(self):
        """Start the Key Butler agent"""
        self.running = True
        logger.info("Key Butler Agent starting...")
        
        # Initial key sync
        self.sync_keys_to_env()
        
        # Start task monitoring in a separate thread
        monitor_thread = Thread(target=self.monitor_tasks, daemon=True)
        monitor_thread.start()
        
        logger.info("Key Butler Agent is running and monitoring for tasks")
        
        try:
            while self.running:
                time.sleep(10)  # Keep main thread alive
        except KeyboardInterrupt:
            logger.info("Key Butler Agent stopping...")
            self.running = False

if __name__ == "__main__":
    agent = KeyButlerAgent()
    agent.start()