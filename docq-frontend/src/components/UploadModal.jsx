import { useRef, useState } from "react";
 "react";
import { supabase } from "../services/supabaseClient";
import "../styles/UploadModal.css";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function UploadModal({ onClose, onSuccess }) {
  const [file, setFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState("idle"); // idle | uploading | done | error
  const [errorMsg, setErrorMsg] = useState("");
  const fileInputRef = useRef(null);

  /* ── File selection ── */
  const acceptFile = (f) => {
    if (!f) return;
    if (f.type !== "application/pdf") {
      setErrorMsg("Only PDF files are supported.");
      return;
    }
    if (f.size > 100 * 1024 * 1024) {
      setErrorMsg("File is too large. Max size is 100 MB.");
      return;
    }
    setFile(f);
    setStatus("idle");
    setErrorMsg("");
    setProgress(0);
  };

  const handleFileInput = (e) => {
    acceptFile(e.target.files[0]);
  };

  /* ── Drag & drop ── */
  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };
  const handleDragLeave = () => setIsDragging(false);
  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    acceptFile(e.dataTransfer.files[0]);
  };

  // ── Real upload to FastAPI ───────────────────────
  const handleUpload = async () => {
    if (!file) return;
    setStatus("uploading");
    setProgress(10);
    setErrorMsg("");

    try {
      // Get Supabase JWT token
      const { data: { session } } = await supabase.auth.getSession();
      const token = session?.access_token;

      if (!token) {
        setErrorMsg("You must be logged in to upload.");
        setStatus("error");
        return;
      }

      setProgress(30);

      // Build form data
      const formData = new FormData();
      formData.append("file", file);

      setProgress(50);

      // Call FastAPI upload endpoint
      const response = await fetch(`${API_URL}/documents/upload`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          // Do NOT set Content-Type here — browser sets it with boundary for FormData
        },
        body: formData,
      });

      setProgress(90);

      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || "Upload failed. Please try again.");
      }

      const document = await response.json();
      setProgress(100);
      setStatus("done");

      // Pass the real document object back to Documents page
      setTimeout(() => onSuccess(document), 600);

    } catch (err) {
      setStatus("error");
      setErrorMsg(err.message || "Upload failed. Please try again.");
      setProgress(0);
    }
  };

  const removeFile = () => {
    setFile(null);
    setStatus("idle");
    setProgress(0);
    setErrorMsg("");
    if (fileInputRef.current) fileInputRef.current.value = "";
  };

  const formatSize = (bytes) => {
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
    return (bytes / 1024 / 1024).toFixed(2) + " MB";
  };

  return (
    <div
      className="modal-overlay"
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <div className="modal-box">
        {/* ── Header ── */}
        <div className="modal-header">
          <div className="modal-tabs">
            <button className="modal-tab modal-tab--active">Upload Files</button>
          </div>
          <button className="modal-close-btn" onClick={onClose} title="Close">
            <svg
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2.5"
              strokeLinecap="round"
            >
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        </div>

        <p className="modal-size-limit">Max file size: 100 MB at a time</p>

        {/* ── Drop zone ── */}
        <div
          className={`modal-dropzone${isDragging ? " modal-dropzone--active" : ""}`}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,application/pdf"
            className="modal-file-input"
            onChange={handleFileInput}
          />
          <svg
            width="28"
            height="28"
            viewBox="0 0 24 24"
            fill="none"
            stroke="#9ca3af"
            strokeWidth="1.5"
          >
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
            <polyline points="17 8 12 3 7 8" />
            <line x1="12" y1="3" x2="12" y2="15" />
          </svg>
          <p className="modal-drop-text">Drop files here</p>
          <p className="modal-or-text">— or —</p>
          <button
            type="button"
            className="modal-browse-btn"
            onClick={(e) => {
              e.stopPropagation();
              fileInputRef.current?.click();
            }}
          >
            Browse on your device
          </button>
        </div>

        {/* ── Selected file preview ── */}
        {file && (
          <div className="modal-file-preview">
            <div className="modal-file-info">
              {/* PDF icon */}
              <svg
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="#14b8a6"
                strokeWidth="2"
              >
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                <polyline points="14 2 14 8 20 8" />
              </svg>
              <span className="modal-file-name">{file.name}</span>
              <span className="modal-file-size">{formatSize(file.size)}</span>

              {/* Remove file button (only before uploading) */}
              {status === "idle" && (
                <button
                  className="modal-remove-btn"
                  onClick={removeFile}
                  title="Remove"
                >
                  <svg
                    width="13"
                    height="13"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2.5"
                    strokeLinecap="round"
                  >
                    <line x1="18" y1="6" x2="6" y2="18" />
                    <line x1="6" y1="6" x2="18" y2="18" />
                  </svg>
                </button>
              )}

              {/* Uploading spinner */}
              {status === "uploading" && (
                <div className="modal-spinner" />
              )}

              {/* Done checkmark */}
              {status === "done" && (
                <svg
                  width="16"
                  height="16"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="#14b8a6"
                  strokeWidth="2.5"
                  strokeLinecap="round"
                >
                  <polyline points="20 6 9 17 4 12" />
                </svg>
              )}
            </div>

            {/* Progress bar */}
            {status === "uploading" && (
              <div className="modal-progress-wrap">
                <div className="modal-progress-bar">
                  <div
                    className="modal-progress-fill"
                    style={{ width: `${progress}%` }}
                  />
                </div>
                <span className="modal-progress-label">
                  Uploading {progress}%
                </span>
              </div>
            )}

            {status === "done" && (
              <p className="modal-success-text">Upload complete!</p>
            )}
          </div>
        )}

        {/* ── Error message ── */}
        {errorMsg && <p className="modal-error">{errorMsg}</p>}

        {/* ── Supported formats ── */}
        <details className="modal-formats">
          <summary>Supported formats</summary>
          <p>PDF (.pdf) — up to 100 MB per file</p>
        </details>

        {/* ── Footer ── */}
        <div className="modal-footer">
          <button className="modal-cancel-btn" onClick={onClose}>
            Cancel
          </button>
          <button
            className="modal-upload-btn"
            onClick={handleUpload}
            disabled={!file || status === "uploading" || status === "done"}
          >
            {status === "uploading"
              ? "Uploading…"
              : status === "done"
              ? "Uploaded ✓"
              : "Upload"}
          </button>
        </div>
      </div>
    </div>
  );
}

export default UploadModal;
