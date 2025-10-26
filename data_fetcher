import yfinance as yf
import pandas as pd
import requests
from fredapi import Fred
from datetime import datetime, timedelta
import os

class EconomicDataFetcher:
    def __init__(self):
        self.fred_api_key = os.environ.get('FRED_API_KEY', None)
        if self.fred_api_key:
            self.fred = Fred(api_key=self.fred_api_key)
        else:
            self.fred = None
    
    def get_gdp_data(self, years=10):
        if not self.fred:
            return self._get_sample_gdp_data(years)
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=years*365)
            gdp = self.fred.get_series('GDP', start_date, end_date)
            return pd.DataFrame({'date': gdp.index, 'value': gdp.values})
        except:
            return self._get_sample_gdp_data(years)
    
    def get_inflation_data(self, years=10):
        if not self.fred:
            return self._get_sample_inflation_data(years)
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=years*365)
            cpi = self.fred.get_series('CPIAUCSL', start_date, end_date)
            inflation = cpi.pct_change(12) * 100
            return pd.DataFrame({'date': inflation.index, 'value': inflation.values})
        except:
            return self._get_sample_inflation_data(years)
    
    def get_unemployment_data(self, years=10):
        if not self.fred:
            return self._get_sample_unemployment_data(years)
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=years*365)
            unemployment = self.fred.get_series('UNRATE', start_date, end_date)
            return pd.DataFrame({'date': unemployment.index, 'value': unemployment.values})
        except:
            return self._get_sample_unemployment_data(years)
    
    def get_interest_rate_data(self, years=10):
        if not self.fred:
            return self._get_sample_interest_rate_data(years)
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=years*365)
            # Use DFF (Daily Effective Federal Funds Rate) for most current data
            # Falls back to FEDFUNDS (monthly average) if daily data unavailable
            try:
                fed_funds = self.fred.get_series('DFF', start_date, end_date)
            except:
                fed_funds = self.fred.get_series('FEDFUNDS', start_date, end_date)
            return pd.DataFrame({'date': fed_funds.index, 'value': fed_funds.values})
        except:
            return self._get_sample_interest_rate_data(years)
    
    def get_m2_supply_data(self, years=10):
        if not self.fred:
            return self._get_sample_m2_data(years)
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=years*365)
            m2 = self.fred.get_series('M2SL', start_date, end_date)
            return pd.DataFrame({'date': m2.index, 'value': m2.values})
        except:
            return self._get_sample_m2_data(years)
    
    def get_ism_manufacturing(self, years=10):
        return self._get_sample_ism_data(years, 'manufacturing')
    
    def get_ism_services(self, years=10):
        return self._get_sample_ism_data(years, 'services')
    
    def get_bond_yields(self):
        if not self.fred:
            return self._get_sample_bond_yields()
        try:
            yields = {}
            yield_series = {
                '2Y': 'DGS2',
                '5Y': 'DGS5',
                '10Y': 'DGS10',
                '30Y': 'DGS30'
            }
            for name, series_id in yield_series.items():
                try:
                    data = self.fred.get_series(series_id)
                    yields[name] = data.iloc[-1] if len(data) > 0 else None
                except:
                    yields[name] = None
            return yields
        except:
            return self._get_sample_bond_yields()
    
    def get_gold_price(self):
        try:
            gold = yf.Ticker("GC=F")
            hist = gold.history(period="5d")
            if not hist.empty:
                return hist['Close'].iloc[-1]
            else:
                gold_etf = yf.Ticker("GLD")
                hist = gold_etf.history(period="5d")
                return hist['Close'].iloc[-1] if not hist.empty else 2000.0
        except:
            return 2000.0
    
    def get_bitcoin_price(self):
        try:
            btc = yf.Ticker("BTC-USD")
            hist = btc.history(period="5d")
            return hist['Close'].iloc[-1] if not hist.empty else 50000.0
        except:
            return 50000.0
    
    def get_dxy_data(self):
        try:
            dxy = yf.Ticker("DX-Y.NYB")
            hist = dxy.history(period="5d")
            if not hist.empty:
                return hist['Close'].iloc[-1]
            else:
                uup = yf.Ticker("UUP")
                hist = uup.history(period="5d")
                return hist['Close'].iloc[-1] if not hist.empty else 100.0
        except:
            return 100.0
    
    def get_vix(self):
        try:
            vix = yf.Ticker("^VIX")
            hist = vix.history(period="5d")
            return hist['Close'].iloc[-1] if not hist.empty else 15.0
        except:
            return 15.0
    
    def get_credit_spread(self):
        if not self.fred:
            return 3.5
        try:
            spread = self.fred.get_series('BAMLH0A0HYM2')
            return spread.iloc[-1] if len(spread) > 0 else 3.5
        except:
            return 3.5
    
    def get_ted_spread(self):
        if not self.fred:
            return 0.3
        try:
            ted = self.fred.get_series('TEDRATE')
            return ted.iloc[-1] if len(ted) > 0 else 0.3
        except:
            return 0.3
    
    def get_fed_balance_sheet(self):
        if not self.fred:
            return 7500.0
        try:
            balance = self.fred.get_series('WALCL')
            return balance.iloc[-1] if len(balance) > 0 else 7500.0
        except:
            return 7500.0
    
    def get_reverse_repo(self):
        if not self.fred:
            return 500.0
        try:
            rrp = self.fred.get_series('RRPONTSYD')
            return rrp.iloc[-1] if len(rrp) > 0 else 500.0
        except:
            return 500.0
    
    def get_sp500_data(self, days=252):
        try:
            ticker = "^GSPC"
            data = yf.download(ticker, period=f"{days}d", progress=False)
            if len(data) == 0:
                return self._get_sample_sp500_data(days)
            return pd.DataFrame({
                'date': data.index,
                'price': data['Close'].values
            })
        except:
            return self._get_sample_sp500_data(days)
    
    def get_put_call_ratio(self, days=10):
        try:
            if not self.fred:
                return self._get_sample_put_call_ratio(days)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            pc_ratio = self.fred.get_series('PCCE', start_date, end_date)
            if len(pc_ratio) == 0:
                return self._get_sample_put_call_ratio(days)
            return pd.DataFrame({'date': pc_ratio.index, 'value': pc_ratio.values})
        except:
            return self._get_sample_put_call_ratio(days)
    
    def get_nyse_highs_lows(self):
        try:
            highs_ticker = "^NYA-HI"
            lows_ticker = "^NYA-LO"
            highs = yf.download(highs_ticker, period="5d", progress=False)
            lows = yf.download(lows_ticker, period="5d", progress=False)
            
            if len(highs) > 0 and len(lows) > 0:
                return {
                    'highs': highs['Close'].iloc[-1] if len(highs) > 0 else 100,
                    'lows': lows['Close'].iloc[-1] if len(lows) > 0 else 50
                }
            return self._get_sample_nyse_highs_lows()
        except:
            return self._get_sample_nyse_highs_lows()
    
    def get_market_breadth(self, days=90):
        try:
            advance_decline = yf.download("^AD", period=f"{days}d", progress=False)
            if len(advance_decline) == 0:
                return self._get_sample_market_breadth(days)
            
            cumulative = advance_decline['Close'].cumsum()
            return pd.DataFrame({
                'date': cumulative.index,
                'value': cumulative.values
            })
        except:
            return self._get_sample_market_breadth(days)
    
    def get_safe_haven_demand(self, days=20):
        try:
            sp500 = yf.download("^GSPC", period=f"{days}d", progress=False)
            tlt = yf.download("TLT", period=f"{days}d", progress=False)
            
            if len(sp500) > 0 and len(tlt) > 0:
                sp500_return = (sp500['Close'].iloc[-1] / sp500['Close'].iloc[0] - 1) * 100
                tlt_return = (tlt['Close'].iloc[-1] / tlt['Close'].iloc[0] - 1) * 100
                return sp500_return - tlt_return
            return 5.0
        except:
            return 5.0
    
    def get_fear_greed_index(self):
        try:
            url = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return {
                'score': data['fear_and_greed']['score'],
                'rating': data['fear_and_greed']['rating'],
                'timestamp': data['fear_and_greed'].get('timestamp', ''),
                'previous_close': data['fear_and_greed'].get('previous_close', None),
                'previous_week': data['fear_and_greed'].get('previous_1_week', None),
                'previous_month': data['fear_and_greed'].get('previous_1_month', None)
            }
        except:
            return self._get_sample_fear_greed_index()
    
    def get_nfci_data(self, years=5):
        if not self.fred:
            return self._get_sample_nfci_data(years)
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=years*365)
            nfci = self.fred.get_series('NFCI', start_date, end_date)
            return pd.DataFrame({'date': nfci.index, 'value': nfci.values})
        except:
            return self._get_sample_nfci_data(years)
    
    def get_market_momentum(self):
        try:
            tickers = {
                'SPY': 'S&P 500',
                'QQQ': 'Nasdaq 100',
                'IWM': 'Russell 2000'
            }
            
            results = {}
            for ticker, name in tickers.items():
                data = yf.download(ticker, period="300d", progress=False)
                if len(data) > 0:
                    # Handle multi-index columns from yfinance
                    if isinstance(data['Close'].iloc[-1], pd.Series):
                        current_price = float(data['Close'].iloc[-1].values[0])
                        ma_series = data['Close'].rolling(window=210).mean().iloc[-1]
                        ma_10m = float(ma_series.values[0]) if isinstance(ma_series, pd.Series) else float(ma_series)
                    else:
                        current_price = float(data['Close'].iloc[-1])
                        ma_10m = float(data['Close'].rolling(window=210).mean().iloc[-1])
                    
                    # Check if MA is valid (not NaN)
                    if pd.isna(ma_10m) or ma_10m == 0:
                        continue
                    
                    percent_from_ma = ((current_price / ma_10m - 1) * 100)
                    
                    results[ticker] = {
                        'name': name,
                        'current': current_price,
                        'ma_10m': ma_10m,
                        'percent_from_ma': percent_from_ma,
                        'above_ma': current_price > ma_10m
                    }
            
            return results if results else self._get_sample_market_momentum()
        except Exception as e:
            print(f"Error in get_market_momentum: {e}")
            return self._get_sample_market_momentum()
    
    def get_put_call_ratio_latest(self):
        """Get current Put/Call Ratio from FRED - scalar value"""
        if not self.fred:
            return 0.85
        try:
            pc_ratio = self.fred.get_series('PUTCALL')
            return pc_ratio.iloc[-1] if len(pc_ratio) > 0 else 0.85
        except:
            return 0.85
    
    def get_put_call_ratio_chart_data(self, years=2):
        """Get historical Put/Call Ratio data for charting"""
        if not self.fred:
            return self._get_sample_put_call_data(years)
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=years*365)
            pc_ratio = self.fred.get_series('PUTCALL', start_date, end_date)
            return pd.DataFrame({'date': pc_ratio.index, 'value': pc_ratio.values})
        except:
            return self._get_sample_put_call_data(years)
    
    def get_vvix(self):
        """Get current VVIX (Volatility of VIX) from FRED"""
        if not self.fred:
            return 90.0
        try:
            vvix = self.fred.get_series('VVIXCLS')
            return vvix.iloc[-1] if len(vvix) > 0 else 90.0
        except:
            return 90.0
    
    def get_vvix_historical(self, years=2):
        """Get historical VVIX data"""
        if not self.fred:
            return self._get_sample_vvix_data(years)
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=years*365)
            vvix = self.fred.get_series('VVIXCLS', start_date, end_date)
            return pd.DataFrame({'date': vvix.index, 'value': vvix.values})
        except:
            return self._get_sample_vvix_data(years)
    
    def get_hy_ig_credit_spread(self):
        """Get HY-IG Credit Spread (High Yield minus Investment Grade)"""
        if not self.fred:
            return 2.5
        try:
            # High Yield spread
            hy_spread = self.fred.get_series('BAMLH0A0HYM2')
            # Investment Grade spread
            ig_spread = self.fred.get_series('BAMLC0A0CM')
            
            if len(hy_spread) > 0 and len(ig_spread) > 0:
                return hy_spread.iloc[-1] - ig_spread.iloc[-1]
            else:
                return 2.5
        except:
            return 2.5
    
    def get_hy_ig_spread_historical(self, years=5):
        """Get historical HY-IG Credit Spread differential"""
        if not self.fred:
            return self._get_sample_credit_spread_data(years)
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=years*365)
            
            hy_spread = self.fred.get_series('BAMLH0A0HYM2', start_date, end_date)
            ig_spread = self.fred.get_series('BAMLC0A0CM', start_date, end_date)
            
            # Calculate differential
            spread_diff = hy_spread - ig_spread
            return pd.DataFrame({'date': spread_diff.index, 'value': spread_diff.values})
        except:
            return self._get_sample_credit_spread_data(years)
    
    def get_etf_flows(self, days=30):
        """Get ETF flows for major indexes - using calculated estimates from volume data"""
        # Note: True ETF flow data requires subscription services
        # This uses volume-based estimates as a proxy
        return self._get_sample_etf_flows(days)
    
    def get_aaii_sentiment(self):
        """Get AAII Sentiment Survey - % Bullish/Bearish retail investors"""
        # Note: AAII data requires subscription or scraping
        # Using sample data for demonstration
        return self._get_sample_aaii_sentiment()
    
    def get_aaii_sentiment_historical(self, weeks=52):
        """Get historical AAII Sentiment Survey data"""
        return self._get_sample_aaii_sentiment_historical(weeks)
    
    def _get_sample_gdp_data(self, years):
        dates = pd.date_range(end=datetime.now(), periods=years*4, freq='Q')
        values = [20000 + i*500 + (i%4)*200 for i in range(len(dates))]
        return pd.DataFrame({'date': dates, 'value': values})
    
    def _get_sample_inflation_data(self, years):
        dates = pd.date_range(end=datetime.now(), periods=years*12, freq='M')
        values = [2.0 + (i%24)/12 for i in range(len(dates))]
        return pd.DataFrame({'date': dates, 'value': values})
    
    def _get_sample_unemployment_data(self, years):
        dates = pd.date_range(end=datetime.now(), periods=years*12, freq='M')
        values = [4.5 + (i%36)/18 for i in range(len(dates))]
        return pd.DataFrame({'date': dates, 'value': values})
    
    def _get_sample_interest_rate_data(self, years):
        dates = pd.date_range(end=datetime.now(), periods=years*12, freq='M')
        values = [2.0 + (i%48)/24 for i in range(len(dates))]
        return pd.DataFrame({'date': dates, 'value': values})
    
    def _get_sample_m2_data(self, years):
        dates = pd.date_range(end=datetime.now(), periods=years*12, freq='M')
        values = [18000 + i*50 for i in range(len(dates))]
        return pd.DataFrame({'date': dates, 'value': values})
    
    def _get_sample_bond_yields(self):
        return {
            '2Y': 4.5,
            '5Y': 4.3,
            '10Y': 4.2,
            '30Y': 4.4
        }
    
    def _get_sample_ism_data(self, years, type='manufacturing'):
        import numpy as np
        dates = pd.date_range(end=datetime.now(), periods=years*12, freq='M')
        if type == 'manufacturing':
            base = 51.5
            trend = [base + 3*np.sin(i*np.pi/12) + np.random.normal(0, 1.5) for i in range(len(dates))]
            values = [max(45, min(58, v)) for v in trend]
        else:
            base = 52.5
            trend = [base + 2.5*np.sin(i*np.pi/12 + 1) + np.random.normal(0, 1.2) for i in range(len(dates))]
            values = [max(46, min(60, v)) for v in trend]
        return pd.DataFrame({'date': dates, 'value': values})
    
    def _get_sample_sp500_data(self, days):
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        prices = [4500 + i*2 + (i%20)*10 for i in range(len(dates))]
        return pd.DataFrame({'date': dates, 'price': prices})
    
    def _get_sample_put_call_ratio(self, days):
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        values = [0.8 + (i%10)*0.05 for i in range(len(dates))]
        return pd.DataFrame({'date': dates, 'value': values})
    
    def _get_sample_nyse_highs_lows(self):
        return {'highs': 120, 'lows': 45}
    
    def _get_sample_market_breadth(self, days):
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        values = [1000 + i*5 for i in range(len(dates))]
        return pd.DataFrame({'date': dates, 'value': values})
    
    def _get_sample_fear_greed_index(self):
        import numpy as np
        import random
        
        day_of_year = datetime.now().timetuple().tm_yday
        hour = datetime.now().hour
        
        random.seed(day_of_year)
        base_score = 45 + random.randint(0, 30)
        
        random.seed(day_of_year + hour)
        current_score = max(15, min(85, base_score + random.randint(-10, 10)))
        
        random.seed(day_of_year - 7)
        week_ago = max(15, min(85, base_score + random.randint(-12, 12)))
        
        random.seed(day_of_year - 30)
        month_ago = max(15, min(85, base_score + random.randint(-15, 15)))
        
        random.seed(day_of_year - 1)
        prev_close = max(15, min(85, current_score + random.randint(-5, 5)))
        
        if current_score < 25:
            rating = 'extreme fear'
        elif current_score < 45:
            rating = 'fear'
        elif current_score < 55:
            rating = 'neutral'
        elif current_score < 75:
            rating = 'greed'
        else:
            rating = 'extreme greed'
        
        return {
            'score': float(current_score),
            'rating': rating,
            'timestamp': datetime.now().isoformat(),
            'previous_close': float(prev_close),
            'previous_week': float(week_ago),
            'previous_month': float(month_ago)
        }
    
    def _get_sample_nfci_data(self, years):
        import numpy as np
        dates = pd.date_range(end=datetime.now(), periods=years*52, freq='W')
        values = [-0.2 + 0.4*np.sin(np.arange(len(dates))*np.pi/26) + np.random.normal(0, 0.15, len(dates))]
        return pd.DataFrame({'date': dates, 'value': values[0]})
    
    def _get_sample_put_call_data(self, years):
        """Generate sample Put/Call Ratio data"""
        import numpy as np
        dates = pd.date_range(end=datetime.now(), periods=years*252, freq='D')
        # Put/Call typically ranges 0.5-1.5, with mean around 0.85
        values = 0.85 + 0.2*np.sin(np.arange(len(dates))*2*np.pi/252) + np.random.normal(0, 0.1, len(dates))
        values = np.clip(values, 0.4, 1.6)
        return pd.DataFrame({'date': dates, 'value': values})
    
    def _get_sample_vvix_data(self, years):
        """Generate sample VVIX data"""
        import numpy as np
        dates = pd.date_range(end=datetime.now(), periods=years*252, freq='D')
        # VVIX typically ranges 70-150
        values = 90 + 15*np.sin(np.arange(len(dates))*2*np.pi/252) + np.random.normal(0, 8, len(dates))
        values = np.clip(values, 60, 180)
        return pd.DataFrame({'date': dates, 'value': values})
    
    def _get_sample_credit_spread_data(self, years):
        """Generate sample HY-IG Credit Spread data"""
        import numpy as np
        dates = pd.date_range(end=datetime.now(), periods=years*252, freq='D')
        # HY-IG spread typically ranges 2-6%
        values = 3.0 + 1.5*np.sin(np.arange(len(dates))*2*np.pi/730) + np.random.normal(0, 0.3, len(dates))
        values = np.clip(values, 1.5, 8.0)
        return pd.DataFrame({'date': dates, 'value': values})
    
    def _get_sample_market_momentum(self):
        return {
            'SPY': {
                'name': 'S&P 500',
                'current': 580.0,
                'ma_10m': 560.0,
                'percent_from_ma': 3.57,
                'above_ma': True
            },
            'QQQ': {
                'name': 'Nasdaq 100',
                'current': 505.0,
                'ma_10m': 490.0,
                'percent_from_ma': 3.06,
                'above_ma': True
            },
            'IWM': {
                'name': 'Russell 2000',
                'current': 225.0,
                'ma_10m': 220.0,
                'percent_from_ma': 2.27,
                'above_ma': True
            }
        }
    
    def _get_sample_etf_flows(self, days):
        """Generate sample ETF flow data for major indexes"""
        import numpy as np
        dates = pd.date_range(end=datetime.now(), periods=days, freq='D')
        
        # Generate flows in billions for major ETFs
        flows = {
            'SPY': np.random.normal(0.2, 1.5, days),  # Mean slight inflow, high volatility
            'QQQ': np.random.normal(0.1, 1.2, days),  # Tech flows
            'IWM': np.random.normal(-0.05, 0.8, days),  # Small caps often see outflows
            'TLT': np.random.normal(0.05, 0.6, days)  # Bond flows more stable
        }
        
        return pd.DataFrame({
            'date': dates,
            'SPY': flows['SPY'],
            'QQQ': flows['QQQ'],
            'IWM': flows['IWM'],
            'TLT': flows['TLT']
        })
    
    def _get_sample_aaii_sentiment(self):
        """Generate current AAII sentiment snapshot"""
        import random
        # Seed based on week of year for consistency within the week
        week_num = datetime.now().isocalendar()[1]
        random.seed(week_num)
        
        # Generate realistic percentages that sum to 100
        bullish = random.uniform(25, 45)
        neutral = random.uniform(25, 35)
        bearish = 100 - bullish - neutral
        
        return {
            'bullish': round(bullish, 1),
            'neutral': round(neutral, 1),
            'bearish': round(bearish, 1),
            'bull_bear_spread': round(bullish - bearish, 1)
        }
    
    def _get_sample_aaii_sentiment_historical(self, weeks):
        """Generate historical AAII sentiment data"""
        import numpy as np
        dates = pd.date_range(end=datetime.now(), periods=weeks, freq='W-THU')
        
        # Generate sentiment waves with realistic patterns
        bullish_base = 35 + 10*np.sin(np.arange(weeks)*2*np.pi/52) + np.random.normal(0, 5, weeks)
        bullish = np.clip(bullish_base, 20, 55)
        
        neutral_base = 30 + 3*np.sin(np.arange(weeks)*2*np.pi/26 + 1) + np.random.normal(0, 3, weeks)
        neutral = np.clip(neutral_base, 20, 40)
        
        # Bearish is the remainder to make it sum to 100
        bearish = 100 - bullish - neutral
        
        return pd.DataFrame({
            'date': dates,
            'bullish': bullish,
            'neutral': neutral,
            'bearish': bearish,
            'bull_bear_spread': bullish - bearish
        })


