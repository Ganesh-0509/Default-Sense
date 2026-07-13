import { useEffect, useState } from "react";
import { Loader2, Users } from "lucide-react";
import { getCustomers } from "../services/dataService";
import { errorMessage } from "../services/api";

export default function Customers() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [rows, setRows] = useState([]);
  const [total, setTotal] = useState(0);

  useEffect(() => {
    let active = true;
    (async () => {
      try {
        const data = await getCustomers({ limit: 50 });
        if (!active) return;
        setRows(data.items || []);
        setTotal(data.total ?? 0);
      } catch (err) {
        if (active) setError(errorMessage(err, "Could not load customers."));
      } finally {
        if (active) setLoading(false);
      }
    })();
    return () => {
      active = false;
    };
  }, []);

  return (
    <div>
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-slate-800">Customers</h1>
        {!loading && !error && (
          <span className="text-sm text-slate-500">{total} total</span>
        )}
      </div>

      <div className="mt-6 overflow-hidden rounded-xl border border-slate-200 bg-white">
        {loading ? (
          <div className="flex h-40 items-center justify-center text-slate-400">
            <Loader2 className="mr-2 h-5 w-5 animate-spin" /> Loading…
          </div>
        ) : error ? (
          <div className="px-4 py-3 text-sm text-red-700">{error}</div>
        ) : rows.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-16 text-slate-400">
            <Users className="h-8 w-8" />
            <p className="mt-2 text-sm">No customers yet.</p>
          </div>
        ) : (
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-50 text-xs uppercase text-slate-500">
              <tr>
                <th className="px-4 py-3">Name</th>
                <th className="px-4 py-3">Employment</th>
                <th className="px-4 py-3">Credit Score</th>
                <th className="px-4 py-3">Region</th>
                <th className="px-4 py-3">Income</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {rows.map((c) => (
                <tr key={c.customer_id} className="hover:bg-slate-50">
                  <td className="px-4 py-3 font-medium text-slate-800">{c.customer_name}</td>
                  <td className="px-4 py-3 text-slate-600">{c.employment_type || "—"}</td>
                  <td className="px-4 py-3 text-slate-600">{c.credit_score ?? "—"}</td>
                  <td className="px-4 py-3 text-slate-600">{c.region || "—"}</td>
                  <td className="px-4 py-3 text-slate-600">
                    {c.annual_income ? `₹${Number(c.annual_income).toLocaleString("en-IN")}` : "—"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
