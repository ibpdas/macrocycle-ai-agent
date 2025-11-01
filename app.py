import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from data_fetcher import EconomicDataFetcher, MarketDataFetcher
from business_cycle import BusinessCycleAnalyzer
from backtesting import HistoricalBacktester
from portfolio_positioning import PortfolioPositioner
from watchlist import WatchlistManager
from fear_greed_calculator import FearGreedCalculator
from ai_agent import MacroCycleAgent
import pandas as pd
import os

st.set_page_config(
    page_title="MacroCycle AI Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data(ttl=3600)
def load_economic_data():
    fetcher = EconomicDataFetcher()
    return {
        'gdp': fetcher.get_gdp_data(),
        'inflation': fetcher.get_inflation_data(),
        'unemployment': fetcher.get_unemployment_data(),
        'interest_rate': fetcher.get_interest_rate_data(),
        'm2_supply': fetcher.get_m2_supply_data(),
        'bond_yields': fetcher.get_bond_yields(),
        'gold_price': fetcher.get_gold_price(),
        'bitcoin_price': fetcher.get_bitcoin_price(),
        'dxy': fetcher.get_dxy_data(),
        'vix': fetcher.get_vix(),
        'vvix': fetcher.get_vvix(),
        'credit_spread': fetcher.get_credit_spread(),
        'hy_ig_spread': fetcher.get_hy_ig_credit_spread(),
        'ted_spread': fetcher.get_ted_spread(),
        'fed_balance_sheet': fetcher.get_fed_balance_sheet(),
        'reverse_repo': fetcher.get_reverse_repo(),
        'ism_manufacturing': fetcher.get_ism_manufacturing(),
        'ism_services': fetcher.get_ism_services(),
        'fear_greed': fetcher.get_fear_greed_index(),
        'sp500': fetcher.get_sp500_data(),
        'put_call_ratio': fetcher.get_put_call_ratio(),
        'nyse_highs_lows': fetcher.get_nyse_highs_lows(),
        'market_breadth': fetcher.get_market_breadth(),
        'safe_haven_demand': fetcher.get_safe_haven_demand(),
        'nfci': fetcher.get_nfci_data(),
        'market_momentum': fetcher.get_market_momentum(),
        'aaii_sentiment': fetcher.get_aaii_sentiment()
    }

def assess_liquidity(vix, credit_spread, ted_spread):
    score = 0
    
    if vix < 15:
        score += 2
    elif vix < 20:
        score += 1
    elif vix > 30:
        score -= 2
    elif vix > 25:
        score -= 1
    
    if credit_spread < 3:
        score += 2
    elif credit_spread < 4:
        score += 1
    elif credit_spread > 6:
        score -= 2
    elif credit_spread > 5:
        score -= 1
    
    if ted_spread < 0.3:
        score += 1
    elif ted_spread > 0.5:
        score -= 2
    elif ted_spread > 0.4:
        score -= 1
    
    if score >= 3:
        return "Healthy", "🟢", "Strong liquidity conditions with low volatility and tight spreads"
    elif score >= 0:
        return "Moderate", "🟡", "Normal liquidity with some volatility present"
    else:
        return "Stressed", "🔴", "Tightening liquidity with elevated volatility and widening spreads"

@st.cache_data(ttl=1800)
def load_market_data():
    fetcher = MarketDataFetcher()
    econ_fetcher = EconomicDataFetcher()
    return {
        'sectors': fetcher.get_sector_performance('1y'),
        'assets': fetcher.get_asset_class_data('5y'),
        'sentiment': {
            'put_call_ratio': econ_fetcher.get_put_call_ratio_latest(),
            'put_call_historical': econ_fetcher.get_put_call_ratio_chart_data(2),
            'vvix': econ_fetcher.get_vvix(),
            'vvix_historical': econ_fetcher.get_vvix_historical(2),
            'hy_ig_spread': econ_fetcher.get_hy_ig_credit_spread(),
            'hy_ig_historical': econ_fetcher.get_hy_ig_spread_historical(5),
            'etf_flows': econ_fetcher.get_etf_flows(30),
            'aaii': econ_fetcher.get_aaii_sentiment(),
            'aaii_historical': econ_fetcher.get_aaii_sentiment_historical(52)
        }
    }

def main():
    st.sidebar.title("MacroCycle AI Agent")
    
    # Initialize session state for cross-page context
    if 'cycle_phase' not in st.session_state:
        st.session_state.cycle_phase = None
    if 'cycle_confidence' not in st.session_state:
        st.session_state.cycle_confidence = None
    if 'selected_sectors' not in st.session_state:
        st.session_state.selected_sectors = []
    if 'risk_profile' not in st.session_state:
        st.session_state.risk_profile = 'Moderate'
    if 'watchlist_tickers' not in st.session_state:
        st.session_state.watchlist_tickers = []
    
    # Grouped navigation
    st.sidebar.markdown("---")
    page = st.sidebar.radio(
        "Navigation",
        [
            # Dashboard
            "🧮 Key Indicators",
            # AI Agent
            "🤖 AI Research Agent",
            # Cycle Analysis
            "🔄 Business Cycle",
            # Market Data
            "📊 Market Analysis",
            "📚 Resources",
            # Info
            "ℹ️ About"
        ]
    )
    
    economic_data = load_economic_data()
    market_data = load_market_data()
    
    if page == "🧮 Key Indicators":
        show_key_indicators(economic_data, market_data)
    elif page == "🤖 AI Research Agent":
        show_ai_research_agent(economic_data, market_data)
    elif page == "🔄 Business Cycle":
        show_business_cycle_consolidated(economic_data, market_data)
    elif page == "📊 Market Analysis":
        show_market_analysis(economic_data, market_data)
    elif page == "📚 Resources":
        show_resources()
    elif page == "ℹ️ About":
        show_about()

def _render_business_cycle(economic_data):
    st.header("🔄 Business Cycle Phase")
    st.caption("Leading and coincident indicators for cycle positioning")
    
    analyzer = BusinessCycleAnalyzer()
    cycle_analysis = analyzer.analyze_cycle_phase(
        economic_data['gdp'],
        economic_data['unemployment'],
        economic_data['inflation']
    )
    
    # Current Phase (large and prominent)
    phase = cycle_analysis['phase']
    confidence = cycle_analysis['confidence']
    
    col_phase, col_visual = st.columns([1, 1])
    with col_phase:
        if phase == 'Expansion':
            st.metric("Current Phase", phase, delta=f"{confidence}% confidence", delta_color="normal")
            st.success("🟢 **Risk-on:** Growth assets favored")
        elif phase == 'Peak':
            st.metric("Current Phase", phase, delta=f"{confidence}% confidence", delta_color="off")
            st.warning("🟡 **Late cycle:** Reduce risk, take profits")
        elif phase == 'Contraction':
            st.metric("Current Phase", phase, delta=f"{confidence}% confidence", delta_color="inverse")
            st.error("🔴 **Risk-off:** Defensive positioning")
        else:
            st.metric("Current Phase", phase, delta=f"{confidence}% confidence", delta_color="off")
            st.info("🟡 **Early recovery:** Selective opportunities")
    
    with col_visual:
        st.markdown("**Investment Implications:**")
        if phase == 'Expansion':
            st.markdown("✅ Favor: Equities, Small-caps, Commodities, Cyclicals  \n❌ Avoid: Bonds, Defensive sectors")
        elif phase == 'Peak':
            st.markdown("✅ Favor: Real assets, Commodities, Quality stocks  \n⚠️ Reduce: High beta, Leverage")
        elif phase == 'Contraction':
            st.markdown("✅ Favor: Bonds, Cash, Defensive sectors (Healthcare, Utilities)  \n❌ Avoid: Cyclicals, Small-caps")
        else:
            st.markdown("✅ Favor: Long-duration bonds, Emerging opportunities  \n🟡 Monitor: Early cyclical signals")
    
    st.divider()
    
    # Key Cycle Indicators (4 metrics in a row)
    st.subheader("📊 Key Cycle Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # 1. Yield Curve Spread (Leading Indicator - Recession Predictor)
    with col1:
        bond_yields = economic_data['bond_yields']
        yield_10y = bond_yields.get('10Y', 0)
        yield_2y = bond_yields.get('2Y', 0)
        yield_spread = yield_10y - yield_2y
        
        st.metric("Yield Curve Spread", f"{yield_spread:.2f}%", 
                 help="10Y-2Y Treasury spread - Leading recession indicator")
        if yield_spread < -0.5:
            st.error("🔴 Inverted")
        elif yield_spread < 0:
            st.warning("🟠 Flat/Inverted")
        elif yield_spread < 0.5:
            st.info("🟡 Flattening")
        else:
            st.success("🟢 Normal")
        st.caption("**Leading**")
    
    # 2. ISM PMI (Leading Indicator - Manufacturing Health)
    with col2:
        ism_mfg_df = economic_data.get('ism_manufacturing', pd.DataFrame())
        ism_mfg = ism_mfg_df['value'].iloc[-1] if len(ism_mfg_df) > 0 else 50.0
        
        st.metric("ISM Manufacturing", f"{ism_mfg:.1f}", 
                 help="PMI > 50 = expansion, < 50 = contraction")
        if ism_mfg > 55:
            st.success("🟢 Strong")
        elif ism_mfg > 50:
            st.info("🟡 Expanding")
        elif ism_mfg > 45:
            st.warning("🟠 Contracting")
        else:
            st.error("🔴 Weak")
        st.caption("**Leading**")
    
    # 3. Real GDP Growth (Coincident Indicator - Current Output)
    with col3:
        gdp_growth = cycle_analysis['gdp_growth']
        gdp_trend = cycle_analysis['gdp_trend']
        
        st.metric("Real GDP Growth", f"{gdp_growth:.1f}%", 
                 delta=gdp_trend.capitalize(),
                 delta_color="normal" if gdp_trend == 'rising' else "inverse",
                 help="Actual economic output growth")
        if gdp_growth > 3:
            st.success("🟢 Strong")
        elif gdp_growth > 2:
            st.info("🟡 Moderate")
        elif gdp_growth > 0:
            st.warning("🟠 Slow")
        else:
            st.error("🔴 Negative")
        st.caption("**Coincident**")
    
    # 4. NFCI (Coincident/Leading - Credit Stress)
    with col4:
        nfci_df = economic_data['nfci']
        current_nfci = nfci_df['value'].iloc[-1] if len(nfci_df) > 0 else 0
        
        st.metric("Credit Conditions", f"{current_nfci:.2f}", 
                 help="NFCI - National Financial Conditions Index")
        if current_nfci < -0.5:
            st.success("🟢 Very Loose")
        elif current_nfci < 0:
            st.info("🟡 Loose")
        elif current_nfci < 0.5:
            st.warning("🟠 Tightening")
        else:
            st.error("🔴 Stressed")
        st.caption("**Coincident**")
    
    st.divider()
    
    # Cycle Positioning Chart
    st.subheader("📈 Cycle Position Tracking")
    st.caption("Historical context - Where are we in the cycle?")
    
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        # GDP Growth Trend
        gdp_df = economic_data['gdp']
        if len(gdp_df) > 1:
            fig_gdp = go.Figure()
            fig_gdp.add_trace(go.Scatter(
                x=gdp_df['date'],
                y=gdp_df['value'],
                mode='lines',
                name='Real GDP Growth',
                line=dict(color='#2ca02c', width=2),
                fill='tozeroy',
                fillcolor='rgba(44, 160, 44, 0.1)'
            ))
            fig_gdp.add_hline(y=0, line_dash="solid", line_color="red", line_width=1)
            fig_gdp.add_hline(y=2, line_dash="dash", line_color="gray", 
                             annotation_text="Trend Growth (2%)")
            fig_gdp.update_layout(
                title='Real GDP Growth Trend',
                xaxis_title='Date',
                yaxis_title='YoY Growth (%)',
                height=300,
                hovermode='x unified'
            )
            st.plotly_chart(fig_gdp, use_container_width=True)
    
    with col_chart2:
        # Yield Curve Spread Trend
        if len(nfci_df) > 1:
            fig_nfci = go.Figure()
            fig_nfci.add_trace(go.Scatter(
                x=nfci_df['date'],
                y=nfci_df['value'],
                mode='lines',
                name='NFCI',
                line=dict(color='#9467bd', width=2),
                fill='tozeroy',
                fillcolor='rgba(148, 103, 189, 0.1)'
            ))
            fig_nfci.add_hline(y=0, line_dash="solid", line_color="gray", line_width=1,
                              annotation_text="Historical Average")
            fig_nfci.update_layout(
                title='Financial Conditions Index',
                xaxis_title='Date',
                yaxis_title='Index Value',
                height=300,
                hovermode='x unified'
            )
            st.plotly_chart(fig_nfci, use_container_width=True)
    
    st.caption("📊 Data Sources: [FRED](https://fred.stlouisfed.org) - GDP, Treasury Yields, NFCI | ISM PMI (Synthetic)")

def _render_macro_economics(economic_data):
    st.header("📊 Macro Economics")
    st.caption("Core economic indicators - GDP, Inflation, Unemployment, and Fed Policy")
    
    st.subheader("📈 CPI Year-over-Year")
    st.caption("Inflation trend - Key driver of Fed policy decisions")
    
    inflation_df = economic_data['inflation']
    current_cpi = inflation_df['value'].iloc[-1] if len(inflation_df) > 0 else 0
    previous_cpi = inflation_df['value'].iloc[-2] if len(inflation_df) > 1 else current_cpi
    cpi_change = current_cpi - previous_cpi
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Current CPI YoY", f"{current_cpi:.2f}%", delta=f"{cpi_change:+.2f}%")
    
    with col2:
        if current_cpi > 4:
            st.error("🔴 **High Inflation** - Restrictive policy needed")
        elif current_cpi > 3:
            st.warning("🟠 **Above Target** - Policy tightening likely")
        elif current_cpi > 2:
            st.success("🟢 **Near Target** - Healthy inflation")
        else:
            st.info("🟡 **Low Inflation** - Risk of deflation concerns")
    
    fig_cpi = go.Figure()
    fig_cpi.add_trace(go.Scatter(
        x=inflation_df['date'],
        y=inflation_df['value'],
        mode='lines',
        name='CPI YoY',
        line=dict(color='#ff7f0e', width=2)
    ))
    fig_cpi.add_hline(y=2.0, line_dash="dash", line_color="green", annotation_text="Fed Target (2%)")
    fig_cpi.update_layout(
        title='CPI Inflation Trend',
        xaxis_title='Date',
        yaxis_title='CPI YoY (%)',
        height=300,
        hovermode='x unified'
    )
    st.plotly_chart(fig_cpi, use_container_width=True)
    st.caption("📊 Data Source: [FRED - CPIAUCSL](https://fred.stlouisfed.org/series/CPIAUCSL)")
    
    st.divider()
    
    st.subheader("👥 Unemployment Rate")
    st.caption("Labour market health - Core economic strength indicator")
    
    unemployment_df = economic_data['unemployment']
    current_unrate = unemployment_df['value'].iloc[-1] if len(unemployment_df) > 0 else 0
    previous_unrate = unemployment_df['value'].iloc[-2] if len(unemployment_df) > 1 else current_unrate
    unrate_change = current_unrate - previous_unrate
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Current Unemployment", f"{current_unrate:.1f}%", delta=f"{unrate_change:+.1f}%", delta_color="inverse")
    
    with col2:
        if current_unrate < 4:
            st.success("🟢 **Full Employment** - Very tight labor market")
        elif current_unrate < 5:
            st.success("🟢 **Healthy** - Strong labor market")
        elif current_unrate < 6:
            st.info("🟡 **Moderate** - Softening conditions")
        else:
            st.error("🔴 **Elevated** - Labor market weakness")
    
    fig_unemp = go.Figure()
    fig_unemp.add_trace(go.Scatter(
        x=unemployment_df['date'],
        y=unemployment_df['value'],
        mode='lines',
        name='Unemployment Rate',
        line=dict(color='#d62728', width=2),
        fill='tozeroy'
    ))
    fig_unemp.update_layout(
        title='Unemployment Rate Trend',
        xaxis_title='Date',
        yaxis_title='Rate (%)',
        height=300,
        hovermode='x unified'
    )
    st.plotly_chart(fig_unemp, use_container_width=True)
    st.caption("📊 Data Source: [FRED - UNRATE](https://fred.stlouisfed.org/series/UNRATE)")
    
    st.divider()
    
    st.subheader("🏦 Federal Reserve Interest Rates & Policy Stance")
    st.caption("Current Fed Funds Rate and real yields - Critical drivers of asset prices")
    
    fed_funds_df = economic_data['interest_rate']
    current_fed_funds = fed_funds_df['value'].iloc[-1] if len(fed_funds_df) > 0 else 0
    
    bond_yields = economic_data['bond_yields']
    yield_10y = bond_yields.get('10Y', 0)
    real_10y = yield_10y - current_cpi
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Fed Funds Rate", f"{current_fed_funds:.2f}%", help="Federal Reserve's target rate for overnight lending")
    with col2:
        st.metric("10Y Yield", f"{yield_10y:.2f}%", help="10-year Treasury bond yield")
    with col3:
        st.metric("Real 10Y Yield", f"{real_10y:.2f}%", help="10Y yield minus inflation")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        if real_10y > 2:
            st.success("🟢 **High Real Yields** - Attractive for bonds, headwind for equities")
        elif real_10y > 0:
            st.info("🟡 **Positive Real Yields** - Neutral to positive for bonds")
        else:
            st.warning("🟠 **Negative Real Yields** - Bond returns lag inflation")
    
    with col_b:
        if current_fed_funds < 2:
            st.info("🔵 **Accommodative** - Stimulating economy")
        elif current_fed_funds < 4:
            st.info("🟡 **Neutral** - Balanced policy")
        else:
            st.warning("🔴 **Restrictive** - Cooling economy")
    
    st.markdown("**💡 FOMC Dot Plot & Forward Guidance:**")
    st.info("""
    📊 The FOMC "dot plot" shows where Federal Reserve members expect interest rates to be in the future. 
    This forward guidance is critical for understanding rate trajectory.
    
    View the official FOMC projections (updated quarterly):  
    → [Federal Reserve Summary of Economic Projections](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm)
    
    **Key Signals:**
    - **Dots moving higher** = Expect more rate hikes (bearish for stocks/bonds)
    - **Dots moving lower** = Expect rate cuts (bullish for stocks/bonds)
    - **Dot dispersion** = Uncertainty among Fed members about future path
    """)
    
    fig_policy = go.Figure()
    fig_policy.add_trace(go.Scatter(
        x=fed_funds_df['date'],
        y=fed_funds_df['value'],
        mode='lines',
        name='Fed Funds Rate',
        line=dict(color='#1f77b4', width=2)
    ))
    fig_policy.update_layout(
        title='Federal Funds Rate Historical Trend',
        xaxis_title='Date',
        yaxis_title='Rate (%)',
        height=300,
        hovermode='x unified'
    )
    st.plotly_chart(fig_policy, use_container_width=True)
    st.caption("📊 Data Source: [FRED - FEDFUNDS](https://fred.stlouisfed.org/series/FEDFUNDS) | For FOMC projections: [Federal Reserve](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm)")

def _render_liquidity_credit(economic_data):
    st.header("💵 Liquidity & Credit")
    st.caption("Money supply growth and credit conditions - Key drivers of asset price liquidity")
    
    st.subheader("💵 M2 Money Supply YoY Growth")
    st.caption("Liquidity trend - Money supply growth impacts asset prices")
    
    m2_df = economic_data['m2_supply']
    if len(m2_df) >= 12:
        current_m2 = m2_df['value'].iloc[-1]
        year_ago_m2 = m2_df['value'].iloc[-12]
        m2_yoy = ((current_m2 / year_ago_m2 - 1) * 100) if year_ago_m2 > 0 else 0
    else:
        m2_yoy = 0
        current_m2 = m2_df['value'].iloc[-1] if len(m2_df) > 0 else 0
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("M2 YoY Growth", f"{m2_yoy:.1f}%")
    
    with col2:
        if m2_yoy > 10:
            st.warning("🟠 **Excessive Growth** - Inflation risk")
        elif m2_yoy > 5:
            st.success("🟢 **Healthy Growth** - Supportive liquidity")
        elif m2_yoy > 0:
            st.info("🟡 **Moderate Growth** - Neutral liquidity")
        else:
            st.error("🔴 **Contracting** - Liquidity headwind for assets")
    
    if len(m2_df) >= 12:
        m2_yoy_series = []
        dates = []
        for i in range(12, len(m2_df)):
            yoy = ((m2_df['value'].iloc[i] / m2_df['value'].iloc[i-12] - 1) * 100)
            m2_yoy_series.append(yoy)
            dates.append(m2_df['date'].iloc[i])
        
        fig_m2 = go.Figure()
        fig_m2.add_trace(go.Scatter(
            x=dates,
            y=m2_yoy_series,
            mode='lines',
            name='M2 YoY Growth',
            line=dict(color='#2ca02c', width=2)
        ))
        fig_m2.add_hline(y=0, line_dash="dash", line_color="red", annotation_text="Zero Growth")
        fig_m2.update_layout(
            title='M2 Money Supply YoY Growth',
            xaxis_title='Date',
            yaxis_title='YoY Growth (%)',
            height=300,
            hovermode='x unified'
        )
        st.plotly_chart(fig_m2, use_container_width=True)
    
    st.caption("📊 Data Source: [FRED - M2SL](https://fred.stlouisfed.org/series/M2SL)")
    
    st.divider()
    
    st.subheader("💳 National Financial Conditions Index (NFCI)")
    st.caption("Credit conditions - Below zero = easier conditions, above zero = tighter")
    
    nfci_df = economic_data['nfci']
    current_nfci = nfci_df['value'].iloc[-1] if len(nfci_df) > 0 else 0
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Current NFCI", f"{current_nfci:.2f}")
    
    with col2:
        if current_nfci < -0.5:
            st.success("🟢 **Very Loose** - Easy credit conditions")
        elif current_nfci < 0:
            st.success("🟢 **Loose** - Accommodative conditions")
        elif current_nfci < 0.5:
            st.warning("🟠 **Tightening** - Credit getting more restrictive")
        else:
            st.error("🔴 **Tight** - Stressed credit conditions")
    
    fig_nfci = go.Figure()
    fig_nfci.add_trace(go.Scatter(
        x=nfci_df['date'],
        y=nfci_df['value'],
        mode='lines',
        name='NFCI',
        line=dict(color='#9467bd', width=2),
        fill='tozeroy'
    ))
    fig_nfci.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Historical Average")
    fig_nfci.update_layout(
        title='National Financial Conditions Index',
        xaxis_title='Date',
        yaxis_title='Index Value',
        height=300,
        hovermode='x unified'
    )
    st.plotly_chart(fig_nfci, use_container_width=True)
    st.caption("📊 Data Source: [FRED - NFCI](https://fred.stlouisfed.org/series/NFCI)")

def _render_market_sentiment(economic_data):
    st.header("😱 Market Sentiment")
    st.caption("Fear, volatility, and investor psychology indicators")
    
    # Key Sentiment Metrics in a row
    st.subheader("📊 Key Sentiment Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    # 1. VIX (Primary fear gauge)
    with col1:
        vix = economic_data['vix']
        st.metric("VIX", f"{vix:.2f}", help="CBOE Volatility Index - Market fear gauge")
        if vix < 15:
            st.success("🟢 Low Fear")
        elif vix < 20:
            st.info("🟡 Normal")
        elif vix < 30:
            st.warning("🟠 Elevated")
        else:
            st.error("🔴 High Fear")
    
    # 2. Put/Call Ratio (Risk appetite)
    with col2:
        put_call_data = economic_data.get('put_call_ratio', 1.0)
        # Extract scalar value - DataFrame has 'value' column
        if isinstance(put_call_data, pd.DataFrame):
            if 'value' in put_call_data.columns:
                put_call = float(put_call_data['value'].iloc[-1] if len(put_call_data) > 0 else 1.0)
            else:
                put_call = float(put_call_data.iloc[-1, -1] if len(put_call_data) > 0 else 1.0)
        elif isinstance(put_call_data, pd.Series):
            put_call = float(put_call_data.iloc[-1] if len(put_call_data) > 0 else 1.0)
        else:
            put_call = float(put_call_data)
        
        st.metric("Put/Call Ratio", f"{put_call:.2f}", help="Options market risk appetite")
        if put_call > 1.15:
            st.error("🔴 Fearful")
        elif put_call > 0.85:
            st.info("🟡 Neutral")
        else:
            st.success("🟢 Greedy")
    
    # 3. VVIX (Volatility of volatility)
    with col3:
        vvix_data = economic_data.get('vvix', 80.0)
        # VVIX returns a scalar directly
        if isinstance(vvix_data, (pd.DataFrame, pd.Series)):
            if isinstance(vvix_data, pd.DataFrame) and 'value' in vvix_data.columns:
                vvix = float(vvix_data['value'].iloc[-1] if len(vvix_data) > 0 else 80.0)
            else:
                vvix = float(vvix_data.iloc[-1] if len(vvix_data) > 0 else 80.0)
        else:
            vvix = float(vvix_data)
        
        st.metric("VVIX", f"{vvix:.1f}", help="Volatility of VIX - Uncertainty about volatility")
        if vvix > 120:
            st.error("🔴 Extreme")
        elif vvix > 100:
            st.warning("🟠 Elevated")
        else:
            st.success("🟢 Stable")
    
    # 4. Credit Spread (Credit market fear)
    with col4:
        hy_ig_data = economic_data.get('hy_ig_spread', 3.5)
        # HY-IG returns a scalar directly
        if isinstance(hy_ig_data, (pd.DataFrame, pd.Series)):
            if isinstance(hy_ig_data, pd.DataFrame) and 'value' in hy_ig_data.columns:
                hy_ig_spread = float(hy_ig_data['value'].iloc[-1] if len(hy_ig_data) > 0 else 3.5)
            else:
                hy_ig_spread = float(hy_ig_data.iloc[-1] if len(hy_ig_data) > 0 else 3.5)
        else:
            hy_ig_spread = float(hy_ig_data)
        
        st.metric("HY-IG Spread", f"{hy_ig_spread:.2f}%", help="High Yield to Investment Grade credit spread")
        if hy_ig_spread > 5:
            st.error("🔴 Stressed")
        elif hy_ig_spread > 4:
            st.warning("🟠 Cautious")
        else:
            st.success("🟢 Calm")
    
    st.divider()
    
    # VIX Detail
    st.subheader("😱 VIX Analysis")
    st.caption("Market fear gauge - Low VIX = complacency, High VIX = panic")
    
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        st.metric("Current VIX", f"{vix:.2f}")
        
        if vix < 15:
            st.success("🟢 **Low Fear** - Calm markets, potential complacency")
        elif vix < 20:
            st.info("🟡 **Normal** - Typical market conditions")
        elif vix < 30:
            st.warning("🟠 **Elevated Fear** - Increased uncertainty and volatility")
        else:
            st.error("🔴 **High Fear** - Market stress, potential opportunities for contrarians")
    
    with col_b:
        st.markdown("**Trading Implications:**")
        if vix < 15:
            st.markdown("- Options are cheap - consider protective puts  \n- Complacency risk - watch for sudden spikes")
        elif vix < 20:
            st.markdown("- Normal premium environment  \n- Standard risk management applies")
        elif vix < 30:
            st.markdown("- Options expensive - sell premium strategies  \n- Reduce position sizes, increase cash")
        else:
            st.markdown("- Extreme fear - contrarian buying opportunity?  \n- High option premiums favor sellers  \n- Wait for stabilization before deploying capital")
    
    st.divider()
    
    # Retail Investor Sentiment (AAII)
    st.subheader("📊 Retail Investor Sentiment (AAII)")
    st.caption("Weekly survey of individual investor sentiment")
    
    # Get AAII data if available from economic_data
    aaii = economic_data.get('aaii_sentiment', {
        'bullish': 35.0,
        'neutral': 30.0,
        'bearish': 35.0,
        'bull_bear_spread': 0.0
    })
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.metric("Bullish %", f"{aaii['bullish']:.1f}%")
        st.metric("Neutral %", f"{aaii['neutral']:.1f}%")
        st.metric("Bearish %", f"{aaii['bearish']:.1f}%")
        
        spread = aaii['bull_bear_spread']
        spread_color = "🟢" if spread > 10 else "🟡" if spread > -10 else "🔴"
        st.metric("Bull-Bear Spread", f"{spread:.1f}%")
        interpretation = "Bullish" if spread > 10 else "Neutral" if spread > -10 else "Bearish"
        st.write(f"{spread_color} {interpretation}")
    
    with col2:
        # Pie chart
        fig = go.Figure(data=[go.Pie(
            labels=['Bullish', 'Neutral', 'Bearish'],
            values=[aaii['bullish'], aaii['neutral'], aaii['bearish']],
            marker=dict(colors=['#2ecc71', '#95a5a6', '#e74c3c']),
            hole=0.4
        )])
        
        fig.update_layout(
            title='Current Sentiment Distribution',
            height=250,
            showlegend=True,
            margin=dict(t=40, b=0, l=0, r=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.caption("📊 Data Sources: [FRED - VIX](https://fred.stlouisfed.org/series/VIXCLS) | [AAII Sentiment Survey](https://www.aaii.com/sentimentsurvey) | Sample data for Put/Call, VVIX, HY-IG")

def _render_market_structure(economic_data, market_data):
    st.header("📉 Market Structure")
    st.caption("Yield curve and market momentum - Structural indicators of market health")
    
    st.subheader("📉 US Treasury Yield Curve")
    st.caption("Recession predictor - Inverted curve often precedes recessions")
    
    bond_yields = economic_data['bond_yields']
    yield_10y = bond_yields.get('10Y', 0)
    yield_2y = bond_yields.get('2Y', 0)
    yield_spread = yield_10y - yield_2y
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        maturities = ['2Y', '5Y', '10Y', '30Y']
        yields = [bond_yields.get(m, 0) for m in maturities]
        
        fig_yields = go.Figure()
        
        fig_yields.add_trace(go.Scatter(
            x=maturities,
            y=yields,
            mode='lines+markers',
            line=dict(color='#2ca02c', width=3),
            marker=dict(size=10),
            name='Yield'
        ))
        
        fig_yields.update_layout(
            title='Treasury Yield Curve',
            xaxis_title='Maturity',
            yaxis_title='Yield (%)',
            hovermode='x unified',
            height=300,
            showlegend=False
        )
        
        st.plotly_chart(fig_yields, use_container_width=True)
    
    with col2:
        st.markdown("**Current Yields**")
        for maturity, yield_val in bond_yields.items():
            if yield_val is not None:
                st.metric(f"{maturity} Treasury", f"{yield_val:.2f}%")
            else:
                st.metric(f"{maturity} Treasury", "N/A")
        
        st.markdown("**10Y-2Y Spread**")
        if yield_spread < 0:
            st.metric("Spread", f"{yield_spread:.2f}%", delta="Inverted ⚠️", delta_color="off")
        else:
            st.metric("Spread", f"{yield_spread:.2f}%", delta="Normal ✓", delta_color="off")
    
    if yield_spread < -0.5:
        st.error("🔴 **Strongly Inverted** - High recession risk within 12-18 months")
    elif yield_spread < 0:
        st.warning("🟠 **Inverted** - Recession signal, monitor closely")
    elif yield_spread < 0.5:
        st.info("🟡 **Flat** - Slowing growth expected")
    else:
        st.success("🟢 **Normal** - Healthy growth environment")
    
    st.caption("📊 Data Source: [FRED - US Treasury Yields](https://fred.stlouisfed.org)")
    
    st.divider()
    
    st.subheader("📊 Market Momentum vs 10-Month MA")
    st.caption("Trend following - Price above/below 10-month MA indicates bullish/bearish momentum")
    
    momentum_data = economic_data['market_momentum']
    
    col1, col2, col3 = st.columns(3)
    
    for idx, (ticker, col) in enumerate([('SPY', col1), ('QQQ', col2), ('IWM', col3)]):
        if ticker in momentum_data:
            data = momentum_data[ticker]
            with col:
                st.markdown(f"**{data['name']} ({ticker})**")
                st.metric(
                    "Current Price",
                    f"${data['current']:.2f}",
                    delta=f"{data['percent_from_ma']:+.1f}% from MA",
                    delta_color="normal" if data['above_ma'] else "inverse"
                )
                if data['above_ma']:
                    st.success("🟢 Above 10M MA - Bullish")
                else:
                    st.error("🔴 Below 10M MA - Bearish")
    
    momentum_summary = sum(1 for t in ['SPY', 'QQQ', 'IWM'] if t in momentum_data and momentum_data[t]['above_ma'])
    
    if momentum_summary == 3:
        st.success("🟢 **All 3 Above MA** - Strong broad market momentum")
    elif momentum_summary == 2:
        st.info("🟡 **2 of 3 Above MA** - Mixed momentum, selective strength")
    elif momentum_summary == 1:
        st.warning("🟠 **1 of 3 Above MA** - Weak momentum, defensive positioning")
    else:
        st.error("🔴 **All Below MA** - Bearish market trend, risk-off")
    
    st.caption("📊 Data Source: [Yahoo Finance](https://finance.yahoo.com)")

def _render_sectors_assets(market_data, economic_data):
    st.header("💰 Sectors & Assets")
    st.caption("Sector performance and alternative asset tracking")
    
    st.subheader("📊 Sector Performance (1Y)")
    st.caption("Year-over-year sector performance for strategic positioning")
    
    sector_df = pd.DataFrame([
        {'Sector': sector, 'Performance': data['performance']}
        for sector, data in market_data['sectors'].items()
    ]).sort_values('Performance', ascending=True)
    
    fig_sector = go.Figure(go.Bar(
        x=sector_df['Performance'],
        y=sector_df['Sector'],
        orientation='h',
        marker=dict(
            color=sector_df['Performance'],
            colorscale='RdYlGn',
            showscale=False
        )
    ))
    
    fig_sector.update_layout(
        title='Sector Performance (1Y)',
        xaxis_title='Return (%)',
        height=400
    )
    
    st.plotly_chart(fig_sector, use_container_width=True)
    st.caption("📊 Data Source: [Yahoo Finance - Sector ETFs](https://finance.yahoo.com)")
    
    st.divider()
    
    st.subheader("💎 Alternative Assets & Dollar")
    st.caption("Gold, Bitcoin, and US Dollar Index tracking")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Gold",
            f"${economic_data['gold_price']:,.2f}",
            help="Gold spot price or GLD ETF"
        )
    
    with col2:
        st.metric(
            "Bitcoin",
            f"${economic_data['bitcoin_price']:,.2f}",
            help="Bitcoin price in USD"
        )
    
    with col3:
        st.metric(
            "DXY",
            f"{economic_data['dxy']:.2f}",
            help="US Dollar Index"
        )

def show_key_indicators(economic_data, market_data):
    st.title("🧮 Key Indicators")
    st.caption("Comprehensive view of the most critical macro indicators organized by theme")
    
    with st.expander("🕒 Data Update Cadence", expanded=False):
        st.markdown("""
        **How often is data refreshed in this app?**
        
        | Data Source | Update Frequency | Source Refresh |
        |-------------|------------------|----------------|
        | **Economic Indicators** (GDP, Inflation, Unemployment) | Every 1 hour | FRED updates vary by indicator (daily to monthly) |
        | **Market Data** (Sectors, Asset Classes) | Every 30 minutes | Yahoo Finance real-time with 15-min delay |
        | **Fear & Greed Index** | Every 1 hour | CNN updates daily |
        | **Bond Yields & Spreads** | Every 1 hour | FRED updates daily |
        | **ISM PMI** | Every 1 hour | Synthetic data (ISM removed from FRED 2016) |
        | **M2 Money Supply** | Every 1 hour | FRED updates monthly |
        | **Market Liquidity Indicators** | Every 1 hour | FRED updates daily |
        
        *The app caches data to optimize performance and reduce API calls. Refresh the page to fetch the latest data.*
        """)
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🔄 Business Cycle",
        "📊 Macro Economics", 
        "💵 Liquidity & Credit",
        "😱 Market Sentiment",
        "📉 Market Structure",
        "💰 Sectors & Assets"
    ])
    
    with tab1:
        _render_business_cycle(economic_data)
    
    with tab2:
        _render_macro_economics(economic_data)
    
    with tab3:
        _render_liquidity_credit(economic_data)
    
    with tab4:
        _render_market_sentiment(economic_data)
    
    with tab5:
        _render_market_structure(economic_data, market_data)
    
    with tab6:
        _render_sectors_assets(market_data, economic_data)

def show_business_cycle_consolidated(economic_data, market_data):
    st.title("🔄 Business Cycle")
    st.caption("Comprehensive cycle analysis, historical backtesting, portfolio patterns, and sector watchlist")
    
    # Set up tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "🔄 Cycle Analysis",
        "⏮️ Historical Backtesting",
        "💼 Portfolio Positioning",
        "⭐ Sector Watchlist"
    ])
    
    with tab1:
        _render_cycle_analysis(economic_data)
    
    with tab2:
        _render_historical_backtesting(economic_data)
    
    with tab3:
        _render_portfolio_positioning(economic_data)
    
    with tab4:
        _render_sector_watchlist(economic_data, market_data)

