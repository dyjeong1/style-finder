import type { Metadata } from "next";
import { Fraunces, Space_Grotesk } from "next/font/google";

import "./globals.css";
import { AppShell } from "@/components/app-shell";

const headingFont = Fraunces({
  subsets: ["latin"],
  variable: "--font-heading",
});

const bodyFont = Space_Grotesk({
  subsets: ["latin"],
  variable: "--font-body",
});

export const metadata: Metadata = {
  title: "StyleMatch Frontend MVP",
  description: "Frontend scaffold for StyleMatch private service",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="ko">
      <body className={`${headingFont.variable} ${bodyFont.variable}`}>
        <AppShell>{children}</AppShell>
      </body>
    </html>
  );
}
