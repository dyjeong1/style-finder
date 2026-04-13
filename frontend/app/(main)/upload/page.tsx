"use client";

import { ChangeEvent, useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

import { getStoredToken, setStoredUploadedImageId, uploadImage } from "@/lib/api";

export default function UploadPage() {
  const router = useRouter();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [filePreviewUrl, setFilePreviewUrl] = useState("");

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
    <section className="split-grid">
      <article className="card upload-dropzone">
        <p className="eyebrow">Step 1</p>
        <h1>Upload Outfit Image</h1>
        <p className="lead">코디 이미지를 올리면 카테고리별 추천 결과를 생성합니다.</p>
        <label className="dropzone" htmlFor="image-input">
          {fileName || "Drop image here or click to browse"}
        </label>
        <input id="image-input" type="file" accept="image/*" onChange={handleFileChange} />
        <button type="button" onClick={handleUpload} disabled={uploading}>
          {uploading ? "Uploading..." : "Upload & Analyze"}
        </button>
        {filePreviewUrl ? (
          <div className="preview-wrap">
            <img src={filePreviewUrl} alt="selected preview" className="preview-image" />
          </div>
        ) : null}
        {errorMessage ? <p className="error-text">{errorMessage}</p> : null}
        {successMessage ? <p className="success-text">{successMessage}</p> : null}
        <p className="hint-text">
          로그인을 아직 하지 않았다면 <Link href="/login">로그인 페이지</Link>에서 먼저 인증하세요.
        </p>
      </article>
      <article className="card">
        <p className="eyebrow">Recent</p>
        <h2>최근 업로드</h2>
        <ul className="simple-list">
          <li>street-look-0413.png</li>
          <li>spring-office-fit.jpg</li>
          <li>weekend-casual.webp</li>
        </ul>
      </article>
    </section>
  );
}
