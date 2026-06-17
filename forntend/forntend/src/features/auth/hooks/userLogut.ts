// src/features/auth/hooks/useLogout.ts
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { authService } from "../api/authService";
import { useAuthStore } from "../store/authStore";

export function useLogout() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const clearAuth = useAuthStore((state) => state.clearAuth);

  return useMutation({
    // Dynamic live lookups prevent reading stale render variables
    mutationFn: async () => {
      const liveRefreshToken = useAuthStore.getState().refreshToken;
      return authService.logout(liveRefreshToken || "");
    },
    
    // onSettled always runs, guarding against getting stuck if tokens expire
    onSettled: () => {
      // 1. Wipe out active TanStack Query cached memory layers completely
      queryClient.clear();

      // 2. Clear local storage records and drop edge middleware session cookies
      clearAuth();

      // 3. Navigate back to the login screen safely
      router.push("/login");
      router.refresh();
    },
  });
}