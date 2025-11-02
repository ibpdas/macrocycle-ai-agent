[1️. Data Ingestion Layer]
• FRED (macroeconomics)
• CBOE (volatility)
• Yahoo Finance (market data)

↓  

[2️. Data Processing Layer]
• Normalisation & transformations
• JSON-based lineage tracking
• Time-series management  

↓  

[3️. AI Reasoning Layer]
• OpenAI GPT-5 LLM  
• Cycle classification (Expansion / Peak / Contraction / Trough)
• Confidence scoring & summaries  

↓  

[4️. Interface Layer]
• Replit (current) / Streamlit (planned) dashboard (real-time visualisation)
• Plotly charts
• User prompts & exploration tools  

↓  

[5. Automation & Governance Layer]
• GitHub Actions (scheduled runs)
• Replit agentic development
• Audit logs & version control
• Human-in-the-loop review


## Agentic Components  

MacroCycle implements an *agentic workflow* within the AI Reasoning layer:

| Agent | Role | Example Task |
|--------|------|--------------|
| **Research Agent** | Retrieves and contextualises macroeconomic data | Fetches indicators and writes summaries |
| **Architect Agent** | Validates data structures and ensures reproducibility | Checks JSON lineage and output consistency |
| **Testing Agent** | Evaluates results and identifies anomalies | Runs assertions on cycle classification accuracy |
| **Governance Layer (Human Oversight)** | Provides review and accountability | Reviews summaries before publication |
