import yfinance as yf
import pandas as pd
import json
import math
import time

# Massive Hardcoded Nifty Universe
MASSIVE_TICKER_LIST = [
    "360ONE.NS", "3MINDIA.NS", "ABB.NS", "ACC.NS", "AARTIIND.NS", "AAVAS.NS", "ABBOTINDIA.NS", "ABCAPITAL.NS", 
    "ABFRL.NS", "ADANIENSOL.NS", "ADANIENT.NS", "ADANIGREEN.NS", "ADANIPORTS.NS", "ADANIPOWER.NS", "ATGL.NS", 
    "AWL.NS", "AEGISCHEM.NS", "AETHER.NS", "AFFLE.NS", "AJANTPHARM.NS", "APLLTD.NS", "ALKEM.NS", "ALKYLAMINE.NS", 
    "ALLCARGO.NS", "AMBER.NS", "AMBUJACEM.NS", "ANGELONE.NS", "ANURAS.NS", "APARINDS.NS", "APLAPOLLO.NS", 
    "APOLLOHOSP.NS", "APOLLOTYRE.NS", "APTUS.NS", "ASRAL.NS", "ASTRAL.NS", "ATUL.NS", "AUBANK.NS", "AUROPHARMA.NS", 
    "AVANTIFEED.NS", "DMART.NS", "AXISBANK.NS", "BAJAJ-AUTO.NS", "BAJAJFINSV.NS", "BAJFINANCE.NS", "BALAMINES.NS", 
    "BALKRISIND.NS", "BALRAMCHIN.NS", "BANDHANBNK.NS", "BANKBARODA.NS", "BANKINDIA.NS", "MAHABANK.NS", "BATAINDIA.NS", 
    "BAYERCROP.NS", "BDL.NS", "BEL.NS", "BEML.NS", "BERGEPAINT.NS", "BHARATFORG.NS", "BHEL.NS", "BPCL.NS", 
    "BHARTIARTL.NS", "BIOCON.NS", "BIRLACORPN.NS", "BSOFT.NS", "BLUEDART.NS", "BLUESTARCO.NS", "BOSCHLTD.NS", 
    "BRIGADE.NS", "BRITANNIA.NS", "MAPMYINDIA.NS", "CCL.NS", "CAMPUS.NS", "CANFINHOME.NS", "CANBK.NS", "CAPLIPOINT.NS", 
    "CGPOWER.NS", "CHALET.NS", "CHAMBLFERT.NS", "CHEMPLASTS.NS", "CHENNPETRO.NS", "CHOLAFIN.NS", "CHOLAHLDNG.NS", 
    "CIPLA.NS", "CLEAN.NS", "COALINDIA.NS", "COCHINSHIP.NS", "COFORGE.NS", "COLPAL.NS", "CAMS.NS", "CONCOR.NS", 
    "COROMANDEL.NS", "CRAFTSMAN.NS", "CREDITACC.NS", "CROMPTON.NS", "CUMMINSIND.NS", "CYIENT.NS", "DCMSHRIRAM.NS", 
    "DELHIERY.NS", "DEVYANI.NS", "DIVISLAB.NS", "DIXON.NS", "LALPATHLAB.NS", "DRREDDY.NS", "EIDPARRY.NS", "EIHOTEL.NS", 
    "EICHERMOT.NS", "ELECON.NS", "ELGIEQUIP.NS", "EMAMILTD.NS", "ENDURANCE.NS", "ENGINERSIN.NS", "EPL.NS", 
    "EQUITASBNK.NS", "ESCORTS.NS", "EXIDEIND.NS", "NYKAA.NS", "FEDERALBNK.NS", "FACT.NS", "FINEORG.NS", "FINCABLES.NS", 
    "FINPIPE.NS", "FSL.NS", "FORTIS.NS", "GAIL.NS", "GMMPFAUDLR.NS", "GMRINFRA.NS", "GALAXYSURF.NS", "GARFIBRES.NS", 
    "GICRE.NS", "GILLETTE.NS", "GLAND.NS", "GLAXO.NS", "GLENMARK.NS", "MEDANTA.NS", "GODFRYPHLP.NS", "GODREJCP.NS", 
    "GODREJIND.NS", "GODREJPROP.NS", "GRANULES.NS", "GRAPHITE.NS", "GRASIM.NS", "GRINDWELL.NS", "GUJGASLTD.NS", 
    "GNFC.NS", "GSPL.NS", "HAVELLS.NS", "HCLTECH.NS", "HDFCAMC.NS", "HDFCBANK.NS", "HDFCLIFE.NS", "HEG.NS", 
    "HEROMOTOCO.NS", "HFCL.NS", "HINDALCO.NS", "HAL.NS", "HINDCOPPER.NS", "HINDPETRO.NS", "HINDUNILVR.NS", "HINDZINC.NS", 
    "HONAUT.NS", "HUDCO.NS", "ICICIBANK.NS", "ICICIGI.NS", "ICICIPRULI.NS", "ISEC.NS", "IDBI.NS", "IDFCFIRSTB.NS", 
    "IDFC.NS", "IFBIND.NS", "IGL.NS", "IIFL.NS", "INDHOTEL.NS", "INDIACEM.NS", "INDIANB.NS", "IEX.NS", "INDIGO.NS", 
    "INDIGOPNTS.NS", "INDUSINDBK.NS", "INDUSTOWER.NS", "INFIBEAM.NS", "NAUKRI.NS", "INFY.NS", "INOXLEISUR.NS", 
    "INTELLECT.NS", "IPCALAB.NS", "IRB.NS", "IRCON.NS", "IRCTC.NS", "IRFC.NS", "ITC.NS", "ITDC.NS", "ITI.NS", 
    "J&KBANK.NS", "JSL.NS", "JINDALSTEL.NS", "JIOFIN.NS", "JKCEMENT.NS", "JKPAPER.NS", "JKTYRE.NS", "JSWENERGY.NS", 
    "JSWSTEEL.NS", "JUBLFOOD.NS", "JUBLINGREA.NS", "JUBLPHARMA.NS", "JUSTDIAL.NS", "JYOTHYLAB.NS", "KAJARIACER.NS", 
    "KPITTECH.NS", "KALYANKJIL.NS", "KANSAINER.NS", "KARURVYSYA.NS", "KEC.NS", "KOTAKBANK.NS", "KPRMILL.NS", "KRBL.NS", 
    "L&TFH.NS", "LTTS.NS", "LICHSGFIN.NS", "LICI.NS", "LTIM.NS", "LT.NS", "LAXMIMACH.NS", "LEMONTREE.NS", "LINDEINDIA.NS", 
    "LUPIN.NS", "LUXIND.NS", "MRF.NS", "MTARTECH.NS", "LODHA.NS", "MGL.NS", "M&MFIN.NS", "M&M.NS", "MAHSCOOTER.NS", 
    "MAHASAMLES.NS", "MANAPPURAM.NS", "MARICO.NS", "MARUTI.NS", "MASTEK.NS", "MFSL.NS", "MAXHEALTH.NS", "MAZDOCK.NS", 
    "MEDPLUS.NS", "METROBRAND.NS", "METROPOLIS.NS", "MOTILALOFS.NS", "MPHASIS.NS", "MRPL.NS", "MUTHOOTFIN.NS", 
    "NATCOPHARM.NS", "NATIONALUM.NS", "NAVINFLUOR.NS", "NCC.NS", "NESTLEIND.NS", "NETWORK18.NS", "NAM-INDIA.NS", 
    "NLCINDIA.NS", "NMDC.NS", "NOCIL.NS", "NTPC.NS", "NUVOCO.NS", "OBEROIRLTY.NS", "ONGC.NS", "OIL.NS", "PAYTM.NS", 
    "OFSS.NS", "ORIENTELEC.NS", "PAGEIND.NS", "PATANJALI.NS", "PERSISTENT.NS", "PETRONET.NS", "PFIZER.NS", "PHOENIXLTD.NS", 
    "PIDILITIND.NS", "PEL.NS", "PIIND.NS", "PNBHOUSING.NS", "PNCINFRA.NS", "POLYCAB.NS", "POONAWALLA.NS", "PFC.NS", 
    "POWERGRID.NS", "PRESTIGE.NS", "PRINCEPIPE.NS", "PNB.NS", "QUESS.NS", "RBLBANK.NS", "RECLTD.NS", "REDINGTON.NS", 
    "RELAXO.NS", "RELIANCE.NS", "RBA.NS", "ROUTE.NS", "RVNL.NS", "SAFARI.NS", "SANSERA.NS", "SANOFI.NS", "SAPPHIRE.NS", 
    "SAREGAMA.NS", "SCHAEFFLER.NS", "SCHNEIDER.NS", "SHREECEM.NS", "SHRIRAMFIN.NS", "SHYAMMETL.NS", "SIEMENS.NS", 
    "SIS.NS", "SJVN.NS", "SKFINDIA.NS", "SOBA.NS", "SOLARINDS.NS", "SONACOMS.NS", "SOUTHBANK.NS", "SPARC.NS", 
    "STARHEALTH.NS", "SBILIFE.NS", "SBIN.NS", "SAIL.NS", "SUMICHEM.NS", "SUNPHARMA.NS", "SUNTV.NS", "SUNDARMFIN.NS", 
    "SUNDRMFAST.NS", "SUNTECK.NS", "SUPRAJIT.NS", "SUPREMEIND.NS", "SUVENPHAR.NS", "SUZLON.NS", "SWANENERGY.NS", 
    "SYMPHONY.NS", "SYNGENE.NS", "TCIEXP.NS", "TCNSBRANDS.NS", "TCS.NS", "TATACHEM.NS", "TATACOMM.NS", "TATACONSUM.NS", 
    "TATAELXSI.NS", "TATAINVEST.NS", "TATAMOTORS.NS", "TATAPOWER.NS", "TATASTEEL.NS", "TTML.NS", "TEAMLEASE.NS", 
    "TECHM.NS", "TEJASNET.NS", "NIACL.NS", "RAMCOCEM.NS", "THERMAX.NS", "TIMKEN.NS", "TITAN.NS", "TORNTPHARM.NS", 
    "TORNTPOWER.NS", "TRENT.NS", "TRIDENT.NS", "TRIVENI.NS", "TRITURBINE.NS", "TIINDIA.NS", "UCOBANK.NS", "ULTRACEMCO.NS", 
    "UNIONBANK.NS", "UBL.NS", "MCDOWELL-N.NS", "UPLLTD.NS", "UTIAMC.NS", "VGUARD.NS", "VIPIND.NS", "VTL.NS", "VARROC.NS", 
    "VBL.NS", "VEDL.NS", "VIJAYA.NS", "VINATIORGA.NS", "VOLTAS.NS", "WELCORP.NS", "WELENT.NS", "WHIRLPOOL.NS", "WIPRO.NS", 
    "YESBANK.NS", "ZEEL.NS", "ZENSARTECH.NS", "ZOMATO.NS", "ZYDUSLIFE.NS", "ZYDUSWELL.NS"
]

