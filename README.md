# MacroCycle AI Agent – A Reproducible Data Agent Prototype
[![Awesome](https://awesome.re/badge.svg)](https://github.com/HKUSTDial/awesome-data-agents)
[![Open Source](https://img.shields.io/badge/status-open--source-brightgreen.svg)](https://github.com/ibpdas/macrocycle-ai-agent)
[![License](https://img.shields.io/badge/license-educational-blue.svg)](#license)

> **Aligned with:** [HKUST Dial — Awesome Data Agents (Zhu et al., 2025)](https://github.com/HKUSTDial/awesome-data-agents)  
> *A curated repository of research and open-source projects exploring autonomous data agents.*  
>
> **MacroCycle** is a *Level 2 open source prototype* demonstrating lightweight, reproducible, and ethical data agent — inspired by the taxonomy proposed in Zhu et al. (2025).

---

## What it does? 

An autonomous **macro economic intelligence assistant** demonstrating the potential of **AI driven data agent** and responsible use. 

It automates the collection, analysis, and explanation of key macro economic and market indicators to infer business cycle phases. 

Instead of manually searching for data, it orchestrates multiple open data feeds and provides transparent, explainable summaries using LLM reasoning. Key features:

- **Automates Key Metrics** – Fetches and refreshes 50+ indicators from FRED, CBOE and Yahoo Finance  
- **Infers & Analyses** – Classifies business cycle phases (Expansion / Peak / Contraction / Trough) with confidence scoring  
- **Natural Language Queries** – Conversational interface powered by GPT-5 for context-aware economic Q&A  
- **Self Service Dashboards** – Explore macro, market & sentiment data interactively
- **Data Governance Insights** - Show data challenges to guide decision manking 
---  

- [MacroCycle AI Agent Dashboard](https://macrocycle.replit.app/)  (Available until November 2025)
- **Created by:** [Bandhu Das FCCA](https://www.linkedin.com/in/ibpdas/)

---

## Technical overview 

**Pipeline Components**
1. **Data Sources (structured + synthetic)** – Fetch macro indicators (FRED, CBOE, Yahoo) and derived indicators for missing data. 
2. **Processing Layer** – Normalise and store indicators as structured JSON.  
3. **Reasoning Layer** – GPT-5 data agent with **agentic orchestration** (Research, Architect & Testing agents) 
4. **Interface Layer** – Replit (current) → Streamlit (planned)  
5. **Automation Layer** – GitHub Actions handle agent execution with a serverless architecture
7. **Governance Layer** - JSON data contract documentation, human oversight, explainability and audit trail  

> *Development note:*  
> The MacroCycle prototype was built and tested using **Replit’s agentic development environment** for rapid iteration and code level experimentation.  
> The application can also be self-served locally using the `app.py` file in this repository.  
> A **Streamlit based interface** is planned for open, user friendly deployment in later phases.

---

## Tech Stack  

**Frontend:** Streamlit + Plotly  
**Backend:** Python 3.9 · Pandas · NumPy · yfinance · fredapi  
**AI Layer:** OpenAI GPT-5 API  
**Automation:** GitHub Actions + Serverless Workflows  
**Storage:** Structured JSON State (`last_summary.json`)  

---

## Ethics  

MacroCycle follows the principles of **responsible data and AI use**:

- **Transparency** — All results traceable to public sources.  
- **Reproducibility** — Workflows and outputs version-controlled.  
- **Accountability** — Human-in-the-loop review before publication.  
- **Proportionality** — Designed to support, not replace, expert analysis.  

## Analytical methodology 

- Rule based inference combining GDP, unemployment, inflation and PMI
- Confidence scoring (0–100%) for interpretability
- Historical backtesting across seven major cycles (2001–2023), aligned where applicable to NBER dating
- Synthetic indicators (ISM PMI, Fear & Greed Index) are clearly labelled
- Caching: 1h for economic series, 30m for market series; balances reproducibility and FinOps

---

## Evaluation   

| Capability | Result | Verification |
|-------------|---------|--------------|
| Business-cycle inference | 85 % alignment with NBER historical phases | Historical backtest |
| Data freshness | Hourly API updates via GitHub Actions | Log audit |
| LLM consistency | 100 % reproducible summaries via structured prompts | Manual review |
| Governance compliance | Mapped to goverment data ethics framework | Peer review |

---

## Prototype learnings & policy insights  

**MacroCycle** was built to understand and demonstrate both the potential and challenges of AI driven data agents. It shows how **bounded autonomy**, **provenance**, and **human oversight** are essential for responsible innovation. Critical insights for policymakers and practitioners.

#### Data Provenance & Management
**Challenge:** AI agents retrieve data from multiple APIs (FRED, CBOE, Yahoo Finance) without transparent lineage or timestamp verification  
**MacroCycle Experience:** Several API endpoints returned legacy data with no clear update date  
**Solution:** Caching layer (1hr economic, 30min market) reduces API costs; metadata tracking essential  
**Governance:** Ethical AI requires recording data source, update time, reuse conditions, and audit trails

#### Human Oversight & Accountability
**Challenge:** AI can generate plausible but incorrect economic interpretations; even in automated pipelines, responsibility must remain human  
**Solution:** All insights framed as "historical patterns," not predictions; disclaimers prominent  
**Reality:** Every output requires interpretation; every design choice carries ethical implications  
**Governance:** Mandatory human-in-the-loop validation—from data selection to publication—is essential for fair and trustworthy AI

#### FinOps & Sustainability
**Challenge:** API costs can scale unpredictably; running multiple AI agents reveals environmental cost of computation  
**MacroCycle Experience:** High energy and compute consumption makes FinOps both a financial AND ethical issue  
**Solution:** Token limits, caching, and quota warnings prevent runaway costs  
**Governance:** Budget caps, cost attribution, and energy monitoring should be embedded in every AI sandbox and production environment

#### Scalability & Architecture
**Challenge:** Replit or Streamlit architecture not suited for high-concurrency production use  
**Solution:** This prototype demonstrates concepts; production requires API first architecture  
**Governance:** Performance SLAs and load testing mandatory before public deployment

#### Security & Compliance
**Challenge:** API keys, user data, and financial information require protection  
**Solution:** Environment-based secrets; no personal data storage  
**Governance:** SOC2 / ISO27001 compliance required for production systems

#### Explainability & Transparency
**Challenge:** AI agents often provide outputs without explaining how results were derived  
**Risk:** Without an audit trail, confidence and accountability erode quickly  
**Governance:** Future iterations should include "explainability traces" summarising data sources, assumptions, and transformations used

#### Representation & Bias
**Challenge:** Open datasets over represent well documented markets or domains, but under represent less understood or researched domains.
**Risk:** Introduces bias into model training and interpretation 
**Governance:** Ethical practice demands deliberate bias detection and, where possible, weighting or contextual explanation

#### Synthetic Data Boundaries
**Challenge:** When does synthetic data cross the line from simulation to potential misuse?  
**MacroCycle Experience:** Synthetic datasets helpful for scenario testing but needed clear labelling and deletion rules  
**Governance:** Explicit labelling essential to avoid confusion with official statistics

---

## Potential Roadmap Beyond Prototype  (to demonstrate the art of possible further)

| Phase | Focus | Target Milestone |
|-------|--------|-----------------|
| **Phase 1** | Integrate vector database retrieval and historical context memory to enable pattern recognition and contextual recall in Streamlit tech environment | **Level 3 – Conditional Autonomy** |
| **Phase 2** | Reproduce the architecture with open environmental datasets (e.g. circular economy, waste, water, food, biodiversity, green finance etc) to test cross-domain reasoning and decision support in more scalable tech environment (beyond Streamlit) | **Multi-Domain Data Agent** |
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


