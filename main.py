from models import Student
from reports import student_report
from validators import (
    get_valid_float,
    get_valid_integer,
    get_valid_name,
    MAX_SCORE,
    MAX_STUDENTS,
    MIN_SCORE,
    MIN_STUDENTS,
)


def student_details() -> None:
    """Collect student details interactively with input validation, then display the performance report."""
    students: list[Student] = []

    print("-" * 60)
    print("ENTER STUDENT DETAILS")
    print("-" * 60)

    no_of_students = get_valid_integer(
        "Enter number of students: ", MIN_STUDENTS, MAX_STUDENTS
    )

    for student_index in range(no_of_students):
        print(f"\nEnter details for student {student_index + 1}")
        print("---------------------------")

        name = get_valid_name("Enter the student name: ")
        marks = get_valid_float("Enter the student marks: ", MIN_SCORE, MAX_SCORE)
        attendance = get_valid_float(
            "Enter the student attendance: ", MIN_SCORE, MAX_SCORE
        )
        assignment_score = get_valid_float(
            "Enter the student assignment score: ", MIN_SCORE, MAX_SCORE
        )

        students.append(
            Student(
                name=name,
                marks=marks,
                attendance=attendance,
                assignment_score=assignment_score,
            )
        )

    student_report(students)


if __name__ == "__main__":
    student_details()