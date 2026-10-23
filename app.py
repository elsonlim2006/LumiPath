"""LumiPath - Native HTML/CSS/JS + Flask Web Application
SDC Hackathon 2026 | Domain 1: Future-Ready Workforce
"We Will Light the Path to Your Future."
"""

import base64
import json
import os
import sys
from flask import Flask, jsonify, render_template_string, request
from flask_cors import CORS

# Ensure project root is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from src.infra.data_loader import DataLoader
from src.models.entities import WorkerProfile
from src.services.orchestrator import WorkflowOrchestrator
from src.services.profile_service import ProfileParserService

app = Flask(__name__)
CORS(app)

def get_base64_logo() -> str:
    logo_path = os.path.join(current_dir, "src", "data", "lantern_logo.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    return ""

LOGO_B64 = get_base64_logo()

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>LumiPath - Future-Ready Workforce Navigator</title>
  {% if logo_b64 %}<link rel="icon" type="image/png" href="data:image/png;base64,{{ logo_b64 }}">{% else %}{% if logo_b64 %}<link rel="icon" type="image/png" href="data:image/png;base64,{{ logo_b64 }}">{% else %}<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🔦</text></svg>">{% endif %}{% endif %}
  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    body {
      background-color: #090E17;
      color: #CBD5E1;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    /* Clean no-scrollbar experience while keeping full wheel scrolling */
    html, body {
      scrollbar-width: none;
      -ms-overflow-style: none;
    }
    html::-webkit-scrollbar, body::-webkit-scrollbar {
      display: none;
    }

    /* Top Navigation Bar */
    .top-nav {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 16px 40px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      position: relative;
    }

    .nav-brand {
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
    }

    .nav-brand img {
      height: 42px;
      width: auto;
      filter: drop-shadow(0 0 10px rgba(250, 204, 21, 0.45));
    }

    .brand-name {
      font-size: 1.75rem;
      font-weight: 800;
      color: #FACC15;
      letter-spacing: -0.5px;
      text-shadow: 0 0 14px rgba(250, 204, 21, 0.5);
    }

    .nav-slogan {
      position: absolute;
      left: 50%;
      transform: translateX(-50%);
      font-size: 1.2rem;
      font-weight: 600;
      color: #FEF08A;
      letter-spacing: 0.3px;
      text-shadow: 0 0 14px rgba(250, 204, 21, 0.35);
      white-space: nowrap;
      transition: opacity 0.2s ease;
    }

    .nav-right {
      min-width: 100px;
      text-align: right;
    }

    .btn-reset-link {
      background: transparent;
      border: none;
      color: #64748B;
      font-size: 0.88rem;
      font-weight: 500;
      cursor: pointer;
      display: none;
      transition: color 0.2s;
    }

    .btn-reset-link:hover {
      color: #F8FAFC;
      text-decoration: underline;
    }

    /* Main Content Wrapper */
    .main-container {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      padding: 24px 20px 40px 20px;
      max-width: 1140px;
      width: 100%;
      margin: 0 auto;
    }

    /* STEP 1: PURE BIG UNIFIED BOX */
    .dmt-big-box {
      width: 100%;
      max-width: 760px;
      min-height: 360px;
      background-color: #111827;
      border: 1px solid rgba(250, 204, 21, 0.35);
      border-radius: 16px;
      display: flex;
      justify-content: center;
      align-items: center;
      padding: 40px 24px;
      transition: border-color 0.2s;
      box-shadow: 0 18px 40px rgba(0, 0, 0, 0.5);
    }

    .dmt-big-box.dragover {
      border-color: #FACC15;
      background-color: #131E33;
    }

    .dmt-ops-group {
      display: flex;
      align-items: center;
      gap: 16px;
    }

    .btn-upload-pill {
      background-color: #0B0F17;
      border: 2px solid rgba(250, 204, 21, 0.6);
      border-radius: 14px;
      padding: 18px 36px;
      color: #F8FAFC;
      font-size: 1.35rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      min-width: 290px;
      transition: all 0.2s ease;
      user-select: none;
    }

    .btn-upload-pill:hover {
      border-color: #FACC15;
      background-color: #111827;
      transform: translateY(-1px);
    }

    .btn-upload-pill.selected {
      border-color: #10B981;
      color: #10B981;
    }

    .btn-submit-arrow {
      background-color: #0B0F17;
      border: 2px solid rgba(250, 204, 21, 0.6);
      border-radius: 14px;
      width: 72px;
      height: 72px;
      color: #F8FAFC;
      font-size: 2.2rem;
      font-weight: 800;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s ease;
      user-select: none;
    }

    .btn-submit-arrow:hover {
      background-color: #FACC15;
      color: #090E17;
      border-color: #FACC15;
      transform: translateY(-1px);
    }

    #file-input {
      display: none;
    }

    /* STEP 2: VERIFICATION PANEL (Matte & Clean) */
    .step-card {
      width: 100%;
      max-width: 860px;
      background-color: #111827;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 14px;
      padding: 32px 36px;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.5);
    }

    .form-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 20px;
      margin-bottom: 20px;
    }

    .form-group {
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .form-group label {
      font-size: 0.85rem;
      font-weight: 600;
      color: #94A3B8;
    }

    .form-control {
      background-color: #0B0F17;
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 8px;
      padding: 10px 14px;
      color: #F8FAFC;
      font-size: 0.95rem;
      outline: none;
      transition: border-color 0.2s;
    }

    .form-control:focus {
      border-color: #FACC15;
    }

    /* Modern Mainstream Inline Tag Input */
    .inline-tag-wrapper {
      position: relative;
    }

    .inline-tag-box {
      background-color: #0B0F17;
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 8px;
      padding: 8px 12px;
      min-height: 50px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 8px;
      cursor: text;
      transition: border-color 0.2s;
    }

    .inline-tag-box:focus-within {
      border-color: #FACC15;
    }

    .skill-tag {
      background-color: rgba(250, 204, 21, 0.12);
      border: 1px solid #FACC15;
      color: #FDE047;
      padding: 4px 10px;
      border-radius: 16px;
      font-size: 0.85rem;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      user-select: none;
    }

    .skill-tag-remove {
      cursor: pointer;
      font-weight: bold;
      color: #FACC15;
      font-size: 1rem;
      line-height: 1;
      padding-left: 2px;
    }

    .skill-tag-remove:hover {
      color: #EF4444;
    }

    .inline-tag-input {
      background: transparent;
      border: none;
      outline: none;
      color: #F8FAFC;
      font-size: 0.95rem;
      min-width: 140px;
      flex: 1;
      padding: 4px 6px;
    }

    .inline-tag-input::placeholder {
      color: #64748B;
      font-size: 0.88rem;
    }

    .typeahead-dropdown {
      position: absolute;
      top: calc(100% + 4px);
      left: 0;
      right: 0;
      background: #0B0F17;
      border: 1px solid #FACC15;
      border-radius: 8px;
      max-height: 200px;
      overflow-y: auto;
      z-index: 50;
      display: none;
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.8);
    }

    .typeahead-item {
      padding: 9px 16px;
      cursor: pointer;
      font-size: 0.9rem;
      color: #CBD5E1;
      transition: background-color 0.15s;
    }

    .typeahead-item:hover {
      background-color: rgba(250, 204, 21, 0.18);
      color: #FDE047;
    }

    .btn-primary {
      background-color: #FACC15;
      color: #090E17;
      font-weight: 700;
      border: none;
      border-radius: 8px;
      padding: 12px 28px;
      font-size: 1rem;
      cursor: pointer;
      transition: background-color 0.2s, transform 0.2s;
    }

    .btn-primary:hover {
      background-color: #FDE047;
      transform: translateY(-1px);
    }

    /* STEP 3: DUAL-TRACK SCENARIO SELECTOR & TOP 3 ROLES */
    .summary-bar {
      width: 100%;
      background-color: #111827;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 8px;
      padding: 12px 20px;
      margin-bottom: 18px;
      font-size: 0.92rem;
      color: #CBD5E1;
    }

    /* Scenario Toggle Strip */
    .scenario-strip {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      width: 100%;
      margin-bottom: 22px;
    }

    .scenario-pill {
      background-color: #111827;
      border: 2px solid rgba(255, 255, 255, 0.08);
      border-radius: 12px;
      padding: 14px 18px;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      flex-direction: column;
      gap: 5px;
      user-select: none;
    }

    .scenario-pill:hover {
      border-color: rgba(250, 204, 21, 0.35);
    }

    .scenario-pill.active {
      border-color: #FACC15 !important;
      background-color: rgba(250, 204, 21, 0.08);
      box-shadow: 0 0 16px rgba(250, 204, 21, 0.2);
    }

    .scenario-pill-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .scenario-pill-title {
      font-size: 1rem;
      font-weight: 700;
    }

    .scenario-pill-badge {
      font-size: 0.75rem;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 4px;
    }

    .scenario-pill-meta {
      font-size: 0.82rem;
      color: #94A3B8;
    }

    /* Top 3 Roles Horizontal Grid (1 Row 3 Columns) */
    .top3-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 18px;
      width: 100%;
      margin-bottom: 22px;
    }

    .role-card {
      background-color: #111827;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 12px;
      padding: 20px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: border-color 0.2s, transform 0.2s;
    }

    .role-card:hover {
      border-color: rgba(250, 204, 21, 0.5);
      transform: translateY(-2px);
    }

    .role-rank-badge {
      font-size: 0.72rem;
      font-weight: 700;
      color: #FACC15;
      background: rgba(250, 204, 21, 0.12);
      border: 1px solid rgba(250, 204, 21, 0.3);
      padding: 2px 7px;
      border-radius: 4px;
      display: inline-block;
      margin-bottom: 8px;
    }

    .role-title {
      font-size: 1.08rem;
      font-weight: 700;
      color: #F8FAFC;
      margin-bottom: 6px;
      line-height: 1.3;
      min-height: 42px;
    }

    .role-score-salary {
      font-size: 0.86rem;
      font-weight: 600;
      color: #FACC15;
      margin-bottom: 8px;
    }

    .role-col-badge {
      font-size: 0.78rem;
      color: #94A3B8;
      margin-bottom: 14px;
    }

    .role-skill-summary {
      font-size: 0.8rem;
      color: #94A3B8;
      background: #0B0F17;
      padding: 8px 10px;
      border-radius: 6px;
      margin-bottom: 16px;
    }

    .btn-view-pathway {
      background-color: #1F2937;
      color: #F8FAFC;
      border: 1px solid #FACC15;
      font-weight: 600;
      border-radius: 8px;
      padding: 10px 16px;
      font-size: 0.9rem;
      cursor: pointer;
      width: 100%;
      transition: background-color 0.2s;
      text-align: center;
    }

    .btn-view-pathway:hover {
      background-color: #374151;
    }

    .trends-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      width: 100%;
      margin-top: 8px;
    }

    .trend-box {
      background-color: #111827;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 8px;
      padding: 14px 18px;
    }

    /* STEP 4: DEEP DIVE PATHWAY */
    .deep-dive-grid {
      display: grid;
      grid-template-columns: 1fr 2fr;
      gap: 24px;
      width: 100%;
    }

    .phase-item {
      background: #0B0F17;
      border-left: 3px solid #FACC15;
      padding: 16px 20px;
      border-radius: 8px;
      margin-bottom: 14px;
      border-top: 1px solid rgba(255, 255, 255, 0.05);
      border-right: 1px solid rgba(255, 255, 255, 0.05);
      border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }

    .expander-box {
      background: #0B0F17;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 8px;
      padding: 12px 16px;
      margin-top: 14px;
      font-size: 0.85rem;
    }

    .expander-header {
      cursor: pointer;
      color: #FACC15;
      font-weight: 600;
      display: flex;
      justify-content: space-between;
    }

    .expander-content {
      display: none;
      margin-top: 10px;
      color: #94A3B8;
      line-height: 1.5;
    }

    .spinner {
      display: none;
      border: 3px solid rgba(250, 204, 21, 0.15);
      border-top: 3px solid #FACC15;
      border-radius: 50%;
      width: 36px;
      height: 36px;
      animation: spin 0.8s linear infinite;
      margin: 20px auto;
    }

    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
  </style>
