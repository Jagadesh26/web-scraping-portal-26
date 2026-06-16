"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useUiStore } from "@/core/store/uiStore";
import { dashboardNavigationStructure } from "@/core/config/navigation";
import { X, Sparkles, ChevronDown } from "lucide-react";
import { cn } from "@/lib/utils";
import * as React from "react";

export function MobileSidebar() {
  const pathname = usePathname();
  const { isMobileSidebarOpen, setMobileSidebarOpen } = useUiStore();
  
  // Manage expandable groups locally for mobile touch targets
  const [openGroups, setOpenGroups] = React.useState<Record<string, boolean>>({
    Resume: true,
    "Jobs Module": true,
    "ATS Engine": true,
  });

  const toggleGroup = (title: string) => {
    setOpenGroups((prev) => ({ ...prev, [title]: !prev[title] }));
  };

  if (!isMobileSidebarOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex lg:hidden animate-in fade-in duration-200">
      {/* Backdrop Overlay */}
      <div 
        className="fixed inset-0 bg-background/80 backdrop-blur-sm" 
        onClick={() => setMobileSidebarOpen(false)}
      />

      {/* Drawer Body Container */}
      <div className="relative flex w-full max-w-xs flex-col bg-card border-r border-border p-6 shadow-xl overflow-y-auto animate-in slide-in-from-left duration-300 style-scrollbar">
        
        {/* Mobile Header Branding */}
        <div className="flex items-center justify-between border-b border-border pb-4 mb-4">
          <Link 
            href="/dashboard" 
            className="flex items-center gap-2 font-bold text-base text-foreground"
            onClick={() => setMobileSidebarOpen(false)}
          >
            <Sparkles className="h-5 w-5 text-primary fill-primary/10" />
            <span>TalentAI Portal</span>
          </Link>
          <button
            onClick={() => setMobileSidebarOpen(false)}
            className="rounded-lg p-1.5 text-muted-foreground hover:bg-accent hover:text-foreground cursor-pointer"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Dynamic Navigation Tree */}
        <nav className="flex-1 space-y-2">
          {dashboardNavigationStructure.map((group) => {
            const Icon = group.icon;
            const hasSubItems = !!group.items;
            const isGroupOpen = openGroups[group.title];

            const isDirectActive = group.href ? pathname === group.href : false;
            const isSubActive = group.items?.some(sub => pathname === sub.href) || false;

            // Render single top-level link item
            if (!hasSubItems && group.href) {
              return (
                <Link
                  key={group.title}
                  href={group.href}
                  onClick={() => setMobileSidebarOpen(false)}
                  className={cn(
                    "flex items-center gap-3 px-3 py-2.5 text-xs font-semibold rounded-xl transition-all",
                    isDirectActive
                      ? "bg-primary text-primary-foreground shadow-md shadow-primary/10"
                      : "text-muted-foreground hover:bg-accent hover:text-foreground"
                  )}
                >
                  <Icon className="h-4 w-4 flex-shrink-0" />
                  <span>{group.title}</span>
                </Link>
              );
            }

            // Render expandable submenu container item
            return (
              <div key={group.title} className="space-y-1">
                <button
                  onClick={() => toggleGroup(group.title)}
                  className={cn(
                    "w-full flex items-center justify-between px-3 py-2.5 text-xs font-semibold rounded-xl transition-all text-muted-foreground hover:bg-accent hover:text-foreground cursor-pointer",
                    isSubActive && "text-foreground font-bold"
                  )}
                >
                  <div className="flex items-center gap-3 truncate">
                    <Icon className={cn("h-4 w-4 flex-shrink-0", isSubActive && "text-primary")} />
                    <span>{group.title}</span>
                  </div>
                  <ChevronDown className={cn("h-4 w-4 transition-transform duration-200", isGroupOpen && "rotate-180")} />
                </button>

                {/* Submenu links list drop down */}
                {isGroupOpen && group.items && (
                  <div className="pl-6 space-y-1 border-l border-border/80 ml-5 mt-0.5 animate-in fade-in duration-150">
                    {group.items.map((sub) => {
                      const isCurrentRoute = pathname === sub.href;
                      return (
                        <Link
                          key={sub.href}
                          href={sub.href}
                          onClick={() => setMobileSidebarOpen(false)}
                          className={cn(
                            "block px-3 py-2 text-[11px] font-semibold rounded-lg transition-colors truncate",
                            isCurrentRoute
                              ? "text-primary bg-primary/5"
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
      </div>
    </div>
  );
}