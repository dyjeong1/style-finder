"use client";

import { ChangeEvent, DragEvent, MouseEvent, useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";

import { UploadAnalysis, uploadImage } from "@/lib/api";

const CATEGORY_LABELS: Record<string, string> = {
  top: "상의",
  bottom: "하의",
  outer: "아우터",
  shoes: "신발",
  bag: "가방",
  accessory: "악세서리",
};

const STUDIO_SIGNALS = [
  "톤과 주요 색감을 먼저 읽어냅니다.",
  "착장 무드와 실루엣을 함께 정리합니다.",
  "감지 품목별 검색어를 만들어 추천으로 연결합니다.",
];

const CURATION_STEPS = ["이미지 업로드", "AI 스타일 분석", "카테고리별 검색어 생성", "추천 피드 큐레이션"];
const DEFAULT_CURATION_HINTS = ["미니멀 재킷", "와이드 팬츠", "메리제인 슈즈", "숄더백", "실버 주얼리"];

function getCategoryLabel(category: string): string {
  return CATEGORY_LABELS[category] ?? category;
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
  const [isDragActive, setIsDragActive] = useState(false);

  const fileName = selectedFile?.name ?? "";
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
    }
  }

  return (
    <section className="upload-page" aria-label="코디 이미지 업로드">
      <article className="upload-hero-panel upload-hero-panel-luxe" aria-busy={uploading}>
        <div className="upload-hero-copy">
          <p className="eyebrow">Upload Studio</p>
          <h1 className="display-title">A single look, turned into a shoppable edit.</h1>
          <p className="lead page-lead">
            지금 올리는 코디 한 장을 기준으로 톤, 무드, 실루엣, 감지 품목을 읽고 바로 쇼핑 가능한 스타일 피드로 연결합니다.
          </p>
          <div className="hero-signal-row">
            <span className="hero-pill">AI 스타일 분석</span>
            <span className="hero-pill">1장 기준 추천</span>
            <span className="hero-pill">카테고리별 큐레이션</span>
          </div>
          <div className="upload-hero-rail">
            <div className="editorial-note">
              <span>Studio Mood</span>
              <strong>Warm minimal, structured silhouette, curated shopping flow.</strong>
            </div>
            <ol className="step-rail">
              {CURATION_STEPS.map((step, index) => (
                <li key={step}>
                  <span>{String(index + 1).padStart(2, "0")}</span>
                  <strong>{step}</strong>
                </li>
              ))}
            </ol>
          </div>
        </div>

        <div className="upload-stage-shell upload-stage-shell-luxe">
          <div className="upload-stage-frame">
            <div className="upload-stage-heading">
              <span className="workspace-chip">Ready to Upload</span>
              <strong>{fileName || "코디 이미지 업로드"}</strong>
              <p>클릭하거나 이미지를 끌어다 놓아 주세요. 분석이 끝나면 바로 추천 화면으로 이어집니다.</p>
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
              <div className="upload-stage-unified-copy">
                <strong>{fileName || "스타일 기준이 될 이미지를 선택하세요"}</strong>
                <span>{isDragActive ? "여기에 이미지를 놓아주세요" : "PNG, JPG, JPEG, WEBP 파일을 바로 업로드할 수 있습니다."}</span>
                <small>추천은 현재 업로드한 이미지 한 장만 기준으로 생성됩니다.</small>
              </div>
              {filePreviewUrl ? (
                <div className="upload-stage-square">
                  <img src={filePreviewUrl} alt={`선택한 이미지 미리보기: ${fileName}`} className="upload-stage-image" />
                </div>
              ) : (
                <div className="upload-stage-placeholder upload-stage-placeholder-rich" aria-hidden="true">
                  <span>Preview</span>
                  <small>Curated visual anchor</small>
                </div>
              )}
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
            </div>
            <input ref={fileInputRef} id="image-input" type="file" accept="image/*" onChange={handleFileChange} />
            <div className="upload-primary-row">
              <button
                type="button"
                className="upload-primary-button"
                onClick={handleUpload}
                disabled={uploading || !selectedFile}
                aria-busy={uploading}
              >
                {uploading ? "이미지 분석 중..." : "이미지 분석하기"}
              </button>
            </div>
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
          </div>
        </div>
      </article>

      <div className="upload-support-grid">
        <section className="support-panel support-panel-luxe">
          <div className="support-panel-header">
            <p className="eyebrow">Detected Focus</p>
            <h2>추천이 집중해서 읽는 포인트</h2>
          </div>
          {analysis ? (
            <>
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
            </>
          ) : (
            <>
              <ul className="bullet-data-list">
                {STUDIO_SIGNALS.map((signal) => (
                  <li key={signal}>{signal}</li>
                ))}
              </ul>
            </>
          )}
        </section>

        <section className="support-panel support-panel-luxe">
          <div className="support-panel-header">
            <p className="eyebrow">Search Hints</p>
            <h2>생성될 검색 힌트의 분위기</h2>
          </div>
          {Object.keys(analysisQueryHints).length > 0 ? (
            <div className="keyword-chip-row">
              {Object.entries(analysisQueryHints).map(([category, hint]) => (
                <span key={`${category}-${hint}`} className="keyword-chip">
                  {getCategoryLabel(category)} · {hint}
                </span>
              ))}
            </div>
          ) : (
            <div className="keyword-chip-row">
              {DEFAULT_CURATION_HINTS.map((hint) => (
                <span key={hint} className="keyword-chip">
                  {hint}
                </span>
              ))}
            </div>
          )}
          {analysis ? <p className="hint-text">분석 코드: {analysis.checksum}</p> : <p className="hint-text">업로드 후 카테고리별 검색어가 여기에 채워집니다.</p>}
        </section>
      </div>
    </section>
  );
}
