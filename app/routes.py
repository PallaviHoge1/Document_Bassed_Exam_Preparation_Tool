import os
import uuid
import json
from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash

from .services.pdf_loader import extract_text_from_pdf
from .services.summarizer import summarize_text
from .services.quiz_generator import generate_mcqs
from .utils.text_clean import normalize_whitespace

bp = Blueprint("main", __name__)

def _job_paths(job_id: str):
    data_dir = current_app.config["DATA_FOLDER"]
    return {
        "text": os.path.join(data_dir, f"{job_id}.txt"),
        "summary": os.path.join(data_dir, f"{job_id}.summary.txt"),
        "quiz": os.path.join(data_dir, f"{job_id}.quiz.json"),
    }

@bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@bp.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("document")
    if not file or file.filename == "":
        flash("Please choose a PDF file.", "error")
        return redirect(url_for("main.index"))

    if not file.filename.lower().endswith(".pdf"):
        flash("Only PDF files are supported.", "error")
        return redirect(url_for("main.index"))

    job_id = str(uuid.uuid4())[:8]
    upload_path = os.path.join(current_app.config["UPLOAD_FOLDER"], f"{job_id}.pdf")
    file.save(upload_path)

    # Extract text
    try:
        raw_text = extract_text_from_pdf(upload_path)
        clean_text = normalize_whitespace(raw_text)
        paths = _job_paths(job_id)
        with open(paths["text"], "w", encoding="utf-8") as f:
            f.write(clean_text)
    except Exception as e:
        current_app.logger.exception("PDF extraction failed")
        flash(f"Failed to read PDF: {e}", "error")
        return redirect(url_for("main.index"))

    # Auto-generate summary after upload (as required)
    try:
        summary = summarize_text(clean_text)
        with open(paths["summary"], "w", encoding="utf-8") as f:
            f.write(summary)
    except Exception as e:
        current_app.logger.exception("Summarization failed")
        flash(f"Failed to summarize: {e}", "error")
        return redirect(url_for("main.index"))

    return redirect(url_for("main.summary", job_id=job_id))

@bp.route("/summary/<job_id>", methods=["GET"])
def summary(job_id):
    paths = _job_paths(job_id)
    if not os.path.exists(paths["summary"]):
        flash("Summary not found for this job.", "error")
        return redirect(url_for("main.index"))

    with open(paths["summary"], "r", encoding="utf-8") as f:
        summary_text = f.read()

    return render_template("summary.html", job_id=job_id, summary=summary_text)

@bp.route("/quiz/<job_id>", methods=["GET"])
def quiz(job_id):
    paths = _job_paths(job_id)
    if not os.path.exists(paths["summary"]):
        flash("Please generate summary first.", "error")
        return redirect(url_for("main.index"))

    quiz_items = None
    if os.path.exists(paths["quiz"]):
        with open(paths["quiz"], "r", encoding="utf-8") as f:
            quiz_items = json.load(f)

    return render_template("quiz.html", job_id=job_id, quiz=quiz_items)

@bp.route("/quiz/<job_id>/generate", methods=["POST"])
def generate_quiz(job_id):
    num_q = request.form.get("num_questions", type=int, default=5)
    paths = _job_paths(job_id)

    if not os.path.exists(paths["summary"]):
        flash("Summary not found.", "error")
        return redirect(url_for("main.index"))

    with open(paths["summary"], "r", encoding="utf-8") as f:
        summary_text = f.read()

    try:
        quiz = generate_mcqs(summary_text, num_questions=num_q)
        with open(paths["quiz"], "w", encoding="utf-8") as f:
            json.dump(quiz, f, ensure_ascii=False, indent=2)
        flash("Quiz generated successfully!", "success")
    except Exception as e:
        current_app.logger.exception("Quiz generation failed")
        flash(f"Failed to generate quiz: {e}", "error")

    return redirect(url_for("main.quiz", job_id=job_id))
