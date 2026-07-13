from flask import Flask, render_template, request
from models.resume_parser import extract_resume_text
from models.resume_analyzer import analyze_resume
import os

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        uploaded_files = request.files.getlist("resume")

        results = []

        for resume in uploaded_files:

            if resume.filename == "":
                continue

            resume_path = os.path.join(
                app.config["UPLOAD_FOLDER"],
                resume.filename
            )

            resume.save(resume_path)

            resume_text = extract_resume_text(resume_path)

            analysis = analyze_resume(resume_text)

            analysis["file_name"] = resume.filename

            results.append(analysis)

        if len(results) == 1:

            return render_template(
                "result.html",
                analysis=results[0]
            )

        results.sort(
            key=lambda x: x["resume_score"],
            reverse=True
        )

        return render_template(
            "ranking.html",
            results=results
        )

    return render_template("upload.html")


if __name__ == "__main__":
    app.run(debug=True)