from ..infra.data_loader import DataLoader
from ..models.entities import WorkerProfile, RoleMatch

class RoleMatcherService:
    def __init__(self):
        self.data_loader = DataLoader()

    def match_top_roles(self, worker: WorkerProfile) -> list[RoleMatch]:
        raw_roles = self.data_loader.get_role_catalog()
        worker_skills_set = set(s.strip().lower() for s in worker.current_skills)
        exp_factor = min(1.0, max(0.0, worker.experience_years / 5.0))
        
        matches = []
        for role in raw_roles:
            req_skills = role.get("required_skills", [])
            total_req = len(req_skills) if req_skills else 1
            
            matched = [s for s in req_skills if s.strip().lower() in worker_skills_set]
            missing = [s for s in req_skills if s.strip().lower() not in worker_skills_set]
            
            skill_overlap_ratio = len(matched) / total_req
            score = round(0.7 * skill_overlap_ratio + 0.3 * exp_factor, 2)
            
            skill_pct = int(skill_overlap_ratio * 70)
            exp_pct = int(exp_factor * 30)
            breakdown = f"Matched {len(matched)} of {total_req} required skills ({skill_pct}%), combined with {worker.experience_years} years experience ({exp_pct}%), resulting in an overall match score of {int(score * 100)}%"
            
            matches.append({
                "role_code": role.get("role_code", ""),
                "role_title": role.get("role_title", ""),
                "salary_range": role.get("salary_range", ""),
                "match_score": score,
                "score_breakdown": breakdown,
                "matched_skills": matched,
                "missing_skills": missing,
                "malaysia_col_aligned": role.get("malaysia_col_aligned", False)
            })
            
        # Sort descending by match_score
        matches.sort(key=lambda x: x["match_score"], reverse=True)
        top_3 = matches[:3]
        
        results = []
        for i, m in enumerate(top_3):
            results.append(RoleMatch(
                rank=i + 1,
                role_code=m["role_code"],
                role_title=m["role_title"],
                match_score=m["match_score"],
                score_breakdown=m["score_breakdown"],
                salary_range=m["salary_range"],
                matched_skills=m["matched_skills"],
                missing_skills=m["missing_skills"],
                malaysia_col_aligned=m["malaysia_col_aligned"]
            ))
        return results
