"""SDC Hackathon 2026 - Profile Parser Service
Domain 1: Future-Ready Workforce
Extracts structured WorkerProfile from unstructured resume text/files with 8s timeout and fallback cache.
"""

import io
import json
import os
from typing import Optional, Tuple
import pypdf
import docx

from ..infra.data_loader import DataLoader
from ..infra.gemini_client import GeminiClient
from ..models.entities import WorkerProfile


class ProfileParserService:
    def __init__(self, timeout: float = 8.0):
        self.data_loader = DataLoader()
        self.gemini_client = GeminiClient(timeout=timeout)

    def extract_text_from_upload(self, file_bytes: bytes, filename: str) -> str:
        """Extract plain text from uploaded PDF, DOCX or TXT files."""
        ext = os.path.splitext(filename.lower())[1]
        try:
            if ext == ".pdf":
                reader = pypdf.PdfReader(io.BytesIO(file_bytes))
                pages_text = [page.extract_text() or "" for page in reader.pages]
                return "\n".join(pages_text).strip()
            elif ext == ".docx":
                doc = docx.Document(io.BytesIO(file_bytes))
                paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
                return "\n".join(paragraphs).strip()
            else:
                # Default assume UTF-8 plain text
                return file_bytes.decode("utf-8", errors="ignore").strip()
        except Exception as e:
            print(f"[ProfileParserService WARN] Error extracting text from {filename}: {e}")
            return ""

    def get_blank_worker(self) -> WorkerProfile:
        """Return an empty worker profile for manual user entry upon parsing failure."""
        return WorkerProfile(
            worker_id="WORKER-MANUAL",
            worker_name="",
            current_role="",
            experience_years=0.0,
            education_background="",
            target_domains=[],
            current_skills=[]
        )

    def parse_resume_text(self, raw_text: str) -> Tuple[WorkerProfile, bool]:
        """Parse resume plain text into WorkerProfile.
        Returns: (WorkerProfile, parse_error: bool)
        """
        cleaned_text = (raw_text or "").strip()
        if not cleaned_text:
            print("[ProfileParserService INFO] Empty text received, returning blank profile.")
            return self.get_blank_worker(), True

        truncated_text = cleaned_text[:4000]

        prompt = f"""You are an expert HR and workforce diagnostic AI assistant for SDC Hackathon 2026.
Extract structured profile information from the following resume text.

Input Resume:
\"\"\"
{truncated_text}
\"\"\"

Output MUST be a valid JSON object strictly matching this schema with NO markdown and NO commentary:
{{
  "worker_name": "Full Name string",
  "current_role": "Primary current job title or discipline",
  "experience_years": 2.0,
  "education_background": "Highest educational qualification and major",
  "target_domains": ["Area 1", "Area 2"],
  "current_skills": ["Skill 1", "Skill 2", "Skill 3"]
}}
"""
        try:
            res_json = self.gemini_client.generate_json(prompt)
            # If gemini returned the offline diagnosis fallback cache or malformed dict
            if "matched_roles" in res_json or "worker_name" not in res_json:
                raise ValueError("Gemini returned invalid or generic fallback instead of profile schema.")

            worker_name = str(res_json.get("worker_name", "")).strip()
            current_role = str(res_json.get("current_role", "")).strip()
            try:
                experience_years = float(res_json.get("experience_years", 0.0))
            except (ValueError, TypeError):
                experience_years = 0.0
            education_background = str(res_json.get("education_background", "")).strip()
            
            raw_targets = res_json.get("target_domains", [])
            target_domains = [str(t).strip() for t in raw_targets if str(t).strip()]

            raw_skills = res_json.get("current_skills", [])
            current_skills = [str(s).strip() for s in raw_skills if str(s).strip()]

            worker = WorkerProfile(
                worker_id="WORKER-EXTRACTED",
                worker_name=worker_name,
                current_role=current_role,
                experience_years=experience_years,
                education_background=education_background,
                target_domains=target_domains,
                current_skills=current_skills
            )
            return worker, False
        except Exception as e:
            print(f"[ProfileParserService WARN] Extraction failed or timed out: {e}. Activating blank manual profile.")
            return self.get_blank_worker(), True
