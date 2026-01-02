import { useState } from "react";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);

  const checkFact = async () => {
    const res = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await res.json();
    setResult(data);
  };

  return (
    <div style={{ padding: "40px", fontFamily: "Arial" }}>
      <h1>LucidVerify – Fact Checker</h1>

      <textarea
        rows="5"
        style={{ width: "100%", marginBottom: "10px" }}
        placeholder="Enter a news statement..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <br />
      <button onClick={checkFact}>Check</button>

      {result && (
        <div style={{ marginTop: "20px" }}>
          <p><b>Label:</b> {result.label}</p>
          <p><b>Confidence:</b> {result.confidence}</p>
          <p><b>Source:</b> {result.source}</p>
        </div>
      )}
    </div>
  );
}

export default App;
