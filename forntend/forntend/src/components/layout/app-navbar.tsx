"use client";

import { useTheme } from "next-themes";
import { useUiStore } from "@/core/store/uiStore";
import { UserNav } from "./user-nav";
import { Menu, Sun, Moon, Bell, Search, Command } from "lucide-react";
import * as React from "react";

export function AppNavbar() {
  const { theme, setTheme } = useTheme();
  const toggleMobileSidebar = useUiStore((state) => state.toggleMobileSidebar);
  const [mounted, setMounted] = React.useState(false);

  React.useEffect(() => setMounted(true), []);

  return (
    <header className="sticky top-0 z-30 h-16 w-full border-b border-border/60 bg-background/80 backdrop-blur-md flex items-center justify-between px-4 lg:px-8">
      {/* Shell Controls & Integrated Search */}
      <div className="flex items-center gap-4 flex-1 max-w-xl">
        <button
          onClick={toggleMobileSidebar}
          className="lg:hidden p-2 -ml-2 text-muted-foreground hover:text-foreground rounded-xl hover:bg-accent cursor-pointer"
        >
          <Menu className="h-5 w-5" />
        </button>
        
        {/* Modern omni-search input layer */}
        <div className="hidden sm:flex items-center gap-2 relative w-full">
          <Search className="absolute left-3.5 h-4 w-4 text-muted-foreground/80 pointer-events-none" />
          <input
            type="text"
            placeholder="Search matching positions, active core skills, or insights analysis..."
            className="w-full bg-accent/30 hover:bg-accent/60 focus:bg-background border border-border/80 rounded-xl pl-10 pr-12 py-2 text-xs focus:outline-none focus:ring-2 focus:ring-primary/20 focus:border-primary transition-all text-foreground font-medium"
          />
          <div className="absolute right-3 hidden md:flex items-center gap-0.5 px-1.5 py-0.5 border border-border/80 bg-popover text-[10px] rounded text-muted-foreground font-bold pointer-events-none shadow-sm">
            <Command className="h-2.5 w-2.5" />
            <span>K</span>
          </div>
        </div>
      </div>

      {/* Network Utilities & Profile Context */}
      <div className="flex items-center gap-4 pl-4">
        {/* Notification bell featuring mock alerts count metric */}
        <button className="p-2 text-muted-foreground hover:text-foreground rounded-xl hover:bg-accent relative transition-colors group cursor-pointer">
          <Bell className="h-4 w-4 transition-transform group-hover:rotate-12" />
          <span className="absolute top-1.5 right-1.5 h-4 w-4 bg-primary text-[10px] font-extrabold text-primary-foreground rounded-full flex items-center justify-center shadow-sm border border-background">
            5
          </span>
        </button>

        {/* Dynamic theme color logic */}
        {mounted && (
          <button
            onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
            className="p-2 text-muted-foreground hover:text-foreground rounded-xl hover:bg-accent transition-colors cursor-pointer"
            aria-label="Toggle system interface theme color scale"
          >
            {theme === "dark" ? <Sun className="h-4 w-4 animate-in fade-in zoom-in" /> : <Moon className="h-4 w-4 animate-in fade-in zoom-in" />}
          </button>
        )}

        <div className="h-4 w-px bg-border/80 hidden sm:block" />
        
        <UserNav />
      </div>
    </header>
  );
}