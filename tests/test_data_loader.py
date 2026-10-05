import pytest
from data_loader import load_students_from_csv

def test_load_students_from_valid_csv(tmp_path):
    csv_file = tmp_path / "valid.csv"
    csv_file.write_text("name,marks,attendance,assignment_score\nAlice,90,95,90\nBob,80,85,80")
    
    students = load_students_from_csv(str(csv_file))
    assert len(students) == 2
    assert students[0].name == "Alice"
    assert students[1].name == "Bob"

def test_load_students_skips_invalid_rows(tmp_path):
    csv_file = tmp_path / "mixed.csv"
    csv_file.write_text("name,marks,attendance,assignment_score\nAlice,90,95,90\nInvalid,105,95,90\nBob,80,85,80\n")
    
    students = load_students_from_csv(str(csv_file))
    assert len(students) == 2
    assert students[0].name == "Alice"
    assert students[1].name == "Bob"

def test_load_students_missing_file():
    with pytest.raises(FileNotFoundError):
        load_students_from_csv("nonexistent_file.csv")

def test_load_students_missing_columns(tmp_path):
    csv_file = tmp_path / "missing_cols.csv"
    csv_file.write_text("name,marks\nAlice,90\n")
    
    with pytest.raises(ValueError, match="Missing required columns"):
        load_students_from_csv(str(csv_file))

def test_load_students_empty_csv(tmp_path):
    csv_file = tmp_path / "empty.csv"
    csv_file.write_text("")
    
    with pytest.raises(ValueError, match="No valid student records found"):
        load_students_from_csv(str(csv_file))
