from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime
from ai_module import generate_iep, risk_assessment

app = Flask(__name__)
app.secret_key = "SPECIAL_INSIGHTS_SECRET"  # For sessions – replace later with environment variable

# --- Database Helper ---
def get_db():
    conn = sqlite3.connect("database/special_insights.db")
    conn.row_factory = sqlite3.Row
    return conn

# --- Auth Pages (Login / Logout) ---
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM teachers WHERE username=? AND password=?", (username, password))
        teacher = cur.fetchone()

        if teacher:
            session["teacher_id"] = teacher["id"]
            return redirect("/dashboard")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# --- Dashboard ---
@app.route("/dashboard")
def dashboard():
    if "teacher_id" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    return render_template("dashboard.html", students=students)


# --- Students Page ---
@app.route("/students", methods=["GET", "POST"])
def students():
    if "teacher_id" not in session:
        return redirect("/login")

    conn = get_db()
    if request.method == "POST":
        alias = request.form["alias"]
        conn.execute("INSERT INTO students (alias) VALUES (?)", (alias,))
        conn.commit()

    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    return render_template("students.html", students=students)


# --- Single Student Page ---
@app.route("/student/<int:student_id>")
def student_page(student_id):
    if "teacher_id" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()

    # student info
    cur.execute("SELECT * FROM students WHERE id=?", (student_id,))
    student = cur.fetchone()

    # behavior logs
    cur.execute("SELECT * FROM behavior WHERE student_id=? ORDER BY timestamp DESC", (student_id,))
    logs = cur.fetchall()

    # risk score
    risk = risk_assessment(logs)

    return render_template("student.html", student=student, logs=logs, risk=risk)


# --- Log Behavior ---
@app.route("/log_behavior", methods=["POST"])
def log_behavior():
    if "teacher_id" not in session:
        return redirect("/login")

    student_id = request.form["student_id"]
    behavior = request.form["behavior"]
    timestamp = datetime.now().isoformat()

    conn = get_db()
    conn.execute("INSERT INTO behavior (student_id, action, timestamp) VALUES (?, ?, ?)",
                 (student_id, behavior, timestamp))
    conn.commit()

    return redirect(f"/student/{student_id}")


# --- IEP Generator ---
@app.route("/student/<int:student_id>/iep")
def iep(student_id):
    if "teacher_id" not in session:
        return redirect("/login")

    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM behavior WHERE student_id=?", (student_id,))
    logs = cur.fetchall()

    iep_text = generate_iep(logs)

    return render_template("iep.html", iep=iep_text, student_id=student_id)


# --- Run App ---
if __name__ == "__main__":
    app.run(debug=True)
