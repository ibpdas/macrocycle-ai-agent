```mermaid
flowchart TD
  subgraph L1[Data Sources]
    DS1[FRED\nGDP, CPI, Unemployment, M2]
    DS2[CBOE\nVIX, VVIX, Put/Call]
    DS3[Yahoo / SEC\nIndices, ETFs, Sectors]
    DS4[Synthetic Indicators\nISM PMI, Fear & Greed]
  end

  subgraph L2[Orchestration Layer]
    OR1[Data Fetcher\nAPI calls + retries]
    OR2[Normalisation\nPandas / NumPy]
    OR3[Metadata Logging\nProvenance, timestamps]
    OR4[Caching\n1h econ / 30m market]
  end

  subgraph L3[AI Reasoning Layer]
    AR1[Business Cycle Classifier]
    AR2[Fear & Greed Calculator]
    AR3[GPT-5 Reasoning Agent]
  end

  subgraph L4[Presentation Layer]
    PR1[Replit Sandbox]
    PR2[Streamlit Dashboard]
    PR3[GitHub Actions\nServerless automation]
  end

  DS1 --> OR1
  DS2 --> OR1
  DS3 --> OR1
  DS4 --> OR1
  OR1 --> OR2 --> OR3 --> OR4 --> AR1 --> AR2 --> AR3 --> PR2
  PR3 -. deploy/run .-> PR2
  PR1 -. prototype/run .-> PR2
