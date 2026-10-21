
from flask import Flask, render_template, request, redirect
import os

from database.database import (
    create_tables,
    add_job,
    add_candidate,
    get_jobs,
    get_candidates,
    get_ranked_candidates,
    get_connection,
    save_matching_result
)

from services.pdf_reader import extract_text_from_pdf
from services.matcher import calculate_score_breakdown

app = Flask(__name__)

create_tables()


@app.route("/")
def home():
    jobs = get_jobs()
    candidates = get_candidates()

    selected_job_id = request.args.get(
        "job_id", default=8, type=int
    )

    # Use an available job if the selected job does not exist.
    valid_job_ids = [job["id"] for job in jobs]

    if valid_job_ids and selected_job_id not in valid_job_ids:
        selected_job_id = valid_job_ids[0]

    ranked_candidates = (
        get_ranked_candidates(selected_job_id)
        if valid_job_ids else []
    )

    return render_template(
        "dashboard.html",
        jobs=jobs,
        candidates=candidates,
        ranked_candidates=ranked_candidates,
        selected_job_id=selected_job_id
    )


@app.route("/add-job", methods=["POST"])
def add_job_route():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()

    if not title or not description:
        return "Job title and description are required.", 400

    add_job(title, description)

    jobs = get_jobs()
    return redirect(f"/?job_id={jobs[0]['id']}")


@app.route("/upload-resumes", methods=["POST"])
def upload_resumes():
    upload_folder = "uploads/resumes"
    os.makedirs(upload_folder, exist_ok=True)

    for file in request.files.getlist("resumes"):
        if not file or not file.filename:
            continue

        if not file.filename.lower().endswith(".pdf"):
            continue

        filename = os.path.basename(file.filename)
        file_path = os.path.join(upload_folder, filename)

        file.save(file_path)

        try:
            resume_text = extract_text_from_pdf(file_path)
        except Exception:
            continue

        candidate_name = os.path.splitext(filename)[0]

        add_candidate(
            candidate_name,
            filename,
            resume_text
        )

    return redirect("/")


@app.route("/analyze-resumes", methods=["POST"])
def analyze_resumes():
    job_id = request.form.get(
        "job_id", default=8, type=int
    )

    connection = get_connection()

    try:
        job = connection.execute(
            "SELECT id, description FROM jobs WHERE id = ?",
            (job_id,)
        ).fetchone()

        candidates = connection.execute(
            "SELECT id, resume_text FROM candidates"
        ).fetchall()

    finally:
        connection.close()

    if not job:
        return "Job not found. Please select a valid job.", 404

    if not candidates:
        return "No candidates found. Please upload resumes first.", 400

    for candidate in candidates:
        resume_text = candidate["resume_text"] or ""

        # Calculate text score, skill score, overall score,
        # and matched/missing skills.
        breakdown = calculate_score_breakdown(
            job["description"],
            resume_text
        )

        save_matching_result(
            job_id=job_id,
            candidate_id=candidate["id"],
            matching_score=breakdown["overall_score"],
            matched_skills=breakdown["matched_skills"],
            missing_skills=breakdown["missing_skills"],
            text_score=breakdown["text_score"],
            skill_score=breakdown["skill_score"]
        )

    return redirect(f"/?job_id={job_id}")


if __name__ == "__main__":
    app.run(debug=True)
