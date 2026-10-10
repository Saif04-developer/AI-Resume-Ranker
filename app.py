from flask import Flask, render_template, request, redirect
import os
from database.database import create_tables

app = Flask(__name__)
create_tables()


@app.route("/")
def home():
    return render_template("dashboard.html")


@app.route("/upload-resumes", methods=["POST"])
def upload_resumes():
    upload_folder = "uploads/resumes"

    for file in request.files.getlist("resumes"):
        if file and file.filename.lower().endswith(".pdf"):
            file.save(os.path.join(upload_folder, file.filename))

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)