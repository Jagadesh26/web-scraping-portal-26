import { AxiosError } from "axios";

export interface ApiBackendError {
  message: string;
  errors?: Record<string, string[]>;
  code?: string;
}

export const parseApiError = (error: unknown): ApiBackendError => {
  if (error instanceof AxiosError && error.response) {
    const data = error.response.data as any;
    return {
      message: data?.message || data?.detail || "An unexpected server error occurred.",
      errors: data?.errors || null,
      code: data?.code || null,
    };
  }
  
  if (error instanceof Error) {
    return { message: error.message };
  }
  
  return { message: "An unidentifiable error network failure has occurred." };
};