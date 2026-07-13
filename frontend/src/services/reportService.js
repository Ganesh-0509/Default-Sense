import api, { unwrap } from "./api";

export async function getPortfolioReport() {
  return unwrap(await api.get("/reports/portfolio"));
}

// Download a binary export (CSV/PDF) via a blob and trigger a browser save.
async function download(path, filename) {
  const res = await api.get(path, { responseType: "blob" });
  const url = window.URL.createObjectURL(new Blob([res.data]));
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  link.remove();
  window.URL.revokeObjectURL(url);
}

export function exportCsv() {
  return download("/reports/export/csv", "portfolio_report.csv");
}

export function exportPdf() {
  return download("/reports/export/pdf", "portfolio_report.pdf");
}
