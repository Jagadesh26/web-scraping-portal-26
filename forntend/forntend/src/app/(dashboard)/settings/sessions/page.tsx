import * as React from "react";
import { SessionsTable } from "@/features/auth/components/sessions-table";
import { ShieldCheck, Fingerprint, HelpCircle } from "lucide-react";

export default function ActiveSessionsSettingsPage() {
  return (
    <div className="space-y-6 max-w-5xl mx-auto animate-in fade-in duration-200">
      
      {/* Header Context Title Typography Matrix */}
      <div className="space-y-0.5">
        <h1 className="text-xl font-black tracking-tight text-foreground sm:text-2xl flex items-center gap-2.5">
          <Fingerprint className="h-5 w-5 text-primary flex-shrink-0" />
          <span>Active Token Sessions</span>
        </h1>
        <p className="text-xs font-semibold text-muted-foreground">
          Audit and manage hardware nodes currently authenticated to read your profile telemetry.
        </p>
      </div>

      <div className="grid gap-6">
        {/* Core Component Interaction Node */}
        <SessionsTable />

        {/* Informative Help Guideline Documentation Card Footer */}
        <div className="p-4 bg-accent/20 border border-border/40 rounded-2xl flex gap-3 text-[11px] font-semibold text-muted-foreground leading-relaxed backdrop-blur-sm">
          <HelpCircle className="h-4 w-4 text-primary flex-shrink-0 mt-0.5" />
          <div className="space-y-1">
            <span className="text-foreground/80 font-bold block uppercase tracking-wider text-[9px]">
              How Session Revocation Operates
            </span>
            <p>
              Hardware records are cataloged dynamically during initial handshake parsing. Device recognition labels are mapped from incoming HTTP user-agent variables. If you revoke a signature parameter, that device's active socket lifecycle is broken inside Django, rejecting any subsequent API traffic instantly.
            </p>
          </div>
        </div>
      </div>

    </div>
  );
}