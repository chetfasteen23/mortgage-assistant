import { useState } from "react";

import { LoginForm } from "../components/LoginForm";
import { UploadLenderSheet } from "../components/UploadLenderSheet";
import { AssistantQuestion } from "../components/AssistantQuestion";


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
      <main>
        <h1>Mortgage Assistant</h1>

        <LoginForm
          onLoginSuccess={handleLoginSuccess}
        />
      </main>
    );
  }

  return (
    <main>
      <header>
        <h1>Mortgage Assistant</h1>

        <button onClick={handleLogout}>
          Logout
        </button>
      </header>

      <section>
        <h2>Dashboard</h2>

        <UploadLenderSheet />
        <AssistantQuestion />
      </section>
    </main>
  );
}


export default App;