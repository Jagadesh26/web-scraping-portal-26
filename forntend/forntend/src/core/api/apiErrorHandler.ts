import { AxiosError } from "axios";

export interface ApiFieldError {
  field: string;
  message: string;
}

export interface CentralizedApiError {
  status: number;
  message: string;
  fieldErrors: ApiFieldError[] | null;
  globalErrors: string[] | null;
  code?: string;
}

export const parseApiError = (error: unknown): CentralizedApiError => {
  if (error instanceof AxiosError && error.response) {
    const status = error.response.status;
    const data = error.response.data;

    const parsedError: CentralizedApiError = {
      status,
      message: data?.message || data?.detail || "A server validation or execution fault occurred.",
      fieldErrors: null,
      globalErrors: null,
      code: data?.code,
    };

    switch (status) {
      case 400:
        if (data && typeof data === "object" && !data.detail && !data.message) {
          const errors: ApiFieldError[] = [];
          const globals: string[] = [];
          
          Object.entries(data).forEach(([key, value]) => {
            const messages = Array.isArray(value) ? value : [String(value)];
            if (key === "non_field_errors" || key === "detail" || key === "global") {
              globals.push(...messages);
            } else {
              messages.forEach((msg) => errors.push({ field: key, message: msg }));
            }
          });
          
          parsedError.fieldErrors = errors.length > 0 ? errors : null;
          parsedError.globalErrors = globals.length > 0 ? globals : null;
          parsedError.message = parsedError.globalErrors?.[0] || "Validation checks failed.";
        }
        break;
      case 401:
        parsedError.message = data?.detail || "Authentication context missing or expired.";
        break;
      case 403:
        parsedError.message = data?.detail || "Access privileges insufficient for this operation.";
        break;
      case 404:
        parsedError.message = data?.detail || "Target resource could not be found on the server.";
        break;
      case 500:
        parsedError.message = "Internal gateway error. System engineering has been auto-notified.";
        break;
    }

    return parsedError;
  }

  if (error instanceof Error) {
    return { status: 0, message: error.message, fieldErrors: null, globalErrors: null };
  }

  return { status: 0, message: "A network connectivity or CORS failure occurred.", fieldErrors: null, globalErrors: null };
};