import { RISK_STYLES } from "../utils/constants";

// Colored pill for a risk level (Low / Moderate / High / Critical).
export default function RiskBadge({ level }) {
  const style = RISK_STYLES[level] || { bg: "bg-slate-100", fg: "text-slate-700" };
  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold ${style.bg} ${style.fg}`}
    >
      {level || "Unknown"}
    </span>
  );
}
