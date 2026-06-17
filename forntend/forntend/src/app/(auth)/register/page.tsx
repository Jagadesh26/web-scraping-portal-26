import * as React from "react";
import { RegisterForm } from "@/features/auth/components/register-form";
import { Sparkles, CheckCircle2, ShieldCheck, Cpu, Zap } from "lucide-react";

export default function RegisterLayoutPage() {
  return (
    <main className="min-h-screen grid lg:grid-cols-12 bg-background relative overflow-hidden bg-radial-gradient">
      
      {/* LEFT SPLIT COLUMN: Corporate branding / Product Context (Visible exclusively on Widescreen viewports) */}
      <div className="hidden lg:flex lg:col-span-5 bg-card/40 border-r border-border/50 p-12 flex-col justify-between relative z-10">
        
        {/* Core Product Logo Header */}
        <div className="flex items-center gap-2.5 font-bold text-foreground">
          <div className="p-2 bg-primary/10 text-primary border border-primary/20 rounded-xl">
            <Sparkles className="h-5 w-5 fill-primary/10" />
          </div>
          <span className="text-base tracking-tight font-black">TalentAI Architecture</span>
        </div>

        {/* Product Pitch Marketing Section */}
        <div className="space-y-6 my-auto max-w-sm">
          <div className="space-y-3">
            <span className="px-3 py-1 bg-primary/5 text-primary border border-primary/10 text-[10px] font-bold uppercase tracking-wider rounded-lg inline-block">
              Enterprise Engine Live
            </span>
            <h1 className="text-3xl font-black tracking-tight text-foreground leading-tight">
              Build Your Career <br />With High-Fidelity AI.
            </h1>
            <p className="text-xs font-semibold text-muted-foreground leading-relaxed">
              Upload structural files, inspect automated gap vulnerabilities, discover targeted sector jobs, and optimize scores to beat automated trackers.
            </p>
          </div>

          {/* Core Feature Value Check List Mapping */}
          <div className="space-y-3 pt-2 text-xs font-semibold text-foreground/90">
            <div className="flex items-center gap-2.5">
              <ShieldCheck className="h-4 w-4 text-primary" />
              <span>Real-time vector metric parsing checkers</span>
            </div>
            <div className="flex items-center gap-2.5">
              <Cpu className="h-4 w-4 text-primary" />
              <span>Automated skills match gap identification</span>
            </div>
            <div className="flex items-center gap-2.5">
              <Zap className="h-4 w-4 text-primary" />
              <span>Thread-safe deployment activity tracking</span>
            </div>
          </div>
        </div>

        {/* Footer Identity Copyright Section */}
        <div className="text-[11px] font-medium text-muted-foreground/80">
          © 2026 TalentAI System Infrastructure Corp. All telemetry monitors active.
        </div>
      </div>

      {/* RIGHT SPLIT COLUMN: Centered Interaction Form Matrix Layer */}
      <div className="col-span-12 lg:col-span-7 flex items-center justify-center p-6 sm:p-12 relative z-10 overflow-y-auto">
        <div className="w-full max-w-md bg-card border border-border/60 rounded-3xl premium-shadow p-6 sm:p-8 backdrop-blur-sm">
          <RegisterForm />
        </div>
      </div>
      
    </main>
  );
}