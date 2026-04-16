# quant_engine.py
import yfinance as yf
import json
from datetime import datetime

# Add '.NS' for Indian stocks on Yahoo Finance
TICKERS = ["SBIN.NS", "HCLTECH.NS", "ONGC.NS", "COALINDIA.NS", "CIPLA.NS", "AWL.NS", "CYIENT.NS", "KPITTECH.NS"]

def fetch_and_analyze():
    processed_data = []
    
    for ticker in TICKERS:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # 1. Extract raw data (Fallback to 0 if missing in yfinance)
            cmp = info.get('currentPrice', 0)
            pe = info.get('trailingPE', 0)
            sector_pe = info.get('trailingPE', 15) * 1.1 # Proxy if sector PE missing
            roe = (info.get('returnOnEquity', 0) or 0) * 100
            debt_eq = info.get('debtToEquity', 0) / 100 if info.get('debtToEquity') else 0
            fwd_eps = info.get('forwardEps', 0)
            beta = info.get('beta', 1.0)
            name = info.get('shortName', ticker)
            sector = info.get('sector', 'Unknown')
            
            # Skip if invalid data
            if cmp == 0 or pe == 0: continue

            # 2. Run Quant Logic (Same as React Dashboard)
            dynamic_fair_pe = min(sector_pe, roe * 2.0, 35) # Capped at 35x
            lt_target = round(fwd_eps * dynamic_fair_pe)
            upside_lt = ((lt_target - cmp) / cmp) * 100
            
            # 3. Quality Math & Rules
            quality = min(((roe/25)*30) + (max(1-debt_eq, 0)*20) + 30, 100) # Simplified for example
            
            action = "BUY"
            if roe < 10 or debt_eq > 1.5 or cmp < info.get('twoHundredDayAverage', 0):
                action = "AVOID"
            elif pe > sector_pe * 1.1:
                action = "HOLD"
                
            raw_weight = quality * (1 / max(0.5, beta)) if action == "BUY" else 0
            
            processed_data.append({
                "id": ticker, "name": name, "ticker": ticker.replace('.NS', ''),
                "sector": sector, "cmp": cmp, "pe": round(pe, 1), 
                "sectorPe": round(sector_pe, 1), "roe": round(roe, 1), 
                "debtEq": round(debt_eq, 2), "fwdEps": fwd_eps, 
                "dynamicFairPe": round(dynamic_fair_pe, 1), "ltTarget": lt_target, 
                "upsideLT": round(upside_lt, 1), "quality": round(quality), 
                "beta": round(beta, 1), "maxDd": 20, "ret3m": 5, "ret6m": 10,
                "action": action, "rawWeight": raw_weight,
                "entryType": "Pullback", "reason": "System Generated", "breaker": "Trend Reversal", "stopLoss": round(cmp * 0.9)
            })
            
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")

    # 4. Calculate Allocations and Rank
    total_weight = sum(s['rawWeight'] for s in processed_data)
    for s in processed_data:
        s['allocation'] = round((s['rawWeight'] / total_weight) * 100, 1) if total_weight > 0 else 0
        
    # Sort by upside & quality
    processed_data.sort(key=lambda x: x['upsideLT'] + x['quality'], reverse=True)
    
    for idx, s in enumerate(processed_data):
        s['rank'] = idx + 1

    # Save to JSON
    with open('daily_picks.json', 'w') as f:
        json.dump(processed_data, f, indent=2)

if __name__ == "__main__":
    fetch_and_analyze()
