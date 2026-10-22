from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Skill:
    skill_name: str
    category: str = "Technical"

@dataclass
class CourseResource:
    course_name: str
    provider: str
    cost_type: str
    milestone_credential: str

@dataclass
class Phase:
    phase_number: int
    phase_name: str
    duration_weeks: int
    skills_addressed: List[str]
    recommended_resource: CourseResource
    milestone_credential: str

@dataclass
class ReskillingPathway:
    total_estimated_weeks: int
    phases: List[Phase]

@dataclass
class StandardRole:
    role_code: str
    role_title: str
    salary_range: str
    required_skills: List[str]
    primary_sdg: str = "SDG 8"
    secondary_sdg: Optional[str] = None
    malaysia_col_aligned: bool = False

@dataclass
class RoleMatch:
    rank: int
    role_code: str
    role_title: str
    match_score: float
    score_breakdown: str
    salary_range: str
    matched_skills: List[str]
    missing_skills: List[str]
    malaysia_col_aligned: bool = False

@dataclass
class TrendSignal:
    source_name: str
    snapshot_date: str
    macro_impact_rate: float
    market_growth_rate: float
    declining_skills: List[str]
    emerging_skills: List[str]

@dataclass
class WorkerProfile:
    worker_id: str
    worker_name: str
    current_role: str
    experience_years: float
    education_background: str
    target_domains: List[str]
    current_skills: List[str]
