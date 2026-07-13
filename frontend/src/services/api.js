import axios from "axios";
import { useAuthStore } from "../store/authStore";

// Base URL: uses the Vite dev proxy (/api → backend) by default; override with
// VITE_API_URL for a deployed backend.
const baseURL = import.meta.env.VITE_API_URL || "/api/v1";

const api = axios.create({ baseURL, headers: { "Content-Type": "application/json" } });

// Attach the JWT to every request.
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// On 401, clear the session so the router redirects to /login.
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
    }
    return Promise.reject(error);
  }
);

// Unwrap the backend envelope { success, message, data }.
export function unwrap(response) {
  return response.data?.data;
}

// Extract a human-readable message from an error envelope.
export function errorMessage(error, fallback = "Something went wrong.") {
  return error?.response?.data?.message || error?.message || fallback;
}

export default api;
