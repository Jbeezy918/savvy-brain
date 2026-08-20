import time
import uuid
from typing import Dict, List, Optional
from app.agents.specialists import SPECIALIST_AGENTS
from app.core.task_engine import task_engine

class AgentPoolManager:
    def __init__(self):
        self.active_workers: Dict[str, dict] = {}
        self.workload_stats: Dict[str, int] = {} # Tracks total tasks completed per worker type
        self.max_concurrency = 8 # Tightened to prevent uncontrolled spawning
        self.idle_timeout = 300 # 5 minutes
        print("[POOL MANAGER] Dynamic controlled worker pool initialized.")

    def spawn_worker(self, agent_type: str) -> Optional[str]:
        if len(self.active_workers) >= self.max_concurrency:
            print("[POOL MANAGER] Max concurrency reached. Blocking spawn.")
            return None
            
        worker_id = f"worker_{agent_type}_{str(uuid.uuid4())[:8]}"
        self.active_workers[worker_id] = {
            "type": agent_type,
            "status": "idle",
            "current_task": None,
            "last_heartbeat": time.time(),
            "spawned_at": time.time()
        }
        self.workload_stats[agent_type] = self.workload_stats.get(agent_type, 0)
        print(f"[POOL MANAGER] Controlled spawn: {worker_id}")
        return worker_id

    def heartbeat(self, worker_id: str):
        if worker_id in self.active_workers:
            self.active_workers[worker_id]["last_heartbeat"] = time.time()

    def assign_task(self, worker_id: str, task_id: str):
        if worker_id in self.active_workers:
            self.active_workers[worker_id]["status"] = "busy"
            self.active_workers[worker_id]["current_task"] = task_id
            self.active_workers[worker_id]["last_heartbeat"] = time.time()

    def release_worker(self, worker_id: str):
        if worker_id in self.active_workers:
            agent_type = self.active_workers[worker_id]["type"]
            self.workload_stats[agent_type] += 1
            self.active_workers[worker_id]["status"] = "idle"
            self.active_workers[worker_id]["current_task"] = None

    def prune_and_reassign(self):
        """Monitors heartbeats and reassigns tasks from dead workers."""
        now = time.time()
        dead_workers = []
        for wid, data in self.active_workers.items():
            # Idle too long
            if data["status"] == "idle" and (now - data["last_heartbeat"]) > self.idle_timeout:
                dead_workers.append(wid)
            # Busy but heartbeat stopped (Worker Crash)
            elif data["status"] == "busy" and (now - data["last_heartbeat"]) > (self.idle_timeout * 2):
                print(f"[POOL MANAGER ALERT] Worker {wid} unresponsive. Reassigning task {data['current_task']}")
                task_id = data["current_task"]
                if task_id:
                    task_engine.retry_task(int(task_id)) # Push back to queue
                dead_workers.append(wid)

        for wid in dead_workers:
            del self.active_workers[wid]
            print(f"[POOL MANAGER] Worker {wid} terminated.")

agent_pool_manager = AgentPoolManager()