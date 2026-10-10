import re


def clean_text(text):
    # Convert text to lowercase
    text = text.lower()

    # Remove extra whitespace and new lines
    text = re.sub(r"\s+", " ", text)

    # Remove special characters
    text = re.sub(r"[^a-z0-9\s]", " ", text)

    # Remove extra spaces again
    text = re.sub(r"\s+", " ", text)

    # Remove leading and trailing spaces
    text = text.strip()

    return text