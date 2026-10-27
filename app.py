from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB_PATH = Path(__file__).with_name('planner.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            topic TEXT NOT NULL,
            exam_date TEXT NOT NULL,
            priority TEXT NOT NULL DEFAULT 'Medium',
            done INTEGER NOT NULL DEFAULT 0
        )''')
        if conn.execute('SELECT COUNT(*) FROM tasks').fetchone()[0] == 0:
            conn.executemany('INSERT INTO tasks (subject, topic, exam_date, priority, done) VALUES (?, ?, ?, ?, ?)', [
                ('Mathematics', 'Revise algebra', '2026-11-02', 'High', 0),
                ('Science', 'Review force and motion', '2026-11-04', 'Medium', 0),
                ('English', 'Practice grammar', '2026-11-06', 'Low', 1),
            ])

@app.route('/')
def index():
    with get_db() as conn:
        tasks = conn.execute('SELECT * FROM tasks ORDER BY done ASC, exam_date ASC').fetchall()
    total = len(tasks)
    completed = sum(task['done'] for task in tasks)
    subjects = len(set(task['subject'] for task in tasks))
    progress = round(completed / total * 100) if total else 0
    return render_template('index.html', tasks=tasks, total=total, completed=completed, subjects=subjects, progress=progress)

@app.route('/add', methods=['POST'])
def add_task():
    subject = request.form.get('subject', '').strip()
    topic = request.form.get('topic', '').strip()
    exam_date = request.form.get('exam_date', '').strip()
    priority = request.form.get('priority', 'Medium')
    if subject and topic and exam_date:
        if priority not in ('Low', 'Medium', 'High'):
            priority = 'Medium'
        with get_db() as conn:
            conn.execute('INSERT INTO tasks (subject, topic, exam_date, priority) VALUES (?, ?, ?, ?)', (subject, topic, exam_date, priority))
    return redirect(url_for('index'))

@app.route('/toggle/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    with get_db() as conn:
        conn.execute('UPDATE tasks SET done = CASE done WHEN 0 THEN 1 ELSE 0 END WHERE id = ?', (task_id,))
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    with get_db() as conn:
        conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    return redirect(url_for('index'))

@app.route('/clear-completed', methods=['POST'])
def clear_completed():
    with get_db() as conn:
        conn.execute('DELETE FROM tasks WHERE done = 1')
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
