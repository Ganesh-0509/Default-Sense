import { useEffect, useState } from "react";
import { Users, Landmark, AlertTriangle, Activity, Loader2 } from "lucide-react";
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Legend,
  Tooltip,
  BarChart,
  Bar,
  XAxis,
  YAxis,
} from "recharts";
import KpiCard from "../components/KpiCard";
import RiskBadge from "../components/RiskBadge";
import { getSummary, getRiskDistribution, getHighRisk } from "../services/dashboardService";
import { errorMessage } from "../services/api";

const RISK_COLORS = { Low: "#16a34a", Moderate: "#eab308", High: "#f97316", Critical: "#dc2626" };

export default function Dashboard() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [summary, setSummary] = useState(null);
  const [dist, setDist] = useState({});
  const [highRisk, setHighRisk] = useState([]);

  useEffect(() => {
    let active = true;
    (async () => {
      try {
        const [s, d, h] = await Promise.all([getSummary(), getRiskDistribution(), getHighRisk()]);
        if (!active) return;
        setSummary(s);
        setDist(d.distribution || {});
        setHighRisk(h || []);
      } catch (err) {
        if (active) setError(errorMessage(err, "Could not load dashboard."));
      } finally {
        if (active) setLoading(false);
      }
    })();
    return () => {
      active = false;
    };
  }, []);

  if (loading) {
    return (
      <div className="flex h-64 items-center justify-center text-slate-400">
        <Loader2 className="mr-2 h-5 w-5 animate-spin" /> Loading dashboard…
      </div>
    );
  }
  if (error) {
    return <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div>;
  }

  const pieData = Object.entries(dist)
    .filter(([, v]) => v > 0)
    .map(([name, value]) => ({ name, value }));

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-800">Dashboard</h1>
      <p className="mt-1 text-sm text-slate-500">Portfolio risk overview.</p>

      <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <KpiCard label="Total Customers" value={summary.total_customers} icon={Users} />
        <KpiCard label="Active Loans" value={summary.active_loans} icon={Activity} accent="text-risk-low" />
        <KpiCard
          label="High-Risk Borrowers"
          value={summary.high_risk_borrowers}
          icon={AlertTriangle}
          accent="text-risk-high"
        />
        <KpiCard
          label="Average PD"
          value={summary.average_pd != null ? `${summary.average_pd}%` : "—"}
          icon={Landmark}
          hint={`${summary.customers_scored} scored`}
        />
      </div>

      <div className="mt-6 grid grid-cols-1 gap-4 lg:grid-cols-2">
        <div className="rounded-xl border border-slate-200 bg-white p-5">
          <h2 className="text-sm font-semibold text-slate-700">Risk Distribution</h2>
          {pieData.length === 0 ? (
            <p className="mt-8 text-center text-xs text-slate-400">
              No predictions yet. Run predictions to populate this chart.
            </p>
          ) : (
            <ResponsiveContainer width="100%" height={240}>
              <PieChart>
                <Pie data={pieData} dataKey="value" nameKey="name" innerRadius={50} outerRadius={85} paddingAngle={2}>
                  {pieData.map((entry) => (
                    <Cell key={entry.name} fill={RISK_COLORS[entry.name] || "#94a3b8"} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          )}
        </div>

        <div className="rounded-xl border border-slate-200 bg-white p-5">
          <h2 className="text-sm font-semibold text-slate-700">Risk Tiers</h2>
          {pieData.length === 0 ? (
            <p className="mt-8 text-center text-xs text-slate-400">No data.</p>
          ) : (
            <ResponsiveContainer width="100%" height={240}>
              <BarChart data={pieData}>
                <XAxis dataKey="name" tick={{ fontSize: 12 }} />
                <YAxis allowDecimals={false} tick={{ fontSize: 12 }} />
                <Tooltip />
                <Bar dataKey="value" radius={[4, 4, 0, 0]}>
                  {pieData.map((entry) => (
                    <Cell key={entry.name} fill={RISK_COLORS[entry.name] || "#94a3b8"} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      <div className="mt-6 rounded-xl border border-slate-200 bg-white">
        <h2 className="border-b border-slate-100 px-5 py-3 text-sm font-semibold text-slate-700">
          High-Risk Borrowers
        </h2>
        {highRisk.length === 0 ? (
          <p className="px-5 py-8 text-center text-sm text-slate-400">No high-risk borrowers.</p>
        ) : (
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-50 text-xs uppercase text-slate-500">
              <tr>
                <th className="px-5 py-2">Customer</th>
                <th className="px-5 py-2">PD</th>
                <th className="px-5 py-2">Risk</th>
                <th className="px-5 py-2">Recommendation</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {highRisk.map((r) => (
                <tr key={r.customer_id} className="hover:bg-slate-50">
                  <td className="px-5 py-2 font-medium text-slate-800">{r.customer_name}</td>
                  <td className="px-5 py-2 text-slate-600">{r.probability_of_default}%</td>
                  <td className="px-5 py-2"><RiskBadge level={r.risk_level} /></td>
                  <td className="px-5 py-2 text-slate-600">{r.recommendation}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
