import { useState } from "react";
import "./App.css";

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
      alert("Backend not reachable");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>LucidVerify</h1>
      <p className="subtitle">Fact Checker</p>

      <textarea
        placeholder="Paste a news statement here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button onClick={checkFact} disabled={loading}>
        {loading ? "Checking..." : "Check"}
      </button>

      {result && (
        <div className={`result ${result.label}`}>
          <h3>Result: {result.label.toUpperCase()}</h3>
          <p>Confidence: {(result.confidence * 100).toFixed(1)}%</p>
          <p>Source: {result.source}</p>
        </div>
      )}
    </div>
  );
}

export default App;
