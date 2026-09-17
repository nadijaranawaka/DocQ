import { useState, useRef, useEffect, useCallback } from "react";
import { useNavigate, useParams } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import { supabase } from "../services/supabaseClient";
import "../styles/ChatConversation.css";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

// ── Simple markdown renderer for bold and bullet lists ──
function renderContent(text) {
  const lines = text.split("\n");
  const elements = [];
  let key = 0;

  for (const line of lines) {
    if (line.trim() === "") {
      elements.push(<br key={key++} />);
      continue;
    }
    if (line.trim().startsWith("- ")) {
      elements.push(
        <li key={key++}>{parseBold(line.trim().slice(2))}</li>
      );
      continue;
    }
    if (line.match(/^\s{2,}- /)) {
      elements.push(
        <li key={key++} className="sub-bullet">
          {parseBold(line.trim().slice(2))}
        </li>
      );
      continue;
    }
    elements.push(<p key={key++}>{parseBold(line)}</p>);
  }
  return elements;
}

function parseBold(text) {
  const parts = text.split(/\*\*(.*?)\*\*/g);
  return parts.map((part, i) =>
    i % 2 === 1 ? <strong key={i}>{part}</strong> : part
  );
}

function ChatConversation() {
  const { chatId }  = useParams();
  const navigate    = useNavigate();

  const [messages,  setMessages]  = useState([]);
  const [chatInfo,  setChatInfo]  = useState(null);
  const [inputValue, setInputValue] = useState("");
  const [loading,   setLoading]   = useState(true);
  const [sending,   setSending]   = useState(false);
  const [error,     setError]     = useState("");

  const messagesEndRef = useRef(null);
  const textareaRef    = useRef(null);

  const fetchMessages = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const { data: { session } } = await supabase.auth.getSession();
      const token = session?.access_token;

      const response = await fetch(
        `${API_URL}/chats/${chatId}/messages`,
        { headers: { Authorization: `Bearer ${token}` } }
      );

      if (!response.ok) throw new Error("Failed to load chat");

      const data = await response.json();
      setChatInfo(data.chat);
      setMessages(data.messages || []);
    } catch {
      setError("Could not load this chat. Is the backend running?");
    } finally {
      setLoading(false);
    }
  }, [chatId]);

  // ── Load messages on mount ───────────────────────
  useEffect(() => {
    let cancelled = false;

    const loadMessages = async () => {
      if (cancelled) return;
      await fetchMessages();
    };

    void loadMessages();

    return () => {
      cancelled = true;
    };
  }, [fetchMessages]);

  // ── Scroll to bottom on new message ─────────────
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // ── Auto-resize textarea ─────────────────────────
  const handleInputChange = (e) => {
    setInputValue(e.target.value);
    const ta = textareaRef.current;
    if (ta) {
      ta.style.height = "auto";
      ta.style.height = Math.min(ta.scrollHeight, 120) + "px";
    }
  };

  // ── Send message ─────────────────────────────────
  const handleSend = async () => {
    const text = inputValue.trim();
    if (!text || sending) return;

    // Optimistically add user message to UI
    const tempUserMsg = {
      message_id: `temp-${Date.now()}`,
      role:       "user",
      content:    text,
    };
    setMessages((prev) => [...prev, tempUserMsg]);
    setInputValue("");
    if (textareaRef.current) textareaRef.current.style.height = "auto";
    setSending(true);

    try {
      const { data: { session } } = await supabase.auth.getSession();
      const token = session?.access_token;

      const response = await fetch(
        `${API_URL}/chats/${chatId}/messages`,
        {
          method:  "POST",
          headers: {
            Authorization:  `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ content: text }),
        }
      );

      if (!response.ok) {
        const err = await response.json().catch(() => ({}));
        throw new Error(err.detail || "Failed to send message");
      }

      const data = await response.json();

      // Replace temp message with real one and add AI response
      setMessages((prev) => [
        ...prev.filter((m) => m.message_id !== tempUserMsg.message_id),
        data.user_message,
        data.assistant_message,
      ]);
    } catch (err) {
      // Remove the optimistic message on failure
      setMessages((prev) =>
        prev.filter((m) => m.message_id !== tempUserMsg.message_id)
      );
      alert(err.message || "Failed to send message. Please try again.");
    } finally {
      setSending(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // ── Error state ──────────────────────────────────
  if (!loading && error) {
    return (
      <div className="chat-conv-container">
        <Sidebar activePage="chats" />
        <main className="chat-conv-main">
          <div className="chat-conv-topbar">
            <button className="chat-conv-back-btn" onClick={() => navigate("/chats")}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
                <line x1="19" y1="12" x2="5" y2="12" />
                <polyline points="12 19 5 12 12 5" />
              </svg>
              all chats
            </button>
          </div>
          <div className="chat-conv-error">
            <p>{error}</p>
            <button className="chat-conv-retry-btn" onClick={fetchMessages}>
              Try again
            </button>
          </div>
        </main>
      </div>
    );
  }

  return (
    <div className="chat-conv-container">
      <Sidebar activePage="chats" />

      <main className="chat-conv-main">

        {/* ── Top bar ── */}
        <div className="chat-conv-topbar">
          <button
            className="chat-conv-back-btn"
            onClick={() => navigate("/chats")}
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
              <line x1="19" y1="12" x2="5" y2="12" />
              <polyline points="12 19 5 12 12 5" />
            </svg>
            all chats
          </button>

          {chatInfo?.document_filename && (
            <div className="chat-conv-doc-badge">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" strokeWidth="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
                <polyline points="14 2 14 8 20 8" />
              </svg>
              <span>{chatInfo.document_filename}</span>
            </div>
          )}
        </div>

        {/* ── Messages ── */}
        <div className="chat-conv-messages">
          {loading ? (
            <div className="chat-conv-loading">
              <div className="chat-conv-spinner" />
              <p>Loading conversation…</p>
            </div>
          ) : messages.length === 0 ? (
            <div className="chat-conv-empty">
              <p>Ask anything about your document to get started.</p>
            </div>
          ) : (
            messages.map((msg) => (
              <MessageBubble key={msg.message_id} msg={msg} />
            ))
          )}

          {/* Typing indicator */}
          {sending && (
            <div className="chat-conv-typing">
              <div className="chat-conv-ai-avatar">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#14b8a6" strokeWidth="2">
                  <circle cx="12" cy="12" r="10" />
                  <path d="M8 12h8M12 8v8" />
                </svg>
              </div>
              <div className="typing-dots">
                <span /><span /><span />
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* ── Input area ── */}
        <div className="chat-conv-input-area">
          <div className="chat-conv-model-row">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" strokeWidth="2">
              <circle cx="12" cy="12" r="10" />
              <path d="M8 12h8M12 8v8" />
            </svg>
            <span className="chat-conv-model-name">GPT O5S 120b</span>
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" strokeWidth="2">
              <polyline points="18 13 12 19 6 13" />
            </svg>
            <span className="chat-conv-model-divider">|</span>
          </div>

          <div className="chat-conv-input-wrap">
            <textarea
              ref={textareaRef}
              className="chat-conv-textarea"
              placeholder={
                chatInfo?.document_filename
                  ? `Ask any question about '${chatInfo.document_filename}'`
                  : "Ask a question about your document…"
              }
              value={inputValue}
              onChange={handleInputChange}
              onKeyDown={handleKeyDown}
              rows={1}
              disabled={sending || loading}
            />
            <button
              className="chat-conv-send-btn"
              onClick={handleSend}
              disabled={!inputValue.trim() || sending || loading}
              title="Send"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
                <line x1="22" y1="2" x2="11" y2="13" />
                <polygon points="22 2 15 22 11 13 2 9 22 2" />
              </svg>
            </button>
          </div>

          <p className="chat-conv-char-count">
            {inputValue.length} characters
          </p>
        </div>
      </main>
    </div>
  );
}

// ── Single message bubble ────────────────────────────────────
function MessageBubble({ msg }) {
  const isUser = msg.role === "user";
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(msg.content);
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  };

  return (
    <div className={`chat-conv-msg-row ${isUser ? "user-row" : "ai-row"}`}>
      <div className={`chat-conv-avatar ${isUser ? "user-avatar" : "ai-avatar"}`}>
        {isUser ? (
          <span>U</span>
        ) : (
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#14b8a6" strokeWidth="2">
            <circle cx="12" cy="12" r="10" />
            <path d="M8 12h8M12 8v8" />
          </svg>
        )}
      </div>

      <div className={`chat-conv-bubble ${isUser ? "user-bubble" : "ai-bubble"}`}>
        <div className="chat-conv-bubble-content">
          {isUser ? (
            <p>{msg.content}</p>
          ) : (
            <div className="ai-content">{renderContent(msg.content)}</div>
          )}
        </div>

        {!isUser && (
          <div className="chat-conv-msg-actions">
            <button onClick={handleCopy} title={copied ? "Copied!" : "Copy"}>
              {copied ? (
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#14b8a6" strokeWidth="2">
                  <polyline points="20 6 9 17 4 12" />
                </svg>
              ) : (
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" strokeWidth="2">
                  <rect x="9" y="9" width="13" height="13" rx="2" />
                  <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" />
                </svg>
              )}
            </button>
            <button title="Good response">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" strokeWidth="2">
                <path d="M14 9V5a3 3 0 0 0-3-3l-4 9v11h11.28a2 2 0 0 0 2-1.7l1.38-9a2 2 0 0 0-2-2.3H14z" />
                <path d="M7 22H4a2 2 0 0 1-2-2v-7a2 2 0 0 1 2-2h3" />
              </svg>
            </button>
            <button title="Bad response">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" strokeWidth="2">
                <path d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3H10z" />
                <path d="M17 2h2.67A2.31 2.31 0 0 1 22 4v7a2.31 2.31 0 0 1-2.33 2H17" />
              </svg>
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default ChatConversation;
