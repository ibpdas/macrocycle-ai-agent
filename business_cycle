import pandas as pd
import numpy as np
from datetime import datetime

class BusinessCycleAnalyzer:
    def __init__(self):
        self.phases = ['Expansion', 'Peak', 'Contraction', 'Trough']
        self.phase_descriptions = {
            'Expansion': 'Economic growth, rising employment, increasing consumer confidence',
            'Peak': 'Maximum economic output, tight labor market, potential overheating',
            'Contraction': 'Economic slowdown, rising unemployment, declining activity',
            'Trough': 'Economic bottom, high unemployment, potential for recovery'
        }
    
    def analyze_cycle_phase(self, gdp_data, unemployment_data, inflation_data, ism_mfg_data=None, ism_svc_data=None):
        gdp_trend = self._calculate_trend(gdp_data)
        unemployment_trend = self._calculate_trend(unemployment_data)
        inflation_trend = self._calculate_trend(inflation_data)
        
        gdp_recent = gdp_data['value'].iloc[-4:].mean() if len(gdp_data) >= 4 else gdp_data['value'].mean()
        gdp_previous = gdp_data['value'].iloc[-8:-4].mean() if len(gdp_data) >= 8 else gdp_data['value'].iloc[:4].mean()
        gdp_growth = ((gdp_recent - gdp_previous) / gdp_previous) * 100 if gdp_previous != 0 else 0
        
        unemployment_current = unemployment_data['value'].iloc[-1] if len(unemployment_data) > 0 else 5.0
        unemployment_avg = unemployment_data['value'].mean() if len(unemployment_data) > 0 else 5.0
        
        inflation_current = inflation_data['value'].iloc[-1] if len(inflation_data) > 0 else 2.0
        
        ism_mfg_current = None
        ism_svc_current = None
        ism_signal = 'neutral'
        
        if ism_mfg_data is not None and len(ism_mfg_data) > 0:
            ism_mfg_current = ism_mfg_data['value'].iloc[-1]
        if ism_svc_data is not None and len(ism_svc_data) > 0:
            ism_svc_current = ism_svc_data['value'].iloc[-1]
        
        if ism_mfg_current is not None and ism_svc_current is not None:
            ism_avg = (ism_mfg_current + ism_svc_current) / 2
            if ism_avg > 52:
                ism_signal = 'expansion'
            elif ism_avg < 48:
                ism_signal = 'contraction'
        
        phase = self._determine_phase(gdp_growth, gdp_trend, unemployment_trend, 
                                      unemployment_current, unemployment_avg, 
                                      inflation_current, inflation_trend, ism_signal)
        
        return {
            'phase': phase,
            'description': self.phase_descriptions[phase],
            'gdp_growth': gdp_growth,
            'gdp_trend': gdp_trend,
            'unemployment_trend': unemployment_trend,
            'inflation_trend': inflation_trend,
            'unemployment_current': unemployment_current,
            'inflation_current': inflation_current,
            'confidence': self._calculate_confidence(gdp_trend, unemployment_trend, inflation_trend, ism_signal)
        }
    
    def _calculate_trend(self, data):
        if len(data) < 3:
            return 'neutral'
        
        recent_values = data['value'].iloc[-6:] if len(data) >= 6 else data['value']
        
        if len(recent_values) < 2:
            return 'neutral'
        
        slope = np.polyfit(range(len(recent_values)), recent_values, 1)[0]
        
        threshold = recent_values.std() * 0.1
        
        if slope > threshold:
            return 'rising'
        elif slope < -threshold:
            return 'falling'
        else:
            return 'neutral'
    
    def _determine_phase(self, gdp_growth, gdp_trend, unemployment_trend, 
                        unemployment_current, unemployment_avg, 
                        inflation_current, inflation_trend, ism_signal='neutral'):
        if gdp_growth > 2 and gdp_trend == 'rising' and unemployment_trend == 'falling':
            return 'Expansion'
        
        elif gdp_growth > 1 and gdp_trend == 'neutral' and unemployment_current < unemployment_avg:
            if inflation_current > 3 or inflation_trend == 'rising':
                return 'Peak'
            else:
                return 'Expansion'
        
        elif gdp_growth < 0 or (gdp_trend == 'falling' and unemployment_trend == 'rising'):
            return 'Contraction'
        
        elif gdp_growth < 1 and unemployment_current > unemployment_avg and unemployment_trend == 'neutral':
            return 'Trough'
        
        else:
            if ism_signal == 'expansion':
                return 'Expansion'
            elif ism_signal == 'contraction':
                if gdp_growth > 0:
                    return 'Peak'
                else:
                    return 'Contraction'
            elif gdp_growth > 0:
                return 'Expansion'
            else:
                return 'Trough'
    
    def _calculate_confidence(self, gdp_trend, unemployment_trend, inflation_trend, ism_signal='neutral'):
        score = 0
        
        if gdp_trend in ['rising', 'falling']:
            score += 30
        else:
            score += 10
        
        if unemployment_trend in ['rising', 'falling']:
            score += 30
        else:
            score += 10
        
        if inflation_trend in ['rising', 'falling']:
            score += 25
        else:
            score += 10
        
        if ism_signal in ['expansion', 'contraction']:
            score += 15
        else:
            score += 5
        
        return min(score, 100)
    
    def get_phase_recommendations(self, phase):
        recommendations = {
            'Expansion': {
                'investment': 'Focus on growth stocks, cyclical sectors (technology, consumer discretionary)',
                'bonds': 'Consider reducing bond duration as rates may rise',
                'commodities': 'Positive outlook for industrial commodities',
                'sectors': ['Technology', 'Consumer Discretionary', 'Industrials', 'Financials']
            },
            'Peak': {
                'investment': 'Take profits on cyclical positions, rotate to defensive sectors',
                'bonds': 'Short-term bonds preferred, watch for rate peaks',
                'commodities': 'Energy and precious metals as inflation hedge',
                'sectors': ['Healthcare', 'Consumer Staples', 'Utilities', 'Energy']
            },
            'Contraction': {
                'investment': 'Defensive positioning, quality over growth, preserve capital',
                'bonds': 'Increase allocation to high-quality bonds',
                'commodities': 'Gold and defensive commodities',
                'sectors': ['Healthcare', 'Consumer Staples', 'Utilities']
            },
            'Trough': {
                'investment': 'Prepare for recovery, accumulate quality cyclicals at discount',
                'bonds': 'Lock in higher yields with longer duration',
                'commodities': 'Position for recovery in industrial commodities',
                'sectors': ['Financials', 'Industrials', 'Materials', 'Real Estate']
            }
        }
        return recommendations.get(phase, recommendations['Expansion'])
    
    def get_historical_cycles(self):
        historical_cycles = [
            {'period': '2001-2003', 'phase': 'Contraction', 'event': 'Dot-com bubble burst, 9/11'},
            {'period': '2003-2007', 'phase': 'Expansion', 'event': 'Post-recession recovery'},
            {'period': '2007-2009', 'phase': 'Contraction', 'event': 'Global Financial Crisis'},
            {'period': '2009-2019', 'phase': 'Expansion', 'event': 'Longest expansion in US history'},
            {'period': '2020', 'phase': 'Contraction', 'event': 'COVID-19 pandemic'},
            {'period': '2020-2021', 'phase': 'Expansion', 'event': 'Pandemic recovery'},
            {'period': '2022-2023', 'phase': 'Trough/Early Expansion', 'event': 'Post-inflation adjustment'}
        ]
        return historical_cycles
