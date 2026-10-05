from models import Student
from calculations import (
    calculate_average,
    calculate_grade,
    calculate_status,
)
from analyzer import find_top_performers


def student_report(students: list[Student]) -> None:
    """Print a formatted console report including summary statistics,
    per-student grades and status, and top performers.
    """
    no_of_students = len(students)

    print("-" * 60)
    print("STUDENT REPORT")
    print("-" * 60)

    # ── Summary Statistics ───────────────────────────────────────
    print("-" * 20 + "Summary Statistics" + "-" * 20)

    print("Total enrolled students: ", no_of_students)
    print("Average exam marks: ", calculate_average([s.marks for s in students]))
    print("Average assignment: ", calculate_average([s.assignment_score for s in students]))
    print("Average attendance: ", calculate_average([s.attendance for s in students]))

    # ── Student Status & Grades ──────────────────────────────────
    print("-" * 20 + "Student Status & Grades" + "-" * 20)
    print(
        f"{'Name':<12} | {'Marks':<8} | {'Attend%':<10} | "
        f"{'Assign':<8} | {'Grade':<8} | {'Status':<10}"
    )
    print("-" * 75)

    for student in students:
        print(
            f"{student.name:<12} | "
            f"{student.marks:<8} | "
            f"{student.attendance:<10} | "
            f"{student.assignment_score:<8} | "
            f"{calculate_grade(student.marks, student.assignment_score):<8} | "
            f"{calculate_status(student.marks, student.attendance):<10}"
        )

    # ── Top Performers ───────────────────────────────────────────
    print("-" * 20 + "Top Performers" + "-" * 20)

    top_students = find_top_performers(students)

    for name in top_students:
        print(name)
