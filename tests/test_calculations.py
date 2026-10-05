import pytest
from calculations import (
    calculate_average,
    calculate_composite_score,
    calculate_grade,
    calculate_status,
    GRADE_A_THRESHOLD,
    GRADE_B_THRESHOLD,
    GRADE_C_THRESHOLD,
    GRADE_D_THRESHOLD,
    PASS_MARKS_THRESHOLD,
    MIN_ATTENDANCE_THRESHOLD,
)

def test_calculate_average():
    assert calculate_average([80, 90, 100]) == 90.0
    assert calculate_average([50]) == 50.0
    assert calculate_average([]) == 0.0

def test_calculate_composite_score():
    assert calculate_composite_score(80, 90) == 83.0  # (80*0.7) + (90*0.3) = 56 + 27 = 83
    assert calculate_composite_score(0, 0) == 0.0
    assert calculate_composite_score(100, 100) == 100.0

def test_calculate_grade():
    assert calculate_grade(GRADE_A_THRESHOLD, 100) == "A"
    assert calculate_grade(GRADE_B_THRESHOLD, 80) == "B"
    assert calculate_grade(GRADE_C_THRESHOLD, 80) == "C"
    assert calculate_grade(GRADE_D_THRESHOLD, 80) == "D"
    assert calculate_grade(GRADE_D_THRESHOLD - 10, 50) == "E"

def test_calculate_status():
    # Passing student
    assert calculate_status(PASS_MARKS_THRESHOLD + 10, MIN_ATTENDANCE_THRESHOLD + 5) == "Pass"
    
    # Boundary passing
    assert calculate_status(PASS_MARKS_THRESHOLD, MIN_ATTENDANCE_THRESHOLD) == "Pass"
    
    # Failing due to marks
    assert calculate_status(PASS_MARKS_THRESHOLD - 1, MIN_ATTENDANCE_THRESHOLD + 10) == "Fail"
    
    # Failing due to attendance
    assert calculate_status(PASS_MARKS_THRESHOLD + 20, MIN_ATTENDANCE_THRESHOLD - 1) == "Fail"
    
    # Failing due to both
    assert calculate_status(PASS_MARKS_THRESHOLD - 10, MIN_ATTENDANCE_THRESHOLD - 10) == "Fail"
