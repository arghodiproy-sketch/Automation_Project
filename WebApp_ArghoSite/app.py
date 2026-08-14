"""
app.py — Flask web application: Resume Upload → Job Search → Results.

Usage:
    python app.py
    Open: http://127.0.0.1:5000
"""
import os
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename

from resume_parser import parse_resume
from job_scraper   import search_all_jobs
from job_matcher   import match_and_rank

# ── App config ────────────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = "arghosite-secret-2026"

UPLOAD_FOLDER   = Path(__file__).parent / "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "doc", "txt"}
UPLOAD_FOLDER.mkdir(exist_ok=True)
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024   # 5 MB limit


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/search", methods=["POST"])
def search():
    # ── 1. Validate file upload ───────────────────────────────────────────────
    if "resume" not in request.files:
        flash("Please select a resume file.", "error")
        return redirect(url_for("index"))

    file = request.files["resume"]
    if file.filename == "":
        flash("No file selected.", "error")
        return redirect(url_for("index"))

    if not allowed_file(file.filename):
        flash("Unsupported file type. Please upload PDF, DOCX, or TXT.", "error")
        return redirect(url_for("index"))

    # ── 2. Save the file ──────────────────────────────────────────────────────
    filename = secure_filename(file.filename)
    filepath = UPLOAD_FOLDER / filename
    file.save(str(filepath))

    # ── 3. Parse resume ───────────────────────────────────────────────────────
    location = request.form.get("location", "India").strip() or "India"
    try:
        resume = parse_resume(filepath)
    except Exception as exc:
        flash(f"Could not parse resume: {exc}", "error")
        return redirect(url_for("index"))
    finally:
        # Clean up uploaded file
        try:
            filepath.unlink(missing_ok=True)
        except Exception:
            pass

    if not resume["skills"]:
        flash("No recognisable skills found. Try a clearer PDF/DOCX.", "warning")

    # ── 4. Search job boards ──────────────────────────────────────────────────
    jobs = search_all_jobs(
        query    = resume["search_query"],
        location = location,
        max_per_source = 10,
    )

    # ── 5. Score and rank ─────────────────────────────────────────────────────
    ranked = match_and_rank(jobs, resume)

    return render_template(
        "results.html",
        resume   = resume,
        jobs     = ranked,
        location = location,
        query    = resume["search_query"],
    )


@app.route("/about")
def about():
    return render_template("about.html")


# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 50)
    print("  WebApp_ArghoSite — Job Finder")
    print("  Local  : http://127.0.0.1:5000")
    import socket
    try:
        local_ip = socket.gethostbyname(socket.gethostname())
        print(f"  Network: http://{local_ip}:5000  ← share this with others")
    except Exception:
        pass
    print("=" * 50)
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)
