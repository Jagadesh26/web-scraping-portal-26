// src/features/auth/hooks/useRegister.ts
import { useMutation } from "@tanstack/react-query";
import { authService } from "../api/authService";
import { RegisterSchemaValues } from "../schemas/authSchemas";
// Swap the import line to target your local hook registry:
import { useToast } from "@/hooks/use-toast"; 

export function useRegister() {
  const { toast } = useToast(); // Initialize local state portal

  return useMutation({
    mutationFn: async (data: RegisterSchemaValues) => {
      const payload = {
        first_name: data.first_name,
        last_name: data.last_name,
        email: data.email,
        password: data.password,
        confirm_password: data.confirm_password,
        ...(data.phone_number ? { phone_number: data.phone_number } : {}),
      };
      return authService.register(payload);
    },
    onSuccess: () => {
      toast({
        title: "Profile initiated!",
        description: "Please check your inbox for verification instructions.",
        variant: "default", // Maps to your clean corporate style
      });
    },
    onError: (error: any) => {
      const apiMessage = 
        error?.response?.data?.email?.[0] || 
        error?.response?.data?.detail || 
        "Account creation process aborted.";
      
      toast({
        title: "Registration Failed",
        description: apiMessage,
        variant: "destructive",
      });
    },
  });
}