"use client";

import * as React from "react";
import { useSearchParams, useRouter } from "next/navigation";
import Link from "next/link";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { resetPasswordSchema } from "@/features/auth/schemas/authSchemas";
import { useResetPassword } from "@/features/auth/hooks/useResetPassword";
import { cn } from "@/lib/utils";
import { Eye, EyeOff, Loader2, AlertTriangle, ShieldAlert, Sparkles, Check, X } from "lucide-react";

type ResetPasswordValues = z.infer<typeof resetPasswordSchema>;

export default function ResetPasswordPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const token = searchParams.get("token") || "";

  const { mutateAsync: executeReset, isPending, isSuccess } = useResetPassword();
  const [showPassword, setShowPassword] = React.useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = React.useState(false);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<ResetPasswordValues>({
    resolver: zodResolver(resetPasswordSchema),
    defaultValues: { token, password: "", confirm_password: "" },
  });

  const passwordValue = watch("password") || "";

  const checks = {
    length: passwordValue.length >= 8,
    hasUpper: /[A-Z]/.test(passwordValue),
    hasLower: /[a-z]/.test(passwordValue),
    hasNumber: /[0-9]/.test(passwordValue),
    hasSpecial: /[^A-Za-z0-9]/.test(passwordValue),
  };

  const strengthScore = Object.values(checks).filter(Boolean).length;

  const onSubmit = async (data: ResetPasswordValues) => {
    try {
      await executeReset({ token: data.token, password: data.password, confirm_password: data.confirm_password });
      setTimeout(() => {
        router.push("/login");
      }, 2000);
    } catch {
      // Handled globally via the useToast structure
    }
  };

  if (!token) {
    return (
      <main className="min-h-screen bg-background flex items-center justify-center p-6 bg-radial-gradient relative overflow-hidden">
        <div className="w-full max-w-md bg-card border border-border/60 rounded-3xl premium-shadow p-8 text-center backdrop-blur-sm relative z-10 space-y-5">
          <div className="h-12 w-12 rounded-2xl bg-destructive/10 text-destructive flex items-center justify-center mx-auto border border-destructive/20">
            <ShieldAlert className="h-5 w-5" />
          </div>
          <div className="space-y-1">
            <h2 className="text-lg font-black tracking-tight text-foreground">Missing Token Signature</h2>
            <p className="text-xs font-semibold text-muted-foreground max-w-xs mx-auto">
              This request wrapper is unauthenticated. Please follow the explicit link routed to your corporate mailbox account.
            </p>
          </div>
          <Link href="/login" className="block text-xs font-bold text-primary hover:underline pt-2">
            Return to Login Panel
          </Link>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-background flex items-center justify-center p-6 bg-radial-gradient relative overflow-hidden">
      <div className="w-full max-w-md bg-card border border-border/60 rounded-3xl premium-shadow p-6 sm:p-8 backdrop-blur-sm relative z-10">
        
        <div className="flex justify-center mb-6">
          <div className="flex items-center gap-2 font-bold text-foreground">
            <Sparkles className="h-4 w-4 text-primary fill-primary/10" />
            <span className="text-xs tracking-wider font-black uppercase">TalentAI Cryptographic Node</span>
          </div>
        </div>

        {!isSuccess ? (
          <div className="space-y-5 animate-in fade-in duration-200">
            <div className="space-y-1 text-center">
              <h2 className="text-xl font-black tracking-tight text-foreground sm:text-2xl">
                Establish New Password
              </h2>
              <p className="text-xs text-muted-foreground font-semibold">
                Update your security shield metrics to restore live dashboard execution contexts.
              </p>
            </div>

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              {/* Hidden configuration input block matching form values mapping definitions */}
              <input type="hidden" {...register("token")} value={token} />

              {/* Password field input row */}
              <div className="space-y-1.5">
                <label htmlFor="password" className="text-xs font-bold text-foreground/90 tracking-wide">
                  New Password
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
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground/80 hover:text-foreground cursor-pointer p-0.5"
                  >
                    {showPassword ? <EyeOff className="h-3.5 w-3.5" /> : <Eye className="h-3.5 w-3.5" />}
                  </button>
                </div>
                {errors.password && (
                  <p className="text-[11px] font-semibold text-destructive">{errors.password.message}</p>
                )}
              </div>

              {/* Confirm Password field row */}
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
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground/80 hover:text-foreground cursor-pointer p-0.5"
                  >
                    {showConfirmPassword ? <EyeOff className="h-3.5 w-3.5" /> : <Eye className="h-3.5 w-3.5" />}
                  </button>
                </div>
                {errors.confirm_password && (
                  <p className="text-[11px] font-semibold text-destructive">{errors.confirm_password.message}</p>
                )}
              </div>

              {/* Complexity checklist criteria matrix component view block */}
              <div className="p-3 bg-secondary/40 border border-border/60 rounded-xl space-y-1.5 text-[11px] font-semibold text-muted-foreground">
                <div className="grid grid-cols-2 gap-1.5">
                  <div className={cn("flex items-center gap-1.5", checks.length ? "text-feature-green" : "text-muted-foreground/70")}>
                    {checks.length ? <Check className="h-3.5 w-3.5" /> : <X className="h-3.5 w-3.5" />}
                    <span>Min 8 entries</span>
                  </div>
                  <div className={cn("flex items-center gap-1.5", checks.hasUpper ? "text-feature-green" : "text-muted-foreground/70")}>
                    {checks.hasUpper ? <Check className="h-3.5 w-3.5" /> : <X className="h-3.5 w-3.5" />}
                    <span>Uppercase code</span>
                  </div>
                  <div className={cn("flex items-center gap-1.5", checks.hasLower ? "text-feature-green" : "text-muted-foreground/70")}>
                    {checks.hasLower ? <Check className="h-3.5 w-3.5" /> : <X className="h-3.5 w-3.5" />}
                    <span>Lowercase code</span>
                  </div>
                  <div className={cn("flex items-center gap-1.5", checks.hasNumber ? "text-feature-green" : "text-muted-foreground/70")}>
                    {checks.hasNumber ? <Check className="h-3.5 w-3.5" /> : <X className="h-3.5 w-3.5" />}
                    <span>Numeric digits</span>
                  </div>
                </div>
              </div>

              <button
                type="submit"
                disabled={isPending || strengthScore < 4}
                className="w-full h-10 bg-zinc-900 dark:bg-zinc-100 text-zinc-50 dark:text-zinc-900 hover:bg-zinc-800 dark:hover:bg-zinc-200 disabled:opacity-50 text-xs font-bold rounded-xl shadow-sm transition-all cursor-pointer flex items-center justify-center gap-2 mt-2"
              >
                {isPending ? (
                  <>
                    <Loader2 className="h-3.5 w-3.5 animate-spin" />
                    <span>Synchronizing new parameters...</span>
                  </>
                ) : (
                  <span>Commit Password Matrix</span>
                )}
              </button>
            </form>
          </div>
        ) : (
          <div className="text-center space-y-4 animate-in zoom-in-95 duration-300">
            <div className="h-12 w-12 rounded-2xl bg-feature-green/10 text-feature-green flex items-center justify-center mx-auto border border-feature-green/20">
              <Check className="h-5 w-5 animate-pulse" />
            </div>
            <div className="space-y-1">
              <h2 className="text-lg font-black tracking-tight text-foreground">Shield Parameters Committed</h2>
              <p className="text-xs font-semibold text-muted-foreground">
                Routing back to the primary authentication page interface frame module.
              </p>
            </div>
          </div>
        )}
      </div>
    </main>
  );
}