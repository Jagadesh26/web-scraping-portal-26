"use client";

import * as React from "react";
import { Loader2, AlertTriangle, X } from "lucide-react";

interface LogoutSessionDialogProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => Promise<void>;
  isPending: boolean;
  deviceName: string;
}

export function LogoutSessionDialog({
  isOpen,
  onClose,
  onConfirm,
  isPending,
  deviceName,
}: LogoutSessionDialogProps) {
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
        <div className="flex items-center justify-between px-5 py-4 border-b border-border/60 bg-accent/5">
          <div className="flex items-center gap-2 text-destructive font-bold text-sm">
            <AlertTriangle className="h-4 w-4" />
            <span>Revoke Remote Connection</span>
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
          <p className="text-xs font-semibold text-foreground/90 leading-relaxed">
            Are you sure you want to terminate the session authorization wrapper for{" "}
            <span className="text-primary font-black">“{deviceName || "Unknown Device"}”</span>?
          </p>
          <p className="text-[11px] font-medium text-muted-foreground leading-relaxed">
            This action instantly blacklists the specific refresh token signature inside the database cluster. The targeted device will be forced back to the account verification screen on its next network fetch cycle.
          </p>
        </div>

        <div className="flex items-center justify-end gap-2 px-5 py-3.5 bg-accent/10 border-t border-border/60">
          <button
            type="button"
            disabled={isPending}
            onClick={onClose}
            className="h-8 px-4 border border-border bg-popover hover:bg-accent text-xs font-bold rounded-xl transition-colors cursor-pointer disabled:opacity-50"
          >
            Cancel
          </button>
          <button
            type="button"
            disabled={isPending}
            onClick={onConfirm}
            className="h-8 px-4 bg-destructive text-destructive-foreground hover:bg-destructive/90 disabled:opacity-40 text-xs font-bold rounded-xl transition-colors cursor-pointer flex items-center gap-1.5"
          >
            {isPending ? (
              <>
                <Loader2 className="h-3.5 w-3.5 animate-spin" />
                <span>Revoking...</span>
              </>
            ) : (
              <span>Confirm Revocation</span>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}