# 📋 Online Feedback Collector with Admin Dashboard

A full-stack Flask web application that collects user feedback and displays analytics in an admin dashboard.

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
python app.py
```

### 3. Open in browser
```
http://127.0.0.1:5000/
```

---

## 🔐 Admin Login
Go to `http://127.0.0.1:5000/admin/login`

| Field    | Value      |
|----------|------------|
| Username | `admin`    |
| Password | `admin123` |

---

## 📁 Project Structure

```
OnlineFeedbackCollector/
├── app.py               # Flask backend (routes, DB, auth)
├── requirements.txt     # Python dependencies
├── database.db          # SQLite DB (auto-created on first run)
├── README.md
├── static/
│   ├── css/style.css    # Dark-theme stylesheet
│   └── js/script.js     # Star rating + AJAX form submit
└── templates/
    ├── layout.html      # Base template (navbar, footer)
    ├── index.html       # Feedback form page
    ├── admin.html       # Admin dashboard with charts
    └── login.html       # Admin login page
```

---

## 🛠️ Features

### User Side
- Responsive feedback form (name, email, 1–5 star rating, comments)
- Client-side validation with friendly error messages
- AJAX submit (no page reload) with success animation

### Admin Dashboard
- Login-protected (`/admin/login`)
- Summary stats: total responses, average rating, positive/negative counts
- Bar chart (rating distribution) + Doughnut chart (sentiment)
- Searchable feedback table
- One-click CSV export (`/admin/export-csv`)

### REST API
- `GET /api/feedback` — Returns all feedback as JSON (login required)

---

## 📦 Tech Stack

| Layer    | Technology             |
|----------|------------------------|
| Frontend | HTML, CSS, JavaScript  |
| Backend  | Python + Flask         |
| Database | SQLite                 |
| Charts   | Chart.js (CDN)         |
| Fonts    | Google Fonts (DM Sans) |

---

## 🎓 Learning Outcomes

- Full-stack request flow (form → Flask → SQLite → response)
- Flask routing, Jinja2 templating, session-based auth
- CRUD operations with SQLite
- Chart.js data visualization
- CSV export with Python's `csv` module
- Responsive dark-theme UI design
