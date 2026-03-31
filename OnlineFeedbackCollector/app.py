from flask import Flask, request, jsonify, render_template, redirect, url_for, session, send_file
import sqlite3
import os
import csv
import io
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = "feedbacksecretkey2024"

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


# ─── DB Setup ───────────────────────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                name          TEXT    NOT NULL,
                email         TEXT    NOT NULL,
                rating        INTEGER NOT NULL CHECK(rating BETWEEN 1 AND 5),
                comments      TEXT,
                date_submitted TEXT   NOT NULL
            )
        """)
        conn.commit()


# ─── Auth helper ────────────────────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated


# ─── Public Routes ──────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit-feedback", methods=["POST"])
def submit_feedback():
    data = request.get_json() if request.is_json else request.form
    name     = (data.get("name") or "").strip()
    email    = (data.get("email") or "").strip()
    rating   = data.get("rating")
    comments = (data.get("comments") or "").strip()

    errors = []
    if not name:
        errors.append("Name is required.")
    if not email or "@" not in email:
        errors.append("Valid email is required.")
    try:
        rating = int(rating)
        if not 1 <= rating <= 5:
            raise ValueError
    except (TypeError, ValueError):
        errors.append("Rating must be between 1 and 5.")

    if errors:
        if request.is_json:
            return jsonify({"success": False, "errors": errors}), 400
        return render_template("index.html", errors=errors, form_data=data)

    date_submitted = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_db() as conn:
        conn.execute(
            "INSERT INTO feedback (name, email, rating, comments, date_submitted) VALUES (?,?,?,?,?)",
            (name, email, rating, comments, date_submitted)
        )
        conn.commit()

    if request.is_json:
        return jsonify({"success": True, "message": "Feedback submitted successfully!"})
    return render_template("index.html", success=True)


# ─── Admin Auth ─────────────────────────────────────────────────────────────

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin_dashboard"))
        error = "Invalid credentials. Try admin / admin123"
    return render_template("login.html", error=error)


@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))


# ─── Admin Dashboard ────────────────────────────────────────────────────────

@app.route("/admin-dashboard")
@login_required
def admin_dashboard():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM feedback ORDER BY date_submitted DESC"
        ).fetchall()

    entries   = [dict(r) for r in rows]
    total     = len(entries)
    avg_rating = round(sum(e["rating"] for e in entries) / total, 2) if total else 0

    rating_counts = {i: 0 for i in range(1, 6)}
    for e in entries:
        rating_counts[e["rating"]] += 1

    return render_template(
        "admin.html",
        entries=entries,
        total=total,
        avg_rating=avg_rating,
        rating_counts=rating_counts,
    )


# ─── REST API ────────────────────────────────────────────────────────────────

@app.route("/api/feedback")
@login_required
def api_feedback():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM feedback ORDER BY date_submitted DESC").fetchall()
    return jsonify([dict(r) for r in rows])


# ─── CSV Export ─────────────────────────────────────────────────────────────

@app.route("/admin/export-csv")
@login_required
def export_csv():
    with get_db() as conn:
        rows = conn.execute("SELECT * FROM feedback ORDER BY date_submitted DESC").fetchall()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Name", "Email", "Rating", "Comments", "Date Submitted"])
    for r in rows:
        writer.writerow([r["id"], r["name"], r["email"], r["rating"], r["comments"], r["date_submitted"]])

    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="feedback_export.csv"
    )


# ─── Entry Point ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
