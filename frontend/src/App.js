import { useState } from "react";
import "./App.css";

const App = () => {
  const [inputText, setInputText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const processText = async () => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch("http://127.0.0.1:5000/process", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: inputText }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to process text");
      }

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="card">
        <h1 className="card-title">BERT Text Processing Workshop</h1>

        <div className="input-area">
          <textarea
            className="textarea"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Enter text to process..."
          />
        </div>

        <button
          className="button"
          onClick={processText}
          disabled={loading || !inputText.trim()}
        >
          {loading ? "Processing..." : "Process Text"}
        </button>

        {error && <div className="error">Error: {error}</div>}

        {result && (
          <div className="results">
            <h3 className="results-title">Results:</h3>
            <div className="results-content">
              {JSON.stringify(result, null, 2)}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
