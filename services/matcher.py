
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from services.skill_extractor import extract_skills


def create_tfidf_vectors(job_description, resume_text):
    documents = [job_description, resume_text]
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(documents)
    return vectors


def calculate_similarity(job_description, resume_text):
    vectors = create_tfidf_vectors(
        job_description,
        resume_text
    )

    score = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return round(float(score) * 100, 2)


def calculate_skill_match(job_description, resume_text):
    job_skills = set(extract_skills(job_description))
    resume_skills = set(extract_skills(resume_text))

    matched_skills = sorted(
        job_skills.intersection(resume_skills)
    )
    missing_skills = sorted(
        job_skills.difference(resume_skills)
    )

    if not job_skills:
        return {
            "skill_score": 0.0,
            "matched_skills": [],
            "missing_skills": []
        }

    skill_score = (
        len(matched_skills) / len(job_skills)
    ) * 100

    return {
        "skill_score": round(skill_score, 2),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }

def calculate_overall_score(job_description, resume_text):
    text_score = calculate_similarity(
        job_description,
        resume_text
    )

    skill_result = calculate_skill_match(
        job_description,
        resume_text
    )

    skill_score = skill_result["skill_score"]

    overall_score = (
        text_score * 0.60
        + skill_score * 0.40
    )

    return round(overall_score, 2)

def rank_candidates(candidates):
    return sorted(
        candidates,
        key=lambda candidate: candidate["overall_score"],
        reverse=True
    )
