# Deploying this project to Render

This repository includes a ready-to-use `render.yaml` manifest and a small Flask web app under `web/` so you can deploy to Render quickly.

What the manifest does
- `render.yaml` defines a single web service that installs `web/requirements.txt` and starts the app using Gunicorn:
  - Build: `pip install -r web/requirements.txt`
  - Start: `gunicorn web.app:app --bind 0.0.0.0:$PORT`

Pre-deployment checklist
- `render.yaml` is present at repository root. ✅
- `web/requirements.txt` exists and includes `Flask` and `gunicorn`. ✅
- `web/app.py` exists and exposes `app` (Flask app). ✅
- `web/templates/` exists and contains `index.html`. ✅
- Static assets: by default this project serves images from `assets/` at `/assets/...`.
  - Option A (recommended): create `web/static/` and copy `assets/` into it so the standard Flask layout is used.
  - Option B: leave `assets/` in repo root (current code serves them via `/assets/<path>`). Both work, but `web/static/` is conventional.

Optional: pin Python version
- If you want a specific Python runtime on Render, add a `runtime.txt` (e.g. `python-3.11.4`) in repo root.

How to deploy (recommended, using the manifest)
1. Push your repo to GitHub (or your Git provider). See the exact `git` commands in the project README or run:

```bash
git init
git add .
git commit -m "Prepare project for Render deployment"
git remote add origin https://github.com/Aditya452255/Chess-Game-with-python.git
git branch -M main
git push -u origin main
```

2. On Render:
  - Create a new service by importing the repo and choose the `render.yaml` option (Render will read the manifest).
  - Or create a new Web Service and set:
    - Build Command: `pip install -r web/requirements.txt`
    - Start Command: `gunicorn web.app:app --bind 0.0.0.0:$PORT`

3. After deployment, open the service URL. The UI is at `/` and the backend API endpoints are under `/api/*`.

Local testing before push
1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r web/requirements.txt
python web/app.py
```

2. Visit `http://127.0.0.1:5000` and verify the game loads and images appear.

Troubleshooting
- If images do not show, ensure the `assets/` folder is deployed and the `/assets/...` URLs match where files are stored.
- If your start command fails on Render, check the build logs and make sure `gunicorn` is installed (it is in `web/requirements.txt`).
- For multi-user or persistent games: the server currently holds game state in memory. Add a persistent store (Redis/Postgres) for production.

Security & production notes
- Consider adding rate-limiting, input validation, and authentication if you make the app public.
- Signing or scanning the desktop executables is separate from web deployment.

If you want, I can:
- Add a `web/static/` copy of `assets/` and a small commit so the standard Flask layout is used.
- Create a `runtime.txt` pin for Python on Render.
- Prepare a `Dockerfile` instead of using `render.yaml`.

---
Rendered by the project assistant. Follow the checklist above and push your repo; Render will deploy automatically using `render.yaml`.
