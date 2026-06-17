import { useMutation } from "@tanstack/react-query";
import { authService } from "../api/authService";
import { useToast } from "@/hooks/use-toast";

export function useForgotPassword() {
  const { toast } = useToast();

  return useMutation({
    mutationFn: (email: string) => authService.forgotPassword(email),
    onSuccess: () => {
      toast({
        title: "Recovery Link Dispatched",
        description: "If the email is registered on our network, a reset link will arrive shortly.",
        variant: "default",
      });
    },
    onError: (error: any) => {
      const apiMessage = error?.response?.data?.detail || "Unable to process password recovery request.";
      toast({
        title: "Request Failed",
        description: apiMessage,
        variant: "destructive",
      });
    },
  });
}