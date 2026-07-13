import { Navigate, useLocation } from "react-router-dom";
import { useAuthStore } from "../store/authStore";

// Gate for authenticated routes. Redirects to /login, remembering the target.
export default function ProtectedRoute({ children }) {
  const token = useAuthStore((s) => s.token);
  const location = useLocation();

  if (!token) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }
  return children;
}
