import { useState } from "react";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const verifyNews = async () => {
    if (!text.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const res = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });
      const data = await res.json();
      setResult(data);
    } catch {
      setResult({ label: "error", confidence: 0, source: "backend error" });
    }

    setLoading(false);
  };

  return (
    <div className="page">
      <div className="card">
        <h1>LucidVerify</h1>
        <p className="tagline">Verify news. Instantly.</p>

        <textarea
          placeholder="Paste a news headline or paragraph here…"
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <button onClick={verifyNews} disabled={loading}>
          {loading ? "Verifying…" : "Verify News"}
        </button>

        {result && (
          <div className={`result ${result.label}`}>
            <h3>{result.label.toUpperCase()}</h3>
            <p>{(result.confidence * 100).toFixed(0)}% confidence</p>
            <span>{result.source}</span>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
