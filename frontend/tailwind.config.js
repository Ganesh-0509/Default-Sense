/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        // Risk color system (docs/06 §12)
        risk: {
          low: "#16a34a", // green
          moderate: "#eab308", // yellow
          high: "#f97316", // orange
          critical: "#dc2626", // red
          info: "#2563eb", // blue
        },
        brand: {
          50: "#eef4ff",
          100: "#d9e6ff",
          500: "#2563eb",
          600: "#1d4ed8",
          700: "#1e40af",
          900: "#172554",
        },
      },
    },
  },
  plugins: [],
};
