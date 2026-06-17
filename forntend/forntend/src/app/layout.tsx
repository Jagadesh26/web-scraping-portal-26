import type { Metadata } from "next";
import { AppProvider } from "@/core/providers/app-provider";
import "@/styles/globals.css";

export const metadata: Metadata = {
  title: "TalentAI - Web Scraping Portal",
  description: "A modern web scraping portal built with Next.js",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <AppProvider>{children}</AppProvider>
      </body>
    </html>
  );
}