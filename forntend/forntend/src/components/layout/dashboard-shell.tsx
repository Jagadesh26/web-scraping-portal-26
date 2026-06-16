"use client";

import { useUiStore } from "@/core/store/uiStore";
import { cn } from "@/lib/utils";
import { ReactNode } from "react";

interface DashboardShellProps {
  children: ReactNode;
}

export function DashboardShell({ children }: DashboardShellProps) {
  const isSidebarCollapsed = useUiStore((state) => state.isSidebarCollapsed);

  return (
    <div className="min-h-screen bg-background">
      {/* Content wrapper taking into account desktop fixed sidebar dimension boundaries */}
      <div
        className={cn(
          "min-h-screen flex flex-col transition-all duration-300",
          isSidebarCollapsed ? "lg:pl-20" : "lg:pl-64"
        )}
      >
        {children}
      </div>
    </div>
  );
}