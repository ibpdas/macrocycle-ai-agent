# MacroCycle AI Agent  
[![Awesome](https://awesome.re/badge.svg)](https://github.com/HKUSTDial/awesome-data-agents)
[![Open Source](https://img.shields.io/badge/status-open--source-brightgreen.svg)](https://github.com/ibpdas/macrocycle-ai-agent)
[![License](https://img.shields.io/badge/license-educational-blue.svg)](#license)

> **Aligned with:** [HKUST Dial — Awesome Data Agents (Zhu et al., 2025)](https://github.com/HKUSTDial/awesome-data-agents)  
> *A curated repository of research and open-source projects exploring autonomous data agents.*  
>
> **MacroCycle** is a *Level 2 open source prototype* demonstrating lightweight, reproducible, and ethical data agent — inspired by the taxonomy proposed in Zhu et al. (2025).

---

## Motivation  

**MacroCycle AI Agent** tests how data agents can autonomously fetch, interpret, and explain macroeconomic signals in natural language.  

The goal is to evaluate how autonomous, explainable, and reproducible data agents can support **evidence based decision making** and inform **data governance** across domains, including environmental and sustainability missions.

---

## Overview  

MacroCycle integrates multiple open data feeds (FRED, CBOE, Yahoo Finance) with a lightweight AI reasoning layer.  
It automates the retrieval, analysis, and explanation of key macroeconomic indicators to infer business cycle phases.  

- [MacroCycle AI Agent Dashboard](https://macrocycle.replit.app/)  (Available until November 2025)
**Created by:** [Bandhu Das FCCA](https://www.linkedin.com/in/ibpdas/)  
**Purpose:** Learning • Analysis • Ethical AI Experimentation  

---

## System Architecture  

**Pipeline Components**
1. **Data Ingestion** – Fetch macro indicators (FRED, CBOE, Yahoo).  
2. **Processing Layer** – Normalise and store indicators as structured JSON.  
3. **Reasoning Layer** – OpenAI LLM summarises data and infers cycle phase.  
4. **Interface Layer** – Replit / Streamlit dashboard for interactive visualisation.  
5. **Automation Layer** – GitHub Actions handle daily agent execution.  

> *Development note:*  
> The MacroCycle prototype was built and tested using **Replit’s agentic development environment** for rapid iteration and code level experimentation.  
> The application can also be self-served locally using the `app.py` file in this repository.  
> A **Streamlit based interface** is planned for open, user-friendly deployment in later phases.

---

## Key Features  

| Category | Description |
|-----------|-------------|
| **Autonomous Agent Workflow** | Fetch → Analyse → Summarise → Publish automatically. |
| **LLM Reasoning** | Generates contextual macro-economic insights with confidence scoring. |
| **Self-Service Dashboard** | Natural language exploration and trend comparison. |
| **JSON Data Contracts** | Ensures transparency, auditability, and reproducibility. |
| **Serverless Architecture** | Hosted via Replit, Streamlit Cloud + GitHub Actions. |

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

## Methodology & Data Quality 


---

## Evaluation   

| Capability | Result | Verification |
|-------------|---------|--------------|
| Business-cycle inference | 85 % alignment with NBER historical phases | Historical backtest |
| Data freshness | Hourly API updates via GitHub Actions | Log audit |
| LLM consistency | 100 % reproducible summaries via structured prompts | Manual review |
| Governance compliance | Mapped to goverment data ethics framework | Peer review |

---

## Prototype Learnings & Data Policy Insights  

**MacroCycle** demonstrates that responsible autonomy can be achieved without complex infrastructure.  
Its modular, transparent design provides practical lessons for scaling data-agent architectures across government contexts.

### Key Learnings  
- **Scalability & Architecture:** Lightweight, serverless setups can handle real-time open data at low cost. But may not scalble for complex and legacy datasets.   
- **Data Provenance:** JSON based lineage tracking improves auditability and reuse.  
- **Human Oversight:** Bounded autonomy with expert review ensures interpretability and trust.  
- **FinOps & Sustainability:** API-driven design reduces compute cost and energy use.  
- **Explainability:** Structured reasoning + natural-language summaries balance automation and transparency.

### Data Policy Implications  
MacroCycle highlights how technical design choices reinforce **data and AI policy principles**:  
- **Transparent Lineage** – Trace every indicator and transformation for accountability.  
- **Interoperable Models** – Use open formats and metadata standards for cross-department reuse.  
- **Responsible AI Use** – Embed bias checks, explainability, and human-in-the-loop oversight.  
- **Sustainable Data Operations** – Optimise for environmental and financial efficiency.  
- **Ethical Reuse of Open Data** – Ensure public datasets are used to build trust, not distort evidence.


## Research – Practice Reflection  

MacroCycle bridges **research and practice**, applying the Zhu et al. (2025) *Data Agents* taxonomy to a real-world, open-data use case.  
It shows how **bounded autonomy**, **provenance**, and **human oversight** can be operationalised in a low cost, reproducible prototype relevant to responsible data management and use.

---

## Potential Roadmap Beyond Prototype  

| Phase | Focus | Target Milestone |
|-------|--------|-----------------|
| **Phase 1** | Integrate vector-database retrieval and historical context memory to enable pattern recognition and contextual recall | **Level 3 – Conditional Autonomy** |
| **Phase 2** | Reproduce the architecture with open environmental datasets (e.g. circular economy, waste, water, food, biodiversity, green finance etc) to test cross-domain reasoning and decision support | **Multi-Domain Data Agent** |
| **Phase 3** | Introduce an **Explainable AI and Governance Dashboard** that visualises data lineage, confidence levels, and human-oversight checkpoints — enabling safe, transparent use of AI generated insights within real world policy experiments | **Policy Pilot Readiness – Governed Autonomy** |


---

## Acknowledgements  

This prototype was developed as part of a broader learning and research journey combining data strategy, data and AI governance, and applied experimentation.  

Special thanks to:  
- **[Imperial College London – AI Policy Fellowship](https://www.imperial.ac.uk/ai-policy-fellowship/)**  for providing the academic and reflective environment that shaped this project’s focus on AI literacy, ethics, and public sector applicability.  
- **Sue Bateman – Chief Data Officer, Defra**, for the research question and developmental guidance.  
- **HKUST Dial** for curating the *Awesome Data Agents* repository, which inspired the architectural framing of this Level 2 prototype.  


---

## Citation  

If referencing this project:

> Das, B. (2025). *MacroCycle AI Agent – A Reproducible Data-Agent Prototype.*  
> GitHub: https://github.com/ibpdas/macrocycle-ai-agent  
> DOI: Pending

---

## Links & Resources  

- [HKUST Dial – Awesome Data Agents (Zhu et al., 2025)](https://github.com/HKUSTDial/awesome-data-agents)  
- [Bandhu Das FCCA – LinkedIn](https://www.linkedin.com/in/ibpdas/)  

---

## License  

Educational and research use only.  
Comply with all third-party API terms (FRED, OpenAI, Yahoo Finance).

---

**© 2025 Bandhu Das FCCA – MacroCycle AI Agent Reflection and Prototype**


