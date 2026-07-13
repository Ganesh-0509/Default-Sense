import api, { unwrap } from "./api";

export async function getAlerts(status = null) {
  return unwrap(await api.get("/alerts", { params: status ? { status } : {} }));
}

export async function markAlertRead(alertId) {
  return unwrap(await api.put(`/alerts/${alertId}/read`));
}
