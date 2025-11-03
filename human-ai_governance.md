```mermaid
flowchart TD

  %% =========================
  %% GOVERNANCE OVERLAY (GATES)
  %% =========================
  subgraph GOV[Governance Controls - applied across stages]
    G1[Human-in-the-loop Review]
    G2[Bias and Representation Check]
    G3[Security Controls\nSecrets management, no PII]
    G4[FinOps Guardrails\nToken limits, quotas, cost logs]
    G5[Traceability and Lineage\nProvenance, versioning]
    G6[Risk and Assurance\nDPIA/IA, ATRS-ready notes]
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
