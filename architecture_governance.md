## MacroCycle – Combined System Architecture, Multi Agent Collaboration & Governance

```mermaid
flowchart TD
  %% =========================
  %% HUMAN OVERSIGHT (TOP)
  %% =========================
  H[👤 Human Creator\nBandhu Das FCCA\nConcept • Design • Policy framing]:::human

  %% =========================
  %% DATA / SYSTEM ARCHITECTURE
  %% =========================
  subgraph L1[📥 Data Sources]
    DS1[FRED\nGDP • CPI • Unemp • M2]
    DS2[CBOE\nVIX • VVIX • Put/Call]
    DS3[Yahoo/SEC\nIndices • ETFs • Sectors]
    DS4[Synthetic Indicators\nISM PMI • Fear & Greed]
  end

  subgraph L2[⚙️ Orchestration]
    OR1[Data Fetcher\nAPI calls + retries]
    OR2[Normalisation\nPandas / NumPy]
    OR3[Metadata Logging\nProvenance • Timestamps]
    OR4[Caching\n1h econ / 30m market]
  end

  subgraph L3[🧠 AI Reasoning]
    AR1[Business Cycle Classifier\nRule-based GDP/Unemp/CPI/PMI]
    AR2[Fear & Greed Calculator\n7-indicator method]
    AR3[GPT-5 Reasoning Agent\nContextual NL summaries]
  end

  subgraph L4[🗣️ Output Generation]
    OG1[Charts & Tables\nPlotly]
    OG2[Explanations\nHistorical patterns • Not predictions]
    OG3[Explainability Trace\nSources • Assumptions • Confidence]
  end

  subgraph L5[💻 Presentation & Automation]
    PR1[Replit Sandbox\nSafe, rapid experimentation]
    PR2[Streamlit Dashboard\nInteractive UI]
    PR3[GitHub Actions\nServerless automation • CI]
  end

  %% System flow
  DS1 --> OR1
  DS2 --> OR1
  DS3 --> OR1
  DS4 --> OR1
  OR1 --> OR2 --> OR3 --> OR4 --> AR1 --> AR2 --> AR3 --> OG1 --> OG2 --> OG3 --> PR2
  PR3 -. deploy/run .-> PR2
  PR1 -. prototype/run .-> PR2

  %% =========================
  %% MULTI-AGENT COLLABORATION
  %% =========================
  subgraph AG[🤖 Multi-Agent Collaboration]
    A1[🏗 Replit Agent\nCode gen • Rapid experiments]
    A2[🔍 Architect Agent\nCode review • Patterns]
    A3[🧪 Testing Agent\nPlaywright • QA reports]
    A4[🧠 GPT-5 Research Agent\nEcon context • Q&A]
  end

  %% Collaboration flow
  H --> A1 --> A2 --> A3 --> A4 --> H
  %% Agents influence system pieces
  A1 -. authors/improves .-> PR2
  A2 -. refines patterns .-> OR2
  A3 -. validates .-> PR2
  A4 -. curates context .-> AR3
  %% All agents contribute to final artefact
  A1 --> PR3
  A2 --> PR3
  A3 --> PR3
  A4 --> PR3

  %% =========================
  %% GOVERNANCE OVERLAY (GATES)
  %% =========================
  subgraph GOV[🛡 Governance Controls (applied across stages)]
    G1[Human-in-the-loop Review]
    G2[Bias/Representation Check]
    G3[Security Controls\nSecrets mgmt • No PII]
    G4[FinOps Guardrails\nToken limits • Quotas • Cost logs]
    G5[Traceability & Lineage\nProvenance • Versioning]
    G6[Risk & Assurance\nDPIA/IA • ATRS-ready notes]
  end

  %% Where gates apply
  OR3 --- G5
  OR4 --- G4
  AR1 --- G2
  AR2 --- G2
  AR3 --- G1
  OG3 --- G5
  PR2 --- G6
  PR3 --- G3
  H --- G1

  %% =========================
  %% STYLES
  %% =========================
  classDef human fill:#FFF7E6,stroke:#A86B00,stroke-width:1.5px;
  classDef layer fill:#EEF7FB,stroke:#1565C0,stroke-width:1.5px;
  classDef agents fill:#F2F7F6,stroke:#007B83,stroke-width:1.5px;
  classDef gate fill:#EAF6EA,stroke:#2E7D32,stroke-width:1.5px;

  class L1,L2,L3,L4,L5 layer;
  class AG agents;
  class GOV gate;
