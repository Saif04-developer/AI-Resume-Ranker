
import sqlite3

DATABASE = "database/resume_ranker.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables():
    connection = get_connection()

    try:
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
                FOREIGN KEY (candidate_id) REFERENCES candidates(id),
                UNIQUE (job_id, candidate_id)
            )
        """)

        # Safely add the new columns to an existing database.
        # Existing jobs, candidates, and results are preserved.
        columns = {
            row["name"]
            for row in cursor.execute(
                "PRAGMA table_info(results)"
            ).fetchall()
        }

        if "text_score" not in columns:
            cursor.execute("""
                ALTER TABLE results
                ADD COLUMN text_score REAL
            """)

        if "skill_score" not in columns:
            cursor.execute("""
                ALTER TABLE results
                ADD COLUMN skill_score REAL
            """)

        connection.commit()

    finally:
        connection.close()


def add_job(title, job_description):
    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO jobs (title, description)
            VALUES (?, ?)
            """,
            (title, job_description)
        )
        connection.commit()

    finally:
        connection.close()


def get_jobs():
    connection = get_connection()

    try:
        return connection.execute(
            """
            SELECT id, title
            FROM jobs
            ORDER BY id DESC
            """
        ).fetchall()

    finally:
        connection.close()


def add_candidate(name, resume_filename, resume_text):
    connection = get_connection()

    try:
        existing = connection.execute(
            """
            SELECT id
            FROM candidates
            WHERE resume_filename = ?
            LIMIT 1
            """,
            (resume_filename,)
        ).fetchone()

        if existing:
            connection.execute(
                """
                UPDATE candidates
                SET name = ?, resume_text = ?
                WHERE id = ?
                """,
                (name, resume_text, existing["id"])
            )

        else:
            connection.execute(
                """
                INSERT INTO candidates (
                    name, resume_filename, resume_text
                )
                VALUES (?, ?, ?)
                """,
                (name, resume_filename, resume_text)
            )

        connection.commit()

    finally:
        connection.close()


def get_candidates():
    connection = get_connection()

    try:
        return connection.execute(
            """
            SELECT id, name, resume_filename
            FROM candidates
            ORDER BY id DESC
            """
        ).fetchall()

    finally:
        connection.close()


def save_matching_result(
    job_id,
    candidate_id,
    matching_score,
    matched_skills,
    missing_skills,
    text_score=None,
    skill_score=None
):
    connection = get_connection()

    try:
        existing_result = connection.execute(
            """
            SELECT id
            FROM results
            WHERE job_id = ? AND candidate_id = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (job_id, candidate_id)
        ).fetchone()

        matched = ", ".join(matched_skills)
        missing = ", ".join(missing_skills)

        if existing_result:
            connection.execute(
                """
                UPDATE results
                SET matching_score = ?,
                    matched_skills = ?,
                    missing_skills = ?,
                    text_score = ?,
                    skill_score = ?
                WHERE id = ?
                """,
                (
                    matching_score,
                    matched,
                    missing,
                    text_score,
                    skill_score,
                    existing_result["id"]
                )
            )

        else:
            connection.execute(
                """
                INSERT INTO results (
                    job_id,
                    candidate_id,
                    matching_score,
                    matched_skills,
                    missing_skills,
                    text_score,
                    skill_score
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    job_id,
                    candidate_id,
                    matching_score,
                    matched,
                    missing,
                    text_score,
                    skill_score
                )
            )

        connection.commit()

    finally:
        connection.close()


def get_ranked_candidates(job_id):
    connection = get_connection()

    try:
        return connection.execute(
            """
            SELECT
                results.id AS result_id,
                results.job_id,
                results.candidate_id,
                results.matching_score,
                results.text_score,
                results.skill_score,
                results.matched_skills,
                results.missing_skills,
                candidates.name AS candidate_name,
                candidates.resume_filename,
                jobs.title AS job_title
            FROM results
            JOIN candidates
                ON results.candidate_id = candidates.id
            JOIN jobs
                ON results.job_id = jobs.id
            WHERE results.job_id = ?
            ORDER BY results.matching_score DESC
            """,
            (job_id,)
        ).fetchall()

    finally:
        connection.close()
