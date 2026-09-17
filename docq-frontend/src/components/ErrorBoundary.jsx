import { Component } from "react";

class ErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, info) {
    // Log to console in development
    console.error("ErrorBoundary caught:", error, info);
  }

  handleReload() {
    window.location.href = "/";
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={styles.page}>
          <div style={styles.card}>
            <div style={styles.iconWrap}>
              <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="#ef4444" strokeWidth="1.5">
                <circle cx="12" cy="12" r="10" />
                <line x1="12" y1="8" x2="12" y2="12" />
                <line x1="12" y1="16" x2="12.01" y2="16" />
              </svg>
            </div>
            <h1 style={styles.title}>Something went wrong</h1>
            <p style={styles.desc}>
              An unexpected error occurred. Your data is safe — please
              refresh the page to continue.
            </p>
            {this.state.error && (
              <details style={styles.details}>
                <summary style={styles.summary}>Error details</summary>
                <pre style={styles.pre}>
                  {this.state.error.toString()}
                </pre>
              </details>
            )}
            <button style={styles.btn} onClick={this.handleReload}>
              Go to home page
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

const styles = {
  page: {
    minHeight: "100vh",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background: "#f0f2f5",
    padding: "24px",
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
  },
  card: {
    background: "#fff",
    borderRadius: "12px",
    padding: "40px 36px",
    maxWidth: "460px",
    width: "100%",
    textAlign: "center",
    boxShadow: "0 4px 24px rgba(0,0,0,0.08)",
  },
  iconWrap: {
    marginBottom: "16px",
    display: "flex",
    justifyContent: "center",
  },
  title: {
    fontSize: "20px",
    fontWeight: "700",
    color: "#111827",
    margin: "0 0 10px",
  },
  desc: {
    fontSize: "14px",
    color: "#6b7280",
    lineHeight: "1.6",
    margin: "0 0 20px",
  },
  details: {
    textAlign: "left",
    background: "#fef2f2",
    border: "1px solid #fecaca",
    borderRadius: "8px",
    padding: "12px",
    marginBottom: "20px",
  },
  summary: {
    fontSize: "13px",
    color: "#ef4444",
    cursor: "pointer",
    fontWeight: "600",
  },
  pre: {
    fontSize: "12px",
    color: "#7f1d1d",
    marginTop: "8px",
    whiteSpace: "pre-wrap",
    wordBreak: "break-all",
  },
  btn: {
    background: "#14b8a6",
    color: "#fff",
    border: "none",
    borderRadius: "8px",
    padding: "10px 24px",
    fontSize: "14px",
    fontWeight: "600",
    cursor: "pointer",
  },
};

export default ErrorBoundary;
