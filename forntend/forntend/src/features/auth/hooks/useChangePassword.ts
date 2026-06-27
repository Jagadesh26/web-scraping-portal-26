import { useMutation } from "@tanstack/react-query";
import { authService } from "../api/authService";
import { useAuthStore } from "../store/authStore";
import { useToast } from "@/hooks/use-toast";
import { useRouter } from "next/navigation";

export function useChangePassword() {
  const { toast } = useToast();
  const router = useRouter();
  const clearAuth = useAuthStore((state) => state.clearAuth);

  return useMutation({
    mutationFn: async (payload: { old_password: string; new_password: string }) => {
      return authService.changePassword(payload);
    },
    onSuccess: (response: any) => {
      // Check if your Django configuration automatically invalidates active tokens on change
      const sessionRevoked = response?.data?.revoked || response?.logged_out || false;

      if (sessionRevoked) {
        toast({
          title: "Password Updated Successfully",
          description: "Your security credentials have changed. Please log back in to re-authenticate.",
          variant: "default",
        });
        
        // Wipe local storage, flush token state memory, and kick to login screen
        clearAuth();
        router.push("/login");
        router.refresh();
      } else {
        toast({
          title: "Security Shield Rotated",
          description: "Your account password has been updated successfully.",
          variant: "default",
        });
      }
    },
    onError: (error: any) => {
      const apiMessage = 
        error?.response?.data?.old_password?.[0] || 
        error?.response?.data?.detail || 
        "Failed to change password. Please verify your current credentials.";

      toast({
        title: "Credential Update Refused",
        description: apiMessage,
        variant: "destructive",
      });
    },
  });
}