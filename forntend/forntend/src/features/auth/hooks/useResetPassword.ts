import { useMutation } from "@tanstack/react-query";
import { authService } from "../api/authService";
import { useToast } from "@/hooks/use-toast";

export function useResetPassword() {
  const { toast } = useToast();

  return useMutation({
    mutationFn: (payload: any) => authService.resetPassword(payload),
    onSuccess: () => {
      toast({
        title: "Security Shield Updated",
        description: "Your password has been reset successfully. You can now log in with your new credentials.",
        variant: "default",
      });
    },
    onError: (error: any) => {
      const apiMessage = error?.response?.data?.detail || "Password synchronization failed. Link may be expired.";
      toast({
        title: "Reset Failed",
        description: apiMessage,
        variant: "destructive",
      });
    },
  });
}