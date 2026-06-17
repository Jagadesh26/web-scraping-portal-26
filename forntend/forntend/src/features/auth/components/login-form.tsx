"use client";

import * as React from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { loginSchema } from "@/features/auth/schemas/authSchemas";
import { useLogin } from "@/features/auth/hooks/userLogin";
import { parseApiError } from "@/core/api/apiErrorHandler";
import { Eye, EyeOff, Loader2, AlertCircle, CheckCircle2 } from "lucide-react";
import { cn } from "@/lib/utils";

type LoginFormValues = z.infer<typeof loginSchema>;

export function LoginForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const { mutateAsync: login, isPending } = useLogin();
  
  const [showPassword, setShowPassword] = React.useState(false);
  const [globalError, setGlobalError] = React.useState<string | null>(null);
  const [globalSuccess, setGlobalSuccess] = React.useState<string | null>(null);

  // Read callback URL parameter injected by edge middleware logic
  const callbackUrl = searchParams?.get("callbackUrl") || "/dashboard";

  const {
    register,
    handleSubmit,
    setError,
    formState: { errors },
  } = useForm<LoginFormValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const onSubmit = async (data: LoginFormValues) => {
    setGlobalError(null);
    setGlobalSuccess(null);
    
    try {
      await login(data);
      setGlobalSuccess("Authentication confirmed. Directing to workspace dashboard...");
      
      // Delay slightly to allow success animation state to propagate to UI
      setTimeout(() => {
        router.push(callbackUrl);
        router.refresh();
      }, 800);
    } catch (err) {
      const parsedError = parseApiError(err);
      
      if (parsedError.fieldErrors) {
        // Map DRF field validation keys cleanly onto local form handlers
        parsedError.fieldErrors.forEach((error) => {
          setError(error.field as keyof LoginFormValues, {
            type: "server",
            message: error.message,
          });
        });
      } else {
        setGlobalError(parsedError.message);
      }
    }
  };

  return (
    <div className="w-full max-w-sm space-y-6">
      <div className="space-y-2">
        <h2 className="text-xl font-bold tracking-tight text-foreground sm:text-2xl">
          Sign in to Platform
        </h2>
        <p className="text-xs text-muted-foreground font-medium">
          Enter corporate credentials to access your tracking pipeline.
        </p>
      </div>

      {/* Global Context Message Banners (Toasts/Alert Fallbacks) */}
      {globalError && (
        <div className="flex items-start gap-2.5 p-3.5 bg-destructive/10 border border-destructive/20 text-destructive rounded-xl text-xs font-semibold animate-in fade-in slide-in-from-top-1 duration-200">
          <AlertCircle className="h-4 w-4 flex-shrink-0 mt-0.5" />
          <span>{globalError}</span>
        </div>
      )}

      {globalSuccess && (
        <div className="flex items-start gap-2.5 p-3.5 bg-emerald-500/10 border border-emerald-500/20 text-emerald-600 dark:text-emerald-500 rounded-xl text-xs font-semibold animate-in fade-in slide-in-from-top-1 duration-200">
          <CheckCircle2 className="h-4 w-4 flex-shrink-0 mt-0.5" />
          <span>{globalSuccess}</span>
        </div>
      )}

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        {/* Email Address Input Block */}
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
              "w-full bg-accent/30 focus:bg-background border rounded-xl px-3.5 py-2 text-xs font-medium focus:outline-none focus:ring-2 transition-all text-foreground placeholder:text-muted-foreground/60",
              errors.email 
                ? "border-destructive focus:ring-destructive/20" 
                : "border-border/80 focus:border-primary focus:ring-primary/10"
            )}
          />
          {errors.email && (
            <p className="text-[11px] font-semibold text-destructive animate-in fade-in">
              {errors.email.message}
            </p>
          )}
        </div>

        {/* Password Input Block */}
        <div className="space-y-1.5">
          <div className="flex items-center justify-between">
            <label htmlFor="password" className="text-xs font-bold text-foreground/90 tracking-wide">
              Password
            </label>
            <a
              href="/forgot-password"
              className="text-[11px] font-bold text-primary hover:underline transition-all"
            >
              Forgot password?
            </a>
          </div>
          <div className="relative">
            <input
              {...register("password")}
              id="password"
              type={showPassword ? "text" : "password"}
              disabled={isPending}
              placeholder="••••••••"
              autoComplete="current-password"
              className={cn(
                "w-full bg-accent/30 focus:bg-background border rounded-xl pl-3.5 pr-10 py-2 text-xs font-medium focus:outline-none focus:ring-2 transition-all text-foreground placeholder:text-muted-foreground/60",
                errors.password 
                  ? "border-destructive focus:ring-destructive/20" 
                  : "border-border/80 focus:border-primary focus:ring-primary/10"
              )}
            />
            <button
              type="button"
              tabIndex={-1}
              disabled={isPending}
              onClick={() => setShowPassword(!showPassword)}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground/80 hover:text-foreground cursor-pointer transition-colors p-0.5 rounded"
            >
              {showPassword ? <EyeOff className="h-3.5 w-3.5" /> : <Eye className="h-3.5 w-3.5" />}
            </button>
          </div>
          {errors.password && (
            <p className="text-[11px] font-semibold text-destructive animate-in fade-in">
              {errors.password.message}
            </p>
          )}
        </div>

        {/* Utility Filters (Remember Me Option Link) */}
        <div className="flex items-center justify-between pt-1">
          <label className="flex items-center gap-2 text-xs font-medium text-muted-foreground select-none cursor-pointer">
            <input
              type="checkbox"
              disabled={isPending}
              className="h-3.5 w-3.5 rounded border-border/80 bg-accent/30 text-primary focus:ring-0 focus:ring-offset-0 transition-all accent-primary cursor-pointer"
            />
            <span>Remember device metrics</span>
          </label>
        </div>

        {/* Form Action Controls Matrix */}
        <div className="space-y-3 pt-2">
          <button
            type="submit"
            disabled={isPending}
            className="w-full h-10 bg-zinc-900 dark:bg-zinc-100 text-zinc-50 dark:text-zinc-900 hover:bg-zinc-800 dark:hover:bg-zinc-200 disabled:opacity-50 text-xs font-bold rounded-xl shadow-sm transition-all cursor-pointer flex items-center justify-center gap-2 border border-transparent"
          >
            {isPending ? (
              <>
                <Loader2 className="h-3.5 w-3.5 animate-spin" />
                <span>Validating profile data...</span>
              </>
            ) : (
              <span>Sign In</span>
            )}
          </button>

          {/* Social OAuth Presentation UI Section */}
          <div className="relative my-4 flex items-center justify-center">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-border/60" />
            </div>
            <span className="relative bg-card px-3 text-[10px] font-bold uppercase tracking-wider text-muted-foreground">
              Or continue with
            </span>
          </div>

          <button
            type="button"
            disabled={isPending}
            className="w-full h-9 bg-card hover:bg-accent/40 text-foreground border border-border/80 text-xs font-semibold rounded-xl shadow-sm transition-all cursor-pointer flex items-center justify-center gap-2"
          >
            <svg className="h-3.5 w-3.5 flex-shrink-0" viewBox="0 0 24 24">
              <path
                fill="currentColor"
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
              />
              <path
                fill="currentColor"
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
              />
              <path
                fill="currentColor"
                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"
              />
              <path
                fill="currentColor"
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
              />
            </svg>
            <span>Continue with Google</span>
          </button>
        </div>
      </form>

      {/* Footer System Paths */}
      <p className="text-center text-xs text-muted-foreground font-medium">
        Don&apos;t have an account?{" "}
        <a href="/register" className="text-primary font-bold hover:underline transition-all ml-0.5">
          Create Account
        </a>
      </p>
    </div>
  );
}