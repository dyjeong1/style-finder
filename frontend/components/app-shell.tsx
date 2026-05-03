"use client";

import Image from "next/image";
import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
  { href: "/upload", label: "업로드" },
  { href: "/recommendations", label: "추천" },
  { href: "/wishlist", label: "위시리스트" },
];

const pageMeta: Record<string, { label: string; title: string; description: string }> = {
  "/upload": {
    label: "Upload Studio",
    title: "Look to Curation",
    description: "코디 한 장을 편집된 추천 흐름으로 바꾸는 AI 스타일 스튜디오",
  },
  "/recommendations": {
    label: "Curated Feed",
    title: "Editorial Match Edit",
    description: "업로드에서 읽은 감성을 쇼핑 가능한 상품 컬렉션으로 정리하는 화면",
  },
  "/wishlist": {
    label: "Saved Board",
    title: "Personal Style Archive",
    description: "저장한 상품을 다시 비교하고 다음 쇼핑으로 이어가는 개인 컬렉션 보드",
  },
};

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const currentMeta = pageMeta[pathname] ?? pageMeta["/upload"];

  return (
    <div className="app-background">
      <a href="#main-content" className="skip-link">
        본문으로 바로가기
      </a>
      <div className="glow glow-left" />
      <div className="glow glow-right" />
      <div className="glow glow-bottom" />
      <div className="mesh-orb mesh-orb-left" />
      <div className="mesh-orb mesh-orb-right" />
      <header className="top-nav fade-in">
        <div className="nav-shell">
          <div className="nav-brand-cluster">
            <Link href="/upload" className="brand" aria-label="StyleMatch 홈으로 이동">
              <span className="brand-mark">
                <Image src="/brand/stylefinder_logo.png" alt="StyleMatch 로고" width={44} height={44} className="brand-logo-image" priority />
              </span>
              <span className="brand-copy">
                <small className="brand-label">Style Commerce Studio</small>
                <strong className="brand-wordmark">StyleMatch</strong>
              </span>
            </Link>
            <div className="brand-context">
              <span className="workspace-chip">{currentMeta.label}</span>
              <strong>{currentMeta.title}</strong>
              <small>{currentMeta.description}</small>
            </div>
          </div>
          <div className="top-nav-right">
            <nav aria-label="주요 메뉴">
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
            <div className="nav-utility">
              <span className="nav-utility-label">Current Flow</span>
              <strong>{currentMeta.label}</strong>
              <small>{currentMeta.title}</small>
            </div>
          </div>
        </div>
      </header>
      <main id="main-content" className="page-container fade-in" tabIndex={-1}>
        {children}
      </main>
    </div>
  );
}
