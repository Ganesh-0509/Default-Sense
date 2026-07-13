import { useEffect, useRef, useState } from "react";
import { FileText, Loader2, UploadCloud, CheckCircle2, AlertTriangle } from "lucide-react";
import { getCustomers } from "../services/dataService";
import { getOcrStatus, uploadDocument, processOcr } from "../services/documentService";
import { errorMessage } from "../services/api";

const DOC_TYPES = [
  "Bank Statement",
  "Salary Slip",
  "ITR / Tax Return",
  "Loan Agreement",
  "KYC Document",
  "Other",
];

export default function Documents() {
  const [customers, setCustomers] = useState([]);
  const [selected, setSelected] = useState("");
  const [docType, setDocType] = useState(DOC_TYPES[0]);
  const [file, setFile] = useState(null);
  const [busy, setBusy] = useState(false);
  const [stage, setStage] = useState("");
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);
  const [engine, setEngine] = useState(null);
  const fileRef = useRef(null);

  useEffect(() => {
    getOcrStatus().then(setEngine).catch(() => setEngine({ available: false }));
    getCustomers({ limit: 100 })
      .then((d) => {
        setCustomers(d.items || []);
        if (d.items?.length) setSelected(d.items[0].customer_id);
      })
      .catch((err) => setError(errorMessage(err, "Could not load customers.")));
  }, []);

  const handleRun = async () => {
    if (!selected || !file) return;
    setError("");
    setResult(null);
    setBusy(true);
    try {
      setStage("Uploading document…");
      const doc = await uploadDocument({ customerId: selected, documentType: docType, file });
      setStage("Extracting text (Tesseract OCR)…");
      const ocr = await processOcr(doc.document_id);
      setResult({ doc, ocr });
      setStage("");
    } catch (err) {
      setError(errorMessage(err, "Upload or OCR failed."));
      setStage("");
    } finally {
      setBusy(false);
    }
  };

  const confidence =
    result?.ocr?.confidence_score != null ? Number(result.ocr.confidence_score) : null;

  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-800">Documents &amp; OCR</h1>
      <p className="mt-1 text-sm text-slate-500">
        Upload a borrower document and extract its text with Tesseract OCR — the unstructured
        intelligence layer feeding the risk model.
      </p>

      {engine && (
        <div
          className={`mt-4 flex items-center gap-2 rounded-lg border px-4 py-2.5 text-sm ${
            engine.available
              ? "border-green-200 bg-green-50 text-green-700"
              : "border-amber-200 bg-amber-50 text-amber-800"
          }`}
        >
          {engine.available ? (
            <>
              <CheckCircle2 className="h-4 w-4" />
              OCR engine online — Tesseract {engine.version || ""}
            </>
          ) : (
            <>
              <AlertTriangle className="h-4 w-4" />
              OCR engine unavailable on the server.
            </>
          )}
        </div>
      )}

      <div className="mt-6 grid grid-cols-1 gap-4 lg:grid-cols-2">
        {/* Upload form */}
        <div className="rounded-xl border border-slate-200 bg-white p-5">
          <h2 className="text-sm font-semibold text-slate-700">Upload</h2>

          <label className="mt-4 block text-sm font-medium text-slate-700">Customer</label>
          <select
            value={selected}
            onChange={(e) => setSelected(e.target.value)}
            className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
          >
            {customers.map((c) => (
              <option key={c.customer_id} value={c.customer_id}>
                {c.customer_name}
              </option>
            ))}
          </select>

          <label className="mt-4 block text-sm font-medium text-slate-700">Document type</label>
          <select
            value={docType}
            onChange={(e) => setDocType(e.target.value)}
            className="mt-1 w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-brand-500 focus:outline-none"
          >
            {DOC_TYPES.map((t) => (
              <option key={t} value={t}>
                {t}
              </option>
            ))}
          </select>

          <label className="mt-4 block text-sm font-medium text-slate-700">File</label>
          <div
            onClick={() => fileRef.current?.click()}
            className="mt-1 flex cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed border-slate-300 bg-slate-50 py-6 text-center hover:border-brand-400"
          >
            <UploadCloud className="h-7 w-7 text-slate-400" />
            <p className="mt-2 text-sm text-slate-600">
              {file ? file.name : "Click to choose an image (PNG, JPG, TIFF)"}
            </p>
            <input
              ref={fileRef}
              type="file"
              accept="image/png,image/jpeg,image/jpg,image/tiff"
              className="hidden"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
            />
          </div>

          <button
            onClick={handleRun}
            disabled={busy || !selected || !file}
            className="mt-5 flex w-full items-center justify-center gap-2 rounded-lg bg-brand-600 py-2.5 text-sm font-semibold text-white hover:bg-brand-700 disabled:opacity-60"
          >
            {busy ? <Loader2 className="h-4 w-4 animate-spin" /> : <FileText className="h-4 w-4" />}
            {busy ? stage || "Working…" : "Upload & Extract Text"}
          </button>

          {error && (
            <div className="mt-4 rounded-lg border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-700">
              {error}
            </div>
          )}
        </div>

        {/* Extraction result */}
        <div className="rounded-xl border border-slate-200 bg-white p-5">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-semibold text-slate-700">Extracted Text</h2>
            {confidence != null && (
              <span className="rounded-full bg-brand-50 px-2.5 py-0.5 text-xs font-semibold text-brand-700">
                {confidence.toFixed(1)}% confidence
              </span>
            )}
          </div>

          {!result ? (
            <p className="mt-10 text-center text-xs text-slate-400">
              The extracted text will appear here after processing.
            </p>
          ) : (
            <>
              <div className="mt-3 text-xs text-slate-400">
                {result.doc.file_name} · {result.doc.document_type}
              </div>
              <pre className="mt-2 max-h-[380px] overflow-auto whitespace-pre-wrap rounded-lg bg-slate-50 p-4 text-xs leading-relaxed text-slate-700">
                {result.ocr.extracted_text?.trim() || "(No text detected in this image.)"}
              </pre>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
