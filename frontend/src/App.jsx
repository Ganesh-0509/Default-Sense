import { Routes, Route, Navigate } from "react-router-dom";
import ProtectedRoute from "./routes/ProtectedRoute";
import DashboardLayout from "./layouts/DashboardLayout";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Customers from "./pages/Customers";
import Loans from "./pages/Loans";
import Settings from "./pages/Settings";
import PagePlaceholder from "./components/PagePlaceholder";
import NotFound from "./pages/NotFound";

export default function App() {
  return (
    <Routes>
      {/* Public */}
      <Route path="/login" element={<Login />} />

      {/* Protected — wrapped in the dashboard layout */}
      <Route
        element={
          <ProtectedRoute>
            <DashboardLayout />
          </ProtectedRoute>
        }
      >
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/customers" element={<Customers />} />
        <Route path="/loans" element={<Loans />} />
        <Route path="/settings" element={<Settings />} />
        {/* Stubs — filled in during later phases */}
        <Route path="/predictions" element={<PagePlaceholder title="AI Predictions" phase={6} />} />
        <Route path="/graph" element={<PagePlaceholder title="Knowledge Graph" phase={5} />} />
        <Route path="/documents" element={<PagePlaceholder title="Documents & OCR" phase={4} />} />
        <Route path="/reports" element={<PagePlaceholder title="Reports" phase={7} />} />
        <Route path="/alerts" element={<PagePlaceholder title="Alerts" phase={7} />} />
      </Route>

      {/* Defaults */}
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}
