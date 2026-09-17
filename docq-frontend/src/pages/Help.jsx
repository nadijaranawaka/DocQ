import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import "../styles/Help.css";

// Mock user data — replace with real Supabase session when backend is ready
const MOCK_USER = {
  email: "xxtxxskullxx2007@gmail.com",
  userId: "usr-we45-wet-qht-qehs-pw4bsda4sd4",
};

const FAQS = [
  {
    q: "How do I upload a document?",
    a: "Go to the Documents page and click the Add button. You can drag and drop a PDF or click Browse on your device to select one.",
  },
  {
    q: "What file formats are supported?",
    a: "Currently docAnalyzer supports PDF files only, up to 100 MB per file.",
  },
  {
    q: "How do credits work?",
    a: "Each question you ask costs 1 credit. You receive 20 free credits per month on the Community plan. Credits reset at the start of each billing period.",
  },
  {
    q: "How long does document processing take?",
    a: "Most documents are processed within a few seconds to a minute depending on file size. You will see the status update on the Documents page.",
  },
  {
    q: "Can I chat about multiple documents at once?",
    a: "In the current version each chat is linked to a single document. Multi-document querying is planned for a future release.",
  },
  {
    q: "How do I delete my account?",
    a: "Go to Account settings by clicking your profile at the bottom of the sidebar, then scroll to the Danger Zone section and click Delete account.",
  },
];

