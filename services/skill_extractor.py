
import re

SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "c#",
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
        # Match complete skill names instead of substrings.
        if skill == "c":
            pattern = r"(?<!\w)c(?![\w+#])"
        else:
            pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):
            found_skills.append(skill)

    return sorted(set(found_skills))
