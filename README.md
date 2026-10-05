# Student Performance Analyzer

## Features
- Manual student data entry
- CSV data import
- Pandas-based data processing
- Input/data validation
- Student performance reporting
- Advanced student analytics (Pandas-based)

## Project Structure
- `models.py` → data models (Student dataclass)
- `validators.py` → input validation
- `calculations.py` → calculation/business rules
- `analyzer.py` → analytical logic
- `analytics.py` → advanced pandas analytics functions
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
