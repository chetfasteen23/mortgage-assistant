import { useState } from "react";

import { AssistantQuestion } from "../components/AssistantQuestion";
import { LoginForm } from "../components/LoginForm";
import { UploadLenderSheet } from "../components/UploadLenderSheet";
import "./App.css";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(
    Boolean(localStorage.getItem("access_token"))
  );

  function handleLoginSuccess() {
    setIsAuthenticated(true);
  }

  function handleLogout() {
    localStorage.removeItem("access_token");
    setIsAuthenticated(false);
  }

  if (!isAuthenticated) {
    return (
      <main className="page auth-page">
        <section className="auth-card">
          <div className="brand-pill">Mortgage Assistant</div>
          <h1>Sign in to your workspace</h1>
          <p className="subtitle">
            Upload lender guidelines, ask borrower scenario questions, and review AI-assisted matches.
          </p>

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

      <section className="dashboard-grid">
        <div className="panel">
          <AssistantQuestion />
        </div>
        
        <div className="panel">
          <UploadLenderSheet />
        </div>
      </section>
    </main>
  );
}

export default App;