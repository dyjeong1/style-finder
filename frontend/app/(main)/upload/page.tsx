"use client";

import { ChangeEvent, DragEvent, useEffect, useMemo, useState } from "react";
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

  function handleFileChange(event: ChangeEvent<HTMLInputElement>) {
    applySelectedFile(event.target.files?.[0] ?? null);
  }

  function handleDragEnter(event: DragEvent<HTMLLabelElement>) {
    event.preventDefault();
    event.stopPropagation();
    setIsDragActive(true);
  }

  function handleDragOver(event: DragEvent<HTMLLabelElement>) {
    event.preventDefault();
    event.stopPropagation();
    event.dataTransfer.dropEffect = "copy";
    setIsDragActive(true);
  }

  function handleDragLeave(event: DragEvent<HTMLLabelElement>) {
    event.preventDefault();
    event.stopPropagation();
    setIsDragActive(false);
  }

  function handleDrop(event: DragEvent<HTMLLabelElement>) {
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
          <p className="eyebrow">Style intake</p>
          <div className="upload-stage-frame">
            <div className="upload-stage-copy">
              <h1 id="upload-title">코디 이미지를 올려보세요</h1>
              <p className="lead page-lead">한 장의 이미지로 톤, 무드, 실루엣을 분석하고 추천 리스트를 만듭니다.</p>
            </div>
            <div className="upload-stage-preview">
              {filePreviewUrl ? (
                <img src={filePreviewUrl} alt={`선택한 이미지 미리보기: ${fileName}`} className="upload-stage-image" />
              ) : (
                <div className="upload-stage-placeholder" aria-hidden="true">
                  <span className="upload-stage-placeholder-chip">Preview</span>
                  <strong>선택한 이미지가 이곳에 표시됩니다</strong>
                  <p>룩북, 셀피, 스크린샷 모두 업로드할 수 있어요.</p>
                </div>
              )}
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

        <div className="upload-action-card">
          <label
            className={`dropzone upload-reference-dropzone${isDragActive ? " is-drag-active" : ""}`}
            htmlFor="image-input"
            onDragEnter={handleDragEnter}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
          >
            <span className="dropzone-badge">Drop or browse</span>
            <strong>{fileName || "코디 이미지 업로드"}</strong>
            <span>{isDragActive ? "여기에 이미지를 놓아주세요" : "JPG, PNG, WEBP 이미지를 올리면 바로 분석을 시작합니다."}</span>
          </label>
        </div>
        <input
          id="image-input"
          type="file"
          accept="image/*"
          aria-describedby="upload-description upload-help"
          onChange={handleFileChange}
        />
        <p id="upload-help" className="hint-text compact-hint">
          모바일 스크린샷, 룩북 이미지, 셀피 착장 사진 모두 테스트 가능합니다.
        </p>
        <div className="upload-primary-row">
          <button type="button" className="upload-primary-button" onClick={handleUpload} disabled={uploading} aria-busy={uploading}>
            {uploading ? "이미지 분석 중..." : "이미지 분석하기"}
          </button>
          <span className="micro-copy">로컬 단일 사용자 모드로 바로 저장됩니다.</span>
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
            <p className="eyebrow">Recent</p>
            <h2 id="recent-upload-title">최근 업로드</h2>
          </div>
          <span className="section-badge">{recentUploads.length} items</span>
        </div>
        {recentUploads.length > 0 ? (
          <ul className="simple-list recent-upload-list">
            {recentUploads.map((item) => (
              <li key={item.id} className="recent-upload-card">
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
                  <button type="button" className="recent-upload-action" onClick={() => handleReuseUpload(item)}>
                    추천 상품 보기
                  </button>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <div className="empty-box soft-empty-box">
            <p className="lead">아직 최근 업로드가 없습니다.</p>
            <p className="hint-text">첫 이미지를 올리면 여기서 최근 분석 이력을 다시 확인할 수 있습니다.</p>
          </div>
        )}
      </article>
    </section>
  );
}
