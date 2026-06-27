"use client";

import * as React from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { changePasswordSchema } from "@/features/auth/schemas/authSchemas";
import { useChangePassword } from "../hooks/useChangePassword";
import { cn } from "@/lib/utils";
import { Eye, EyeOff, Loader2, Check, X, AlertCircle } from "lucide-react";

type ChangePasswordValues = z.infer<typeof changePasswordSchema>;

export function ChangePasswordForm() {
  const { mutateAsync: executePasswordRotation, isPending } = useChangePassword();

  const [showOldPassword, setShowOldPassword] = React.useState(false);
  const [showNewPassword, setShowNewPassword] = React.useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = React.useState(false);

  const {
    register,
    handleSubmit,
    watch,
    reset,
    formState: { errors },
  } = useForm<ChangePasswordValues>({
    resolver: zodResolver(changePasswordSchema),
    defaultValues: {
      old_password: "",
      new_password: "",
      confirm_password: "",
    },
  });

  const newPasswordValue = watch("new_password") || "";

  // Password Requirement Checks
  const checks = {
    length: newPasswordValue.length >= 8,
    hasUpper: /[A-Z]/.test(newPasswordValue),
    hasLower: /[a-z]/.test(newPasswordValue),
    hasNumber: /[0-9]/.test(newPasswordValue),
    hasSpecial: /[^A-Za-z0-9]/.test(newPasswordValue),
  };

  const strengthScore = Object.values(checks).filter(Boolean).length;

  const getStrengthLabel = () => {
    if (!newPasswordValue) return { label: "Not Entered", color: "bg-muted" };
    if (strengthScore <= 2) return { label: "Weak Profile", color: "bg-destructive" };
    if (strengthScore <= 4) return { label: "Medium Security", color: "bg-feature-amber" };
    return { label: "Strong Shield", color: "bg-feature-green" };
  };

  const strength = getStrengthLabel();

  const onSubmit = async (data: ChangePasswordValues) => {
    try {
      await executePasswordRotation({
        old_password: data.old_password,
        new_password: data.new_password,
      });
      reset(); // Clear input elements upon successful API processing
    } catch {
      // Caught and processed gracefully inside the custom mutation hook
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
      {/* Current Password Field */}
      <div className="space-y-1.5">
        <label htmlFor="old_password" className="text-xs font-bold text-foreground/90 tracking-wide">
          Current Password
        </label>
        <div className="relative">
          <input
            {...register("old_password")}
            id="old_password"
            type={showOldPassword ? "text" : "password"}
            disabled={isPending}
            placeholder="••••••••"
            className={cn(
              "w-full bg-accent/30 focus:bg-background border rounded-xl pl-3.5 pr-10 py-2 text-xs font-medium focus:outline-none focus:ring-2 transition-all text-foreground",
              errors.old_password ? "border-destructive focus:ring-destructive/20" : "border-border focus:border-primary focus:ring-primary/10"
            )}
          />
          <button
            type="button"
            tabIndex={-1}
            onClick={() => setShowOldPassword(!showOldPassword)}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground/80 hover:text-foreground cursor-pointer p-0.5 rounded"
          >
            {showOldPassword ? <EyeOff className="h-3.5 w-3.5" /> : <Eye className="h-3.5 w-3.5" />}
          </button>
        </div>
        {errors.old_password && (
          <p className="text-[11px] font-semibold text-destructive">{errors.old_password.message}</p>
        )}
      </div>

      <div className="h-px bg-border/40 my-2" />

      {/* New Password Field */}
      <div className="space-y-1.5">
        <label htmlFor="new_password" className="text-xs font-bold text-foreground/90 tracking-wide">
          New Password
        </label>
        <div className="relative">
          <input
            {...register("new_password")}
            id="new_password"
            type={showNewPassword ? "text" : "password"}
            disabled={isPending}
            placeholder="••••••••"
            className={cn(
              "w-full bg-accent/30 focus:bg-background border rounded-xl pl-3.5 pr-10 py-2 text-xs font-medium focus:outline-none focus:ring-2 transition-all text-foreground",
              errors.new_password ? "border-destructive focus:ring-destructive/20" : "border-border focus:border-primary focus:ring-primary/10"
            )}
          />
          <button
            type="button"
            tabIndex={-1}
            onClick={() => setShowNewPassword(!showNewPassword)}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground/80 hover:text-foreground cursor-pointer p-0.5 rounded"
          >
            {showNewPassword ? <EyeOff className="h-3.5 w-3.5" /> : <Eye className="h-3.5 w-3.5" />}
          </button>
        </div>

        {/* Password Strength Indicator */}
        {newPasswordValue && (
          <div className="space-y-1 pt-1 animate-in fade-in duration-200">
            <div className="flex items-center justify-between text-[10px] font-bold">
              <span className="text-muted-foreground uppercase">Strength Evaluation:</span>
              <span className={cn(
                strengthScore <= 2 && "text-destructive",
                strengthScore === 3 || strengthScore === 4 ? "text-feature-amber" : "",
                strengthScore === 5 && "text-feature-green"
              )}>{strength.label}</span>
            </div>
            <div className="h-1.5 w-full bg-secondary rounded-full overflow-hidden flex gap-0.5">
              {[...Array(5)].map((_, i) => (
                <div
                  key={i}
                  className={cn(
                    "h-full flex-1 transition-all duration-300",
                    i < strengthScore ? strength.color : "bg-muted"
                  )}
                />
              ))}
            </div>
          </div>
        )}
        {errors.new_password && (
          <p className="text-[11px] font-semibold text-destructive">{errors.new_password.message}</p>
        )}
      </div>

      {/* Confirm New Password Field */}
      <div className="space-y-1.5">
        <label htmlFor="confirm_password" className="text-xs font-bold text-foreground/90 tracking-wide">
          Confirm New Password
        </label>
        <div className="relative">
          <input
            {...register("confirm_password")}
            id="confirm_password"
            type={showConfirmPassword ? "text" : "password"}
            disabled={isPending}
            placeholder="••••••••"
            className={cn(
              "w-full bg-accent/30 focus:bg-background border rounded-xl pl-3.5 pr-10 py-2 text-xs font-medium focus:outline-none focus:ring-2 transition-all text-foreground",
              errors.confirm_password ? "border-destructive focus:ring-destructive/20" : "border-border focus:border-primary focus:ring-primary/10"
            )}
          />
          <button
            type="button"
            tabIndex={-1}
            onClick={() => setShowConfirmPassword(!showConfirmPassword)}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground/80 hover:text-foreground cursor-pointer p-0.5 rounded"
          >
            {showConfirmPassword ? <EyeOff className="h-3.5 w-3.5" /> : <Eye className="h-3.5 w-3.5" />}
          </button>
        </div>
        {errors.confirm_password && (
          <p className="text-[11px] font-semibold text-destructive">{errors.confirm_password.message}</p>
        )}
      </div>

      {/* Real-time Requirements Checklist */}
      <div className="p-3 bg-secondary/30 border border-border/50 rounded-xl space-y-1.5 text-[11px] font-semibold text-muted-foreground">
        <span className="text-[9px] uppercase font-bold text-foreground/60 tracking-wider block mb-0.5">Security Guidelines</span>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-1.5">
          <div className={cn("flex items-center gap-1.5 transition-colors", checks.length ? "text-feature-green" : "text-muted-foreground/60")}>
            {checks.length ? <Check className="h-3.5 w-3.5" /> : <X className="h-3.5 w-3.5" />}
            <span>At least 8 characters</span>
          </div>
          <div className={cn("flex items-center gap-1.5 transition-colors", checks.hasUpper ? "text-feature-green" : "text-muted-foreground/60")}>
            {checks.hasUpper ? <Check className="h-3.5 w-3.5" /> : <X className="h-3.5 w-3.5" />}
            <span>One uppercase letter</span>
          </div>
          <div className={cn("flex items-center gap-1.5 transition-colors", checks.hasLower ? "text-feature-green" : "text-muted-foreground/60")}>
            {checks.hasLower ? <Check className="h-3.5 w-3.5" /> : <X className="h-3.5 w-3.5" />}
            <span>One lowercase letter</span>
          </div>
          <div className={cn("flex items-center gap-1.5 transition-colors", checks.hasNumber ? "text-feature-green" : "text-muted-foreground/60")}>
            {checks.hasNumber ? <Check className="h-3.5 w-3.5" /> : <X className="h-3.5 w-3.5" />}
            <span>One numeric digit</span>
          </div>
          <div className={cn("flex items-center gap-1.5 transition-colors", checks.hasSpecial ? "text-feature-green" : "text-muted-foreground/60")}>
            {checks.hasSpecial ? <Check className="h-3.5 w-3.5" /> : <X className="h-3.5 w-3.5" />}
            <span>One special character</span>
          </div>
        </div>
      </div>

      {/* Submit Button */}
      <div className="flex justify-end pt-2">
        <button
          type="submit"
          disabled={isPending || strengthScore < 5}
          className="w-full sm:w-auto h-9 px-5 bg-zinc-900 dark:bg-zinc-100 text-zinc-50 dark:text-zinc-900 hover:bg-zinc-800 dark:hover:bg-zinc-200 disabled:opacity-40 text-xs font-bold rounded-xl shadow-sm transition-all cursor-pointer flex items-center justify-center gap-2 border border-transparent"
        >
          {isPending ? (
            <>
              <Loader2 className="h-3.5 w-3.5 animate-spin" />
              <span>Updating secure hashes...</span>
            </>
          ) : (
            <span>Update Password</span>
          )}
        </button>
      </div>
    </form>
  );
}