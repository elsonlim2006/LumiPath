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
        # Step A: Matching for both scenarios (Moderate vs Accelerated)
        matches_mod = self.matcher.match_top_roles(worker, scenario="moderate")
        matches_acc = self.matcher.match_top_roles(worker, scenario="accelerated")
        top_1 = matches_mod[0] if matches_mod else None

        # Step B: Trends (Calls Gemini with whitelist)
        trends = self.trend_service.analyze_trends(worker)

        # Step C: Dual Pathways for Top Roles under each scenario
        def serialize_pathway(pw):
            return {
                "total_estimated_weeks": pw.total_estimated_weeks,
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
                    } for p in pw.phases
                ]
            }

        def build_roles_data(matches, pace):
            roles_list = []
            for m in matches:
                pw = self.pathway_service.plan_pathway(m, pace=pace)
                roles_list.append({
                    "rank": m.rank,
                    "role_code": m.role_code,
                    "role_title": m.role_title,
                    "match_score": m.match_score,
                    "score_breakdown": m.score_breakdown,
                    "salary_range": m.salary_range,
                    "matched_skills": m.matched_skills,
                    "missing_skills": m.missing_skills,
                    "malaysia_col_aligned": m.malaysia_col_aligned,
                    "pathway": serialize_pathway(pw)
                })
            return roles_list

        mod_roles = build_roles_data(matches_mod, pace="moderate")
        acc_roles = build_roles_data(matches_acc, pace="accelerated")
        default_pathway = mod_roles[0]["pathway"] if mod_roles else {}

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
        ) if top_1 else False

        if is_green:
            sdg_list.append({
                "sdg_code": "SDG 13",
                "sdg_name": "Climate Action",
                "targets": ["Target 13.3"]
            })

        # Dual scenarios & disclaimer
        snapshot = self.data_loader.get_trend_snapshot()
        disclaimer = snapshot.get("disclaimer", "All match scores, skill gaps, and salary benchmarks are indicative estimates based on O*NET 28.1, TalentCorp COL, and Hays Asia 2025. They serve as guidance only and do not guarantee future employment, wages, or training subsidies.")

        scenarios = {
            "moderate": {
                "scenario_name": "Moderate Transition",
                "timeline_horizon": "3-5 Years",
                "macro_impact_rate": 0.42,
                "urgency_level": "Medium",
                "recommended_duration_weeks": 14,
                "declining_skills": trends.declining_skills or ["Manual Titration", "Excel Data Entry", "Paper Log Archiving"],
                "emerging_skills": trends.emerging_skills or ["Spectrometry Automation", "Green Chemistry Compliance", "Lab Data Digital Logging"],
                "matched_roles": mod_roles
            },
            "accelerated": {
                "scenario_name": "Fast Disruption",
                "timeline_horizon": "1-2 Years",
                "macro_impact_rate": 0.74,
                "urgency_level": "High",
                "recommended_duration_weeks": 8,
                "declining_skills": ["Routine Wet Lab Titration", "Manual Batch Sampling", "Paper QA Checklists"],
                "emerging_skills": ["Electrochemical Testing", "Automated Assembly Monitoring", "SCADA & Cleanroom Ops"],
                "matched_roles": acc_roles
            }
        }

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
            "matched_roles": mod_roles,
            "reskilling_pathway": default_pathway,
            "sdg_alignment": sdg_list,
            "uncertainty_scenarios": scenarios,
            "disclaimer": disclaimer
        }
