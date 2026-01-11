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
          placeholder="Enter a news claim or statement..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <button onClick={verifyNews} disabled={loading}>
          {loading ? "Verifying..." : "Verify"}
        </button>

        {error && <p className="error">{error}</p>}

        {result && (
          <div className="result">
            <p><strong>Label:</strong> {result.label}</p>
            <p><strong>Confidence:</strong> {result.confidence}</p>
            <p><strong>Source:</strong> {result.source}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
