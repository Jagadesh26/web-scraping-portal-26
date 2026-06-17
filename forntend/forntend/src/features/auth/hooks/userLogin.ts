// src/features/auth/hooks/useLogin.ts
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { authService } from "../api/authService";
import { useAuthStore } from "../store/authStore";

export function useLogin() {
  const setTokens = useAuthStore((state) => state.setTokens);
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: authService.login,
    onSuccess: (response: any) => {
      // 1. Handle case where the raw Axios response wrapper is passed instead of response.data
      const data = response?.data ? response.data : response;
      
      // CRITICAL DEBUG LOG: Open your browser inspect console (F12) to see exactly what Django sent!
      console.log("DEBUG: Raw Django Login Payload received on frontend:", data);

      // 2. Check every possible naming convention for the Access Token
      const access = 
        data?.access || 
        data?.tokens?.access || 
        data?.accessToken || 
        data?.access_token;
      
      // 3. Check every possible naming convention for the Refresh Token
      const refresh = 
        data?.refresh || 
        data?.tokens?.refresh || 
        data?.refreshToken || 
        data?.refresh_token;

      // 4. Extract user properties dynamically
      const user = data?.user || data;

      if (access && refresh) {
        // Tokens successfully verified and extracted! Save them to Zustand
        setTokens({ access, refresh });
        
        if (user && (user.id || user.pk)) {
          queryClient.setQueryData(["auth", "current-user-context"], user);
        }
      } else {
        // If it still fails, log the exact culprit keys to the console
        console.error("Token extraction failed. Missing 'access' or 'refresh'. Received object keys:", Object.keys(data || {}));
        throw new Error("Invalid token payload structure returned from server.");
      }
    },
  });
}