import React, { useState } from "react";
import axios from "axios";

const API_URL = "http://localhost:8000";

function ExecuteView({ rankedTests, setRunId, setResults }) {
  const [loading, setLoading] = useState(false);

  const handleExecute = async () => {
    if (!rankedTests || rankedTests.length === 0) {
      alert("⚠️ No test cases to execute.");
      return;
    }

    setLoading(true);

    try {
      const res = await axios.post(
        `${API_URL}/execute`,
        { test_cases: rankedTests },
        { headers: { "Content-Type": "application/json" } }
      );

      setRunId(res.data.run_id);
      setResults(res.data.results);
    } catch (err) {
      console.error("Execution failed:", err);
      alert("❌ Test execution failed. Check if backend is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card">
      <h3>Execute Test Cases</h3>
      <button onClick={handleExecute} disabled={loading}>
        {loading ? "Running Tests..." : "Run Tests"}
      </button>
    </div>
  );
}

export default ExecuteView;
