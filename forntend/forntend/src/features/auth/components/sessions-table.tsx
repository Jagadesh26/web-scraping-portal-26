"use client";

import * as React from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { authService } from "../api/authService";
import { LogoutSessionDialog } from "./logout-session-dialog";
import { LogoutAllDialog } from "./logout-all-dialog";
import { useToast } from "@/hooks/use-toast";
import { formatDistanceToNow } from "date-fns";
import { Monitor, Smartphone, ShieldCheck, LogOut, Radio, KeyRound, Globe } from "lucide-react";
import { cn } from "@/lib/utils";
import type { Session } from "../types";

export function SessionsTable() {
  const queryClient = useQueryClient();
  const { toast } = useToast();

  const [targetSession, setTargetSession] = React.useState<Session | null>(null);
  const [isSingleOpen, setIsSingleOpen] = React.useState(false);
  const [isMasterOpen, setIsMasterOpen] = React.useState(false);

  // 1. Fetch data arrays from backend cache pipelines
  const { data: rawSessions, isLoading, isError } = useQuery<Session[]>({
    queryKey: ["auth", "sessions"],
    queryFn: authService.getSessions,
  });

  // Ensure consistent current-session mapping fallback
  const sessions = React.useMemo(() => {
    if (!rawSessions) return [];
    // If backend doesn't flag current session explicitly, mark the first active entity as a fallback safety
    return rawSessions.map((session, index) => ({
      ...session,
      is_current: session.is_current ?? index === 0,
    }));
  }, [rawSessions]);

  // 2. Individual remote device logout mutation handler
  const { mutateAsync: revokeSession, isPending: isRevokingSingle } = useMutation({
    mutationFn: (id: string) => authService.logoutSession(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["auth", "sessions"] });
      toast({ title: "Connection Severed", description: "Remote session token entry has been deleted." });
      setIsSingleOpen(false);
    },
    onError: (err: any) => {
      const message = err?.response?.data?.detail || "Target session termination refused by database connection pool.";
      toast({ title: "Revocation Failed", description: message, variant: "destructive" });
    },
  });

  // 3. Global logout mutation killer switch configuration
  const { mutateAsync: revokeAllSessions, isPending: isRevokingMaster } = useMutation({
    mutationFn: authService.logoutAll,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["auth", "sessions"] });
      toast({ title: "Global Clean Sweep Complete", description: "All secondary validation threads have been deleted." });
      setIsMasterOpen(false);
    },
    onError: (err: any) => {
      const message = err?.response?.data?.detail || "Global connection clearing process failed.";
      toast({ title: "Action Terminated", description: message, variant: "destructive" });
    },
  });

  const handleOpenSingleModal = (session: Session) => {
    setTargetSession(session);
    setIsSingleOpen(true);
  };

  const getDeviceIcon = (name: string = "") => {
    const lower = name.toLowerCase();
    if (lower.includes("iphone") || lower.includes("android") || lower.includes("mobile")) {
      return <Smartphone className="h-4 w-4" />;
    }
    return <Monitor className="h-4 w-4" />;
  };

  const formatTimestamp = (isoString: string) => {
    try {
      return formatDistanceToNow(new Date(isoString), { addSuffix: true });
    } catch {
      return "Active Now";
    }
  };

  // SKELETON RENDER LAYER (Simulates premium content metrics placeholders)
  if (isLoading) {
    return (
      <div className="space-y-4 animate-pulse">
        <div className="h-12 bg-muted rounded-xl w-full" />
        <div className="h-28 bg-muted rounded-2xl w-full" />
        <div className="h-28 bg-muted rounded-2xl w-full" />
      </div>
    );
  }

  // INTERACTIVE ERROR FALLBACK VIEWPORT
  if (isError) {
    return (
      <div className="p-6 text-center border border-destructive/20 bg-destructive/5 rounded-2xl space-y-2">
        <Radio className="h-5 w-5 mx-auto text-destructive animate-pulse" />
        <h4 className="text-xs font-bold text-foreground">Telemetry Gathering Aborted</h4>
        <p className="text-[11px] text-muted-foreground">Unable to fetch hardware state variables from Django engine.</p>
      </div>
    );
  }

  // EMPTY WORKSPACE STATUS FALLBACK
  if (sessions.length === 0) {
    return (
      <div className="p-8 text-center border border-dashed border-border rounded-2xl text-muted-foreground text-xs font-semibold">
        No active profile telemetry vectors verified inside current session block registries.
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Danger Zone Trigger Banner Card */}
      <div className="p-5 border border-border/60 bg-card rounded-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-4 backdrop-blur-sm">
        <div className="space-y-0.5">
          <h3 className="text-xs font-bold text-foreground flex items-center gap-2">
            <Radio className="h-3.5 w-3.5 text-primary animate-pulse" />
            <span>Concurrent Connection Monitor</span>
          </h3>
          <p className="text-[11px] font-medium text-muted-foreground">
            Clear all other login parameters if you suspect unauthenticated profile access breaches.
          </p>
        </div>
        <button
          type="button"
          disabled={sessions.length <= 1}
          onClick={() => setIsMasterOpen(true)}
          className="h-8 px-4 bg-destructive/10 text-destructive border border-destructive/20 hover:bg-destructive hover:text-destructive-foreground disabled:opacity-40 text-xs font-bold rounded-xl transition-all cursor-pointer flex items-center justify-center gap-1.5 flex-shrink-0"
        >
          <LogOut className="h-3.5 w-3.5" />
          <span>Sign Out All Other Devices</span>
        </button>
      </div>

      {/* DESKTOP TABLE VIEW CONTAINER VIEWPORT */}
      <div className="hidden md:block bg-card border border-border/60 rounded-2xl overflow-hidden shadow-sm">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-accent/10 border-b border-border/60 text-[10px] font-bold uppercase tracking-wider text-muted-foreground/80">
              <th className="px-5 py-3">Hardware / Node</th>
              <th className="px-5 py-3">Browser Engine</th>
              <th className="px-5 py-3">Network IP Address</th>
              <th className="px-5 py-3">Telemetry Context</th>
              <th className="px-5 py-3 text-right">Action Gate</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border/40 text-xs font-semibold text-foreground/90">
            {sessions.map((session) => (
              <tr
                key={session.id}
                className={cn(
                  "transition-colors hover:bg-accent/5",
                  session.is_current && "bg-primary/[0.02]"
                )}
              >
                <td className="px-5 py-4 flex items-center gap-3">
                  <div className={cn(
                    "p-2 rounded-lg border flex-shrink-0",
                    session.is_current ? "bg-primary/10 text-primary border-primary/20" : "bg-secondary text-muted-foreground border-border/40"
                  )}>
                    {getDeviceIcon(session.device_name)}
                  </div>
                  <div className="min-w-0 flex flex-col">
                    <span className="font-bold truncate">{session.device_name || "Unknown Hardware"}</span>
                    {session.is_current && (
                      <span className="text-[9px] px-1.5 py-0.5 bg-primary/10 text-primary border border-primary/20 rounded font-black w-max mt-0.5 uppercase tracking-wide">
                        Current Session
                      </span>
                    )}
                  </div>
                </td>
                <td className="px-5 py-4 text-muted-foreground font-medium">{session.browser || "System Engine"}</td>
                <td className="px-5 py-4 font-mono text-[11px] text-foreground/80 flex items-center gap-1.5">
                  <Globe className="h-3.5 w-3.5 text-muted-foreground/60" />
                  <span>{session.ip_address || "0.0.0.0"}</span>
                </td>
                <td className="px-5 py-4 text-muted-foreground font-medium">
                  <span className="block text-foreground/80">Active: {formatTimestamp(session.last_activity)}</span>
                  <span className="text-[10px] opacity-70 block font-normal">Created: {new Date(session.created_at).toLocaleDateString()}</span>
                </td>
                <td className="px-5 py-4 text-right">
                  {session.is_current ? (
                    <div className="inline-flex items-center gap-1 text-feature-green bg-feature-green/10 px-2 py-1 rounded-xl border border-feature-green/20 text-[10px] font-black uppercase tracking-wider">
                      <ShieldCheck className="h-3 w-3" />
                      <span>Active Node</span>
                    </div>
                  ) : (
                    <button
                      type="button"
                      onClick={() => handleOpenSingleModal(session)}
                      className="p-1.5 rounded-lg text-muted-foreground hover:text-destructive hover:bg-destructive/10 transition-all cursor-pointer border border-transparent hover:border-destructive/10"
                      title="Terminate authentication pipeline"
                    >
                      <LogOut className="h-3.5 w-3.5" />
                    </button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* MOBILE SCALED CARDS VISUAL SYSTEM CONTAINER */}
      <div className="block md:hidden space-y-3">
            {sessions.map((session) => (
          <div
            key={session.id}
            className={cn(
              "p-4 bg-card border rounded-2xl space-y-3 shadow-sm relative overflow-hidden",
              session.is_current ? "border-primary/30 bg-primary/[0.01]" : "border-border/60"
            )}
          >
            <div className="flex items-start justify-between gap-2">
              <div className="flex items-center gap-3 min-w-0">
                <div className={cn(
                  "p-2 rounded-lg border flex-shrink-0",
                  session.is_current ? "bg-primary/10 text-primary border-primary/20" : "bg-secondary text-muted-foreground border-border/40"
                )}>
                  {getDeviceIcon(session.device_name)}
                </div>
                <div className="min-w-0">
                  <p className="font-bold text-xs text-foreground truncate">{session.device_name || "Unknown Hardware"}</p>
                  <p className="text-[11px] font-medium text-muted-foreground truncate">{session.browser || "System Client"}</p>
                </div>
              </div>
              
              {!session.is_current && (
                <button
                  type="button"
                  onClick={() => handleOpenSingleModal(session)}
                  className="p-2 bg-secondary text-muted-foreground hover:text-destructive hover:bg-destructive/10 border border-border/40 hover:border-transparent rounded-xl transition-all cursor-pointer flex-shrink-0"
                >
                  <LogOut className="h-3.5 w-3.5" />
                </button>
              )}
            </div>

            <div className="h-px bg-border/40" />

            <div className="grid grid-cols-2 gap-2 text-[11px] font-semibold text-muted-foreground">
              <div>
                <span className="block text-[9px] uppercase tracking-wider opacity-60">IP Identity</span>
                <span className="font-mono text-foreground/80 block mt-0.5">{session.ip_address || "0.0.0.0"}</span>
              </div>
              <div>
                <span className="block text-[9px] uppercase tracking-wider opacity-60">Last Signal Delta</span>
                <span className="text-foreground/80 block mt-0.5">{formatTimestamp(session.last_activity)}</span>
              </div>
            </div>

            {session.is_current && (
              <div className="w-full bg-primary/5 border border-primary/10 rounded-xl px-3 py-1.5 flex items-center justify-center gap-1.5 text-[10px] text-primary font-black uppercase tracking-wider">
                <ShieldCheck className="h-3.5 w-3.5" />
                <span>Primary Operations Node</span>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* MODAL MOUNT REGISTRY LINKS */}
      <LogoutSessionDialog
        isOpen={isSingleOpen}
        onClose={() => setIsSingleOpen(false)}
        onConfirm={() => revokeSession(targetSession?.id || "")}
        isPending={isRevokingSingle}
        deviceName={targetSession?.device_name || ""}
      />

      <LogoutAllDialog
        isOpen={isMasterOpen}
        onClose={() => setIsMasterOpen(false)}
        onConfirm={() => revokeAllSessions()}
        isPending={isRevokingMaster}
      />
    </div>
  );
}