import api, { unwrap } from "./api";

export async function getGraphStatus() {
  return unwrap(await api.get("/graph/status")); // { available, engine }
}

export async function searchGraph(q, limit = 25) {
  return unwrap(await api.get("/graph/search", { params: { q, limit } }));
}

export async function getCustomerGraph(customerId) {
  // { customer_id, nodes:[{id,label,name,properties}], edges:[{id,type,source,target}], counts }
  return unwrap(await api.get(`/graph/customer/${customerId}`));
}

export async function getCustomerRisk(customerId) {
  // { customer, employer, industry, connected_defaulters, relationship_risk_score/level, factors, ... }
  return unwrap(await api.get(`/graph/risk/${customerId}`));
}
