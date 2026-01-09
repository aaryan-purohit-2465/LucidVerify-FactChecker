import { useState } from "react";
import "./App.css";
import { verifyNews as verifyNewsAPI } from "./services/api";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const verifyNews = async () => {
    if (!text.trim()) {
      setError("Please enter some news text.");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      const data = await verifyNewsAPI(text);
      setResult(data);
    } catch (err) {
      setError("Backend not reachable.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <h1>LucidVerify — Fact Checker</h1>

      <textarea
        placeholder="Paste news text here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button onClick={verifyNews} disabled={loading}>
        {loading ? "Checking..." : "Verify"}
      </button>

      {error && <p className="error">{error}</p>}

      {result && (
        <div className="result">
          <h3>Result</h3>
          <p><b>Label:</b> {result.label}</p>
          <p><b>Confidence:</b> {result.confidence}</p>
          <p><b>Source:</b> {result.source}</p>
        </div>
      )}
    </div>
  );
}

export default App;
