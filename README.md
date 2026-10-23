# LumiPath - Future-Ready Workforce Navigator

> "We Will Light the Path to Your Future."  
> An AI-powered personalised career navigation and reskilling platform tailored for mid-career laboratory and chemical technicians undergoing digital and green industrial transformation in Malaysia.

---

## Team Information

| Field                  | Details                                     |
| ---------------------- | ------------------------------------------- |
| **Team Name**          | LumiPath Team                               |
| **Team Domain**        | Domain 1: Future-Ready Workforce            |
| **SDG Track (1–17)**   | SDG 8 (Target 8.2, 8.5), SDG 4 (Target 4.3, 4.4), SDG 13 (Target 13.3) |
| **Team Leader**        | Team Leader                                 |
| **University**         | University Name                             |
| **Number of Members**  | 3                                           |

## Links

| Resource          | Link                                           |
| ----------------- | ---------------------------------------------- |
| GitHub Repository | https://github.com/your-username/lumipath      |
| Replit Project    | https://replit.com/@your-username/lumipath     |
| Live Demo         | https://your-project.replit.app                |
| RunPod Endpoint   | https://api.runpod.ai/v2/your-endpoint-id      |
| Slide Deck        | `submission/SDC2026_TeamName_PitchDeck.pdf`    |
| Demo Video        | YouTube Link (5–7 min)                         |

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
| AI / LLM      | Google Gemini API (`gemini-1.5-flash`), Local Fallback Cache |
| GPU / Compute | RunPod Serverless GPU Endpoint (`runpod/handler.py`)         |
| Hosting / Dev | Replit Deployment Platform                                   |

---

## Project Structure

```
code/
├── .replit                  # Replit execution entry configuration (python app.py)
├── LICENSE                  # Apache License 2.0
├── README.md                # Project documentation and reproduction guide
├── requirements.txt         # Production dependencies (Flask, flask-cors, google-genai)
├── app.py                   # Main web application entry point
├── runpod/
│   └── handler.py           # RunPod serverless handler for GPU workloads
├── src/
│   ├── main.py              # CLI diagnostic probe
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
│   ├── 2. SDC Hackathon_ Technical Tools Declaration Template.pdf
│   ├── REPLIT PROOF OF USE.pdf
│   ├── RUNPOD PROOF OF USE.pdf
│   └── Submission Template SDC Hackathon.pdf
└── tests/
    ├── test_e2e.py          # End-to-end integration and API tests
    └── test_utils.py        # Utility tests
```

---

## How to Run

### Option 1 — Run on Replit (Recommended)

1. Import this repository into Replit via **Create Repl → Import from GitHub**.
2. Open the **Secrets** tab (🔒) and configure your environment variables:
   - `GEMINI_API_KEY` (Required for dynamic AI analysis; fallback heuristic runs automatically if absent)
   - `RUNPOD_API_KEY` (Optional / Conditional for GPU endpoint)
   - `RUNPOD_ENDPOINT_ID` (Optional / Conditional for GPU endpoint)
3. Click **Run**. Replit will execute `python app.py` and expose the web interface on the designated port.

### Option 2 — Run Locally

```bash
# 1. Clone the repository
git clone https://github.com/your-username/lumipath.git
cd lumipath

# 2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate       # Linux/macOS: source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Set environment variables
set GEMINI_API_KEY=your_key_here    # Linux/macOS: export GEMINI_API_KEY=your_key_here

# 5. Start the web application
python app.py
```
Open your browser and navigate to `http://127.0.0.1:8501`.

### Run Tests

Execute the full suite of end-to-end and domain validation tests:

```bash
python tests/test_e2e.py
```

---

## How We Use Replit *(Required)*

- **Development & Prototyping:** Rapid development and iterative testing of Flask web endpoints and responsive UI.
- **Hosting & Live Demo:** Production deployment via Replit Deployments providing a 24/7 public live prototype URL for judges.
- **Environment & Secrets:** Secure environment configuration with zero credential exposure.

📄 Proof of use: [`submission/REPLIT PROOF OF USE.pdf`](submission/REPLIT%20PROOF%20OF%20USE.pdf)

## How We Use RunPod *(Conditional for GPU)*

- **Workload:** High-performance model inference and batch embeddings handler via `runpod/handler.py`.
- **Architecture:** Serverless endpoint container supporting rapid GPU spin-up when complex neural embeddings or custom LLM fine-tuning is triggered.

📄 Proof of use: [`submission/RUNPOD PROOF OF USE.pdf`](submission/RUNPOD%20PROOF%20OF%20USE.pdf)

---

## License

This project is licensed under the [Apache License 2.0](LICENSE).
