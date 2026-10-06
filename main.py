from models import Student
from reports import student_report
from data_loader import load_students_from_csv
from validators import (
    get_valid_float,
    get_valid_integer,
    get_valid_name,
    MAX_SCORE,
    MAX_STUDENTS,
    MIN_SCORE,
    MIN_STUDENTS,
)
import database
from logger import app_logger


def collect_manual_students() -> list[Student]:
    """Collect student details interactively with input validation."""
    students: list[Student] = []

    print("-" * 60)
    print("ENTER STUDENT DETAILS")
    print("-" * 60)

    no_of_students = get_valid_integer(
        "Enter number of students: ", MIN_STUDENTS, MAX_STUDENTS
    )

    for student_index in range(no_of_students):
        print(f"\nEnter details for student {student_index + 1}")
        print("---------------------------")

        name = get_valid_name("Enter the student name: ")
        marks = get_valid_float("Enter the student marks: ", MIN_SCORE, MAX_SCORE)
        attendance = get_valid_float(
            "Enter the student attendance: ", MIN_SCORE, MAX_SCORE
        )
        assignment_score = get_valid_float(
            "Enter the student assignment score: ", MIN_SCORE, MAX_SCORE
        )

        students.append(
            Student(
                name=name,
                marks=marks,
                attendance=attendance,
                assignment_score=assignment_score,
            )
        )

    return students


def collect_csv_students() -> list[Student]:
    """Collect student details from a CSV file."""
    print("-" * 60)
    print("LOAD CSV DATA")
    print("-" * 60)
    
    file_path = input(
        "Enter CSV file path\nPress Enter to use the default:\ndata/student_data.csv\n> "
    ).strip()
    
    if not file_path:
        file_path = "data/student_data.csv"
        
    try:
        return load_students_from_csv(file_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return []
    except ValueError as e:
        print(f"Error: {e}")
        return []


def collect_database_students() -> list[Student]:
    """Retrieve students from the SQLite database."""
    print("-" * 60)
    print("LOAD DATABASE DATA")
    print("-" * 60)

    students = database.get_all_students()

    if not students:
        print("No students found in the database.")

    return students


def import_csv_to_database() -> None:
    """Load students from CSV and insert them into the database."""
    print("-" * 60)
    print("IMPORT CSV INTO DATABASE")
    print("-" * 60)

    file_path = input(
        "Enter CSV file path\nPress Enter to use the default:\ndata/student_data.csv\n> "
    ).strip()

    if not file_path:
        file_path = "data/student_data.csv"

    try:
        students = load_students_from_csv(file_path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    except ValueError as e:
        print(f"Error: {e}")
        return

    if not students:
        print("No valid students found in the CSV file.")
        return

    database.add_students(students)
    print(f"Successfully imported {len(students)} students into the database.")


def main() -> None:
    """Main application loop."""
    app_logger.info("Student Performance Analyzer started")
    database.initialize_database()

    while True:
        print("-" * 40)
        print("STUDENT PERFORMANCE ANALYZER")
        print("-" * 40)
        print("1. Enter student details manually")
        print("2. Load student data from CSV")
        print("3. Load student data from Database")
        print("4. Import CSV into Database")
        print("5. Exit")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == "1":
            app_logger.info("User selected manual input")
            students = collect_manual_students()
            if students:
                student_report(students)
        elif choice == "2":
            app_logger.info("User selected CSV input")
            students = collect_csv_students()
            if students:
                student_report(students)
        elif choice == "3":
            app_logger.info("User selected database input")
            students = collect_database_students()
            if students:
                student_report(students)
        elif choice == "4":
            app_logger.info("User selected CSV import")
            import_csv_to_database()
        elif choice == "5":
            app_logger.info("Student Performance Analyzer exited")
            print("Exiting...")
            return
        else:
            print("Invalid choice. Please select 1, 2, 3, 4, or 5.")


if __name__ == "__main__":
    main()