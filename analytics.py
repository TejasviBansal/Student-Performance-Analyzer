import pandas as pd
from logger import app_logger
from models import Student
from calculations import (
    GRADE_A_THRESHOLD,
    GRADE_B_THRESHOLD,
    GRADE_C_THRESHOLD,
    GRADE_D_THRESHOLD,
    PASS_MARKS_THRESHOLD,
    MIN_ATTENDANCE_THRESHOLD,
    calculate_composite_score,
    calculate_grade,
    calculate_status,
)

def _students_to_dataframe(students: list[Student]) -> pd.DataFrame:
    """Convert a list of Student objects into a Pandas DataFrame.
    Calculates derived analytical columns without modifying the original Student objects.
    """
    if not students:
        app_logger.warning("No students available for analytics")
        raise ValueError("At least one student is required for analytics.")

    app_logger.info("Calculating student performance analytics")

    data = []
    for s in students:
        composite = calculate_composite_score(s.marks, s.assignment_score)
        grade = calculate_grade(s.marks, s.assignment_score)
        status = calculate_status(s.marks, s.attendance)
        
        data.append({
            "name": s.name,
            "marks": s.marks,
            "attendance": s.attendance,
            "assignment_score": s.assignment_score,
            "composite_score": composite,
            "grade": grade,
            "status": status,
        })
    
    return pd.DataFrame(data)

def calculate_performance_summary(students: list[Student]) -> dict[str, int | float]:
    """Calculate overall performance metrics."""
    df = _students_to_dataframe(students)
    return {
        "total_students": len(df),
        "average_marks": round(df["marks"].mean(), 2),
        "median_marks": round(df["marks"].median(), 2),
        "highest_marks": round(df["marks"].max(), 2),
        "lowest_marks": round(df["marks"].min(), 2),
        "average_assignment_score": round(df["assignment_score"].mean(), 2),
        "average_attendance": round(df["attendance"].mean(), 2),
    }

def calculate_pass_fail_summary(students: list[Student]) -> dict[str, int | float]:
    """Calculate pass and fail counts and percentages."""
    df = _students_to_dataframe(students)
    total = len(df)
    pass_count = int((df["status"] == "Pass").sum())
    fail_count = total - pass_count
    
    return {
        "pass_count": pass_count,
        "fail_count": fail_count,
        "pass_percentage": round((pass_count / total) * 100, 2),
        "fail_percentage": round((fail_count / total) * 100, 2),
    }

def calculate_grade_distribution(students: list[Student]) -> dict[str, int]:
    """Calculate the number of students receiving each grade."""
    df = _students_to_dataframe(students)
    counts = df["grade"].value_counts().to_dict()
    
    return {
        "A": counts.get("A", 0),
        "B": counts.get("B", 0),
        "C": counts.get("C", 0),
        "D": counts.get("D", 0),
        "E": counts.get("E", 0),
    }

def calculate_attendance_summary(students: list[Student]) -> dict[str, int | float]:
    """Calculate average, highest, lowest attendance, and below-threshold statistics."""
    df = _students_to_dataframe(students)
    total = len(df)
    below_req_count = int((df["attendance"] < MIN_ATTENDANCE_THRESHOLD).sum())
    
    return {
        "average_attendance": round(df["attendance"].mean(), 2),
        "highest_attendance": round(df["attendance"].max(), 2),
        "lowest_attendance": round(df["attendance"].min(), 2),
        "below_required_attendance_count": below_req_count,
        "below_required_attendance_percentage": round((below_req_count / total) * 100, 2),
    }

def calculate_score_distribution(students: list[Student]) -> dict[str, int]:
    """Group students into exam score ranges."""
    df = _students_to_dataframe(students)
    marks = df["marks"]
    
    return {
        "90+": int(marks[marks >= 90].count()),
        "80-89.99": int(marks[(marks >= 80) & (marks < 90)].count()),
        "70-79.99": int(marks[(marks >= 70) & (marks < 80)].count()),
        "60-69.99": int(marks[(marks >= 60) & (marks < 70)].count()),
        "50-59.99": int(marks[(marks >= 50) & (marks < 60)].count()),
        "Below 50": int(marks[marks < 50].count()),
    }

