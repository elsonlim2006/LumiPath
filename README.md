# LumiPath - Future-Ready Workforce Navigator

> "We Will Light the Path to Your Future."  
> An AI-powered personalised career navigation and reskilling platform tailored for mid-career laboratory and chemical technicians undergoing digital and green industrial transformation in Malaysia.

---

## Team Information

| Field                  | Details                                     |
| ---------------------- | ------------------------------------------- |
| **Team Name**          | White Cloud                                 |
| **Team Domain**        | Domain 1: Future-Ready Workforce            |
| **SDG Track (1–17)**   | SDG 8 (Target 8.2, 8.5), SDG 4 (Target 4.3, 4.4), SDG 13 (Target 13.3) |
| **Team Leader**        | Elson Lim Zhong Qin                         |
| **University**         | Xiamen University Malaysia                  |
| **Number of Members**  | 3                                           |

## Links

| Resource          | Link                                           |
| ----------------- | ---------------------------------------------- |
| GitHub Repository | https://github.com/elsonlim2006/LumiPath       |
| Replit Project    | https://replit.com/@elsonlimzhongqi/LumiPath   |
| Live Demo         | https://lumipath.replit.app                    |
| RunPod Endpoint   | Standalone Serverless Handler (`runpod/handler.py`) |
| Slide Deck        | Included in Demo Video (`submission/LumiPath SDC Hackathon Presentation.pptx`) |
| Demo Video        | https://youtu.be/VyJyOq9TzOI                   |

---

## Overview

### Problem

Industrial automation, automated chemical analyzers, and green transitions are rapidly displacing conventional manual laboratory testing and routine sampling roles (e.g. Chemical Technicians, QC Analysts). Workers in Malaysia face high replacement pressure, skill opacity, and uncertainty without clear, structured reskilling pathways backed by local certifications and funding.

### Solution

LumiPath ingests technician profiles, references authoritative industry and labor market benchmarks (Hays Asia 2025, O*NET 28.1, TalentCorp Critical Occupations List, DOSM Q2 2026), and computes realistic career transitions into high-demand roles. It provides transparent skill gap breakdowns, dual-scenario impact timelines, and localized, actionable 3-phase reskilling roadmaps linked to HRD Corp claimable courses.

### Key Features

- **Skill Profile Intake & Parsing**: Supports direct resume upload (PDF/TXT/DOCX) or curated sample profiles, with interactive chip editing for skills and experience.
- **AI Trend Signal Layer**: Grounded macro trend signals displaying source authority and snapshot date (`Hays Asia 2025 & O*NET 28.1, Snapshot: 2025-01-15`).
- **Future-Role Matching**: Quantitative suitability scoring based on skill overlap ($0.7$) and work tenure ($0.3$), outputting Top 3 recommended career trajectories.
- **Personalised 3-Phase Reskilling Roadmap**: Chronological learning stages (Foundation $\to$ Core Certification $\to$ Practical Capstone) highlighting free audits and HRD Corp SBL-KHAS claimable courses.
- **Dual-Scenario Uncertainty Handling**: Toggle between *Moderate Transition* (8-week timeline) and *Fast Disruption* (4-week accelerated timeline) with dynamic automation risk adjustments.
- **SDG Impact Mapping**: Explicit alignment to UN SDG 4, SDG 8, and context-aware SDG 13 targets with measurable workforce transition metrics.

### Tech Stack

| Layer         | Technology                                                   |
| ------------- | ------------------------------------------------------------ |
| Frontend      | HTML5, CSS3, Vanilla JavaScript (Single-Page Responsive UI)  |
| Backend       | Python 3.10+, Flask, Flask-CORS                              |
| AI / LLM      | Google Gemini API (`gemini-flash-lite-latest`), Local Fallback Cache |
| GPU / Compute | RunPod Serverless Endpoint (`runpod/handler.py`)             |
| Hosting / Dev | Replit Deployment Platform                                   |

---

## Project Structure

```
.
├── .env.example             # Example environment variables template
├── .gitignore               # Ignored files (.env, __pycache__)
├── .replit                  # Replit deployment configuration (python app.py)
├── LICENSE                  # Apache License 2.0
├── README.md                # Project documentation and submission guide
├── requirements.txt         # Production dependencies
├── app.py                   # Main interactive web application entry point
├── runpod/
│   └── handler.py           # RunPod serverless handler for decoupled workloads
├── src/
│   ├── main.py              # CLI diagnostic verification probe
│   ├── utils.py             # Utility helpers
│   ├── data/                # Authoritative reference datasets & sample profiles
│   │   ├── course_catalog.json
│   │   ├── fallback_cache.json
│   │   ├── onet_roles.json
│   │   ├── sample_profiles.json
│   │   └── trend_snapshot.json
│   ├── infra/               # Data loader and LLM client
│   │   ├── data_loader.py
│   │   └── gemini_client.py
│   ├── models/              # Domain entities and data models
│   │   └── entities.py
│   └── services/            # Core business and orchestration logic
│       ├── matcher_service.py
│       ├── orchestrator.py
│       ├── pathway_service.py
│       └── profile_service.py
├── submission/              # Official competition submission documents
│   ├── LumiPath SDC Hackathon Presentation.pptx
│   ├── SDC2026_White Cloud_Preliminary.pdf
│   ├── SDC2026_White Cloud_Replit_POU.pdf
│   ├── SDC2026_White Cloud_Runpod_POU.pdf
│   └── SDC2026_White Cloud_TechDeclaration.pdf
└── tests/
    ├── test_e2e.py          # End-to-end integration and API test suite
    └── test_utils.py        # Utility unit tests
```

