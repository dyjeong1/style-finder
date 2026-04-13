export default function UploadPage() {
  return (
    <section className="split-grid">
      <article className="card upload-dropzone">
        <p className="eyebrow">Step 1</p>
        <h1>Upload Outfit Image</h1>
        <p className="lead">코디 이미지를 올리면 카테고리별 추천 결과를 생성합니다.</p>
        <div className="dropzone">Drop image here or click to browse</div>
        <button type="button">Upload & Analyze</button>
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
