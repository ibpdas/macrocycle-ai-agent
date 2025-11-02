# MacroCycle AI Agent – A Reproducible Data Agent Prototype  
[![Awesome](https://awesome.re/badge.svg)](https://github.com/HKUSTDial/awesome-data-agents)
[![Open Source](https://img.shields.io/badge/status-open--source-brightgreen.svg)](https://github.com/ibpdas/macrocycle-ai-agent)
[![License](https://img.shields.io/badge/license-educational-blue.svg)](#license)

> **Academic Alignment:**  
> Classified as a **Level 2 – Reproducible Data Agent** under the [HKUST Dial “Awesome Data Agents” taxonomy (Zhu et al., 2025)](https://github.com/HKUSTDial/awesome-data-agents).  
> Demonstrates *bounded autonomy, reproducibility, and human oversight* through modular, open data pipelines.  
>
> **Government Alignment:**  
> Reviewed against the **UK Government AI Playbook (CDDO, 2024)** — showing **strong foundational compliance (4 fully met, 6 partially met)** across lawfulness, transparency, human oversight, and lifecycle management principles.  
> Serves as an educational reference for how **responsible AI agents** can be developed and governed in the UK public sector.

---

## 📘 Table of Contents
- [Purpose](#purpose)
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

## Purpose  

**MacroCycle AI Agent** is an autonomous macroeconomic intelligence prototype built in a sandboxed environment as part of the Imperial College London AI Policy Fellowship.
It demonstrates how AI driven data agents can safely automate open data analysis while maintaining human accountability and ethical guardrails.

The prototype tests world-leading economic data publications from USA to test how such agents could be adapted to UK public sector data ecosystems, including potential applications across Defra’s circular economy, waste, and environmental protection domains.

Key features and focus areas:

- **Automation of Key Metrics** – Fetches and analyses 50+ economic indicators (FRED, CBOE, Yahoo Finance).  
- **Structured Reasoning** – Classifies business cycle phases with confidence scoring and metadata logging.  
- **Human Oversight** – Maintains human-in-the-loop control; all AI outputs are explanatory, not predictive.  
- **Open Data Ethics** – Built entirely on public APIs with clear provenance and synthetic data boundaries.  
- **Reproducibility** – All workflows version-controlled, modular, and open for reuse.  
- **Educational Value** – Demonstrates how public organisations can explore AI safely before scaling.  

---

- [MacroCycle AI Agent Dashboard](https://macrocycle.replit.app/) *(Available until November 2025)*  
- **Created by:** [Bandhu Das FCCA](https://www.linkedin.com/in/ibpdas/)

---

## Technical Overview  

**Pipeline Components**
1. **Data Sources (structured + synthetic)** – Fetch macro indicators (FRED, CBOE, Yahoo) and derive proxies for missing data  
2. **Processing** – Normalise and store indicators as structured JSON  
3. **Reasoning** – GPT-5 data agent with *agentic orchestration* (Research, Architect & Testing agents)  
4. **Interface** – Replit (current); Streamlit (planned); Internal tools (planned) (See Roadmap)   
5. **Automation** – GitHub Actions handle agent execution with a serverless workflow  
6. **Governance** – JSON data contracts, human oversight, explainability, and audit trail  

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

MacroCycle follows the principles of **Data Ethics Framework (2020)**:

- **Transparency** — All results traceable to public sources. Workflows and outputs version-controlled.  
- **Accountability** — Human-in-the-loop review before publication.  
- **Fairness** — Designed to make decisions with bias detection, counterfactuals and disbenefit considerations.

---

## Analytical Methodology  

MacroCycle follows the principles of **AQuA book (2025)**:

- Rule-based inference combining GDP, unemployment, inflation, and PMI  
- Confidence scoring (0–100%) for interpretability  
- Historical backtesting across seven major cycles (2001–2023), aligned where applicable to NBER dating  
- Synthetic indicators (ISM PMI, Fear & Greed Index) are clearly labelled  
- Caching: 1h for economic series, 30m for market series (balancing reproducibility and FinOps)  

---

## Evaluation  

| Capability | Result | Verification |
|-------------|---------|--------------|
| Business cycle inference | 85% alignment with NBER historical phases | Historical backtest |
| Data freshness | Hourly API updates via GitHub Actions | Log audit |
| LLM consistency | 100% reproducible summaries via structured prompts | Manual review |
| Governance compliance | Mapped to government data ethics framework | Peer review |

---

## Prototype Learnings & Policy Insights  

**MacroCycle** was built to understand and demonstrate both the potential and challenges of AI-driven data agents.  
It shows how **bounded autonomy**, **provenance**, and **human oversight** are essential for responsible innovation. It highlights the importance of **data acqusition, metdadata, data lineage, interoperability** as prerequisites for deploying AI tools safely and effectively in public sector domains.  

---

### Data provenance
- **Challenge:** AI agents retrieve data from multiple APIs (FRED, CBOE, Yahoo Finance) without transparent lineage or timestamp verification
- **MacroCycle Experience:** Several API endpoints returned legacy data with no clear update date
- **Solution:** Caching layer (1hr economic, 30min market) reduces API costs; metadata tracking essential
- **Insight:** Effectice AI use requires recording data source, update time, reuse conditions, and audit trails  

### Human oversight  
- **Challenge:** AI can generate plausible but incorrect economic interpretations; responsibility must remain human
- **Solution:** Insights framed as "historical patterns," not predictions; disclaimers prominent
- **Reality:** Every output requires interpretation; every design choice carries ethical implications
- **Insight:** Mandatory human-in-the-loop validation from data selection to publication is essential for effective AI use. Furthermore, decision intelligence skills, prompt engineering and data and AI literacy as part of wider workforece development. 

### Costs  
- **Challenge:** API costs can scale unpredictably; running multiple AI agents reveals the environmental cost of computation
- **MacroCycle Experience:** High compute use makes FinOps both a financial AND ethical issue
- **Solution:** Token limits, caching, and quota warnings prevent runaway costs
- **Insight:** Budget caps, cost attribution, and energy monitoring embedded in every AI sandbox  

### Scalability 
- **Challenge:** Rapid fail-safe, sandboxing environment with advanceed capabilites are missing.
- **MarcoCycle Experience:** Replit or Streamlit architecture not suited for high-concurrency production use
- **Solution:** Prototype demonstrates concepts; production requires API-first design; well designed sandbox environment with fast access to advanced capabilites. 
- **Insight:** Performance SLAs and load testing mandatory before deployment  

### Security   
- **Challenge:** API keys and data access require protection
- **Solution:** Environment-based secrets; no personal data stored
- **Insight:** ISO/IEC 42001 compliance required for production systems  

### Explainability & transparency  
- **Challenge:** AI agents often provide outputs without explaining derivations
- **Risk:** Without an audit trail, confidence and accountability erode quickly
- **Governance:** Future iterations should include “explainability traces” summarising data sources and assumptions  


### Representation & bias  
- **Challenge:** Open datasets over represent developed or known domains, under represent less researched or understood domains
- **Risk:** Introduces bias into analysis and interpretation
- **Governance:** Ethical practice demands deliberate bias detection and contextual explanation  

### Synthetic data boundaries  
- **Challenge:** When does synthetic data cross from simulation to potential misuse?
- **MacroCycle Experience:** Synthetic datasets helpful for scenario testing but require clear labelling and deletion rules
- **Insight:** Explicit labelling prevents confusion with official statistics  

---

## Potential Roadmap Beyond Prototype  

| Phase | Focus | Target Milestone |
|-------|--------|-----------------|
| **Phase 1** | Integrate vector database retrieval and historical context memory for pattern recognition and recall (using Streamlit and Green Finance use case) | **Level 3 – Contextual Data Agent and full compliance with AI Playbook** |
| **Phase 2** | Reproduce the architecture with environmental datasets (circular economy, waste, water, biodiversity) to test cross-domain reasoning (using internal platform like DASH)| **Level 4 - Multi Domain Data Agent and full compliance with AI Playbook** |
| **Phase 3** | Introduce an 'Explainable AI and Data Governance Dashboard' visualising lineage, confidence, and oversight checkpoints — enabling safe use within live policy pilots | **Level 4 – Multi Domain Data Agent and Governed Autonomy and full compliance with AI Playbook** |

---

## Acknowledgements  

This prototype was developed as part of a broader learning and research journey combining **data strategy**, **AI governance**, and **applied experimentation**.  

Special thanks to:  
- **[Imperial College London – AI Policy Fellowship](https://www.imperial.ac.uk/ai-policy-fellowship/)** for providing the academic and reflective environment that shaped this project’s focus on AI literacy, ethics, and public sector applicability.  
- **Sue Bateman – Chief Data Officer, Defra**, for the research question, career guidance, and mentorship.  
- **HKUST Dial** for curating the *Awesome Data Agents* repository, which inspired the architectural framing of this Level 2 prototype.  

---

| **Framework** | **Relevance** |
|:--|:--|
| [HKUST Dial – Awesome Data Agents (Zhu et al., 2025)](https://github.com/HKUSTDial/awesome-data-agents) | Academic classification of MacroCycle as a *Level 2 reproducible, governed data agent.* |
| [UK Government AI Playbook (CDDO, 2024)](https://www.gov.uk/government/publications/ai-playbook-for-the-uk-government) | 10 principles for safe, ethical, and transparent AI — MacroCycle meets 4 fully, 6 partially. |
| [Imperial College London AI Policy Fellowship](https://www.imperial.ac.uk/the-forum/courses-for-policymakers/fellowships/2025-fellows/) | Programme context for experimental design, governance reflection, and capability building. |

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
