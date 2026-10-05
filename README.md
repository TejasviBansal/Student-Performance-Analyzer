# Student Performance Analyzer

## Features
- Manual student data entry
- CSV data import
- Pandas-based data processing
- Input/data validation
- Student performance reporting
- Advanced student analytics (Pandas-based)
- SQLite database persistence

## Project Structure
- `models.py` → data models (Student dataclass)
- `validators.py` → input validation
- `calculations.py` → calculation/business rules
- `analyzer.py` → analytical logic
- `analytics.py` → advanced pandas analytics functions
- `visualizations.py` → matplotlib/seaborn charting functions
- `database.py` → SQLite persistence (CRUD operations)
- `reports.py` → console reporting
- `data_loader.py` → CSV loading and pandas processing
- `main.py` → application entry point

## CSV Format
The expected CSV format contains the following columns:
`name,marks,attendance,assignment_score`

- marks: 0–100
- attendance: 0–100
- assignment_score: 0–100

Invalid rows will automatically be skipped during loading.

## Running the Application
Run the main script:
```bash
python main.py
```

## CSV Import
You can select the CSV import mode from the application menu. 
Provide a custom CSV path or press Enter to use the default `data/student_data.csv`.

## Analytics
The application computes advanced analytics on the student data using Pandas:
- Overall performance summary (mean, median, max, min)
- Pass/Fail distribution
- Grade distribution
- Attendance analysis
- Score distribution mapping
- Categorical performance mapping
- At-risk student identification
- High performers identification
- Metric correlation analysis
- Automated deterministic analytical insights

## Data Visualization

The project uses Matplotlib and Seaborn to visualize student performance. Generated charts are saved to the `output/` directory, which is ignored by Git.

Available visualizations:
- Grade distribution
- Score distribution
- Performance categories
- Marks vs attendance
- Marks vs assignment score

## SQLite Database

The application uses SQLite for persistent student data storage.

The database stores:
- student name
- marks
- attendance
- assignment score

Derived metrics such as grade, status, composite score, and performance categories are calculated by the application rather than stored in the database.

The database file `data/students.db` is generated locally and ignored by Git.
