import {
  LayoutDashboard,
  Users,
  Landmark,
  Brain,
  Share2,
  FileText,
  BarChart3,
  Bell,
  Settings,
} from "lucide-react";

// Sidebar navigation (docs/06 §5). `phase` marks which build phase fills it in.
export const NAV_ITEMS = [
  { label: "Dashboard", path: "/dashboard", icon: LayoutDashboard, phase: 3 },
  { label: "Customers", path: "/customers", icon: Users, phase: 3 },
  { label: "Loans", path: "/loans", icon: Landmark, phase: 3 },
  { label: "Predictions", path: "/predictions", icon: Brain, phase: 6 },
  { label: "Knowledge Graph", path: "/graph", icon: Share2, phase: 5 },
  { label: "Documents", path: "/documents", icon: FileText, phase: 4 },
  { label: "Reports", path: "/reports", icon: BarChart3, phase: 7 },
  { label: "Alerts", path: "/alerts", icon: Bell, phase: 7 },
  { label: "Settings", path: "/settings", icon: Settings, phase: 3 },
];

// Risk color system (docs/06 §12)
export const RISK_STYLES = {
  Low: { text: "text-risk-low", bg: "bg-green-100", fg: "text-green-800" },
  Moderate: { text: "text-risk-moderate", bg: "bg-yellow-100", fg: "text-yellow-800" },
  High: { text: "text-risk-high", bg: "bg-orange-100", fg: "text-orange-800" },
  Critical: { text: "text-risk-critical", bg: "bg-red-100", fg: "text-red-800" },
};
