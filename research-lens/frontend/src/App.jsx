
import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

export default function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function askQuestion(e) {
    e.preventDefault();

    const trimmed = question.trim();
    if (!trimmed || loading) return;

    setMessages((previous) => [
      ...previous,
      { role: "user", content: trimmed },
    ]);
    setQuestion("");
    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API_URL}/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: trimmed }),
      });

      if (!response.ok) {
        throw new Error(`Request failed (${response.status})`);
      }

      const data = await response.json();

      setMessages((previous) => [
        ...previous,
        { role: "assistant", content: data.answer },
      ]);
    } catch (err) {
      setError(
        "Couldn't connect to ResearchLens. Check that the backend is running."
      );
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <div className="brand-mark">R</div>
        <div>
          <h1>ResearchLens</h1>
          <p>Research papers, understood.</p>
        </div>
        <span className="status">● RAG enabled</span>
      </header>

      <section className="workspace">
        <div className="intro">
          <span className="eyebrow">YOUR RESEARCH ASSISTANT</span>
          <h2>Ask better questions.<br />Find meaningful insights.</h2>
          <p>
            Ask questions about your indexed research papers and get
            evidence-based answers.
          </p>
        </div>

        <div className="chat-panel">
          <div className="chat-heading">
            <div>
              <h3>Research chat</h3>
              <p>Powered by LangChain, FAISS and Groq</p>
            </div>
            <span className="live-dot">Ready</span>
          </div>

          <div className="messages">
            {messages.length === 0 && (
              <div className="empty-state">
                <div className="sparkle">✳</div>
                <h3>What would you like to explore?</h3>
                <p>Try asking a question about your research collection.</p>

                <button
                  className="suggestion"
                  onClick={() =>
                    setQuestion(
                      "What methods are used to study beta-thalassemia?"
                    )
                  }
                >
                  What methods are used to study beta-thalassemia? ↗
                </button>

                <button
                  className="suggestion"
                  onClick={() =>
                    setQuestion(
                      "What deep learning methods are discussed for COVID-19 detection?"
                    )
                  }
                >
                  What deep learning methods are discussed for COVID-19 detection? ↗
                </button>
              </div>
            )}

            {messages.map((message, index) => (
              <div
                className={`message ${message.role}`}
                key={`${message.role}-${index}`}
              >
                <span className="message-label">
                  {message.role === "user" ? "YOU" : "RESEARCHLENS"}
                </span>
                <p>{message.content}</p>
              </div>
            ))}

            {loading && (
              <div className="message assistant">
                <span className="message-label">RESEARCHLENS</span>
                <p>Reading the evidence and preparing an answer…</p>
              </div>
            )}

            <div aria-live="polite" className="error-message">
              {error}
            </div>
          </div>

          <form className="question-form" onSubmit={askQuestion}>
            <input
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask something about your papers..."
              aria-label="Your research question"
            />
            <button type="submit" disabled={loading || !question.trim()}>
              {loading ? "Thinking…" : "Ask ↗"}
            </button>
          </form>
          <p className="privacy-note">
            Answers depend on the papers indexed in your collection.
            Verify important findings against the original sources.
          </p>
        </div>
      </section>

      <footer>ResearchLens · Built for curious minds</footer>
    </main>
  );
}
