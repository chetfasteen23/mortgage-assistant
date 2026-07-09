import { useState } from "react";
import { api } from "../src/api/client";

type LoginFormProps = {
  onLoginSuccess: () => void;
};

export function LoginForm({ onLoginSuccess }: LoginFormProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");

  async function handleLogin(event: React.FormEvent) {
    event.preventDefault();

    try {
      const response = await api.post("/auth/login", {
        email,
        password,
      });

      localStorage.setItem(
        "access_token",
        response.data.access_token
      );

      onLoginSuccess();
    } catch {
      setMessage("Invalid email or password.");
    }
  }

  return (
    <form onSubmit={handleLogin}>

      <input
        type="email"
        value={email}
        onChange={(event) => setEmail(event.target.value)}
        placeholder="Email"
        required
      />

      <input
        type="password"
        value={password}
        onChange={(event) => setPassword(event.target.value)}
        placeholder="Password"
        required
      />

      <button type="submit">
        Sign In
      </button>

      {message && <p>{message}</p>}
    </form>
  );
}