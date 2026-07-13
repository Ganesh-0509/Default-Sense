import api, { unwrap } from "./api";

export async function login(email, password) {
  const res = await api.post("/auth/login", { email, password });
  return unwrap(res); // { access_token, token_type, expires_in, user }
}

export async function fetchProfile() {
  const res = await api.get("/auth/profile");
  return unwrap(res); // user object
}

export async function changePassword(currentPassword, newPassword) {
  const res = await api.post("/auth/change-password", {
    current_password: currentPassword,
    new_password: newPassword,
  });
  return res.data;
}
