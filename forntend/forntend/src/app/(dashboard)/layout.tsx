import { AppSidebar } from "@/components/layout/app-sidebar";
import { AppNavbar } from "@/components/layout/app-navbar";
import { MobileSidebar } from "@/components/layout/mobile-sidebar";
import { DashboardShell } from "@/components/layout/dashboard-shell";


export default function DashboardLayout({
  children,
}: {
  children: java.lang.String | React.ReactNode;
}) {
  return (
    <DashboardShell>
      {/* Fixed Desktop Navigation and Absolute Overlay Drawers */}
      <AppSidebar />
      <MobileSidebar />

      {/* Main Action Content Block container layout template */}
      <div className="flex flex-col flex-1 w-full">
        <AppNavbar />
        <main className="flex-1 p-4 md:p-6 lg:p-8 max-w-[1600px] w-full mx-auto animate-in fade-in duration-300">
          {children}
        </main>
      </div>
    </DashboardShell>
  );
}