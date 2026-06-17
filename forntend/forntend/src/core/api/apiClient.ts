import axios, { AxiosError, InternalAxiosRequestConfig } from "axios";
import { useAuthStore } from "@/features/auth/store/authStore";

export const apiClient = axios.create({
  baseURL: "http://localhost:8000/api",
  headers: {
    "Content-Type": "application/json",
  },
  timeout: 15000,
});

let isRefreshing = false;
let failedQueue: Array<{
  resolve: (token: string) => void;
  reject: (error: unknown) => void;
}> = [];

const processQueue = (error: unknown, token: string | null = null) => {
  failedQueue.forEach((item) => {
    if (token) item.resolve(token);
    else item.reject(error);
  });
  failedQueue = [];
};

apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = useAuthStore.getState().accessToken;
    if (token && config.headers && !config.headers.Authorization) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retryCount?: number };

    if (!originalRequest) {
      return Promise.reject(error);
    }

    // Initialize or increment retry counter to catch and kill circular loops
    originalRequest._retryCount = originalRequest._retryCount ?? 0;

    if (error.response?.status === 401 && !originalRequest.url?.includes("/accounts/login/")) {
      
      // Infinite loop block: break execution if single retry step has already been evaluated
      if (originalRequest._retryCount >= 1) {
        useAuthStore.getState().clearAuth();
        return Promise.reject(error);
      }

      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject });
        })
          .then((token) => {
            if (originalRequest.headers) {
              originalRequest.headers.Authorization = `Bearer ${token}`;
            }
            originalRequest._retryCount! += 1;
            return apiClient(originalRequest);
          })
          .catch((err) => Promise.reject(err));
      }

      isRefreshing = true;
      const currentRefreshToken = useAuthStore.getState().refreshToken;

      if (!currentRefreshToken) {
        isRefreshing = false;
        useAuthStore.getState().clearAuth();
        return Promise.reject(error);
      }

      try {
        const refreshResponse = await axios.post("http://localhost:8000/api/accounts/token/refresh/", {
          refresh: currentRefreshToken,
        });

        const { access, refresh } = refreshResponse.data;
        
        // Update store with structural parameters received from Django server
        useAuthStore.getState().setTokens({ 
          access, 
          refresh: refresh || currentRefreshToken 
        });

        if (originalRequest.headers) {
          originalRequest.headers.Authorization = `Bearer ${access}`;
        }

        processQueue(null, access);
        originalRequest._retryCount += 1;
        return apiClient(originalRequest);
      } catch (refreshError) {
        processQueue(refreshError, null);
        useAuthStore.getState().clearAuth();
        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  }
);