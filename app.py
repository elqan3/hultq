from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# =========================
# Database Configuration
# =========================
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# =========================
# Database Model
# =========================
class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

# =========================
# Routes
# =========================

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form.get("question", "").strip()
        if text:
            q = Question(text=text)
            db.session.add(q)
            db.session.commit()
        return redirect(url_for("index"))

    return render_template("index.html")

@app.route("/admin")
def admin():
    questions = Question.query.order_by(
        Question.created_at.desc()
    ).all()
    return render_template("admin.html", questions=questions)

# =========================
# Create Tables
# =========================
with app.app_context():
    db.create_all()
