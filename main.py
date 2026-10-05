# ── Constants ────────────────────────────────────────────────────────────────

EXAM_WEIGHT: float = 0.70
ASSIGNMENT_WEIGHT: float = 0.30

GRADE_A_THRESHOLD: float = 85
GRADE_B_THRESHOLD: float = 70
GRADE_C_THRESHOLD: float = 55
GRADE_D_THRESHOLD: float = 40

PASS_MARKS_THRESHOLD: float = 40
MIN_ATTENDANCE_THRESHOLD: float = 75


# ── Helper Functions ─────────────────────────────────────────────────────────

def calculate_average(values: list[float]) -> float:
    """Calculate the arithmetic average of a list of numeric values.

    Returns 0.0 for an empty list. The result is rounded to 2 decimal places.
    """
    if not values:
        return 0.0

    return round(sum(values) / len(values), 2)


def calculate_composite_score(marks: float, assignment_score: float) -> float:
    """Calculate the weighted composite performance score.

    Formula: marks × 0.70 + assignment_score × 0.30
    The result is rounded to 2 decimal places.
    """
    return round(marks * EXAM_WEIGHT + assignment_score * ASSIGNMENT_WEIGHT, 2)


def calculate_grade(marks: float, assignment_score: float) -> str:
    """Assign a letter grade based on the weighted composite score.

    Grade thresholds:
        >= 85 → A
        >= 70 → B
        >= 55 → C
        >= 40 → D
        <  40 → E
    """
    composite_score = calculate_composite_score(marks, assignment_score)

    if composite_score >= GRADE_A_THRESHOLD:
        letter_grade = "A"
    elif composite_score >= GRADE_B_THRESHOLD:
        letter_grade = "B"
    elif composite_score >= GRADE_C_THRESHOLD:
        letter_grade = "C"
    elif composite_score >= GRADE_D_THRESHOLD:
        letter_grade = "D"
    else:
        letter_grade = "E"

    return letter_grade


def calculate_status(marks: float, attendance: float) -> str:
    """Determine whether a student has passed based on marks and attendance.

    A student passes if marks >= 40 AND attendance >= 75%.
    """
    if marks >= PASS_MARKS_THRESHOLD and attendance >= MIN_ATTENDANCE_THRESHOLD:
        return "Pass"
    else:
        return "Fail"


# ── Report ───────────────────────────────────────────────────────────────────

def student_report(student_data: dict[str, list]) -> None:
    """Print a formatted console report including summary statistics,
    per-student grades and status, and top performers.
    """
    no_of_students = len(student_data["names"])

    print("-" * 60)
    print("STUDENT REPORT")
    print("-" * 60)

    # ── Summary Statistics ───────────────────────────────────────
    print("-" * 20 + "Summary Statistics" + "-" * 20)

    print("Total enrolled students: ", no_of_students)
    print("Average exam marks: ", calculate_average(student_data["marks"]))
    print("Average assignment: ", calculate_average(student_data["assignment_score"]))
    print("Average attendance: ", calculate_average(student_data["attendance"]))

    # ── Student Status & Grades ──────────────────────────────────
    print("-" * 20 + "Student Status & Grades" + "-" * 20)
    print(
        f"{'Name':<12} | {'Marks':<8} | {'Attend%':<10} | "
        f"{'Assign':<8} | {'Grade':<8} | {'Status':<10}"
    )
    print("-" * 75)

    for student_index in range(no_of_students):
        name = student_data["names"][student_index]
        marks = student_data["marks"][student_index]
        attendance = student_data["attendance"][student_index]
        assignment_score = student_data["assignment_score"][student_index]

        print(
            f"{name:<12} | "
            f"{marks:<8} | "
            f"{attendance:<10} | "
            f"{assignment_score:<8} | "
            f"{calculate_grade(marks, assignment_score):<8} | "
            f"{calculate_status(marks, attendance):<10}"
        )

    # ── Top Performers ───────────────────────────────────────────
    print("-" * 20 + "Top Performers" + "-" * 20)

    top_score = -1.0
    top_students: list[str] = []

    for student_index in range(no_of_students):
        marks = student_data["marks"][student_index]
        assignment_score = student_data["assignment_score"][student_index]
        composite_score = calculate_composite_score(marks, assignment_score)

        if composite_score > top_score:
            top_score = composite_score
            top_students = [student_data["names"][student_index]]
        elif composite_score == top_score:
            top_students.append(student_data["names"][student_index])

    for student in top_students:
        print(student)


# ── Entry Point ──────────────────────────────────────────────────────────────

def student_details() -> None:
    """Collect student details interactively and display the performance report."""
    student_data: dict[str, list] = {
        "names": [],
        "marks": [],
        "attendance": [],
        "assignment_score": [],
    }

    print("-" * 60)
    print("ENTER STUDENT DETAILS")
    print("-" * 60)

    no_of_students = int(input("Enter number of students: "))

    for student_index in range(no_of_students):
        student_data["names"].append(input("Enter the student name: ").strip())
        student_data["marks"].append(float(input("Enter the student marks: ")))
        student_data["attendance"].append(float(input("Enter the student attendance: ")))
        student_data["assignment_score"].append(float(input("Enter the student assignment score: ")))

    student_report(student_data)


if __name__ == "__main__":
    student_details()