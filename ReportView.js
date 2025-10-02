import React from "react";
import axios from "axios";

function ReportView({ runId, setReport }) {
  const fetchReport = async () => {
    const res = await axios.get(`http://localhost:8000/report/${runId}`);
    setReport(res.data);
  };

  return (
    <div className="card">
      <h3>Generate Report</h3>
      <button onClick={fetchReport}>Fetch Report</button>
    </div>
  );
}

export default ReportView;
