import React, { useState } from "react";
import axios from "axios";

const API_URL = "http://localhost:8000";

function UploadUrl() {
  const [url, setUrl] = useState("");
  const [message, setMessage] = useState("");
  const [uploading, setUploading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!url) return;

    setUploading(true);
    setMessage("⏳ Starting URL ingestion...");

    try {
      const formData = new FormData();
      formData.append("url", url);

      const res = await axios.post(`${API_URL}/ingest_url`, formData);
      setMessage(res?.data?.message || "✅ URL uploaded started.");
      setUrl("");
    } catch (err) {
      console.error(err);
      setMessage("❌ Failed to ingest URL.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="card">
      <h3>Upload Reference URL</h3>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter game URL"
          required
        />
        <button type="submit" disabled={uploading}>
          {uploading ? "Uploading..." : "Upload & Ingest"}
        </button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
}

export default UploadUrl;
