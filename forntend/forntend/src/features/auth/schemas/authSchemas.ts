import { z } from "zod";

// Shared reusable password validation regex segments
const passwordRules = z
  .string()
  .min(8, "Password must be at least 8 characters long")
  .regex(/[A-Z]/, "Password must contain at least one uppercase letter")
  .regex(/[a-z]/, "Password must contain at least one lowercase letter")
  .regex(/[0-9]/, "Password must contain at least one numeric digit")
  .regex(/[^A-Za-z0-9]/, "Password must contain at least one special character");

export const loginSchema = z.object({
  email: z
    .string()
    .min(1, "Corporate email is required")
    .email("Please enter a valid corporate email address"),
  password: z
    .string()
    .min(1, "Password is required"),
});

export const registerSchema = z
  .object({
    first_name: z
      .string()
      .min(1, "First name is required")
      .max(150, "First name must be under 150 characters"),
    last_name: z
      .string()
      .min(1, "Last name is required")
      .max(150, "Last name must be under 150 characters"),
    email: z
      .string()
      .min(1, "Corporate email is required")
      .email("Please enter a valid corporate email address"),
    phone_number: z
      .string()
      .optional(),
    password: passwordRules,
    confirm_password: z
      .string()
      .min(1, "Please confirm your password"),
    termsAccepted: z
      .boolean()
      .refine((val) => val === true, "You must accept the terms and conditions to proceed"),
  })
  .refine((data) => data.password === data.confirm_password, {
    message: "Passwords do not match",
    path: ["confirm_password"], // Targets the error directly to the confirm password field
  });

export const forgotPasswordSchema = z.object({
  email: z
    .string()
    .min(1, "Corporate email is required")
    .email("Please enter a valid corporate email address"),
});

export const resetPasswordSchema = z
  .object({
    token: z
      .string()
      .min(1, "Verification token signature is required"),
    password: passwordRules,
    confirm_password: z
      .string()
      .min(1, "Please confirm your new password"),
  })
  .refine((data) => data.password === data.confirm_password, {
    message: "Passwords do not match",
    path: ["confirm_password"],
  });

export const changePasswordSchema = z
  .object({
    old_password: z
      .string()
      .min(1, "Current password is required"),
    new_password: passwordRules,
    confirm_password: z
      .string()
      .min(1, "Please confirm your new password"),
  })
  .refine((data) => data.new_password === data.confirm_password, {
    message: "New passwords do not match",
    path: ["confirm_password"],
  });

// Type definitions for complete form type-safety across the app
export type LoginSchemaValues = z.infer<typeof loginSchema>;
export type RegisterSchemaValues = z.infer<typeof registerSchema>;
export type ForgotPasswordSchemaValues = z.infer<typeof forgotPasswordSchema>;
export type ResetPasswordSchemaValues = z.infer<typeof resetPasswordSchema>;
export type ChangePasswordSchemaValues = z.infer<typeof changePasswordSchema>;