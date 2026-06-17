import { useMutation } from "@tanstack/react-query";
import { authService } from "../api/authService";
import { useToast } from "@/hooks/use-toast";

export function useVerifyEmail() {
  const { toast } = useToast();

  return useMutation({
    mutationFn: (token: string) => authService.verifyEmail(token),
    onSuccess: () => {
      toast({
        title: "Account Secured",
        description: "Your professional email context has been verified successfully.",
        variant: "default",
      });
    },
    onError: (error: any) => {
      const apiMessage = 
        error?.response?.data?.detail || 
        "The verification link is invalid or has expired.";
      
      toast({
        title: "Verification Failed",
        description: apiMessage,
        variant: "destructive",
      });
    },
  });
}