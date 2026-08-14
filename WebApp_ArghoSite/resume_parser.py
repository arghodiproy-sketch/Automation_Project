"""
resume_parser.py — Extract text, skills and job title from uploaded PDF/DOCX.
"""
import re
from pathlib import Path

# ── Common tech / domain skills to look for ────────────────────────────────
SKILL_KEYWORDS = [
    # Languages
    "python","java","javascript","typescript","c#","c++","ruby","go","scala","kotlin","swift",
    # Web
    "html","css","react","angular","vue","flask","django","fastapi","nodejs","spring","rest","api",
    # Testing
    "selenium","appium","pytest","junit","testng","cucumber","cypress","playwright","postman",
    "jmeter","loadrunner","gatling","allure","bdd","tdd","automation","manual testing",
    "page object","pom","qa","qe","sdet","sqa",
    # Cloud / DevOps
    "aws","azure","gcp","docker","kubernetes","jenkins","github actions","ci/cd","terraform",
    "ansible","linux","bash","powershell","git",
    # Data
    "sql","mysql","postgresql","mongodb","redis","elasticsearch","kafka","spark","hadoop",
    "pandas","numpy","machine learning","ai","llm","rag","crewai",
    # Mobile
    "android","ios","flutter","react native","xcode",
    # Tools
    "jira","confluence","postman","swagger","sonarqube","splunk","grafana",
]

# ── Job title patterns ──────────────────────────────────────────────────────
TITLE_PATTERNS = [
    r"(senior|lead|principal|staff|junior)?\s*(software|test|qa|sdet|automation|backend|frontend|full.?stack)\s*(engineer|developer|analyst|architect|manager)",
    r"(it manager|delivery manager|project manager|product manager|scrum master|devops engineer)",
    r"(data scientist|data engineer|ml engineer|ai engineer|cloud architect)",
]

def extract_text_from_pdf(filepath: Path) -> str:
    from pypdf import PdfReader
    reader = PdfReader(str(filepath))
    return "\n".join(page.extract_text() or "" for page in reader.pages)

def extract_text_from_docx(filepath: Path) -> str:
    from docx import Document
    doc = Document(str(filepath))
    return "\n".join(p.text for p in doc.paragraphs)

def extract_text(filepath: Path) -> str:
    ext = filepath.suffix.lower()
    if ext == ".pdf":
        return extract_text_from_pdf(filepath)
    elif ext in (".docx", ".doc"):
        return extract_text_from_docx(filepath)
    return filepath.read_text(encoding="utf-8", errors="ignore")

def extract_skills(text: str) -> list[str]:
    """Return a sorted list of unique skills found in the resume text."""
    text_lower = text.lower()
    found = []
    for skill in SKILL_KEYWORDS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text_lower):
            found.append(skill)
    return sorted(set(found))

def extract_job_title(text: str) -> str:
    """Try to detect the candidate's current/target job title."""
    text_lower = text.lower()
    for pattern in TITLE_PATTERNS:
        match = re.search(pattern, text_lower)
        if match:
            return match.group(0).strip().title()
    return "Software Professional"

def extract_experience_years(text: str) -> int:
    """Parse total years of experience mentioned in the resume."""
    matches = re.findall(r"(\d+)\+?\s*years?\s*(of\s*)?(experience|exp)", text, re.IGNORECASE)
    if matches:
        return max(int(m[0]) for m in matches)
    return 0

def parse_resume(filepath: Path) -> dict:
    """
    Parse a resume file and return a dict with:
        text        : full raw text
        skills      : list of detected skills
        job_title   : inferred job title
        experience  : years of experience
        search_query: best query string for job boards
    """
    text  = extract_text(filepath)
    skills = extract_skills(text)
    title  = extract_job_title(text)
    exp    = extract_experience_years(text)

    # Build a search query: top 5 skills + job title
    top_skills = skills[:5] if skills else ["software engineer"]
    query = f"{title} {' '.join(top_skills[:3])}"

    return {
        "text":         text,
        "skills":       skills,
        "job_title":    title,
        "experience":   exp,
        "search_query": query.strip(),
    }
