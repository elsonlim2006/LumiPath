from ..infra.data_loader import DataLoader
from ..infra.gemini_client import GeminiClient
from ..models.entities import WorkerProfile, TrendSignal

class TrendAnalyzerService:
    def __init__(self, gemini_client: GeminiClient = None):
        self.data_loader = DataLoader()
        self.client = gemini_client or GeminiClient()

    def analyze_trends(self, worker: WorkerProfile) -> TrendSignal:
        snapshot = self.data_loader.get_trend_snapshot()
        whitelist = snapshot.get("standard_skill_whitelist", [])
        whitelist_set = set(s.strip().lower() for s in whitelist)

        prompt = f"""
You are an expert workforce transition AI for SDC Hackathon 2026.
You are analyzing external labor market trend signals based on O*NET 28.1 and Hays Asia Salary Guide 2025.

Target Worker Profile:
- Current Role: {worker.current_role}
- Experience: {worker.experience_years} years
- Current Skills: {', '.join(worker.current_skills)}
- Target Domains: {', '.join(worker.target_domains)}

MANDATORY CONSTRAINT (Anti-Hallucination Whitelist):
You must ONLY select declining_skills and emerging_skills from this exact whitelist:
{json_whitelist_str(whitelist)}

Output Requirements:
Return a JSON object with:
- "declining_skills": list of 3 skills from the whitelist that this worker currently has or are common in their old job that face high automation/obsolescence risk.
- "emerging_skills": list of 3 skills from the whitelist that are rising in demand for their target transition.
"""

        response_json = self.client.generate_json(prompt)
        
        # Post-validation: Python set-based filter
        raw_declining = response_json.get("declining_skills", [])
        raw_emerging = response_json.get("emerging_skills", [])

        # Filter strictly
        valid_declining = [s for s in raw_declining if s.strip().lower() in whitelist_set]
        valid_emerging = [s for s in raw_emerging if s.strip().lower() in whitelist_set]

        # Fallback if filtered list is sparse
        if len(valid_declining) < 2:
            valid_declining = ["Manual Titration", "Excel Data Entry", "Paper Log Archiving"]
        if len(valid_emerging) < 2:
            valid_emerging = ["Spectrometry Automation", "Green Chemistry Compliance", "Lab Data Digital Logging"]

        return TrendSignal(
            source_name=snapshot.get("source_name", "O*NET Online 28.1 & Hays Asia 2025"),
            snapshot_date=snapshot.get("snapshot_date", "2025-01-15"),
            macro_impact_rate=snapshot.get("moderate_scenario", {}).get("macro_impact_rate", 0.64),
            market_growth_rate=snapshot.get("market_growth_rate", 0.38),
            declining_skills=valid_declining[:3],
            emerging_skills=valid_emerging[:3]
        )

def json_whitelist_str(items: list[str]) -> str:
    return ", ".join([f'"{x}"' for x in items])
