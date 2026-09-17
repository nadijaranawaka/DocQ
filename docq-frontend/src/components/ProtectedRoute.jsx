import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function ProtectedRoute() {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          height: "100vh",
          background: "#f0f2f5",
          fontSize: "14px",
          color: "#9ca3af",
        }}
      >
        Loading…
      </div>
    );
  }

  return user ? <Outlet /> : <Navigate to="/" replace />;
}

export default ProtectedRoute;
