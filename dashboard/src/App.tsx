import { useState, useEffect } from 'react';
import {
  AreaChart, Area, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  BarChart, Bar
} from 'recharts';
import {
  TrendingUp, Activity, PieChart, Users, Download, ChevronUp
} from 'lucide-react';
import './App.css';

const inflowData = [
  { name: 'Equity', amount: 4500 },
  { name: 'Debt', amount: 3000 },
  { name: 'Hybrid', amount: 2000 },
  { name: 'Liquid', amount: 2780 },
];

const topFunds = [
  { id: 1, name: 'HDFC Top 100 Direct', category: 'Large Cap', aum: '₹34,500 Cr', return1y: '+24.5%', risk: 'High' },
  { id: 2, name: 'SBI Bluechip', category: 'Large Cap', aum: '₹42,100 Cr', return1y: '+21.2%', risk: 'High' },
  { id: 3, name: 'Axis Midcap', category: 'Mid Cap', aum: '₹18,200 Cr', return1y: '+32.1%', risk: 'Very High' },
  { id: 4, name: 'Kotak Liquid', category: 'Debt', aum: '₹55,000 Cr', return1y: '+7.2%', risk: 'Low' },
];

const SCHEMES = [
  { id: "125497", name: "HDFC Top 100 Direct" },
  { id: "119551", name: "SBI Bluechip" },
  { id: "120503", name: "ICICI Bluechip" },
  { id: "118632", name: "Nippon Large Cap" },
  { id: "119092", name: "Axis Bluechip" },
  { id: "120841", name: "Kotak Bluechip" },
];

