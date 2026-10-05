import sqlite3
from pathlib import Path

from models import Student

DATABASE_PATH = Path("data/students.db")


def initialize_database() -> None:
    """Create the students table if it does not exist."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

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


def add_student(student: Student) -> None:
    """Insert one student into the database."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute(
            """
            INSERT INTO students (name, marks, attendance, assignment_score)
            VALUES (?, ?, ?, ?)
            """,
            (
                student.name,
                student.marks,
                student.attendance,
                student.assignment_score,
            ),
        )


def add_students(students: list[Student]) -> None:
    """Insert multiple students into the database."""
    if not students:
        return

    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.executemany(
            """
            INSERT INTO students (name, marks, attendance, assignment_score)
            VALUES (?, ?, ?, ?)
            """,
            [
                (
                    student.name,
                    student.marks,
                    student.attendance,
                    student.assignment_score,
                )
                for student in students
            ],
        )


def get_all_students() -> list[Student]:
    """Retrieve all students from the database as Student objects."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        rows = connection.execute(
            """
            SELECT name, marks, attendance, assignment_score
            FROM students
            ORDER BY id
            """
        ).fetchall()

    return [
        Student(
            name=row[0],
            marks=float(row[1]),
            attendance=float(row[2]),
            assignment_score=float(row[3]),
        )
        for row in rows
    ]


def delete_all_students() -> None:
    """Delete all student records from the database."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        connection.execute("DELETE FROM students")


def count_students() -> int:
    """Return the number of students in the database."""
    with sqlite3.connect(DATABASE_PATH) as connection:
        result = connection.execute("SELECT COUNT(*) FROM students").fetchone()

    return result[0]
