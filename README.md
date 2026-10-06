# Student Performance Analyzer

![CI](https://github.com/TejasviBansal/Student-Performance-Analyzer/actions/workflows/ci.yml/badge.svg)

A Python application for managing student data and analyzing academic performance.

## Features

- Manual student data entry
- CSV import
- Student performance analysis
- Pandas-based analytics
- SQLite database
- FastAPI REST API
- Streamlit dashboard
- Data visualizations
- Automated testing with Pytest
- GitHub Actions CI

## Tech Stack

Python · Pandas · Matplotlib · Seaborn · SQLite · FastAPI · Pydantic · Streamlit · Pytest · GitHub Actions

## Project Structure

```text
Student-Performance-Analyzer/
├── api.py
├── api_client.py
├── streamlit_app.py
├── models.py
├── validators.py
├── calculations.py
├── analyzer.py
├── analytics.py
├── database.py
├── data_loader.py
├── visualizations.py
├── reports.py
├── logger.py
├── main.py
├── tests/
├── data/
├── requirements.txt
└── .github/
    └── workflows/
        └── ci.yml
```

## Run Locally

```bash
git clone https://github.com/TejasviBansal/Student-Performance-Analyzer.git
cd Student-Performance-Analyzer

pip install -r requirements.txt
```

### CLI

```bash
python main.py
```

### FastAPI

```bash
uvicorn api:app --reload
```

API documentation: http://127.0.0.1:8000/docs

### Streamlit

Start the FastAPI server first, then run:

```bash
streamlit run streamlit_app.py
```

## Testing

Run the complete test suite:

```bash
pytest
```

The project currently has 76 automated tests.

## Architecture

```
                Streamlit
                    │
                   HTTP
                    ▼
                 FastAPI
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
      SQLite              Analytics


CLI ──────────────► Core Modules ──────────────► SQLite
```

The Streamlit dashboard communicates with the FastAPI backend through `api_client.py`.

## CI

GitHub Actions automatically installs the project dependencies and runs the complete test suite on every push and pull request.
