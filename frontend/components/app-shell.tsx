"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

import { clearStoredToken, clearStoredUploadedImageId, getStoredToken } from "@/lib/api";

const navItems = [
  { href: "/login", label: "Login" },
  { href: "/upload", label: "Upload" },
  { href: "/recommendations", label: "Recommendations" },
  { href: "/wishlist", label: "Wishlist" },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    setIsLoggedIn(Boolean(getStoredToken()));
  }, [pathname]);

  function handleSignOut() {
    clearStoredToken();
    clearStoredUploadedImageId();
    setIsLoggedIn(false);
  }

  return (
    <div className="app-background">
      <div className="glow glow-left" />
      <div className="glow glow-right" />
      <header className="top-nav fade-in">
        <Link href="/upload" className="brand">
          STYLEMATCH
        </Link>
        <nav className="top-nav-right">
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
            <span className={isLoggedIn ? "auth-chip auth-chip-on" : "auth-chip auth-chip-off"}>
              {isLoggedIn ? "Signed In" : "Guest"}
            </span>
            {isLoggedIn ? (
              <button type="button" className="ghost-button" onClick={handleSignOut}>
                Sign Out
              </button>
            ) : null}
          </div>
        </nav>
      </header>
      <main className="page-container fade-in">{children}</main>
    </div>
  );
}
