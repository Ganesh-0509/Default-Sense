import { useNavigate } from "react-router-dom";
import { LogOut, UserCircle } from "lucide-react";
import { useAuthStore } from "../store/authStore";

export default function Navbar() {
  const navigate = useNavigate();
  const user = useAuthStore((s) => s.user);
  const logout = useAuthStore((s) => s.logout);

  const handleLogout = () => {
    logout();
    navigate("/login", { replace: true });
  };

  return (
    <header className="flex items-center justify-between border-b border-slate-200 bg-white px-6 py-3">
      <div className="text-sm text-slate-500">
        Loan Default Prediction &amp; Decision Intelligence
      </div>

      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 text-sm">
          <UserCircle className="h-6 w-6 text-slate-400" />
          <div className="hidden sm:block">
            <div className="font-medium text-slate-800">{user?.full_name || "User"}</div>
            <div className="text-xs capitalize text-slate-400">
              {user?.role?.replace("_", " ") || ""}
            </div>
          </div>
        </div>
        <button
          onClick={handleLogout}
          className="flex items-center gap-1.5 rounded-lg border border-slate-200 px-3 py-1.5 text-sm font-medium text-slate-600 transition-colors hover:bg-slate-50"
        >
          <LogOut className="h-4 w-4" />
          Logout
        </button>
      </div>
    </header>
  );
}
