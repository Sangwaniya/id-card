# Remote Agent Directives - ID Card Studio

This document instructs autonomous AI agents (such as Antigravity CLI `agy`) working in this repository.

## 1. Architecture & Source of Truth

- **Single Source of Truth**: `build_app.py` contains the master application template and compiles into `index.html` and `id-card-generator.html`.
- **Do NOT manually modify `index.html` directly**: Any permanent UI or logic changes must be made in `build_app.py`, followed by compiling.
- **Assets**: `template_front.jpg` and `template_back.jpg` are loaded and converted to Base64 in `build_app.py`. The resulting HTML files are completely standalone and offline.

## 2. Verification Protocol

After making any changes to files in this repository:
1. Run `python3 build_app.py` (or `python build_app.py` on Windows).
2. Ensure it exits with code 0 and reports `Generated index.html and id-card-generator.html`.
3. Check `git status` to ensure only expected files are updated.

## 3. Git Discipline for Autonomous Runs

- When working on a feature or bugfix, create and switch to a descriptive branch (e.g. `agent/add-feature-x`).
- Keep commits focused and atomic with descriptive commit messages.
- Never force-push to `main`.
