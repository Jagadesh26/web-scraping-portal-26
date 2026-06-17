import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import { AuthState, AuthTokens, User } from "../types";

// Helper to update edge-accessible tracking cookie
const setSessionCookie = (value: boolean) => {
  if (typeof document !== "undefined") {
    document.cookie = `talentai_has_session=${value}; path=/; max-age=${value ? 604800 : 0}; SameSite=Strict; Secure`;
  }
};

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,
      isInitialized: false,

      initializeAuth: () => {
        if (get().isInitialized) return;
        const hasAccess = !!get().accessToken;
        setSessionCookie(hasAccess);
        set({ isInitialized: true, isAuthenticated: hasAccess });
      },

      setTokens: (tokens: AuthTokens) => {
        setSessionCookie(true);
        set({
          accessToken: tokens.access,
          refreshToken: tokens.refresh,
          isAuthenticated: true,
        });
      },

      setUser: (user: User) => set({ user }),

      clearAuth: () => {
        setSessionCookie(false);
        set({
          user: null,
          accessToken: null,
          refreshToken: null,
          isAuthenticated: false,
        });
      },

      logout: () => {
        get().clearAuth();
      },
    }),
    {
      name: "talentai-secure-auth-vault",
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        user: state.user,
        accessToken: state.accessToken,
        refreshToken: state.refreshToken,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);