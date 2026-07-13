import { useEffect, useState } from "react";
import { Loader2, Landmark } from "lucide-react";
import { getLoans } from "../services/dataService";
import { errorMessage } from "../services/api";

const STATUS_STYLES = {
  Active: "bg-green-100 text-green-800",
  Closed: "bg-slate-100 text-slate-700",
  Overdue: "bg-orange-100 text-orange-800",
  Defaulted: "bg-red-100 text-red-800",
};

export default function Loans() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [rows, setRows] = useState([]);
  const [total, setTotal] = useState(0);

  useEffect(() => {
    let active = true;
    (async () => {
      try {
        const data = await getLoans({ limit: 50 });
        if (!active) return;
        setRows(data.items || []);
        setTotal(data.total ?? 0);
      } catch (err) {
        if (active) setError(errorMessage(err, "Could not load loans."));
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
        <h1 className="text-2xl font-bold text-slate-800">Loans</h1>
        {!loading && !error && <span className="text-sm text-slate-500">{total} total</span>}
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
            <Landmark className="h-8 w-8" />
            <p className="mt-2 text-sm">No loans yet.</p>
          </div>
        ) : (
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-50 text-xs uppercase text-slate-500">
              <tr>
                <th className="px-4 py-3">Type</th>
                <th className="px-4 py-3">Amount</th>
                <th className="px-4 py-3">EMI</th>
                <th className="px-4 py-3">Outstanding</th>
                <th className="px-4 py-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {rows.map((l) => (
                <tr key={l.loan_id} className="hover:bg-slate-50">
                  <td className="px-4 py-3 font-medium text-slate-800">{l.loan_type}</td>
                  <td className="px-4 py-3 text-slate-600">
                    ₹{Number(l.loan_amount).toLocaleString("en-IN")}
                  </td>
                  <td className="px-4 py-3 text-slate-600">
                    ₹{Number(l.emi).toLocaleString("en-IN")}
                  </td>
                  <td className="px-4 py-3 text-slate-600">
                    ₹{Number(l.outstanding_amount).toLocaleString("en-IN")}
                  </td>
                  <td className="px-4 py-3">
                    <span
                      className={`inline-flex rounded-full px-2.5 py-0.5 text-xs font-semibold ${
                        STATUS_STYLES[l.loan_status] || "bg-slate-100 text-slate-700"
                      }`}
                    >
                      {l.loan_status}
                    </span>
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
