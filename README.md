# Exam Preparation Planner 🎓

A beginner-friendly student planner web app built with Python Flask, SQLite, HTML, and CSS.

## Features
- Add study tasks with subject, topic, target date, and priority
- Mark tasks complete or incomplete
- Delete individual tasks or clear all completed tasks
- Dashboard statistics for tasks, completed work, subjects, and progress
- SQLite database stores tasks between app restarts
- Responsive desktop/mobile layout
- Sample tasks are added on first launch

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this project folder.
3. Optional virtual environment: `python -m venv .venv`
   - Windows activation: `.venv\\Scripts\\activate`
   - macOS/Linux activation: `source .venv/bin/activate`
4. Install packages: `pip install -r requirements.txt`
5. Run: `python app.py`
6. Open http://127.0.0.1:5000 in your browser.

The `planner.db` database is created automatically.

## Project structure
```
exam_preparation_planner/
├── app.py
├── requirements.txt
├── README.md
├── templates/index.html
└── static/style.css
```

## SaaS learning note
This is a local learning prototype with a SaaS-style dashboard. A production multi-user SaaS should add secure authentication, user-specific data isolation, deployment configuration, and backups. Do not use Flask's debug server for public production hosting.
