
from flask import Flask, render_template, request, redirect
import os

from database.database import create_tables, add_candidate, get_candidates
from services.pdf_reader import extract_text_from_pdf

app = Flask(__name__)

create_tables()

@app.route("/")
def home():
    candidates = get_candidates()
    return render_template(
        "dashboard.html",
        candidates=candidates
    )
    
@app.route("/add-job", methods=["POST"])
def add_job_route():
    title = request.form["title"]
    description = request.form["description"]

    from database.database import add_job
    add_job(title, description)

    return redirect("/")



@app.route("/upload-resumes", methods=["POST"])
def upload_resumes():
    upload_folder = "uploads/resumes"
    os.makedirs(upload_folder, exist_ok=True)

    for file in request.files.getlist("resumes"):
        if file and file.filename.lower().endswith(".pdf"):
            filename = file.filename
            file_path = os.path.join(upload_folder, filename)

            file.save(file_path)

            resume_text = extract_text_from_pdf(file_path)
            candidate_name = os.path.splitext(filename)[0]

            add_candidate(
                candidate_name,
                filename,
                resume_text
            )

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
