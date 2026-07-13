import api, { unwrap } from "./api";

export async function getOcrStatus() {
  return unwrap(await api.get("/ocr/status")); // { available, engine, version }
}

export async function uploadDocument({ customerId, documentType, file }) {
  const form = new FormData();
  form.append("customer_id", customerId);
  form.append("document_type", documentType);
  form.append("file", file);
  // Content-Type must be unset so the browser adds the multipart boundary itself.
  const res = await api.post("/documents/upload", form, {
    headers: { "Content-Type": undefined },
  });
  return unwrap(res); // { document_id, customer_id, document_type, file_name, upload_date }
}

export async function processOcr(documentId) {
  const res = await api.post("/ocr/process", { document_id: documentId });
  return unwrap(res); // { ocr_result_id, document_id, extracted_text, confidence_score, processed_at }
}

export async function getDocumentText(documentId) {
  return unwrap(await api.get(`/documents/${documentId}/text`));
}
