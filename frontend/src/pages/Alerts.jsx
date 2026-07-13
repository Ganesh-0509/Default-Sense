import { useEffect, useState } from "react";
import { Bell, Loader2, Check } from "lucide-react";
import { getAlerts, markAlertRead } from "../services/alertService";
import { errorMessage } from "../services/api";

const SEVERITY_STYLES = {
  Low: "bg-green-100 text-green-800",
  Moderate: "bg-yellow-100 text-yellow-800",
  High: "bg-orange-100 text-orange-800",
  Critical: "bg-red-100 text-red-800",
};

export default function Alerts() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [alerts, setAlerts] = useState([]);
  const [busy, setBusy] = useState(null);

  const load = async () => {
    try {
      setAlerts(await getAlerts());
    } catch (err) {
      setError(errorMessage(err, "Could not load alerts."));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const handleRead = async (id) => {
    setBusy(id);
    try {
      const updated = await markAlertRead(id);
      setAlerts((prev) => prev.map((a) => (a.alert_id === id ? updated : a)));
    } catch (err) {
      setError(errorMessage(err, "Could not update alert."));
    } finally {
      setBusy(null);
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-800">Alerts</h1>

      <div className="mt-6 space-y-3">
        {loading ? (
          <div className="flex h-32 items-center justify-center text-slate-400">
            <Loader2 className="mr-2 h-5 w-5 animate-spin" /> Loading…
          </div>
        ) : error ? (
          <div className="rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div>
        ) : alerts.length === 0 ? (
          <div className="flex flex-col items-center justify-center rounded-xl border border-dashed border-slate-300 bg-white py-16 text-slate-400">
            <Bell className="h-8 w-8" />
            <p className="mt-2 text-sm">No alerts.</p>
          </div>
        ) : (
          alerts.map((a) => (
            <div
              key={a.alert_id}
              className="flex items-center justify-between rounded-xl border border-slate-200 bg-white p-4"
            >
              <div className="flex items-center gap-3">
                <span
                  className={`inline-flex rounded-full px-2.5 py-0.5 text-xs font-semibold ${
                    SEVERITY_STYLES[a.severity] || "bg-slate-100 text-slate-700"
                  }`}
                >
                  {a.severity}
                </span>
                <div>
                  <div className="text-sm font-medium text-slate-800">{a.alert_type}</div>
                  <div className="text-xs text-slate-500">{a.description}</div>
                </div>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-xs capitalize text-slate-400">{a.status}</span>
                {a.status === "open" && (
                  <button
                    onClick={() => handleRead(a.alert_id)}
                    disabled={busy === a.alert_id}
                    className="flex items-center gap-1 rounded-lg border border-slate-200 px-2.5 py-1 text-xs font-medium text-slate-600 hover:bg-slate-50 disabled:opacity-60"
                  >
                    {busy === a.alert_id ? (
                      <Loader2 className="h-3 w-3 animate-spin" />
                    ) : (
                      <Check className="h-3 w-3" />
                    )}
                    Mark read
                  </button>
                )}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
