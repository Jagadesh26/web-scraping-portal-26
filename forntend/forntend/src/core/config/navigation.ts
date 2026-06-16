import { 
  LayoutDashboard, 
  User, 
  FileText, 
  Briefcase, 
  Sparkles, 
  Settings,
  LucideIcon
} from "lucide-react";

export interface SubNavigationItem {
  title: string;
  href: string;
}

export interface NavigationGroup {
  title: string;
  icon: LucideIcon;
  href?: string; // If it's a direct single link
  items?: SubNavigationItem[]; // If it contains an expandable menu cluster
}

export const dashboardNavigationStructure: NavigationGroup[] = [
  {
    title: "Dashboard",
    icon: LayoutDashboard,
    href: "/dashboard",
  },
  {
    title: "Profile",
    icon: User,
    href: "/profile",
  },
  {
    title: "Resume",
    icon: FileText,
    items: [
      { title: "Resume Analysis", href: "/resume" },
      { title: "Skills Profiles", href: "/resume/skills" },
      { title: "Experience", href: "/resume/experience" },
      { title: "Education Tracker", href: "/resume/education" },
      { title: "Projects Portfolio", href: "/resume/projects" },
    ],
  },
  {
    title: "Jobs Module",
    icon: Briefcase,
    items: [
      { title: "Browse Jobs", href: "/jobs" },
      { title: "Saved Listings", href: "/jobs/saved" },
    ],
  },
  {
    title: "ATS Engine",
    icon: Sparkles,
    items: [
      { title: "Recommendations", href: "/ats" },
      { title: "Skill Gap Analysis", href: "/ats/gap" },
      { title: "ATS Check Metrics", href: "/ats/checker" },
    ],
  },
  {
    title: "Settings",
    icon: Settings,
    href: "/settings",
  },
];