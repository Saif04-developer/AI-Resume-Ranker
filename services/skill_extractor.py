SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "javascript",
    "html",
    "css",
    "sql",
    "flask",
    "django",
    "react",
    "node.js",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "nlp",
    "tensorflow",
    "pytorch",
    "git",
    "github",
    "mysql",
    "sqlite",
    "mongodb",
    "data structures",
    "algorithms",
    "computer networks",
    "operating system"
]


def extract_skills(text):
    text = text.lower()

    found_skills = []

    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)

    return sorted(set(found_skills))