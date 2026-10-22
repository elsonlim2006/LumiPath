import os
import re
import json
import requests
from .data_loader import DataLoader

class GeminiClient:
    def __init__(self, timeout: float = 8.0):
        self.timeout = timeout
        self.api_key = self._load_api_key()
        self.model = "gemini-3.8-flash"
        self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"

    def _load_api_key(self) -> str:
        # Check env var first
        key = os.environ.get("GEMINI_API_KEY", "")
        if key:
            return key
        
        # Check code/.env
        env_candidates = [
            os.path.join(os.path.dirname(__file__), "..", "..", ".env"),
            os.path.join(os.getcwd(), "code", ".env"),
            os.path.join(os.getcwd(), ".env")
        ]
        for env_path in env_candidates:
            if os.path.exists(env_path):
                with open(env_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("GEMINI_API_KEY="):
                            return line.split("=", 1)[1].strip().strip('"').strip("'")
        return ""

    def clean_markdown_json(self, raw_text: str) -> str:
        text = raw_text.strip()
        # Remove markdown code fences
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.MULTILINE)
        text = re.sub(r"\s*```$", "", text, flags=re.MULTILINE)
        return text.strip()

    def generate_json(self, prompt: str) -> dict:
        if not self.api_key:
            print("[GeminiClient WARN] No GEMINI_API_KEY found, invoking offline fallback.")
            return DataLoader().get_fallback_cache()

        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "response_mime_type": "application/json",
                "temperature": 0.2
            }
        }
        url = f"{self.base_url}?key={self.api_key}"

        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=self.timeout)
            if resp.status_code != 200:
                print(f"[GeminiClient WARN] API responded with {resp.status_code}: {resp.text[:200]}")
                return DataLoader().get_fallback_cache()

            data = resp.json()
            candidates = data.get("candidates", [])
            if not candidates:
                return DataLoader().get_fallback_cache()

            parts = candidates[0].get("content", {}).get("parts", [])
            if not parts:
                return DataLoader().get_fallback_cache()

            raw_text = parts[0].get("text", "")
            cleaned = self.clean_markdown_json(raw_text)
            return json.loads(cleaned)

        except (requests.Timeout, requests.RequestException, json.JSONDecodeError, Exception) as e:
            print(f"[GeminiClient ERROR] Request/JSON error: {e}. Gracefully falling back.")
            return DataLoader().get_fallback_cache()