def calculate_performance_categories(students: list[Student]) -> dict[str, int]:
    """Group students by performance categories based on composite score."""
    df = _students_to_dataframe(students)
    scores = df["composite_score"]
    
    return {
        "Excellent": int(scores[scores >= GRADE_A_THRESHOLD].count()),
        "Good": int(scores[(scores >= GRADE_B_THRESHOLD) & (scores < GRADE_A_THRESHOLD)].count()),
        "Average": int(scores[(scores >= GRADE_C_THRESHOLD) & (scores < GRADE_B_THRESHOLD)].count()),
        "Needs Improvement": int(scores[(scores >= GRADE_D_THRESHOLD) & (scores < GRADE_C_THRESHOLD)].count()),
        "Critical": int(scores[scores < GRADE_D_THRESHOLD].count()),
    }

def identify_at_risk_students(students: list[Student]) -> list[str]:
    """Identify students who fall below thresholds for marks, attendance, or composite score."""
    df = _students_to_dataframe(students)
    mask = (
        (df["marks"] < PASS_MARKS_THRESHOLD) |
        (df["attendance"] < MIN_ATTENDANCE_THRESHOLD) |
        (df["composite_score"] < GRADE_D_THRESHOLD)
    )
    return df.loc[mask, "name"].tolist()

def identify_high_performers(students: list[Student]) -> list[str]:
    """Identify students who achieve an A grade equivalent or higher."""
    df = _students_to_dataframe(students)
    mask = df["composite_score"] >= GRADE_A_THRESHOLD
    return df.loc[mask, "name"].tolist()

def calculate_correlations(students: list[Student]) -> dict[str, float]:
    """Calculate the Pearson correlation between core metrics.
    
    Raises ValueError if there are fewer than 2 students.
    Note: An undefined correlation caused by zero variance is represented as 0.0 in this project's analytics output.
    """
    if len(students) < 2:
        app_logger.warning("Insufficient students to calculate correlations")
        raise ValueError("At least two students are required for correlation analysis.")
        
    df = _students_to_dataframe(students)
    corr_matrix = df[["marks", "attendance", "assignment_score"]].corr()
    
    # Fillna is useful because standard deviation might be 0 causing NaN correlation
    corr_matrix = corr_matrix.fillna(0)
    
    return {
        "marks_attendance": round(corr_matrix.loc["marks", "attendance"], 2),
        "marks_assignment": round(corr_matrix.loc["marks", "assignment_score"], 2),
        "attendance_assignment": round(corr_matrix.loc["attendance", "assignment_score"], 2),
    }

def find_strongest_correlation(correlations: dict[str, float]) -> tuple[str, float]:
    """Find the correlation pair with the largest absolute value."""
    if not correlations:
        raise ValueError("Correlations dictionary is empty.")
        
    best_pair = ""
    best_val = 0.0
    best_abs = -1.0
    
    for pair, val in correlations.items():
        if abs(val) > best_abs:
            best_abs = abs(val)
            best_val = val
            best_pair = pair
            
    return best_pair, best_val

def generate_performance_insights(students: list[Student]) -> list[str]:
    """Generate deterministic, human-readable insights based on analytical metrics."""
    if not students:
        return []

    insights = []
    
    # 1. Pass rate insight
    pass_fail = calculate_pass_fail_summary(students)
    pass_pct = pass_fail["pass_percentage"]
    insights.append(f"{pass_pct}% of students passed the course.")
    
    # 2. Attendance insight
    attendance = calculate_attendance_summary(students)
    below_req = int(attendance["below_required_attendance_count"])
    if below_req > 0:
        insights.append(f"{below_req} student(s) did not meet the {MIN_ATTENDANCE_THRESHOLD}% attendance threshold.")
    else:
        insights.append("All students met the required attendance threshold.")
        
    # 3. Risk insight
    at_risk = identify_at_risk_students(students)
    if at_risk:
        insights.append(f"{len(at_risk)} student(s) require academic attention.")
    
    # 4. Correlation insight
    try:
        corrs = calculate_correlations(students)
        strongest_pair, strongest_val = find_strongest_correlation(corrs)
        pair_desc = strongest_pair.replace("_", " vs ")
        insights.append(f"The strongest performance correlation is between {pair_desc} ({strongest_val}).")
    except ValueError:
        pass  # Skip correlation insight if < 2 students
        
    return insights
