export default function LoginPage() {
  return (
    <section className="card card-auth">
      <p className="eyebrow">Private Access</p>
      <h1>Login to StyleMatch</h1>
      <p className="lead">개인 테스트 계정으로 로그인해 업로드와 추천 기능을 확인하세요.</p>
      <form className="form-grid">
        <label>
          Email
          <input type="email" placeholder="admin@stylematch.com" />
        </label>
        <label>
          Password
          <input type="password" placeholder="••••••••" />
        </label>
        <button type="button">Sign In</button>
      </form>
    </section>
  );
}
