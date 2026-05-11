"use client";

import { ChangeEvent, DragEvent, MouseEvent, useEffect, useMemo, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { flushSync } from "react-dom";

import {
  UploadAnalysis,
  uploadImage,
} from "@/lib/api";
import {
  deleteStoredUploadImage,
  getStoredUploadImage,
  listStoredUploadImages,
  saveStoredUploadImage,
} from "@/lib/recent-upload-store";
const CATEGORY_LABELS: Record<string, string> = {
  top: "상의",
  bottom: "하의",
  outer: "아우터",
  shoes: "신발",
  bag: "가방",
  accessory: "악세서리",
};

function getCategoryLabel(category: string): string {
  return CATEGORY_LABELS[category] ?? category;
}

const MIN_UPLOAD_LOADING_VISIBLE_MS = 800;

type RecentUploadCard = {
  id: string;
  name: string;
  sizeBytes: number;
  createdAt: string;
  previewUrl: string;
};

function waitForNextPaint(): Promise<void> {
  return new Promise((resolve) => {
    requestAnimationFrame(() => resolve());
  });
}

function sleep(delayMs: number): Promise<void> {
  return new Promise((resolve) => {
    window.setTimeout(resolve, delayMs);
  });
}

function formatRecentUploadDate(createdAt: string): string {
  const createdDate = new Date(createdAt);
  if (Number.isNaN(createdDate.getTime())) {
    return "업로드 시각 정보 없음";
  }

  return createdDate.toLocaleString("ko-KR", {
    month: "numeric",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
  });
}

function formatFileSize(sizeBytes: number): string {
  if (sizeBytes < 1024 * 1024) {
    return `${Math.max(1, Math.round(sizeBytes / 1024))}KB`;
  }

  return `${(sizeBytes / (1024 * 1024)).toFixed(1)}MB`;
}

export default function UploadPage() {
  const router = useRouter();
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const recentUploadPreviewUrlsRef = useRef<string[]>([]);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadStartedAt, setUploadStartedAt] = useState<number | null>(null);
  const [uploadElapsedMs, setUploadElapsedMs] = useState(0);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [filePreviewUrl, setFilePreviewUrl] = useState("");
  const [analysis, setAnalysis] = useState<UploadAnalysis | null>(null);
  const [isDragActive, setIsDragActive] = useState(false);
  const [recentUploads, setRecentUploads] = useState<RecentUploadCard[]>([]);

  const fileName = useMemo(() => selectedFile?.name ?? "", [selectedFile]);
  const analysisQueryHints = analysis?.category_query_hints ?? {};

  function revokeRecentUploadPreviewUrls() {
    for (const previewUrl of recentUploadPreviewUrlsRef.current) {
      URL.revokeObjectURL(previewUrl);
    }
    recentUploadPreviewUrlsRef.current = [];
  }

  async function refreshRecentUploads() {
    try {
      const storedUploads = await listStoredUploadImages();
      const nextRecentUploads = storedUploads.map((storedUpload) => ({
        id: storedUpload.id,
        name: storedUpload.name,
        sizeBytes: storedUpload.sizeBytes,
        createdAt: storedUpload.createdAt,
        previewUrl: URL.createObjectURL(storedUpload.blob),
      }));

      revokeRecentUploadPreviewUrls();
      recentUploadPreviewUrlsRef.current = nextRecentUploads.map((item) => item.previewUrl);
      setRecentUploads(nextRecentUploads);
    } catch (storageError) {
      console.warn("최근 업로드 이미지를 불러오지 못했습니다.", storageError);
      revokeRecentUploadPreviewUrls();
      setRecentUploads([]);
    }
  }

  useEffect(() => {
    document.title = "스타일매치 | 업로드";
  }, []);

  useEffect(() => {
    void refreshRecentUploads();

    return () => {
      revokeRecentUploadPreviewUrls();
    };
  }, []);

  useEffect(() => {
    if (!selectedFile) {
      setFilePreviewUrl("");
      return;
    }

    const objectUrl = URL.createObjectURL(selectedFile);
    setFilePreviewUrl(objectUrl);
    return () => {
      URL.revokeObjectURL(objectUrl);
    };
  }, [selectedFile]);

  useEffect(() => {
    if (!uploading || uploadStartedAt === null) {
      setUploadElapsedMs(0);
      return;
    }

    setUploadElapsedMs(Date.now() - uploadStartedAt);
    const timer = window.setInterval(() => {
      setUploadElapsedMs(Date.now() - uploadStartedAt);
    }, 1000);

    return () => {
      window.clearInterval(timer);
    };
  }, [uploadStartedAt, uploading]);

  function applySelectedFile(nextFile: File | null) {
    setSelectedFile(nextFile);
    setErrorMessage(null);
    setSuccessMessage(null);
    setAnalysis(null);
  }

  function handleOpenFilePicker() {
    fileInputRef.current?.click();
  }

  function handleResetSelectedFile(event?: MouseEvent<HTMLButtonElement>) {
    event?.stopPropagation();
    setSelectedFile(null);
    setErrorMessage(null);
    setSuccessMessage(null);
    setAnalysis(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  }

  function handleFileChange(event: ChangeEvent<HTMLInputElement>) {
    applySelectedFile(event.target.files?.[0] ?? null);
  }

  function handleDragEnter(event: DragEvent<HTMLDivElement>) {
    event.preventDefault();
    event.stopPropagation();
    setIsDragActive(true);
  }

  function handleDragOver(event: DragEvent<HTMLDivElement>) {
    event.preventDefault();
    event.stopPropagation();
    event.dataTransfer.dropEffect = "copy";
    setIsDragActive(true);
  }

  function handleDragLeave(event: DragEvent<HTMLDivElement>) {
    event.preventDefault();
    event.stopPropagation();
    setIsDragActive(false);
  }

  function handleDrop(event: DragEvent<HTMLDivElement>) {
    event.preventDefault();
    event.stopPropagation();
    setIsDragActive(false);

    const nextFile = event.dataTransfer.files?.[0] ?? null;
    if (!nextFile) {
      return;
    }

    if (!nextFile.type.startsWith("image/")) {
      setErrorMessage("이미지 파일만 업로드할 수 있습니다.");
      setSuccessMessage(null);
      return;
    }

    applySelectedFile(nextFile);
  }

  async function runUpload(fileToUpload: File, historyRecordId?: string) {
    const uploadStartedAt = Date.now();
    flushSync(() => {
      setUploading(true);
      setUploadStartedAt(uploadStartedAt);
      setUploadElapsedMs(0);
      setErrorMessage(null);
      setSuccessMessage(null);
    });
    await waitForNextPaint();

    try {
      const uploaded = await uploadImage(fileToUpload);
      let savedRecentUploadId: string | null = historyRecordId ?? null;
      try {
        savedRecentUploadId = await saveStoredUploadImage(fileToUpload, {
          id: historyRecordId,
          name: fileToUpload.name,
          type: fileToUpload.type || "image/jpeg",
          uploadedImageId: uploaded.id,
        });
      } catch (storageError) {
        console.warn("최근 업로드 이미지 저장에 실패했습니다.", storageError);
      }
      if (savedRecentUploadId) {
        await refreshRecentUploads();
      }
      const elapsedMs = Date.now() - uploadStartedAt;
      if (elapsedMs < MIN_UPLOAD_LOADING_VISIBLE_MS) {
        await sleep(MIN_UPLOAD_LOADING_VISIBLE_MS - elapsedMs);
      }
      setAnalysis(uploaded.analysis);
      setSuccessMessage("업로드가 완료되었습니다. 추천 페이지로 이동합니다.");
      const nextUrl = `/recommendations?uploaded_image_id=${encodeURIComponent(uploaded.id)}`;
      router.push(nextUrl);
      if (typeof window !== "undefined") {
        window.location.assign(nextUrl);
      }
    } catch (error) {
      const message = error instanceof Error ? error.message : "업로드 중 오류가 발생했습니다.";
      setErrorMessage(message);
    } finally {
      setUploading(false);
      setUploadStartedAt(null);
      setUploadElapsedMs(0);
    }
  }

  async function handleUpload() {
    if (!selectedFile) {
      setErrorMessage("업로드할 이미지 파일을 선택해주세요.");
      return;
    }

    await runUpload(selectedFile);
  }

  async function handleReuseRecentUpload(recentUploadId: string) {
    if (uploading) {
      return;
    }

    setErrorMessage(null);
    setSuccessMessage(null);

    const storedUpload = await getStoredUploadImage(recentUploadId);
    if (!storedUpload) {
      setErrorMessage("저장된 최근 업로드 이미지를 찾지 못했습니다. 목록을 다시 불러옵니다.");
      await refreshRecentUploads();
      return;
    }

    const reusableFile = new File([storedUpload.blob], storedUpload.name, {
      type: storedUpload.type || "image/jpeg",
      lastModified: Date.parse(storedUpload.createdAt) || Date.now(),
    });
    applySelectedFile(reusableFile);
    await runUpload(reusableFile, recentUploadId);
  }

  async function handleDeleteRecentUpload(recentUploadId: string, event: MouseEvent<HTMLButtonElement>) {
    event.stopPropagation();
    await deleteStoredUploadImage(recentUploadId);
    await refreshRecentUploads();
  }

  const elapsedMinutes = Math.floor(uploadElapsedMs / 60_000);
  const elapsedSeconds = Math.floor((uploadElapsedMs % 60_000) / 1000);
  const uploadElapsedLabel = `분석 진행 시간 : ${elapsedMinutes}분 ${elapsedSeconds}초`;
  const uploadInstruction = isDragActive
    ? "이미지를 이곳에 놓아주세요.\n클릭해서 업로드할 수도 있습니다."
    : "이미지를 이곳으로 드래그하거나\n클릭해서 업로드 해주세요.";

  return (
    <section className="split-grid upload-reference-grid" aria-label="코디 이미지 업로드">
      <article className="card upload-reference-shell" aria-busy={uploading}>
        <div className="upload-stage-card">
          <div className="upload-stage-frame">
            <div className="upload-stage-copy">
              <h1>이미지로 상품 찾기</h1>
            </div>
            <div
              className={`upload-stage-unified-zone${isDragActive ? " is-drag-active" : ""}${filePreviewUrl ? " has-preview" : ""}`}
              role="button"
              tabIndex={0}
              aria-label="코디 이미지 업로드 영역"
              aria-busy={uploading}
              onClick={() => {
                if (!uploading) {
                  handleOpenFilePicker();
                }
              }}
              onDragEnter={handleDragEnter}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onKeyDown={(event) => {
                if (event.key === "Enter" || event.key === " ") {
                  event.preventDefault();
                  handleOpenFilePicker();
                }
              }}
            >
              <div className="upload-stage-unified-copy">
                {!filePreviewUrl ? (
                  <span className="upload-stage-icon" aria-hidden="true">
                    <svg viewBox="0 0 24 24" focusable="false">
                      <path
                        d="M9 5.5 10.2 4h3.6L15 5.5H19A2.5 2.5 0 0 1 21.5 8v8A2.5 2.5 0 0 1 19 18.5H5A2.5 2.5 0 0 1 2.5 16V8A2.5 2.5 0 0 1 5 5.5h4Z"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="1.8"
                        strokeLinejoin="round"
                      />
                      <circle cx="12" cy="12" r="3.5" fill="none" stroke="currentColor" strokeWidth="1.8" />
                    </svg>
                  </span>
                ) : null}
                {filePreviewUrl ? <strong>{fileName}</strong> : null}
                <span className="upload-stage-instruction">
                  {filePreviewUrl ? "선택한 이미지를 다시 클릭하면\n다른 파일로 바꿀 수 있습니다." : uploadInstruction}
                </span>
                <small>허용 이미지: PNG, JPG, JPEG, WEBP</small>
              </div>
              {filePreviewUrl ? (
                <div className="upload-stage-square">
                  <img src={filePreviewUrl} alt={`선택한 이미지 미리보기: ${fileName}`} className="upload-stage-image" />
                </div>
              ) : null}
              {selectedFile ? (
                <button type="button" className="upload-remove-button" onClick={handleResetSelectedFile}>
                  사진 삭제
                </button>
              ) : null}
              {analysis ? (
                <div className="upload-stage-analysis">
                  <span>{analysis.dominant_tone}</span>
                  {analysis.dominant_color ? <span>{analysis.dominant_color}</span> : null}
                  <span>{analysis.style_mood}</span>
                  <span>{analysis.silhouette}</span>
                </div>
              ) : null}
              {uploading ? (
                <div className="upload-stage-loading" role="status" aria-live="polite" aria-label="이미지 분석 진행 표시">
                  <span className="loading-spinner" aria-hidden="true" />
                  <strong>AI가 이미지를 분석하고 있습니다</strong>
                  <span>분석이 끝나면 추천 페이지로 자동 이동합니다.</span>
                </div>
              ) : null}
            </div>
          </div>
        </div>
        <input
          ref={fileInputRef}
          id="image-input"
          type="file"
          accept="image/*"
          onChange={handleFileChange}
        />
        <div className="upload-primary-row">
          <button type="button" className="upload-primary-button" onClick={handleUpload} disabled={uploading || !selectedFile} aria-busy={uploading}>
            {uploading ? "이미지 분석 중..." : "이미지 분석하기"}
          </button>
        </div>
        {uploading ? <p className="upload-progress-text">{uploadElapsedLabel}</p> : null}
        {analysis ? (
          <div className="analysis-panel upload-inline-analysis">
            <div className="panel-title-row">
              <h2>빠른 분석</h2>
              <span className="metric-chip">추천 준비 완료</span>
            </div>
            <div className="analysis-chip-row">
              <span className="analysis-chip">톤 {analysis.dominant_tone}</span>
              {analysis.dominant_color ? <span className="analysis-chip">색상 {analysis.dominant_color}</span> : null}
              <span className="analysis-chip">무드 {analysis.style_mood}</span>
              <span className="analysis-chip">실루엣 {analysis.silhouette}</span>
            </div>
            <p className="hint-text">감지 카테고리: {analysis.preferred_categories.map(getCategoryLabel).join(", ")}</p>
            {analysis.detected_items && analysis.detected_items.length > 0 ? (
              <p className="hint-text">감지 품목: {analysis.detected_items.map((item) => item.query).join(" / ")}</p>
            ) : null}
            {Object.keys(analysisQueryHints).length > 0 ? (
              <p className="hint-text">검색 힌트: {Object.values(analysisQueryHints).join(" / ")}</p>
            ) : null}
            <p className="hint-text">분석 코드: {analysis.checksum}</p>
          </div>
        ) : null}
        <div className="status-region" aria-live="polite" aria-atomic="true">
          {errorMessage ? (
            <p className="error-text" role="alert">
              {errorMessage}
            </p>
          ) : null}
          {successMessage ? (
            <p className="success-text" role="status">
              {successMessage}
            </p>
          ) : null}
        </div>
      </article>
      <aside className="card side-panel upload-recent-panel" aria-label="최근 업로드">
        <div className="upload-recent-panel-head">
          <div className="panel-title-row">
            <h2>최근 업로드</h2>
            <span className="metric-chip">{recentUploads.length}개</span>
          </div>
        </div>
        {recentUploads.length > 0 ? (
          <ul className="simple-list recent-upload-list">
            {recentUploads.map((recentUpload) => (
              <li key={recentUpload.id} className="recent-upload-card-shell">
                <button
                  type="button"
                  className="recent-upload-card-button"
                  onClick={() => void handleReuseRecentUpload(recentUpload.id)}
                  disabled={uploading}
                >
                  <img src={recentUpload.previewUrl} alt={`${recentUpload.name} 최근 업로드 미리보기`} className="recent-upload-thumb" />
                  <div className="recent-upload-body">
                    <strong>{recentUpload.name}</strong>
                    <span className="recent-upload-meta">
                      {formatRecentUploadDate(recentUpload.createdAt)} · {formatFileSize(recentUpload.sizeBytes)}
                    </span>
                  </div>
                </button>
                <button
                  type="button"
                  className="recent-upload-delete-icon"
                  onClick={(event) => void handleDeleteRecentUpload(recentUpload.id, event)}
                  aria-label={`${recentUpload.name} 최근 업로드 삭제`}
                  disabled={uploading}
                >
                  ×
                </button>
              </li>
            ))}
          </ul>
        ) : (
          <div className="recent-upload-empty">
            <strong>최근 업로드가 없습니다.</strong>
          </div>
        )}
      </aside>
    </section>
  );
}
