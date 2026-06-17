"use client";

import * as React from "react";
import Link from "next/link";
// FIX 1: Point to the unified feature store path where real session data resides
import { useAuthStore } from "@/features/auth/store/authStore";
// FIX 2: Import your verified, backend-connected custom logout hook
import { useLogout } from "@/features/auth/hooks/userLogut";
import { LogOut, User, CreditCard, Loader2 } from "lucide-react";

export function UserNav() {
  const { user } = useAuthStore();
  const [isOpen, setIsOpen] = React.useState(false);
  const dropdownRef = React.useRef<HTMLDivElement>(null);

  // Connect your refactored TanStack mutation hook cleanly
  const { mutate: handleLogout, isPending: isLoggingOut } = useLogout();

  // Close dropdown on click outside
  React.useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // FIX 3: Defensive computation mapping fields across both corporate identity models cleanly
  const fallbackName = 
    user?.first_name 
      ? `${user.first_name} ${user.last_name || ""}`.trim() 
      : (user as any)?.fullName || "Candidate User";
      
  const fallbackEmail = user?.email || "candidate@platform.com";
  const initials = fallbackName.split(" ").map((n: any[]) => n[0]).join("").toUpperCase().slice(0, 2);

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex h-9 w-9 items-center justify-center rounded-full bg-primary/10 text-sm font-semibold text-primary focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 border border-border transition-all cursor-pointer hover:bg-primary/15"
      >
        {initials}
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-56 origin-top-right rounded-xl border border-border bg-card p-1 shadow-md ring-1 ring-black/5 focus:outline-none z-50 transition-all animate-in fade-in slide-in-from-top-2 duration-150">
          <div className="px-3 py-2 text-sm border-b border-border/60 mb-1">
            <p className="font-bold text-foreground truncate">{fallbackName}</p>
            <p className="text-xs text-muted-foreground truncate">{fallbackEmail}</p>
          </div>
          
          <Link 
            href="/profile"
            onClick={() => setIsOpen(false)}
            className="flex w-full items-center px-3 py-2 text-xs font-semibold rounded-lg text-foreground hover:bg-accent hover:text-accent-foreground transition-colors cursor-pointer"
          >
            <User className="mr-2 h-4 w-4 text-muted-foreground" />
            <span>Profile Settings</span>
          </Link>
          
          <Link 
            href="/billing"
            onClick={() => setIsOpen(false)}
            className="flex w-full items-center px-3 py-2 text-xs font-semibold rounded-lg text-foreground hover:bg-accent hover:text-accent-foreground transition-colors cursor-pointer"
          >
            <CreditCard className="mr-2 h-4 w-4 text-muted-foreground" />
            <span>Billing & Plans</span>
          </Link>

          <div className="h-px bg-border my-1" />
          
          {/* FIX 4: ATTACH DISCRETE ISOLATION EVENT TRIGGERS TO SECURE THE ASYNC NET CONTRACT */}
          <button
            type="button"
            disabled={isLoggingOut}
            onClick={(e) => {
              e.preventDefault();
              e.stopPropagation();
              setIsOpen(false); // Snap the menu overlay closed immediately 
              handleLogout();   // Fire the async blacklisting transaction to Django
            }}
            className="flex w-full items-center px-3 py-2 text-xs font-bold rounded-lg text-destructive hover:bg-destructive/10 transition-colors cursor-pointer disabled:opacity-50"
          >
            {isLoggingOut ? (
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            ) : (
              <LogOut className="mr-2 h-4 w-4" />
            )}
            <span>{isLoggingOut ? "Signing out..." : "Log out"}</span>
          </button>
        </div>
      )}
    </div>
  );
}