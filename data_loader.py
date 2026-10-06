from pathlib import Path
import pandas as pd
from logger import app_logger
from models import Student

REQUIRED_COLUMNS: set[str] = {
    "name",
    "marks",
    "attendance",
    "assignment_score",
}

def load_students_from_csv(file_path: str) -> list[Student]:
    """Load students from a CSV file using Pandas.
    
    Reads the CSV, validates required columns, cleans string fields, 
    validates numeric fields, and drops invalid rows gracefully.
    Returns a list of clean Student objects.
    """
    path = Path(file_path)
    app_logger.info("Loading student data from %s", file_path)
    if not path.exists():
        app_logger.error("CSV file not found: %s", file_path)
        raise FileNotFoundError(f"Student data file not found: {file_path}")
    
    try:
        dataframe = pd.read_csv(path)
    except pd.errors.EmptyDataError:
        raise ValueError("No valid student records found in the CSV file.")

    # Normalize column names
    dataframe.columns = dataframe.columns.str.strip()

    missing_columns = REQUIRED_COLUMNS - set(dataframe.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(list(missing_columns))}")

    # Clean the name column
    dataframe["name"] = dataframe["name"].astype("string").str.strip()

    # Convert numeric columns
    for col in ["marks", "attendance", "assignment_score"]:
        dataframe[col] = pd.to_numeric(dataframe[col], errors="coerce")

    # Find valid rows
    valid_rows = (
        dataframe["name"].notna()
        & dataframe["name"].ne("")
        & dataframe["marks"].between(0, 100)
        & dataframe["attendance"].between(0, 100)
        & dataframe["assignment_score"].between(0, 100)
    )

    invalid_count = (~valid_rows).sum()
    total_count = len(dataframe)
    valid_count = valid_rows.sum()

    print(f"Loaded {total_count} rows.")
    print(f"Valid rows: {valid_count}.")
    print(f"Skipped invalid rows: {invalid_count}.")

    if invalid_count > 0:
        app_logger.warning("Skipped %d invalid student row(s)", invalid_count)

    if valid_count == 0:
        app_logger.error("No valid student records found in the CSV file.")
        raise ValueError("No valid student records found in the CSV file.")

    app_logger.info("Loaded %d valid students from CSV", valid_count)

    clean_df = dataframe.loc[valid_rows].copy()

    students = []
    for _, row in clean_df.iterrows():
        students.append(
            Student(
                name=row["name"],
                marks=float(row["marks"]),
                attendance=float(row["attendance"]),
                assignment_score=float(row["assignment_score"])
            )
        )

    return students
