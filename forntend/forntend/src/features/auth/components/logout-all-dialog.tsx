"use client";

import * as React from "react";
import { Loader2, ShieldAlert, X } from "lucide-react";

interface LogoutAllDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => Promise<void>;
  isPending: boolean;
}

export function LogoutAllDialog({ isOpen, onClose, onConfirm, isPending }: LogoutAllDialogProps) {
  React.useEffect(() => {
    if (!isOpen) return;
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === "Escape" && !isPending) onClose();
    };
    document.addEventListener("keydown", handleEscape);
    return () => document.removeEventListener("keydown", handleEscape);
  }, [isOpen, isPending, onClose]);

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-background/80 backdrop-blur-sm animate-in fade-in duration-200">
      <div 
        onClick={(e) => e.stopPropagation()} 
        className="w-full max-w-md bg-card border border-border/80 rounded-2xl shadow-xl overflow-hidden animate-in zoom-in-95 duration-200"
      >
        <div className="flex items-center justify-between px-5 py-4 border-b border-border/60 bg-destructive/5">
          <div className="flex items-center gap-2 text-destructive font-black text-sm tracking-tight">
            <ShieldAlert className="h-4 w-4" />
            <span>Emergency Session Lockout Trigger</span>
          </div>
          <button
            type="button"
            disabled={isPending}
            onClick={onClose}
            className="p-1 rounded-lg text-muted-foreground hover:text-foreground hover:bg-accent transition-colors cursor-pointer disabled:opacity-40"
          >
            <X className="h-4 w-4" />
          </button>
        </div>

        <div className="p-5 space-y-3">
          <p className="text-xs font-bold text-foreground/90 leading-relaxed">
            Are you sure you want to invalidate all concurrent hardware connections assigned to this profile context?
          </p>
          <p className="text-[11px] font-medium text-muted-foreground leading-relaxed">
            This will wipe out all active entries from the <code className="px-1 py-0.5 bg-muted rounded font-mono text-[10px] text-foreground">user_sessions</code> database index, logging out every browser, mobile instance, and remote location globally. Your current browser terminal session will remain active.
          </p>
        </div>

        <div className="flex items-center justify-end gap-2 px-5 py-3.5 bg-accent/10 border-t border-border/60">
          <button
            type="button"
            disabled={isPending}
            onClick={onClose}
            className="h-8 px-4 border border-border bg-popover hover:bg-accent text-xs font-bold rounded-xl transition-colors cursor-pointer disabled:opacity-50"
          >
            Abort Action
          </button>
          <button
            type="button"
            disabled={isPending}
            onClick={onConfirm}
            className="h-8 px-4 bg-destructive text-destructive-foreground hover:bg-destructive/90 disabled:opacity-40 text-xs font-bold rounded-xl transition-colors cursor-pointer flex items-center gap-1.5 shadow-sm shadow-destructive/10"
          >
            {isPending ? (
              <>
                <Loader2 className="h-3.5 w-3.5 animate-spin" />
                <span>Terminating Assets...</span>
              </>
            ) : (
              <span>Sign Out All Other Devices</span>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}