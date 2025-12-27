function ResultCard({ result }) {
  const isReal = result.label === "real";

  return (
    <div className={`result-card ${isReal ? "real" : "fake"}`}>
      <h2>{isReal ? "Likely Real ✅" : "Possibly Fake ⚠️"}</h2>

      <p className="confidence">
        Confidence: {(result.confidence * 100).toFixed(1)}%
      </p>

      <p className="source">
        Source: <strong>{result.source}</strong>
      </p>
    </div>
  );
}

export default ResultCard;
