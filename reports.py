from models import Student
from calculations import (
    calculate_average,
    calculate_grade,
    calculate_status,
)
from analyzer import find_top_performers
import analytics
from visualizations import generate_all_visualizations

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

    # ── Advanced Analytics ───────────────────────────────────────
    if students:
        print("\n" + "-" * 40)
        print("Advanced Analytics")
        print("-" * 40)
        
        # Overall Performance
        perf_summary = analytics.calculate_performance_summary(students)
        print("\nOverall Performance")
        print(f"- Average marks: {perf_summary['average_marks']}")
        print(f"- Median marks: {perf_summary['median_marks']}")
        print(f"- Highest marks: {perf_summary['highest_marks']}")
        print(f"- Lowest marks: {perf_summary['lowest_marks']}")
        print(f"- Average assignment: {perf_summary['average_assignment_score']}")
        print(f"- Average attendance: {perf_summary['average_attendance']}")

        # Pass/Fail
        pf_summary = analytics.calculate_pass_fail_summary(students)
        print("\nPass/Fail")
        print(f"- Pass count: {pf_summary['pass_count']}")
        print(f"- Fail count: {pf_summary['fail_count']}")
        print(f"- Pass percentage: {pf_summary['pass_percentage']}")
        print(f"- Fail percentage: {pf_summary['fail_percentage']}")

        # Grade Distribution
        grades = analytics.calculate_grade_distribution(students)
        print("\nGrade Distribution")
        for grade in ["A", "B", "C", "D", "E"]:
            print(f"- {grade}: {grades.get(grade, 0)}")

        # Attendance
        att_summary = analytics.calculate_attendance_summary(students)
        print("\nAttendance")
        print(f"- Average attendance: {att_summary['average_attendance']}")
        print(f"- Below required attendance count: {att_summary['below_required_attendance_count']}")
        print(f"- Below required attendance percentage: {att_summary['below_required_attendance_percentage']}")

        # Score Distribution
        score_dist = analytics.calculate_score_distribution(students)
        print("\nScore Distribution")
        for rng in ["90+", "80-89.99", "70-79.99", "60-69.99", "50-59.99", "Below 50"]:
            print(f"- {rng}: {score_dist.get(rng, 0)}")

        # Performance Categories
        categories = analytics.calculate_performance_categories(students)
        print("\nPerformance Categories")
        for cat in ["Excellent", "Good", "Average", "Needs Improvement", "Critical"]:
            print(f"- {cat}: {categories.get(cat, 0)}")

        # At-Risk Students
        at_risk = analytics.identify_at_risk_students(students)
        print("\nAt-Risk Students")
        if at_risk:
            for name in at_risk:
                print(f"- {name}")
        else:
            print("- None")

        # High Performers
        high_perf = analytics.identify_high_performers(students)
        print("\nHigh Performers")
        if high_perf:
            for name in high_perf:
                print(f"- {name}")
        else:
            print("- None")

        # Correlations
        print("\nCorrelations")
        try:
            corrs = analytics.calculate_correlations(students)
            print(f"- Marks vs Attendance: {corrs['marks_attendance']}")
            print(f"- Marks vs Assignment: {corrs['marks_assignment']}")
            print(f"- Attendance vs Assignment: {corrs['attendance_assignment']}")
        except ValueError:
            print("- Not enough students for correlation analysis")

        # Insights
        insights = analytics.generate_performance_insights(students)
        print("\nInsights")
        if insights:
            for insight in insights:
                print(f"- {insight}")
        else:
            print("- No insights available")

        # ── Visualizations ───────────────────────────────────────────
        print("\n" + "-" * 40)
        print("Visualizations")
        print("-" * 40)
        
        generate_all_visualizations(students)
        print("Charts generated successfully in: output/")
