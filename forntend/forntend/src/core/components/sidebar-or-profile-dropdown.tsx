// Example: src/core/components/sidebar-or-profile-dropdown.tsx
"use client";

import * as React from "react";
import { useLogout } from "@/features/auth/hooks/userLogut";
import { LogOut, Loader2 } from "lucide-react";
import { useAuthStore } from "@/features/auth/store/authStore";

export function UserProfileDropdown() {
  const { mutate: logout, isPending } = useLogout();
  const refreshToken = useAuthStore((state) => state.refreshToken);

  const handleLogoutClick = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    
    // Trigger the mutation directly. Do NOT clear localStorage or state here!
    if (refreshToken) {
      logout(refreshToken);
    }
  };

  return (
    <button
      type="button"
      disabled={isPending}
      onClick={handleLogoutClick}
      className="flex w-full items-center gap-2 px-3 py-2 text-xs font-semibold text-destructive hover:bg-destructive/10 rounded-xl transition-all cursor-pointer disabled:opacity-50"
    >
      {isPending ? (
        <Loader2 className="h-3.5 w-3.5 animate-spin" />
      ) : (
        <LogOut className="h-3.5 w-3.5" />
      )}
      <span>{isPending ? "Signing out..." : "Log out session"}</span>
    </button>
  );
}