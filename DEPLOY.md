Deployment guide — GitHub -> Render

Overview
- This repository contains the web-ready app under `web/`.
- `web/requirements.txt` lists `Flask` and `gunicorn`.
- `Procfile` and `render.yaml` are configured for Render.

Steps to publish on GitHub
1. Create a new GitHub repository (do not initialize with README/license). Copy its clone URL (HTTPS or SSH).
2. From the project root run (PowerShell):

   # set remote and push (replace <REMOTE_URL>)
   .\scripts\push_to_github.ps1 -RemoteUrl '<REMOTE_URL>'

3. Verify your repository on GitHub shows the `main` branch and files including `web/`, `Procfile`, and `render.yaml`.

Connect to Render
1. In Render dashboard, click "New" → "Web Service".
2. Choose "Connect a repository" and select your GitHub repository.
3. Configure: branch `main`, root directory `.` (or leave default), and the following build & start commands are already in `render.yaml`:
   - Build command: `pip install -r web/requirements.txt`
   - Start command: `gunicorn web.app:app --bind 0.0.0.0:$PORT`
4. Enable "Auto deploy" if you want Render to redeploy on new commits.
5. Click Create. Render will run a build and deploy.

Notes & troubleshooting
- If your app fails on Render, open the service page → Activity to see build and deploy logs.
- If images are missing, confirm they are under `web/static/images/` and the frontend uses `/static-files/...` (the Flask app maps that route).
- To preserve in-memory game state on Render avoid scaling to multiple workers; `Procfile` uses `--workers 1`.

Optional: use the GitHub CLI (gh)
- If you have `gh` installed you can create a repo from terminal: `gh repo create <name> --public --source=. --remote=origin --push`.

If you'd like, I can:
- Run the `push_to_github.ps1` for you if you provide the GitHub repo URL (or run it locally for you), or
- Walk through the Render dashboard screen-by-screen.
