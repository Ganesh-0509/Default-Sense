# Deploying DefaultSense AI to Railway

This gets you a **public demo link** for the IDBI hackathon.

## Architecture on Railway

To keep it simple and avoid Railway's IPv6-only private networking, we run everything
over public HTTPS + managed connections:

| Piece      | Where it runs                        | Gives you                          |
| ---------- | ------------------------------------ | ---------------------------------- |
| PostgreSQL | Railway **managed Postgres** (free)  | `DATABASE_URL`                     |
| Neo4j      | **Neo4j AuraDB** free tier (external)| `neo4j+s://...` URI                |
| Backend    | Railway service (Docker), **public** | `https://<backend>.up.railway.app` |
| Frontend   | Railway service (Docker), **public** | `https://<frontend>.up.railway.app` ← **your demo link** |

The frontend calls the backend's public URL directly; the backend's CORS is opened to the
frontend URL. No private networking needed.

---

## Step 0 — Push the repo (Railway builds from GitHub)

Railway deploys from your GitHub repo, so the latest commit must be pushed first. This repo
already has the one change needed (`docker/frontend.Dockerfile` accepts a `VITE_API_URL`
build arg). From the project root:

```bash
git add docker/frontend.Dockerfile DEPLOY_RAILWAY.md
git commit -m "Add Railway deploy config (frontend VITE_API_URL build arg)"
git push origin main
```

---

## Step 1 — Neo4j AuraDB (2 min)

1. Go to https://console.neo4j.io → **New Instance** → **AuraDB Free**.
2. When it finishes, **download the credentials file** (you only see the password once).
3. Note these — you'll paste them into the backend:
   - `NEO4J_URI`  = `neo4j+s://xxxxxxxx.databases.neo4j.io`
   - `NEO4J_USERNAME` = `neo4j`
   - `NEO4J_PASSWORD` = (from the file)

---

## Step 2 — Create the Railway project + Postgres (2 min)

1. Go to https://railway.app → **New Project** → **Deploy from GitHub repo** → pick
   `Ganesh-0509/Default-Sense`.
2. In the project, click **+ New** → **Database** → **Add PostgreSQL**. Railway provisions it
   and exposes a `DATABASE_URL` variable you'll reference from the backend.

---

## Step 3 — Backend service (5 min)

Railway may auto-create a service from the repo. Configure it as the **backend**:

1. **Point Railway at the Dockerfile** (critical — otherwise Railway uses its auto-detect
   builder "Railpack" and fails with *"could not determine how to build the app"*, because the
   Dockerfiles live under `docker/`, not the repo root). Easiest: add a service **Variable**
   ```
   RAILWAY_DOCKERFILE_PATH=docker/backend.Dockerfile
   ```
   (Equivalent UI path: **Settings → Build → Builder = Dockerfile**, then **Dockerfile Path =
   `docker/backend.Dockerfile`**.) Leave **Root Directory** as `/` — the Dockerfile copies
   `backend/`, `models/`, `database/` relative to the repo root.
2. **Settings → Networking → Generate Domain** → set **target port `8000`**.
   Copy the generated URL, e.g. `https://defaultsense-backend.up.railway.app`.
3. **Variables** (Raw Editor — paste and edit):
   ```
   RAILWAY_DOCKERFILE_PATH=docker/backend.Dockerfile
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   NEO4J_URI=neo4j+s://xxxxxxxx.databases.neo4j.io
   NEO4J_USERNAME=neo4j
   NEO4J_PASSWORD=your-aura-password
   JWT_SECRET=<paste a long random string>
   FRONTEND_URL=https://PLACEHOLDER-set-in-step-5
   ```
   - `${{Postgres.DATABASE_URL}}` is a Railway reference — it auto-fills from the Postgres plugin.
   - Generate a `JWT_SECRET` with: `python -c "import secrets; print(secrets.token_urlsafe(48))"`
4. **Deploy.** First boot runs `init_all` — it creates the Postgres schema, seeds Postgres +
   Neo4j, creates the admin user, and **trains the XGBoost model** (takes ~2–4 min; watch the
   logs until you see `Starting API server`).
5. Verify: open `https://<backend>.up.railway.app/health` → should return OK. `/docs` shows the API.

---

## Step 4 — Frontend service (3 min)

1. In the project: **+ New** → **GitHub Repo** → same repo (creates a second service).
2. **Point Railway at the Dockerfile** (same reason as the backend) — add the variable in the
   next step, or **Settings → Build → Builder = Dockerfile**, **Dockerfile Path =
   `docker/frontend.Dockerfile`**. Leave **Root Directory** as `/`.
3. **Variables** — `RAILWAY_DOCKERFILE_PATH` selects the Dockerfile, `VITE_API_URL` bakes the
   backend URL into the build:
   ```
   RAILWAY_DOCKERFILE_PATH=docker/frontend.Dockerfile
   VITE_API_URL=https://<backend>.up.railway.app/api/v1
   ```
   (Railway passes service variables as Docker build args, so `ARG VITE_API_URL` in the
   Dockerfile picks it up. Note the trailing **`/api/v1`**.)
4. **Settings → Networking → Generate Domain** → target port **`80`**.
   This URL is your **public demo link**.

---

## Step 5 — Close the CORS loop

1. Copy the frontend domain from Step 4.
2. Go back to the **backend** service → **Variables** → set:
   ```
   FRONTEND_URL=https://<frontend>.up.railway.app
   ```
3. The backend redeploys automatically. Done.

---

## Step 6 — Verify the demo

Open the frontend URL and check:

- Click **"Explore the demo (for judges)"** — one-click login, no sign-up
  (seeds `demo@defaultsense.ai` / `Demo@1234`, role `risk_manager` = full
  business access). Admin login `admin@defaultsense.ai` / `ChangeMe123!` also works.
- Dashboard loads, a prediction returns a PD + SHAP explanation, reports export.

If the browser console shows CORS errors, re-check that `FRONTEND_URL` (backend) exactly
matches the frontend origin (no trailing slash), and `VITE_API_URL` (frontend) ends in `/api/v1`.

---

## Notes & gotchas

- **First boot is slow** (~2–4 min) because it trains the model. Subsequent boots reuse the
  trained model stored on the service volume, so they're fast.
- **Demo vs admin accounts:** the `demo@defaultsense.ai` account is *meant* to be public (that's
  the judges' one-click login). It's `risk_manager`, so it can create/edit business data but has no
  user-management/admin surface. The privileged **admin** account's password (`ChangeMe123!`) is
  public in this repo — override it for the deploy by setting `ADMIN_PASSWORD` as a backend variable
  before first boot. To rotate the demo password too, set `DEMO_PASSWORD` (and update the button
  default in `frontend/src/pages/Login.jsx`).
- **Cost:** Postgres + 2 small services fit Railway's trial credit for a demo, but Railway's free
  trial is time/credit limited — check current limits. Neo4j AuraDB Free is genuinely free.
- **Alternative (no Aura):** you *can* run Neo4j as a 5th Railway service from `neo4j:5-community`,
  but then backend→Neo4j must cross Railway's private network, which is IPv6-only and requires
  extra Neo4j listen-address config. AuraDB avoids all of that — recommended for the demo.
