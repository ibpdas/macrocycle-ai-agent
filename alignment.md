# Alignment with HKUST Dial Framework & UK AI Playbook  

---

## HKUST Dial Framework – Levels of Data Agents  

Based on **Zhu et al., (2025)** [*HKUST Dial – Awesome Data Agents*](https://github.com/HKUSTDial/awesome-data-agents).  
Data agents evolve through five maturity levels. **MacroCycle AI Agent** aligns with **Level 2 – Reproducible Data Agent**, representing *bounded autonomy, reproducibility, and human oversight*.

| **Level** | **Title** | **Key Characteristics (HKUST)** | **MacroCycle Implementation** | **Typical Public-Sector Use Case** | **Alignment** |
|:--|:--|:--|:--|:--|:--:|
| **0** | Data Script | Static / rule-based automation with no learning. | Exceeds this level – MacroCycle includes multi-step reasoning and data fusion. | Batch ETL scripts or Excel macros. | ❌ |
| **1** | Automated Data Tool | Performs a single task (e.g. fetch or visualise data). | Automates multiple tasks – fetching, normalising, analysing, visualising. | Automated open-data report tool. | ❌ |
| **2** | **Reproducible Data Agent** | Multi-step workflows with structured reasoning and bounded autonomy; ensures auditability and human supervision. | ✅ Fully achieved:<br>• Multi-source orchestration (FRED, CBOE, Yahoo) <br>• Rule-based cycle inference <br>• Explainable LLM summaries <br>• Caching + metadata governance | Economic or environmental **observatory** (e.g. macroeconomic monitoring or circular-economy tracking). | 🟢 **MacroCycle = Level 2** |
| **3** | Contextual Data Agent | Adds adaptive learning and context memory (RAG / vector database). | Planned – Phase 1 roadmap to add vector retrieval and context recall. | Policy simulation or scenario testing (e.g. food security, energy resilience). | 🟡 Planned |
| **4** | Collaborative Multi-Agent System | Multiple domain agents coordinate under shared governance. | Prototype includes research, architect & testing agents but no domain coordination. | Inter-departmental data mesh (Defra, Treasury, DESNEZ). | ⚪ Partial |
| **5** | Self-Evolving Ecosystem | Fully autonomous self-optimising system with minimal human intervention. | Out of scope for governed public-sector AI. | Autonomous national data ecosystem / policy foresight. | 🔴 N/A |

> **Summary**  
> MacroCycle is positioned as a Level 2 prototype that demonstrates responsible, governed autonomy in AI data systems.  
> It prioritises reproducibility, transparency, and oversight — core requirements for data agent experimentation.  

---

## Alignment with the UK Government AI Playbook (2024)  

MacroCycle was assessed against the 10 principles of the UK Government AI Playbook for responsible AI delivery in the public sector.  

| **AI Playbook Principle** | **MacroCycle Alignment (✓ = strong, ~ = partial)** | **Supporting Evidence** |
|:--|:--:|:--|
| 1. Clearly define the problem AI is solving | ✓ | Addresses economic monitoring automation and data reuse for policy insight. |
| 2. Assess if AI is appropriate | ✓ | Demonstrates safe AI agent use via bounded autonomy (Level 2). |
| 3. Design with ethics & transparency | ✓ | Open data sources, clear method statements, and explainable outputs. |
| 4. Ensure data quality & governance | ✓ | Caching layer, metadata tracking, provenance control. |
| 5. Embed human oversight | ✓ | Human-in-the-loop validation for all AI outputs. |
| 6. Mitigate bias & risk | ✓ | Explicit bias section + synthetic data boundaries. |
| 7. Plan for sustainability & cost ( FinOps ) | ✓ | API quotas and cost/energy tracking built in. |
| 8. Monitor & evaluate performance | ~ | Manual review and logs present; no automated KPIs yet. |
| 9. Share knowledge & reusability | ✓ | Fully open-source with documented architecture and readme. |
| 10. Build trust through transparency & governance | ✓ | Governance layer visible in system architecture. |

> **Result summary:**  
> MacroCycle partially meets 10 AI principles, qualifying as a model for ethical, reproducible AI experimentation.  

---

### References  

- Zhu et al. (2025). *Awesome Data Agents: Taxonomy of Data-Centric AI Autonomy*. HKUST Dial Lab.  
- UK Government (2024). *Artificial Intelligence Playbook for the UK Government*.  
- Das, B. (2025). *MacroCycle AI Agent – A Reproducible Data Agent Prototype*. GitHub Repository.  
