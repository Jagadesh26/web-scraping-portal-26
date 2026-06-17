"use client";

import * as React from "react";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { registerSchema } from "@/features/auth/schemas/authSchemas";
import { useRegister } from "@/features/auth/hooks/useRegister"; // Reusing existing hook
import { parseApiError } from "@/core/api/apiErrorHandler";
import { cn } from "@/lib/utils";
import { Eye, EyeOff, Loader2, AlertCircle, CheckCircle2, Check, X, Link } from "lucide-react";

type RegisterFormValues = z.infer<typeof registerSchema>;

export function RegisterForm() {
  const router = useRouter();
  const { mutateAsync: registerUser, isPending } = useRegister();

  const [showPassword, setShowPassword] = React.useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = React.useState(false);
  const [globalError, setGlobalError] = React.useState<string | null>(null);

  const {
    register,
    handleSubmit,
    watch,
    setError,
    formState: { errors },
  } = useForm<RegisterFormValues>({
    resolver: zodResolver(registerSchema),
    defaultValues: {
      first_name: "",
      last_name: "",
      email: "",
      password: "",
      confirm_password: "",
      termsAccepted: false,
    },
  });

  const passwordValue = watch("password") || "";

  // Password Requirement Checklist Evaluation States
  const checks = {
    length: passwordValue.length >= 8,
    hasUpper: /[A-Z]/.test(passwordValue),
    hasLower: /[a-z]/.test(passwordValue),
    hasNumber: /[0-9]/.test(passwordValue),
    hasSpecial: /[^A-Za-z0-9]/.test(passwordValue),
  };

  // Dynamic Score Calculation for the UI Strength Indicator Bar
  const strengthScore = Object.values(checks).filter(Boolean).length;
  
  const getStrengthLabel = () => {
    if (!passwordValue) return { label: "Not Entered", color: "bg-muted" };
    if (strengthScore <= 2) return { label: "Weak Profile", color: "bg-destructive" };
    if (strengthScore <= 4) return { label: "Medium Security", color: "bg-feature-amber" };
    return { label: "Strong Shield", color: "bg-feature-green" };
  };

  const strength = getStrengthLabel();

  const onSubmit = async (data: RegisterFormValues) => {
    setGlobalError(null);
    try {
      await registerUser(data);
      
      // OPTION A: Reroute to verification wait state matching the User.is_verified architecture
      router.push(`/verify-email?email=${encodeURIComponent(data.email)}`);
      router.refresh();
    } catch (err: any) {
      const parsedError = parseApiError(err);
      
      if (parsedError.fieldErrors) {
        parsedError.fieldErrors.forEach((error) => {
          setError(error.field as keyof RegisterFormValues, {
            type: "server",
            message: error.message,
          });
        });
      } else {
        setGlobalError(parsedError.message || "An unexpected error occurred during profile registration.");
      }
    }
  };

  return (
    <div className="w-full max-w-md mx-auto space-y-6">
      <div className="space-y-1">
        <h2 className="text-xl font-black tracking-tight text-foreground sm:text-2xl">
          Create Corporate Account
        </h2>
        <p className="text-xs text-muted-foreground font-semibold">
          Gain access to dynamic resume metrics and automated pipeline matching models.
        </p>
      </div>

      {globalError && (
        <div className="flex items-start gap-2.5 p-3.5 bg-destructive/10 border border-destructive/20 text-destructive rounded-xl text-xs font-semibold animate-in fade-in slide-in-from-top-1">
          <AlertCircle className="h-4 w-4 flex-shrink-0 mt-0.5" />
          <span>{globalError}</span>
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        {/* Row block split for Name Inputs */}
        <div className="grid grid-cols-2 gap-3">
          <div className="space-y-1.5">
            <label htmlFor="first_name" className="text-xs font-bold text-foreground/90 tracking-wide">
              First Name
            </label>
            <input
              {...register("first_name")}
              id="first_name"
              type="text"
              disabled={isPending}
              placeholder="Karthick"
              className={cn(
                "w-full bg-accent/30 focus:bg-background border rounded-xl px-3.5 py-2 text-xs font-medium focus:outline-none focus:ring-2 transition-all text-foreground",
                errors.first_name ? "border-destructive focus:ring-destructive/20" : "border-border focus:border-primary focus:ring-primary/10"
              )}
            />
            {errors.first_name && (
              <p className="text-[11px] font-semibold text-destructive">{errors.first_name.message}</p>
            )}
          </div>

          <div className="space-y-1.5">
            <label htmlFor="last_name" className="text-xs font-bold text-foreground/90 tracking-wide">
              Last Name
            </label>
            <input
              {...register("last_name")}
              id="last_name"
              type="text"
              disabled={isPending}
              placeholder="S"
              className={cn(
                "w-full bg-accent/30 focus:bg-background border rounded-xl px-3.5 py-2 text-xs font-medium focus:outline-none focus:ring-2 transition-all text-foreground",
                errors.last_name ? "border-destructive focus:ring-destructive/20" : "border-border focus:border-primary focus:ring-primary/10"
              )}
            />
            {errors.last_name && (
              <p className="text-[11px] font-semibold text-destructive">{errors.last_name.message}</p>
            )}
          </div>
        </div>

        {/* Corporate Email input field */}
        <div className="space-y-1.5">
          <label htmlFor="email" className="text-xs font-bold text-foreground/90 tracking-wide">
            Corporate Email
          </label>
          <input
            {...register("email")}
            id="email"
            type="email"
            disabled={isPending}
            placeholder="name@company.com"
            autoComplete="email"
            className={cn(
              "w-full bg-accent/30 focus:bg-background border rounded-xl px-3.5 py-2 text-xs font-medium focus:outline-none focus:ring-2 transition-all text-foreground",
              errors.email ? "border-destructive focus:ring-destructive/20" : "border-border focus:border-primary focus:ring-primary/10"
            )}
          />
          {errors.email && (
            <p className="text-[11px] font-semibold text-destructive">{errors.email.message}</p>
          )}
        </div>

        {/* Password input block */}
        <div className="space-y-1.5">
          <label htmlFor="password" className="text-xs font-bold text-foreground/90 tracking-wide">
            Password
          </label>
          <div className="relative">
            <input
              {...register("password")}
              id="password"
              type={showPassword ? "text" : "password"}
              disabled={isPending}
              placeholder="••••••••"
              className={cn(
                "w-full bg-accent/30 focus:bg-background border rounded-xl pl-3.5 pr-10 py-2 text-xs font-medium focus:outline-none focus:ring-2 transition-all text-foreground",
                errors.password ? "border-destructive focus:ring-destructive/20" : "border-border focus:border-primary focus:ring-primary/10"
              )}
            />
            <button
              type="button"
              tabIndex={-1}
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground/80 hover:text-foreground cursor-pointer p-0.5 rounded"
            >
              {showPassword ? <EyeOff className="h-3.5 w-3.5" /> : <Eye className="h-3.5 w-3.5" />}
            </button>
          </div>

          {/* Dynamic Strength Indicator Metric Bar */}
          {passwordValue && (
            <div className="space-y-1 pt-1 animate-in fade-in duration-200">
              <div className="flex items-center justify-between text-[10px] font-bold">
                <span className="text-muted-foreground uppercase">Password Strength:</span>
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

          {errors.password && (
            <p className="text-[11px] font-semibold text-destructive">{errors.password.message}</p>
          )}
        </div>

        {/* Confirm Password input block */}
        <div className="space-y-1.5">
          <label htmlFor="confirm_password" className="text-xs font-bold text-foreground/90 tracking-wide">
            Confirm Password
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

        {/* Real-Time Criteria Checklist Interface Block */}
        <div className="p-3 bg-secondary/40 border border-border/60 rounded-xl space-y-1.5 text-[11px] font-semibold text-muted-foreground">
          <p className="text-[10px] uppercase font-bold text-foreground/70 tracking-wider mb-1">Security Blueprint Requirements</p>
          <div className="grid grid-cols-2 gap-1.5">
            <div className={cn("flex items-center gap-1.5 transition-colors", checks.length ? "text-feature-green" : "text-muted-foreground/70")}>
              {checks.length ? <Check className="h-3.5 w-3.5 flex-shrink-0" /> : <X className="h-3.5 w-3.5 flex-shrink-0" />}
              <span>At least 8 characters</span>
            </div>
            <div className={cn("flex items-center gap-1.5 transition-colors", checks.hasUpper ? "text-feature-green" : "text-muted-foreground/70")}>
              {checks.hasUpper ? <Check className="h-3.5 w-3.5 flex-shrink-0" /> : <X className="h-3.5 w-3.5 flex-shrink-0" />}
              <span>One uppercase character</span>
            </div>
            <div className={cn("flex items-center gap-1.5 transition-colors", checks.hasLower ? "text-feature-green" : "text-muted-foreground/70")}>
              {checks.hasLower ? <Check className="h-3.5 w-3.5 flex-shrink-0" /> : <X className="h-3.5 w-3.5 flex-shrink-0" />}
              <span>One lowercase character</span>
            </div>
            <div className={cn("flex items-center gap-1.5 transition-colors", checks.hasNumber ? "text-feature-green" : "text-muted-foreground/70")}>
              {checks.hasNumber ? <Check className="h-3.5 w-3.5 flex-shrink-0" /> : <X className="h-3.5 w-3.5 flex-shrink-0" />}
              <span>One numeric digit</span>
            </div>
            <div className={cn("flex items-center gap-1.5 transition-colors", checks.hasSpecial ? "text-feature-green" : "text-muted-foreground/70")}>
              {checks.hasSpecial ? <Check className="h-3.5 w-3.5 flex-shrink-0" /> : <X className="h-3.5 w-3.5 flex-shrink-0" />}
              <span>One special icon matrix</span>
            </div>
          </div>
        </div>

        {/* Terms & Conditions Checkbox */}
        <div className="space-y-1.5 pt-1">
          <label className="flex items-start gap-2.5 text-xs font-medium text-muted-foreground select-none cursor-pointer">
            <input
              {...register("termsAccepted")}
              type="checkbox"
              disabled={isPending}
              className="mt-0.5 h-4 w-4 rounded border-border bg-accent/30 text-primary focus:ring-0 focus:ring-offset-0 transition-all accent-primary cursor-pointer"
            />
            <span className="leading-tight font-semibold">
              I certify that I accept the platform's standard{" "}
              <a href="/terms" className="text-primary hover:underline">Terms of Service</a> and{" "}
              <a href="/privacy" className="text-primary hover:underline">Privacy Architecture Policy</a>.
            </span>
          </label>
          {errors.termsAccepted && (
            <p className="text-[11px] font-semibold text-destructive">{errors.termsAccepted.message}</p>
          )}
        </div>

        {/* Action Registration Form Submit controls */}
        <button
          type="submit"
          disabled={isPending}
          className="w-full h-10 bg-zinc-900 dark:bg-zinc-100 text-zinc-50 dark:text-zinc-900 hover:bg-zinc-800 dark:hover:bg-zinc-200 disabled:opacity-50 text-xs font-bold rounded-xl shadow-sm transition-all cursor-pointer flex items-center justify-center gap-2 border border-transparent mt-2"
        >
          {isPending ? (
            <>
              <Loader2 className="h-3.5 w-3.5 animate-spin" />
              <span>Provisioning secure profile...</span>
            </>
          ) : (
            <span>Create Account</span>
          )}
        </button>
      </form>

      <p className="text-center text-xs text-muted-foreground font-semibold">
        Already have an account?{" "}
        <Link href="/login" className="text-primary font-bold hover:underline ml-0.5">
          Sign In
        </Link>
      </p>
    </div>
  );
}