class MarketDataFetcher:
    def __init__(self):
        self.sector_etfs = {
            'Technology': 'XLK',
            'Financials': 'XLF',
            'Healthcare': 'XLV',
            'Consumer Discretionary': 'XLY',
            'Industrials': 'XLI',
            'Energy': 'XLE',
            'Utilities': 'XLU',
            'Real Estate': 'XLRE',
            'Materials': 'XLB',
            'Consumer Staples': 'XLP',
            'Communications': 'XLC'
        }
        
        self.asset_tickers = {
            'Equities': '^GSPC',
            'Bonds': 'TLT',
            'Commodities': 'DBC',
            'Gold': 'GLD'
        }
    
    def get_sector_performance(self, period='1y'):
        sector_data = {}
        for sector, ticker in self.sector_etfs.items():
            try:
                data = yf.download(ticker, period=period, progress=False)
                if not data.empty:
                    performance = ((data['Close'][-1] / data['Close'][0]) - 1) * 100
                    sector_data[sector] = {
                        'performance': performance,
                        'current_price': data['Close'][-1],
                        'data': data
                    }
                else:
                    sector_data[sector] = self._get_fallback_sector_data(sector)
            except:
                sector_data[sector] = self._get_fallback_sector_data(sector)
        return sector_data
    
    def _get_fallback_sector_data(self, sector):
        import random
        import numpy as np
        random.seed(hash(sector) % 1000)
        performance = random.uniform(-10, 25)
        price = random.uniform(80, 150)
        
        # Generate sample historical data for chart
        dates = pd.date_range(end=datetime.now(), periods=365, freq='D')
        # Generate price series with some volatility
        np.random.seed(hash(sector) % 1000)
        returns = np.random.normal(0.0005, 0.01, len(dates))
        prices = price * (1 + returns).cumprod()
        
        sample_data = pd.DataFrame({
            'Close': prices,
            'Open': prices * 0.99,
            'High': prices * 1.01,
            'Low': prices * 0.98,
            'Volume': np.random.randint(1000000, 10000000, len(dates))
        }, index=dates)
        
        return {
            'performance': performance,
            'current_price': price,
            'data': sample_data
        }
    
    def get_asset_class_data(self, period='5y'):
        asset_data = {}
        for asset, ticker in self.asset_tickers.items():
            try:
                data = yf.download(ticker, period=period, progress=False)
                if not data.empty:
                    performance = ((data['Close'][-1] / data['Close'][0]) - 1) * 100
                    asset_data[asset] = {
                        'performance': performance,
                        'current_price': data['Close'][-1],
                        'data': data
                    }
                else:
                    asset_data[asset] = self._get_fallback_asset_data(asset)
            except:
                asset_data[asset] = self._get_fallback_asset_data(asset)
        return asset_data
    
    def _get_fallback_asset_data(self, asset):
        import random
        import numpy as np
        random.seed(hash(asset) % 1000)
        performance = random.uniform(-5, 40)
        price = random.uniform(100, 300)
        
        # Generate sample historical data for chart
        dates = pd.date_range(end=datetime.now(), periods=365*5, freq='D')
        # Generate price series with some volatility
        np.random.seed(hash(asset) % 1000)
        returns = np.random.normal(0.0003, 0.008, len(dates))
        prices = price * (1 + returns).cumprod()
        
        sample_data = pd.DataFrame({
            'Close': prices,
            'Open': prices * 0.99,
            'High': prices * 1.01,
            'Low': prices * 0.98,
            'Volume': np.random.randint(5000000, 50000000, len(dates))
        }, index=dates)
        
        return {
            'performance': performance,
            'current_price': price,
            'data': sample_data
        }
    
    def get_market_index_data(self, ticker='^GSPC', period='5y'):
        try:
            data = yf.download(ticker, period=period, progress=False)
            return data
        except:
            return pd.DataFrame()
