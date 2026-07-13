import api, { unwrap } from "./api";

export async function getCustomers({ skip = 0, limit = 50 } = {}) {
  const res = await api.get("/customers", { params: { skip, limit } });
  return unwrap(res); // { items, total, skip, limit }
}

export async function getLoans({ skip = 0, limit = 50 } = {}) {
  const res = await api.get("/loans", { params: { skip, limit } });
  return unwrap(res); // { items, total, skip, limit }
}
