EXAM_WEIGHT: float = 0.70
ASSIGNMENT_WEIGHT: float = 0.30

GRADE_A_THRESHOLD: float = 85
GRADE_B_THRESHOLD: float = 70
GRADE_C_THRESHOLD: float = 55
GRADE_D_THRESHOLD: float = 40

PASS_MARKS_THRESHOLD: float = 40
MIN_ATTENDANCE_THRESHOLD: float = 75

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
