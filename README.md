# Cloud AI Resume Analyzer

A student-friendly cloud project that lets users upload/paste a resume, extracts useful information, calculates a transparent rule-based ATS-style score, and compares the resume against a job description.

## Features
- Resume text input and `.txt` upload
- Job description input
- Skills extraction
- ATS-style keyword match score
- Section detection
- Resume improvement suggestions
- Responsive web UI
- Simple Flask backend
- Ready to deploy to Render/Railway or another Python cloud host

> Note: The default analyzer is intentionally rule-based and does not send resumes to an external AI service. You can later connect an LLM API in `app.py`.

## Run locally
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

## Deploy
A `Procfile` is included. Set the start command to:
`gunicorn app:app`

For production, add authentication, file-size limits, secure storage, and a real database.
