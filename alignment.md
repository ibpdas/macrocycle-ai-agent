# Alignment with HKUST Dial Framework & UK AI Playbook  

---

## HKUST Dial Framework – Levels of Data Agents  

Based on **Zhu et al., (2025)** [*HKUST Dial – Awesome Data Agents*](https://github.com/HKUSTDial/awesome-data-agents).  
Data agents evolve through five maturity levels. **MacroCycle AI Agent** aligns with **Level 2 – Reproducible Data Agent**, representing *bounded autonomy, reproducibility, and human oversight*.

| **Level** | **Title** | **Key Characteristics (HKUST)** | **MacroCycle Implementation** | **Typical Public-Sector Use Case** | **Alignment** |
|:--|:--|:--|:--|:--|:--:|
| **0** | Data Script | Static / rule-based automation with no learning. | Exceeds this level – MacroCycle includes multi-step reasoning and data fusion. | Batch ETL scripts or Excel macros. | 🟢 |
| **1** | Automated Data Tool | Performs a single task (e.g. fetch or visualise data). | Automates multiple tasks – fetching, normalising, analysing, visualising. | Automated open-data report tool. | 🟢 |
| **2** | **Reproducible Data Agent** | Multi-step workflows with structured reasoning and bounded autonomy; ensures auditability and human supervision. | ✅ Fully achieved:<br>• Multi-source orchestration (FRED, CBOE, Yahoo) <br>• Rule-based cycle inference <br>• Explainable LLM summaries <br>• Caching + metadata governance | Economic or environmental **observatory** (e.g. macroeconomic monitoring or circular-economy tracking). | 🟢 **MacroCycle = Level 2** |
| **3** | Contextual Data Agent | Adds adaptive learning and context memory (RAG / vector database). | Planned – Phase 1 roadmap to add vector retrieval and context recall. | Policy simulation or scenario testing (e.g. food security, energy resilience). | 🟡 Planned |
| **4** | Collaborative Multi-Agent System | Multiple domain agents coordinate under shared governance. | Prototype includes research, architect & testing agents but no domain coordination. | Inter-departmental data mesh (Defra, Treasury, DESNEZ). | ⚪ Partial |
| **5** | Self Evolving Ecosystem | Fully autonomous self-optimising system with minimal human intervention. | Out of scope for governed public-sector AI. | Autonomous national data ecosystem / policy foresight. | 🔴 N/A |

> **Summary**  
> MacroCycle is positioned as a Level 2 prototype that demonstrates responsible, governed autonomy in AI data systems.  
> It prioritises reproducibility, transparency, and oversight — core requirements for data agent experimentation.  

---

## Alignment with the UK Government AI Playbook (2024)  


The **UK Government Artificial Intelligence Playbook (CDDO, 2024)** sets out ten guiding principles for the safe, lawful and ethical use of AI across the public sector.  
MacroCycle AI Agent was reviewed against these principles to test its policy, ethical and technical readiness.

| **Principle** | **Summary** | **MacroCycle Alignment** | **Supporting Evidence** |
|:--|:--|:--:|:--|
| **1. You know what AI is and what its limitations are** | Understand AI’s capabilities, limits, and accuracy risks. | ✅ | Explicitly demonstrates bounded autonomy, transparency of limitations, and interprets outputs as “historical patterns,” not predictions. |
| **2. You use AI lawfully, ethically and responsibly** | Ensure compliance with legal and ethical standards; manage bias and sustainability. | ✅ | Open, non-personal datasets; bias management; FinOps for sustainability; strong emphasis on ethical and proportional AI use. |
| **3. You know how to use AI securely** | Build and deploy AI systems securely and resiliently. | ✅ | Environment-based secret management; no personal data; secure API handling; aligns with Secure by Design principles. |
| **4. You have meaningful human control at the right stages** | Maintain human oversight and intervention across AI lifecycle. | ⚪ Partial | Human-in-the-loop validation and oversight; users interpret insights rather than automate decisions. |
| **5. You understand how to manage the full AI life cycle** | Manage design, maintenance, monitoring, and closure. | ⚪ Partial | Documented lifecycle (arhcitechture diagram, learning); caching and metadata logging embedded. |
| **6. You use the right tool for the job** | Choose the most appropriate and proportionate solution. | ⚪ Partial | LLM orchestration chosen intentionally over complex ML; AI supports, not replaces, human judgment. |
| **7. You are open and collaborative** | Promote reuse, openness, and algorithmic transparency. | ✅ | Fully open-source; transparent README; linked to HKUST Dial academic taxonomy; encourages reuse and learning. |
| **8. You work with commercial colleagues from the start** | Engage commercial and procurement teams early to ensure shared ethical standards. | ⚪ Partial | Not yet applicable — to be embedded in Phase 2 (via in house tool deployment and supplier collaboration). |
| **9. You have the skills and expertise needed to implement and use AI solutions** | Build technical and ethical AI literacy across teams. | ⚪ Partial | Explicit focus on decision intelligence skills, prompt engineering, AI and data literacy and bias detection training. |
| **10. You use these principles alongside your organisation’s policies and have the right assurance in place** | Integrate AI governance with existing organisational policies. | ⚪ Partial | Aligned with Data & Information Strategic Roadmap, QFAIR principles, and Sustainability and AI strategy. |

> **Summary:**  
> MacroCycle demonstrates **alignment with 4 of 10 Playbook principles** and **partial alignment with 6 of 10 Playbook principles **.  
> It offers a practical reference for how *Level 2 reproducible data agents* can embody responsible, ethical, and transparent AI design within the UK public sector.

**References**  
- [Artificial Intelligence Playbook for the UK Government (CDDO, 2024)](https://www.gov.uk/government/publications/ai-playbook-for-the-uk-government)  
- [Defra Data & Information Strategic Roadmap 2030](https://www.gov.uk/government/publications/data-roadmap-for-defra-group)  
- [Das, B. (2025). *MacroCycle AI Agent – A Reproducible Data Agent Prototype.*](https://github.com/ibpdas/macrocycle-ai-agent)

---
