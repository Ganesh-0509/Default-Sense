import { create } from "zustand";
import { persist } from "zustand/middleware";

// Auth state persisted to localStorage so a refresh keeps the session.
export const useAuthStore = create(
  persist(
    (set, get) => ({
      token: null,
      user: null,
      setAuth: (token, user) => set({ token, user }),
      setUser: (user) => set({ user }),
      logout: () => set({ token: null, user: null }),
      isAuthenticated: () => Boolean(get().token),
    }),
    { name: "defaultsense-auth" }
  )
);
