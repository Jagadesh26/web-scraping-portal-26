import { apiClient } from "@/core/api/apiClient";
import * as T from "../types";

export const authService = {
  register: async (data: Record<string, unknown>): Promise<T.User> => {
    const res = await apiClient.post<T.User>("/accounts/register/", data);
    return res.data;
  },

  login: async (data: Record<string, unknown>): Promise<T.LoginResponse> => {
    const res = await apiClient.post<T.LoginResponse>("/accounts/login/", data);
    return res.data;
  },

  logout: async (refreshToken: string): Promise<void> => {
    await apiClient.post("/accounts/logout/", { refresh: refreshToken });
  },

  logoutAll: async (): Promise<void> => {
    await apiClient.post("/accounts/logout-all/");
  },

  logoutSession: async (sessionId: string): Promise<void> => {
    await apiClient.post(`/accounts/sessions/${sessionId}/logout/`);
  },

  getMe: async (): Promise<T.User> => {
    const res = await apiClient.get<T.User>("/accounts/me/");
    return res.data;
  },

  forgotPassword: async (email: string): Promise<void> => {
    await apiClient.post("/accounts/forgot-password/", { email });
  },

  resetPassword: async (data: Record<string, unknown>): Promise<void> => {
    await apiClient.post("/accounts/reset-password/", data);
  },

  verifyEmail: async (token: string): Promise<void> => {
    await apiClient.post("/accounts/verify-email/", { token });
  },

  resendVerificationEmail: async (email: string): Promise<void> => {
    await apiClient.post("/accounts/resend-verification-email/", { email });
  },

  changePassword: async (data: Record<string, unknown>): Promise<void> => {
    await apiClient.post("/accounts/change-password/", data);
  },

  getSessions: async (): Promise<T.Session[]> => {
    const res = await apiClient.get<T.Session[]>("/accounts/sessions/");
    return res.data;
  },
};