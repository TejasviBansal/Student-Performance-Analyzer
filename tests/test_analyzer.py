from models import Student
from analyzer import find_top_performers

def test_find_top_performers_single_clear_winner():
    students = [
        Student("A", 90, 90, 90),
        Student("B", 80, 80, 80),
        Student("C", 70, 70, 70),
    ]
    top_performers = find_top_performers(students)
    assert len(top_performers) == 1
    assert top_performers[0] == "A"

def test_find_top_performers_tied():
    students = [
        Student("A", 90, 90, 90),
        Student("B", 90, 90, 90),  # Tied with A
        Student("C", 80, 80, 80),
    ]
    top_performers = find_top_performers(students)
    assert len(top_performers) == 2
    assert "A" in top_performers
    assert "B" in top_performers
    assert "C" not in top_performers

def test_find_top_performers_single_student():
    students = [
        Student("A", 75, 80, 70),
    ]
    top_performers = find_top_performers(students)
    assert len(top_performers) == 1
    assert top_performers[0] == "A"

def test_find_top_performers_empty_list():
    assert find_top_performers([]) == []
