import pandas as pd
from pathlib import Path

ROOT = Path.home() / "GOVCON_AI"
JOBS = ROOT / "data/jobs/remote_jobs.csv"

def score_job(title="", desc=""):
    text = f"{title} {desc}".lower()
    score = 50
    for x in ["remote","work from home","training","logistics","coordinator","government","analyst","operations","contract"]:
        if x in text:
            score += 8
    for x in ["commission only","door to door","travel required"]:
        if x in text:
            score -= 20
    return max(0, min(100, score))

def save_job(title, company, link, desc):
    JOBS.parent.mkdir(parents=True, exist_ok=True)
    row = pd.DataFrame([{
        "score": score_job(title, desc),
        "title": title,
        "company": company,
        "link": link,
        "description": desc,
        "status": "new"
    }])
    if JOBS.exists():
        row = pd.concat([pd.read_csv(JOBS), row], ignore_index=True)
    row.to_csv(JOBS, index=False)
    return row

def draft_application(job_title="", company=""):
    return f"""Hello,

I’m interested in the {job_title} role with {company}. I bring 20+ years of government, logistics, training coordination, SAP, audit, compliance, and operations experience.

Respectfully,
Joe Budds
"""
