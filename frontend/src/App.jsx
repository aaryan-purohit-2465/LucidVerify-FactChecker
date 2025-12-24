import { useState } from "react";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const checkNews = async () => {
    if (!text.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      setResult({ label: "error", confidence: 0 });
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <h1>LucidVerify</h1>
      <p>AI-powered Fact Checker</p>

      <textarea
        placeholder="Paste news text here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button onClick={checkNews} disabled={loading}>
        {loading ? "Checking..." : "Check"}
      </button>

      {result && (
        <div className="result">
          <h3>Result</h3>
          <p>
            <strong>Label:</strong> {result.label}
          </p>
          <p>
            <strong>Confidence:</strong>{" "}
            {(result.confidence * 100).toFixed(2)}%
          </p>
          <p>
            <strong>Source:</strong> {result.source}
          </p>
        </div>
      )}
    </div>
  );
}

export default App;
