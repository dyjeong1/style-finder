"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
  { href: "/login", label: "Login" },
  { href: "/upload", label: "Upload" },
  { href: "/recommendations", label: "Recommendations" },
  { href: "/wishlist", label: "Wishlist" },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();

  return (
    <div className="app-background">
      <div className="glow glow-left" />
      <div className="glow glow-right" />
      <header className="top-nav fade-in">
        <Link href="/upload" className="brand">
          STYLEMATCH
        </Link>
        <nav>
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
        </nav>
      </header>
      <main className="page-container fade-in">{children}</main>
    </div>
  );
}
