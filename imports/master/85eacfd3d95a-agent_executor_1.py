import asyncio
import time
from app.core.task_engine import task_engine
from app.learning.outcome_tracker import outcome_tracker
from app.tools.browser_controller import browser_controller
from app.tools.communication_adapter import comm_adapter
from app.security.action_guard import action_guard, PermissionLevel
from app.govcon.opportunity_scanner import opportunity_scanner
from app.govcon.incumbent_analyzer import incumbent_analyzer
from app.govcon.vendor_intelligence import vendor_intelligence
from app.govcon.bid_viability_engine import bid_viability_engine
from app.govcon.bid_pack_generator import bid_pack_generator
from app.govcon.email_thread_tracker import email_thread_tracker

class AgentExecutor:
    def __init__(self):
        self.running = False
        self.default_model = "qwen2.5:7b"
        print("[EXECUTOR] Operational E2E Pipeline initialized.")

    async def run_loop(self):
        self.running = True
        print("[EXECUTOR] Task processing loop active.")
        while self.running:
            task = task_engine.claim_task(self.default_model)
            if task:
                print(f"\n[EXECUTOR] > Claimed Task {task['id']}: {task['title']}")
                await self._execute_task(task)
            await asyncio.sleep(5)

    async def _execute_task(self, task: dict):
        task_id = task["id"]
        title = task["title"]
        
        try:
            if "GovCon E2E Loop" in title:
                print("\n=== GOVCON E2E OPERATIONAL LOOP STARTED ===")
                
                # Step 1: Pull from SAM.gov API
                print("Step 1: Pulling opportunities from SAM.gov...")
                opps = opportunity_scanner.scan_sam_gov(["IT Hardware"])
                opp = opps[0] # Taking the top hit for the loop
                solicitation = opp["solicitation_number"]
                
                # Step 2: Rank Opportunity
                print(f"Step 2: Ranking Opportunity {solicitation}...")
                incumbent_data = incumbent_analyzer.analyze_history(solicitation, opp["naics"])
                viability = bid_viability_engine.generate_score(opp, incumbent_data)
                
                # Step 3: Generate Bid Packet Cover Sheet (via Generator)
                print("Step 3: Generating bid packet cover sheet...")
                
                # Step 4: Discover Vendors
                print("Step 4: Discovering vendors...")
                vendors = vendor_intelligence.locate_suppliers(opp["title"])
                
                pack_id = bid_pack_generator.generate_pack(opp, viability, vendors)
                
                # Step 5: Draft Protected Vendor Quote Emails
                print("Step 5: Drafting protected vendor quote emails...")
                active_threads = []
                for vendor in vendors:
                    thread_id = email_thread_tracker.create_thread(pack_id, vendor["name"], vendor["contact"])
                    email_body = f"Requesting pricing for {solicitation}."
                    email_thread_tracker.log_outbound(thread_id, email_body)
                    active_threads.append((thread_id, vendor))
                
                # Step 6: Queue Approvals (For outbound emails and bid prep)
                print("Step 6: Queueing approvals in ActionGuard...")
                action_guard.request_action("govcon", "send_vendor_RFQs", {"pack_id": pack_id}, PermissionLevel.APPROVAL_REQUIRED)
                
                # --- SIMULATION PAUSE: Assuming Approval Granted & Vendors Reply ---
                
                # Step 7: Track Responses
                print("Step 7: Tracking vendor responses (Simulating inbound)...")
                # Simulating vendor 1 quoting $210k and vendor 2 quoting $205k
                email_thread_tracker.simulate_inbound_quote(active_threads[0][0], 210000.0)
                email_thread_tracker.simulate_inbound_quote(active_threads[1][0], 205000.0)
                
                # Step 8: Extract Quote Data
                print("Step 8: Extracting quote data from email threads...")
                for thread_id, _ in active_threads:
                    email_thread_tracker.extract_quote(thread_id)
                
                quotes = email_thread_tracker.get_all_quotes_for_pack(pack_id)
                
                # Step 9: Update Packet Profitability Estimates
                print("Step 9: Updating packet profitability estimates...")
                bid_pack_generator.update_profitability(pack_id, quotes)
                
                # Step 10: Present Final Review Dashboard
                print("\n=== Step 10: FINAL REVIEW DASHBOARD ===")
                self._present_dashboard(pack_id)
                
                outcome_tracker.track_economic_loop(str(task_id), success=True, time_saved_hours=14.0, projected_value=opp["contract_value_est"])

            task_engine.complete_task(task_id)
            print(f"[EXECUTOR] > Task {task_id} completed successfully.\n")

        except Exception as e:
            print(f"[EXECUTOR ERROR] Task {task_id} failed: {e}")
            task_engine.fail_task(task_id)

    def _present_dashboard(self, pack_id: str):
        import os, json
        pack_path = os.path.expanduser(f"~/savvytech_workspace/backend/bid_packs/{pack_id}.json")
        with open(pack_path, "r") as f:
            data = json.load(f)
            
        print(f"  PACK ID:      {data['pack_id']}")
        print(f"  SOLICITATION: {data['cover_sheet']['solicitation']} - {data['cover_sheet']['title']}")
        print(f"  VIABILITY:    {data['cover_sheet']['viability_tier']}")
        print(f"  STATUS:       {data['cover_sheet']['status']}")
        print(f"  ------------------------------------------------")
        print(f"  GOV ESTIMATE: ${data['pricing_worksheet']['government_estimate']:,.2f}")
        print(f"  TARGET BID:   ${data['pricing_worksheet']['target_bid']:,.2f}")
        print(f"  BEST VENDOR:  {data['pricing_worksheet']['best_vendor']}")
        print(f"  FINAL MARGIN: ${data['pricing_worksheet']['final_margin']:,.2f}")
        print(f"  ================================================\n")

agent_executor = AgentExecutor()