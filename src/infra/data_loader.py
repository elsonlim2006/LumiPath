import json
import os

class DataLoader:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataLoader, cls).__new__(cls)
            cls._instance._base_dir = os.path.join(os.path.dirname(__file__), "..", "data")
            cls._instance._roles = None
            cls._instance._trend = None
            cls._instance._courses = None
            cls._instance._fallback = None
        return cls._instance

    def get_role_catalog(self) -> list[dict]:
        if self._roles is None:
            path = os.path.join(self._base_dir, "onet_roles.json")
            with open(path, "r", encoding="utf-8") as f:
                self._roles = json.load(f)
        return self._roles

    def get_trend_snapshot(self) -> dict:
        if self._trend is None:
            path = os.path.join(self._base_dir, "trend_snapshot.json")
            with open(path, "r", encoding="utf-8") as f:
                self._trend = json.load(f)
        return self._trend

    def get_course_catalog(self) -> list[dict]:
        if self._courses is None:
            path = os.path.join(self._base_dir, "course_catalog.json")
            with open(path, "r", encoding="utf-8") as f:
                self._courses = json.load(f)
        return self._courses

    def get_fallback_cache(self) -> dict:
        if self._fallback is None:
            path = os.path.join(self._base_dir, "fallback_cache.json")
            with open(path, "r", encoding="utf-8") as f:
                self._fallback = json.load(f)
        return self._fallback

    def get_sample_profiles(self) -> list[dict]:
        path = os.path.join(self._base_dir, "sample_profiles.json")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    @classmethod
    def get_all_skill_candidates(cls) -> list[str]:
        instance = cls()
        if not hasattr(instance, "_skill_candidates") or instance._skill_candidates is None:
            skills_set = set()
            for r in instance.get_role_catalog():
                for s in r.get("required_skills", []):
                    if s and s.strip():
                        skills_set.add(s.strip())
            for p in instance.get_sample_profiles():
                for s in p.get("current_skills", []):
                    if s and s.strip():
                        skills_set.add(s.strip())
            trend = instance.get_trend_snapshot()
            for s in trend.get("standard_skill_whitelist", []):
                if s and s.strip():
                    skills_set.add(s.strip())
            for s in trend.get("emerging_skills", []):
                if s and s.strip():
                    skills_set.add(s.strip())
            for s in trend.get("declining_skills", []):
                if s and s.strip():
                    skills_set.add(s.strip())
            instance._skill_candidates = sorted(list(skills_set))
        return instance._skill_candidates
