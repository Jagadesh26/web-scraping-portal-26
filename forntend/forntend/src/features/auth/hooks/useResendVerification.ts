import { useMutation } from "@tanstack/react-query";
import { authService } from "../api/authService";
import { useToast } from "@/hooks/use-toast";

export function useResendVerification() {
  const { toast } = useToast();

  return useMutation({
    mutationFn: (email: string) => authService.resendVerificationEmail(email),
    onSuccess: () => {
      toast({
        title: "Dispatched Successfully",
        description: "A fresh cryptographic link has been routed to your inbox.",
        variant: "default",
      });
    },
    onError: (error: any) => {
      const apiMessage = error?.response?.data?.detail || "Unable to complete mail routing request.";
      toast({
        title: "Delivery Failure",
        description: apiMessage,
        variant: "destructive",
      });
    },
  });
}