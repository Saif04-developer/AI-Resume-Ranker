import sqlite3

DATABASE = "database/resume_ranker.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            resume_filename TEXT,
            resume_text TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER,
            candidate_id INTEGER,
            matching_score REAL,
            matched_skills TEXT,
            missing_skills TEXT,
            FOREIGN KEY (job_id) REFERENCES jobs(id),
            FOREIGN KEY (candidate_id) REFERENCES candidates(id)
        )
    """)

    connection.commit()
    connection.close()
def add_job(title, job_description):
    connection = get_connection()

    connection.execute(
        "INSERT INTO jobs (title, description) VALUES (?, ?)",
        (title, job_description)
    )

    connection.commit()
    connection.close()