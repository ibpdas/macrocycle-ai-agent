# MacroCycle Human–AI Governance Model (Based on Real Implementation)

MacroCycle was created to explore *what good looks like* when humans and AI agents collaborate responsibly in data rich environments.  
This model distils the *actual governance-by-design* principles tested within the MacroCycle ecosystem.

---

## 1. Governance Layers (G1–G5)

| Layer | Focus | Description | Typical Ownership |
|:--:|:--|:--|:--|
| **G1** | Ethical & Legal Grounding | Ensures privacy, fairness, and safe experimentation; defines boundaries for AI use. | Human Orchestrator (Bandhu Das) |
| **G2** | Data & Model Integrity | Controls input data quality (FRED), prompt logs, and model lineage. | Data Collector & Modeller Agents |
| **G3** | Human–AI Collaboration | Structures how reasoning agents explain outputs and accept feedback. | Orchestrator + Reasoning Agent |
| **G4** | System Reliability | Manages reproducibility, version control, and workflow traceability. | Technical Steward |
| **G5** | Learning & Transparency | Shares results, insights, and lessons for wider AI literacy. | MacroCycle Documentation |

---

## 2. Human Roles (HR1–HR4)

| Code | Role | Function in MacroCycle |
|:--:|:--|:--|
| **HR1** | Orchestrator | Defines objectives, supervises agents, validates outputs. |
| **HR2** | Technical Steward | Maintains code, tracks versions, and enforces data hygiene. |
| **HR3** | Reviewer / Evaluator | Tests reasoning quality, identifies drift or bias. |
| **HR4** | Learner / Observer | Uses MacroCycle as a learning environment to understand AI governance. |

---

## 3. AI Agent Roles (AR1–AR3)

| Code | Agent | Real Function | Governance Layer |
|:--:|:--|:--|:--:|
| **AR1** | Data Collector Agent | Accesses and cleans FRED macroeconomic data for reproducibility. | G2 |
| **AR2** | Modelling Agent | Runs analytical transformations, trend detection, and basic forecasting. | G2 |
| **AR3** | Reasoning Agent | Explains outputs, generates insights, accepts human feedback for refinement. | G3 |

---

## 4. Collaboration Protocols (OR1–OR4)

| Code | Protocol | Description | Governance Link |
|:--:|:--|:--|:--:|
| **OR1** | Human-in-the-Loop (HITL) | All results reviewed by Orchestrator before interpretation. | G1–G3 |
| **OR2** | Explainability Loop | Agents generate plain-English rationale for decisions. | G3 |
| **OR3** | Prompt Refinement Loop | Human feedback used to iteratively improve reasoning quality. | G3–G5 |
| **OR4** | Continuous Learning | Captures lessons for future AI literacy and data leadership work. | G5 |

---

## 5. Embedded Governance Controls

| Control | Description | Embedded In |
|:--|:--|:--|
| **Transparency Logs** | All prompts and outputs recorded for traceability. | MacroCycle app logs |
| **Explainability Reports** | AI agents summarise reasoning steps for review. | Reasoning Agent |
| **Bias & Drift Checks** | Comparison of outputs across runs to spot anomalies. | Orchestrator |
| **Audit Trail (Lightweight)** | Version controlled notebooks and dataset metadata. | GitHub / Streamlit |
| **Ethical Sandbox** | No personal data; only open FRED data. | System Boundary |

---

## 6. Governance Flow Diagram (Mermaid)

```mermaid
flowchart TB

subgraph G5["Learning & Transparency"]
  DOCS["Insights Shared / Data, AI & Decision Literacy"]
end

subgraph G4["System Reliability"]
  CODE["Version Control / Logs"]
end

subgraph G3["Human–AI Collaboration"]
  ORCH["Orchestrator"]
  REASON["Reasoning Agent (AR3)"]
end

subgraph G2["Data & Model Integrity"]
  DATA["Data Collector (AR1)"]
  MODEL["Modelling Agent (AR2)"]
end

subgraph G1["Ethical & Legal Grounding"]
  SAFE["Sandbox Boundary"]
end

SAFE --> DATA
DATA --> MODEL
MODEL --> REASON
REASON --> ORCH
ORCH --> CODE
CODE --> DOCS
DOCS --> SAFE

style SAFE fill:#f9c74f,stroke:#333
style DATA fill:#577590,stroke:#333
style MODEL fill:#43aa8b,stroke:#333
style REASON fill:#90be6d,stroke:#333
style ORCH fill:#f3722c,stroke:#333
style DOCS fill:#f94144,stroke:#333
