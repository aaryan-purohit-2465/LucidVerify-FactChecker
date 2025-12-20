import { useState } from "react";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);

  const checkNews = async () => {
    const res = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });

    const data = await res.json();
    setResult(data);
  };

  return (
    <div style={{ padding: "40px", fontFamily: "sans-serif" }}>
      <h1>LucidVerify</h1>

      <textarea
        rows="5"
        style={{ width: "100%" }}
        placeholder="Paste news text here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <br /><br />

      <button onClick={checkNews}>Check</button>

      {result && (
        <div style={{ marginTop: "20px" }}>
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
