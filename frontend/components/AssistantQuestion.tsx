import { useState } from "react";
import { api } from "../src/api/client";

type Source = {
  sheet_name: string;
  chunk_text: string;
};

export function AssistantQuestion() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState<Source[]>([]);
  const [message, setMessage] = useState("");

  async function handleAsk(event: React.FormEvent) {
    event.preventDefault();

    try {
      setMessage("Thinking...");
      const response = await api.post("/assistant/ask", {
        question,
      });

      setAnswer(response.data.answer);
      setSources(response.data.sources);
      setMessage("");
    } catch {
      setMessage("Failed to get assistant response.");
    }
  }

  return (
    <section>
      <h2>Ask Assistant</h2>

      <form onSubmit={handleAsk}>
        <textarea
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="Example: Which lenders allow FHA with a 620 credit score?"
          required
        />

        <button type="submit">Ask</button>
      </form>

      {message && <p>{message}</p>}

      {answer && (
        <div>
          <h3>Answer</h3>
          <p>{answer}</p>
        </div>
      )}

      {sources.length > 0 && (
        <div>
          <h3>Sources</h3>

          {sources.map((source, index) => (
            <div key={index}>
              <strong>{source.sheet_name}</strong>
              <pre>{source.chunk_text}</pre>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}