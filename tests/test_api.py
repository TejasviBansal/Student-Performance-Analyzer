import pytest
from fastapi.testclient import TestClient

import database
from api import app

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_test_db(tmp_path):
    """Isolate API tests with a temporary database."""
    original_path = database.DATABASE_PATH
    test_db_path = tmp_path / "api_test_students.db"
    database.DATABASE_PATH = test_db_path
    
    # Initialize fresh DB per test
    database.initialize_database()
    
    yield
    
    # Restore standard DB path
    database.DATABASE_PATH = original_path

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_students_empty():
    response = client.get("/students")
    assert response.status_code == 200
    assert response.json() == []

def test_get_students_count_empty():
    response = client.get("/students/count")
    assert response.status_code == 200
    assert response.json() == {"count": 0}

def test_analytics_empty_db_returns_404():
    response = client.get("/analytics/performance")
    assert response.status_code == 404
    assert response.json() == {"detail": "No student data available."}

def test_create_student():
    payload = {"name": "Alice", "marks": 85, "attendance": 90, "assignment_score": 88}
    response = client.post("/students", json=payload)
    assert response.status_code == 200
    
    response = client.get("/students/count")
    assert response.json() == {"count": 1}

def test_create_student_invalid_data():
    payload = {"name": "", "marks": 105, "attendance": -5, "assignment_score": 50}
    response = client.post("/students", json=payload)
    assert response.status_code == 422

def test_bulk_create_students():
    payload = [
        {"name": "Alice", "marks": 90, "attendance": 95, "assignment_score": 90},
        {"name": "Bob", "marks": 80, "attendance": 85, "assignment_score": 80},
    ]
    response = client.post("/students/bulk", json=payload)
    assert response.status_code == 200
    assert response.json()["count"] == 2
    
    response = client.get("/students/count")
    assert response.json() == {"count": 2}

def test_delete_all_students():
    payload = {"name": "Alice", "marks": 85, "attendance": 90, "assignment_score": 88}
    client.post("/students", json=payload)
    assert client.get("/students/count").json() == {"count": 1}
    
    response = client.delete("/students")
    assert response.status_code == 200
    assert client.get("/students/count").json() == {"count": 0}

@pytest.fixture
def populate_db():
    payload = [
        {"name": "Alice", "marks": 90, "attendance": 95, "assignment_score": 90},
        {"name": "Bob", "marks": 80, "attendance": 85, "assignment_score": 80},
        {"name": "Charlie", "marks": 70, "attendance": 75, "assignment_score": 70},
    ]
    client.post("/students/bulk", json=payload)

def test_analytics_performance(populate_db):
    response = client.get("/analytics/performance")
    assert response.status_code == 200
    data = response.json()
    assert data["total_students"] == 3
    assert "average_marks" in data

def test_analytics_pass_fail(populate_db):
    response = client.get("/analytics/pass-fail")
    assert response.status_code == 200
    data = response.json()
    assert data["pass_count"] + data["fail_count"] == 3

def test_analytics_correlations(populate_db):
    response = client.get("/analytics/correlations")
    assert response.status_code == 200
    data = response.json()
    assert "marks_attendance" in data

def test_analytics_correlations_insufficient_data():
    payload = {"name": "Alice", "marks": 85, "attendance": 90, "assignment_score": 88}
    client.post("/students", json=payload)
    
    response = client.get("/analytics/correlations")
    assert response.status_code == 400

def test_analytics_grades(populate_db):
    response = client.get("/analytics/grades")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_analytics_attendance(populate_db):
    response = client.get("/analytics/attendance")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_analytics_scores(populate_db):
    response = client.get("/analytics/scores")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_analytics_categories(populate_db):
    response = client.get("/analytics/categories")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_analytics_at_risk(populate_db):
    response = client.get("/analytics/at-risk")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_analytics_high_performers(populate_db):
    response = client.get("/analytics/high-performers")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_analytics_strongest_correlation(populate_db):
    response = client.get("/analytics/strongest-correlation")
    assert response.status_code == 200
    data = response.json()
    assert "pair" in data
    assert "value" in data

def test_analytics_insights(populate_db):
    response = client.get("/analytics/insights")
    assert response.status_code == 200
    data = response.json()
    assert "insights" in data
    assert isinstance(data["insights"], list)
