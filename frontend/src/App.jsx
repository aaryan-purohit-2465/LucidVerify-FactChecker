import { useState } from "react";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const checkNews = async () => {
    if (!text.trim()) return;

    setLoading(true);
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
      console.error(err);
      alert("Backend not reachable");
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: "2rem", maxWidth: "600px", margin: "auto" }}>
      <h1>LucidVerify</h1>
      <p>Fake News Fact Checker</p>

      <textarea
        rows="6"
        style={{ width: "100%", padding: "10px" }}
        placeholder="Paste news text here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <br /><br />

      <button onClick={checkNews} disabled={loading}>
        {loading ? "Checking..." : "Check"}
      </button>

      {result && (
        <div style={{ marginTop: "1.5rem" }}>
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
