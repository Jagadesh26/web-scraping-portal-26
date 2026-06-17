import { LoginForm } from "@/features/auth/components/login-form";
import { Sparkles, CheckCircle, BrainCircuit } from "lucide-react";

export const metadata = {
  title: "Secure Identity Portal | TalentAI Engine",
  description: "Access account tracking indices via enterprise JWT pipelines.",
};

export default function LoginPage() {
  return (
    <div className="min-h-screen grid lg:grid-cols-2 bg-background select-none">
      
      {/* BRAND PANEL - Exclusively rendered on Desktop Viewports */}
      <section className="hidden lg:flex flex-col justify-between p-12 bg-card relative overflow-hidden border-r border-border/60">
        {/* Subtle geometric structural pattern layer to match Linear style layouts */}
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_60%_50%_at_50%_-10%,var(--primary-foreground),transparent)] opacity-40 pointer-events-none" />
        <div className="absolute inset-0 bg-[linear-gradient(to_right,var(--border)_1px,transparent_1px),linear-gradient(to_bottom,var(--border)_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_40%,#000_70%,transparent_100%)] opacity-15 pointer-events-none" />

        {/* Header Content Top Branding */}
        <div className="flex items-center gap-2.5 relative z-10">
          <div className="h-8 w-8 rounded-xl bg-primary flex items-center justify-center shadow-md shadow-primary/20">
            <Sparkles className="h-4 w-4 text-primary-foreground fill-primary-foreground/10" />
          </div>
          <span className="text-sm font-black tracking-tight text-foreground">
            TalentAI Systems
          </span>
        </div>

        {/* Center Marketing Value Statements Proposition */}
        <div className="max-w-md space-y-6 my-auto relative z-10">
          <div className="inline-flex items-center gap-1.5 px-3 py-1 bg-primary/5 text-primary border border-primary/10 rounded-full text-[10px] font-black uppercase tracking-wider">
            <BrainCircuit className="h-3 w-3" />
            <span>AI Platform Engine Live</span>
          </div>
          
          <div className="space-y-3">
            <h1 className="text-3xl font-black tracking-tight text-foreground xl:text-4xl leading-tight">
              Find Jobs Faster.<br />Analyze Resumes Smarter.
            </h1>
            <p className="text-xs text-muted-foreground font-medium leading-relaxed max-w-sm">
              Discover verified market vectors, trace dynamic ATS alignment models, and access customized employment pipelines through a centralized hub.
            </p>
          </div>

          {/* Premium telemetry list array display */}
          <div className="space-y-2.5 pt-2">
            <div className="flex items-center gap-2.5 text-xs font-semibold text-foreground/90">
              <CheckCircle className="h-4 w-4 text-primary flex-shrink-0" />
              <span>Real-time vector alignment metrics checker</span>
            </div>
            <div className="flex items-center gap-2.5 text-xs font-semibold text-foreground/90">
              <CheckCircle className="h-4 w-4 text-primary flex-shrink-0" />
              <span>Thread-safe multi-session activity isolation</span>
            </div>
            <div className="flex items-center gap-2.5 text-xs font-semibold text-foreground/90">
              <CheckCircle className="h-4 w-4 text-primary flex-shrink-0" />
              <span>Automated skills match correction feedback</span>
            </div>
          </div>
        </div>

        {/* Corporate Legal Footer */}
        <div className="text-[11px] text-muted-foreground/60 font-medium relative z-10">
          &copy; 2026 TalentAI Architecture Corporation. All access logs monitored under security protocols.
        </div>
      </section>

      {/* CREDENTIALS FORM CARD PANEL - Adaptive Grid Layout */}
      <main className="flex flex-col items-center justify-center p-6 sm:p-10 lg:p-12 bg-background relative">
        {/* Mobile-only subtle header to preserve brand identification across small screens */}
        <div className="absolute top-6 left-6 flex items-center gap-2 lg:hidden">
          <Sparkles className="h-5 w-5 text-primary fill-primary/10" />
          <span className="text-xs font-black tracking-tight text-foreground">TalentAI</span>
        </div>

        <div className="w-full flex items-center justify-center animate-in fade-in slide-in-from-bottom-2 duration-300">
          <LoginForm />
        </div>
      </main>

    </div>
  );
}