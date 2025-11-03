```mermaid
flowchart TD
  H[Human Creator\nBandhu Das]

  subgraph AG[AI Agent Roles]
    A1[Replit Agent\nCode generation, rapid iteration]
    A2[Architect Agent\nReview and structure]
    A3[Testing Agent\nValidation and QA]
    A4[GPT-5 Research Agent\nContextual reasoning, Q&A]
  end

  H --> A1 --> A2 --> A3 --> A4 --> H
  A1 -. authors Streamlit .-> PR2[Streamlit Dashboard / planned]
  A2 -. reviews code .-> OR2[Normalisation Layer]
  A3 -. validates .-> PR2
  A4 -. generates insight .-> AR3[Reasoning Layer]

  H --> OUT[Replit MacroCycle Prototype\nReproducible AI Data Agent]
  A1 --> OUT
  A2 --> OUT
  A3 --> OUT
  A4 --> OUT
