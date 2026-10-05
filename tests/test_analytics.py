import pytest
from models import Student
from analytics import (
    calculate_performance_summary,
    calculate_pass_fail_summary,
    calculate_grade_distribution,
    calculate_attendance_summary,
    calculate_score_distribution,
    calculate_performance_categories,
    identify_at_risk_students,
    identify_high_performers,
    calculate_correlations,
    find_strongest_correlation,
    generate_performance_insights,
)

@pytest.fixture
def sample_students():
    return [
        Student("Alice", 90, 95, 90),     # A, Excellent, Pass
        Student("Bob", 80, 85, 80),       # B, Good, Pass
        Student("Charlie", 70, 75, 70),   # C, Average, Pass
        Student("David", 60, 65, 60),
        Student("Eve", 40, 50, 40),
    ]

def test_calculate_performance_summary(sample_students):
    summary = calculate_performance_summary(sample_students)
    assert summary["total_students"] == 5
    assert summary["average_marks"] == pytest.approx(68.0)
    assert summary["average_attendance"] == pytest.approx(74.0)
    assert summary["average_assignment_score"] == pytest.approx(68.0)
    assert summary["highest_marks"] == 90.0
    assert summary["lowest_marks"] == 40.0

def test_calculate_pass_fail_summary(sample_students):
    summary = calculate_pass_fail_summary(sample_students)
    assert summary["pass_count"] + summary["fail_count"] == 5
    assert summary["pass_percentage"] + summary["fail_percentage"] == 100.0
    
    # David passed marks (60>=40) but failed attendance (65<75) -> Fail
    # Eve passed marks (40>=40) but failed attendance (50<75) -> Fail
    # Alice, Bob, Charlie pass.
    assert summary["pass_count"] == 3
    assert summary["fail_count"] == 2

def test_calculate_grade_distribution(sample_students):
    dist = calculate_grade_distribution(sample_students)
    assert dist["A"] == 1
    assert dist["B"] == 2
    assert dist["C"] == 1
    assert dist["D"] == 1
    assert dist["E"] == 0
    assert sum(dist.values()) == 5

def test_calculate_attendance_summary(sample_students):
    summary = calculate_attendance_summary(sample_students)
    assert summary["average_attendance"] == pytest.approx(74.0)
    assert summary["below_required_attendance_count"] == 2  # David and Eve

def test_calculate_score_distribution(sample_students):
    dist = calculate_score_distribution(sample_students)
    assert dist["90+"] == 1
    assert dist["80-89.99"] == 1
    assert dist["70-79.99"] == 1
    assert dist["60-69.99"] == 1
    assert dist["Below 50"] == 1
    assert sum(dist.values()) == 5

def test_calculate_performance_categories(sample_students):
    cats = calculate_performance_categories(sample_students)
    assert cats["Excellent"] == 1
    assert cats["Good"] == 2
    assert cats["Average"] == 1
    assert sum(cats.values()) == 5

def test_identify_at_risk_students(sample_students):
    at_risk = identify_at_risk_students(sample_students)
    assert "David" in at_risk
    assert "Eve" in at_risk
    assert "Alice" not in at_risk

def test_identify_high_performers(sample_students):
    high_perf = identify_high_performers(sample_students)
    assert "Alice" in high_perf
    assert "Bob" not in high_perf

def test_calculate_correlations(sample_students):
    corrs = calculate_correlations(sample_students)
    assert "marks_attendance" in corrs
    assert "marks_assignment" in corrs
    assert "attendance_assignment" in corrs
    assert isinstance(float(corrs["marks_attendance"]), float)

def test_calculate_correlations_insufficient_data():
    with pytest.raises(ValueError):
        calculate_correlations([Student("Alone", 90, 90, 90)])

def test_find_strongest_correlation():
    corrs = {
        "marks_attendance": 0.5,
        "marks_assignment": -0.9,
        "attendance_assignment": 0.2
    }
    pair, val = find_strongest_correlation(corrs)
    assert pair == "marks_assignment"
    assert val == -0.9

def test_find_strongest_correlation_empty():
    with pytest.raises(ValueError):
        find_strongest_correlation({})

def test_generate_performance_insights(sample_students):
    insights = generate_performance_insights(sample_students)
    assert type(insights) is list
    assert len(insights) > 0
    # Just checking that it generates something coherent without brittle string matching
    assert any("students passed the course" in insight for insight in insights)
