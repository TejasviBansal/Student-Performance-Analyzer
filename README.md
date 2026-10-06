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
- `api.py` → FastAPI REST API
- `logger.py` → Application logging configuration
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
- `data/` → default directory for CSV data files
- `output/` → directory for generated charts
- `logs/` → generated application logs (ignored by Git)
- `tests/` → Pytest automated test suite

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

## REST API

The project includes a FastAPI REST API for accessing student data and performance analytics.

Run the API:
```bash
uvicorn api:app --reload
```

API documentation:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

Endpoint Groups:
- **Health Check**: Verify API is running (`/health`)
- **Student Management**: Create, read, and delete student records (`/students`)
- **Analytics**: Access all derived performance metrics and insights (`/analytics/...`)

## Streamlit Dashboard

The project includes a Streamlit dashboard that provides interactive student performance analysis. It displays analytics and visualizations, and supports adding students and CSV imports directly through a web interface.

Run the dashboard:
```bash
streamlit run streamlit_app.py
```

*Note: The dashboard currently accesses the existing Python modules directly. API integration is planned for a later phase.*

## Testing

Run the automated test suite:

```bash
pytest
```

Optionally, for more detail:
```bash
pytest -v
```

## Logging

The project uses Python's built-in `logging` module to track application events and errors without replacing normal user-facing CLI output.

- Logs are written to `logs/app.log`.
- The `logs/` directory is ignored by Git.
- INFO, WARNING, and ERROR levels are used for recording important application events.
