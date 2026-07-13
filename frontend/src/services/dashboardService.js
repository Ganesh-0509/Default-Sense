import api, { unwrap } from "./api";

export async function getSummary() {
  return unwrap(await api.get("/dashboard/summary"));
}

export async function getRiskDistribution() {
  return unwrap(await api.get("/dashboard/risk-distribution"));
}

export async function getHighRisk() {
  return unwrap(await api.get("/dashboard/high-risk"));
}

export async function getTrends() {
  return unwrap(await api.get("/dashboard/trends"));
}
