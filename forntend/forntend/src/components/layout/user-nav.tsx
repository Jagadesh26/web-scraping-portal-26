"use client";

import * as React from "react";
import { useAuthStore } from "@/core/store/authStore";
import { LogOut, User, Settings, CreditCard } from "lucide-react";

export function UserNav() {
  const { user, logout } = useAuthStore();
  const [isOpen, setIsOpen] = React.useState(false);
  const dropdownRef = React.useRef<HTMLDivElement>(null);

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

  const fallbackName = user?.fullName || "Candidate User";
  const fallbackEmail = user?.email || "candidate@platform.com";
  const initials = fallbackName.split(" ").map(n => n[0]).join("").toUpperCase().slice(0, 2);

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
            <p className="font-medium text-foreground truncate">{fallbackName}</p>
            <p className="text-xs text-muted-foreground truncate">{fallbackEmail}</p>
          </div>
          
          <button 
            onClick={() => setIsOpen(false)}
            className="flex w-full items-center px-3 py-2 text-sm rounded-lg text-foreground hover:bg-accent hover:text-accent-foreground transition-colors cursor-pointer"
          >
            <User className="mr-2 h-4 w-4 text-muted-foreground" />
            <span>Profile Settings</span>
          </button>
          
          <button 
            onClick={() => setIsOpen(false)}
            className="flex w-full items-center px-3 py-2 text-sm rounded-lg text-foreground hover:bg-accent hover:text-accent-foreground transition-colors cursor-pointer"
          >
            <CreditCard className="mr-2 h-4 w-4 text-muted-foreground" />
            <span>Billing & Plans</span>
          </button>

          <div className="h-px bg-border my-1" />
          
          <button
            onClick={() => {
              setIsOpen(false);
              logout();
            }}
            className="flex w-full items-center px-3 py-2 text-sm rounded-lg text-destructive hover:bg-destructive/10 transition-colors cursor-pointer"
          >
            <LogOut className="mr-2 h-4 w-4" />
            <span>Log out</span>
          </button>
        </div>
      )}
    </div>
  );
}