function App() {
  const [navData, setNavData] = useState<any[]>([]);
  const [latestNav, setLatestNav] = useState<string>("Loading...");
  const [fundName, setFundName] = useState<string>("Loading...");
  const [selectedScheme, setSelectedScheme] = useState<string>("125497");
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchLiveData = async () => {
      setLoading(true);
      try {
        const response = await fetch(`https://api.mfapi.in/mf/${selectedScheme}`);
        const json = await response.json();

        if (json && json.data && json.data.length > 0) {
          if (json.meta && json.meta.scheme_name) {
            setFundName(json.meta.scheme_name);
          }

          // Take the last 30 days of NAV data and reverse it to be chronological
          const recentData = json.data.slice(0, 30).reverse().map((item: any) => ({
            name: item.date.substring(0, 5), // short date (DD-MM)
            value: parseFloat(item.nav),
            // Simulated benchmark just for the chart visualization comparison
            benchmark: parseFloat(item.nav) * 0.97
          }));

          setNavData(recentData);
          setLatestNav("₹" + parseFloat(json.data[0].nav).toFixed(2));
        }
      } catch (error) {
        console.error("Failed to fetch live API data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchLiveData();
  }, [selectedScheme]); // Re-run effect whenever selectedScheme changes

  return (
    <div className="dashboard-container">
      {/* Header */}
      <header className="header animate-fade-in">
        <div className="header-title">
          <h1>Mutual Funds Intelligence</h1>
          <p>Real-time analytics and performance monitoring</p>
        </div>
        <div className="header-actions">
          <select
            className="scheme-selector btn"
            style={{ backgroundColor: 'rgba(30, 41, 59, 0.9)', color: 'white', borderColor: 'rgba(255, 255, 255, 0.2)' }}
            value={selectedScheme}
            onChange={(e) => setSelectedScheme(e.target.value)}
          >
            {SCHEMES.map(scheme => (
              <option key={scheme.id} value={scheme.id}>
                {scheme.name} ({scheme.id})
              </option>
            ))}
          </select>
          <button className="btn btn-primary"><Download size={18} /> Export Report</button>
        </div>
      </header>

      {/* KPI Cards */}
      <div className="kpi-grid">
        <div className="glass-panel kpi-card animate-fade-in delay-100">
          <div className="kpi-header">
            Live NAV
            <div className="kpi-icon"><Activity size={20} /></div>
          </div>
          <div className="kpi-value">{loading ? "..." : latestNav}</div>
          <div className="kpi-trend trend-up" style={{ fontSize: '11px', lineHeight: '1.2' }}>
            <TrendingUp size={14} style={{ flexShrink: 0 }} />
            <span style={{ whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
              {loading ? "Fetching..." : fundName}
            </span>
          </div>
        </div>

        <div className="glass-panel kpi-card animate-fade-in delay-200">
          <div className="kpi-header">
            Active Folios
            <div className="kpi-icon"><Users size={20} /></div>
          </div>
          <div className="kpi-value">14.8M</div>
          <div className="kpi-trend trend-up">
            <TrendingUp size={16} /> +4.2% vs last month
          </div>
        </div>

        <div className="glass-panel kpi-card animate-fade-in delay-300">
          <div className="kpi-header">
            Total AUM (Platform)
            <div className="kpi-icon"><PieChart size={20} /></div>
          </div>
          <div className="kpi-value">₹4.2L Cr</div>
          <div className="kpi-trend trend-up">
            <ChevronUp size={16} /> +12.5% vs last year
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="charts-grid">
        <div className="glass-panel chart-panel animate-fade-in delay-100">
          <h3 style={{ fontSize: '14px' }}><Activity size={20} className="text-accent" /> {loading ? "Loading..." : fundName} - Live 30 Day Trend</h3>
          <div className="chart-container">
            {!loading && navData.length > 0 ? (
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={navData}>
                  <defs>
                    <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" vertical={false} />
                  <XAxis dataKey="name" stroke="#94a3b8" tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={false} />
                  <YAxis stroke="#94a3b8" tick={{ fill: '#94a3b8', fontSize: 12 }} axisLine={false} tickLine={false} domain={['dataMin - 2', 'dataMax + 2']} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#1e293b', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px' }}
                    labelStyle={{ color: '#94a3b8' }}
                  />
                  <Area type="monotone" dataKey="value" stroke="#3b82f6" strokeWidth={3} fillOpacity={1} fill="url(#colorValue)" name="Live NAV" />
                  <Line type="monotone" dataKey="benchmark" stroke="#94a3b8" strokeWidth={2} strokeDasharray="5 5" dot={false} name="Benchmark" />
                </AreaChart>
              </ResponsiveContainer>
            ) : (
              <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%', color: '#94a3b8' }}>
                Fetching live API data...
              </div>
            )}
          </div>
        </div>

        <div className="glass-panel chart-panel animate-fade-in delay-200">
          <h3><PieChart size={20} className="text-accent" /> Inflows by Category (Cr)</h3>
          <div className="chart-container">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={inflowData} layout="vertical" margin={{ top: 0, right: 0, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" horizontal={true} vertical={false} />
                <XAxis type="number" stroke="#94a3b8" hide />
                <YAxis dataKey="name" type="category" stroke="#94a3b8" axisLine={false} tickLine={false} width={60} />
                <Tooltip
                  cursor={{ fill: 'rgba(255,255,255,0.05)' }}
                  contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px' }}
                />
                <Bar dataKey="amount" fill="#8b5cf6" radius={[0, 4, 4, 0]} barSize={24} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Table Section */}
      <div className="glass-panel table-panel animate-fade-in delay-300">
        <div className="table-header">
          <h3>Top Performing Schemes</h3>
          <button className="btn">View All</button>
        </div>
        <div className="table-responsive">
          <table className="custom-table">
            <thead>
              <tr>
                <th>Scheme Name</th>
                <th>AUM</th>
                <th>1Y Return</th>
                <th>Risk Profile</th>
              </tr>
            </thead>
            <tbody>
              {topFunds.map((fund) => (
                <tr key={fund.id}>
                  <td>
                    <div className="fund-name">{fund.name}</div>
                    <div className="fund-category">{fund.category}</div>
                  </td>
                  <td>{fund.aum}</td>
                  <td className="trend-up font-medium">{fund.return1y}</td>
                  <td>
                    <span className={`badge ${fund.risk.includes('High') ? 'badge-high' : 'badge-low'}`}>
                      {fund.risk}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default App;
