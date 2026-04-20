"use client";

import { ChangeEvent, DragEvent, MouseEvent, useEffect, useMemo, useRef, useState } from "react";
import { useRouter } from "next/navigation";

import {
  getUploadHistory,
  prependUploadHistory,
  setStoredUploadedImageAnalysis,
  setStoredUploadedImageId,
  UploadAnalysis,
  UploadHistoryItem,
  uploadImage,
} from "@/lib/api";

function buildRecentFallbackImage(item: UploadHistoryItem): string {
  const label = item.file_name.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const subtitle = `${item.analysis.dominant_tone} / ${item.analysis.style_mood} / ${item.analysis.silhouette}`;
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" width="240" height="240" viewBox="0 0 240 240">
      <defs>
        <linearGradient id="g" x1="0" x2="1" y1="0" y2="1">
          <stop offset="0%" stop-color="#f5ead6" />
          <stop offset="100%" stop-color="#ead8bb" />
        </linearGradient>
      </defs>
      <rect width="240" height="240" rx="28" fill="url(#g)" />
      <rect x="18" y="18" width="204" height="204" rx="22" fill="rgba(255,255,255,0.45)" />
      <text x="30" y="78" fill="#111827" font-family="Pretendard, Arial, sans-serif" font-size="22" font-weight="700">${label}</text>
      <text x="30" y="118" fill="#6b7280" font-family="Pretendard, Arial, sans-serif" font-size="14">${subtitle}</text>
    </svg>
  `;

  return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`;
}

export default function UploadPage() {
  const router = useRouter();
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [filePreviewUrl, setFilePreviewUrl] = useState("");
  const [analysis, setAnalysis] = useState<UploadAnalysis | null>(null);
  const [recentUploads, setRecentUploads] = useState<UploadHistoryItem[]>([]);
  const [isDragActive, setIsDragActive] = useState(false);

  const fileName = useMemo(() => selectedFile?.name ?? "", [selectedFile]);

  useEffect(() => {
    setRecentUploads(getUploadHistory());
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

    setUploading(true);
    setErrorMessage(null);
    setSuccessMessage(null);

    try {
      const uploaded = await uploadImage(selectedFile);
      setStoredUploadedImageId(uploaded.id);
      setStoredUploadedImageAnalysis(uploaded.analysis);
      setAnalysis(uploaded.analysis);
      setRecentUploads(
        prependUploadHistory({
          id: uploaded.id,
          image_url: uploaded.image_url,
          created_at: uploaded.created_at,
          file_name: selectedFile.name,
          analysis: uploaded.analysis,
        }),
      );
      setSuccessMessage("업로드가 완료되었습니다. 추천 페이지로 이동합니다.");
      router.push("/recommendations");
    } catch (error) {
      const message = error instanceof Error ? error.message : "업로드 중 오류가 발생했습니다.";
      setErrorMessage(message);
    } finally {
      setUploading(false);
    }
  }

  function handleReuseUpload(item: UploadHistoryItem) {
    setStoredUploadedImageId(item.id);
    setStoredUploadedImageAnalysis(item.analysis);
    router.push("/recommendations");
  }

  return (
    <section className="split-grid upload-reference-grid" aria-labelledby="upload-title">
      <article className="card upload-reference-shell" aria-busy={uploading}>
        <div className="upload-stage-card">
          <div className="upload-stage-frame">
            <div className="upload-stage-copy">
              <h1 id="upload-title">코디 이미지를 올려보세요</h1>
              <p className="lead page-lead">한 장만 올리면 바로 추천 리스트를 만듭니다.</p>
            </div>
            <div
              className={`upload-stage-unified-zone${isDragActive ? " is-drag-active" : ""}${filePreviewUrl ? " has-preview" : ""}`}
              role="button"
              tabIndex={0}
              aria-label="코디 이미지 업로드 영역"
              onClick={handleOpenFilePicker}
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
              <div className="upload-stage-square">
                {filePreviewUrl ? (
                  <img src={filePreviewUrl} alt={`선택한 이미지 미리보기: ${fileName}`} className="upload-stage-image" />
                ) : (
                  <div className="upload-stage-placeholder" aria-hidden="true">
                    <strong>이미지를 선택하면 여기에 보입니다</strong>
                  </div>
                )}
              </div>
              <div className="upload-stage-unified-copy">
                <strong>{fileName || "코디 이미지 업로드"}</strong>
                <span>{isDragActive ? "여기에 이미지를 놓아주세요" : "클릭하거나 이미지를 끌어다 놓아 선택하세요."}</span>
              </div>
              {selectedFile ? (
                <button type="button" className="upload-remove-button" onClick={handleResetSelectedFile}>
                  사진 삭제
                </button>
              ) : null}
              {analysis ? (
                <div className="upload-stage-analysis">
                  <span>{analysis.dominant_tone}</span>
                  <span>{analysis.style_mood}</span>
                  <span>{analysis.silhouette}</span>
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
        {analysis ? (
          <div className="analysis-panel upload-inline-analysis">
            <div className="panel-title-row">
              <h2>Quick Analysis</h2>
              <span className="metric-chip">ready for recommendations</span>
            </div>
            <div className="analysis-chip-row">
              <span className="analysis-chip">tone {analysis.dominant_tone}</span>
              <span className="analysis-chip">mood {analysis.style_mood}</span>
              <span className="analysis-chip">fit {analysis.silhouette}</span>
            </div>
            <p className="hint-text">preferred: {analysis.preferred_categories.join(", ")}</p>
            <p className="hint-text">checksum: {analysis.checksum}</p>
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

      <article className="card side-panel upload-recent-panel" aria-labelledby="recent-upload-title">
        <div className="section-heading-row">
          <div>
            <h2 id="recent-upload-title">최근 업로드</h2>
          </div>
        </div>
        {recentUploads.length > 0 ? (
          <ul className="simple-list recent-upload-list">
            {recentUploads.map((item) => (
              <li key={item.id} className="recent-upload-card">
                <button type="button" className="recent-upload-card-button" onClick={() => handleReuseUpload(item)}>
                  <img
                    src={item.image_url}
                    alt={`${item.file_name} 썸네일`}
                    className="recent-upload-thumb"
                    onError={(event) => {
                      event.currentTarget.onerror = null;
                      event.currentTarget.src = buildRecentFallbackImage(item);
                    }}
                  />
                  <div className="recent-upload-body">
                    <strong>{item.file_name}</strong>
                    <p className="hint-text">
                      {item.analysis.dominant_tone} / {item.analysis.style_mood} / {item.analysis.silhouette}
                    </p>
                    <p className="hint-text">{new Date(item.created_at).toLocaleString("ko-KR")}</p>
                  </div>
                </button>
              </li>
            ))}
          </ul>
        ) : (
          <div className="empty-box soft-empty-box">
            <p className="lead">아직 최근 업로드가 없습니다.</p>
          </div>
        )}
      </article>
    </section>
  );
}
