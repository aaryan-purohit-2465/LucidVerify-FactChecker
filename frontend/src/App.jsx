import { useState } from "react";
import ResultCard from "./components/ResultCard";
import "./index.css";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleCheck = async () => {
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
      setResult({
        label: "error",
        confidence: 0,
        source: "error",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="card">
        <h1 className="title">LucidVerify</h1>
        <p className="subtitle">
          Fact-checking news using intelligent analysis
        </p>

        <textarea
          className="input-box"
          placeholder="Paste news or statement here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <button className="check-btn" onClick={handleCheck} disabled={loading}>
          {loading ? "Checking..." : "Verify"}
        </button>

        {result && <ResultCard result={result} />}
      </div>
    </div>
  );
}

export default App;
