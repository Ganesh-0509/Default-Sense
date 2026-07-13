import { useEffect, useState } from "react";
import { Brain, Loader2 } from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Cell,
  ResponsiveContainer,
  Tooltip,
} from "recharts";
import RiskBadge from "../components/RiskBadge";
import { getCustomers } from "../services/dataService";
import { runPrediction, getShap } from "../services/predictionService";
import { errorMessage } from "../services/api";

export default function Predictions() {
  const [customers, setCustomers] = useState([]);
  const [selected, setSelected] = useState("");
  const [running, setRunning] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);
  const [drivers, setDrivers] = useState([]);

  useEffect(() => {
    getCustomers({ limit: 100 })
      .then((d) => {
        setCustomers(d.items || []);
        if (d.items?.length) setSelected(d.items[0].customer_id);
      })
      .catch((err) => setError(errorMessage(err, "Could not load customers.")));
  }, []);

  const handleRun = async () => {
    if (!selected) return;
    setError("");
    setRunning(true);
    setResult(null);
    setDrivers([]);
    try {
      const prediction = await runPrediction(selected);
      setResult(prediction);
      const shap = await getShap(prediction.prediction_id);
      setDrivers(
        (shap || [])
          .map((s) => ({
            name: s.feature_name,
            value: Number(s.contribution),
            direction: s.impact_direction,
          }))
          .sort((a, b) => Math.abs(b.value) - Math.abs(a.value))
      );
    } catch (err) {
      setError(errorMessage(err, "Prediction failed."));
    } finally {
      setRunning(false);
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-800">AI Predictions</h1>
      <p className="mt-1 text-sm text-slate-500">12-month Probability of Default with SHAP explanation.</p>

      <div className="mt-6 flex flex-wrap items-end gap-3 rounded-xl border border-slate-200 bg-white p-5">
        <div className="flex-1 min-w-[220px]">
          <label className="mb-1 block text-sm font-medium text-slate-700">Customer</label>
          <select
            value={selected}
            onChange={(e) => setSelected(e.target.value)}
            className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
          >
            {customers.map((c) => (
              <option key={c.customer_id} value={c.customer_id}>
                {c.customer_name} ({c.employment_type || "—"})
              </option>
            ))}
          </select>
        </div>
        <button
          onClick={handleRun}
          disabled={running || !selected}
          className="flex items-center gap-2 rounded-lg bg-brand-600 px-5 py-2 text-sm font-semibold text-white hover:bg-brand-700 disabled:opacity-60"
        >
          {running ? <Loader2 className="h-4 w-4 animate-spin" /> : <Brain className="h-4 w-4" />}
          Run Prediction
        </button>
      </div>

      {error && (
        <div className="mt-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
          {error}
        </div>
      )}

      {result && (
        <div className="mt-6 grid grid-cols-1 gap-4 lg:grid-cols-3">
          <div className="rounded-xl border border-slate-200 bg-white p-6 text-center">
            <div className="text-sm text-slate-500">Probability of Default (12 mo)</div>
            <div className="mt-2 text-5xl font-bold text-slate-800">{result.probability_of_default}%</div>
            <div className="mt-3"><RiskBadge level={result.risk_level} /></div>
            <div className="mt-4 text-sm text-slate-500">
              Confidence: <span className="font-semibold text-slate-700">{result.confidence_score}%</span>
            </div>
            <div className="mt-1 text-sm font-medium text-brand-700">{result.recommendation}</div>
          </div>

          <div className="rounded-xl border border-slate-200 bg-white p-5 lg:col-span-2">
            <h2 className="text-sm font-semibold text-slate-700">Top Risk Drivers (SHAP)</h2>
            {drivers.length === 0 ? (
              <p className="mt-8 text-center text-xs text-slate-400">No SHAP data.</p>
            ) : (
              <ResponsiveContainer width="100%" height={260}>
                <BarChart data={drivers} layout="vertical" margin={{ left: 40 }}>
                  <XAxis type="number" tick={{ fontSize: 11 }} />
                  <YAxis type="category" dataKey="name" width={130} tick={{ fontSize: 11 }} />
                  <Tooltip />
                  <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                    {drivers.map((d) => (
                      <Cell key={d.name} fill={d.direction === "positive" ? "#dc2626" : "#16a34a"} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            )}
            <p className="mt-2 text-xs text-slate-400">
              Red pushes toward default; green pushes away.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
