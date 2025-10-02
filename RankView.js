import React from "react";
import axios from "axios";

const API_URL = "http://localhost:8000";

function RankView({ plannedTests, setRankedTests }) {
  const handleRank = async () => {
    if (!plannedTests || plannedTests.length === 0) {
      alert("⚠️ No planned tests to rank.");
      return;
    }

    try {
      console.log("Sending planned tests:", plannedTests);

      const res = await axios.post(
        `${API_URL}/rank`,
        { test_cases: plannedTests, top_k: 10 }, // JSON body
        { headers: { "Content-Type": "application/json" } }
      );

      setRankedTests(res.data.ranked_test_cases);
    } catch (err) {
      console.error("Ranking failed:", err);
      alert("❌ Ranking failed. Check backend is running.");
    }
  };

  return (
    <div className="card">
      <h3>Rank Test Cases</h3>
      <button onClick={handleRank}>Rank Top Tests</button>
    </div>
  );
}

export default RankView;
