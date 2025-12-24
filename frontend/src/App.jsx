import { useState } from "react";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const checkFact = async () => {
    if (!text.trim()) {
      setError("Please enter some text");
      return;
    }

    setLoading(true);
    setError("");
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
    } catch (err) {
      setError("Failed to connect to backend");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>LucidVerify</h1>
      <p className="subtitle">Fact Checker</p>

      <textarea
        placeholder="Enter a news statement..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button onClick={checkFact} disabled={loading}>
        {loading ? "Checking..." : "Check"}
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
  );
}

export default App;