function Help() {
  const navigate = useNavigate();
  const [openFaq, setOpenFaq] = useState(null);
  const [faqOpen, setFaqOpen] = useState(false);

  const toggleFaq = (index) => {
    setOpenFaq(openFaq === index ? null : index);
  };

  return (
    <div className="help-container">
      <Sidebar activePage="help" />

      <main className="help-main">
        <div className="help-scroll">

          {/* ── Close button top right ── */}
          <div className="help-topbar">
            <button
              className="help-close-btn"
              onClick={() => navigate(-1)}
              title="Go back"
            >
              <svg
                width="16"
                height="16"
                viewBox="0 0 24 24"
                fill="none"
                stroke="#9ca3af"
                strokeWidth="2"
              >
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
          </div>

          <div className="help-body">
            {/* ── Page heading ── */}
            <h1 className="help-title">Support</h1>
            <p className="help-subtitle">
              Get help from the team and other docAnalyzer users.
            </p>

            {/* ── FAQ accordion ── */}
            <div className="help-faq-wrap">
              <button
                className="help-faq-toggle"
                onClick={() => setFaqOpen((o) => !o)}
              >
                <div className="help-faq-toggle-left">
                  {/* Clipboard icon */}
                  <svg
                    width="15"
                    height="15"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="#6b7280"
                    strokeWidth="2"
                  >
                    <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2" />
                    <rect x="8" y="2" width="8" height="4" rx="1" ry="1" />
                  </svg>
                  <span>
                    <strong>Check the docs first</strong> — Most common
                    questions are answered there.
                  </span>
                </div>
                <svg
                  className={`faq-chevron${faqOpen ? " faq-chevron--open" : ""}`}
                  width="14"
                  height="14"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="#9ca3af"
                  strokeWidth="2"
                >
                  <polyline points="6 9 12 15 18 9" />
                </svg>
              </button>

              {faqOpen && (
                <div className="help-faqs">
                  {FAQS.map((faq, i) => (
                    <div key={i} className="faq-item">
                      <button
                        className="faq-question"
                        onClick={() => toggleFaq(i)}
                      >
                        <span>{faq.q}</span>
                        <svg
                          className={`faq-chevron${openFaq === i ? " faq-chevron--open" : ""}`}
                          width="13"
                          height="13"
                          viewBox="0 0 24 24"
                          fill="none"
                          stroke="#9ca3af"
                          strokeWidth="2"
                        >
                          <polyline points="6 9 12 15 18 9" />
                        </svg>
                      </button>
                      {openFaq === i && (
                        <p className="faq-answer">{faq.a}</p>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* ── Support channels ── */}
            <div className="help-channels">

              {/* Discord card */}
              <div className="help-channel-card help-channel-card--discord">
                <div className="channel-icon-wrap channel-icon-wrap--discord">
                  {/* Discord icon */}
                  <svg width="22" height="22" viewBox="0 0 71 55" fill="none">
                    <path
                      d="M60.1 4.9A58.6 58.6 0 0045.7.4a.2.2 0 00-.2.1 40.9 40.9 0 00-1.8 3.7 54 54 0 00-16.2 0A37 37 0 0025.7.5a.2.2 0 00-.2-.1A58.5 58.5 0 0011 4.9a.2.2 0 00-.1.1C1.5 18.6-.9 32 .3 45.1a.2.2 0 00.1.2 58.9 58.9 0 0017.7 8.9.2.2 0 00.2-.1 42 42 0 003.6-5.9.2.2 0 00-.1-.3 38.8 38.8 0 01-5.5-2.6.2.2 0 010-.3l1.1-.9a.2.2 0 01.2 0c11.5 5.3 24 5.3 35.4 0a.2.2 0 01.2 0l1.1.9a.2.2 0 010 .3 36 36 0 01-5.5 2.6.2.2 0 00-.1.3 47 47 0 003.6 5.9.2.2 0 00.2.1 58.7 58.7 0 0017.8-8.9.2.2 0 00.1-.2C72.9 30 70.1 16.8 60.2 5a.2.2 0 00-.1-.1zM23.7 37.3c-3.5 0-6.4-3.2-6.4-7.2s2.8-7.2 6.4-7.2c3.6 0 6.5 3.2 6.4 7.2 0 4-2.8 7.2-6.4 7.2zm23.6 0c-3.5 0-6.4-3.2-6.4-7.2s2.8-7.2 6.4-7.2c3.6 0 6.5 3.2 6.4 7.2 0 4-2.8 7.2-6.4 7.2z"
                      fill="#ffffff"
                    />
                  </svg>
                </div>
                <h3 className="channel-title">Join us on Discord</h3>
                <p className="channel-desc">
                  Ask questions, share what you build, and get feature previews
                  from the team. We're most active during European business
                  hours.
                </p>
                <div className="discord-tags">
                  <span>#help</span>
                  <span>#feature-requests</span>
                  <span>#showcase</span>
                </div>
                <a
                  href="https://discord.gg/docanalyzer"
                  target="_blank"
                  rel="noreferrer"
                  className="btn-discord"
                >
                  Join the Discord →
                </a>
              </div>

              {/* Email card */}
              <div className="help-channel-card">
                <div className="channel-icon-wrap channel-icon-wrap--email">
                  {/* Mail icon */}
                  <svg
                    width="22"
                    height="22"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="#ffffff"
                    strokeWidth="2"
                  >
                    <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" />
                    <polyline points="22,6 12,13 2,6" />
                  </svg>
                </div>
                <h3 className="channel-title">Email support</h3>
                <p className="channel-desc">
                  For account-specific issues, billing, or anything you can't
                  share publicly. We reply within one business day.
                </p>
                <div className="email-ref-box">
                  <span className="email-ref-label">ref:</span>
                  <span className="email-ref-value">
                    ↑ paste it into your message. It helps us trace exactly what
                    went wrong.
                  </span>
                </div>
                <a
                  href="mailto:help@docanalyzer.ai"
                  className="btn-email"
                >
                  help@docanalyzer.ai
                </a>
              </div>
            </div>

            {/* ── Account info ── */}
            <div className="help-account-card">
              <h3 className="help-account-title">Account</h3>
              <div className="help-account-row">
                <span className="help-account-label">Signed in as</span>
                <span className="help-account-value">{MOCK_USER.email}</span>
              </div>
              <div className="help-account-row">
                <span className="help-account-label">User ID</span>
                <span className="help-account-value help-account-mono">
                  {MOCK_USER.userId}
                </span>
              </div>
            </div>

          </div>
        </div>
      </main>
    </div>
  );
}

export default Help;
