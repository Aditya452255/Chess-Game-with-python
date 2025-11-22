# Game Instructions

* Working on AI gamemode...

- Entry point: main.py
- Press 't' to change theme (green, brown, blue, gray)
- Press 'r' to restart the game

# Game Snapshots

## Snapshot 1 - Start (green)
![snapshot1](snapshots/snapshot1.png)

## Snapshot 2 - Start (brown)
![snapshot2](snapshots/snapshot2.png)

## Snapshot 3 - Start (blue)
![snapshot3](snapshots/snapshot3.png)

## Snapshot 4 - Start (gray)
![snapshot4](snapshots/snapshot4.png)

## Snapshot 5 - Valid Moves
![snapshot5](snapshots/snapshot5.png)

## Snapshot 6 - Castling
![snapshot6](snapshots/snapshot6.png)

## Build (Windows)

- A simple double-click build script is included: `build.bat`.
- This script installs `pyinstaller` in your configured conda environment, builds a one-folder distributable (`--onedir`) for `src/main.py`, includes the `assets/` folder, and creates `dist/Chess-python-dist.zip`.
- To run the build from PowerShell or by double-clicking, open the project folder and run:

```powershell
.\build.bat
```

- If your Conda/Python is installed in a different location, edit the `CONDA_EXE` and `CONDA_PREFIX_ARGS` variables at the top of `build.bat` (or run `build.ps1` which uses the same pattern).
- After the build completes you can distribute the `dist\main` folder (or `dist\Chess-python-dist.zip`) to other Windows machines — `main.exe` runs without installing Python.

Notes:
- Keep the `assets/` folder next to the executable (the build script bundles it into the distributable).
- If you prefer a single `.exe` instead of a folder, rerun PyInstaller with the `--onefile` flag (modify `build.bat` accordingly).

## Preview

Here is a quick preview of the running game (captured from the built executable):

![screenshot](screenshot.png)

