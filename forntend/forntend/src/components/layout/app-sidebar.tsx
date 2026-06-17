"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useUiStore } from "@/core/store/uiStore";
// FIX 1: Point to the correct unified feature store path where real tokens live
import { useAuthStore } from "@/features/auth/store/authStore";
import { useLogout } from "@/features/auth/hooks/userLogut";
import { dashboardNavigationStructure } from "@/core/config/navigation";
import { cn } from "@/lib/utils";
import * as React from "react";
import { ChevronLeft, ChevronRight, ChevronDown, Sparkles, LogOut, Loader2 } from "lucide-react";

export function AppSidebar() {
  const pathname = usePathname();
  const user = useAuthStore((state) => state.user);
  const { isSidebarCollapsed, toggleSidebar } = useUiStore();
  
  // Connect your refactored mutation hook cleanly
  const { mutate: handleLogout, isPending: isLoggingOut } = useLogout();
  
  const [openGroups, setOpenGroups] = React.useState<Record<string, boolean>>({
    Resume: true,
    "Jobs Module": true,
    "ATS Engine": true,
  });

  const toggleGroup = (title: string) => {
    setOpenGroups((prev) => ({ ...prev, [title]: !prev[title] }));
  };

  // Maps backend user records (first_name/last_name) or custom fullName values defensively
  const fallbackName = 
    user?.first_name 
      ? `${user.first_name} ${user.last_name || ""}`.trim() 
      : (user as any)?.fullName || "Candidate User";

  const userInitials = fallbackName
  ? fallbackName
      .split(" ")
      .map((n: string[]) => n[0].match(/[a-zA-Z]/) ? n[0].toUpperCase() : "")
      .join("")
      .slice(0, 2)
  : "";

  return (
    <aside
      className={cn(
        "hidden lg:flex flex-col fixed inset-y-0 left-0 bg-card border-r border-border h-full transition-all duration-300 z-20",
        isSidebarCollapsed ? "w-20" : "w-64"
      )}
    >
      {/* Platform Branding Header */}
      <div className="h-16 flex items-center justify-between px-4 border-b border-border/60">
        <Link href="/dashboard" className="flex items-center gap-2.5 font-bold text-foreground overflow-hidden whitespace-nowrap">
          <Sparkles className="h-5 w-5 text-primary fill-primary/10 flex-shrink-0" />
          {!isSidebarCollapsed && (
            <span className="text-base tracking-tight font-extrabold animate-in fade-in duration-200">
              TalentAI Portal
            </span>
          )}
        </Link>
        <button
          onClick={toggleSidebar}
          className="rounded-lg p-1 border border-border bg-popover text-muted-foreground hover:text-foreground hover:bg-accent shadow-sm cursor-pointer"
        >
          {isSidebarCollapsed ? <ChevronRight className="h-4 w-4" /> : <ChevronLeft className="h-4 w-4" />}
        </button>
      </div>

      {/* Expandable Navigation Tree */}
      <nav className="flex-1 px-3 py-4 space-y-1.5 overflow-y-auto style-scrollbar">
        {dashboardNavigationStructure.map((group) => {
          const Icon = group.icon;
          const hasSubItems = !!group.items;
          const isGroupOpen = openGroups[group.title];

          const isDirectActive = group.href ? pathname === group.href : false;
          const isSubActive = group.items?.some(sub => pathname === sub.href) || false;

          if (!hasSubItems && group.href) {
            return (
              <Link
                key={group.title}
                href={group.href}
                className={cn(
                  "flex items-center gap-3 px-3 py-2 text-xs font-semibold rounded-xl transition-all group relative",
                  isDirectActive
                    ? "bg-primary text-primary-foreground shadow-sm shadow-primary/20"
                    : "text-muted-foreground hover:bg-accent hover:text-foreground"
                )}
              >
                <Icon className="h-4 w-4 flex-shrink-0" />
                {!isSidebarCollapsed && <span className="truncate">{group.title}</span>}
              </Link>
            );
          }

          return (
            <div key={group.title} className="space-y-1">
              <button
                onClick={() => !isSidebarCollapsed && toggleGroup(group.title)}
                className={cn(
                  "w-full flex items-center justify-between px-3 py-2 text-xs font-semibold rounded-xl transition-all text-muted-foreground group cursor-pointer",
                  !isSidebarCollapsed && "hover:bg-accent hover:text-foreground",
                  isSubActive && "text-foreground font-bold"
                )}
              >
                <div className="flex items-center gap-3 truncate">
                  <Icon className={cn("h-4 w-4 flex-shrink-0", isSubActive && "text-primary")} />
                  {!isSidebarCollapsed && <span className="truncate">{group.title}</span>}
                </div>
                {!isSidebarCollapsed && (
                  <ChevronDown className={cn("h-3.5 w-3.5 transition-transform duration-200", isGroupOpen && "rotate-180")} />
                )}
              </button>

              {/* Render Submenu items */}
              {!isSidebarCollapsed && isGroupOpen && group.items && (
                <div className="pl-7 space-y-1 border-l border-border/80 ml-5 mt-0.5 animate-in fade-in duration-200">
                  {group.items.map((sub) => {
                    const isCurrentRoute = pathname === sub.href;
                    return (
                      <Link
                        key={sub.href}
                        href={sub.href}
                        className={cn(
                          "block px-3 py-1.5 text-[11px] font-medium rounded-lg transition-colors truncate",
                          isCurrentRoute
                            ? "text-primary font-bold bg-primary/5"
                            : "text-muted-foreground hover:text-foreground hover:bg-accent/5"
                        )}
                      >
                        {sub.title}
                      </Link>
                    );
                  })}
                </div>
              )}
            </div>
          );
        })}
      </nav>

      {/* Footprint Profiler Component */}
      <div className="p-4 border-t border-border/60 flex items-center justify-between gap-2 overflow-hidden bg-background/20">
        <div className="flex items-center gap-3 min-w-0">
          <div className="h-8 w-8 flex-shrink-0 rounded-lg bg-primary/10 text-primary flex items-center justify-center font-bold text-xs border border-primary/20">
            {userInitials}
          </div>
          {!isSidebarCollapsed && (
            <div className="flex flex-col min-w-0 animate-in fade-in duration-200">
              <span className="text-xs font-bold text-foreground truncate">{fallbackName}</span>
              <span className="text-[10px] text-muted-foreground truncate uppercase tracking-wider font-semibold">Premium Tier</span>
            </div>
          )}
        </div>

        {/* FIX 2: INJECT THE PHYSICALLY MISSING LOGOUT INTERACTION BUTTON */}
        {!isSidebarCollapsed && (
          <button
            type="button"
            disabled={isLoggingOut}
            onClick={(e) => {
              e.preventDefault();
              e.stopPropagation();
              handleLogout();
            }}
            className="p-2 rounded-xl text-muted-foreground hover:text-destructive hover:bg-destructive/10 transition-all cursor-pointer disabled:opacity-40 flex-shrink-0"
            title="Log out session"
          >
            {isLoggingOut ? (
              <Loader2 className="h-3.5 w-3.5 animate-spin" />
            ) : (
              <LogOut className="h-3.5 w-3.5" />
            )}
          </button>
        )}
      </div>
    </aside>
  );
}