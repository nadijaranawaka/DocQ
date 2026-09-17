import "../styles/Chats.css";
import Sidebar from "../components/Sidebar";
import SearchIcon from "../assets/search.svg";
import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { supabase } from "../services/supabaseClient";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function Chats() {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState("");
  const [chats, setChats] = useState([]);
  const [selectedIds, setSelectedIds] = useState([]);
  const [openMenuId, setOpenMenuId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // ── Load chats on mount ──────────────────────────

  const fetchChats = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const {
        data: { session },
      } = await supabase.auth.getSession();
      const token = session?.access_token;

      const response = await fetch(`${API_URL}/chats`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!response.ok) throw new Error("Failed to load chats");

      const data = await response.json();
      setChats(data);
    } catch {
      setError("Could not load chats. Is the backend running?");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    let cancelled = false;

    const loadChats = async () => {
      if (cancelled) return;
      await fetchChats();
    };

    void loadChats();

    return () => {
      cancelled = true;
    };
  }, [fetchChats]);

  // ── Delete chat ──────────────────────────────────
  const handleDelete = async (chat) => {
    if (!window.confirm("Delete this chat? This cannot be undone.")) return;
    try {
      const {
        data: { session },
      } = await supabase.auth.getSession();
      const token = session?.access_token;

      const response = await fetch(`${API_URL}/chats/${chat.chat_id}`, {
        method: "DELETE",
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!response.ok) throw new Error("Delete failed");

      setChats((prev) => prev.filter((c) => c.chat_id !== chat.chat_id));
      setSelectedIds((prev) => prev.filter((id) => id !== chat.chat_id));
      setOpenMenuId(null);
    } catch {
      alert("Failed to delete chat. Please try again.");
    }
  };

  // ── Select helpers ───────────────────────────────
  const filteredChats = chats.filter((c) =>
    (c.title || "Untitled chat")
      .toLowerCase()
      .includes(searchQuery.toLowerCase()),
  );

  const allSelected =
    filteredChats.length > 0 && selectedIds.length === filteredChats.length;

  const toggleSelect = (id) => {
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((s) => s !== id) : [...prev, id],
    );
  };

  const toggleSelectAll = () => {
    if (allSelected) setSelectedIds([]);
    else setSelectedIds(filteredChats.map((c) => c.chat_id));
  };

  return (
    <div className="chats-container">
      <Sidebar activePage="chats" />
      <main className="chats-main">
        {/* ── Top bar ── */}
        <div className="chats-topbar">
          <div className="chats-topbar-left">
            <h1 className="chats-title">Chats</h1>
            {chats.length > 0 && (
              <p className="chats-subtitle">
                You have {chats.length} chat{chats.length !== 1 ? "s" : ""} in
                this workspace.
              </p>
            )}
          </div>
          <div className="chats-topbar-right">
            <button
              className="btn-new-chat"
              onClick={() => navigate("/documents")}
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
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
              </svg>
              New Chat
            </button>
          </div>
        </div>

        {/* ── Content ── */}
        <div className="chats-content">
          {/* Loading */}
          {loading && (
            <div className="chats-loading">
              <div className="chats-spinner" />
              <p>Loading chats…</p>
            </div>
          )}

          {/* Error */}
          {!loading && error && (
            <div className="chats-error">
              <p>{error}</p>
              <button className="btn-new-chat" onClick={fetchChats}>
                Try again
              </button>
            </div>
          )}

          {/* Empty */}
          {!loading && !error && chats.length === 0 && (
            <div className="chats-empty">
              <svg
                width="48"
                height="48"
                viewBox="0 0 24 24"
                fill="none"
                stroke="#d1d5db"
                strokeWidth="1.5"
              >
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
              </svg>
              <p className="chats-empty-title">No chats yet</p>
              <p className="chats-empty-desc">
                Upload a document and click "New Chat" to get started.
              </p>
            </div>
          )}

          {/* Chat list */}
          {!loading && !error && chats.length > 0 && (
            <div className="chats-list-card">
              {/* Controls */}
              <div className="chats-controls">
                <label className="select-all-label">
                  <input
                    type="checkbox"
                    checked={allSelected}
                    onChange={toggleSelectAll}
                  />
                  <span>Select all</span>
                </label>
                <div className="chats-controls-right">
                  <span className="filter-updated">
                    <svg
                      width="13"
                      height="13"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="#9ca3af"
                      strokeWidth="2"
                    >
                      <circle cx="12" cy="12" r="10" />
                      <polyline points="12 6 12 12 16 14" />
                    </svg>
                    Updated
                  </span>
                  <div className="search-bar">
                    <img
                      src={SearchIcon}
                      alt="Search"
                      className="search-icon"
                    />
                    <input
                      type="text"
                      placeholder="Search chats..."
                      value={searchQuery}
                      onChange={(e) => setSearchQuery(e.target.value)}
                    />
                  </div>
                </div>
              </div>

              {/* No search results */}
              {filteredChats.length === 0 && searchQuery ? (
                <p className="chats-no-results">
                  No chats match "{searchQuery}"
                </p>
              ) : (
                filteredChats.map((chat) => (
                  <div
                    key={chat.chat_id}
                    className={`chat-row${selectedIds.includes(chat.chat_id) ? " chat-row--selected" : ""}`}
                  >
                    <input
                      type="checkbox"
                      className="chat-check"
                      checked={selectedIds.includes(chat.chat_id)}
                      onChange={() => toggleSelect(chat.chat_id)}
                    />

                    <svg
                      className="chat-row-icon"
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="#9ca3af"
                      strokeWidth="2"
                    >
                      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                    </svg>

                    <span className="chat-row-title">
                      {chat.title || "Untitled chat"}
                    </span>

                    <button
                      className="btn-open-chat"
                      onClick={() => navigate(`/chat/${chat.chat_id}`)}
                    >
                      <svg
                        width="13"
                        height="13"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                      >
                        <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
                        <polyline points="15 3 21 3 21 9" />
                        <line x1="10" y1="14" x2="21" y2="3" />
                      </svg>
                      Open Chat
                    </button>

                    <div className="chat-doc-badge">
                      <svg
                        width="12"
                        height="12"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="#9ca3af"
                        strokeWidth="2"
                      >
                        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                        <polyline points="14 2 14 8 20 8" />
                      </svg>
                      <span>{chat.document_filename || "Unknown"}</span>
                    </div>

                    <div className="chat-menu-wrap">
                      <button
                        className="chat-icon-btn"
                        onClick={() =>
                          setOpenMenuId(
                            openMenuId === chat.chat_id ? null : chat.chat_id,
                          )
                        }
                      >
                        <svg
                          width="16"
                          height="16"
                          viewBox="0 0 24 24"
                          fill="#6b7280"
                        >
                          <circle cx="12" cy="5" r="1.5" />
                          <circle cx="12" cy="12" r="1.5" />
                          <circle cx="12" cy="19" r="1.5" />
                        </svg>
                      </button>
                      {openMenuId === chat.chat_id && (
                        <div className="chat-dropdown">
                          <button
                            className="chat-dropdown-item chat-dropdown-item--danger"
                            onClick={() => handleDelete(chat)}
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
    </div>
  );
}

export default Chats;
