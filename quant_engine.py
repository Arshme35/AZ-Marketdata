import yfinance as yf
import json
import time
import math

# Built-in High-Liquidity Indian Market List (Bypasses NSE blocks entirely)
CORE_TICKERS = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "BHARTIARTL.NS", "SBIN.NS", "INFY.NS", 
    "LICI.NS", "ITC.NS", "HINDUNILVR.NS", "LT.NS", "BAJFINANCE.NS", "HCLTECH.NS", "MARUTI.NS", 
    "SUNPHARMA.NS", "ADANIENT.NS", "KOTAKBANK.NS", "TITAN.NS", "ONGC.NS", "TATAMOTORS.NS", 
    "NTPC.NS", "AXISBANK.NS", "DMART.NS", "ADANIPORTS.NS", "ULTRACEMCO.NS", "ASIANPAINT.NS", 
    "COALINDIA.NS", "BAJAJFINSV.NS", "BAJAJ-AUTO.NS", "POWERGRID.NS", "NESTLEIND.NS", "WIPRO.NS", 
    "M&M.NS", "IOC.NS", "JIOFIN.NS", "HAL.NS", "DLF.NS", "ADANIPOWER.NS", "JSWSTEEL.NS", 
    "TATASTEEL.NS", "SIEMENS.NS", "IRFC.NS", "VBL.NS", "ZOMATO.NS", "PIDILITIND.NS", "GRASIM.NS", 
    "SBILIFE.NS", "BEL.NS", "LTIM.NS", "TRENT.NS", "PNB.NS", "INDIGO.NS", "BANKBARODA.NS", 
    "HDFCLIFE.NS", "ABB.NS", "BPCL.NS", "PFC.NS", "GODREJCP.NS", "TATAPOWER.NS", "HINDALCO.NS",
    "VEDL.NS", "CHOLAFIN.NS", "AMBUJACEM.NS", "RECLTD.NS", "CIPLA.NS", "GAIL.NS", "SRF.NS", 
    "TVSMOTOR.NS", "BOSCHLTD.NS", "EICHERMOT.NS", "DIVISLAB.NS", "CGPOWER.NS", "ZYDUSLIFE.NS",
    "APOLLOHOSP.NS", "TECHM.NS", "MAXHEALTH.NS", "TORNTPOWER.NS", "COLPAL.NS", "KPITTECH.NS",
    "AWL.NS", "CYIENT.NS"
]

def safe_get(info_dict, key, default=0):
    """Safe Math: Prevents NaN (Not a Number) errors in the dashboard"""
    val = info_dict.get(key)
    if val is None or (isinstance(val, float) and math.isnan(val)): 
        return default
    return val

def analyze_stock(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        cmp = safe_get(info, 'currentPrice')
        if cmp == 0: return None # Skip if no price data
        
        # Safe Fundamental Fetching
        pe = safe_get(info, 'trailingPE', 25)
        roe = safe_get(info, 'returnOnEquity', 0) * 100
        debt_eq = safe_get(info, 'debtToEquity', 0) / 100
        fwd_eps = safe_get(info, 'forwardEps', cmp/pe if pe else 1)
        sector_pe = safe_get(info, 'trailingPE', 25)
        peg = safe_get(info, 'pegRatio', 1.5)
        eps_growth = pe / peg if (peg and peg > 0) else 15
        
        # Institutional Model
        fair_pe = min(sector_pe, roe * 2.0, eps_growth * 1.5, 45)
        lt_target = fwd_eps * fair_pe
        upside_lt = ((lt_target - cmp) / cmp) * 100 if cmp > 0 else 0
        upside_st = upside_lt * 0.35
        
        # Technicals
        rsi = safe_get(info, 'rsi', 50)
        dma200 = safe_get(info, 'twoHundredDayAverage', cmp * 0.95)
        beta = safe_get(info, 'beta', 1.0)
        
        # Risk & Action Logic
        action = "BUY"
        risk = "BALANCED"
        if roe < 8 or debt_eq > 1.5 or cmp < dma200: 
            action = "AVOID"
            risk = "HIGH"
        elif rsi > 70: 
            action = "WAIT"
            risk = "BALANCED"
        elif beta > 1.3: risk = "AGGRESSIVE"
        elif beta < 0.8: risk = "CONSERVATIVE"

        # Reasoning Generator
        reasons = []
        if pe > 0 and pe < sector_pe * 0.8: reasons.append(f"Trades at {round((1-pe/sector_pe)*100)}% discount to historical.")
        if roe > 18: reasons.append(f"Elite capital efficiency (ROE {round(roe, 1)}%).")
        if debt_eq < 0.15: reasons.append("Virtually debt-free balance sheet.")
        if cmp > dma200 and rsi < 60: reasons.append("Strong technical trend with RSI headroom.")
        reasoning = " ".join(reasons[:2]) if reasons else "Standard quality metrics with stable valuation."

        return {
            "id": ticker, "name": info.get('shortName', ticker), "ticker": ticker.replace('.NS', ''),
            "sector": info.get('sector', 'Equities'), "cmp": round(cmp, 2), "pe": round(pe, 1), 
            "roe": round(roe, 1), "debtEq": round(debt_eq, 2), "rsi": round(rsi), 
            "dma200": round(dma200, 2), "upsideST": round(upside_st, 1), "upsideLT": round(upside_lt, 1), 
            "risk": risk, "stopLoss": round(cmp * 0.9, 2), "action": action, 
            "ltTarget": round(lt_target, 2), "reasoning": reasoning
        }
    except Exception as e:
        return None

def fetch_and_analyze():
    print(f"Starting robust scan of {len(CORE_TICKERS)} Top Indian Equities...")
    all_results = []
    
    for i, ticker in enumerate(CORE_TICKERS):
        res = analyze_stock(ticker)
        if res: all_results.append(res)
        time.sleep(0.5) # Crucial: Prevents Yahoo Finance from blocking us
        
    print(f"Successfully analyzed {len(all_results)} stocks.")
    
    # Sort by LT Upside and pick Top 50
    all_results.sort(key=lambda x: x['upsideLT'], reverse=True)
    final_50 = all_results[:50]
    
    with open('daily_picks.json', 'w') as f:
        json.dump(final_50, f, indent=2)

if __name__ == "__main__":
    fetch_and_analyze()
