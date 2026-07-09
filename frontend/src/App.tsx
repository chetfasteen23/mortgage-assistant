import { useEffect, useState } from "react";

import { AssistantQuestion } from "../components/AssistantQuestion";
import { LoginForm } from "../components/LoginForm";
import { UploadLenderSheet } from "../components/UploadLenderSheet";
import { api } from "./api/client";
import { LenderFileStatus } from "../components/LenderFileStatus"
import "./App.css";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(
    Boolean(localStorage.getItem("access_token"))
  );

  const [isCheckingAuth, setIsCheckingAuth] = useState(true);
  const [fileRefreshKey, setFileRefreshKey] = useState(0);
  const [isUploadOpen, setIsUploadOpen] = useState(false);

  function refreshLenderFileStatus() {
    setFileRefreshKey((current) => current + 1);
  }

  function handleLoginSuccess() {
    setIsAuthenticated(true);
  }

  function handleLogout() {
    localStorage.removeItem("access_token");
    setIsAuthenticated(false);
  }

  useEffect(() => {
  async function checkAuth() {
    const token = localStorage.getItem("access_token");

    if (!token) {
      setIsAuthenticated(false);
      setIsCheckingAuth(false);
      return;
    }

    try {
      await api.get("/users/me");
      setIsAuthenticated(true);
    } catch {
      localStorage.removeItem("access_token");
      setIsAuthenticated(false);
    } finally {
      setIsCheckingAuth(false);
    }
  }

  checkAuth();
}, []);

  if (isCheckingAuth) {
    return (
      <main className="page auth-page">
        <section className="auth-card">
          <h1>Loading...</h1>
        </section>
      </main>
    );
  }

  if (!isAuthenticated) {
    return (
      <main className="page auth-page">
        <section className="auth-card">
          <h1 color="black">Sign in to your workspace</h1>
          <div style={{padding: "20px"}}></div>

          <LoginForm onLoginSuccess={handleLoginSuccess} />
        </section>
      </main>
    );
  }

  return (
    <main className="page dashboard-page">
      <header className="dashboard-header">
        <div>
          <div className="brand-pill">Mortgage Assistant</div>
          <h1>Lender Intelligence Dashboard</h1>
          <p className="subtitle">
            Manage your lender sheet and ask guideline questions with sourced answers.
          </p>
        </div>

        <button className="secondary-button" onClick={handleLogout}>
          Logout
        </button>
      </header>

      <section className="dashboard-stack">
        <div className="chat-panel">
          <AssistantQuestion />
        </div>

        <div className="sheet-management-card">
  <div className="sheet-card-header">
    <LenderFileStatus refreshKey={fileRefreshKey} />

    <button
      className="secondary-button"
      onClick={() => setIsUploadOpen((current) => !current)}
    >
      {isUploadOpen ? "Hide upload" : "Manage lender sheet"}
    </button>
  </div>

  {isUploadOpen && (
    <div className="collapsible-upload">
      <UploadLenderSheet onUploadSuccess={refreshLenderFileStatus} />
    </div>
  )}
</div>
      </section>
    </main>
  );
}

export default App;