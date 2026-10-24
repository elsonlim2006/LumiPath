"""RunPod Serverless Handler for Future-Ready Workforce Pipeline.

Deploys the LumiPath diagnosis and reskilling engine as a RunPod Serverless Endpoint
for fast-response workflow orchestration and low-latency inference.
"""

import os
import sys

# Ensure parent directory is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from src.models.entities import WorkerProfile
from src.services.orchestrator import WorkflowOrchestrator

# Initialize orchestrator once for warm container reuse
orchestrator = WorkflowOrchestrator()


def handler(job: dict) -> dict:
    """Execute end-to-end diagnosis pipeline on job input."""
    job_input = job.get("input", {})

    worker = WorkerProfile(
        worker_id=job_input.get("worker_id", "RUNPOD-WORKER-01"),
        worker_name=job_input.get("worker_name", "Alex Tan"),
        current_role=job_input.get("current_role", "Chemical Laboratory Technician"),
        experience_years=float(job_input.get("experience_years", 3.5)),
        education_background=job_input.get("education_background", "Diploma in Chemical Process Technology"),
        target_domains=job_input.get("target_domains", ["Green Chemistry", "Sustainable Manufacturing"]),
        current_skills=job_input.get("current_skills", ["Manual Titration", "Excel Data Entry", "SOP Inspection"]),
    )

    result = orchestrator.run_full_diagnosis(worker)
    return {"status": "success", "data": result}


if __name__ == "__main__":
    try:
        import runpod

        if hasattr(runpod, "serverless"):
            runpod.serverless.start({"handler": handler})
        else:
            raise ImportError("Local directory collision: official runpod SDK not installed.")
    except ImportError:
        print("[RunPod Handler] 'runpod' SDK not active in local environment.")
        print("[RunPod Handler] Running local self-test with benchmark worker profile...")
        test_job = {
            "input": {
                "worker_id": "BENCHMARK-RUNPOD-01",
                "worker_name": "Dr. Benchmark",
                "current_role": "Chemical Quality Analyst",
                "experience_years": 4.0,
                "education_background": "Bachelor of Chemical Science",
                "target_domains": ["Green Chemistry"],
                "current_skills": ["Manual Titration", "SOP Inspection"],
            }
        }
        res = handler(test_job)
        print(f"[RunPod Handler OK] Status: {res['status']}, Top Role: {res['data']['matched_roles'][0]['role_title']}")
