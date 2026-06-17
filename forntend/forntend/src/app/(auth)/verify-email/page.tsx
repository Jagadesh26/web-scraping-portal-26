"use client";

import * as React from "react";
import { useSearchParams, useRouter } from "next/navigation";
import Link from "next/link";
import { useVerifyEmail } from "@/features/auth/hooks/useVerifyEmail";
import { useResendVerification } from "@/features/auth/hooks/useResendVerification";
import { Mail, ShieldCheck, AlertTriangle, Loader2, RefreshCw, ArrowRight, Sparkles } from "lucide-react";

export default function VerifyEmailPage() {
  const searchParams = useSearchParams();
  const router = useRouter();
  
  const token = searchParams.get("token");
  const email = searchParams.get("email") || "";

  const { mutateAsync: executeVerification, isPending: isVerifying, isSuccess: verified, isError: verificationFailed } = useVerifyEmail();
  const { mutateAsync: triggerResend, isPending: isResending } = useResendVerification();

  const [countdown, setCountdown] = React.useState(0);
  const verificationAttempted = React.useRef(false);

  // Auto-trigger verification if a token exists in the URL parameters
  React.useEffect(() => {
    if (token && !verificationAttempted.current) {
      verificationAttempted.current = true;
      executeVerification(token);
    }
  }, [token, executeVerification]);

  // Handle resend timeout intervals
  React.useEffect(() => {
    if (countdown > 0) {
      const timer = setTimeout(() => setCountdown(countdown - 1), 1000);
      return () => clearTimeout(timer);
    }
  }, [countdown]);

  const handleResendClick = async () => {
    if (!email || countdown > 0) return;
    try {
      await triggerResend(email);
      setCountdown(60); // Freeze the button with a 60-second cooldown
    } catch {
      // Handled cleanly by toast notifications
    }
  };

  return (
    <main className="min-h-screen bg-background flex items-center justify-center p-6 bg-radial-gradient relative overflow-hidden">
      <div className="w-full max-w-md bg-card border border-border/60 rounded-3xl premium-shadow p-8 text-center backdrop-blur-sm relative z-10">
        
        {/* Core Identity Branding Layout header */}
        <div className="flex justify-center mb-6">
          <div className="flex items-center gap-2 font-bold text-foreground">
            <Sparkles className="h-4 w-4 text-primary fill-primary/10" />
            <span className="text-xs tracking-wider font-black uppercase">TalentAI Engineering Core</span>
          </div>
        </div>

        {/* CASE 1: Active Inbound Verification Token Hook is processing data */}
        {token && (
          <div className="space-y-6">
            {isVerifying && (
              <div className="space-y-4 animate-in fade-in duration-300">
                <div className="h-12 w-12 rounded-2xl bg-primary/10 text-primary flex items-center justify-center mx-auto border border-primary/20">
                  <Loader2 className="h-5 w-5 animate-spin" />
                </div>
                <h2 className="text-lg font-black tracking-tight text-foreground">Validating Credentials</h2>
                <p className="text-xs font-semibold text-muted-foreground max-w-xs mx-auto">
                  Verifying cryptographic records with our secure Django identity cluster.
                </p>
              </div>
            )}

            {verified && (
              <div className="space-y-5 animate-in zoom-in-95 duration-300">
                <div className="h-12 w-12 rounded-2xl bg-feature-green/10 text-feature-green flex items-center justify-center mx-auto border border-feature-green/20">
                  <ShieldCheck className="h-5 w-5" />
                </div>
                <div className="space-y-1">
                  <h2 className="text-lg font-black tracking-tight text-foreground">Profile Authenticated</h2>
                  <p className="text-xs font-semibold text-muted-foreground max-w-xs mx-auto">
                    Your email address has been verified. Your profile is now active on our network architecture platform.
                  </p>
                </div>
                <button
                  type="button"
                  onClick={() => router.push("/login")}
                  className="w-full h-10 bg-zinc-900 dark:bg-zinc-100 text-zinc-50 dark:text-zinc-900 hover:bg-zinc-800 dark:hover:bg-zinc-200 text-xs font-bold rounded-xl shadow-sm transition-all cursor-pointer flex items-center justify-center gap-2 mt-2"
                >
                  <span>Proceed to Identity Portal</span>
                  <ArrowRight className="h-3.5 w-3.5" />
                </button>
              </div>
            )}

            {verificationFailed && (
              <div className="space-y-5 animate-in zoom-in-95 duration-300">
                <div className="h-12 w-12 rounded-2xl bg-destructive/10 text-destructive flex items-center justify-center mx-auto border border-destructive/20">
                  <AlertTriangle className="h-5 w-5" />
                </div>
                <div className="space-y-1">
                  <h2 className="text-lg font-black tracking-tight text-foreground">Link Verification Failed</h2>
                  <p className="text-xs font-semibold text-muted-foreground max-w-xs mx-auto">
                    This verification sequence signature key has expired, been modified, or already used.
                  </p>
                </div>
                <div className="grid grid-cols-2 gap-2 mt-2">
                  <Link
                    href="/login"
                    className="h-10 border border-border bg-popover text-foreground hover:bg-accent text-xs font-bold rounded-xl flex items-center justify-center transition-all"
                  >
                    Back to Login
                  </Link>
                  <Link
                    href="/register"
                    className="h-10 bg-zinc-900 dark:bg-zinc-100 text-zinc-50 dark:text-zinc-900 hover:bg-zinc-800 dark:hover:bg-zinc-200 text-xs font-bold rounded-xl flex items-center justify-center transition-all"
                  >
                    Re-register Profile
                  </Link>
                </div>
              </div>
            )}
          </div>
        )}

        {/* CASE 2: Outbound Waiting State (User just completed signup) */}
        {!token && (
          <div className="space-y-6 animate-in fade-in duration-300">
            <div className="h-12 w-12 rounded-2xl bg-primary/10 text-primary flex items-center justify-center mx-auto border border-primary/20">
              <Mail className="h-5 w-5" />
            </div>
            
            <div className="space-y-1">
              <h2 className="text-lg font-black tracking-tight text-foreground">Confirm Security Registry</h2>
              <p className="text-xs font-semibold text-muted-foreground max-w-xs mx-auto">
                We've sent a validation link to <span className="text-foreground font-bold">{email || "your provided address"}</span>.
              </p>
            </div>

            <div className="p-3.5 bg-secondary/40 border border-border/60 rounded-xl text-left text-[11px] font-semibold text-muted-foreground space-y-1">
              <span className="text-foreground/70 font-bold block uppercase tracking-wider text-[9px]">Developer Telemetry Note</span>
              <p>For sandbox local environments, if routing delay occurs, ensure the Django configuration console print logs hook is monitoring outbound messages.</p>
            </div>

            <div className="space-y-2 pt-2">
              <button
                type="button"
                disabled={isResending || countdown > 0 || !email}
                onClick={handleResendClick}
                className="w-full h-10 border border-border bg-popover text-foreground hover:bg-accent disabled:opacity-50 text-xs font-bold rounded-xl shadow-sm transition-all cursor-pointer flex items-center justify-center gap-2"
              >
                {isResending ? (
                  <Loader2 className="h-3.5 w-3.5 animate-spin" />
                ) : (
                  <RefreshCw className="h-3.5 w-3.5" />
                )}
                <span>
                  {countdown > 0 ? `Resend Available in (${countdown}s)` : "Resend Security Link"}
                </span>
              </button>
              
              <Link
                href="/login"
                className="block text-center text-xs font-bold text-primary hover:underline pt-2"
              >
                Return to Login Page
              </Link>
            </div>
          </div>
        )}

      </div>
    </main>
  );
}