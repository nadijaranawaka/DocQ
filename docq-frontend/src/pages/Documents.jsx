import { useState, useEffect, useRef, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import UploadModal from "../components/UploadModal";
import SearchIcon from "../assets/search.svg";
import HomeIcon from "../assets/home-icon.svg";
import { supabase } from "../services/supabaseClient";
import "../styles/Documents.css";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";
const POLL_INTERVAL_MS = 4000; // check every 4 seconds

function Documents() {
  const navigate = useNavigate();
  const [documents,       setDocuments]      = useState([]);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [selectedIds,     setSelectedIds]    = useState([]);
  const [openMenuId,      setOpenMenuId]     = useState(null);
  const [searchQuery,     setSearchQuery]    = useState("");
  const [loading,         setLoading]        = useState(true);
  const [error,           setError]          = useState("");
  const pollRef = useRef(null);

  const stopPolling = useCallback(() => {
    if (pollRef.current) {
      clearInterval(pollRef.current);
      pollRef.current = null;
    }
  }, []);

  // ── Poll — only fetches to update statuses, no loading flash ─
  const pollDocumentStatuses = useCallback(async () => {
    try {
      const { data: { session } } = await supabase.auth.getSession();
      const token = session?.access_token;
      const response = await fetch(`${API_URL}/documents`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!response.ok) return;
      const fresh = await response.json();

      setDocuments((prev) =>
        prev.map((doc) => {
          const updated = fresh.find(
            (f) => f.document_id === doc.document_id
          );
          return updated ? { ...doc, status: updated.status } : doc;
        })
      );
    } catch {
      // silent — don't show errors during polling
    }
  }, []);

  const startPolling = useCallback(() => {
    if (pollRef.current) return; // already polling
    pollRef.current = setInterval(() => {
      pollDocumentStatuses();
    }, POLL_INTERVAL_MS);
  }, [pollDocumentStatuses]);

  const fetchDocuments = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const { data: { session } } = await supabase.auth.getSession();
      const token = session?.access_token;
      const response = await fetch(`${API_URL}/documents`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!response.ok) throw new Error("Failed to load documents");
      const data = await response.json();
      setDocuments(data);
    } catch {
      setError("Could not load documents. Is the backend running?");
    } finally {
      setLoading(false);
    }
  }, []);

  // ── Load documents on mount ──────────────────────
  useEffect(() => {
    const loadTimer = setTimeout(() => {
      fetchDocuments();
    }, 0);
    return () => {
      clearTimeout(loadTimer);
      stopPolling();
    };
  }, [fetchDocuments, stopPolling]);

  // ── Start polling if any doc is still processing ─
  useEffect(() => {
    const hasProcessing = documents.some(
      (d) => d.status === "processing" || d.status === "uploaded"
    );
    if (hasProcessing) {
      startPolling();
    } else {
      stopPolling();
    }
  }, [documents, startPolling, stopPolling]);

  const handleUploadSuccess = (newDoc) => {
    setDocuments((prev) => [newDoc, ...prev]);
    setShowUploadModal(false);
  };

  const handleDelete = async (doc) => {
    if (!window.confirm(`Delete "${doc.filename}"? This cannot be undone.`))
      return;
    try {
      const { data: { session } } = await supabase.auth.getSession();
      const token = session?.access_token;
      const response = await fetch(
        `${API_URL}/documents/${doc.document_id}`,
        { method: "DELETE", headers: { Authorization: `Bearer ${token}` } }
      );
      if (!response.ok) throw new Error("Delete failed");
      setDocuments((prev) =>
        prev.filter((d) => d.document_id !== doc.document_id)
      );
      setSelectedIds((prev) =>
        prev.filter((id) => id !== doc.document_id)
      );
      setOpenMenuId(null);
    } catch {
      alert("Failed to delete document. Please try again.");
    }
  };

  const handleNewChat = async (doc) => {
    if (doc.status !== "ready") {
      alert(
        doc.status === "processing" || doc.status === "uploaded"
          ? "This document is still being processed. Please wait until it shows Ready."
          : "This document failed to process. Please delete it and upload again."
      );
      return;
    }
    try {
      const { data: { session } } = await supabase.auth.getSession();
      const token = session?.access_token;
      const response = await fetch(`${API_URL}/chats`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ document_id: doc.document_id }),
      });
      if (!response.ok) throw new Error("Failed to create chat");
      const chat = await response.json();
      navigate(`/chat/${chat.chat_id}`);
    } catch {
      alert("Could not create chat. Please try again.");
    }
  };

  const toggleSelect = (id) => {
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((s) => s !== id) : [...prev, id]
    );
  };

  const toggleSelectAll = () => {
    if (selectedIds.length === documents.length) setSelectedIds([]);
    else setSelectedIds(documents.map((d) => d.document_id));
  };

  const allSelected =
    documents.length > 0 && selectedIds.length === documents.length;

  const filteredDocuments = documents.filter((doc) =>
    doc.filename.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="docs-container">
      <Sidebar activePage="documents" />
      <main className="docs-main">

        {/* ── Top bar ── */}
        <div className="docs-topbar">
          <div className="docs-topbar-left">
            <h1 className="docs-title">Documents</h1>
            {documents.length > 0 && (
              <p className="docs-subtitle">
                You have {documents.length} document
                {documents.length !== 1 ? "s" : ""} in this workspace.
              </p>
            )}
          </div>
          <div className="docs-topbar-right">
            <div className="search-bar">
              <img src={SearchIcon} alt="Search" className="search-icon" />
              <input
                type="text"
                placeholder="Search documents..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
            <button
              className="btn-add"
              onClick={() => setShowUploadModal(true)}
            >
              <svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
                <line x1="6" y1="1" x2="6" y2="11" />
                <line x1="1" y1="6" x2="11" y2="6" />
              </svg>
              Add
            </button>
          </div>
        </div>

        {/* ── Content ── */}
        <div className="docs-content">

          {loading && (
            <div className="docs-loading">
              <div className="docs-spinner" />
              <p>Loading documents…</p>
            </div>
          )}

          {!loading && error && (
            <div className="docs-error">
              <p>{error}</p>
              <button className="btn-add" onClick={fetchDocuments}>
                Try again
              </button>
            </div>
          )}

          {!loading && !error && documents.length === 0 && (
            <div className="empty-state">
              <div className="empty-icon-wrap">
                <img src={HomeIcon} alt="No documents" />
              </div>
              <h2 className="empty-title">Welcome to docAnalyzer!</h2>
              <p className="empty-subtitle-text">
                There are no documents in this workspace yet.
              </p>
              <p className="empty-desc">
                Add, view, and control your documents from here.
              </p>
              <button
                className="btn-add-doc"
                onClick={() => setShowUploadModal(true)}
              >
                <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
                  <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                  <polyline points="17 8 12 3 7 8" />
                  <line x1="12" y1="3" x2="12" y2="15" />
                </svg>
                + Add document
              </button>
            </div>
          )}

          {!loading && !error && documents.length > 0 && (
            <div className="doc-list-card">
              <div className="doc-list-controls">
                <label className="select-all-label">
                  <input
                    type="checkbox"
                    checked={allSelected}
                    onChange={toggleSelectAll}
                  />
                  <span>Select all</span>
                </label>
                <div className="doc-filters">
                  <span className="filter-created">
                    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" strokeWidth="2">
                      <circle cx="12" cy="12" r="10" />
                      <polyline points="12 6 12 12 16 14" />
                    </svg>
                    Created
                  </span>
                  <select className="filter-select">
                    <option>Date</option>
                    <option>Name</option>
                  </select>
                </div>
              </div>

              {filteredDocuments.length === 0 && searchQuery ? (
                <p className="doc-no-results">
                  No documents match "{searchQuery}"
                </p>
              ) : (
                filteredDocuments.map((doc) => (
                  <div
                    key={doc.document_id}
                    className={`doc-row${selectedIds.includes(doc.document_id) ? " doc-row--selected" : ""}`}
                  >
                    <input
                      type="checkbox"
                      className="doc-check"
                      checked={selectedIds.includes(doc.document_id)}
                      onChange={() => toggleSelect(doc.document_id)}
                    />
                    <svg className="doc-file-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" strokeWidth="2">
                      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                      <polyline points="14 2 14 8 20 8" />
                    </svg>

                    <span className="doc-name">{doc.filename}</span>

                    {/* Status badge with spinner for processing */}
                    <span className={`doc-status-badge doc-status--${doc.status}`}>
                      {(doc.status === "processing" || doc.status === "uploaded") && (
                        <span className="status-spinner" />
                      )}
                      {doc.status === "ready"      ? "Ready"
                        : doc.status === "processing" ? "Processing…"
                        : doc.status === "uploaded"   ? "Uploading…"
                        : doc.status === "failed"     ? "Failed"
                        : doc.status}
                    </span>

                    <button
                      className={`btn-new-chat${doc.status !== "ready" ? " btn-new-chat--disabled" : ""}`}
                      onClick={() => handleNewChat(doc)}
                    >
                      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                      </svg>
                      New Chat
                    </button>

                    <div className="doc-menu-wrap">
                      <button
                        className="doc-icon-btn"
                        onClick={() =>
                          setOpenMenuId(
                            openMenuId === doc.document_id
                              ? null
                              : doc.document_id
                          )
                        }
                      >
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="#6b7280">
                          <circle cx="12" cy="5" r="1.5" />
                          <circle cx="12" cy="12" r="1.5" />
                          <circle cx="12" cy="19" r="1.5" />
                        </svg>
                      </button>
                      {openMenuId === doc.document_id && (
                        <div className="doc-dropdown">
                          <button
                            className="doc-dropdown-item doc-dropdown-item--danger"
                            onClick={() => handleDelete(doc)}
                          >
                            Delete
                          </button>
                        </div>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>
          )}
        </div>
      </main>

      {showUploadModal && (
        <UploadModal
          onClose={() => setShowUploadModal(false)}
          onSuccess={handleUploadSuccess}
        />
      )}
    </div>
  );
}

export default Documents;
