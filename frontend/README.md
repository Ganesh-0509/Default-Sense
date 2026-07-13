# DefaultSense AI — Frontend (Phase 3)

React + Vite SPA shell: routing, protected dashboard layout, and the authentication
screens. Design source: [`docs/06_Frontend_UI_UX.md`](../docs/06_Frontend_UI_UX.md).

## What's in the shell (Phase 3)

- **Auth**: Login page → calls the Phase 2 backend, stores the JWT (Zustand + localStorage),
  Settings page with a working change-password form, logout.
- **Routing**: `react-router-dom` with a `ProtectedRoute` guard; unauthenticated users are
  redirected to `/login` (remembering their target).
- **Layout**: fixed Sidebar + top Navbar + routed content (`DashboardLayout`).
- **Live pages**: Dashboard (KPIs from `/customers` + `/loans`), Customers list, Loans list —
  each handling loading, error, and empty states.
- **Stubs**: Predictions, Knowledge Graph, Documents, Reports, Alerts — routed placeholders
  that name the phase that fills them in.
- **API client**: Axios instance with a JWT request interceptor and a 401 → logout interceptor.
- **Design tokens**: Tailwind with the risk color system (Low/Moderate/High/Critical/Info).

## Structure

```
frontend/src/
├── main.jsx / App.jsx        # entry + route table
├── routes/ProtectedRoute.jsx # auth guard
├── layouts/DashboardLayout   # sidebar + navbar shell
├── components/               # Sidebar, Navbar, KpiCard, RiskBadge, PagePlaceholder
├── pages/                    # Login, Dashboard, Customers, Loans, Settings, NotFound
├── services/                 # api (axios), authService, dataService
├── store/authStore.js        # Zustand auth state (persisted)
└── utils/constants.js        # nav items + risk styles
```

## Run

Prerequisite: backend running on `:8000` (Phase 2) with databases up (Phase 1).

```bash
cd frontend
npm install
npm run dev        # http://localhost:5173  (proxies /api → :8000)
```

Build for production:

```bash
npm run build && npm run preview
```

## Default login

`admin@defaultsense.ai` / `ChangeMe123!` (set via `backend`'s `seed_admin` script).
