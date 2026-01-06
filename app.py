from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = "questions.json"  # ملف حفظ الأسئلة

# تحميل الأسئلة
def load_questions():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# حفظ الأسئلة
def save_questions(questions):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

# صفحة طرح السؤال
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        text = request.form.get("question", "").strip()
        if text:
            questions = load_questions()
            questions.append({
                "text": text,
                "created_at": datetime.utcnow().isoformat()
            })
            save_questions(questions)
        return redirect(url_for("index"))
    return render_template("index.html")

# لوحة الأدمن
@app.route("/admin")
def admin():
    questions = load_questions()
    # ترتيب الأسئلة من الأحدث للأقدم
    questions = sorted(questions, key=lambda x: x["created_at"], reverse=True)
    return render_template("admin.html", questions=questions)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
