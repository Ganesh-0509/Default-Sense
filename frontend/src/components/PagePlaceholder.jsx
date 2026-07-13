import { Construction } from "lucide-react";

// Consistent stub for screens delivered in later phases.
export default function PagePlaceholder({ title, phase }) {
  return (
    <div>
      <h1 className="text-2xl font-bold text-slate-800">{title}</h1>
      <div className="mt-6 flex flex-col items-center justify-center rounded-xl border border-dashed border-slate-300 bg-white py-16 text-center">
        <Construction className="h-10 w-10 text-slate-300" />
        <p className="mt-4 text-sm font-medium text-slate-500">
          {title} arrives in Phase {phase}.
        </p>
        <p className="mt-1 text-xs text-slate-400">
          The navigation, layout, and auth shell are ready now.
        </p>
      </div>
    </div>
  );
}
