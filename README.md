# MacroCycle AI Agent – A Reproducible Data Agent Prototype  
[![Awesome](https://awesome.re/badge.svg)](https://github.com/HKUSTDial/awesome-data-agents)
[![Open Source](https://img.shields.io/badge/status-open--source-brightgreen.svg)](https://github.com/ibpdas/macrocycle-ai-agent)
[![License](https://img.shields.io/badge/license-educational-blue.svg)](#license)

> **Aligned with:** [HKUST Dial — Awesome Data Agents (Zhu et al., 2025)](https://github.com/HKUSTDial/awesome-data-agents)  
> *A curated repository of research and open-source projects exploring autonomous data agents.*  
>
> **MacroCycle** is a *Level 2 open source prototype* demonstrating a lightweight, reproducible, and ethical data agent — inspired by the taxonomy proposed in Zhu et al. (2025).

---

## 📘 Table of Contents
- [What It Does](#what-it-does)
- [Technical Overview](#technical-overview)
- [Tech Stack](#tech-stack)
- [Ethics](#ethics)
- [Analytical Methodology](#analytical-methodology)
- [Evaluation](#evaluation)
- [Prototype Learnings & Policy Insights](#prototype-learnings--policy-insights)
- [Potential Roadmap Beyond Prototype](#potential-roadmap-beyond-prototype)
- [Acknowledgements](#acknowledgements)
- [Citation](#citation)
- [Disclaimer](#disclaimer)

---

## What It Does  

An autonomous **macroeconomic intelligence assistant** demonstrating the potential of **AI-driven data agents** and responsible innovation.  

MacroCycle automates the collection, analysis, and explanation of key macroeconomic and market indicators to infer business cycle phases.  
Instead of manually searching for data, it orchestrates multiple open data feeds and provides transparent, explainable summaries using LLM reasoning.  

### Key Features
- **Automates Key Metrics** – Fetches and refreshes 50+ indicators from FRED, CBOE, and Yahoo Finance  
- **Infers & Analyses** – Classifies business cycle phases (Expansion / Peak / Contraction / Trough) with confidence scoring  
- **Natural Language Queries** – Conversational interface powered by GPT-5 for context-aware economic Q&A  
- **Self-Service Dashboards** – Explore macro, market, and sentiment data interactively  
- **Data Governance Insights** – Surfaces data quality challenges to guide ethical, unbiased and confident decision-making  

---

- [MacroCycle AI Agent Dashboard](https://macrocycle.replit.app/) *(Available until November 2025)*  
- **Created by:** [Bandhu Das FCCA](https://www.linkedin.com/in/ibpdas/)

---

## Technical Overview  

**Pipeline Components**
1. **Data Sources (structured + synthetic)** – Fetch macro indicators (FRED, CBOE, Yahoo) and derive proxies for missing data  
2. **Processing Layer** – Normalise and store indicators as structured JSON  
3. **Reasoning Layer** – GPT-5 data agent with *agentic orchestration* (Research, Architect & Testing agents)  
4. **Interface Layer** – Replit (current) → Streamlit (planned)  
5. **Automation Layer** – GitHub Actions handle agent execution with a serverless workflow  
6. **Governance Layer** – JSON data contracts, human oversight, explainability, and audit trail  

> *Development note:*  
> The MacroCycle prototype was built and tested using **Replit’s AI-assisted development environment** for rapid iteration and experimentation.  
> The application can also be self-served locally using the `app.py` file in this repository.  
> A **Streamlit-based interface** is planned for open, user friendly deployment in later phases.

---

## Tech Stack  

**Frontend:** Replit (current) + Streamlit (planned) + Plotly  
**Backend:** Python 3.9 · Pandas · NumPy · yfinance · fredapi  
**AI Layer:** OpenAI GPT-5 API  
**Automation:** GitHub Actions (data refresh + report generation)  
**Storage:** Structured JSON State (`last_summary.json`)  

---

## Ethics  

MacroCycle follows the principles of **Government data ethics framework**:

- **Transparency** — All results traceable to public sources. Workflows and outputs version-controlled.  
- **Accountability** — Human-in-the-loop review before publication.  
- **Fairness** — Designed to support, not replace, expert analysis.  

---

## Analytical Methodology  

MacroCycle follows the principles of **Aquabook**:

- Rule-based inference combining GDP, unemployment, inflation, and PMI  
- Confidence scoring (0–100%) for interpretability  
- Historical backtesting across seven major cycles (2001–2023), aligned where applicable to NBER dating  
- Synthetic indicators (ISM PMI, Fear & Greed Index) are clearly labelled  
- Caching: 1h for economic series, 30m for market series (balancing reproducibility and FinOps)  

---

## Evaluation  

| Capability | Result | Verification |
|-------------|---------|--------------|
| Business-cycle inference | 85% alignment with NBER historical phases | Historical backtest |
| Data freshness | Hourly API updates via GitHub Actions | Log audit |
| LLM consistency | 100% reproducible summaries via structured prompts | Manual review |
| Governance compliance | Mapped to government data ethics framework | Peer review |

---

## Prototype Learnings & Policy Insights  

**MacroCycle** was built to understand and demonstrate both the potential and challenges of AI-driven data agents.  
It shows how **bounded autonomy**, **provenance**, and **human oversight** are essential for responsible innovation. It highlights the importance of **metdadata, data lineage, interoperability, and human oversight** as prerequisites for deploying AI tools safely in public sector domains.  

---

### Data provenance
- **Challenge:** AI agents retrieve data from multiple APIs (FRED, CBOE, Yahoo Finance) without transparent lineage or timestamp verification
- **MacroCycle Experience:** Several API endpoints returned legacy data with no clear update date
- **Solution:** Caching layer (1hr economic, 30min market) reduces API costs; metadata tracking essential
- **Governance:** Ethical AI requires recording data source, update time, reuse conditions, and audit trails  
<br>

### Human oversight  
- **Challenge:** AI can generate plausible but incorrect economic interpretations; responsibility must remain human
- **Solution:** Insights framed as "historical patterns," not predictions; disclaimers prominent
- **Reality:** Every output requires interpretation; every design choice carries ethical implications
- **Governance:** Mandatory human-in-the-loop validation—from data selection to publication—is essential for trustworthy AI  
<br>

### Costs  
- **Challenge:** API costs can scale unpredictably; running multiple AI agents reveals the environmental cost of computation
- **MacroCycle Experience:** High compute use makes FinOps both a financial AND ethical issue
- **Solution:** Token limits, caching, and quota warnings prevent runaway costs
- **Governance:** Budget caps, cost attribution, and energy monitoring embedded in every AI sandbox  
<br>

### Scalability 
- **Challenge:** Replit or Streamlit architecture not suited for high-concurrency production use
- **Solution:** Prototype demonstrates concepts; production requires API-first design
- **Governance:** Performance SLAs and load testing mandatory before deployment  
<br>

### Security   
- **Challenge:** API keys and data access require protection
- **Solution:** Environment-based secrets; no personal data stored
- **Governance:** SOC2 / ISO27001 compliance required for production systems  
<br>

### Explainability & transparency  
- **Challenge:** AI agents often provide outputs without explaining derivations
- **Risk:** Without an audit trail, confidence and accountability erode quickly
- **Governance:** Future iterations should include “explainability traces” summarising data sources and assumptions  
<br>

### Representation & bias  
- **Challenge:** Open datasets over represent developed or known domains, under represent less researched or understood domains
- **Risk:** Introduces bias into analysis and interpretation
- **Governance:** Ethical practice demands deliberate bias detection and contextual explanation  
<br>

### Synthetic data boundaries  
- **Challenge:** When does synthetic data cross from simulation to potential misuse?
- **MacroCycle Experience:** Synthetic datasets helpful for scenario testing but require clear labelling and deletion rules
- **Governance:** Explicit labelling prevents confusion with official statistics  

---

## Potential Roadmap Beyond Prototype  

| Phase | Focus | Target Milestone |
|-------|--------|-----------------|
| **Phase 1** | Integrate vector database retrieval and historical context memory for pattern recognition and recall (using Streamlit) | **Level 3 – Conditional Autonomy** |
| **Phase 2** | Reproduce the architecture with open environmental datasets (circular economy, waste, water, biodiversity, green finance) to test cross-domain reasoning (using more scalable environment beyond Streamlit)| **Multi-Domain Data Agent** |
| **Phase 3** | Introduce an **Explainable AI and Governance Dashboard** visualising lineage, confidence, and oversight checkpoints — enabling safe use within live policy pilots | **Policy Pilot Readiness – Governed Autonomy** |

---

## Acknowledgements  

This prototype was developed as part of a broader learning and research journey combining **data strategy**, **AI governance**, and **applied experimentation**.  

Special thanks to:  
- **[Imperial College London – AI Policy Fellowship](https://www.imperial.ac.uk/ai-policy-fellowship/)** for providing the academic and reflective environment that shaped this project’s focus on AI literacy, ethics, and public sector applicability.  
- **Sue Bateman – Chief Data Officer, Defra**, for the research question, career guidance, and mentorship.  
- **HKUST Dial** for curating the *Awesome Data Agents* repository, which inspired the architectural framing of this Level 2 prototype.  

---

## Citation  

If referencing this project:

> Das, B. (2025). *MacroCycle AI Agent – A Reproducible Data Agent Prototype.*  
> GitHub: https://github.com/ibpdas/macrocycle-ai-agent  
> DOI: Not available  

---

## Disclaimer  

- MacroCycle is a prototype for educational and research purposes only.  
- It does not constitute investment or financial advice.  
- All outputs should be independently verified before use.  
- Comply with all third-party API terms (FRED, OpenAI, Yahoo Finance).  

---

**© 2025 Bandhu Das FCCA – MacroCycle AI Agent Reflection and Prototype**
