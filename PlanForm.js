import React, { useState } from "react";
import axios from "axios";

function PlanForm({ setPlannedTests }) {
  const [desc, setDesc] = useState("");

  const handlePlan = async () => {
    const res = await axios.post("http://localhost:8000/plan", null, { params: { description: desc } });
    setPlannedTests(res.data.test_cases);
  };

  return (
    <div className="card">
      <h3>Plan Test Cases</h3>
      <textarea placeholder="Describe the game or scenario..." value={desc} onChange={(e) => setDesc(e.target.value)} />
      <button onClick={handlePlan}>Generate Test Cases</button>
    </div>
  );
}

export default PlanForm;
