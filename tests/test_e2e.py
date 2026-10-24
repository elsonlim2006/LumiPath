"""SDC Hackathon 2026 - LumiPath End-to-End Automated Test
"""
import os
import sys
import unittest

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from src.models.entities import WorkerProfile
from src.services.profile_service import ProfileParserService
from src.services.orchestrator import WorkflowOrchestrator
from src.infra.data_loader import DataLoader


class TestE2EWorkflow(unittest.TestCase):
    def test_e2e_flow(self):
        print("=== LUMIPATH END-TO-END VERIFICATION TEST ===")

        # Step 1 Test: Extract from actual generated PDF
        pdf_path = os.path.join(parent_dir, "src", "data", "Wong_Swee_Tiam_Resume.pdf")
        self.assertTrue(os.path.exists(pdf_path), f"Resume PDF must exist at {pdf_path}")
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        parser = ProfileParserService(timeout=4.0)
        text = parser.extract_text_from_upload(pdf_bytes, "Wong_Swee_Tiam_Resume.pdf")
        self.assertGreater(len(text), 100, "Extracted text should not be empty")
        worker, is_fallback = parser.parse_resume_text(text)
        print(f"[Step 1 -> 2 OK] Extracted Worker: {worker.worker_name} ({worker.current_role}), Fallback: {is_fallback}")

        # Step 2 Test: Edit / Calibrate with custom skill
        worker.current_skills.append("Industrial Automation Protocol")
        loader = DataLoader()
        all_skills = loader.get_all_skill_candidates()
        self.assertGreaterEqual(len(all_skills), 30, "Skill catalog should have at least 30 entries")
        print(f"[Step 2 OK] Verified {len(all_skills)} skill candidates & added custom skill safely.")

        # Step 3 Test: Confirm & Diagnosis Orchestration
        orch = WorkflowOrchestrator()
        diag = orch.run_full_diagnosis(worker)
        self.assertIn("matched_roles", diag)
        self.assertGreaterEqual(len(diag["matched_roles"]), 1)
        self.assertIn("trend_signals", diag)
        top_role = diag["matched_roles"][0]
        role_title = top_role["role_title"]
        match_score = top_role["match_score"]
        print(f"[Step 3 OK] Diagnosis generated Top 1 Role: {role_title} (Score: {match_score * 100:.1f}%)")

        # Step 4 Test: Deep Dive Pathway & SDG
        self.assertIn("reskilling_pathway", diag)
        phases = diag["reskilling_pathway"].get("phases", [])
        self.assertEqual(len(phases), 3, "Must have exactly 3 phases")
        self.assertTrue(any(sdg["sdg_code"] == "SDG 8" for sdg in diag.get("sdg_alignment", [])))
        p3_credential = phases[2]["milestone_credential"]
        print(f"[Step 4 OK] 3-Phase roadmap validated. Phase 3 Credential: {p3_credential}")
        print("=== ALL 4 STEPS E2E VERIFIED SUCCESSFULLY ===")


if __name__ == "__main__":
    unittest.main()
