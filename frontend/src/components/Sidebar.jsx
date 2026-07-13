import { NavLink } from "react-router-dom";
import { ShieldCheck } from "lucide-react";
import { NAV_ITEMS } from "../utils/constants";

export default function Sidebar() {
  return (
    <aside className="hidden w-64 flex-shrink-0 flex-col bg-brand-900 text-white md:flex">
      <div className="flex items-center gap-2 px-6 py-5 border-b border-white/10">
        <ShieldCheck className="h-7 w-7 text-brand-100" />
        <div>
          <div className="text-lg font-bold leading-tight">DefaultSense</div>
          <div className="text-xs text-brand-100/70">AI Risk Intelligence</div>
        </div>
      </div>

      <nav className="flex-1 space-y-1 px-3 py-4">
        {NAV_ITEMS.map(({ label, path, icon: Icon }) => (
          <NavLink
            key={path}
            to={path}
            className={({ isActive }) =>
              [
                "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors",
                isActive
                  ? "bg-white/15 text-white"
                  : "text-brand-100/80 hover:bg-white/10 hover:text-white",
              ].join(" ")
            }
          >
            <Icon className="h-5 w-5" />
            {label}
          </NavLink>
        ))}
      </nav>

      <div className="px-6 py-4 text-xs text-brand-100/50 border-t border-white/10">
        Phase 3 · Shell
      </div>
    </aside>
  );
}
