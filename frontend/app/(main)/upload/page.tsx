"use client";

import { ChangeEvent, useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

import {
  getStoredToken,
  setStoredUploadedImageAnalysis,
  setStoredUploadedImageId,
  UploadAnalysis,
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

  const fileName = useMemo(() => selectedFile?.name ?? "", [selectedFile]);

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
    const token = getStoredToken();
    if (!token) {
      setErrorMessage("로그인이 필요합니다. 먼저 로그인해주세요.");
      return;
    }

    if (!selectedFile) {
      setErrorMessage("업로드할 이미지 파일을 선택해주세요.");
      return;
    }

    setUploading(true);
    setErrorMessage(null);
    setSuccessMessage(null);

    try {
      const uploaded = await uploadImage(selectedFile, token);
      setStoredUploadedImageId(uploaded.id);
      setStoredUploadedImageAnalysis(uploaded.analysis);
      setAnalysis(uploaded.analysis);
      setSuccessMessage("업로드가 완료되었습니다. 추천 페이지로 이동합니다.");
      router.push("/recommendations");
    } catch (error) {
      const message = error instanceof Error ? error.message : "업로드 중 오류가 발생했습니다.";
      setErrorMessage(message);
    } finally {
      setUploading(false);
    }
  }

  return (
    <section className="split-grid" aria-labelledby="upload-title">
      <article className="card upload-dropzone" aria-busy={uploading}>
        <p className="eyebrow">Step 1</p>
        <h1 id="upload-title">Upload Outfit Image</h1>
        <p id="upload-description" className="lead">
          코디 이미지를 올리면 카테고리별 추천 결과를 생성합니다.
        </p>
        <label className="dropzone" htmlFor="image-input">
          {fileName || "Drop image here or click to browse"}
        </label>
        <input
          id="image-input"
          type="file"
          accept="image/*"
          aria-describedby="upload-description upload-help"
          onChange={handleFileChange}
        />
        <p id="upload-help" className="hint-text">
          JPG, PNG, WEBP 등 이미지 파일을 선택할 수 있습니다.
        </p>
        <button type="button" onClick={handleUpload} disabled={uploading} aria-busy={uploading}>
          {uploading ? "Uploading..." : "Upload & Analyze"}
        </button>
        {filePreviewUrl ? (
          <div className="preview-wrap">
            <img src={filePreviewUrl} alt={`선택한 이미지 미리보기: ${fileName}`} className="preview-image" />
          </div>
        ) : null}
        {analysis ? (
          <div className="analysis-panel">
            <h2>Quick Analysis</h2>
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
        <p className="hint-text">
          로그인을 아직 하지 않았다면 <Link href="/login">로그인 페이지</Link>에서 먼저 인증하세요.
        </p>
      </article>
      <article className="card" aria-labelledby="recent-upload-title">
        <p className="eyebrow">Recent</p>
        <h2 id="recent-upload-title">최근 업로드</h2>
        <ul className="simple-list">
          <li>street-look-0413.png</li>
          <li>spring-office-fit.jpg</li>
          <li>weekend-casual.webp</li>
        </ul>
      </article>
    </section>
  );
}
