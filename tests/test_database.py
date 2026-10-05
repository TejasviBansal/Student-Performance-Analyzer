import pytest
import sqlite3
from pathlib import Path
from models import Student
import database

@pytest.fixture
def temp_db(tmp_path):
    """Fixture to create a temporary database for testing."""
    # Save the original path
    original_path = database.DATABASE_PATH
    
    # Point to a temporary file
    test_db_path = tmp_path / "test_students.db"
    database.DATABASE_PATH = test_db_path
    
    # Initialize the temporary database
    database.initialize_database()
    
    yield test_db_path
    
    # Restore the original path after the test
    database.DATABASE_PATH = original_path

def test_initialize_database(temp_db):
    assert temp_db.exists()
    
    with sqlite3.connect(temp_db) as conn:
        tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='students'").fetchall()
        assert len(tables) == 1

def test_add_student(temp_db):
    student = Student("Test", 85, 90, 88)
    database.add_student(student)
    assert database.count_students() == 1

def test_add_students(temp_db):
    students = [
        Student("A", 90, 90, 90),
        Student("B", 80, 80, 80),
    ]
    database.add_students(students)
    assert database.count_students() == 2

def test_get_all_students(temp_db):
    database.add_student(Student("Alice", 95, 95, 95))
    students = database.get_all_students()
    
    assert len(students) == 1
    assert type(students[0]) is Student
    assert students[0].name == "Alice"

def test_get_all_student_records(temp_db):
    database.add_student(Student("Bob", 85, 85, 85))
    records = database.get_all_student_records()
    
    assert len(records) == 1
    assert type(records[0]) is dict
    assert "id" in records[0]
    assert records[0]["name"] == "Bob"

def test_delete_all_students(temp_db):
    database.add_student(Student("Charlie", 70, 70, 70))
    assert database.count_students() == 1
    
    database.delete_all_students()
    assert database.count_students() == 0

def test_empty_database_returns_empty_list(temp_db):
    assert database.get_all_students() == []
    assert database.get_all_student_records() == []
    assert database.count_students() == 0
