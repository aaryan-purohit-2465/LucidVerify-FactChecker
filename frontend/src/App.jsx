import { useState } from "react";
import "./index.css";

export default function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const API_URL = "https://lucidverify-backend.onrender.com/predict"; 
  // Replace with your real backend URL if different

  const verifyClaim = async () => {
    if (!text.trim()) return;

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
      });

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError("Backend not reachable.");
    }

    setLoading(false);
  };

  return (
    <>
      <div className="app-bg"></div>

      <div className="card">
        <div className="title">Lucid Verify</div>
        <div className="subtitle">AI-powered Fact Checker</div>

        <textarea
          placeholder="Paste a news headline, tweet or claim..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <button onClick={verifyClaim} disabled={loading}>
          {loading ? "Verifying..." : "Verify"}
        </button>

        {loading && <div className="loading">Analyzing claim...</div>}

        {error && <div className="loading" style={{ color: "#f87171" }}>{error}</div>}

        {result && (
          <div className="result">
            <div className={`badge ${result.label === "real" ? "real" : "fake"}`}>
              {result.label.toUpperCase()}
            </div>
            <p><b>Confidence:</b> {(result.confidence * 100).toFixed(1)}%</p>
            <p><b>Source:</b> {result.source}</p>
          </div>
        )}

        <div className="footer">
          Built with FastAPI & React — LucidVerify © 2026
        </div>
      </div>
    </>
  );
}
