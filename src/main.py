"""SDC Hackathon 2026 - Main Application Entry Point
Domain 1: Future-Ready Workforce (Chemical & Sustainable Engineering)
"""

import os
import sys
import time

# Ensure UTF-8 console output encoding on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure code root directory is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.models.entities import WorkerProfile
from src.services.orchestrator import WorkflowOrchestrator


def main() -> None:
    print("=" * 60)
    print(" [SDC Hackathon 2026] Future-Ready Workforce Pipeline")
    print("=" * 60)

    # 1. Inject benchmark worker profile (Alex Tan - Chemical Lab Tech)
    sample_worker = WorkerProfile(
        worker_id="WORKER-DEMO-01",
        worker_name="Alex Tan",
        current_role="Chemical Laboratory Technician",
        experience_years=3.5,
        education_background="Diploma in Chemical Process Technology",
        target_domains=["Green Chemistry", "Sustainable Manufacturing"],
        current_skills=["Manual Titration", "Excel Data Entry", "SOP Inspection"],
    )

    print(f"[*] Worker Profile: {sample_worker.worker_name} | {sample_worker.current_role} | Experience: {sample_worker.experience_years} years")
    print(f"[*] Possessed Skills: {sample_worker.current_skills}")
    print("\n[*] Starting WorkflowOrchestrator for end-to-end diagnosis...")

    start_time = time.time()
    orchestrator = WorkflowOrchestrator()
    result = orchestrator.run_full_diagnosis(sample_worker)
    elapsed = time.time() - start_time

    print(f"[OK] Diagnosis complete! Total elapsed time: {elapsed:.2f}s (Crash-prevention timeout threshold: 8.0s)")

    # 2. Display key business deduction results
    top_match = result["matched_roles"][0]
    score_pct = int(round(top_match['match_score'] * 100)) if top_match['match_score'] <= 1.0 else int(top_match['match_score'])
    print(f"\n[*] Top 1 Recommended Role: {top_match['role_title']} ({top_match['role_code']})")
    print(f"    - Overall Match Score:  {score_pct}%")
    print(f"    - Scoring Breakdown:    {top_match['score_breakdown']}")
    print(f"    - Market Salary Range:  {top_match['salary_range']}")
    if top_match.get("malaysia_col_aligned"):
        print(f"    - National Priority:    Aligned with TalentCorp Critical Occupations List (COL)")
    print(f"    - Skill Gaps Identified:{top_match['missing_skills']}")

    trends = result["trend_signals"]
    print(f"\n[*] External Trend Signals (Source: {trends['source_name']})")
    print(f"    - Declining Skills:     {trends['declining_skills']}")
    print(f"    - Emerging Core Skills: {trends['emerging_skills']}")

    pathway = result["reskilling_pathway"]
    print(f"\n[*] 3-Phase Reskilling Pathway (Total Duration: {pathway['total_estimated_weeks']} weeks)")
    for phase in pathway["phases"]:
        res = phase["recommended_resource"]
        print(f"    - Phase {phase['phase_number']} ({phase['phase_name']}, {phase['duration_weeks']} weeks): Targeted Skills {phase['skills_addressed']}")
        print(f"      Recommended Course:   {res['course_name']} [{res['provider']} / {res['cost_type']}]")

    print("\n[*] UN Sustainable Development Goals (SDG) Alignment:")
    for sdg in result["sdg_alignment"]:
        print(f"    - [{sdg['sdg_code']}] {sdg['sdg_name']} (Targets: {', '.join(sdg['targets'])})")

    # 3. Validate structural schema contract integrity
    required_keys = [
        "worker_profile",
        "trend_signals",
        "matched_roles",
        "reskilling_pathway",
        "sdg_alignment",
        "uncertainty_scenarios",
        "disclaimer",
    ]
    assert all(k in result for k in required_keys), "Contract schema validation failed: missing root keys!"
    print("\n" + "=" * 60)
    print(" [SUCCESS] All 7 root contract keys validated. Zero crashes.")
    print("=" * 60)


if __name__ == "__main__":
    main()
