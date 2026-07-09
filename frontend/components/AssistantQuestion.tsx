import { useState } from "react";
import { api } from "../src/api/client";

type Source = {
  sheet_name: string;
  chunk_text: string;
};

type ChatMessage = {
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
};

export function AssistantQuestion() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  async function handleAsk(event: React.FormEvent) {
    event.preventDefault();

    if (!question.trim()) {
      return;
    }

    const userMessage: ChatMessage = {
      role: "user",
      content: question,
    };

    setMessages((current) => [...current, userMessage]);
    setQuestion("");
    setIsLoading(true);

    try {
      const response = await api.post("/assistant/ask", {
        question,
      });

      const assistantMessage: ChatMessage = {
        role: "assistant",
        content: response.data.answer,
        sources: response.data.sources,
      };

      setMessages((current) => [...current, assistantMessage]);
    } catch {
      const errorMessage: ChatMessage = {
        role: "assistant",
        content: "Sorry, I could not get a response. Please try again.",
      };

      setMessages((current) => [...current, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <section className="chat-section">
      <div className="chat-header">
        <h2>Ask a guideline question</h2>
        <p>
          Ask about lender guidelines using the uploaded Excel sheet as context.
        </p>
      </div>

      <div className="chat-window">
        {messages.length === 0 && (
          <div className="empty-chat">
            <p>Try asking:</p>
            <strong>Which lenders allow FHA with a 620 credit score?</strong>
          </div>
        )}

        {messages.map((message, index) => (
          <div
            key={index}
            className={`chat-message ${
              message.role === "user" ? "user-message" : "assistant-message"
            }`}
          >
            <div className="message-bubble">
              <p>{message.content}</p>

              {message.sources && message.sources.length > 0 && (
                <details className="sources-details">
                  <summary>View sources</summary>

                  {message.sources.map((source, sourceIndex) => (
                    <div key={sourceIndex} className="source-card">
                      <strong>{source.sheet_name}</strong>
                      <pre>{source.chunk_text}</pre>
                    </div>
                  ))}
                </details>
              )}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="chat-message assistant-message">
            <div className="message-bubble">
              <p>Thinking...</p>
            </div>
          </div>
        )}
      </div>

      <form onSubmit={handleAsk} className="chat-input-row">
        <textarea
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="Ask a borrower scenario or lender guideline question..."
          required
        />

        <button type="submit" disabled={isLoading}>
          Send
        </button>
      </form>
    </section>
  );
}