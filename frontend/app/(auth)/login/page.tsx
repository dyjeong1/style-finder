"use client";

import { FormEvent, useState } from "react";
import { useRouter } from "next/navigation";

import { login, setStoredToken } from "@/lib/api";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("admin@stylematch.com");
  const [password, setPassword] = useState("stylematch1234");
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setErrorMessage(null);

    try {
      const result = await login(email, password);
      setStoredToken(result.access_token);
      router.push("/upload");
    } catch (error) {
      const message = error instanceof Error ? error.message : "로그인 중 오류가 발생했습니다.";
      setErrorMessage(message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="card card-auth">
      <p className="eyebrow">Private Access</p>
      <h1>Login to StyleMatch</h1>
      <p className="lead">개인 테스트 계정으로 로그인해 업로드와 추천 기능을 확인하세요.</p>
      <p className="hint-text">기본 계정: admin@stylematch.com / stylematch1234</p>
      <form className="form-grid" onSubmit={handleSubmit}>
        <label>
          Email
          <input type="email" value={email} placeholder="admin@stylematch.com" onChange={(event) => setEmail(event.target.value)} />
        </label>
        <label>
          Password
          <input
            type="password"
            value={password}
            placeholder="••••••••"
            onChange={(event) => setPassword(event.target.value)}
          />
        </label>
        <button type="submit" disabled={loading}>
          {loading ? "Signing In..." : "Sign In"}
        </button>
        {errorMessage ? <p className="error-text">{errorMessage}</p> : null}
      </form>
    </section>
  );
}
