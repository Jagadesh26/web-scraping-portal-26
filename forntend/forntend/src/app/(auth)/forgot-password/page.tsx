"use client";

import * as React from "react";
import Link from "next/link";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { forgotPasswordSchema } from "@/features/auth/schemas/authSchemas";
import { useForgotPassword } from "@/features/auth/hooks/useForgotPassword";
import { cn } from "@/lib/utils";
import { Mail, Loader2, ArrowLeft, Sparkles, CheckCircle2 } from "lucide-react";

type ForgotPasswordValues = z.infer<typeof forgotPasswordSchema>;

export default function ForgotPasswordPage() {
  const { mutateAsync: sendRecoveryLink, isPending, isSuccess } = useForgotPassword();
  const [submittedEmail, setSubmittedEmail] = React.useState("");

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<ForgotPasswordValues>({
    resolver: zodResolver(forgotPasswordSchema),
    defaultValues: { email: "" },
  });

  const onSubmit = async (data: ForgotPasswordValues) => {
    try {
      setSubmittedEmail(data.email);
      await sendRecoveryLink(data.email);
    } catch {
      // Caught and handled by the global toast framework
    }
  };

  return (
    <main className="min-h-screen bg-background flex items-center justify-center p-6 bg-radial-gradient relative overflow-hidden">
      <div className="w-full max-w-md bg-card border border-border/60 rounded-3xl premium-shadow p-6 sm:p-8 backdrop-blur-sm relative z-10">
        
        {/* Identity Branding Header */}
        <div className="flex justify-center mb-6">
          <div className="flex items-center gap-2 font-bold text-foreground">
            <Sparkles className="h-4 w-4 text-primary fill-primary/10" />
            <span className="text-xs tracking-wider font-black uppercase">TalentAI Recovery Gateway</span>
          </div>
        </div>

        {!isSuccess ? (
          <div className="space-y-5 animate-in fade-in duration-200">
            <div className="space-y-1 text-center">
              <h2 className="text-xl font-black tracking-tight text-foreground sm:text-2xl">
                Reset Security Key
              </h2>
              <p className="text-xs text-muted-foreground font-semibold max-w-xs mx-auto">
                Provide your registered corporate email to generate an encrypted credential recovery token link.
              </p>
            </div>

            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
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
                  className={cn(
                    "w-full bg-accent/30 focus:bg-background border rounded-xl px-3.5 py-2 text-xs font-medium focus:outline-none focus:ring-2 transition-all text-foreground",
                    errors.email ? "border-destructive focus:ring-destructive/20" : "border-border focus:border-primary focus:ring-primary/10"
                  )}
                />
                {errors.email && (
                  <p className="text-[11px] font-semibold text-destructive">{errors.email.message}</p>
                )}
              </div>

              <button
                type="submit"
                disabled={isPending}
                className="w-full h-10 bg-zinc-900 dark:bg-zinc-100 text-zinc-50 dark:text-zinc-900 hover:bg-zinc-800 dark:hover:bg-zinc-200 disabled:opacity-50 text-xs font-bold rounded-xl shadow-sm transition-all cursor-pointer flex items-center justify-center gap-2 mt-2"
              >
                {isPending ? (
                  <>
                    <Loader2 className="h-3.5 w-3.5 animate-spin" />
                    <span>Routing recovery link...</span>
                  </>
                ) : (
                  <span>Send Recovery Instructions</span>
                )}
              </button>
            </form>
          </div>
        ) : (
          <div className="text-center space-y-5 animate-in zoom-in-95 duration-300">
            <div className="h-12 w-12 rounded-2xl bg-feature-green/10 text-feature-green flex items-center justify-center mx-auto border border-feature-green/20">
              <CheckCircle2 className="h-5 w-5" />
            </div>
            <div className="space-y-1">
              <h2 className="text-lg font-black tracking-tight text-foreground">Dispatched Successfully</h2>
              <p className="text-xs font-semibold text-muted-foreground max-w-xs mx-auto">
                An encrypted security link has been dispatched to <span className="text-foreground font-bold">{submittedEmail}</span> if it matches our identity logs.
              </p>
            </div>
          </div>
        )}

        <div className="mt-6 pt-4 border-t border-border/40">
          <Link
            href="/login"
            className="flex items-center justify-center gap-2 text-xs font-bold text-muted-foreground hover:text-foreground transition-colors group"
          >
            <ArrowLeft className="h-3.5 w-3.5 transition-transform group-hover:-translate-x-0.5" />
            <span>Return to Account Login</span>
          </Link>
        </div>

      </div>
    </main>
  );
}