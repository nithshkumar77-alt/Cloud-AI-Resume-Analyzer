from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)

SKILLS = [
    "python", "java", "javascript", "typescript", "c", "c++", "c#", "html",
    "css", "react", "angular", "node.js", "nodejs", "express", "flask",
    "django", "spring", "sql", "mysql", "postgresql", "mongodb", "firebase",
    "aws", "azure", "gcp", "docker", "kubernetes", "git", "github",
    "machine learning", "deep learning", "artificial intelligence", "nlp",
    "data analysis", "pandas", "numpy", "tensorflow", "pytorch", "figma",
    "rest api", "api", "linux", "cloud computing", "excel"
]

SECTIONS = [
    "education", "experience", "work experience", "projects", "skills",
    "certifications", "summary", "objective", "achievements", "internship",
    "contact"
]

def clean(text):
    return re.sub(r"\s+", " ", text.lower()).strip()

def contains_term(text, term):
    pattern = r"(?<![a-z0-9])" + re.escape(term.lower()) + r"(?![a-z0-9])"
    return re.search(pattern, text) is not None

def analyze_resume(resume, job_description=""):
    resume_l = clean(resume)
    jd_l = clean(job_description)

    found_skills = [s for s in SKILLS if contains_term(resume_l, s)]
    jd_skills = [s for s in SKILLS if contains_term(jd_l, s)]
    matched = [s for s in jd_skills if s in found_skills]
    missing = [s for s in jd_skills if s not in found_skills]

    sections_found = []
    for section in SECTIONS:
        if contains_term(resume_l, section):
            sections_found.append(section)

    score = 0
    score += min(len(found_skills) * 3, 30)

    if job_description.strip():
        if jd_skills:
            score += round((len(matched) / len(jd_skills)) * 40)
        else:
            score += 20
    else:
        score += 20

    section_score = min(len(set(sections_found)) * 3, 20)
    score += section_score

    suggestions = []
    if len(resume.split()) < 150:
        suggestions.append("Add more measurable detail. Mention projects, responsibilities, technologies and outcomes.")
    if "summary" not in sections_found and "objective" not in sections_found:
        suggestions.append("Consider adding a short professional summary tailored to the target role.")
    if "projects" not in sections_found:
        suggestions.append("Add a Projects section with 2–3 relevant projects and your contribution.")
    if "experience" not in sections_found and "work experience" not in sections_found and "internship" not in sections_found:
        suggestions.append("If applicable, add internships, volunteering, freelance work or practical experience.")
    if "certifications" not in sections_found:
        suggestions.append("Add relevant certifications or courses if you have them.")
    if jd_skills and missing:
        suggestions.append("If you genuinely have these skills, add them naturally to the resume: " + ", ".join(missing[:8]) + ".")
    if not suggestions:
        suggestions.append("Good structure detected. Tailor your bullet points to the exact job description and quantify results where possible.")

    score = min(score, 100)

    return {
        "score": score,
        "skills": sorted(found_skills),
        "job_skills": sorted(jd_skills),
        "matched": sorted(matched),
        "missing": sorted(missing),
        "sections": sorted(set(sections_found)),
        "suggestions": suggestions
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.post("/api/analyze")
def analyze():
    data = request.get_json(silent=True) or {}
    resume = data.get("resume", "")
    job_description = data.get("job_description", "")

    if not resume.strip():
        return jsonify({"error": "Please provide resume text."}), 400

    return jsonify(analyze_resume(resume, job_description))

@app.post("/api/upload")
def upload():
    file = request.files.get("resume")
    if not file:
        return jsonify({"error": "No file uploaded."}), 400
    if not file.filename.lower().endswith(".txt"):
        return jsonify({"error": "For this starter version, upload a .txt resume."}), 400

    text = file.read().decode("utf-8", errors="ignore")
    return jsonify({"resume": text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
