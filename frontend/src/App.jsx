import { useState } from "react";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const verifyNews = async () => {
    if (!text.trim()) {
      setError("Please enter some text to verify.");
      return;
    }

    setError("");
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

      if (!response.ok) {
        throw new Error("Server error");
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError("Could not connect to backend. Make sure the server is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <div className="card">
        <h1>LucidVerify</h1>
        <p className="tagline">Verify news. Instantly.</p>

        <textarea
          placeholder="Paste a news headline or paragraph here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <button onClick={verifyNews} disabled={loading}>
          {loading ? "Verifying..." : "Verify News"}
        </button>

        {error && <p style={{ color: "#f87171", marginTop: "16px" }}>{error}</p>}

        {result && (
          <div className={`result ${result.label}`}>
            <h3>{result.label.toUpperCase()}</h3>
            <p>
              <strong>Confidence:</strong>{" "}
              {(result.confidence * 100).toFixed(0)}%
            </p>
            <p>
              <strong>Source:</strong> {result.source}
            </p>

            {result.keywords && result.keywords.length > 0 && (
              <p>
                <strong>Key indicators:</strong>{" "}
                {result.keywords.join(", ")}
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