### Architecture

```
User ──► Replit (Web UI / Flask API) ──► Google Gemini API (gemini-flash-lite-latest)
                │                                    │
                ├────────────────────────────────────┘ (Heuristic Fallback Cache)
                ▼
        RunPod Endpoint (Serverless Handler: runpod/handler.py)
```

---

## How to Run

### Option 1 — Run on Replit (Recommended)

1. Open the [Replit Project](https://replit.com/@elsonlimzhongqi/LumiPath), or import this repository via **Create Repl → Import from GitHub**.
2. Open the **Secrets** tab (🔒) and add the environment variables listed in `.env.example`:
   - `GEMINI_API_KEY` (Required for dynamic AI analysis; deterministic fallback runs automatically if absent)
   - `RUNPOD_API_KEY` (Optional / For RunPod serverless testing)
   - `RUNPOD_ENDPOINT_ID` (Optional / For RunPod serverless testing)
3. Click **Run**. Replit will execute `python app.py` and serve the web application.

### Option 2 — Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/elsonlim2006/LumiPath.git
cd LumiPath

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate       # Linux/macOS: source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables (optional)
cp .env.example .env        # then fill in your values

# 5. Run the web application
python app.py
```
Open your browser and navigate to `http://127.0.0.1:8501`.

### Run Tests

Run the complete test suite via standard unittest discovery:

```bash
python -m unittest discover tests
```

---

## How We Use Replit *(Required)*

- **Development & Prototyping:** Rapid development, environment configuration, and iterative testing of the single-page application and backend endpoints.
- **Hosting & Live Demo:** Production deployment via Replit Autoscale Deployments providing a resilient 24/7 public live prototype URL: https://lumipath.replit.app
- **Secrets Management:** Sensitive keys and runtime configurations are securely isolated via Replit Secrets.

📄 Proof of use: [`submission/SDC2026_White Cloud_Replit_POU.pdf`](submission/SDC2026_White%20Cloud_Replit_POU.pdf)

## How We Use RunPod *(Required)*

- **Workload:** Serverless execution handler via `runpod/handler.py` for decoupled background diagnostic processing and inference tasks.
- **Setup:** Configured as a RunPod Serverless Endpoint container using standard payload specifications.
- **Integration:** The backend architecture supports routing batch profile evaluations to RunPod endpoints via authenticated API calls.

Example request:

```bash
curl -X POST https://api.runpod.ai/v2/$RUNPOD_ENDPOINT_ID/runsync \
  -H "Authorization: Bearer $RUNPOD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"worker_name": "Alex Tan", "current_role": "Chemical Laboratory Technician", "experience_years": 3.5, "current_skills": ["Manual Titration", "Excel Data Entry"]}}'
```

📄 Proof of use: [`submission/SDC2026_White Cloud_Runpod_POU.pdf`](submission/SDC2026_White%20Cloud_Runpod_POU.pdf)

---

## Challenges & Learnings

- **Data Grounding vs LLM Hallucination:** Balancing open-ended LLM recommendations with strict local vocational realities was addressed by anchoring AI prompts to a deterministic skill whitelist and regional occupational databases (TalentCorp COL, O*NET).
- **Graceful Fallback Engineering:** Ensured complete system resilience by designing a robust dual-layer offline fallback cache, guaranteeing zero UI crashes even when external AI API calls experience network latency or quota limits.
- **Local Industry Alignment:** Mapping reskilling pathways directly to Malaysia HRD Corp claimable frameworks (SBL-KHAS) provided actionable value beyond generic course suggestions.

## Future Improvements

- [ ] Integration with Malaysia National Employment Portal (MYFutureJobs) for real-time job vacancy matching.
- [ ] Direct credential verification and badge issuing via blockchain or institutional micro-credentials.
- [ ] Expansion of localized benchmark datasets across additional manufacturing and electronics sub-sectors.

## Team

| Name                 | Role                        | GitHub                                          |
| -------------------- | --------------------------- | ----------------------------------------------- |
| Elson Lim Zhong Qin  | Team Lead / Backend & AI    | [@elsonlim2006](https://github.com/elsonlim2006)|
| Tan Ping Yang        | Frontend & UI/UX            | N/A                                             |
| Choo Zi Yun          | Research & Domain Alignment | N/A                                             |

---

## Submission Checklist

- [x] Team name, domain (Domain 1: Future-Ready Workforce) and SDG track filled in
- [x] Slide deck included in repository (`submission/`) and demo video
- [x] Demo video link added (YouTube)
- [x] Replit used, with proof of use in `submission/`
- [x] RunPod used, with proof of use in `submission/`
- [x] Submission templates completed in `submission/`
- [x] "How to Run" steps verified
- [x] No API keys or secrets committed to the repository

## License

This project is licensed under the [Apache License 2.0](LICENSE).
