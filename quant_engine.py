import yfinance as yf
import pandas as pd
import json
import requests
import io
from datetime import datetime
import time

def get_total_market_tickers():
    """Fetches the Nifty Total Market constituent list (~750 stocks)."""
    url = "https://archives.nseindia.com/content/indices/ind_niftytotalmarketlist.csv"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        df = pd.read_csv(io.StringIO(response.text))
        return [symbol + ".NS" for symbol in df['Symbol'].tolist()]
    except Exception as e:
        print(f"Failed to fetch Total Market list: {e}")
        return ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "SBIN.NS"]

def generate_reasoning(ticker, pe, sector_pe, roe, debt_eq, rsi, dma200, cmp):
    """Generates human-like institutional reasoning for the dashboard."""
    reasons = []
    if pe < sector_pe * 0.7: reasons.append(f"Trades at {round((1-pe/sector_pe)*100)}% discount to sector.")
    if roe > 20: reasons.append(f"Elite ROE of {roe}%.")
    if debt_eq < 0.1: reasons.append("Virtually debt-free balance sheet.")
    if cmp > dma200 and rsi < 60: reasons.append("Strong technical trend with RSI headroom.")
    
    if not reasons:
        return "Standard quality metrics with stable valuation."
    return " ".join(reasons[:2])

def analyze_stock(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        cmp = info.get('currentPrice', 0)
        if cmp == 0: return None
        
        # Fundamental Data
        pe = info.get('trailingPE', 25)
        roe = (info.get('returnOnEquity', 0) or 0) * 100
        debt_eq = info.get('debtToEquity', 0) / 100 if info.get('debtToEquity') else 0
        fwd_eps = info.get('forwardEps', cmp/pe if pe != 0 else 1)
        sector_pe = info.get('trailingPE', 25)
        peg = info.get('pegRatio', 1.5)
        eps_growth = round(pe / peg if peg and peg != 0 else 15, 1)
        
        # Institutional Model
        fair_pe = min(sector_pe, roe * 2.0, eps_growth * 1.5, 45)
        lt_target = round(fwd_eps * fair_pe)
        upside_lt = ((lt_target - cmp) / cmp) * 100
        upside_st = upside_lt * 0.35 # Standard ST projection
        
        # Technicals
        rsi = info.get('rsi', 50) 
        dma200 = info.get('twoHundredDayAverage', cmp * 0.95)
        beta = info.get('beta', 1.0)

        # Action Engine
        action = "BUY"
        risk = "BALANCED"
        if roe < 10 or debt_eq > 1.5 or cmp < dma200: 
            action = "AVOID"
            risk = "HIGH"
        elif rsi > 70: 
            action = "WAIT"
            risk = "BALANCED"
        elif beta > 1.3:
            risk = "AGGRESSIVE"
        elif beta < 0.8:
            risk = "CONSERVATIVE"

        return {
            "id": ticker, "name": info.get('shortName', ticker), "ticker": ticker.replace('.NS', ''),
            "sector": info.get('sector', 'General'), "cmp": cmp, "pe": round(pe, 1), "roe": round(roe, 1),
            "debtEq": round(debt_eq, 2), "rsi": round(rsi), "dma200": round(dma200),
            "upsideST": round(upside_st, 1), "upsideLT": round(upside_lt, 1), "risk": risk,
            "stopLoss": round(cmp * 0.9), "action": action,
            "reasoning": generate_reasoning(ticker, pe, sector_pe, roe, debt_eq, rsi, dma200, cmp)
        }
    except: return None

def fetch_and_analyze():
    tickers = get_total_market_tickers()
    all_results = []
    for i, ticker in enumerate(tickers):
        res = analyze_stock(ticker)
        if res: all_results.append(res)
        if i % 20 == 0: time.sleep(0.5) # Anti-block delay
    
    # Sort by LT Upside and pick Top 50
    all_results.sort(key=lambda x: x['upsideLT'], reverse=True)
    final_50 = all_results[:50]
    
    with open('daily_picks.json', 'w') as f:
        json.dump(final_50, f, indent=2)

if __name__ == "__main__":
    fetch_and_analyze()
