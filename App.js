import React, { useState } from "react";
import PlanForm from "./components/PlanForm";
import RankView from "./components/RankView";
import ExecuteView from "./components/ExecuteView";
import ReportView from "./components/ReportView";
import UploadDoc from "./components/UploadDoc";
import UploadUrl from "./components/UploadUrl";   // ✅ New component

function App() {
  const [plannedTests, setPlannedTests] = useState([]);
  const [rankedTests, setRankedTests] = useState([]);
  const [runId, setRunId] = useState("");
  const [results, setResults] = useState([]);
  const [report, setReport] = useState(null);

  return (
    <div className="container">
      <h1>Multi-Agent Game Tester</h1>

      {/* ✅ PDF Upload */}
      <UploadDoc />

      {/* ✅ URL Upload */}
      <UploadUrl />

      {/* ✅ Test Flow */}
      <PlanForm setPlannedTests={setPlannedTests} />
      {plannedTests.length > 0 && (
        <RankView plannedTests={plannedTests} setRankedTests={setRankedTests} />
      )}
      {rankedTests.length > 0 && (
        <ExecuteView
          rankedTests={rankedTests}
          setRunId={setRunId}
          setResults={setResults}
        />
      )}
      {results.length > 0 && <ReportView runId={runId} setReport={setReport} />}

      {report && (
        <div className="card">
          <h3>Report</h3>
          <pre>{JSON.stringify(report, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
