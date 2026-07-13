import { useEffect, useState } from "react";
import { Users, Landmark, AlertTriangle, Activity, Loader2 } from "lucide-react";
import KpiCard from "../components/KpiCard";
import { getCustomers, getLoans } from "../services/dataService";
import { errorMessage } from "../services/api";

export default function Dashboard() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [stats, setStats] = useState({ customers: 0, loans: 0, activeLoans: 0, atRisk: 0 });

  useEffect(() => {
    let active = true;
    (async () => {
      try {
        const [customers, loans] = await Promise.all([
          getCustomers({ limit: 1 }),
          getLoans({ limit: 200 }),
        ]);
        if (!active) return;
        const items = loans.items || [];
        setStats({
          customers: customers.total ?? 0,
          loans: loans.total ?? 0,
          activeLoans: items.filter((l) => l.loan_status === "Active").length,
          atRisk: items.filter((l) => ["Overdue", "Defaulted"].includes(l.loan_status)).length,
        });
      } catch (err) {
        if (active) setError(errorMessage(err, "Could not load dashboard data."));
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
    return (
      <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
        {error}
      </div>
    );
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-800">Dashboard</h1>
      <p className="mt-1 text-sm text-slate-500">Portfolio overview at a glance.</p>

      <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <KpiCard label="Total Customers" value={stats.customers} icon={Users} />
        <KpiCard label="Total Loans" value={stats.loans} icon={Landmark} />
        <KpiCard
          label="Active Loans"
          value={stats.activeLoans}
          icon={Activity}
          accent="text-risk-low"
        />
        <KpiCard
          label="At-Risk Loans"
          value={stats.atRisk}
          icon={AlertTriangle}
          accent="text-risk-high"
          hint="Overdue or defaulted"
        />
      </div>

      <div className="mt-6 grid grid-cols-1 gap-4 lg:grid-cols-2">
        <div className="rounded-xl border border-dashed border-slate-300 bg-white p-6">
          <h2 className="text-sm font-semibold text-slate-700">Portfolio Risk Distribution</h2>
          <p className="mt-2 text-xs text-slate-400">
            Charts populate once the AI engine runs (Phase 6) and dashboard APIs land (Phase 7).
          </p>
        </div>
        <div className="rounded-xl border border-dashed border-slate-300 bg-white p-6">
          <h2 className="text-sm font-semibold text-slate-700">Average 12-Month PD</h2>
          <p className="mt-2 text-xs text-slate-400">
            Prediction metrics appear after the ML prediction engine is built.
          </p>
        </div>
      </div>
    </div>
  );
}