</head>
<body>

  <!-- Top Navigation Bar -->
  <header class="top-nav">
    <a href="#" class="nav-brand" onclick="goToStep(1)">
      {% if logo_b64 %}
      <img src="data:image/png;base64,{{ logo_b64 }}" alt="LumiPath">
      {% else %}
      <span style="font-size: 2rem;">🔦</span>
      {% endif %}
      <span class="brand-name">LumiPath</span>
    </a>
    <div class="nav-slogan" id="nav-slogan">"We Will Light the Path to Your Future."</div>
  </header>

  <!-- Main Container -->
  <main class="main-container">

    <!-- Loading Spinner -->
    <div id="loading-spinner" class="spinner"></div>

    <!-- STEP 1: Upload Box -->
    <section id="step-1" class="dmt-big-box">
      <div class="dmt-ops-group">
        <input type="file" id="file-input" accept=".pdf,.txt,.docx">
        <div class="btn-upload-pill" id="btn-upload-pill" onclick="document.getElementById('file-input').click()">
          Upload CV File Here
        </div>
        <div class="btn-submit-arrow" id="btn-submit-arrow" onclick="handleFileSubmit()" title="Click to parse resume">
          ⬆
        </div>
      </div>
    </section>

    <!-- STEP 2: Verification Panel (Zero Redundant Headers) -->
    <section id="step-2" class="step-card" style="display: none;">
      <div id="parse-error-banner" style="display: none; background: rgba(239, 68, 68, 0.15); border: 1px solid #EF4444; color: #FCA5A5; padding: 12px 18px; border-radius: 8px; margin-bottom: 20px; font-size: 0.92rem;">
        ⚠️ AI auto-parsing could not extract all details. Please review and fill in your profile manually below.
      </div>
      <div class="form-grid">
        <div class="form-group">
          <label>Full Name</label>
          <input type="text" id="input-worker-name" class="form-control">
        </div>
        <div class="form-group">
          <label>Current Role</label>
          <input type="text" id="input-current-role" class="form-control">
        </div>
        <div class="form-group">
          <label>Experience (Years)</label>
          <input type="number" id="input-experience-years" class="form-control" step="0.5" min="0" max="40">
        </div>
        <div class="form-group">
          <label>Education Background</label>
          <input type="text" id="input-education-bg" class="form-control">
        </div>
      </div>

      <div class="form-group" style="margin-bottom: 20px;">
        <label>Target Domain</label>
        <input type="text" id="input-target-domains" class="form-control" placeholder="Chemical Quality Control, Laboratory Analytical Operations">
      </div>

      <!-- Mainstream Inline Tag Input -->
      <div class="form-group">
        <label>Current Skills</label>
        <div class="inline-tag-wrapper">
          <div class="inline-tag-box" id="inline-tag-box" onclick="focusSkillInput()">
            <div id="skills-tags-list" style="display: contents;"></div>
            <input type="text" id="input-skill-inline" class="inline-tag-input" placeholder="+ Add a skill...">
          </div>
          <div class="typeahead-dropdown" id="typeahead-dropdown"></div>
        </div>
      </div>

      <div style="display: flex; justify-content: flex-end; margin-top: 28px;">
        <button class="btn-primary" onclick="confirmProfileAndDiagnose()">Confirm Profile →</button>
      </div>
    </section>

    <!-- STEP 3: Dual-Track Scenarios & TOP 3 Career Matrix (OECD Benchmark) -->
    <section id="step-3" style="display: none; width: 100%;">
      <div class="summary-bar" id="step3-summary-bar"></div>

      <!-- Dual Scenario Toggle Strip -->
      <div class="scenario-strip">
        <div class="scenario-pill active" id="scenario-pill-moderate" onclick="switchScenario('moderate')">
          <div class="scenario-pill-header">
            <span class="scenario-pill-title" style="color: #F8FAFC;">🌿 Moderate Disruption</span>
            <span class="scenario-pill-badge" style="background: rgba(250,204,21,0.15); color: #FACC15;">14-Week Steady Pace</span>
          </div>
          <div class="scenario-pill-meta">3-5 Yr Horizon · 42% Automation Impact · In-Sector Chemical Quality Deepening</div>
        </div>

        <div class="scenario-pill" id="scenario-pill-accelerated" onclick="switchScenario('accelerated')">
          <div class="scenario-pill-header">
            <span class="scenario-pill-title" style="color: #F8FAFC;">⚡ Fast Disruption</span>
            <span class="scenario-pill-badge" style="background: rgba(250,204,21,0.15); color: #FACC15;">8-Week Sprint Pace</span>
          </div>
          <div class="scenario-pill-meta">1-2 Yr Horizon · 74% Lab Workflow Automation · Cross-Sector Clean Energy Pivot</div>
        </div>
      </div>

      <!-- Top 3 Career Roles Grid (Dynamic) -->
      <div class="top3-grid" id="top3-roles-container"></div>

      <!-- Macro Trend Radar (Dynamic) -->
      <div id="radar-header-container"></div>
      <div class="trends-grid" id="trends-container"></div>
      <p id="step3-disclaimer" style="font-size: 0.75rem; color: #64748B; text-align: center; margin-top: 24px;"></p>
    </section>

    <!-- STEP 4: Deep Dive Pathway (Focused & Clean) -->
    <section id="step-4" style="display: none; width: 100%;">
      <button class="btn-reset-link" style="display: inline-block; margin-bottom: 16px;" onclick="goToStep(3)">← Back to Career Pathways</button>

      <div style="margin-bottom: 18px;">
        <h2 style="font-size: 1.55rem; color: #F8FAFC; margin-bottom: 4px;" id="step4-role-title">Quality Control Analyst</h2>
        <p style="font-size: 0.88rem; color: #FACC15; font-weight: 600;" id="step4-pace-subtitle">14-Week Steady Transition</p>
      </div>

      <div class="deep-dive-grid">
        <!-- Left: Gap Pool & SDGs -->
        <div style="background: #111827; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 20px;">
          <h4 style="color: #F8FAFC; margin-bottom: 12px; font-size: 0.95rem;">Skills Breakdown</h4>
          <p style="font-size: 0.82rem; font-weight: 600; color: #94A3B8; margin-bottom: 6px;">Matched Skills</p>
          <div id="step4-matched-skills" style="margin-bottom: 14px;"></div>

          <p style="font-size: 0.82rem; font-weight: 600; color: #94A3B8; margin-bottom: 6px;">Skills to Acquire</p>
          <div id="step4-missing-skills" style="margin-bottom: 20px;"></div>

          <hr style="border: none; border-top: 1px solid rgba(255, 255, 255, 0.08); margin-bottom: 16px;">

          <h4 style="color: #F8FAFC; margin-bottom: 10px; font-size: 0.95rem;">UN SDG Alignment</h4>
          <div id="step4-sdgs-container"></div>

          <!-- Official UN Target Compliance Details Expander -->
          <div class="expander-box">
            <div class="expander-header" onclick="toggleExpander()">
              <span>Resolution Target Details</span>
              <span id="expander-arrow">▼</span>
            </div>
            <div class="expander-content" id="expander-content">
              <p><b>UN 2030 Agenda Targets:</b></p>
              <ul style="padding-left: 18px; margin-top: 6px;">
                <li><b>Target 4.3</b>: Equal access to affordable technical & vocational education.</li>
                <li><b>Target 4.4</b>: Substantially increase skills for employment and entrepreneurship.</li>
                <li><b>Target 8.2</b>: Achieve economic productivity through technological upgrading.</li>
                <li><b>Target 8.5</b>: Full and productive employment and decent work for all.</li>
                <li><b>Target 13.3</b>: Education and institutional capacity on climate change mitigation.</li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Right: 3-Phase Timeline -->
        <div style="background: #111827; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 14px; padding: 24px;">
          <h4 style="color: #F8FAFC; margin-bottom: 18px; font-size: 1rem;" id="step4-timeline-header">Transition Roadmap</h4>
          <div id="step4-phases-container"></div>
        </div>
      </div>


    </section>

  </main>

  <script>
    let currentStep = 1;
    let selectedFile = null;
    let workerProfile = null;
    let diagnosisResult = null;
    let activeScenario = 'moderate'; // 'moderate' or 'accelerated'
    let allSkillCandidates = [];

    fetch('/api/skills')
      .then(res => res.json())
      .then(data => { allSkillCandidates = data; })
      .catch(err => console.error(err));

    const dmtBox = document.getElementById('step-1');
    const fileInput = document.getElementById('file-input');
    const uploadPill = document.getElementById('btn-upload-pill');

    ['dragenter', 'dragover'].forEach(eventName => {
      dmtBox.addEventListener(eventName, (e) => {
        e.preventDefault();
        dmtBox.classList.add('dragover');
      }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
      dmtBox.addEventListener(eventName, (e) => {
        e.preventDefault();
        dmtBox.classList.remove('dragover');
      }, false);
    });

    dmtBox.addEventListener('drop', (e) => {
      e.preventDefault();
      dmtBox.classList.remove('dragover');
      if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
        setFile(e.dataTransfer.files[0]);
      }
    });

    fileInput.addEventListener('change', (e) => {
      if (e.target.files && e.target.files.length > 0) {
        setFile(e.target.files[0]);
      }
    });

    function setFile(file) {
      selectedFile = file;
      uploadPill.innerText = `Selected: ${file.name}`;
      uploadPill.classList.add('selected');
    }

    function handleFileSubmit() {
      if (!selectedFile) {
        alert('Please select a CV file first before submitting.');
        return;
      }

      const formData = new FormData();
      formData.append('resume', selectedFile);

      showSpinner(true);
      fetch('/api/upload-resume', {
        method: 'POST',
        body: formData
      })
      .then(res => res.json())
      .then(data => {
        showSpinner(false);
        const banner = document.getElementById('parse-error-banner');
        if (data.parse_error) {
          if (banner) banner.style.display = 'block';
        } else {
          if (banner) banner.style.display = 'none';
        }

        if (data.worker) {
          workerProfile = data.worker;
          populateStep2(workerProfile);
          goToStep(2);
        } else {
          alert(data.error || 'Extraction failed');
        }
      })
      .catch(err => {
        showSpinner(false);
        alert('Server communication error. Check Flask terminal.');
      });
    }

    function goToStep(step) {
      currentStep = step;
      document.getElementById('step-1').style.display = step === 1 ? 'flex' : 'none';
      document.getElementById('step-2').style.display = step === 2 ? 'block' : 'none';
      document.getElementById('step-3').style.display = step === 3 ? 'block' : 'none';
      document.getElementById('step-4').style.display = step === 4 ? 'block' : 'none';

      // reset button removed (logo handles reset)

      // Slogan is only shown on Step 1 landing page
      const slogan = document.getElementById('nav-slogan');
      if (slogan) {
        slogan.style.display = step === 1 ? 'block' : 'none';
      }

      if (step === 1) {
        selectedFile = null;
        uploadPill.innerText = 'Upload CV File Here';
        uploadPill.classList.remove('selected');
        fileInput.value = '';
      }
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function populateStep2(worker) {
      document.getElementById('input-worker-name').value = worker.worker_name || '';
      document.getElementById('input-current-role').value = worker.current_role || '';
      document.getElementById('input-experience-years').value = (worker.experience_years !== undefined && worker.experience_years !== null && worker.experience_years !== 0) ? worker.experience_years : '';
      document.getElementById('input-education-bg').value = worker.education_background || '';
      document.getElementById('input-target-domains').value = (worker.target_domains || []).join(', ');

      renderSkillTags(worker.current_skills || []);
    }

    function renderSkillTags(skills) {
      const list = document.getElementById('skills-tags-list');
      list.innerHTML = '';
      skills.forEach(skill => {
        const tag = document.createElement('span');
        tag.className = 'skill-tag';
        tag.innerHTML = `<span>✓ ${skill}</span><span class="skill-tag-remove" onclick="removeSkill(event, '${skill}')">×</span>`;
        list.appendChild(tag);
      });
    }

    function focusSkillInput() {
      document.getElementById('input-skill-inline').focus();
    }

    function removeSkill(e, skillName) {
      e.stopPropagation();
      workerProfile.current_skills = workerProfile.current_skills.filter(s => s !== skillName);
      renderSkillTags(workerProfile.current_skills);
    }

    function addSkill(skillName) {
      const s = skillName.trim();
      if (s && !workerProfile.current_skills.includes(s)) {
        workerProfile.current_skills.push(s);
        renderSkillTags(workerProfile.current_skills);
      }
    }

    const skillInput = document.getElementById('input-skill-inline');
    const dropdown = document.getElementById('typeahead-dropdown');

    skillInput.addEventListener('input', () => {
      const q = skillInput.value.toLowerCase().trim();
      if (!q) {
        dropdown.style.display = 'none';
        return;
      }
      const matches = allSkillCandidates.filter(c => c.toLowerCase().includes(q) && !workerProfile.current_skills.includes(c));
      if (matches.length > 0) {
        dropdown.innerHTML = matches.slice(0, 8).map(m => `<div class="typeahead-item" onclick="selectTypeahead('${m}')">${m}</div>`).join('');
        dropdown.style.display = 'block';
      } else {
        dropdown.style.display = 'none';
      }
    });

    skillInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        if (skillInput.value.trim()) {
          addSkill(skillInput.value.trim());
          skillInput.value = '';
          dropdown.style.display = 'none';
        }
      } else if (e.key === 'Backspace' && !skillInput.value && workerProfile.current_skills.length > 0) {
        workerProfile.current_skills.pop();
        renderSkillTags(workerProfile.current_skills);
      }
    });

    function selectTypeahead(skill) {
      addSkill(skill);
      skillInput.value = '';
      dropdown.style.display = 'none';
      skillInput.focus();
    }

    document.addEventListener('click', (e) => {
      if (!e.target.closest('.inline-tag-wrapper')) {
        dropdown.style.display = 'none';
      }
    });

    function confirmProfileAndDiagnose() {
      workerProfile.worker_name = document.getElementById('input-worker-name').value.trim() || 'Wong Swee Tiam';
      workerProfile.current_role = document.getElementById('input-current-role').value.trim() || 'Chemical Technician';
      workerProfile.experience_years = parseFloat(document.getElementById('input-experience-years').value) || 2.0;
      workerProfile.education_background = document.getElementById('input-education-bg').value.trim() || 'Bachelor of Chemical Technology';
      const domainsStr = document.getElementById('input-target-domains').value;
      workerProfile.target_domains = domainsStr.split(',').map(s => s.trim()).filter(s => s);

      showSpinner(true);
      fetch('/api/diagnose', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(workerProfile)
      })
      .then(res => res.json())
      .then(data => {
        showSpinner(false);
        diagnosisResult = data;
        populateStep3(diagnosisResult, workerProfile);
        goToStep(3);
      })
      .catch(err => {
        showSpinner(false);
        alert('Diagnosis error. Check backend.');
      });
    }

    function switchScenario(scKey) {
      activeScenario = scKey;
      const modPill = document.getElementById('scenario-pill-moderate');
      const accPill = document.getElementById('scenario-pill-accelerated');
      if (scKey === 'moderate') {
        modPill.classList.add('active');
        accPill.classList.remove('active');
      } else {
        modPill.classList.remove('active');
        accPill.classList.add('active');
      }
      renderStep3Content(activeScenario);
    }

    function populateStep3(diag, worker) {
      const target = worker.target_domains && worker.target_domains[0] ? worker.target_domains[0] : 'Chemical Quality Control';
      document.getElementById('step3-summary-bar').innerHTML = `
        <span style="color: #F8FAFC; font-weight: 600;">${worker.worker_name}</span> &nbsp;|&nbsp;
        <span>${worker.current_role}</span> &nbsp;|&nbsp;
        <span>${worker.experience_years} Years Experience</span> &nbsp;|&nbsp;
        <span style="color: #94A3B8;">Target: <b>${target}</b></span>
      `;

      renderStep3Content(activeScenario);
      document.getElementById('step3-disclaimer').innerText = 'Estimates based on O*NET 28.1, TalentCorp COL & Hays Asia 2025. For guidance only.';
    }

    function renderStep3Content(scKey) {
      const scData = (diagnosisResult.uncertainty_scenarios && diagnosisResult.uncertainty_scenarios[scKey]) 
        ? diagnosisResult.uncertainty_scenarios[scKey] 
        : { matched_roles: diagnosisResult.matched_roles || [], macro_impact_rate: 0.42, scenario_name: 'Moderate Transition', declining_skills: [], emerging_skills: [] };

      // Render Top 3 Roles for this specific scenario
      const roles = scData.matched_roles || [];
      const rankLabels = ['#1 Match', '#2 Match', '#3 Match'];

      document.getElementById('top3-roles-container').innerHTML = roles.slice(0, 3).map((r, idx) => {
        const rawScore = typeof r.match_score === 'number' ? r.match_score : 0.35;
        const displayScore = rawScore <= 1.0 ? Math.round(rawScore * 100) : Math.round(rawScore);
        const colTag = r.malaysia_col_aligned ? '✓ Aligned with TalentCorp COL' : '✓ National Priority Strategic Sector';
        const matchedCnt = (r.matched_skills || []).length;
        const missingCnt = (r.missing_skills || []).length;

        return `
          <div class="role-card">
            <div>
              <span class="role-rank-badge">${rankLabels[idx] || ('#' + (idx + 1))}</span>
              <h4 class="role-title">${r.role_title}</h4>
              <div class="role-score-salary">Match Score: ${displayScore}% | Salary: ${r.salary_range}</div>
              <div class="role-col-badge">${colTag}</div>
              <div class="role-skill-summary">
                <b>${matchedCnt}</b> Matched · <b>${missingCnt}</b> Skills to Acquire
              </div>
            </div>
            <button class="btn-view-pathway" onclick="exploreRole('${scKey}', ${idx})">View Pathway →</button>
          </div>
        `;
      }).join('');

      // Render Radar for this specific scenario
      const impactPct = Math.round((scData.macro_impact_rate || 0.42) * 100);
      document.getElementById('radar-header-container').innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: baseline; margin-top: 14px; margin-bottom: 8px;">
          <h3 style="font-size: 1.05rem; color: #F8FAFC;">Future Skills Radar · ${impactPct}% Automation Impact</h3>
          <span style="font-size: 0.75rem; color: #64748B;">Source: Hays Asia 2025 & O*NET 28.1 (Snapshot: 2025-01-15)</span>
        </div>
      `;

      const declining = (scData.declining_skills || ['Manual Titration', 'Excel Data Entry']).join(', ');
      const emerging = (scData.emerging_skills || ['Spectrometry Automation', 'Lab Data Digital Logging']).join(', ');

      document.getElementById('trends-container').innerHTML = `
        <div class="trend-box">
          <div style="font-size: 0.85rem; font-weight: 700; color: #CBD5E1; margin-bottom: 6px;">Declining Routine Skills</div>
          <div style="font-size: 0.85rem; color: #94A3B8; line-height: 1.5;">${declining}</div>
        </div>
        <div class="trend-box">
          <div style="font-size: 0.85rem; font-weight: 700; color: #CBD5E1; margin-bottom: 6px;">Emerging Core Competencies</div>
          <div style="font-size: 0.85rem; color: #94A3B8; line-height: 1.5;">${emerging}</div>
        </div>
      `;
    }

    function exploreRole(scKey, roleIndex) {
      populateStep4(diagnosisResult, scKey, roleIndex);
      goToStep(4);
    }

    function populateStep4(diag, scKey, roleIndex) {
      const scData = (diag.uncertainty_scenarios && diag.uncertainty_scenarios[scKey]) 
        ? diag.uncertainty_scenarios[scKey] 
        : { matched_roles: diag.matched_roles || [], recommended_duration_weeks: 14 };

      const roles = scData.matched_roles || [];
      const role = roles[roleIndex] || roles[0] || {};
      const pw = role.pathway || diag.reskilling_pathway || {};

      document.getElementById('step4-role-title').innerText = role.role_title || 'Quality Control Analyst';
      
      const paceText = scKey === 'accelerated' 
        ? `8-Week Fast-Track Sprint · ${role.salary_range || 'RM 4,000 - RM 5,500'}`
        : `14-Week Steady Transition · ${role.salary_range || 'RM 3,500 - RM 5,000'}`;
      const paceSubtitle = document.getElementById('step4-pace-subtitle');
      paceSubtitle.innerText = paceText;
      paceSubtitle.style.color = '#FACC15';

      const matchedContainer = document.getElementById('step4-matched-skills');
      const matchedList = (role.matched_skills && role.matched_skills.length > 0) ? role.matched_skills : [];
      if (matchedList.length > 0) {
        matchedContainer.innerHTML = matchedList.map(s => `<span class="skill-tag" style="border-color:#10B981; color:#10B981; background:rgba(16,185,129,0.12);">✓ ${s}</span>`).join(' ');
      } else {
        matchedContainer.innerHTML = '<span style="color:#64748B; font-size:0.82rem; font-style:italic;">No direct technical overlap · Baseline entry level</span>';
      }

      const missingContainer = document.getElementById('step4-missing-skills');
      const missingList = (role.missing_skills && role.missing_skills.length > 0) ? role.missing_skills : ['Spectrometry Automation', 'Green Chemistry Compliance'];
      missingContainer.innerHTML = missingList.map(s => `<span class="skill-tag">⚡ ${s}</span>`).join(' ');

      const phases = pw.phases || [];
      document.getElementById('step4-phases-container').innerHTML = phases.map(p => {
        const c = p.recommended_resource || {};
        return `
          <div class="phase-item">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
              <h5 style="color:#FACC15; font-size:1.02rem;">${p.phase_name}</h5>
              <span style="font-size:0.8rem; background:rgba(250,204,21,0.15); color:#FACC15; padding:2px 8px; border-radius:4px;">${p.duration_weeks} Weeks</span>
            </div>
            <p style="font-size:0.92rem; color:#F8FAFC; font-weight:700; margin-bottom:4px;">${c.course_name || 'Industry Specialized Training'}</p>
            <p style="font-size:0.82rem; color:#94A3B8; margin-bottom:6px;">Provider: ${c.provider || 'Accredited Institution'} | Funding: ${c.cost_type || 'HRD Corp / Subsidized'}</p>
            <span style="font-size:0.8rem; color:#CBD5E1; font-weight:600;">Credential: ${p.milestone_credential || 'Certificate of Completion'}</span>
          </div>
        `;
      }).join('');

      const sdgs = diag.sdg_alignment || [
        { sdg_code: "SDG 8.2", sdg_name: "Economic productivity through technological upgrading and innovation." },
        { sdg_code: "SDG 8.5", sdg_name: "Full and productive employment and decent work for all." },
        { sdg_code: "SDG 4.4", sdg_name: "Substantially increase youth and adults with relevant skills for employment." }
      ];

      document.getElementById('step4-sdgs-container').innerHTML = sdgs.map(sdg => `
        <div style="background:#0B0F17; border-left:3px solid #64748B; padding:8px 12px; border-radius:4px; margin-bottom:8px; font-size:0.8rem;">
          <b style="color:#CBD5E1;">${sdg.sdg_code}</b>: ${sdg.sdg_name}
        </div>
      `).join('');


    }

    function toggleExpander() {
      const content = document.getElementById('expander-content');
      const arrow = document.getElementById('expander-arrow');
      if (content.style.display === 'block') {
        content.style.display = 'none';
        arrow.innerText = '▼';
      } else {
        content.style.display = 'block';
        arrow.innerText = '▲';
      }
    }

    function showSpinner(show) {
      document.getElementById('loading-spinner').style.display = show ? 'block' : 'none';
    }
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, logo_b64=LOGO_B64)

@app.route("/api/skills", methods=["GET"])
def get_skills():
    try:
        skills = DataLoader().get_all_skill_candidates()
        return jsonify(skills)
    except Exception as e:
        return jsonify([]), 500

@app.route("/api/upload-resume", methods=["POST"])
def upload_resume():
    if "resume" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["resume"]
    filename = file.filename or "uploaded_cv.pdf"
    file_bytes = file.read()

    parser = ProfileParserService(timeout=8.0)
    raw_text = parser.extract_text_from_upload(file_bytes, filename)
    worker, parse_error = parser.parse_resume_text(raw_text)

    return jsonify({
        "worker": {
            "worker_id": worker.worker_id,
            "worker_name": worker.worker_name,
            "current_role": worker.current_role,
            "experience_years": worker.experience_years,
            "education_background": worker.education_background,
            "target_domains": worker.target_domains,
            "current_skills": worker.current_skills,
        },
        "parse_error": parse_error
    })

@app.route("/api/diagnose", methods=["POST"])
def diagnose():
    data = request.get_json() or {}
    worker = WorkerProfile(
        worker_id=data.get("worker_id", "WORKER-DEMO"),
        worker_name=data.get("worker_name", "Wong Swee Tiam"),
        current_role=data.get("current_role", "Chemical Technician"),
        experience_years=float(data.get("experience_years", 2.0)),
        education_background=data.get("education_background", "Bachelor of Chemical Technology"),
        target_domains=data.get("target_domains", ["Chemical Quality Control"]),
        current_skills=data.get("current_skills", ["Quality Control Analysis"]),
    )

    orchestrator = WorkflowOrchestrator()
    result = orchestrator.run_full_diagnosis(worker)
    return jsonify(result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8501))
    print(f"[*] LumiPath Web App launching on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
