//import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/SignIn.css";
import Logo from "../assets/logo-icon.svg.svg";
import Google from "../assets/google-logo.svg";
import Microsoft from "../assets/microsoft-logo.svg";
import Apple from "../assets/ios-logo.svg";
import { useAuth } from "../context/AuthContext";
import { useState } from "react";

function SignIn() {
  const { signInWithGoogle, signInWithEmail } = useAuth();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // --- Google OAuth-----------
  const handleGoogle = async () => {
    setError("");
    const { error } = await signInWithGoogle();
    if (error) setError(error.message);
  };

  // ── Email + password sign in ──────────────────────
  const handleEmailSignIn = async (e) => {
    e.preventDefault();
    setError("");

    // Validation
    if (!email || !password) {
      setError("Please fill in all fields");
      setLoading(false);
      return;
    }
    if (!email.includes("@")) {
      setError("Please enter a valid email address.");
      setLoading(false);
      return;
    }

    setLoading(true);
    const { error } = await signInWithEmail(email, password);

    if (error) {
      // Make Supabase error messages more user friendly
      if (error.message.includes("Invalid login credentials")) {
        setError("Incorrect email or password. Please try again.");
      } else if (error.message.includes("Email not confirmed")) {
        setError(
          "Please verify your email before signing in. Check your inbox.",
        );
      } else {
        setError(error.message);
      }
    } else {
      navigate("/documents");
    }
    setLoading(false);
  };

  //   const handleEmailSubmit = (e) => {
  //     e.preventDefault();
  //     if (!email) return;
  //     setError("");
  //     setVerifying(true);
  //     // TODO: hook up real auth
  //    try {
  //   // TODO: replace this URL with your real auth API endpoint
  //   const res = await fetch("https://your-api.com/auth/send-otp", {
  //     method: "POST",
  //     headers: { "Content-Type": "application/json" },
  //     body: JSON.stringify({ email }),
  //   });

  //   if (!res.ok) throw new Error("Failed to send verification email.");

  //   // TODO: navigate to OTP / check-email screen
  //   console.log("Verification email sent to", email);

  // } catch (err) {
  //   setError(err.message || "Something went wrong. Please try again.");
  //   setVerifying(false);
  // }
  //   };

  return (
    <div className="signin-page">
      <nav className="signin-nav">
        <div className="signin-logo">
          <div className="logo-icon">
            <img
              width="20"
              height="20"
              viewBox=" 0 0 24 24"
              src={Logo}
              alt="logo-icon"
              fill="none"
              stroke="white"
              strokeWidth="2"
            />
          </div>
          <span>DocQ</span>
        </div>
        <button
          className="nav-signin-btn"
          onClick={() => navigate("/documents")}
        >
          Documents
        </button>
        <button className="nav-signin-btn" onClick={() => navigate("/signup")}>
          Sign Up
        </button>
      </nav>

      <main className=" signin-main">
        <div className="signin-card">
          <div className="card-logo">
            <div className="logo-icon large">
              <img
                src={Logo}
                alt="logo-icon"
                viewBox="0 0 24 24"
                fill="none"
                stroke="white"
                strokeWidth="2"
              />
            </div>
          </div>

          <h1 className="signin-title">Sign in to DocQ</h1>
          <p className="signin-subtitle">Ask your documents anything</p>
          <p className="signin-note">
            Continue via Google, Microsoft, or Apple for{" "}
            <strong>AI For Verticals</strong> , maker of docAnalyzer.
          </p>

          <div className="social-buttons">
            <button
              className="social-btn google"
              onClick={handleGoogle}
              type="button"
            >
              <img src={Google} alt="google-icon" width="18" height="18" />
              Continue with Google
            </button>
            <button className="social-btn microsoft">
              <img src={Microsoft} alt="google-icon" width="18" height="18" />
              Continue with Microsoft
            </button>
            <button className="social-btn apple">
              <img src={Apple} alt="google-icon" width="18" height="18" />
              Continue with Apple
            </button>
          </div>

          <div className="or-divider">
            <span> OR USE EMAIL</span>
          </div>

          {/* Email + Password field */}
          <form onSubmit={handleEmailSignIn} noValidate>
            {/* Email Input */}
            <div className="form-field">
              <label className="email-label">
                Email <span className="required">*</span>
              </label>
              <input
                type="email"
                className={`email-input${error ? " input-error" : ""}`}
                placeholder="you@example.com"
                value={email}
                onChange={(e) => {
                  setEmail(e.target.value);
                  setError(""); // Clear error when user types
                }}
                disabled={loading}
                autoComplete="email"
              />
            </div>

            {/* Password field */}
            <div className="form-field">
              <label className="email-label">
                Password <span className="required">*</span>
              </label>
              <input
                type="password"
                className={`email-input${error ? " input-error" : ""}`}
                placeholder="••••••••"
                value={password}
                onChange={(e) => {
                  setPassword(e.target.value);
                  setError("");
                }}
                disabled={loading}
                autoComplete="current-password"
              />
            </div>

            {/* Error message */}
            {error && (
              <div className="error-box">
                <svg
                  width="14"
                  height="14"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                >
                  <circle cx="12" cy="12" r="10" />
                  <line x1="12" y1="8" x2="12" y2="12" />
                  <line x1="12" y1="16" x2="12.01" y2="16" />
                </svg>
                {error}
              </div>
            )}

            {/* Submit button */}
            <button type="submit" className="continue-btn" disabled={loading}>
              {loading ? (
                <span className="btn-loading">
                  <span className="signin-spinner" />
                  Signing in…
                </span>
              ) : (
                "Sign in"
              )}
            </button>

            {/* Link to sign up */}
            <p className="switch-auth">
              Don't have an account?{" "}
              <button
                type="button"
                className="switch-auth-link"
                onClick={() => navigate("/signup")}
              >
                Sign up
              </button>
            </p>
          </form>

          <div className="signin-footer">
            <a href="#">Privacy</a>
            <span>.</span>
            <a href="#">Terms</a>
          </div>
        </div>
      </main>
    </div>
  );
}

export default SignIn;
