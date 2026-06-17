"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { authService } from "../api/authService";
import { useAuthStore } from "../store/authStore";
import * as React from "react";

// 1. Current User Query Hook (with TanStack v5 Effect Synchronization)
export function useCurrentUser() {
  const { isAuthenticated, setUser, logout } = useAuthStore();

  const query = useQuery({
    queryKey: ["auth", "current-user-context"],
    queryFn: authService.getMe,
    enabled: isAuthenticated,
    staleTime: 5 * 60 * 1000,
    gcTime: 15 * 60 * 1000,
    retry: false,
  });

  React.useEffect(() => {
    if (query.data) {
      setUser(query.data);
    } else if (query.error) {
      logout();
    }
  }, [query.data, query.error, setUser, logout]);

  return query;
}

// 2. Authentication Mutations & Session Hooks
export function useLogin() {
  const setTokens = useAuthStore((state) => state.setTokens);
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: authService.login,
    onSuccess: (data) => {
      setTokens(data.tokens);
      queryClient.setQueryData(["auth", "current-user-context"], data.user);
    },
  });
}

export function useRegister() {
  return useMutation({
    mutationFn: authService.register,
  });
}

export function useLogout() {
  const queryClient = useQueryClient();
  const { refreshToken, clearAuth } = useAuthStore();

  return useMutation({
    mutationFn: async () => {
      if (refreshToken) await authService.logout(refreshToken);
    },
    onSettled: () => {
      clearAuth();
      queryClient.clear();
    },
  });
}

export function useLogoutAll() {
  const queryClient = useQueryClient();
  const clearAuth = useAuthStore((state) => state.clearAuth);

  return useMutation({
    mutationFn: authService.logoutAll,
    onSettled: () => {
      clearAuth();
      queryClient.clear();
    },
  });
}

export function useLogoutSession() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (sessionId: string) => authService.logoutSession(sessionId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["auth", "user-sessions-matrix"] });
    },
  });
}

export function useForgotPassword() {
  return useMutation({
    mutationFn: (email: string) => authService.forgotPassword(email),
  });
}

export function useResetPassword() {
  return useMutation({
    mutationFn: authService.resetPassword,
  });
}

export function useVerifyEmail() {
  return useMutation({
    mutationFn: (token: string) => authService.verifyEmail(token),
  });
}

export function useResendVerificationEmail() {
  return useMutation({
    mutationFn: (email: string) => authService.resendVerificationEmail(email),
  });
}

export function useChangePassword() {
  return useMutation({
    mutationFn: authService.changePassword,
  });
}

export function useSessions() {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);

  return useQuery({
    queryKey: ["auth", "user-sessions-matrix"],
    queryFn: authService.getSessions,
    enabled: isAuthenticated,
    staleTime: 60 * 1000,
  });
}