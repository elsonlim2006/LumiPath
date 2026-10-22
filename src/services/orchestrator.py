from ..models.entities import WorkerProfile
from .matcher_service import RoleMatcherService
from .trend_service import TrendAnalyzerService
from .pathway_service import PathwayPlannerService
from ..infra.data_loader import DataLoader
from ..infra.gemini_client import GeminiClient

class WorkflowOrchestrator:
    def __init__(self, gemini_client: GeminiClient = None):
        self.data_loader = DataLoader()
        self.client = gemini_client or GeminiClient()
        self.matcher = RoleMatcherService()
        self.trend_service = TrendAnalyzerService(self.client)
        self.pathway_service = PathwayPlannerService()

    def run_full_diagnosis(self, worker: WorkerProfile) -> dict:
        # Step A: Matching (Local math, fast)
        matches = self.matcher.match_top_roles(worker)
        top_1 = matches[0] if matches else None

        # Step B: Trends (Calls Gemini with whitelist)
        trends = self.trend_service.analyze_trends(worker)

        # Step C: Pathway for Top 1
        pathway = self.pathway_service.plan_pathway(top_1)

        # Step D: Assemble SDGs
        sdg_list = [
            {
                "sdg_code": "SDG 4",
                "sdg_name": "Quality Education",
                "targets": ["Target 4.3", "Target 4.4"]
            },
            {
                "sdg_code": "SDG 8",
                "sdg_name": "Decent Work and Economic Growth",
                "targets": ["Target 8.2", "Target 8.5"]
            }
        ]
        # Activate SDG 13 if role has green orientation or addresses green skills
        is_green = (
            "green" in top_1.role_title.lower()
            or "environmental" in top_1.role_title.lower()
            or "hydrogen" in top_1.role_title.lower()
            or any("green" in s.lower() for s in (top_1.matched_skills + top_1.missing_skills))
        )
        if is_green:
            sdg_list.append({
                "sdg_code": "SDG 13",
                "sdg_name": "Climate Action",
                "targets": ["Target 13.3"]
            })

        # Dual scenarios & disclaimer
        snapshot = self.data_loader.get_trend_snapshot()
        scenarios = {
            "moderate": snapshot.get("moderate_scenario", {}),
            "accelerated": snapshot.get("accelerated_scenario", {})
        }
        disclaimer = snapshot.get("disclaimer", "")

        return {
            "worker_profile": {
                "worker_id": worker.worker_id,
                "worker_name": worker.worker_name,
                "current_role": worker.current_role,
                "experience_years": worker.experience_years,
                "education_background": worker.education_background,
                "target_domains": worker.target_domains,
                "current_skills": worker.current_skills
            },
            "trend_signals": {
                "source_name": trends.source_name,
                "snapshot_date": trends.snapshot_date,
                "macro_impact_rate": trends.macro_impact_rate,
                "market_growth_rate": trends.market_growth_rate,
                "declining_skills": trends.declining_skills,
                "emerging_skills": trends.emerging_skills
            },
            "matched_roles": [
                {
                    "rank": m.rank,
                    "role_code": m.role_code,
                    "role_title": m.role_title,
                    "match_score": m.match_score,
                    "score_breakdown": m.score_breakdown,
                    "salary_range": m.salary_range,
                    "matched_skills": m.matched_skills,
                    "missing_skills": m.missing_skills,
                    "malaysia_col_aligned": m.malaysia_col_aligned
                } for m in matches
            ],
            "reskilling_pathway": {
                "total_estimated_weeks": pathway.total_estimated_weeks,
                "phases": [
                    {
                        "phase_number": p.phase_number,
                        "phase_name": p.phase_name,
                        "duration_weeks": p.duration_weeks,
                        "skills_addressed": p.skills_addressed,
                        "recommended_resource": {
                            "course_name": p.recommended_resource.course_name,
                            "provider": p.recommended_resource.provider,
                            "cost_type": p.recommended_resource.cost_type
                        },
                        "milestone_credential": p.milestone_credential
                    } for p in pathway.phases
                ]
            },
            "sdg_alignment": sdg_list,
            "uncertainty_scenarios": scenarios,
            "disclaimer": disclaimer
        }
