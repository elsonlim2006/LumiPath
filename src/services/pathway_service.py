from ..infra.data_loader import DataLoader
from ..models.entities import RoleMatch, ReskillingPathway, Phase, CourseResource

class PathwayPlannerService:
    def __init__(self):
        self.data_loader = DataLoader()

    def plan_pathway(self, match: RoleMatch, pace: str = "moderate") -> ReskillingPathway:
        catalog = self.data_loader.get_course_catalog()
        missing = match.missing_skills if match and match.missing_skills else ["Spectrometry Automation", "Green Chemistry Compliance"]
        
        # Partition missing skills across 3 phases
        phase1_skills = [missing[0]] if len(missing) >= 1 else ["Lab Data Digital Logging"]
        phase2_skills = [missing[1]] if len(missing) >= 2 else (phase1_skills if len(missing) == 1 else ["Spectrometry Automation"])
        phase3_skills = missing[2:] if len(missing) >= 3 else ["Green Chemistry Compliance"]

        if pace == "accelerated":
            weeks = [2, 3, 3]  # 8 weeks sprint
        else:
            weeks = [4, 6, 4]  # 14 weeks steady

        phases = [
            self._build_phase(1, "Phase 1: Foundation & Digital Baseline", weeks[0], phase1_skills, catalog),
            self._build_phase(2, "Phase 2: Applied Instrumental & Process Skills", weeks[1], phase2_skills, catalog),
            self._build_phase(3, "Phase 3: Industry Certification & Micro-credential", weeks[2], phase3_skills, catalog)
        ]

        total_weeks = sum(p.duration_weeks for p in phases)
        return ReskillingPathway(
            total_estimated_weeks=total_weeks,
            phases=phases
        )

    def _build_phase(self, num: int, name: str, weeks: int, skills: list[str], catalog: list[dict]) -> Phase:
        # Match a course from catalog based on skills
        matched_course = None
        for skill in skills:
            for item in catalog:
                if item.get("skill_keyword", "").lower() == skill.lower():
                    matched_course = item
                    break
            if matched_course:
                break
        
        if not matched_course:
            matched_course = catalog[min(num - 1, len(catalog) - 1)]

        course_obj = CourseResource(
            course_name=matched_course.get("course_name", "Industrial Reskilling Course"),
            provider=matched_course.get("provider", "Coursera / edX"),
            cost_type=matched_course.get("cost_type", "Free Audit"),
            milestone_credential=matched_course.get("milestone_credential", "Certificate of Completion")
        )

        return Phase(
            phase_number=num,
            phase_name=name,
            duration_weeks=weeks,
            skills_addressed=skills,
            recommended_resource=course_obj,
            milestone_credential=course_obj.milestone_credential
        )
