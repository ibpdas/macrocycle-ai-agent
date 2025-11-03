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

The prototype applies world leading economic data from the United States to explore how such agents could be adapted to UK public sector data ecosystems, including potential applications across circular economy, green finance, and environmental protection domains.

**Key features and focus areas**:

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

- Rule based inference combining GDP, unemployment, inflation, and PMI  
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

MacroCycle was built to understand and demonstrate both the **potential and challenges** of AI driven data agents.  
It shows how **bounded autonomy, provenance, and human oversight** are essential for responsible innovation and how **data acquisition, metadata, lineage, and interoperability** are prerequisites for deploying AI tools safely and effectively across public sector domains.

| **Theme** | **Core Challenge / Assumption** | **MacroCycle Experience** | **MacroCycle Solution** | **Policy Insight for Data & AI Strategy** |
|:--|:--|:--|:--|:--|
| **1. Data Provenance** | AI agents retrieved data from multiple APIs (FRED, CBOE, Yahoo Finance) with no transparent lineage or timestamps. | Several endpoints returned legacy data with unclear update dates. | Introduced caching (1 hr economic / 30 min market) and metadata logging to record freshness and provenance. | Effective AI use requires audit trails for source, timestamp, reuse conditions, and version control — foundational for trustworthy AI. |
| **2. Human Oversight** | AI can generate plausible but incorrect economic interpretations; responsibility must remain human. | Automated outputs required interpretation and ethical framing. | Insights presented as *historical patterns*, not predictions, with disclaimers and validation. | Human-in-the-loop oversight is essential. Decision intelligence skills, prompt engineering, and Data and AI literacy must be part of wider workforce development. |
| **3. Cost & Sustainability (FinOps)** | API and compute costs can scale unpredictably; multi-agent use adds environmental cost. | High compute demand highlighted the ethical dimension of cost. | Token limits, caching, and quota warnings introduced to prevent overuse. | Treat FinOps as both financial and ethical governance: embed budget caps, cost attribution, and energy monitoring in every AI sandbox. |
| **4. Scalability & Infrastructure** | Rapid, fail-safe sandboxing with advanced capabilities is limited in current tools. | Replit / Streamlit not suited to high concurrency production. | Used sandbox for concept validation; recommended API-first, modular architecture for production. | Sandbox environments with secure, scalable access to advanced AI are vital precursors to enterprise deployment; require performance SLAs and load testing. |
| **5. Security & Compliance** | API keys and data connections risk exposure. | Managed credentials manually during prototyping. | Used environment-based secrets; avoided personal data storage. | Move toward ISO/IEC 42001 or equivalent industry and wider government-led compliance for AI system assurance. |
| **6. Explainability & Transparency** | AI agents can output results without showing how they were derived. | Traceability gaps limited auditability. | Proposed explainability traces to document data sources, assumptions, and logic paths. | Explainability dashboards should be standard in public-sector AI to build confidence and accountability. |
| **7. Representation & Bias** | Open datasets overrepresent developed and familiar domains. | Limited generalisability beyond US economic data. | Acknowledged bias; diversified indicators for future iterations. | Ethical AI requires proactive bias detection and contextual explanation, mirrored in environmental and social data gaps. |
| **8. Synthetic Data Boundaries** | Simulated data can blur into potential misuse if unlabeled. | Synthetic datasets aided scenario testing but risked misinterpretation. | Clearly labeled and deleted synthetic data post-demo. | Explicit labeling and retention policies are essential to distinguish simulation from official statistics and maintain public trust. |

> **Overall**, MacroCycle highlights the need for a more deliberate approach to **open data publication, usage tracking, and cost recovery**.  
> As AI driven tools increasingly consume open datasets at scale, public bodies should design data platforms that not only enable discovery and reuse, but also record usage metrics, manage API demand, and attribute operational costs transparently to esnure open access continues to deliver public value, economic growth, and environmental sustainability.
---

## Potential Roadmap Beyond Prototype  

| Phase | Focus | Target Milestone |
|-------|--------|-----------------|
| **Phase 1** | Integrate vector database retrieval and historical context memory for pattern recognition and recall (using Streamlit and Green Finance use case) | **Level 3 – Contextual Data Agent and full compliance with AI Playbook** |
| **Phase 2** | Reproduce the architecture with graph database and environmental datasets (circular economy, waste, water, biodiversity) to test cross-domain reasoning (using internal platform like DASH)| **Level 4 - Multi Domain Data Agent and full compliance with AI Playbook** |
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
