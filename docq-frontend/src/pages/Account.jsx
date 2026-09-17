import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import Sidebar from "../components/Sidebar";
import { supabase } from "../services/supabaseClient";
import { useAuth } from "../context/AuthContext";
import "../styles/Account.css";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const PLAN_FEATURES_LEFT = [
  "20 documents upload / month",
  "20 prompts / day",
  "20 free credits / month **",
  "3 desks / 1 workspace",
  "100 MB storage ***",
];

const PLAN_FEATURES_RIGHT = [
  "120 pages per document",
  "Math documents (100 pages max) *",
  "2 workspaces max",
  "50 MB per document",
  "Share links",
];

function Account() {
  const navigate = useNavigate();
  const { user, signOut, refreshProfile } = useAuth();

  const [profile,             setProfile]             = useState(null);
  const [loading,             setLoading]             = useState(true);
  const [editingName,         setEditingName]         = useState(false);
  const [tempName,            setTempName]            = useState("");
  const [saving,              setSaving]              = useState(false);
  const [saveMsg,             setSaveMsg]             = useState("");
  const [error,               setError]               = useState("");
  const [showDeleteConfirm,   setShowDeleteConfirm]   = useState(false);

  const fetchProfile = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const { data: { session } } = await supabase.auth.getSession();
      const token = session?.access_token;

      const response = await fetch(`${API_URL}/users/me`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (!response.ok) throw new Error("Failed to load profile");

      const data = await response.json();
      setProfile(data);
      setTempName(data.name || "");
    } catch {
      setError("Could not load profile. Is the backend running?");
    } finally {
      setLoading(false);
    }
  }, []);

  // ── Load profile on mount ────────────────────────
  useEffect(() => {
    let cancelled = false;

    const loadProfile = async () => {
      if (cancelled) return;
      await fetchProfile();
    };

    void loadProfile();

    return () => {
      cancelled = true;
    };
  }, [fetchProfile]);

  // ── Save display name ────────────────────────────
  const handleNameSave = async () => {
    if (!tempName || tempName.trim().length < 2) {
      setSaveMsg("Name must be at least 2 characters.");
      return;
    }
    setSaving(true);
    setSaveMsg("");
    try {
      const { data: { session } } = await supabase.auth.getSession();
      const token = session?.access_token;

      const response = await fetch(`${API_URL}/users/me`, {
        method:  "PUT",
        headers: {
          Authorization:  `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ name: tempName.trim() }),
      });

      if (!response.ok) throw new Error("Failed to update profile");

      const updated = await response.json();
      setProfile(updated);
      setEditingName(false);
      setSaveMsg("Saved!");
      setTimeout(() => setSaveMsg(""), 2500);

      // Refresh credits in sidebar
      if (refreshProfile) refreshProfile();

    } catch {
      setSaveMsg("Failed to save. Please try again.");
    } finally {
      setSaving(false);
    }
  };

  const handleNameCancel = () => {
    setTempName(profile?.name || "");
    setEditingName(false);
    setSaveMsg("");
  };

  // ── Sign out ─────────────────────────────────────
  const handleSignOut = async () => {
    await signOut();
    navigate("/");
  };

  // ── Delete account ───────────────────────────────
  const handleDeleteAccount = async () => {
    // TODO: call DELETE /users/me when backend endpoint is added
    alert("Account deletion will be available soon.");
    setShowDeleteConfirm(false);
  };

  const displayName    = profile?.name || user?.email?.split("@")[0] || "User";
  const avatarInitial  = displayName[0].toUpperCase();
  const creditsLeft    = profile?.credits_remaining ?? 0;

  return (
    <div className="account-container">
      <Sidebar activePage="" />

      <main className="account-main">
        <div className="account-scroll">

          {/* ── Top bar ── */}
          <div className="account-topbar">
            <button
              className="account-close-btn"
              onClick={() => navigate(-1)}
              title="Go back"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" strokeWidth="2">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
          </div>

          <div className="account-body">
            <h1 className="account-page-title">Account</h1>

            {/* Loading */}
            {loading && (
              <div className="account-loading">
                <div className="account-spinner" />
                <p>Loading profile…</p>
              </div>
            )}

            {/* Error */}
            {!loading && error && (
              <div className="account-error">
                <p>{error}</p>
                <button className="btn-save" onClick={fetchProfile}>
                  Try again
                </button>
              </div>
            )}

            {/* Profile content */}
            {!loading && !error && profile && (
              <>
                {/* ── Profile section ── */}
                <section className="account-section">
                  <h2 className="account-section-title">Profile</h2>
                  <div className="account-card">

                    {/* Avatar row */}
                    <div className="profile-avatar-row">
                      <div
                        className="profile-avatar"
                        style={{ background: "#e11d48" }}
                      >
                        {avatarInitial}
                      </div>
                      <div className="profile-avatar-info">
                        <p className="profile-avatar-name">{displayName}</p>
                        <p className="profile-avatar-email">{user?.email}</p>
                      </div>
                    </div>

                    {/* Display name */}
                    <div className="account-field">
                      <label className="account-field-label">Display name</label>
                      <div className="account-field-body">
                        {editingName ? (
                          <div className="account-field-edit">
                            <input
                              className="account-input"
                              value={tempName}
                              onChange={(e) => setTempName(e.target.value)}
                              autoFocus
                              onKeyDown={(e) => {
                                if (e.key === "Enter") handleNameSave();
                                if (e.key === "Escape") handleNameCancel();
                              }}
                            />
                            <div className="account-field-edit-actions">
                              <button
                                className="btn-save"
                                onClick={handleNameSave}
                                disabled={saving}
                              >
                                {saving ? "Saving…" : "Save"}
                              </button>
                              <button
                                className="btn-cancel-edit"
                                onClick={handleNameCancel}
                              >
                                Cancel
                              </button>
                            </div>
                          </div>
                        ) : (
                          <div className="account-field-display">
                            <input
                              className="account-input"
                              value={profile.name || ""}
                              readOnly
                              onClick={() => setEditingName(true)}
                            />
                            {saveMsg && (
                              <span className={`save-msg${saveMsg.includes("Failed") ? " save-msg--error" : ""}`}>
                                {saveMsg}
                              </span>
                            )}
                          </div>
                        )}
                        <p className="account-field-hint">
                          Shown on your profile and in messages. Click to edit.
                        </p>
                      </div>
                    </div>

                    {/* Email */}
                    <div className="account-field">
                      <label className="account-field-label">Email</label>
                      <div className="account-field-body">
                        <div className="account-field-row">
                          <input
                            className="account-input"
                            value={user?.email || ""}
                            readOnly
                          />
                          <button className="btn-change">Change…</button>
                        </div>
                        <p className="account-field-hint">
                          Used to sign in and receive notifications.
                        </p>
                      </div>
                    </div>

                    {/* Password */}
                    <div className="account-field account-field--last">
                      <label className="account-field-label">Password</label>
                      <div className="account-field-body">
                        <div className="account-field-row">
                          <input
                            className="account-input"
                            type="password"
                            value="placeholder"
                            readOnly
                          />
                          <button className="btn-change">Change…</button>
                        </div>
                        <p className="account-field-hint">
                          Required when signing in with email + password.
                        </p>
                      </div>
                    </div>

                  </div>
                </section>

                {/* ── Credits section ── */}
                <section className="account-section">
                  <h2 className="account-section-title">Credits</h2>
                  <div className="account-card">
                    <div className="credits-row">
                      <div className="credits-info">
                        <p className="credits-number">{creditsLeft}</p>
                        <p className="credits-label">credits remaining</p>
                      </div>
                      <p className="credits-hint">
                        Each question costs 1 credit. Credits reset monthly.
                      </p>
                    </div>
                  </div>
                </section>

                {/* ── Plan section ── */}
                <section className="account-section">
                  <h2 className="account-section-title">Plan</h2>
                  <div className="plan-card">
                    <p className="plan-name">Community</p>
                    <div className="plan-features-grid">
                      <ul className="plan-features-col">
                        {PLAN_FEATURES_LEFT.map((f) => (
                          <li key={f}>
                            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#14b8a6" strokeWidth="2.5">
                              <polyline points="20 6 9 17 4 12" />
                            </svg>
                            {f}
                          </li>
                        ))}
                      </ul>
                      <ul className="plan-features-col">
                        {PLAN_FEATURES_RIGHT.map((f) => (
                          <li key={f}>
                            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#14b8a6" strokeWidth="2.5">
                              <polyline points="20 6 9 17 4 12" />
                            </svg>
                            {f}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                </section>

                {/* ── Sign out ── */}
                <section className="account-section">
                  <div className="account-card">
                    <div className="signout-row">
                      <div>
                        <p className="signout-label">Sign out</p>
                        <p className="signout-desc">
                          Sign out of your account on this device.
                        </p>
                      </div>
                      <button
                        className="btn-signout"
                        onClick={handleSignOut}
                      >
                        Sign out
                      </button>
                    </div>
                  </div>
                </section>

                {/* ── Danger zone ── */}
                <section className="account-section">
                  <h2 className="account-section-title danger-title">
                    Danger Zone
                  </h2>
                  <div className="account-card danger-card">
                    <div className="danger-row">
                      <div>
                        <p className="danger-label">Delete account</p>
                        <p className="danger-desc">
                          Permanently delete your account and all data. This
                          cannot be undone.
                        </p>
                      </div>
                      <button
                        className="btn-delete-account"
                        onClick={() => setShowDeleteConfirm(true)}
                      >
                        Delete account
                      </button>
                    </div>
                  </div>
                </section>
              </>
            )}
          </div>
        </div>

        {/* ── Delete confirmation modal ── */}
        {showDeleteConfirm && (
          <div
            className="confirm-overlay"
            onClick={(e) =>
              e.target === e.currentTarget && setShowDeleteConfirm(false)
            }
          >
            <div className="confirm-modal">
              <h3>Delete your account?</h3>
              <p>
                This will permanently delete your account and all your
                documents and chats. This cannot be undone.
              </p>
              <div className="confirm-actions">
                <button
                  className="btn-cancel-edit"
                  onClick={() => setShowDeleteConfirm(false)}
                >
                  Cancel
                </button>
                <button
                  className="btn-delete-account"
                  onClick={handleDeleteAccount}
                >
                  Yes, delete my account
                </button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default Account;
