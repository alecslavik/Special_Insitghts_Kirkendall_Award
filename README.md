
# SmartIEP Prototype

## Overview
This is a lightweight prototype of **SmartIEP**, a privacy-first AI-assisted IEP and behavior tracking web app intended to run on a school's local server (FERPA-friendly architecture).

The prototype demonstrates:
- Local SQLite storage
- Alias-based student records
- Behavior logging
- A simple rule-based "IEP draft" generator and a basic risk prediction endpoint
- Clear code comments where you can plug in real ML models or a local LLM

## Run locally (recommended)
1. Create a Python virtual environment and activate it.
2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Initialize and run the app:
   ```bash
   export FLASK_APP=app.py       # Windows: set FLASK_APP=app.py
   flask run --host=0.0.0.0 --port=5000
   ```
4. Open http://127.0.0.1:5000 in your browser.

## Notes for extension
- Replace `generate_iep` logic with a locally-hosted model or secure LLM running within district infrastructure.
- Add authentication and role-based access (teachers, admins).
- Consider Dockerizing for easy deployment on school servers.
- Add encryption at rest (SQLite -> encrypted DB) for production deployments.

## Files in this prototype
- `app.py` — Flask application (backend + simple UI templates)
- `templates/` — HTML templates for index, student, and IEP
- `smartiep.db` — created at runtime (not included in repo)
- `requirements.txt`, `README.md`

This prototype is intentionally simple for rapid demonstration and iteration.
