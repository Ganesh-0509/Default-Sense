import api, { unwrap } from "./api";

export async function runPrediction(customerId, loanId = null) {
  return unwrap(await api.post("/predictions/run", { customer_id: customerId, loan_id: loanId }));
}

export async function getCustomerPredictions(customerId) {
  return unwrap(await api.get(`/predictions/customer/${customerId}`));
}

export async function getShap(predictionId) {
  return unwrap(await api.get(`/predictions/${predictionId}/shap`));
}

export async function getModelInfo() {
  return unwrap(await api.get("/predictions/model"));
}
