# MacroCycle AI Agent

An autonomous macro-economic intelligence assistant that integrates multiple public data feeds to analyze liquidity conditions, volatility measures, and key macro indicators for inferring business cycle stages.

**Created by:** [Bandhu Das FCCA](https://www.linkedin.com/in/ibpdas/)  
**Developed as part of the Imperial AI Policy Fellowship**

## 🎯 What Does It Do?

MacroCycle demonstrates the potential of AI-agent orchestration for real-time economic data management:

- **Automates Key Metrics**: Continuously fetches and processes economic indicators from FRED, CBOE, and Yahoo Finance
- **Infers & Analyzes**: Uses data-driven algorithms to classify business cycle phases (Expansion, Peak, Contraction, Trough) with confidence scoring
- **Natural Language Query**: Powered by OpenAI GPT-5, the AI research agent answers questions about economic data and market conditions
- **Self-Service Analysis**: Enables policymakers, academics, and investors to explore macro-economic relationships interactively

## 🏗️ Key Features

### 📊 Dashboard
- **6 Themed Tabs**: Business Cycle, Macro Economics, Liquidity & Credit, Market Sentiment, Market Structure, Sectors & Assets
- **Real-time Indicators**: GDP, unemployment, inflation, ISM PMI, yield curves, VIX, M2 money supply, and more
- **Interactive Visualizations**: Powered by Plotly for publication-quality charts

### 🤖 AI Research Agent
- **Autonomous Actions**: AI can fetch data, create visualizations, and suggest navigation autonomously
- **Economic Context Awareness**: Access to 12+ key metrics for data-driven responses
- **Educational Insights**: Historical patterns framed as insights, not predictions
- **Conversation History**: Multi-turn natural language conversations

### 🔄 Business Cycle Analysis
- **Phase Classification**: Determines current cycle stage using GDP, unemployment, inflation, and ISM PMI
- **Historical Backtesting**: Compares current conditions with past cycles
- **Portfolio Insights**: Historical asset allocation patterns across cycle phases
- **Sector Patterns**: Tracks sectors that historically outperformed/underperformed in each phase

### 📈 Market Data
- **Sector Performance**: Tracks 11 S&P 500 sectors plus alternative assets (Gold, Bitcoin, DXY)
- **Sentiment Indicators**: VIX, Put/Call Ratio, VVIX, HY-IG Spread, ETF Flows, AAII Survey
- **Fear & Greed Index**: Educational approximation using CNN's 7-indicator methodology

### 📚 Resources
- Curated collection of official data sources, academic materials, policy resources, and recommended reading

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- API Keys:
  - [FRED API Key](https://fredaccount.stlouisfed.org/apikeys) (free)
  - [OpenAI API Key](https://platform.openai.com/api-keys) (requires account)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/ibpdas/macrocycle-ai-agent.git
cd macrocycle-ai-agent
```

2. **Install dependencies:**
```bash
pip install streamlit pandas numpy plotly yfinance fredapi openai requests
```

3. **Set up environment variables:**
Create a `.streamlit/secrets.toml` file:
```toml
FRED_API_KEY = "your_fred_api_key_here"
OPENAI_API_KEY = "your_openai_api_key_here"
SESSION_SECRET = "any_random_string_for_session_management"
```

4. **Run the application:**
```bash
streamlit run app.py --server.port 5000
```

5. **Open your browser:**
Navigate to `http://localhost:5000`

## 📊 Data Sources

- **FRED (Federal Reserve Economic Data)**: GDP, CPI, unemployment, interest rates, M2 money supply, NFCI
- **Yahoo Finance (yfinance)**: Sector performance, ETFs, alternative assets
- **CBOE**: VIX, VVIX, Put/Call Ratio
- **Custom Calculations**: Fear & Greed Index, ISM PMI (synthetic for demonstration)

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Visualizations**: Plotly (graph_objects & express)
- **Data Processing**: Pandas, NumPy
- **APIs**: FRED API, Yahoo Finance, OpenAI GPT-5
- **Business Logic**: Custom Python algorithms for cycle analysis

## 📖 Who Can Use It?

### 👔 Policymakers
- Monitor real-time liquidity and credit conditions
- Track leading vs lagging indicators
- Understand global events' impact on economic cycles

### 🎓 Academics & Students
- Explore relationships between macro variables
- Study historical business cycles
- Learn about economic indicators and their interpretations

### 💼 Investors
- Analyze historical sector patterns across business cycles
- Track market sentiment and volatility
- Compare current conditions with past cycles

## ⚠️ Important Disclaimers

### Investment Disclaimer
This tool is for **educational and research purposes only**. It does not provide investment advice, financial recommendations, or trading signals. All content shows historical patterns and should not be interpreted as predictions or guidance for future investment decisions. Past performance does not indicate future results.

### AI & Data Limitations
- **Historical Patterns**: All insights are based on past data and do not predict future outcomes
- **Data Quality**: Relies on third-party APIs; accuracy depends on source data quality
- **Model Assumptions**: Business cycle classification uses simplified algorithms and should be validated against professional analysis
- **AI Responses**: Generated insights may contain errors; always verify with authoritative sources

## 🔬 Prototype Learnings: AI Governance & Operational Realities

This prototype demonstrates critical challenges in deploying autonomous AI agents for financial analysis:

### Core Operational Challenges
1. **Data Provenance & Management**: Tracking lineage from FRED/CBOE/Yahoo Finance
2. **Human Oversight & Accountability**: Critical for financial applications
3. **FinOps & Sustainability**: Managing API costs and computational resources
4. **Scalability & Architecture**: Handling real-time data at scale
5. **Security & Compliance**: Protecting sensitive financial data
6. **Explainability & Transparency**: Making AI decisions interpretable

### Data Ethics Considerations
- **Representation & Bias**: Ensuring diverse data sources and avoiding historical biases
- **Synthetic Data Boundaries**: Clear labeling when using approximations (e.g., ISM PMI, Fear & Greed Index)

### Policy Implications
Highlights the need for regulatory frameworks addressing AI in financial services, particularly around:
- Automated decision-making transparency
- Data quality standards
- Human-in-the-loop requirements
- Consumer protection in AI-driven analytics

## 👥 Multi-Agent Collaboration

This project was built through collaboration between multiple AI agents:
- **Replit Agent**: Core application development
- **Architect Agent**: Code review and architectural guidance
- **Testing Agent**: End-to-end testing with Playwright
- **OpenAI GPT-5 Agent**: Natural language research assistant

This meta-narrative demonstrates AI governance principles in practice—an AI tool built BY AI agents, showcasing both capabilities and limitations.

## 📝 Project Structure

```
macrocycle-ai-agent/
├── app.py                 # Main Streamlit application
├── ai_agent.py            # AI research agent with function calling
├── data_fetcher.py        # API integrations for FRED, Yahoo Finance
├── business_cycle.py      # Business cycle classification logic
├── pages/                 # Streamlit multi-page navigation
│   ├── 2_AI_Research_Agent.py
│   ├── 3_Business_Cycle.py
│   ├── 4_Market_Analysis.py
│   ├── 5_Resources.py
│   └── 6_About.py
├── .streamlit/
│   └── config.toml        # Streamlit configuration
├── replit.md              # Project documentation
└── README.md              # This file
```

## 🔗 Links & Resources

- **Creator**: [Bandhu Das FCCA on LinkedIn](https://www.linkedin.com/in/ibpdas/)
- **Imperial AI Policy Fellowship**: Research on AI governance and policy
- **Data Sources**: [FRED](https://fred.stlouisfed.org/), [CBOE](https://www.cboe.com/), [Yahoo Finance](https://finance.yahoo.com/)

## 📄 License

This project is for educational and research purposes. Please ensure compliance with all third-party API terms of service (FRED, OpenAI, Yahoo Finance).

---

**Questions or Feedback?** Connect with [Bandhu Das on LinkedIn](https://www.linkedin.com/in/ibpdas/)

*Built with ❤️ using Streamlit, Plotly, and OpenAI*
