import json
import os
import time
from typing import List, Dict, Any

class BaseAgent:
    def __init__(self, name: str, role: str, allowed_skills: List[str]):
        self.name = name
        self.role = role
        self.allowed_skills = allowed_skills
        self.memory_dir = os.path.expanduser("~/savvytech_workspace/backend/agent_memory")
        os.makedirs(self.memory_dir, exist_ok=True)
        self.memory_file = os.path.join(self.memory_dir, f"{self.name.lower().replace(' ', '_')}.json")
        self._init_memory()

    def _init_memory(self):
        if not os.path.exists(self.memory_file):
            with open(self.memory_file, 'w') as f:
                json.dump({
                    "successful_strategies": [], 
                    "mistakes": [], 
                    "execution_stats": {"runs": 0, "success": 0, "failures": 0}, 
                    "confidence_level": 1.0
                }, f, indent=4)

    def update_memory(self, success: bool, notes: str):
        with open(self.memory_file, 'r') as f:
            mem = json.load(f)
            
        mem["execution_stats"]["runs"] += 1
        if success:
            mem["execution_stats"]["success"] += 1
            if notes and notes not in mem["successful_strategies"]:
                mem["successful_strategies"].append(notes)
            mem["confidence_level"] = min(1.0, mem["confidence_level"] + 0.05)
        else:
            mem["execution_stats"]["failures"] += 1
            if notes and notes not in mem["mistakes"]:
                mem["mistakes"].append(notes)
            mem["confidence_level"] = max(0.1, mem["confidence_level"] - 0.15)
            
        with open(self.memory_file, 'w') as f:
            json.dump(mem, f, indent=4)

    async def execute(self, task_details: Dict[str, Any]) -> Dict[str, Any]:
        """Base execution method. Overridden by specific specialist logic or skills."""
        print(f"[{self.name.upper()}] Starting task: {task_details.get('description', 'Unknown Task')}")
        # In a full implementation, this dynamically maps self.allowed_skills to the SkillRegistry
        
        # Simulating execution success
        self.update_memory(success=True, notes="Successfully parsed standard data schema.")
        return {"status": "success", "agent": self.name, "output": f"Task executed within bounds."}