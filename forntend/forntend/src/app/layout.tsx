import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "@/styles/globals.css";
import { AppProvider } from "@/core/providers/app-provider";

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" });

export const metadata: Metadata = {
  title: "Enterprise AI Job Portal & Resume Intelligence",
  description: "Next-Generation Production Recruitment and Score Engine Platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.variable} font-sans min-h-screen dynamic-scrollbar`}>
        <AppProvider>
          {children}
        </AppProvider>
      </body>
    </html>
  );
}