def clean_val(val, default="N/A"):
    try:
        if val is None: return default
        f_val = float(val)
        if math.isnan(f_val) or math.isinf(f_val): return default
        return f_val
    except: return default

def analyze_stock(ticker):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        cmp = clean_val(info.get('currentPrice'))
        if cmp == "N/A" or cmp <= 0: return None 
        
        # --- LONG TERM VALUE METRICS ---
        pe = clean_val(info.get('trailingPE'))
        roe_raw = clean_val(info.get('returnOnEquity'))
        roe = roe_raw * 100 if roe_raw != "N/A" else "N/A"
        debt_eq_raw = clean_val(info.get('debtToEquity'))
        debt_eq = debt_eq_raw / 100 if debt_eq_raw != "N/A" else "N/A"
        fwd_eps = clean_val(info.get('forwardEps'))
        sector_pe = clean_val(info.get('trailingPE'), 25)
        peg = clean_val(info.get('pegRatio'))
        low52 = clean_val(info.get('fiftyTwoWeekLow'))
        high52 = clean_val(info.get('fiftyTwoWeekHigh'))
        dma200 = clean_val(info.get('twoHundredDayAverage'))
        
        # --- SHORT TERM / SWING METRICS ---
        vol_today = clean_val(info.get('volume'))
        vol_avg = clean_val(info.get('averageDailyVolume10Day'))
        dma50 = clean_val(info.get('fiftyDayAverage'))
        rsi = clean_val(info.get('rsi'))
        
        # Safe calculations (Bypasses missing volume issues)
        vol_surge = round(vol_today / vol_avg, 2) if vol_avg != "N/A" and vol_today != "N/A" and vol_avg > 0 else "N/A"
        dist_50dma = round(((cmp - dma50) / dma50) * 100, 1) if dma50 != "N/A" and dma50 > 0 else "N/A"
        
        try:
            latest_news = stock.news[0]['title'] if stock.news else "No recent catalysts."
        except:
            latest_news = "News feed unavailable."
        
        if pe != "N/A" and peg != "N/A" and peg > 0: eps_growth = pe / peg
        else: eps_growth = 15
            
        if pe != "N/A" and roe != "N/A" and fwd_eps != "N/A":
            fair_pe = min(sector_pe, roe * 2.0, eps_growth * 1.5, 45)
            lt_target = round(fwd_eps * fair_pe, 2)
            upside_lt = round(((lt_target - cmp) / cmp) * 100, 1) if cmp > 0 else "N/A"
            upside_st = round(upside_lt * 0.35, 1) if upside_lt != "N/A" else "N/A"
        else:
            lt_target, upside_lt, upside_st = "N/A", "N/A", "N/A"

        # --- LONG TERM LOGIC ---
        lt_action = "BUY"
        avoid_reasons = []
        if roe != "N/A" and roe < 8: 
            lt_action = "AVOID"
            avoid_reasons.append("Low Capital Efficiency (ROE < 8%)")
        if debt_eq != "N/A" and debt_eq > 1.5: 
            lt_action = "AVOID"
            avoid_reasons.append("High Debt Risk (D/E > 1.5)")
        if dma200 != "N/A" and cmp < dma200: 
            lt_action = "AVOID"
            avoid_reasons.append("Downtrend (Below 200 DMA)")
        if rsi != "N/A" and rsi > 70: 
            lt_action = "WAIT"
            avoid_reasons.append("Overbought Technicals (RSI > 70)")
        if pe != "N/A" and sector_pe != "N/A" and pe > sector_pe * 1.5:
            lt_action = "WAIT"
            avoid_reasons.append("Overvalued vs Sector peers")
            
        avoid_reason_str = " • ".join(avoid_reasons) if avoid_reasons else "None"
        
        risk = "BALANCED"
        beta = clean_val(info.get('beta'))
        if beta != "N/A":
            if beta > 1.3: risk = "AGGRESSIVE"
            elif beta < 0.8: risk = "CONSERVATIVE"

        lt_reasons = []
        if pe != "N/A" and sector_pe != "N/A" and pe < sector_pe * 0.8: lt_reasons.append(f"Trades at {round((1-pe/sector_pe)*100)}% discount to sector.")
        if roe != "N/A" and roe > 18: lt_reasons.append(f"Elite capital efficiency (ROE {round(roe, 1)}%).")
        if debt_eq != "N/A" and debt_eq < 0.15: lt_reasons.append("Virtually debt-free balance sheet.")
        if dma200 != "N/A" and rsi != "N/A" and cmp > dma200 and rsi < 60: lt_reasons.append("Strong technical trend with RSI headroom.")
        reasoning = " ".join(lt_reasons[:2]) if lt_reasons else "Solid fundamentals but lacks extreme asymmetry."

        # --- SHORT TERM / SWING LOGIC (Robust Top 20) ---
        st_reasons = []
        st_score = 0
        
        # 1. Price Momentum (Proximity to 50 DMA)
        if dist_50dma != "N/A":
            if dist_50dma > 0:
                st_score += 25
                st_reasons.append("Trading above 50 DMA trend.")
            elif -5 <= dist_50dma <= 0:
                st_score += 15
                st_reasons.append("Consolidating near 50 DMA support.")
                
        # 2. Macro Trend
        if dma200 != "N/A" and cmp > dma200:
            st_score += 15
            st_reasons.append("Confirmed long-term uptrend.")

        # 3. RSI Momentum (Goldilocks zone)
        if rsi != "N/A":
            if 55 <= rsi <= 72:
                st_score += 35
                st_reasons.append("Bullish momentum RSI zone.")
            elif 40 <= rsi < 55:
                st_score += 10
                st_reasons.append("RSI structure recovering.")
        
        # 4. Volume Catalyst (If data exists)
        if vol_surge != "N/A" and vol_surge > 1.3:
            st_score += 25
            st_reasons.append(f"Heavy Volume Accumulation ({vol_surge}x Avg).")
            
        st_reasoning = " ".join(st_reasons) if st_reasons else "Weak structure / Lack of momentum."
        
        if st_score >= 70: st_action = "HIGH PROB"
        elif st_score >= 40: st_action = "MOMENTUM"
        else: st_action = "WATCH"

        return {
            "id": ticker, "name": info.get('shortName', ticker), "ticker": ticker.replace('.NS', ''),
            "sector": info.get('sector', 'Equities'), "cmp": round(cmp, 2), "pe": round(pe, 1) if pe != "N/A" else pe, 
            "roe": round(roe, 1) if roe != "N/A" else roe, "debtEq": round(debt_eq, 2) if debt_eq != "N/A" else debt_eq, 
            "rsi": round(rsi) if rsi != "N/A" else rsi, "dma200": round(dma200, 2) if dma200 != "N/A" else dma200, 
            "dma50": round(dma50, 2) if dma50 != "N/A" else dma50, "volSurge": vol_surge, "dist50dma": dist_50dma,
            "low52": round(low52, 2) if low52 != "N/A" else low52, "high52": round(high52, 2) if high52 != "N/A" else high52,
            "upsideLT": upside_lt, "ltTarget": lt_target, "ltAction": lt_action, "stAction": st_action, 
            "stScore": st_score, "stReasoning": st_reasoning, "news": latest_news, "avoidReason": avoid_reason_str,
            "risk": risk, "stopLoss": round(cmp * 0.9, 2), "reasoning": reasoning
        }
    except Exception as e: return None

def fetch_and_analyze():
    print("Starting dual-strategy scan for Top 20 Probabilities...")
    all_results = []
    
    for ticker in MASSIVE_TICKER_LIST:
        res = analyze_stock(ticker)
        if res: all_results.append(res)
        time.sleep(0.5) 
        
    # --- 1. Top 20 Long Term Value ---
    def sort_lt(x): return x['upsideLT'] if isinstance(x['upsideLT'], (int, float)) else -9999
    lt_results = sorted(all_results, key=sort_lt, reverse=True)[:20] # Strict TOP 20
    with open('daily_picks.json', 'w') as f:
        json.dump(lt_results, f, indent=2)

    # --- 2. Top 20 Short Term Swing ---
    def sort_st(x): return x['stScore'] if isinstance(x['stScore'], (int, float)) else -9999
    # Now it ranks securely by probability score regardless of volume glitches
    st_results = sorted(all_results, key=sort_st, reverse=True)[:20] # Strict TOP 20
    with open('swing_picks.json', 'w') as f:
        json.dump(st_results, f, indent=2)

    print("Successfully generated Top 20 daily_picks.json AND Top 20 swing_picks.json!")

if __name__ == "__main__":
    fetch_and_analyze()
