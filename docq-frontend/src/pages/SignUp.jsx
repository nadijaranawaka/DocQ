import "../styles/SignUp.css";
import { useNavigate } from "react-router-dom";
import Logo from "../assets/logo-icon.svg.svg";
import { useAuth } from "../context/AuthContext";
import { useState } from "react";

function SignUp() {
  const { signUpWithEmail } = useAuth();
  const navigate = useNavigate();

  const [name,     setName]     = useState("");
  const [email,    setEmail]    = useState("");
  const [password, setPassword] = useState("");
  const [confirm,  setConfirm]  = useState("");
  const [error,    setError]    = useState("");
  const [loading,  setLoading]  = useState(false);
  const [success,  setSuccess]  = useState(false);

  const handleSignUp = async (e) => {
    e.preventDefault();
    setError("");

    // ── Validations ──────────────────────────────────
    if (!name || !email || !password || !confirm) {
      setError("Please fill in all fields.");
      return;
    }
    if (name.trim().length < 2) {
      setError("Display name must be at least 2 characters.");
      return;
    }
    if (!email.includes("@") || !email.includes(".")) {
      setError("Please enter a valid email address.");
      return;
    }
    if (password.length < 6) {
      setError("Password must be at least 6 characters.");
      return;
    }
    if (password !== confirm) {
      setError("Passwords do not match.");
      return;
    }

    setLoading(true);
    const { error } = await signUpWithEmail(email, password, name);

    if (error) {
      // Map Supabase errors to friendly messages
      if (error.message.includes("User already registered")) {
        setError("An account with this email already exists. Try signing in.");
      } else if (error.message.includes("Password should be")) {
        setError("Password is too weak. Use at least 6 characters.");
      } else {
        setError(error.message);
      }
    } else {
      setSuccess(true);
    }
    setLoading(false);
  };

  // ── Success screen ────────────────────────────────
  if (success) {
    return (
      <div className="signin-page">
        <nav className="signin-nav">
          <div className="signin-logo">
            <div className="logo-icon">
              <img width="20" height="20" src={Logo} alt="logo-icon" />
            </div>
            <span>DocQ</span>
          </div>
        </nav>

        <main className="signin-main">
          <div className="signin-card">
            <div className="success-icon">
              <svg
                width="48"
                height="48"
                viewBox="0 0 24 24"
                fill="none"
                stroke="#14b8a6"
                strokeWidth="2"
                strokeLinecap="round"
              >
                <circle cx="12" cy="12" r="10" />
                <polyline points="20 6 9 17 4 12" />
              </svg>
            </div>
            <h1 className="signin-title">Check your email</h1>
            <p className="signin-subtitle">
              We sent a confirmation link to:
            </p>
            <p className="success-email">{email}</p>
            <p className="signin-note">
              Click the link in the email to activate your account, then come
              back and sign in.
            </p>
            <button
              className="continue-btn"
              onClick={() => navigate("/")}
            >
              Go to Sign In
            </button>
            <p className="switch-auth">
              Wrong email?{" "}
              <button
                type="button"
                className="switch-auth-link"
                onClick={() => {
                  setSuccess(false);
                  setEmail("");
                  setPassword("");
                  setConfirm("");
                  setName("");
                }}
              >
                Try again
              </button>
            </p>
          </div>
        </main>
      </div>
    );
  }

  // ── Sign up form ──────────────────────────────────
  return (
    <div className="signin-page">

      {/* ── Nav ── */}
      <nav className="signin-nav">
        <div className="signin-logo">
          <div className="logo-icon">
            <img width="20" height="20" src={Logo} alt="logo-icon" />
          </div>
          <span>DocQ</span>
        </div>
        <button className="nav-signin-btn" onClick={() => navigate("/")}>
          Sign In
        </button>
      </nav>

      {/* ── Card ── */}
      <main className="signin-main">
        <div className="signin-card">

          <div className="card-logo">
            <div className="logo-icon large">
              <img src={Logo} alt="logo-icon" />
            </div>
          </div>

          <h1 className="signin-title">Sign Up for DocQ</h1>
          <p className="signin-subtitle">Ask your documents anything</p>
          <p className="signin-note">
            Sign up for <strong>AI For Verticals</strong>, maker of
            docAnalyzer.
          </p>

          {/* ── Form ── */}
          <form onSubmit={handleSignUp} noValidate>

            {/* Display name */}
            <div className="form-field">
              <label className="email-label">
                Display Name <span className="required">*</span>
              </label>
              <input
                type="text"
                className={`email-input${error && !name ? " input-error" : ""}`}
                placeholder="xxTxxSKULLxx"
                value={name}
                onChange={(e) => { setName(e.target.value); setError(""); }}
                disabled={loading}
                autoComplete="name"
              />
            </div>

            {/* Email */}
            <div className="form-field">
              <label className="email-label">
                Email <span className="required">*</span>
              </label>
              <input
                type="email"
                className={`email-input${error && !email ? " input-error" : ""}`}
                placeholder="you@example.com"
                value={email}
                onChange={(e) => { setEmail(e.target.value); setError(""); }}
                disabled={loading}
                autoComplete="email"
              />
            </div>

            {/* Password */}
            <div className="form-field">
              <label className="email-label">
                Create Password <span className="required">*</span>
              </label>
              <input
                type="password"
                className={`email-input${error && !password ? " input-error" : ""}`}
                placeholder="Min. 6 characters"
                value={password}
                onChange={(e) => { setPassword(e.target.value); setError(""); }}
                disabled={loading}
                autoComplete="new-password"
              />
            </div>

            {/* Confirm password */}
            <div className="form-field">
              <label className="email-label">
                Re-enter Password <span className="required">*</span>
              </label>
              <input
                type="password"
                className={`email-input${error && password !== confirm ? " input-error" : ""}`}
                placeholder="Re-enter your password"
                value={confirm}
                onChange={(e) => { setConfirm(e.target.value); setError(""); }}
                disabled={loading}
                autoComplete="new-password"
              />
            </div>

            {/* Password match indicator */}
            {password && confirm && (
              <p className={`password-match ${password === confirm ? "match-ok" : "match-fail"}`}>
                {password === confirm ? "✓ Passwords match" : "✗ Passwords do not match"}
              </p>
            )}

            {/* Error box */}
            {error && (
              <div className="error-box">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <circle cx="12" cy="12" r="10" />
                  <line x1="12" y1="8" x2="12" y2="12" />
                  <line x1="12" y1="16" x2="12.01" y2="16" />
                </svg>
                {error}
              </div>
            )}

            {/* Submit */}
            <button
              type="submit"
              className="continue-btn"
              disabled={loading}
            >
              {loading ? (
                <span className="btn-loading">
                  <span className="signin-spinner" />
                  Creating account…
                </span>
              ) : (
                "Create account"
              )}
            </button>

            {/* Switch to sign in */}
            <p className="switch-auth">
              Already have an account?{" "}
              <button
                type="button"
                className="switch-auth-link"
                onClick={() => navigate("/")}
              >
                Sign in
              </button>
            </p>

          </form>

          <div className="signin-footer">
            <a href="#">Privacy</a>
            <span>·</span>
            <a href="#">Terms</a>
          </div>
        </div>
      </main>
    </div>
  );
}

export default SignUp;