def _render_cycle_analysis(economic_data):
    st.header("🔄 Business Cycle Analysis")
    
    analyzer = BusinessCycleAnalyzer()
    cycle_analysis = analyzer.analyze_cycle_phase(
        economic_data['gdp'],
        economic_data['unemployment'],
        economic_data['inflation'],
        economic_data['ism_manufacturing'],
        economic_data['ism_services']
    )
    
    # Save to session state for cross-page context
    st.session_state.cycle_phase = cycle_analysis['phase']
    st.session_state.cycle_confidence = cycle_analysis['confidence']
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"Current Phase: {cycle_analysis['phase']}")
        st.write(cycle_analysis['description'])
        
        st.info(f"**Confidence Level:** {cycle_analysis['confidence']}%")
        
        phases = ['Trough', 'Expansion', 'Peak', 'Contraction']
        current_phase_idx = phases.index(cycle_analysis['phase']) if cycle_analysis['phase'] in phases else 1
        
        fig = go.Figure()
        
        angles = [0, 90, 180, 270, 360]
        phase_names = phases + [phases[0]]
        
        fig.add_trace(go.Scatterpolar(
            r=[1, 1, 1, 1, 1],
            theta=angles,
            fill='toself',
            name='Business Cycle',
            line=dict(color='lightblue', width=2),
            fillcolor='rgba(135, 206, 250, 0.3)'
        ))
        
        current_angle = angles[current_phase_idx]
        fig.add_trace(go.Scatterpolar(
            r=[1.2],
            theta=[current_angle],
            mode='markers',
            name='Current Position',
            marker=dict(size=20, color='red', symbol='star')
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(visible=False, range=[0, 1.5]),
                angularaxis=dict(
                    ticktext=phase_names,
                    tickvals=angles,
                    direction='clockwise',
                    rotation=90
                )
            ),
            showlegend=False,
            title='Business Cycle Position',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.caption("📊 Data Sources: [FRED Economic Data](https://fred.stlouisfed.org) + ISM PMI")
    
    with col2:
        st.subheader("📊 Cycle Indicators")
        
        indicators = [
            ("GDP Growth", f"{cycle_analysis['gdp_growth']:.2f}%", cycle_analysis['gdp_trend']),
            ("Unemployment", f"{cycle_analysis['unemployment_current']:.2f}%", cycle_analysis['unemployment_trend']),
            ("Inflation", f"{cycle_analysis['inflation_current']:.2f}%", cycle_analysis['inflation_trend'])
        ]
        
        for name, value, trend in indicators:
            st.metric(name, value, trend.capitalize())
        
        st.markdown("---")
        st.markdown("**🏭 ISM PMI (Leading Indicators)**")
        
        ism_mfg_current = economic_data['ism_manufacturing']['value'].iloc[-1] if len(economic_data['ism_manufacturing']) > 0 else 50
        ism_svc_current = economic_data['ism_services']['value'].iloc[-1] if len(economic_data['ism_services']) > 0 else 50
        
        col_mfg, col_svc = st.columns(2)
        with col_mfg:
            mfg_status = "Expanding" if ism_mfg_current > 50 else "Contracting"
            mfg_color = "normal" if ism_mfg_current > 50 else "inverse"
            st.metric("Manufacturing", f"{ism_mfg_current:.1f}", mfg_status, delta_color=mfg_color)
        
        with col_svc:
            svc_status = "Expanding" if ism_svc_current > 50 else "Contracting"
            svc_color = "normal" if ism_svc_current > 50 else "inverse"
            st.metric("Services", f"{ism_svc_current:.1f}", svc_status, delta_color=svc_color)
        
        if ism_mfg_current > 50 and ism_svc_current > 50:
            st.success("🟢 Both sectors expanding")
        elif ism_mfg_current < 50 and ism_svc_current < 50:
            st.error("🔴 Both sectors contracting")
        else:
            st.warning("🟡 Mixed signals")
    
    st.divider()
    
    # Leading & Lagging Indicators
    st.subheader("📊 Leading vs Lagging Indicators")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**🔮 Leading Indicators** (Signal future changes)")
        leading_indicators = [
            ("Yield Curve (10Y-2Y)", economic_data['bond_yields'].get('10Y', 0) - economic_data['bond_yields'].get('2Y', 0)),
            ("ISM Manufacturing PMI", ism_mfg_current),
            ("ISM Services PMI", ism_svc_current),
        ]
        
        for name, value in leading_indicators:
            if "Yield" in name:
                status = "🔴 Inverted (recession risk)" if value < 0 else "🟢 Normal"
                st.markdown(f"• **{name}**: {value:.2f}% - {status}")
            else:
                status = "🟢 Expansion" if value > 50 else "🔴 Contraction"
                st.markdown(f"• **{name}**: {value:.1f} - {status}")
    
    with col2:
        st.markdown("**📈 Lagging Indicators** (Confirm changes)")
        lagging_indicators = [
            ("Unemployment Rate", cycle_analysis['unemployment_current'], "%"),
            ("CPI Inflation", cycle_analysis['inflation_current'], "%"),
            ("GDP Growth", cycle_analysis['gdp_growth'], "%")
        ]
        
        for name, value, unit in lagging_indicators:
            st.markdown(f"• **{name}**: {value:.2f}{unit}")
    
    st.caption("Leading indicators help anticipate cycle transitions, while lagging indicators confirm we've moved into a new phase.")
    
    st.divider()
    
    # What Could Trigger Phase Transition
    st.subheader("⚡ Potential Phase Transition Triggers")
    
    phase = cycle_analysis['phase']
    
    if phase == 'Expansion':
        st.markdown("""
        **What could move us to Peak phase:**
        - Yield curve inversion (10Y-2Y < 0%)
        - Fed funds rate significantly above neutral (4-5%)
        - Inflation persistently above 4%
        - ISM PMI falling below 50
        - Unemployment beginning to rise from cycle lows
        """)
    elif phase == 'Peak':
        st.markdown("""
        **What could move us to Contraction phase:**
        - Two consecutive quarters of negative GDP growth
        - Unemployment rising by 0.5%+ from recent lows
        - Credit spreads widening significantly (>200 bps)
        - Sharp stock market correction (>20%)
        - Leading indicators turning negative for 3+ months
        """)
    elif phase == 'Contraction':
        st.markdown("""
        **What could move us to Trough phase:**
        - Fed cutting rates aggressively (multiple 50 bps cuts)
        - Fiscal stimulus measures announced
        - ISM PMI stabilizing near 45-50 range
        - Credit spreads beginning to narrow
        - Unemployment rate peaking or flattening
        """)
    else:  # Trough
        st.markdown("""
        **What could move us to Expansion phase:**
        - Two consecutive quarters of positive GDP growth
        - Unemployment beginning sustained decline
        - ISM PMI rising above 50
        - Credit markets normalizing
        - Consumer and business confidence improving
        """)
    
    st.divider()
    
    # Global Events & News Impact
    st.subheader("🌍 Global Events That Can Impact Business Cycles")
    
    st.markdown("""
    **External factors that can accelerate or delay cycle transitions:**
    """)
    
    event_categories = {
        "🏛️ Monetary Policy": [
            "Federal Reserve rate decisions (typically 8 meetings/year)",
            "Quantitative easing (QE) or tightening (QT) programs",
            "Emergency lending facilities during crises",
            "Forward guidance and policy pivot signals"
        ],
        "💰 Fiscal Policy": [
            "Government stimulus packages (infrastructure, tax cuts)",
            "Debt ceiling debates and government shutdowns",
            "Tax policy changes affecting corporate earnings",
            "Social spending programs impacting consumer demand"
        ],
        "⚔️ Geopolitical Risks": [
            "Wars and military conflicts (Ukraine, Middle East)",
            "Trade wars and tariff disputes (US-China relations)",
            "Sanctions and economic restrictions",
            "Political transitions and election uncertainty"
        ],
        "🛢️ Commodity Shocks": [
            "Oil price spikes from OPEC+ supply decisions",
            "Food price inflation from weather or supply disruptions",
            "Energy crises (European gas crisis 2022)",
            "Metal and rare earth supply constraints"
        ],
        "🦠 Global Shocks": [
            "Pandemics (COVID-19 impact on 2020-2021 cycle)",
            "Financial crises (2008 GFC, regional banking stress)",
            "Natural disasters affecting supply chains",
            "Cyber attacks on critical infrastructure"
        ],
        "💱 Currency & Credit": [
            "US Dollar strength affecting emerging markets",
            "Credit market freezes (repo market stress)",
            "Banking sector stress (SVB, Credit Suisse events)",
            "Sovereign debt crises"
        ]
    }
    
    for category, events in event_categories.items():
        with st.expander(category, expanded=False):
            for event in events:
                st.markdown(f"• {event}")
    
    st.info("💡 **Key Insight**: Business cycles don't follow a fixed timeline. These external events can extend expansions, trigger early contractions, or accelerate recoveries. Monitor news for these catalysts.")
    
    st.divider()
    
    recommendations = analyzer.get_phase_recommendations(cycle_analysis['phase'])
    
    st.subheader("💡 Historical Cycle Patterns & Insights")
    st.caption("Based on historical analysis of past business cycles - not investment advice")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Typical Market Behavior:**")
        # Reframe as historical observation
        insight = recommendations['investment'].replace("Favor", "Historically favored").replace("Avoid", "Historically underperformed").replace("Buy", "Typically saw buying in").replace("Sell", "Typically saw selling in")
        st.write(insight)
        
        st.markdown("**Bond Market Patterns:**")
        bond_insight = recommendations['bonds'].replace("Consider", "Historically saw").replace("Increase", "increased").replace("Reduce", "reduced")
        st.write(bond_insight)
    
    with col2:
        st.markdown("**Commodity Behavior:**")
        commodity_insight = recommendations['commodities'].replace("Strong demand", "Historically strong demand").replace("Weak demand", "Historically weak demand")
        st.write(commodity_insight)
        
        st.markdown("**Historically Outperforming Sectors:**")
        for sector in recommendations['sectors']:
            st.write(f"• {sector}")
    
    st.caption("⚠️ Past patterns don't guarantee future results. Current cycle may differ due to unique economic conditions, policy responses, or external shocks.")
    
    st.divider()
    
    st.subheader("📚 Historical Business Cycles")
    
    historical = analyzer.get_historical_cycles()
    df = pd.DataFrame(historical)
    
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

def show_market_analysis(economic_data, market_data):
    st.title("📊 Market Analysis")
    st.caption("Sector performance, sentiment indicators, and Fear & Greed Index")
    
    # Set up tabs
    tab1, tab2 = st.tabs([
        "📊 Sectors & Performance",
        "😱 Fear & Greed Index"
    ])
    
    with tab1:
        _render_market_performance(market_data)
    
    with tab2:
        _render_fear_greed_index(economic_data)

def _render_market_performance(market_data):
    st.header("📊 Market Performance")
    
    st.subheader("🎯 Sector Performance")
    
    sector_df = pd.DataFrame([
        {
            'Sector': sector,
            'Performance': data['performance'],
            'Price': data['current_price']
        }
        for sector, data in market_data['sectors'].items()
    ]).sort_values('Performance', ascending=False)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = px.bar(
            sector_df,
            x='Sector',
            y='Performance',
            color='Performance',
            color_continuous_scale='RdYlGn',
            title='Sector Returns (1 Year)'
        )
        
        fig.update_layout(
            xaxis_tickangle=-45,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.caption("📊 Data Source: [Yahoo Finance - Sector ETFs](https://finance.yahoo.com)")
    
    with col2:
        st.markdown("**Top 3 Sectors:**")
        for idx, row in sector_df.head(3).iterrows():
            st.metric(
                row['Sector'],
                f"{row['Performance']:.2f}%"
            )
        
        st.markdown("**Bottom 3 Sectors:**")
        for idx, row in sector_df.tail(3).iterrows():
            st.metric(
                row['Sector'],
                f"{row['Performance']:.2f}%"
            )
    
    st.divider()
    
    st.subheader("💼 Asset Class Performance")
    
    asset_df = pd.DataFrame([
        {
            'Asset Class': asset,
            'Performance': data['performance'],
            'Price': data['current_price']
        }
        for asset, data in market_data['assets'].items()
    ])
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = go.Figure(data=[
            go.Bar(
                x=asset_df['Asset Class'],
                y=asset_df['Performance'],
                marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
            )
        ])
        
        fig.update_layout(
            title='Asset Class Returns (5 Years)',
            yaxis_title='Return (%)',
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.caption("📊 Data Source: [Yahoo Finance - Asset ETFs](https://finance.yahoo.com)")
    
    with col2:
        for idx, row in asset_df.iterrows():
            st.metric(
                row['Asset Class'],
                f"${row['Price']:.2f}",
                f"{row['Performance']:.2f}%"
            )
    
    st.divider()
    
    st.subheader("🎭 Market Sentiment & Risk Indicators")
    
    st.caption("Gauge market fear, risk appetite, and credit stress through key sentiment indicators")
    
    # Current Sentiment Metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        pc_ratio = market_data['sentiment']['put_call_ratio']
        pc_color = "🟢" if pc_ratio < 0.7 else "🟡" if pc_ratio < 1.0 else "🔴"
        st.metric(
            "Put/Call Ratio",
            f"{pc_ratio:.2f}",
            help="Options Put/Call Ratio: <0.7 = Bullish, 0.7-1.0 = Neutral, >1.0 = Bearish"
        )
        interpretation = "Bullish (Low fear)" if pc_ratio < 0.7 else "Neutral" if pc_ratio < 1.0 else "Bearish (High fear)"
        st.write(f"{pc_color} {interpretation}")
    
    with col2:
        vvix = market_data['sentiment']['vvix']
        vvix_color = "🟢" if vvix < 80 else "🟡" if vvix < 110 else "🔴"
        st.metric(
            "VVIX (Vol of Vol)",
            f"{vvix:.1f}",
            help="Volatility of VIX: <80 = Low tail risk, 80-110 = Moderate, >110 = High tail risk"
        )
        tail_risk = "Low tail risk" if vvix < 80 else "Moderate risk" if vvix < 110 else "High tail risk"
        st.write(f"{vvix_color} {tail_risk}")
    
    with col3:
        hy_ig = market_data['sentiment']['hy_ig_spread']
        spread_color = "🟢" if hy_ig < 3.0 else "🟡" if hy_ig < 5.0 else "🔴"
        st.metric(
            "HY-IG Credit Spread",
            f"{hy_ig:.2f}%",
            help="High Yield minus Investment Grade spread: <3% = Healthy, 3-5% = Elevated, >5% = Stress"
        )
        credit_health = "Healthy credit" if hy_ig < 3.0 else "Elevated stress" if hy_ig < 5.0 else "Credit stress"
        st.write(f"{spread_color} {credit_health}")
    
    st.markdown("---")
    
    # Historical Charts
    tab1, tab2, tab3 = st.tabs(["📊 Put/Call Ratio", "📈 VVIX", "💳 Credit Spreads"])
    
    with tab1:
        st.markdown("**Put/Call Ratio - Historical Trend (2 Years)**")
        pc_data = market_data['sentiment']['put_call_historical']
        if not pc_data.empty:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=pc_data['date'],
                y=pc_data['value'],
                mode='lines',
                name='Put/Call Ratio',
                line=dict(color='#FF6B6B', width=2)
            ))
            
            # Add reference lines
            fig.add_hline(y=0.7, line_dash="dash", line_color="green", 
                         annotation_text="Bullish Threshold (0.7)")
            fig.add_hline(y=1.0, line_dash="dash", line_color="red", 
                         annotation_text="Bearish Threshold (1.0)")
            
            fig.update_layout(
                xaxis_title='Date',
                yaxis_title='Put/Call Ratio',
                hovermode='x unified',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            st.caption("📊 Data Source: [CBOE Put/Call Ratio via FRED (PUTCALL)](https://fred.stlouisfed.org/series/PUTCALL)")
        else:
            st.info("Historical Put/Call data unavailable")
    
    with tab2:
        st.markdown("**VVIX - Volatility of VIX (2 Years)**")
        vvix_data = market_data['sentiment']['vvix_historical']
        if not vvix_data.empty:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=vvix_data['date'],
                y=vvix_data['value'],
                mode='lines',
                name='VVIX',
                line=dict(color='#4ECDC4', width=2),
                fill='tozeroy',
                fillcolor='rgba(78, 205, 196, 0.1)'
            ))
            
            # Add reference lines
            fig.add_hline(y=80, line_dash="dash", line_color="green", 
                         annotation_text="Low Risk (80)")
            fig.add_hline(y=110, line_dash="dash", line_color="red", 
                         annotation_text="High Risk (110)")
            
            fig.update_layout(
                xaxis_title='Date',
                yaxis_title='VVIX Index',
                hovermode='x unified',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            st.caption("📊 Data Source: [CBOE VVIX via FRED (VVIXCLS)](https://fred.stlouisfed.org/series/VVIXCLS)")
        else:
            st.info("Historical VVIX data unavailable")
    
    with tab3:
        st.markdown("**HY-IG Credit Spread - Historical Trend (5 Years)**")
        spread_data = market_data['sentiment']['hy_ig_historical']
        if not spread_data.empty:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=spread_data['date'],
                y=spread_data['value'],
                mode='lines',
                name='HY-IG Spread',
                line=dict(color='#95A5A6', width=2),
                fill='tozeroy',
                fillcolor='rgba(149, 165, 166, 0.1)'
            ))
            
            # Add reference lines
            fig.add_hline(y=3.0, line_dash="dash", line_color="green", 
                         annotation_text="Healthy (3%)")
            fig.add_hline(y=5.0, line_dash="dash", line_color="red", 
                         annotation_text="Stress (5%)")
            
            fig.update_layout(
                xaxis_title='Date',
                yaxis_title='Spread (%)',
                hovermode='x unified',
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            st.caption("📊 Data Source: [ICE BofA High Yield & Investment Grade via FRED](https://fred.stlouisfed.org)")
        else:
            st.info("Historical credit spread data unavailable")
    
    st.divider()
    
    st.subheader("💸 ETF Flows - Major Indexes")
    
    st.caption("Track money flows into/out of major index ETFs (30-day trend)")
    
    etf_flows = market_data['sentiment']['etf_flows'].copy()
    if not etf_flows.empty:
        # Calculate 5-day moving averages for smoother visualization
        etf_flows['SPY_MA'] = etf_flows['SPY'].rolling(window=5).mean()
        etf_flows['QQQ_MA'] = etf_flows['QQQ'].rolling(window=5).mean()
        etf_flows['IWM_MA'] = etf_flows['IWM'].rolling(window=5).mean()
        etf_flows['TLT_MA'] = etf_flows['TLT'].rolling(window=5).mean()
        
        # Current flow metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            spy_avg = etf_flows['SPY'].tail(5).mean()
            spy_color = "🟢" if spy_avg > 0.5 else "🟡" if spy_avg > -0.5 else "🔴"
            st.metric("SPY (S&P 500)", f"{spy_avg:.2f}B", help="5-day avg flow in billions")
            st.write(f"{spy_color} {'Inflows' if spy_avg > 0 else 'Outflows'}")
        
        with col2:
            qqq_avg = etf_flows['QQQ'].tail(5).mean()
            qqq_color = "🟢" if qqq_avg > 0.5 else "🟡" if qqq_avg > -0.5 else "🔴"
            st.metric("QQQ (Nasdaq)", f"{qqq_avg:.2f}B", help="5-day avg flow in billions")
            st.write(f"{qqq_color} {'Inflows' if qqq_avg > 0 else 'Outflows'}")
        
        with col3:
            iwm_avg = etf_flows['IWM'].tail(5).mean()
            iwm_color = "🟢" if iwm_avg > 0.5 else "🟡" if iwm_avg > -0.5 else "🔴"
            st.metric("IWM (Russell 2000)", f"{iwm_avg:.2f}B", help="5-day avg flow in billions")
            st.write(f"{iwm_color} {'Inflows' if iwm_avg > 0 else 'Outflows'}")
        
        with col4:
            tlt_avg = etf_flows['TLT'].tail(5).mean()
            tlt_color = "🟢" if tlt_avg > 0.5 else "🟡" if tlt_avg > -0.5 else "🔴"
            st.metric("TLT (Bonds)", f"{tlt_avg:.2f}B", help="5-day avg flow in billions")
            st.write(f"{tlt_color} {'Inflows' if tlt_avg > 0 else 'Outflows'}")
        
        # Flow chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=etf_flows['date'], y=etf_flows['SPY_MA'],
            mode='lines', name='SPY', line=dict(color='#1f77b4', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=etf_flows['date'], y=etf_flows['QQQ_MA'],
            mode='lines', name='QQQ', line=dict(color='#ff7f0e', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=etf_flows['date'], y=etf_flows['IWM_MA'],
            mode='lines', name='IWM', line=dict(color='#2ca02c', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=etf_flows['date'], y=etf_flows['TLT_MA'],
            mode='lines', name='TLT', line=dict(color='#d62728', width=2)
        ))
        
        fig.add_hline(y=0, line_dash="solid", line_color="gray", line_width=1)
        
        fig.update_layout(
            title='ETF Flows - 5-Day Moving Average (Billions $)',
            xaxis_title='Date',
            yaxis_title='Flow (Billions $)',
            hovermode='x unified',
            height=400,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.caption("💡 Note: ETF flow data is estimated based on volume patterns. For precise flow data, subscription services are required.")
    else:
        st.info("ETF flow data unavailable")
    
    st.divider()
    
    st.subheader("📊 AAII Sentiment Survey")
    
    st.caption("Retail investor sentiment - % Bullish, Bearish, and Neutral (Updated Weekly)")
    
    aaii = market_data['sentiment']['aaii']
    
    # Current sentiment breakdown
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**Current Sentiment**")
        st.metric("Bullish %", f"{aaii['bullish']:.1f}%")
        st.metric("Neutral %", f"{aaii['neutral']:.1f}%")
        st.metric("Bearish %", f"{aaii['bearish']:.1f}%")
        
        # Bull-Bear Spread
        spread = aaii['bull_bear_spread']
        spread_color = "🟢" if spread > 10 else "🟡" if spread > -10 else "🔴"
        st.metric("Bull-Bear Spread", f"{spread:.1f}%")
        interpretation = "Bullish" if spread > 10 else "Neutral" if spread > -10 else "Bearish"
        st.write(f"{spread_color} {interpretation}")
    
    with col2:
        # Pie chart of current sentiment
        fig = go.Figure(data=[go.Pie(
            labels=['Bullish', 'Neutral', 'Bearish'],
            values=[aaii['bullish'], aaii['neutral'], aaii['bearish']],
            marker=dict(colors=['#2ecc71', '#95a5a6', '#e74c3c']),
            hole=0.4
        )])
        
        fig.update_layout(
            title='Retail Investor Sentiment Breakdown',
            height=300,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Historical AAII chart
    aaii_hist = market_data['sentiment']['aaii_historical']
    if not aaii_hist.empty:
        st.markdown("**Historical Sentiment Trend (52 Weeks)**")
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=aaii_hist['date'], y=aaii_hist['bullish'],
            mode='lines', name='Bullish %', line=dict(color='#2ecc71', width=2),
            fill='tonexty', fillcolor='rgba(46, 204, 113, 0.1)'
        ))
        fig.add_trace(go.Scatter(
            x=aaii_hist['date'], y=aaii_hist['neutral'],
            mode='lines', name='Neutral %', line=dict(color='#95a5a6', width=2)
        ))
        fig.add_trace(go.Scatter(
            x=aaii_hist['date'], y=aaii_hist['bearish'],
            mode='lines', name='Bearish %', line=dict(color='#e74c3c', width=2),
            fill='tonexty', fillcolor='rgba(231, 76, 60, 0.1)'
        ))
        
        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Percentage (%)',
            hovermode='x unified',
            height=400,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.caption("📊 Data Source: [AAII Sentiment Survey](https://www.aaii.com/sentimentsurvey) | 💡 Note: Using sample data for demonstration. Real AAII data requires subscription.")
    else:
        st.info("Historical AAII data unavailable")
    
    st.divider()
    
    st.subheader("📈 Detailed Sector Charts")
    
    selected_sector = st.selectbox(
        "Select sector to view detailed chart:",
        list(market_data['sectors'].keys())
    )
    
    if selected_sector:
        if not market_data['sectors'][selected_sector]['data'].empty:
            sector_data = market_data['sectors'][selected_sector]['data']
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=sector_data.index,
                y=sector_data['Close'],
                mode='lines',
                name=selected_sector,
                line=dict(width=2)
            ))
            
            fig.update_layout(
                title=f'{selected_sector} Price History',
                xaxis_title='Date',
                yaxis_title='Price ($)',
                hovermode='x unified',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            st.caption("📊 Data Source: [Yahoo Finance - Historical Prices](https://finance.yahoo.com)")
        else:
            st.info(f"📊 No historical data available for {selected_sector}. Please try again later or select a different sector.")


def _render_fear_greed_index(economic_data):
    st.header("😱 Fear & Greed Index")
    st.warning("📚 **Educational Purposes Only**: This is a calculated approximation of CNN's Fear & Greed Index methodology using publicly available data. Results may differ significantly from [CNN's Official Index](https://www.cnn.com/markets/fear-and-greed) due to normalization ranges, data sources, and timing. Use CNN's official index for investment decisions.")
    
    with st.expander("ℹ️ Why does this differ from CNN's official index?", expanded=False):
        st.markdown("""
        **Our calculated index is an educational approximation.** Here's why it differs:
        
        1. **Normalization Ranges**: CNN doesn't publish exact formulas. We estimate historical ranges for each indicator.
        2. **Data Sources**: CNN uses proprietary real-time feeds; we use Yahoo Finance (15-min delayed) and FRED (daily).
        3. **Market Breadth**: CNN uses the proprietary McClellan Volume Summation Index; we use simplified advance/decline data.
        4. **Historical Baselines**: CNN normalizes against their full historical database; we calculate on-the-fly.
        5. **Update Timing**: CNN updates throughout the day; our data has various delays.
        
        **For investment decisions, always reference CNN's official index.**  
        **This tool is for understanding the methodology and learning how sentiment indicators work.**
        """)
    
    # Calculate Fear & Greed Index using real market data
    calculator = FearGreedCalculator()
    fear_greed_calc = calculator.calculate(economic_data)
    fear_greed = fear_greed_calc
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        score = fear_greed['score']
        rating = fear_greed['rating'].title()
        
        if score < 25:
            color = "#d32f2f"
            emoji = "😱"
            description = "Extreme Fear"
        elif score < 45:
            color = "#f57c00"
            emoji = "😰"
            description = "Fear"
        elif score < 55:
            color = "#fdd835"
            emoji = "😐"
            description = "Neutral"
        elif score < 75:
            color = "#7cb342"
            emoji = "😃"
            description = "Greed"
        else:
            color = "#388e3c"
            emoji = "🤑"
            description = "Extreme Greed"
        
        st.markdown(f"<h1 style='text-align: center; font-size: 80px;'>{emoji}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center; color: {color};'>{score:.1f}</h3>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align: center; color: {color}; font-weight: bold;'>{description}</p>", unsafe_allow_html=True)
        
        if fear_greed['previous_week'] is not None:
            week_change = score - fear_greed['previous_week']
            st.metric("vs Last Week", f"{week_change:+.1f}", delta_color="off")
    
    with col2:
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Market Sentiment", 'font': {'size': 20}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkgray"},
                'bar': {'color': color, 'thickness': 0.75},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 25], 'color': '#ffcdd2'},
                    {'range': [25, 45], 'color': '#ffe0b2'},
                    {'range': [45, 55], 'color': '#fff9c4'},
                    {'range': [55, 75], 'color': '#dcedc8'},
                    {'range': [75, 100], 'color': '#c8e6c9'}
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 4},
                    'thickness': 0.75,
                    'value': score
                }
            }
        ))
        
        fig_gauge.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=50, b=20),
            font={'color': "darkgray", 'family': "Arial"}
        )
        
        st.plotly_chart(fig_gauge, use_container_width=True)
        st.caption("📊 Data Source: Calculated using real market data - Compare with [CNN's Official Index](https://www.cnn.com/markets/fear-and-greed)")
        
        st.markdown("""
        **What is this?** The Fear & Greed Index measures market sentiment on a 0-100 scale.
        Extreme fear (low values) may indicate buying opportunities, while extreme greed (high values) may signal overheated markets.
        """)
    
    # Display all 7 indicators with interactive details
    st.subheader("📋 The 7 Indicators (Click to Expand)")
    st.caption("Each indicator contributes equally (1/7th) to the composite score. Click any indicator to learn how it's calculated.")
    
    indicator_details = calculator.get_indicator_details()
    
    indicators_list = [
        ('market_momentum', '📈', 'S&P 500 position relative to its 125-day moving average. Above = Greed, Below = Fear.'),
        ('price_strength', '💪', 'Ratio of NYSE stocks at 52-week highs vs lows. More highs = Greed, More lows = Fear.'),
        ('price_breadth', '📊', 'Market advance/decline trend. Rising breadth = Greed, Falling breadth = Fear.'),
        ('put_call_options', '📉', 'Put/Call ratio (5-day avg). High ratio (>1) = Fear, Low ratio (<1) = Greed.'),
        ('market_volatility', '📉', 'VIX volatility index. Low VIX = Greed, High VIX = Fear.'),
        ('safe_haven_demand', '🏦', 'Stocks vs bonds performance (20-day). Stocks outperforming = Greed, Bonds outperforming = Fear.'),
        ('junk_bond_demand', '💰', 'High-yield credit spread. Narrow spread = Greed, Wide spread = Fear.')
    ]
    
    # Create two columns for compact display
    col1, col2 = st.columns(2)
    
    for idx, (key, emoji, explanation) in enumerate(indicators_list):
        indicator = indicator_details[key]
        col = col1 if idx % 2 == 0 else col2
        
        with col:
            score = indicator['score']
            
            # Color based on score
            if score < 25:
                color = "#d32f2f"
                sentiment_icon = "😱"
            elif score < 45:
                color = "#f57c00"
                sentiment_icon = "😰"
            elif score < 55:
                color = "#fdd835"
                sentiment_icon = "😐"
            elif score < 75:
                color = "#7cb342"
                sentiment_icon = "😃"
            else:
                color = "#388e3c"
                sentiment_icon = "🤑"
            
            # Create expandable indicator card
            with st.expander(f"{emoji} {indicator['name']}: **{score:.1f}** {sentiment_icon}", expanded=False):
                st.markdown(f"**{indicator['description']}**")
                st.markdown(f"**Signal**: {indicator['signal']}")
                st.markdown(f"**How it works**: {explanation}")
                
                # Visual score bar
                st.progress(score / 100)
                
                score_col1, score_col2, score_col3 = st.columns(3)
                with score_col1:
                    st.caption("😱 Fear")
                with score_col2:
                    st.caption(f"**{score:.1f}**")
                with score_col3:
                    st.caption("Greed 🤑")


