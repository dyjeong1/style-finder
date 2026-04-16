"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { clearStoredUploadedImageAnalysis, clearStoredUploadedImageId } from "@/lib/api";

const navItems = [
  { href: "/upload", label: "Upload" },
  { href: "/recommendations", label: "Recommendations" },
  { href: "/wishlist", label: "Wishlist" },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  function handleResetUpload() {
    clearStoredUploadedImageId();
    clearStoredUploadedImageAnalysis();
  }

  return (
    <div className="app-background">
      <a href="#main-content" className="skip-link">
        본문으로 바로가기
      </a>
      <div className="glow glow-left" />
      <div className="glow glow-right" />
      <header className="top-nav fade-in">
        <Link href="/upload" className="brand">
          STYLEMATCH
        </Link>
        <nav className="top-nav-right" aria-label="주요 메뉴">
          <ul className="nav-list">
            {navItems.map((item, index) => {
              const active = pathname === item.href;
              return (
                <li key={item.href} style={{ animationDelay: `${0.05 * (index + 1)}s` }} className="stagger">
                  <Link href={item.href} className={active ? "nav-link active" : "nav-link"}>
                    {item.label}
                  </Link>
                </li>
              );
            })}
          </ul>
          <div className="auth-chip-wrap">
            <span className="auth-chip auth-chip-on">Local Mode</span>
            {pathname !== "/upload" ? (
              <button type="button" className="ghost-button" onClick={handleResetUpload}>
                Reset Upload
              </button>
            ) : null}
          </div>
        </nav>
      </header>
      <main id="main-content" className="page-container fade-in" tabIndex={-1}>
        {children}
      </main>
    </div>
  );
}
