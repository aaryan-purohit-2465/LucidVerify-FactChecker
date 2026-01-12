import { useState } from "react";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL;

export default function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const verify = async () => {
    if (!text.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const res = await fetch(`${API_URL}/predict`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      const data = await res.json();
      setResult(data);
    } catch (err) {
      alert("Backend not reachable");
    }

    setLoading(false);
  };

  return (
    <div className="app">
      <div className="card">
        <h1 className="logo">LucidVerify</h1>
        <p className="tagline">AI-powered Fact Checker</p>

        <textarea
          className="input"
          placeholder="Paste a news headline, tweet or claim..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <button className="btn" onClick={verify} disabled={loading}>
          {loading ? "Verifying..." : "Verify Now"}
        </button>

        {result && (
          <div className="result">
            <div className={`badge ${result.label}`}>
              {result.label.toUpperCase()}
            </div>

            <div className="progress">
              <div
                className="fill"
                style={{ width: `${result.confidence * 100}%` }}
              ></div>
            </div>

            <p className="confidence">
              Confidence: {(result.confidence * 100).toFixed(0)}%
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
