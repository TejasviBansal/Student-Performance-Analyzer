from models import Student
from calculations import calculate_composite_score

def find_top_performers(students: list[Student]) -> list[str]:
    """Find the top performing student(s) based on composite score.

    Returns a list of student names who have the highest composite score.
    Handles ties by returning all students with the highest score.
    """
    top_score = -1.0
    top_students: list[str] = []

    for student in students:
        composite_score = calculate_composite_score(
            student.marks, student.assignment_score
        )

        if composite_score > top_score:
            top_score = composite_score
            top_students = [student.name]
        elif composite_score == top_score:
            top_students.append(student.name)

    return top_students
