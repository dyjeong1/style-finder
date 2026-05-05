"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import { usePathname } from "next/navigation";

import { listStoredUploadImages } from "@/lib/recent-upload-store";

const navItems = [
  { href: "/upload", label: "업로드" },
  { href: "/recommendations", label: "추천" },
  { href: "/wishlist", label: "위시리스트" },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const [latestUploadedImageId, setLatestUploadedImageId] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function syncLatestUploadedImageId() {
      const currentUploadedImageId =
        typeof window === "undefined" ? null : new URLSearchParams(window.location.search).get("uploaded_image_id");

      if (currentUploadedImageId) {
        setLatestUploadedImageId(currentUploadedImageId);
        return;
      }

      try {
        const storedUploads = await listStoredUploadImages();
        if (cancelled) {
          return;
        }

        const recentUploadWithServerId = storedUploads.find((item) => typeof item.uploadedImageId === "string" && item.uploadedImageId.length > 0);
        setLatestUploadedImageId(recentUploadWithServerId?.uploadedImageId ?? null);
      } catch (storageError) {
        console.warn("최근 업로드 기준 추천 링크를 복원하지 못했습니다.", storageError);
        if (!cancelled) {
          setLatestUploadedImageId(null);
        }
      }
    }

    void syncLatestUploadedImageId();

    return () => {
      cancelled = true;
    };
  }, [pathname]);

  const recommendationHref = latestUploadedImageId
    ? `/recommendations?uploaded_image_id=${encodeURIComponent(latestUploadedImageId)}`
    : "/recommendations";

  return (
    <div className="app-background">
      <a href="#main-content" className="skip-link">
        본문으로 바로가기
      </a>
      <div className="glow glow-left" />
      <div className="glow glow-right" />
      <div className="glow glow-bottom" />
      <header className="top-nav fade-in">
        <div className="nav-shell">
          <Link href="/upload" className="brand" aria-label="StyleMatch 홈으로 이동">
            <span className="brand-mark">
              <Image src="/brand/stylefinder_logo.png" alt="StyleMatch 로고" width={40} height={40} className="brand-logo-image" priority />
            </span>
            <span className="brand-copy">
              <strong>StyleMatch</strong>
              <small>이미지 기반 스타일 추천</small>
            </span>
          </Link>
          <nav className="top-nav-right" aria-label="주요 메뉴">
            <ul className="nav-list">
              {navItems.map((item, index) => {
                const active = pathname === item.href;
                const href = item.href === "/recommendations" ? recommendationHref : item.href;
                return (
                  <li key={item.href} style={{ animationDelay: `${0.05 * (index + 1)}s` }} className="stagger">
                    <Link href={href} className={active ? "nav-link active" : "nav-link"}>
                      {item.label}
                    </Link>
                  </li>
                );
              })}
            </ul>
          </nav>
        </div>
      </header>
      <main id="main-content" className="page-container fade-in" tabIndex={-1}>
        {children}
      </main>
    </div>
  );
}
