import { useEffect, useState } from "react";
import { FileText, FileDown, Loader2 } from "lucide-react";
import { getPortfolioReport, exportCsv, exportPdf } from "../services/reportService";
import { errorMessage } from "../services/api";

export default function Reports() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [report, setReport] = useState(null);
  const [downloading, setDownloading] = useState("");

  useEffect(() => {
    getPortfolioReport()
      .then(setReport)
      .catch((err) => setError(errorMessage(err, "Could not load report.")))
      .finally(() => setLoading(false));
  }, []);

  const handleExport = async (kind) => {
    setDownloading(kind);
    try {
      await (kind === "csv" ? exportCsv() : exportPdf());
    } catch (err) {
      setError(errorMessage(err, "Export failed."));
    } finally {
      setDownloading("");
    }
  };

  return (
    <div>
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-slate-800">Reports</h1>
        <div className="flex gap-2">
          <button
            onClick={() => handleExport("csv")}
            disabled={downloading === "csv"}
            className="flex items-center gap-2 rounded-lg border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 disabled:opacity-60"
          >
            {downloading === "csv" ? <Loader2 className="h-4 w-4 animate-spin" /> : <FileDown className="h-4 w-4" />}
            Export CSV
          </button>
          <button
            onClick={() => handleExport("pdf")}
            disabled={downloading === "pdf"}
            className="flex items-center gap-2 rounded-lg bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700 disabled:opacity-60"
          >
            {downloading === "pdf" ? <Loader2 className="h-4 w-4 animate-spin" /> : <FileText className="h-4 w-4" />}
            Export PDF
          </button>
        </div>
      </div>

      {loading ? (
        <div className="mt-6 flex h-32 items-center justify-center text-slate-400">
          <Loader2 className="mr-2 h-5 w-5 animate-spin" /> Loading…
        </div>
      ) : error ? (
        <div className="mt-6 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">{error}</div>
      ) : (
        report && (
          <div className="mt-6 space-y-6">
            <div className="grid grid-cols-2 gap-4 sm:grid-cols-4">
              {[
                ["Customers", report.summary.total_customers],
                ["Loans", report.summary.total_loans],
                ["High-Risk", report.summary.high_risk_borrowers],
                ["Avg PD", report.summary.average_pd != null ? `${report.summary.average_pd}%` : "—"],
              ].map(([label, value]) => (
                <div key={label} className="rounded-xl border border-slate-200 bg-white p-4">
                  <div className="text-xs text-slate-500">{label}</div>
                  <div className="mt-1 text-2xl font-bold text-slate-800">{value}</div>
                </div>
              ))}
            </div>

            <div className="rounded-xl border border-slate-200 bg-white">
              <h2 className="border-b border-slate-100 px-5 py-3 text-sm font-semibold text-slate-700">
                High-Risk Borrowers
              </h2>
              {report.high_risk.length === 0 ? (
                <p className="px-5 py-8 text-center text-sm text-slate-400">None.</p>
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
                    {report.high_risk.map((r) => (
                      <tr key={r.customer_id}>
                        <td className="px-5 py-2 font-medium text-slate-800">{r.customer_name}</td>
                        <td className="px-5 py-2 text-slate-600">{r.probability_of_default}%</td>
                        <td className="px-5 py-2 text-slate-600">{r.risk_level}</td>
                        <td className="px-5 py-2 text-slate-600">{r.recommendation}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              )}
            </div>
          </div>
        )
      )}
    </div>
  );
}