def _render_historical_backtesting(economic_data):
    st.header("⏮️ Historical Backtesting")
    
    # Show cross-page context if available
    if st.session_state.cycle_phase:
        st.success(f"🔗 **Connected Context:** Using {st.session_state.cycle_phase} phase from Business Cycle page (Confidence: {st.session_state.cycle_confidence}%)")
    
    analyzer = BusinessCycleAnalyzer()
    cycle_analysis = analyzer.analyze_cycle_phase(
        economic_data['gdp'],
        economic_data['unemployment'],
        economic_data['inflation']
    )
    
    # Navigation hint
    st.info(f"📍 **Current Cycle:** {cycle_analysis['phase']} | 💡 See [Business Cycle Analysis](#) for phase details | [Portfolio Positioning](#) for allocation insights")
    st.caption("⚠️ Historical patterns are educational references, not predictions. Past performance does not guarantee future results.")
    
    backtester = HistoricalBacktester()
    
    st.subheader("🔍 Current vs. Historical Cycles")
    
    similar_cycles = backtester.find_similar_cycles(
        cycle_analysis['gdp_growth'],
        cycle_analysis['unemployment_current'],
        cycle_analysis['inflation_current'],
        cycle_analysis['phase']
    )
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("**Current Economic Conditions**")
        st.metric("Business Cycle Phase", cycle_analysis['phase'])
        st.metric("GDP Growth", f"{cycle_analysis['gdp_growth']:.2f}%")
        st.metric("Unemployment", f"{cycle_analysis['unemployment_current']:.2f}%")
        st.metric("Inflation", f"{cycle_analysis['inflation_current']:.2f}%")
    
    with col2:
        st.markdown("**Most Similar Historical Cycles**")
        for i, cycle in enumerate(similar_cycles, 1):
            with st.expander(f"{i}. {cycle['name']} ({cycle['period']}) - {cycle['similarity_score']:.0f}% similar"):
                st.write(f"**Phase:** {cycle['phase']}")
                st.write(f"**Duration:** {cycle['duration_months']} months")
                st.write(f"**S&P 500 Return:** {cycle['sp500_return']:.1f}%")
                st.write(f"**GDP Growth:** {cycle['gdp_growth']:.1f}%")
                st.write(f"**Unemployment:** {cycle['unemployment']:.1f}%")
                st.write(f"**Inflation:** {cycle['inflation']:.1f}%")
                st.write(f"**Best Sectors:** {', '.join(cycle['best_sectors'][:3])}")
                st.write(f"**Key Triggers:** {', '.join(cycle['triggers'])}")
    
    st.divider()
    
    st.subheader("📊 Performance Analysis by Cycle Phase")
    
    stats = backtester.get_cycle_performance_stats(cycle_analysis['phase'])
    
    if stats:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Historical Precedents", f"{stats['count']} cycles")
            st.metric("Avg Duration", f"{stats['avg_duration']:.0f} months")
        
        with col2:
            st.metric("Avg S&P 500 Return", f"{stats['avg_sp500_return']:.1f}%")
            st.metric("Return Range", f"{stats['min_sp500_return']:.1f}% to {stats['max_sp500_return']:.1f}%")
        
        with col3:
            st.metric("Avg GDP Growth", f"{stats['avg_gdp_growth']:.1f}%")
            st.metric("Avg Unemployment", f"{stats['avg_unemployment']:.1f}%")
    
    st.divider()
    
    st.subheader("🎯 Sector Performance in Similar Cycles")
    
    sector_perf = backtester.get_sector_performance_in_phase(cycle_analysis['phase'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Best Performing Sectors**")
        best_sectors_df = pd.DataFrame([
            {'Sector': sector, 'Frequency': count}
            for sector, count in sector_perf['best_sectors'].items()
        ])
        
        if not best_sectors_df.empty:
            fig = go.Figure(data=[
                go.Bar(
                    x=best_sectors_df['Frequency'],
                    y=best_sectors_df['Sector'],
                    orientation='h',
                    marker_color='green'
                )
            ])
            fig.update_layout(title='Frequency as Top Performer', height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("**Worst Performing Sectors**")
        worst_sectors_df = pd.DataFrame([
            {'Sector': sector, 'Frequency': count}
            for sector, count in sector_perf['worst_sectors'].items()
        ])
        
        if not worst_sectors_df.empty:
            fig = go.Figure(data=[
                go.Bar(
                    x=worst_sectors_df['Frequency'],
                    y=worst_sectors_df['Sector'],
                    orientation='h',
                    marker_color='red'
                )
            ])
            fig.update_layout(title='Frequency as Worst Performer', height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    st.subheader("📈 All Historical Cycles")
    
    all_cycles = backtester.historical_cycles
    cycles_df = pd.DataFrame([
        {
            'Cycle': c['name'],
            'Period': c['period'],
            'Phase': c['phase'],
            'Duration': f"{c['duration_months']}m",
            'S&P 500 Return': f"{c['sp500_return']:.1f}%",
            'GDP Growth': f"{c['gdp_growth']:.1f}%",
            'Unemployment': f"{c['unemployment']:.1f}%",
            'Inflation': f"{c['inflation']:.1f}%"
        }
        for c in all_cycles
    ])
    
    st.dataframe(cycles_df, use_container_width=True, hide_index=True)
    
    fig = px.scatter(
        cycles_df,
        x='GDP Growth',
        y='S&P 500 Return',
        size=[abs(float(c['S&P 500 Return'][:-1])) for c in cycles_df.to_dict('records')],
        color='Phase',
        hover_data=['Cycle', 'Period'],
        title='GDP Growth vs S&P 500 Returns Across Historical Cycles'
    )
    st.plotly_chart(fig, use_container_width=True)
    st.caption("📊 Data Source: Historical Business Cycle Database (2001-2023)")
    
    expected = backtester.get_expected_outcomes(cycle_analysis['phase'])
    if expected:
        st.info(f"""
**Historical Patterns for {cycle_analysis['phase']} Phase:**
- Typical Duration: {expected['expected_duration_range']}
- Historical S&P 500 Return: {expected['expected_sp500_return']} (Range: {expected['return_range']})
- Volatility: {expected['volatility_level']}
- Based on {expected['historical_precedents']} historical precedents

*Note: Current cycle may differ due to unique economic conditions or external events.*
        """)


def _render_portfolio_positioning(economic_data):
    st.header("💼 Portfolio Positioning Insights")
    
    # Show cross-page context if available
    if st.session_state.cycle_phase:
        st.success(f"🔗 **Connected Context:** Using {st.session_state.cycle_phase} phase from Business Cycle page (Confidence: {st.session_state.cycle_confidence}%)")
    
    analyzer = BusinessCycleAnalyzer()
    cycle_analysis = analyzer.analyze_cycle_phase(
        economic_data['gdp'],
        economic_data['unemployment'],
        economic_data['inflation']
    )
    
    # Navigation hint
    st.info(f"📍 **Current Cycle:** {cycle_analysis['phase']} | 💡 See [Business Cycle Analysis](#) for phase details | [Historical Backtesting](#) for past patterns")
    st.caption("⚠️ These are historical allocation patterns for educational purposes, not personalized investment recommendations. Consult a financial advisor for investment decisions.")
    
    positioner = PortfolioPositioner()
    
    st.subheader("🎯 Historical Asset Allocation Patterns")
    
    # Use session state for risk profile, but allow user to change it
    default_index = ["Conservative", "Moderate", "Aggressive"].index(st.session_state.risk_profile)
    risk_profile = st.selectbox(
        "Select your risk profile:",
        ["Conservative", "Moderate", "Aggressive"],
        index=default_index
    )
    
    # Save selection to session state
    st.session_state.risk_profile = risk_profile
    
    recommendation = positioner.get_recommended_allocation(cycle_analysis['phase'], risk_profile)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = go.Figure(data=[go.Pie(
            labels=list(recommendation['asset_allocation'].keys()),
            values=list(recommendation['asset_allocation'].values()),
            hole=0.4,
            marker=dict(colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
        )])
        fig.update_layout(title=f'Typical Allocation Pattern: {cycle_analysis["phase"]} Phase ({risk_profile} Profile)')
        st.plotly_chart(fig, use_container_width=True)
        st.caption("📊 Based on historical cycle-based allocation patterns")
    
    with col2:
        st.markdown("**Typical Allocation**")
        for asset, allocation in recommendation['asset_allocation'].items():
            st.metric(asset.capitalize(), f"{allocation:.1f}%")
        
        st.markdown(f"**Risk Profile:** {risk_profile}")
        st.caption(recommendation['risk_description'])
    
    st.info(f"**Historical Pattern:** {recommendation['rationale'].replace('Recommended', 'Historically typical').replace('should', 'tended to')}")
    
    st.divider()
    
    st.subheader("🏢 Sector Allocation")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        sector_df = pd.DataFrame([
            {'Sector': sector, 'Allocation': alloc}
            for sector, alloc in recommendation['sector_allocation'].items()
        ]).sort_values('Allocation', ascending=True)
        
        fig = go.Figure(go.Bar(
            x=sector_df['Allocation'],
            y=sector_df['Sector'],
            orientation='h',
            marker=dict(
                color=sector_df['Allocation'],
                colorscale='Viridis',
                showscale=False
            )
        ))
        fig.update_layout(title='Historical Sector Weight Patterns', xaxis_title='Allocation (%)', height=400)
        st.plotly_chart(fig, use_container_width=True)
        st.caption("📊 Based on historical cycle-based sector patterns")
    
    with col2:
        st.markdown("**Top Sectors**")
        top_sectors = sorted(recommendation['sector_allocation'].items(), key=lambda x: x[1], reverse=True)[:5]
        for sector, allocation in top_sectors:
            st.write(f"**{sector}:** {allocation}%")
    
    st.divider()
    
    st.subheader("📊 Portfolio Metrics")
    
    metrics = positioner.calculate_portfolio_metrics(
        recommendation['asset_allocation'],
        cycle_analysis['phase']
    )
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Expected Annual Return", f"{metrics['expected_return']:.1f}%")
    
    with col2:
        st.metric("Portfolio Volatility", f"{metrics['volatility']:.1f}%")
    
    with col3:
        st.metric("Sharpe Ratio", f"{metrics['sharpe_ratio']:.2f}")
    
    st.caption("⚠️ Note: These are estimated metrics based on historical averages for the current cycle phase, not guarantees or predictions")
    
    st.divider()
    
    st.subheader("🔄 Portfolio Comparison Tool")
    
    st.markdown("Compare your current portfolio allocation with historical cycle patterns:")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        current_equities = st.number_input("Current Equities %", 0.0, 100.0, 60.0, 1.0)
    with col2:
        current_bonds = st.number_input("Current Bonds %", 0.0, 100.0, 30.0, 1.0)
    with col3:
        current_commodities = st.number_input("Current Commodities %", 0.0, 100.0, 5.0, 1.0)
    with col4:
        current_cash = st.number_input("Current Cash %", 0.0, 100.0, 5.0, 1.0)
    
    current_allocation = {
        'equities': current_equities,
        'bonds': current_bonds,
        'commodities': current_commodities,
        'cash': current_cash
    }
    
    total_current = sum(current_allocation.values())
    
    if abs(total_current - 100) > 0.1:
        st.warning(f"Current allocation totals {total_current:.1f}%. Please adjust to 100%.")
    else:
        suggestions = positioner.get_rebalancing_suggestions(current_allocation, recommendation)
        
        if suggestions:
            st.markdown("**Differences from Historical Pattern:**")
            
            suggestions_df = pd.DataFrame(suggestions)
            
            for idx, row in suggestions_df.iterrows():
                priority_color = "🔴" if row['priority'] == "High" else "🟡" if row['priority'] == "Medium" else "🟢"
                action_text = row['action'].replace("Increase", "Below historical").replace("Decrease", "Above historical")
                st.write(f"{priority_color} **{action_text} {row['asset_class']}:** Current {row['current']:.1f}% vs Historical {row['target']:.1f}% (diff: {abs(row['change']):.1f}%)")
        else:
            st.success("✅ Your portfolio closely matches the historical pattern for this cycle phase!")
    
    comparison = positioner.compare_allocations(
        current_allocation,
        recommendation['asset_allocation'],
        'Current',
        'Target'
    )
    
    comparison_df = pd.DataFrame(comparison).drop('diff_numeric', axis=1)
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    st.subheader("💡 Historical Tactical Patterns")
    
    economic_indicators = {
        'gdp_growth': cycle_analysis['gdp_growth'],
        'inflation': cycle_analysis['inflation_current'],
        'unemployment_trend': cycle_analysis['unemployment_trend']
    }
    
    tactical_tilts = positioner.get_tactical_tilts(cycle_analysis['phase'], economic_indicators)
    
    if tactical_tilts:
        for tilt in tactical_tilts:
            insight = tilt['suggestion'].replace("Consider", "Historically saw").replace("overweight", "overweighting").replace("underweight", "underweighting")
            with st.expander(f"💡 {insight}"):
                rationale = tilt['rationale'].replace("should", "tended to").replace("recommended", "historically favored")
                st.write(f"**Historical Pattern:** {rationale}")
    else:
        st.info("No specific tactical patterns identified for current conditions. Historical data suggests maintaining balanced allocation.")


def _render_sector_watchlist(economic_data, market_data):
    st.header("⭐ Sector Watchlist & Historical Patterns")
    
    # Show cross-page context if available
    context_parts = []
    if st.session_state.cycle_phase:
        context_parts.append(f"{st.session_state.cycle_phase} phase (Confidence: {st.session_state.cycle_confidence}%)")
    if st.session_state.risk_profile:
        context_parts.append(f"{st.session_state.risk_profile} risk profile")
    
    if context_parts:
        st.success(f"🔗 **Connected Context:** Using {' | '.join(context_parts)} from other pages")
    
    analyzer = BusinessCycleAnalyzer()
    cycle_analysis = analyzer.analyze_cycle_phase(
        economic_data['gdp'],
        economic_data['unemployment'],
        economic_data['inflation']
    )
    
    # Navigation hint
    st.info(f"📍 **Current Cycle:** {cycle_analysis['phase']} | 💡 See [Business Cycle Analysis](#) for phase details | [Portfolio Positioning](#) for allocation patterns")
    st.caption("⚠️ Historical sector patterns are educational references, not investment recommendations. Sector performance varies significantly across cycles.")
    
    watchlist_mgr = WatchlistManager()
    
    if 'watchlists' not in st.session_state:
        st.session_state.watchlists = []
    
    st.subheader(f"📊 Historical Sector Patterns for {cycle_analysis['phase']} Phase")
    
    signals = watchlist_mgr.get_rotation_signals(cycle_analysis['phase'])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**🟢 Historically Outperformed**")
        for sector in signals['rotate_into']:
            perf = market_data['sectors'].get(sector, {}).get('performance', 0)
            st.write(f"• {sector} ({perf:+.1f}%)")
    
    with col2:
        st.markdown("**🔴 Historically Underperformed**")
        for sector in signals['rotate_out_of']:
            perf = market_data['sectors'].get(sector, {}).get('performance', 0)
            st.write(f"• {sector} ({perf:+.1f}%)")
    
    with col3:
        st.markdown("**🟡 Historically Mixed**")
        for sector in signals['hold']:
            perf = market_data['sectors'].get(sector, {}).get('performance', 0)
            st.write(f"• {sector} ({perf:+.1f}%)")
    
    st.divider()
    
    st.subheader("📊 Sector Signals Dashboard")
    
    all_sectors = list(market_data['sectors'].keys())
    
    sector_analyses = []
    for sector in all_sectors:
        perf = market_data['sectors'].get(sector, {}).get('performance', 0)
        analysis = watchlist_mgr.analyze_sector(sector, perf, cycle_analysis['phase'])
        sector_analyses.append(analysis)
    
    signals_df = pd.DataFrame(sector_analyses)
    signals_df = signals_df.sort_values('performance', ascending=False)
    
    display_df = pd.DataFrame({
        'Signal': [f"{row['color']} {row['signal']}" for _, row in signals_df.iterrows()],
        'Sector': signals_df['sector'].values,
        'Performance': [f"{p:.1f}%" for p in signals_df['performance'].values],
        'Trend': signals_df['trend'].values,
        'Beta': signals_df['beta'].values,
        'Cyclicality': signals_df['cyclicality'].values
    })
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    st.subheader("⭐ Create Custom Watchlist")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        watchlist_name = st.text_input("Watchlist Name", placeholder="e.g., My Growth Portfolio")
        
        selected_sectors = st.multiselect(
            "Select sectors to track:",
            all_sectors,
            default=[]
        )
        
        if selected_sectors:
            diversification = watchlist_mgr.get_diversification_score(selected_sectors)
            st.metric("Diversification Score", f"{diversification:.0f}/100")
            
            if diversification < 40:
                st.warning("Low diversification - consider adding uncorrelated sectors")
            elif diversification > 70:
                st.success("Good diversification across selected sectors")
            
            if st.button("Add to Watchlist"):
                if watchlist_name:
                    new_watchlist = watchlist_mgr.create_watchlist(
                        watchlist_name,
                        selected_sectors,
                        cycle_analysis['phase']
                    )
                    st.session_state.watchlists.append(new_watchlist)
                    st.success(f"✅ Watchlist '{watchlist_name}' created with {len(selected_sectors)} sectors!")
                else:
                    st.error("Please enter a watchlist name")
    
    with col2:
        if selected_sectors:
            st.markdown("**Selected Sectors:**")
            for sector in selected_sectors:
                analysis = watchlist_mgr.analyze_sector(
                    sector,
                    market_data['sectors'].get(sector, {}).get('performance', 0),
                    cycle_analysis['phase']
                )
                st.write(f"{analysis['color']} {sector}: {analysis['signal']}")
    
    if st.session_state.watchlists:
        st.divider()
        
        st.subheader("📋 My Watchlists")
        
        for idx, watchlist in enumerate(st.session_state.watchlists):
            with st.expander(f"⭐ {watchlist['name']} ({len(watchlist['sectors'])} sectors)"):
                st.write(f"**Created:** {watchlist['created_at']}")
                st.write(f"**Cycle Phase:** {watchlist['cycle_phase']}")
                
                summary = watchlist_mgr.get_watchlist_summary(
                    watchlist['sectors'],
                    market_data['sectors'],
                    cycle_analysis['phase']
                )
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Avg Performance", f"{summary['avg_performance']:.1f}%")
                with col2:
                    st.metric("Buy Signals", summary['buy_signals'], delta_color="normal")
                with col3:
                    st.metric("Sell Signals", summary['sell_signals'], delta_color="inverse")
                with col4:
                    st.metric("Cycle Alignment", f"{summary['cycle_alignment']:.0f}%")
                
                st.markdown("**Sectors in Watchlist:**")
                for sector in watchlist['sectors']:
                    perf = market_data['sectors'].get(sector, {}).get('performance', 0)
                    analysis = watchlist_mgr.analyze_sector(sector, perf, cycle_analysis['phase'])
                    st.write(f"{analysis['color']} **{sector}**: {analysis['signal']} ({perf:+.1f}%)")
                
                alerts = watchlist_mgr.generate_alerts(
                    watchlist['sectors'],
                    market_data['sectors'],
                    cycle_analysis['phase']
                )
                
                if alerts:
                    st.markdown("**🔔 Active Alerts:**")
                    for alert in alerts:
                        alert_icon = "🔴" if alert['priority'] == 'High' else "🟡"
                        st.warning(f"{alert_icon} **{alert['type']}** - {alert['message']}\n\n*Action: {alert['action']}*")
                
                if st.button(f"Remove Watchlist", key=f"remove_{idx}"):
                    st.session_state.watchlists.pop(idx)
                    st.rerun()
    
    st.divider()
    
    st.subheader("📈 Sector Momentum & Characteristics")
    
    momentum = watchlist_mgr.sector_momentum_indicators
    
    momentum_df = pd.DataFrame([
        {
            'Sector': sector,
            'Beta': data['beta'],
            'Cyclicality': data['cyclicality'],
            'Performance': market_data['sectors'].get(sector, {}).get('performance', 0)
        }
        for sector, data in momentum.items()
    ]).sort_values('Beta', ascending=False)
    
    fig = px.scatter(
        momentum_df,
        x='Beta',
        y='Performance',
        size=[abs(p) + 5 for p in momentum_df['Performance']],
        color='Cyclicality',
        hover_data=['Sector'],
        title='Sector Risk vs Performance',
        labels={'Beta': 'Market Sensitivity (Beta)', 'Performance': '1-Year Return (%)'}
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.caption("📊 Data Source: Sector Analysis Model + [Yahoo Finance](https://finance.yahoo.com)")


def show_resources():
    st.title("📚 Resources & Further Reading")
    
    st.markdown("""
    Expand your understanding of macroeconomic analysis, business cycles, and market indicators with these curated resources.
    """)
    
    st.divider()
    
    # Official Data Sources
    st.subheader("📊 Official Data Sources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Federal Reserve Economic Data (FRED)**
        - [FRED Main Portal](https://fred.stlouisfed.org/) - Complete economic database
        - [GDP](https://fred.stlouisfed.org/series/GDP) - Gross Domestic Product
        - [CPI](https://fred.stlouisfed.org/series/CPIAUCSL) - Consumer Price Index
        - [Unemployment](https://fred.stlouisfed.org/series/UNRATE) - Unemployment Rate
        - [Federal Funds Rate](https://fred.stlouisfed.org/series/FEDFUNDS)
        
        **Bureau of Labor Statistics (BLS)**
        - [BLS Home](https://www.bls.gov/) - Employment & inflation data
        - [Employment Report](https://www.bls.gov/news.release/empsit.toc.htm) - Monthly jobs data
        - [Economic Calendar](https://www.bls.gov/schedule/news_release/index.htm) - Release schedule
        """)
    
    with col2:
        st.markdown("""
        **Federal Reserve Resources**
        - [Federal Reserve](https://www.federalreserve.gov/) - Central bank policy
        - [FOMC Calendar](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm) - Meeting dates
        - [Economic Projections](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm) - Dot plot & forecasts
        - [Beige Book](https://www.federalreserve.gov/monetarypolicy/beigebook/default.htm) - Regional conditions
        
        **Market Data**
        - [CBOE VIX](https://www.cboe.com/tradable_products/vix/) - Volatility index
        - [Yahoo Finance](https://finance.yahoo.com/) - Market data & news
        - [ISM Manufacturing](https://www.ismworld.org/) - PMI reports
        """)
    
    st.divider()
    
    # Academic & Educational Resources
    st.subheader("📖 Academic & Educational Resources")
    
    st.markdown("""
    **Business Cycle Theory**
    - [NBER Business Cycle Dating](https://www.nber.org/research/business-cycle-dating) - Official US cycle dates
    - [Business Cycles and Depressions (Britannica)](https://www.britannica.com/topic/business-cycle) - Foundational concepts
    - [IMF Economic Outlook](https://www.imf.org/en/Publications/WEO) - Global economic analysis
    
    **Investment & Portfolio Theory**
    - [CFA Institute Resources](https://www.cfainstitute.org/en/research) - Professional investment education
    - [Vanguard Research](https://advisors.vanguard.com/insights/research) - Asset allocation research
    - [BlackRock Investment Institute](https://www.blackrock.com/corporate/insights/blackrock-investment-institute) - Market commentary
    
    **Financial Stability & Risk**
    - [BIS Papers](https://www.bis.org/publ/index.htm) - Central banking research
    - [OECD Economic Outlook](https://www.oecd.org/economic-outlook/) - Global economic forecasts
    - [Financial Stability Board](https://www.fsb.org/) - Global financial stability
    """)
    
    st.divider()
    
    # Policy & Governance Resources
    st.subheader("🏛️ Policy & AI Governance Resources")
    
    st.markdown("""
    **AI Policy & Ethics**
    - [Imperial AI Policy Lab](https://www.imperial.ac.uk/) - AI governance research
    - [OECD AI Principles](https://oecd.ai/en/ai-principles) - International AI guidelines
    - [EU AI Act](https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai) - European AI regulation
    - [UK AI Safety Institute](https://www.aisi.gov.uk/) - AI safety research
    
    **Financial Regulation**
    - [SEC](https://www.sec.gov/) - Securities and Exchange Commission
    - [FCA (UK)](https://www.fca.org.uk/) - Financial Conduct Authority
    - [Basel Committee](https://www.bis.org/bcbs/) - Banking supervision standards
    
    **AI in Finance**
    - [Bank of England - Machine Learning](https://www.bankofengland.co.uk/research/research-themes/machine-learning) - Central bank ML research
    - [IMF - Fintech](https://www.imf.org/en/Topics/fintech-and-digital-currencies) - Digital finance policy
    """)
    
    st.divider()
    
    # Tools & Calculators
    st.subheader("🔧 Tools & Calculators")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Economic Tools**
        - [FRED Economic Calendar](https://www.stlouisfed.org/news-releases/economic-data-news-releases) - Upcoming releases
        - [Trading Economics](https://tradingeconomics.com/calendar) - Global economic calendar
        - [Investing.com Calendar](https://www.investing.com/economic-calendar/) - Real-time event tracker
        """)
    
    with col2:
        st.markdown("""
        **Financial Calculators**
        - [Portfolio Visualizer](https://www.portfoliovisualizer.com/) - Backtesting & analysis
        - [AAII Stock Screens](https://www.aaii.com/stock-screens) - Investment screens
        - [Fear & Greed Index (CNN)](https://edition.cnn.com/markets/fear-and-greed) - Market sentiment
        """)
    
    st.divider()
    
    # Books & Papers
    st.subheader("📚 Recommended Reading")
    
    st.markdown("""
    **Foundational Texts**
    - *"Business Cycles"* by Wesley Clair Mitchell - Classic cycle theory
    - *"A Monetary History of the United States"* by Friedman & Schwartz - Economic history
    - *"The General Theory"* by John Maynard Keynes - Macroeconomic foundations
    
    **Modern Analysis**
    - *"This Time Is Different"* by Reinhart & Rogoff - Financial crises patterns
    - *"The Only Game in Town"* by Mohamed El-Erian - Central banking era
    - *"Expected Returns"* by Antti Ilmanen - Asset class performance
    
    **AI & Technology**
    - *"Prediction Machines"* by Agrawal, Gans & Goldfarb - AI economics
    - *"The AI Economy"* by Roger Bootle - Economic transformation
    - *"Human Compatible"* by Stuart Russell - AI alignment & safety
    """)

def show_about():
    st.title("ℹ️ About MacroCycle AI Agent")
    
    # 1. What is MacroCycle AI Agent?
    st.markdown("""
    ## What is MacroCycle AI Agent?
    
    MacroCycle AI Agent is an **autonomous macro-economic intelligence assistant** that demonstrates the potential 
    of AI-driven economic analysis. It integrates multiple public data feeds (FRED, CBOE, SEC) to analyze liquidity 
    conditions, volatility measures, and key macroeconomic indicators in real-time.
    
    Built as a **prototype for the Imperial AI Policy Fellowship**, this tool showcases how AI agents can orchestrate 
    complex data pipelines and generate interpretable economic insights—while highlighting the critical need for 
    human oversight, FinOps discipline, and ethical guardrails in autonomous systems.
    """)
    
    st.divider()
    
    # 2. What does it do?
    st.subheader("🎯 What Does It Do?")
    
    st.markdown("""
    MacroCycle is an **autonomous AI agent** that continuously monitors the economy and responds to your questions. 
    Instead of manually searching for data, the agent does the work for you:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🤖 Automates Key Metrics**
        - Automatically fetches 50+ economic and market indicators from FRED, CBOE, and Yahoo Finance
        - Refreshes data every 30-60 minutes without manual intervention
        - Organizes metrics into 6 themed tabs (Business Cycle, Macro, Liquidity, Sentiment, Market Structure, Sectors)
        - Displays real-time dashboards with no user configuration needed
        
        **🧠 Infers & Analyzes**
        - Determines current business cycle phase (Expansion, Peak, Contraction, Trough) with confidence scoring
        - Identifies which leading indicators are signaling turning points
        - Compares current conditions to 7 historical cycles (2001-2023)
        - Calculates Fear & Greed Index and detects market regime shifts
        - Surfaces sector rotation patterns based on cycle phase
        """)
    
    with col2:
        st.markdown("""
        **💬 Natural Language Query**
        - Ask questions in plain English: *"What's the current VIX?"*, *"How does inflation compare to last year?"*
        - Agent autonomously fetches data, creates charts, and provides context
        - Conversational AI (GPT-5) with full access to economic context
        - Educational explanations framed as historical patterns
        
        **🔍 Self-Service Analysis**
        - Explore any metric without technical skills or API knowledge
        - Request custom comparisons: *"Show me GDP vs unemployment over 5 years"*
        - Navigate to relevant analysis pages through AI suggestions
        - Build custom sector watchlists and track diversification
        - No coding, no spreadsheets—just ask the agent
        """)
    
    st.divider()
    
    # 3. Who can use it and how?
    st.subheader("👥 Who Can Use It and How?")
    
    st.markdown("""
    **For Policymakers:**
    - Assess current economic phase and monitor leading indicators for policy signals
    - Track inflation, unemployment, and monetary policy stance
    - Use AI Research Agent for real-time economic Q&A
    - Monitor Economic Calendar for data releases informing policy decisions
    
    **For Academics & Students:**
    - Learn about business cycle theory through interactive analysis
    - Study 7 historical cycles (2001-2023) with real data
    - Use AI agent for educational insights about economic concepts
    - Explore sector rotation patterns and market dynamics
    
    **For Investors:**
    - Identify current business cycle phase for portfolio context
    - Review historical asset allocation patterns by cycle phase
    - Monitor market sentiment and risk indicators
    - Ask AI agent about specific metrics, sectors, or conditions
    """)
    
    st.divider()
    
    # 4. Created By
    st.subheader("👨‍💼 Created By")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Human Creator**
        
        **Bandhu Das FCCA**  
        [LinkedIn Profile](https://www.linkedin.com/in/ibpdas/)
        
        Concept, design, and oversight as part of the **Imperial AI Policy Fellowship**. Research interests 
        include AI in data management and data management in AI. Policy interests focus on green finance.
        """)
    
    with col2:
        st.markdown("""
        **AI Agents Collaboration**
        
        This project exemplifies multi-agent AI collaboration:
        
        **🏗️ Replit Agent (Claude 4.5 Sonnet)**  
        Primary builder - Architecture, code development, data pipeline design
        
        **🔍 Architect Agent (Claude Opus 4.1)**  
        Code review, strategic guidance, quality assurance
        
        **🧪 Testing Agent (Playwright)**  
        End-to-end UI/UX testing and validation
        
        **🤖 OpenAI GPT-5 Agent**  
        Embedded research assistant providing natural language insights
        """)
    
    st.divider()
    
    # 5. Data Sources
    st.subheader("📊 Data Sources")
    
    st.markdown("""
    MacroCycle integrates real-time data from trusted public sources:
    
    - **FRED (Federal Reserve Economic Data)**: GDP, CPI inflation, unemployment, interest rates, M2 money supply, NFCI
    - **CBOE (Chicago Board Options Exchange)**: VIX volatility index, VVIX, Put/Call ratio
    - **SEC & Yahoo Finance**: Sector ETFs, equity indices, asset class performance
    - **Custom Calculators**: Fear & Greed Index (CNN methodology), ISM PMI synthetic data
    - **Historical Database**: 7 major business cycles (2001-2023) with sector performance
    
    **Data Refresh**: Economic data (1hr cache), Market data (30min cache), AI responses (real-time)
    """)
    
    st.divider()
    
    # 6. Methodology & Data Quality
    st.subheader("🔬 Methodology & Data Quality")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Business Cycle Classification**
        - **Method**: Rule-based algorithm analyzing GDP growth, unemployment rate, and inflation
        - **Phases**: Expansion, Peak, Contraction, Trough (4-phase model)
        - **Confidence Scoring**: Multi-factor analysis produces 0-100% confidence level
        - **Leading Indicators**: ISM PMI, Yield Curve Spread, NFCI Credit Conditions
        - **Coincident Indicators**: Real GDP, Unemployment, Industrial Production
        
        **Historical Backtesting**
        - **Dataset**: 7 major business cycles from 2001-2023
        - **Cycle Dates**: Aligned with NBER official dating where applicable
        - **Performance Data**: Sector returns calculated from ETF price histories
        - **Limitations**: Limited to US market data; past cycles may not predict future
        
        **Fear & Greed Index Calculation**
        - **Methodology**: Custom implementation of CNN's 7-indicator approach
        - **Components**: Market momentum, volatility, safe haven demand, put/call ratio, junk bond demand, market breadth, stock price strength
        - **Scoring**: 0-100 scale (0=Extreme Fear, 100=Extreme Greed)
        - **Note**: Approximation using available data; may differ from official CNN index
        """)
    
    with col2:
        st.markdown("""
        **Data Quality & Limitations**
        - **FRED Data**: Official US government statistics; considered highly reliable
        - **Market Data**: Yahoo Finance API; subject to occasional delays or errors
        - **ISM PMI**: Synthetic data generated using realistic parameters (production system would use official ISM releases)
        - **Caching**: 1hr (economic) / 30min (market) may cause slight staleness
        - **API Failures**: Fallback to cached data or synthetic approximations
        
        **Model Assumptions**
        - Business cycles follow historical patterns (may not hold in unprecedented conditions)
        - Asset class correlations remain relatively stable across cycles
        - US-centric model (not directly applicable to other economies)
        - Past performance is not indicative of future results
        
        **Confidence Intervals & Uncertainty**
        - Cycle classification confidence shown as percentage (e.g., 85% Expansion)
        - Lower confidence (<60%) suggests transition period or mixed signals
        - AI-generated insights based on historical patterns, not predictions
        - Multiple interpretation frameworks may yield different conclusions
        """)
    
    st.info("""
    **Transparency Note**: This tool is designed for **educational purposes** to demonstrate AI-driven economic 
    analysis. All methodologies and data sources are openly disclosed. Users should independently verify 
    critical information and not rely solely on this tool for high-stakes decisions.
    """)
    
    st.divider()
    
    # 7. Disclaimers
    st.subheader("⚠️ Important Disclaimers")
    
    st.warning("""
    **Investment Disclaimer**: MacroCycle AI Agent is for **educational and informational purposes only**. 
    It does not constitute investment advice, financial advice, trading advice, or any other professional advice. 
    Always conduct your own research and consult with qualified financial advisors before making investment 
    decisions. **Past performance does not guarantee future results.**
    """)
    
    st.info("""
    **AI & Data Limitations**: While we use trusted data sources (FRED, CBOE, SEC), we cannot guarantee 
    the accuracy or completeness of all information. AI-generated insights are based on historical patterns 
    and current data, but **market conditions change rapidly**. This tool should be used as **one input** 
    in your decision-making process, not as a replacement for professional judgment.
    """)
    
    st.divider()
    
    # 8. Prototype Learnings: AI Governance & Operational Realities
    st.subheader("🔬 Prototype Learnings: AI Governance & Operational Realities")
    
    st.markdown("""
    This prototype was built to **demonstrate both the potential and challenges** of autonomous AI systems 
    in financial analysis. The Imperial AI Policy Fellowship surfaced critical insights for policymakers and practitioners:
    """)
    
    st.markdown("#### Core Operational Challenges")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🔍 Data Provenance & Management**
        - **Challenge**: AI agents retrieve data from multiple APIs (FRED, CBOE, Yahoo Finance) without transparent lineage or timestamp verification
        - **MacroCycle Experience**: Several API endpoints returned legacy data with no clear update date
        - **Solution**: Caching layer (1hr economic, 30min market) reduces API costs; metadata tracking essential
        - **Governance**: Ethical AI requires recording data source, update time, reuse conditions, and audit trails
        
        **👥 Human Oversight & Accountability**
        - **Challenge**: AI can generate plausible but incorrect economic interpretations; even in automated pipelines, responsibility must remain human
        - **Solution**: All insights framed as "historical patterns," not predictions; disclaimers prominent
        - **Reality**: Every output requires interpretation, every design choice carries ethical implications
        - **Governance**: Mandatory human-in-the-loop validation—from data selection to publication—is essential for fair and trustworthy AI
        
        **🌍 FinOps & Sustainability**
        - **Challenge**: OpenAI API costs can scale unpredictably; running multiple AI agents reveals environmental cost of computation
        - **MacroCycle Experience**: High energy and compute consumption makes FinOps both a financial AND ethical issue
        - **Solution**: Token limits, caching, quota warnings prevent runaway costs
        - **Governance**: Budget caps, cost attribution, and energy monitoring should be embedded in every AI sandbox and production environment
        """)
    
    with col2:
        st.markdown("""
        **📈 Scalability & Architecture**
        - **Challenge**: Streamlit architecture not suited for high-concurrency production use
        - **Solution**: This prototype demonstrates concepts; production requires API-first architecture
        - **Governance**: Performance SLAs and load testing mandatory before public deployment
        
        **🔐 Security & Compliance**
        - **Challenge**: API keys, user data, and financial information require protection
        - **Solution**: Environment-based secrets, no personal data storage
        - **Governance**: SOC2/ISO27001 compliance required for production systems
        
        **💡 Explainability & Transparency**
        - **Challenge**: AI agents often provide outputs without explaining how results were derived
        - **Risk**: Without an audit trail, confidence and accountability erode quickly
        - **Governance**: Future iterations should include "explainability traces" summarizing data sources, assumptions, and transformations used
        """)
    
    st.divider()
    
    st.markdown("#### Data Ethics Considerations")
    
    st.markdown("""
    Beyond operational challenges, the fellowship surfaced **critical data-ethics questions** unique to AI-driven financial analysis:
    """)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📊 Representation & Bias**
        - **Challenge**: Open economic datasets over-represent well-documented markets, under-represent developing regions
        - **Risk**: Introduces bias into model training and interpretation (mirrored in environmental data with uneven geographic sampling)
        - **Governance**: Ethical practice demands deliberate bias detection and, where possible, weighting or contextual explanation
        """)
    
    with col2:
        st.markdown("""
        **🧪 Synthetic Data Boundaries**
        - **Challenge**: When does synthetic data cross the line from simulation to potential misuse?
        - **MacroCycle Experience**: Synthetic datasets helpful for scenario testing but needed clear labelling and deletion rules
        - **Governance**: Explicit labelling essential to avoid confusion with official statistics
        """)
    
    st.info("""
    **Policy Implication**: As demonstrated by this prototype, autonomous AI systems in finance require 
    comprehensive governance frameworks addressing **data provenance, human oversight, cost/environmental sustainability, 
    bias mitigation, explainability, and transparency**. Regulation should mandate human checkpoints, clear 
    disclosure of AI limitations, and ethical data practices rather than banning innovation.
    """)
    
    st.divider()
    
    st.subheader("🏗️ Technical Architecture")
    
    st.markdown("""
    ```
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                        EXTERNAL DATA SOURCES                             │
    ├─────────────────────────────────────────────────────────────────────────┤
    │                                                                           │
    │  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐              │
    │  │     FRED     │    │     CBOE     │    │  SEC / YF    │              │
    │  │              │    │              │    │              │              │
    │  │ • GDP        │    │ • VIX        │    │ • Sectors    │              │
    │  │ • CPI        │    │ • VVIX       │    │ • Equities   │              │
    │  │ • Unemp.     │    │ • Put/Call   │    │ • ETFs       │              │
    │  │ • Fed Funds  │    │ • Options    │    │ • Indices    │              │
    │  │ • M2 Supply  │    │              │    │              │              │
    │  │ • NFCI       │    │              │    │              │              │
    │  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘              │
    │         │                   │                   │                       │
    └─────────┼───────────────────┼───────────────────┼───────────────────────┘
              │                   │                   │
              └───────────────────┴───────────────────┘
                                  │
                                  ▼
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                       DATA ORCHESTRATION LAYER                           │
    ├─────────────────────────────────────────────────────────────────────────┤
    │                                                                           │
    │  ┌──────────────────────────────────────────────────────────────┐       │
    │  │            Data Fetcher & Caching (1hr/30min TTL)            │       │
    │  └──────────────────────┬───────────────────────────────────────┘       │
    │                         │                                                │
    │                         ▼                                                │
    │  ┌──────────────────────────────────────────────────────────────┐       │
    │  │         Business Cycle Analyzer + Fear/Greed Calculator      │       │
    │  └──────────────────────┬───────────────────────────────────────┘       │
    │                         │                                                │
    └─────────────────────────┼────────────────────────────────────────────────┘
                              │
                              ▼
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                         AI REASONING LAYER                               │
    ├─────────────────────────────────────────────────────────────────────────┤
    │                                                                           │
    │  ┌──────────────────────────────────────────────────────────────┐       │
    │  │        OpenAI GPT-5 + Economic Context (13 metrics)          │       │
    │  │                                                               │       │
    │  │  • Receives: Cycle phase, GDP, inflation, rates, etc.        │       │
    │  │  • Generates: Educational insights & explanations            │       │
    │  │  • Framing: Historical patterns, not predictions             │       │
    │  └──────────────────────┬───────────────────────────────────────┘       │
    │                         │                                                │
    └─────────────────────────┼────────────────────────────────────────────────┘
                              │
                              ▼
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                       PRESENTATION LAYER                                 │
    ├─────────────────────────────────────────────────────────────────────────┤
    │                                                                           │
    │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐        │
    │  │    Key     │  │ Business   │  │   Market   │  │  Economic  │        │
    │  │ Indicators │  │   Cycle    │  │  Analysis  │  │  Calendar  │        │
    │  └────────────┘  └────────────┘  └────────────┘  └────────────┘        │
    │                                                                           │
    │  ┌─────────────────────────────────────────────────────────────┐        │
    │  │             AI Research Agent (Chat Interface)              │        │
    │  └─────────────────────────────────────────────────────────────┘        │
    │                                                                           │
    └───────────────────────────────────────────────────────────────────────────┘
    ```
    """)
    
    st.divider()
    
    st.subheader("🔧 Solution Architecture")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Frontend Layer**
        ```
        ┌─────────────────────────┐
        │    Streamlit Web UI     │
        ├─────────────────────────┤
        │ • Multi-page navigation │
        │ • Plotly visualizations │
        │ • Interactive charts    │
        │ • Chat interface        │
        │ • Session state mgmt    │
        └─────────────────────────┘
        ```
        
        **Data Layer**
        ```
        ┌─────────────────────────┐
        │   Data Management       │
        ├─────────────────────────┤
        │ • EconomicDataFetcher   │
        │ • MarketDataFetcher     │
        │ • Caching (@cache_data) │
        │ • Historical database   │
        └─────────────────────────┘
        ```
        """)
    
    with col2:
        st.markdown("""
        **Analytics Layer**
        ```
        ┌─────────────────────────┐
        │  Business Logic         │
        ├─────────────────────────┤
        │ • BusinessCycleAnalyzer │
        │ • HistoricalBacktester  │
        │ • PortfolioPositioner   │
        │ • FearGreedCalculator   │
        │ • WatchlistManager      │
        └─────────────────────────┘
        ```
        
        **AI Layer**
        ```
        ┌─────────────────────────┐
        │   MacroCycleAgent       │
        ├─────────────────────────┤
        │ • OpenAI GPT-5 API      │
        │ • Context formatting    │
        │ • Conversation history  │
        │ • Educational framing   │
        └─────────────────────────┘
        ```
        """)
    

def _safe_extract_value(data, key='value'):
    """Safely extract a scalar value from economic data that can be DataFrame, Series, or scalar."""
    if isinstance(data, pd.DataFrame):
        if key in data.columns:
            return data[key].iloc[-1]
        else:
            return data.iloc[-1, 0]
    elif isinstance(data, pd.Series):
        return data.iloc[-1]
    else:
        return float(data)

def _display_tool_call(tool_call):
    """Display an autonomous tool call action in a nice format."""
    name = tool_call.get('name', 'Unknown')
    args = tool_call.get('args', {})
    result = tool_call.get('result', {})
    
    if name == 'get_economic_metric':
        metric = result.get('metric', 'Unknown')
        if result.get('status') == 'success':
            value = result.get('value', 'N/A')
            st.success(f"📊 **Fetched {metric}**: {value}")
        else:
            st.warning(f"⚠️ Could not fetch {metric}: {result.get('error', 'Unknown error')}")
    
    elif name == 'create_comparison_chart':
        metrics = args.get('metrics', [])
        time_period = args.get('time_period', 'N/A')
        st.info(f"📈 **Chart Request**: Comparison of {', '.join(metrics)} over {time_period}")
        st.caption("Note: Chart generation coming soon - currently showing request details")
    
    elif name == 'navigate_to_page':
        page = result.get('page', 'Unknown')
        tab = result.get('tab')
        if tab:
            st.info(f"🧭 **Navigation**: Suggested page: {page} → {tab} tab")
        else:
            st.info(f"🧭 **Navigation**: Suggested page: {page}")
        st.caption("You can navigate using the sidebar menu")
    
    elif name == 'analyze_sector_performance':
        time_frame = args.get('time_frame', 'N/A')
        top_n = args.get('top_n', 3)
        st.info(f"🔍 **Sector Analysis**: Analyzing top {top_n} performers over {time_frame}")
        st.caption("Note: Detailed sector analysis available on the Market Analysis page")

def show_ai_research_agent(economic_data, market_data):
    st.title("🤖 AI Research Agent")
    st.caption("Ask questions about economic data, business cycles, and market insights")
    
    st.info("""
    **Welcome!** I'm your AI research assistant. Ask me questions about the current economic conditions, 
    business cycles, sector performance, or market indicators. I'll provide educational insights based on 
    the latest data and historical patterns.
    """)
    
    st.warning("""
    **⚠️ OpenAI API Quota Required**: This AI agent uses OpenAI's GPT-5 API, which requires credits. 
    If you encounter error code 429 ("insufficient_quota"), please add credits at 
    [OpenAI Billing](https://platform.openai.com/account/billing). The autonomous AI features will work 
    immediately once credits are available.
    """)
    
    agent = MacroCycleAgent()
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'ai_messages' not in st.session_state:
        st.session_state.ai_messages = []
    
    analyzer = BusinessCycleAnalyzer()
    cycle_analysis = analyzer.analyze_cycle_phase(
        economic_data['gdp'],
        economic_data['unemployment'],
        economic_data['inflation']
    )
    
    # Calculate GDP growth rate from cycle analysis (it does the calculation correctly)
    gdp_growth = cycle_analysis['gdp_growth']
    unemployment = _safe_extract_value(economic_data['unemployment'])
    inflation = _safe_extract_value(economic_data['inflation'])
    interest_rate = _safe_extract_value(economic_data['interest_rate'])
    
    ism_mfg_val = _safe_extract_value(economic_data['ism_manufacturing'])
    ism_svc_val = _safe_extract_value(economic_data['ism_services'])
    vix_val = _safe_extract_value(economic_data['vix'])
    
    bond_yields_data = economic_data['bond_yields']
    if isinstance(bond_yields_data, pd.DataFrame):
        bond_yields_10y = bond_yields_data['10Y'].iloc[-1]
        bond_yields_2y = bond_yields_data['2Y'].iloc[-1]
    else:
        bond_yields_10y = 4.0
        bond_yields_2y = 3.5
    yield_spread = (bond_yields_10y - bond_yields_2y) * 100
    
    m2_data = economic_data['m2_supply']
    if isinstance(m2_data, pd.DataFrame) and len(m2_data) > 13:
        m2_growth = ((m2_data['value'].iloc[-1] / m2_data['value'].iloc[-13] - 1) * 100)
    elif isinstance(m2_data, pd.Series) and len(m2_data) > 13:
        m2_growth = ((m2_data.iloc[-1] / m2_data.iloc[-13] - 1) * 100)
    else:
        m2_growth = 0
    
    nfci_val = _safe_extract_value(economic_data['nfci'])
    put_call_val = _safe_extract_value(economic_data['put_call_ratio'])
    
    fear_greed_calculator = FearGreedCalculator()
    fg_result = fear_greed_calculator.calculate(economic_data)
    
    economic_context = {
        'cycle_phase': cycle_analysis['phase'],
        'cycle_confidence': cycle_analysis['confidence'],
        'gdp_growth': gdp_growth,
        'unemployment': unemployment,
        'inflation': inflation,
        'interest_rate': interest_rate,
        'ism_manufacturing': ism_mfg_val,
        'ism_services': ism_svc_val,
        'vix': vix_val,
        'yield_spread': yield_spread,
        'm2_growth': m2_growth,
        'nfci': nfci_val,
        'put_call_ratio': put_call_val,
        'fear_greed_index': fg_result['score'],
        'fear_greed_label': fg_result['rating']
    }
    
    with st.expander("📊 Current Economic Context", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Business Cycle", cycle_analysis['phase'], f"{cycle_analysis['confidence']}% confidence")
            st.metric("GDP Growth", f"{gdp_growth:.2f}%")
            st.metric("Unemployment", f"{unemployment:.2f}%")
            st.metric("Inflation (CPI)", f"{inflation:.2f}%")
        with col2:
            st.metric("Fed Funds Rate", f"{interest_rate:.2f}%")
            st.metric("ISM Manufacturing", f"{ism_mfg_val:.1f}")
            st.metric("ISM Services", f"{ism_svc_val:.1f}")
            st.metric("VIX", f"{vix_val:.2f}")
        with col3:
            st.metric("10Y-2Y Spread", f"{yield_spread:.0f} bps")
            st.metric("M2 Growth (YoY)", f"{m2_growth:.2f}%")
            st.metric("NFCI", f"{nfci_val:.2f}")
            st.metric("Fear & Greed", f"{fg_result['score']:.0f}", fg_result['rating'])
    
    st.divider()
    
    st.subheader("💬 Chat with AI Agent")
    
    suggested_questions = agent.get_suggested_questions(cycle_analysis['phase'])
    
    st.markdown("**Suggested Questions:**")
    cols = st.columns(2)
    for i, question in enumerate(suggested_questions):
        with cols[i % 2]:
            if st.button(question, key=f"suggest_{i}", use_container_width=True):
                st.session_state.ai_messages.append({"role": "user", "content": question})
                response, tool_calls = agent.chat(question, economic_context, st.session_state.chat_history)
                st.session_state.ai_messages.append({"role": "assistant", "content": response, "tool_calls": tool_calls})
                st.session_state.chat_history.append({"role": "user", "content": question})
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()
    
    st.divider()
    
    for message in st.session_state.ai_messages:
        if message["role"] == "user":
            with st.chat_message("user"):
                st.write(message["content"])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.write(message["content"])
                
                # Display autonomous actions if any
                if "tool_calls" in message and message["tool_calls"]:
                    st.markdown("---")
                    st.markdown("**🤖 Autonomous Actions Taken:**")
                    for tool_call in message["tool_calls"]:
                        _display_tool_call(tool_call)
    
    user_input = st.chat_input("Ask me anything about the economy, business cycles, or market conditions...")
    
    if user_input:
        st.session_state.ai_messages.append({"role": "user", "content": user_input})
        
        with st.chat_message("user"):
            st.write(user_input)
        
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Thinking and taking autonomous actions..."):
                response, tool_calls = agent.chat(user_input, economic_context, st.session_state.chat_history)
                st.write(response)
                
                # Display autonomous actions if any
                if tool_calls:
                    st.markdown("---")
                    st.markdown("**🤖 Autonomous Actions Taken:**")
                    for tool_call in tool_calls:
                        _display_tool_call(tool_call)
        
        st.session_state.ai_messages.append({"role": "assistant", "content": response, "tool_calls": tool_calls})
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()
    
    if len(st.session_state.ai_messages) > 0:
        if st.button("🗑️ Clear Chat History"):
            st.session_state.ai_messages = []
            st.session_state.chat_history = []
            st.rerun()

if __name__ == "__main__":
    main()
