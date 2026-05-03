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
    title: "스타일을 올리고 바로 분석하세요",
    description: "한 장의 코디 이미지를 기준으로 AI 추천 흐름을 바로 시작합니다.",
  },
  "/recommendations": {
    label: "Curated Feed",
    title: "업로드 기반 추천 컬렉션",
    description: "분석 신호와 쇼핑 흐름을 한 화면에서 이어보는 큐레이션 영역입니다.",
  },
  "/wishlist": {
    label: "Saved Board",
    title: "저장한 스타일을 다시 비교하세요",
    description: "찜한 상품을 재정렬하고 다시 쇼핑으로 이어갈 수 있는 개인 보드입니다.",
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
                <strong>StyleMatch</strong>
                <small>이미지 기반 스타일 추천</small>
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
