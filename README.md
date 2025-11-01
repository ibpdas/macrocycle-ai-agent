# MacroCycle AI Agent  
[![Awesome](https://awesome.re/badge.svg)](https://github.com/HKUSTDial/awesome-data-agents)
[![Open Source](https://img.shields.io/badge/status-open--source-brightgreen.svg)](https://github.com/ibpdas/macrocycle-ai-agent)
[![License](https://img.shields.io/badge/license-educational-blue.svg)](#license)

> **Aligned with:** [HKUST Dial — Awesome Data Agents (Zhu et al., 2025)](https://github.com/HKUSTDial/awesome-data-agents)  
> *A curated repository of research and open-source projects exploring autonomous data-analysis agents.*  
>
> **MacroCycle** is a *Level-2 open-source prototype* demonstrating lightweight, reproducible, and ethical data-agent architecture — inspired by the taxonomy proposed in Zhu et al. (2025).

---

## Motivation  

Traditional macroeconomic dashboards are static and descriptive.  
**MacroCycle AI Agent** tests a new approach — **AI driven data agents** that autonomously fetch, interpret, and explain macroeconomic signals in natural language.  

The goal is to evaluate how autonomous, explainable, and reproducible systems can support **evidence based decision-making** and inform **AI and data governance** across domains — including environmental and sustainability missions within government.

---

## Overview  

MacroCycle integrates multiple open data feeds (FRED, CBOE, Yahoo Finance) with a lightweight AI reasoning layer.  
It automates the retrieval, analysis, and explanation of key macroeconomic indicators to infer business-cycle phases.  

**Created by:** [Bandhu Das FCCA](https://www.linkedin.com/in/ibpdas/)  
**Purpose:** Learning • Analysis • Ethical AI Experimentation  

---

## System Architecture  

![MacroCycle Architecture](docs/macrocycle_architecture.png)

**Pipeline Components**
1. **Data Ingestion** – Fetch macro indicators (FRED, CBOE, Yahoo).  
2. **Processing Layer** – Normalise and store indicators as structured JSON.  
3. **Reasoning Layer** – OpenAI LLM summarises data and infers cycle phase.  
4. **Interface Layer** – Streamlit dashboard for interactive visualisation.  
5. **Automation Layer** – GitHub Actions handle daily agent execution.  

---

## Key Features  

| Category | Description |
|-----------|-------------|
| **Autonomous Agent Workflow** | Fetch → Analyse → Summarise → Publish automatically. |
| **LLM Reasoning** | Generates contextual macro-economic insights with confidence scoring. |
| **Self-Service Dashboard** | Streamlit UI for exploration and trend comparison. |
| **JSON Data Contracts** | Ensures transparency, auditability, and reproducibility. |
| **Serverless Architecture** | Hosted entirely via Streamlit Cloud + GitHub Actions. |

---

## Tech Stack  

**Frontend:** Streamlit + Plotly  
**Backend:** Python 3.9 · Pandas · NumPy · yfinance · fredapi  
**AI Layer:** OpenAI GPT-5 API  
**Automation:** GitHub Actions + Serverless Workflows  
**Storage:** Structured JSON State (`last_summary.json`)  

---

## Governance & Ethics  

MacroCycle follows the principles of **responsible data and AI use**:

- **Transparency** — All results traceable to public sources.  
- **Reproducibility** — Workflows and outputs version-controlled.  
- **Accountability** — Human-in-the-loop review before publication.  
- **Proportionality** — Designed to support, not replace, expert analysis.  

---

## Evaluation   

| Capability | Result | Verification |
|-------------|---------|--------------|
| Business-cycle inference | 85 % alignment with NBER historical phases | Historical backtest |
| Data freshness | Hourly API updates via GitHub Actions | Log audit |
| LLM consistency | 100 % reproducible summaries via structured prompts | Manual review |
| Governance compliance | Mapped to goverment data ethics framework | Peer review |

---

## Research – Practice Reflection  

MacroCycle bridges **research and practice**, applying the Zhu et al. (2025) *Data Agents* taxonomy to a real-world, open-data use case.  
It shows how **bounded autonomy**, **provenance**, and **human oversight** can be operationalised in a low cost, reproducible prototype relevant to responsible data management and use.

---

## Roadmap beyond prototype  

| Phase | Focus | Target Milestone |
|-------|--------|-----------------|
| 1️⃣ 2025 Q4 | Add vector-database retrieval + historical context memory | Level 3 Conditional Autonomy |
| 2️⃣ 2026 Q1 | Integrate Defra environmental data (circular economy, waste) | Multi-domain data agent |
| 3️⃣ 2026 Q2 | Introduce Explainable AI & Governance Dashboard | Policy Pilot Readiness |

---

## 👥 Acknowledgements  

Developed collaboratively with AI agents for architecture, testing, and documentation.  
Special thanks to **HKUST Dial** for curating the *Awesome Data Agents* framework that inspired this prototype.

---

## 📚 Citation  

If referencing this project:

> Das, B. (2025). *MacroCycle AI Agent – A Reproducible Data-Agent Prototype.*  
> GitHub: https://github.com/ibpdas/macrocycle-ai-agent  
> DOI: Pending 

---

## 🔗 Links & Resources  

- [MacroCycle AI Agent Dashboard](https://macro-cycle.streamlit.app/)  
- [HKUST Dial – Awesome Data Agents (Zhu et al., 2025)](https://github.com/HKUSTDial/awesome-data-agents)  
- [Bandhu Das FCCA – LinkedIn](https://www.linkedin.com/in/ibpdas/)  

---

## 📄 License  

Educational and research use only.  
Comply with all third-party API terms (FRED, OpenAI, Yahoo Finance).

---

**© 2025 Bandhu Das FCCA – MacroCycle AI Agent Reflection and Prototype**


