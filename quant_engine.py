import React, { useState, useMemo, useEffect } from 'react';
import { Search, Activity, Briefcase, Zap } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('longTerm'); // 'longTerm' or 'shortTerm'
  const [ltData, setLtData] = useState([]);
  const [stData, setStData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [search, setSearch] = useState('');

  // Fetch both data feeds
  useEffect(() => {
    const fetchAllData = async () => {
      try {
        const [ltRes, stRes] = await Promise.all([
          fetch('https://raw.githubusercontent.com/Arshme35/AZ-Marketdata/main/daily_picks.json'),
          fetch('https://raw.githubusercontent.com/Arshme35/AZ-Marketdata/main/swing_picks.json')
        ]);
        
        if (ltRes.ok) setLtData(await ltRes.json());
        if (stRes.ok) setStData(await stRes.json());
        setIsLoading(false);
      } catch (error) {
        console.error("Data Fetch Error:", error);
        setIsLoading(false);
      }
    };
    fetchAllData();
  }, []);

  // Filter based on active tab
  const currentData = activeTab === 'longTerm' ? ltData : stData;
  const filteredData = useMemo(() => {
    if (!search) return currentData;
    return currentData.filter(s => 
      s.name.toLowerCase().includes(search.toLowerCase()) || 
      s.ticker.toLowerCase().includes(search.toLowerCase())
    );
  }, [currentData, search]);

  if (isLoading) {
    return (
      <div className="h-screen flex flex-col items-center justify-center bg-slate-50 font-sans">
        <Activity className="animate-spin text-blue-600 mb-4" size={48} />
        <h2 className="text-xl font-bold text-slate-700 uppercase tracking-widest">Loading Multi-Strategy Engine...</h2>
      </div>
    );
  }

  const formatNumber = (num) => {
    if (num === null || num === undefined || isNaN(num) || num === "N/A") return "N/A";
    return Number(num).toLocaleString('en-IN', { maximumFractionDigits: 1 });
  };

  return (
    <div className="min-h-screen bg-[#f8fafc] p-4 md:p-10 font-sans text-slate-900">
      <div className="max-w-[1700px] mx-auto">
        
        {/* Header & Tabs */}
        <header className="mb-12 flex flex-col lg:flex-row justify-between items-start lg:items-end gap-6">
          <div>
            <div className="flex items-center gap-4 mb-3">
              <h1 className="text-5xl font-black text-slate-900 tracking-tighter">Quant Desk <span className="text-blue-600">Pro</span></h1>
            </div>
            
            {/* Strategy Toggle */}
            <div className="flex bg-slate-200 p-1.5 rounded-xl w-fit mt-6">
              <button 
                onClick={() => setActiveTab('longTerm')}
                className={`flex items-center gap-2 px-6 py-3 rounded-lg font-bold text-sm transition-all ${activeTab === 'longTerm' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}
              >
                <Briefcase size={16} /> Long-Term Value
              </button>
              <button 
                onClick={() => setActiveTab('shortTerm')}
                className={`flex items-center gap-2 px-6 py-3 rounded-lg font-bold text-sm transition-all ${activeTab === 'shortTerm' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}
              >
                <Zap size={16} /> Short-Term / Swing
              </button>
            </div>
          </div>
          
          <div className="relative w-full lg:w-96 shadow-lg rounded-2xl overflow-hidden border border-slate-200">
            <Search className="absolute left-4 top-4 text-slate-400" size={20} />
            <input 
              type="text" 
              className="w-full pl-12 pr-6 py-4 bg-white border-none focus:ring-4 focus:ring-blue-500/20 text-md font-bold transition-all outline-none"
              placeholder="Search assets..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
        </header>

        {/* Master Data Grid */}
        <div className="bg-white rounded-[2rem] shadow-[0_20px_50px_rgba(0,0,0,0.05)] border border-slate-200 overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse min-w-[1600px]">
              
              {/* Dynamic Headers based on active strategy */}
              <thead>
                <tr className="text-[11px] uppercase font-black text-slate-400 tracking-[0.15em] border-b border-slate-100 bg-slate-50/50">
                  <th className="px-10 py-6">Asset & Rank</th>
                  <th className="px-4 py-6 text-right">CMP (₹)</th>
                  
                  {activeTab === 'longTerm' ? (
                    <>
                      <th className="px-4 py-6 text-right">P/E</th>
                      <th className="px-4 py-6 text-right">ROE %</th>
                      <th className="px-4 py-6 text-right">D/E</th>
                      <th className="px-4 py-6 text-right text-emerald-700 font-black">LT Upside</th>
                    </>
                  ) : (
                    <>
                      <th className="px-4 py-6 text-right text-blue-600 font-black">Vol Surge</th>
                      <th className="px-4 py-6 text-right">50 DMA</th>
                      <th className="px-4 py-6 text-right">% from 50DMA</th>
                      <th className="px-4 py-6 text-right text-purple-600 font-black">Momentum Score</th>
                    </>
                  )}

                  <th className="px-4 py-6 text-right">RSI</th>
                  <th className="px-4 py-6 text-right text-slate-500">52W L/H</th>
                  <th className="px-4 py-6 text-center">Action</th>
                  <th className="px-10 py-6 w-[350px]">System Catalyst / Reasoning</th>
                  <th className="px-8 py-6 w-[350px]">Latest News</th>
                </tr>
              </thead>

              <tbody className="divide-y divide-slate-50 text-sm">
                {filteredData.map((stock, idx) => (
                  <tr key={stock.id} className="hover:bg-blue-50/40 transition-colors group">
                    <td className="px-10 py-6">
                      <div className="flex items-center gap-5">
                        <span className="text-[10px] font-black text-slate-300">{(idx + 1).toString().padStart(2, '0')}</span>
                        <div>
                          <div className="font-black text-slate-900 text-base">{stock.name}</div>
                          <div className="text-[11px] text-blue-500 font-bold uppercase tracking-tight mt-1">
                            {stock.ticker} <span className="text-slate-300 mx-1">•</span> {stock.sector}
                          </div>
                        </div>
                      </div>
                    </td>
                    
                    <td className="px-4 py-6 text-right font-bold text-slate-800">
                      {stock.cmp === "N/A" ? "N/A" : `₹${formatNumber(stock.cmp)}`}
                    </td>

                    {/* Dynamic Table Data based on Strategy */}
                    {activeTab === 'longTerm' ? (
                      <>
                        <td className="px-4 py-6 text-right font-bold text-slate-600">{stock.pe === "N/A" ? "N/A" : `${stock.pe}x`}</td>
                        <td className="px-4 py-6 text-right font-black text-blue-600">{stock.roe === "N/A" ? "N/A" : `${stock.roe}%`}</td>
                        <td className="px-4 py-6 text-right text-slate-500 font-bold">{stock.debtEq}</td>
                        <td className="px-4 py-6 text-right font-black text-emerald-700 text-lg">
                          {stock.upsideLT === "N/A" ? "N/A" : `+${stock.upsideLT}%`}
                        </td>
                      </>
                    ) : (
                      <>
                        <td className="px-4 py-6 text-right font-black text-blue-600 text-lg">
                          {stock.volSurge === "N/A" ? "N/A" : `${stock.volSurge}x`}
                        </td>
                        <td className="px-4 py-6 text-right font-bold text-slate-500">
                           {stock.dma50 === "N/A" ? "N/A" : `₹${formatNumber(stock.dma50)}`}
                        </td>
                        <td className="px-4 py-6 text-right font-bold text-emerald-600">
                           {stock.dist50dma === "N/A" ? "N/A" : `${stock.dist50dma > 0 ? '+' : ''}${stock.dist50dma}%`}
                        </td>
                        <td className="px-4 py-6 text-right font-black text-purple-600 text-lg">
                          {stock.stScore}
                        </td>
                      </>
                    )}

                    <td className="px-4 py-6 text-right">
                      <span className={`px-2 py-1 rounded font-black text-xs ${stock.rsi === "N/A" ? 'bg-slate-100 text-slate-400' : stock.rsi > 70 ? 'bg-rose-100 text-rose-600' : 'bg-emerald-100 text-emerald-600'}`}>
                        {stock.rsi}
                      </span>
                    </td>
                    
                    <td className="px-4 py-6 text-right font-bold text-xs">
                      <div className="text-rose-500">L: {stock.low52 === "N/A" ? "N/A" : `₹${formatNumber(stock.low52)}`}</div>
                      <div className="text-emerald-500">H: {stock.high52 === "N/A" ? "N/A" : `₹${formatNumber(stock.high52)}`}</div>
                    </td>

                    <td className="px-4 py-6 text-center">
                      <span className={`px-5 py-2.5 rounded-xl text-[10px] font-black text-white shadow-sm tracking-widest ${
                        (activeTab === 'longTerm' ? stock.ltAction : stock.stAction) === 'BUY' || (activeTab === 'longTerm' ? stock.ltAction : stock.stAction) === 'MOMENTUM' ? 'bg-emerald-500' : 
                        'bg-blue-500' 
                      }`}>
                        {activeTab === 'longTerm' ? stock.ltAction : stock.stAction}
                      </span>
                    </td>

                    <td className="px-10 py-6">
                      <div className="text-[11px] leading-relaxed text-slate-600 bg-slate-50 p-4 rounded-2xl border border-slate-100 font-semibold italic">
                        {activeTab === 'longTerm' ? stock.reasoning : stock.stReasoning}
                      </div>
                    </td>

                    <td className="px-8 py-6">
                      <div className="text-[11px] leading-relaxed text-slate-700 font-medium line-clamp-3">
                        {stock.news}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
