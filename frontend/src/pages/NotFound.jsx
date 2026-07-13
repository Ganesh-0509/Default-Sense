import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-slate-50 text-center">
      <div className="text-6xl font-bold text-brand-600">404</div>
      <p className="mt-2 text-slate-500">This page does not exist.</p>
      <Link
        to="/dashboard"
        className="mt-6 rounded-lg bg-brand-600 px-4 py-2 text-sm font-semibold text-white hover:bg-brand-700"
      >
        Back to Dashboard
      </Link>
    </div>
  );
}
