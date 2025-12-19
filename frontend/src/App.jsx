import "./App.css";
import { useState } from "react";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const checkFact = async () => {
    if (!text.trim()) return;

    setLoading(true);
    setResult(null);

    try {
      const res = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text }),
      });

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setResult({ error: "Backend not reachable" });
    }

    setLoading(false);
  };

  return (
    <div className="container">
      <h1>LucidVerify</h1>
      <p className="subtitle">AI-powered Fact Checker</p>

      <textarea
        placeholder="Enter a claim or news statement..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button onClick={checkFact}>
        {loading ? "Checking..." : "Check"}
      </button>

      {result && (
        <div className="result">
          {result.error ? (
            <p className="error">{result.error}</p>
          ) : (
            <>
              <p><b>Label:</b> {result.label}</p>
              <p><b>Confidence:</b> {result.confidence}</p>
              <p><b>Source:</b> {result.source}</p>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
