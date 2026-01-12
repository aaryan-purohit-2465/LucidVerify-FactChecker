import { useState } from "react";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL;

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const verifyNews = async () => {
    if (!text.trim()) return;

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(`${API_URL}/predict`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ text })
      });

      if (!response.ok) {
        throw new Error("Backend not reachable");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError("Backend not reachable. Please try again later.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="card">
        <h1>LucidVerify — Fact Checker</h1>
        <p className="subtitle">AI-powered Fake News Detection</p>

        <textarea
          placeholder="Paste a news headline, tweet, or claim to verify..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <button onClick={verifyNews} disabled={loading}>
          {loading ? "Verifying..." : "Verify"}
        </button>

        {error && <p className="error">{error}</p>}

        {result && (
          <div className={`result ${result.label}`}>
            <h3>Prediction Result</h3>

            <p className="label">
              {result.label === "real" ? "✅ REAL NEWS" : "❌ FAKE NEWS"}
            </p>

            <div className="confidence-bar">
              <div
                className="confidence-fill"
                style={{ width: `${result.confidence * 100}%` }}
              ></div>
            </div>

            <p className="confidence-text">
              Confidence: {(result.confidence * 100).toFixed(0)}%
            </p>

            <p className="source">Source: {result.source}</p>
          </div>
        )}

        <p className="footer">
          Built with FastAPI & React — LucidVerify © 2025
        </p>
      </div>
    </div>
  );
}

export default App;
