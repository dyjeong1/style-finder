"use client";

import { ChangeEvent, DragEvent, MouseEvent, useEffect, useMemo, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import { flushSync } from "react-dom";

import {
  UploadAnalysis,
  uploadImage,
} from "@/lib/api";
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

export default function UploadPage() {
  const router = useRouter();
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadStartedAt, setUploadStartedAt] = useState<number | null>(null);
  const [uploadElapsedMs, setUploadElapsedMs] = useState(0);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [filePreviewUrl, setFilePreviewUrl] = useState("");
  const [analysis, setAnalysis] = useState<UploadAnalysis | null>(null);
  const [isDragActive, setIsDragActive] = useState(false);

  const fileName = useMemo(() => selectedFile?.name ?? "", [selectedFile]);
  const analysisQueryHints = analysis?.category_query_hints ?? {};

  useEffect(() => {
    document.title = "스타일매치 | 업로드";
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

  async function handleUpload() {
    if (!selectedFile) {
      setErrorMessage("업로드할 이미지 파일을 선택해주세요.");
      return;
    }

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
      const uploaded = await uploadImage(selectedFile);
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

  const elapsedMinutes = Math.floor(uploadElapsedMs / 60_000);
  const elapsedSeconds = Math.floor((uploadElapsedMs % 60_000) / 1000);
  const uploadElapsedLabel = `분석 진행 시간 : ${elapsedMinutes}분 ${elapsedSeconds}초`;

  return (
    <section className="upload-reference-grid" aria-label="코디 이미지 업로드">
      <article className="card upload-reference-shell" aria-busy={uploading}>
        <div className="upload-stage-card">
          <div className="upload-stage-frame">
            <div className="upload-stage-copy">
              <p className="lead page-lead">이미지를 넣으면 유사한 상품을 추천해드립니다.</p>
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
                <strong>{fileName || "코디 이미지 업로드"}</strong>
                <span>{isDragActive ? "여기에 이미지를 놓아주세요" : "클릭하거나 이미지를 끌어다 놓아 주세요."}</span>
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
          {uploading ? <p className="upload-progress-text">{uploadElapsedLabel}</p> : null}
        </div>
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
    </section>
  );
}
