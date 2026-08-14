"""
job_matcher.py — Score and rank jobs against a parsed resume.

Scoring logic:
  - Each skill from the resume found in the job title   →  +10 pts
  - Each skill from the resume found in the job company → +2  pts
  - Job title overlap with resume title                 →  +15 pts
  - Bonus for seniority keyword match                   →  +5  pts

Final score is normalised to 0–100 %.
"""
import re


def _text_contains(text: str, keywords: list[str]) -> list[str]:
    """Return keywords found in text (case-insensitive whole-word match)."""
    text_lower = text.lower()
    return [kw for kw in keywords if re.search(r"\b" + re.escape(kw.lower()) + r"\b", text_lower)]


def score_job(job: dict, resume: dict) -> int:
    """
    Return a 0–100 match score for one job against the parsed resume.
    """
    skills    = resume.get("skills", [])
    res_title = resume.get("job_title", "").lower()
    job_text  = f"{job.get('title','')} {job.get('description','')}".lower()
    score     = 0

    # Skill matches in job title / description
    matched_skills = _text_contains(job_text, skills)
    score += len(matched_skills) * 8

    # Job title overlap with resume title
    res_words = set(res_title.split())
    job_words = set(job.get("title", "").lower().split())
    common    = res_words & job_words - {"and", "or", "the", "a", "in", "for"}
    score += len(common) * 10

    # Seniority / level bonus
    seniority_keywords = ["senior", "lead", "principal", "manager", "architect", "staff"]
    if any(s in job.get("title", "").lower() for s in seniority_keywords):
        score += 5

    # Cap at 100
    return min(score, 100)


def match_and_rank(jobs: list[dict], resume: dict) -> list[dict]:
    """
    Score every job, attach match info, and return sorted by score desc.
    """
    skills = resume.get("skills", [])
    results = []

    for job in jobs:
        job_text = f"{job.get('title','')} {job.get('description','')}".lower()
        matched  = _text_contains(job_text, skills)
        sc       = score_job(job, resume)

        results.append({
            **job,
            "match_score":    sc,
            "matched_skills": matched,
            "match_label":    _label(sc),
        })

    return sorted(results, key=lambda j: j["match_score"], reverse=True)


def _label(score: int) -> str:
    if score >= 70:
        return "Excellent Match"
    if score >= 45:
        return "Good Match"
    if score >= 20:
        return "Partial Match"
    return "Low Match"
