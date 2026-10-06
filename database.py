import sqlite3
from pathlib import Path
from logger import app_logger

from models import Student

DATABASE_PATH = Path("data/students.db")


def initialize_database() -> None:
    """Create the students table if it does not exist."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    try:
        with sqlite3.connect(DATABASE_PATH) as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    marks REAL NOT NULL,
                    attendance REAL NOT NULL,
                    assignment_score REAL NOT NULL
                )
                """
            )
        app_logger.info("Database initialized")
    except sqlite3.Error:
        app_logger.exception("Failed to initialize database")
        raise


def add_student(student: Student) -> None:
    """Insert one student into the database."""
    try:
        with sqlite3.connect(DATABASE_PATH) as connection:
            connection.execute(
                """
                INSERT INTO students (name, marks, attendance, assignment_score)
                VALUES (?, ?, ?, ?)
                """,
                (student.name, student.marks, student.attendance, student.assignment_score),
            )
        app_logger.info("Student added to database")
    except sqlite3.Error:
        app_logger.exception("Failed to add student to database")
        raise


def add_students(students: list[Student]) -> None:
    """Insert multiple students into the database."""
    if not students:
        return

    try:
        with sqlite3.connect(DATABASE_PATH) as connection:
            connection.executemany(
                """
                INSERT INTO students (name, marks, attendance, assignment_score)
                VALUES (?, ?, ?, ?)
                """,
                [
                    (s.name, s.marks, s.attendance, s.assignment_score)
                    for s in students
                ],
            )
        app_logger.info("Added %d students to database", len(students))
    except sqlite3.Error:
        app_logger.exception("Failed to add multiple students to database")
        raise


def get_all_students() -> list[Student]:
    """Retrieve all students from the database as Student objects."""
    app_logger.debug("Fetching students from database")
    try:
        with sqlite3.connect(DATABASE_PATH) as connection:
            rows = connection.execute(
                """
                SELECT name, marks, attendance, assignment_score
                FROM students
                ORDER BY id
                """
            ).fetchall()
    except sqlite3.Error:
        app_logger.exception("Failed to fetch students from database")
        raise

    return [
        Student(
            name=row[0],
            marks=float(row[1]),
            attendance=float(row[2]),
            assignment_score=float(row[3]),
        )
        for row in rows
    ]


def get_all_student_records() -> list[dict[str, int | float | str]]:
    """Retrieve all student records from the database including their IDs."""
    app_logger.debug("Fetching student records from database")
    try:
        with sqlite3.connect(DATABASE_PATH) as connection:
            rows = connection.execute(
                """
                SELECT id, name, marks, attendance, assignment_score
                FROM students
                ORDER BY id
                """
            ).fetchall()
    except sqlite3.Error:
        app_logger.exception("Failed to fetch student records from database")
        raise

    return [
        {
            "id": row[0],
            "name": row[1],
            "marks": float(row[2]),
            "attendance": float(row[3]),
            "assignment_score": float(row[4]),
        }
        for row in rows
    ]


def delete_all_students() -> None:
    """Delete all student records from the database."""
    try:
        with sqlite3.connect(DATABASE_PATH) as connection:
            connection.execute("DELETE FROM students")
        app_logger.info("All students deleted from database")
    except sqlite3.Error:
        app_logger.exception("Failed to delete all students from database")
        raise


def count_students() -> int:
    """Return the number of students in the database."""
    try:
        with sqlite3.connect(DATABASE_PATH) as connection:
            return connection.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    except sqlite3.Error:
        app_logger.exception("Failed to count students in database")
        raise
