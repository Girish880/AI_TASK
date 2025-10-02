import React, { useState } from "react";
import axios from "axios";

const API_URL = "http://localhost:8000";

function UploadDoc() {
  const [file, setFile] = useState(null);
  const [message, setMessage] = useState("");
  const [uploading, setUploading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      setMessage("⚠️ Please select a file first!");
      return;
    }

    setUploading(true);
    setMessage("⏳ Uploading...");

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await axios.post(`${API_URL}/upload_doc`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });

      // Safely access res.data.message or fallback
      const msg = res?.data?.message || "Upload completed successfully!";
      setMessage(`✅ ${msg}`);
    } catch (err) {
      console.error("Upload error:", err);
      if (err.response?.data?.error) {
        setMessage(`❌ Upload failed: ${err.response.data.error}`);
      } else if (err.response?.data?.message) {
        setMessage(`❌ Upload failed: ${err.response.data.message}`);
      } else {
        setMessage("❌ Upload failed. Check if backend is running on port 8000.");
      }
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="card">
      <h3>Upload Reference Document</h3>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload} disabled={uploading}>
        {uploading ? "Uploading..." : "Upload & Ingest"}
      </button>
      {message && <p>{message}</p>}
    </div>
  );
}

export default UploadDoc;
