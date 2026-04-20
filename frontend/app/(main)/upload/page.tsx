"use client";

import { ChangeEvent, useEffect, useMemo, useState } from "react";
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

export default function UploadPage() {
  const router = useRouter();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [filePreviewUrl, setFilePreviewUrl] = useState("");
  const [analysis, setAnalysis] = useState<UploadAnalysis | null>(null);
  const [recentUploads, setRecentUploads] = useState<UploadHistoryItem[]>([]);

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

  function handleFileChange(event: ChangeEvent<HTMLInputElement>) {
    const nextFile = event.target.files?.[0] ?? null;
    setSelectedFile(nextFile);
    setErrorMessage(null);
    setSuccessMessage(null);
    setAnalysis(null);
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
    <section className="split-grid" aria-labelledby="upload-title">
      <article className="card upload-dropzone" aria-busy={uploading}>
        <div className="page-header page-header-accent">
          <p className="eyebrow">Style intake</p>
          <h1 id="upload-title">오늘의 코디 이미지를 올려보세요</h1>
          <p className="lead page-lead">
            한 장의 이미지로 톤, 무드, 실루엣을 분석하고 바로 추천 리스트를 만듭니다.
          </p>
          <div className="page-summary-grid">
            <div className="summary-pill">
              <span className="summary-label">Mode</span>
              <strong>Single user</strong>
            </div>
            <div className="summary-pill">
              <span className="summary-label">Recent uploads</span>
              <strong>{recentUploads.length}</strong>
            </div>
            <div className="summary-pill">
              <span className="summary-label">Best with</span>
              <strong>OOTD, lookbook</strong>
            </div>
          </div>
        </div>

        <label className="dropzone" htmlFor="image-input">
          <span className="dropzone-badge">Drop or browse</span>
          <strong>{fileName || "코디 이미지 업로드"}</strong>
          <span>JPG, PNG, WEBP 이미지를 올리면 바로 분석을 시작합니다.</span>
        </label>
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
        <div className="button-row">
          <button type="button" onClick={handleUpload} disabled={uploading} aria-busy={uploading}>
            {uploading ? "Analyzing..." : "Upload & Analyze"}
          </button>
          <span className="micro-copy">로컬 단일 사용자 모드로 바로 저장됩니다.</span>
        </div>
        {filePreviewUrl ? (
          <div className="preview-wrap preview-frame">
            <img src={filePreviewUrl} alt={`선택한 이미지 미리보기: ${fileName}`} className="preview-image" />
          </div>
        ) : null}
        {analysis ? (
          <div className="analysis-panel">
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

      <article className="card side-panel" aria-labelledby="recent-upload-title">
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
                <img src={item.image_url} alt={`${item.file_name} 썸네일`} className="recent-upload-thumb" />
                <div className="recent-upload-body">
                  <strong>{item.file_name}</strong>
                  <p className="hint-text">
                    {item.analysis.dominant_tone} / {item.analysis.style_mood} / {item.analysis.silhouette}
                  </p>
                  <p className="hint-text">{new Date(item.created_at).toLocaleString("ko-KR")}</p>
                </div>
                <button type="button" className="ghost-button" onClick={() => handleReuseUpload(item)}>
                  추천 다시 보기
                </button>
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
