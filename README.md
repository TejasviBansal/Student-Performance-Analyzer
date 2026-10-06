# Student Performance Analyzer

![CI](https://github.com/TejasviBansal/Student-Performance-Analyzer/actions/workflows/ci.yml/badge.svg)

A Python application for managing student data and analyzing academic performance.

## Live Demo

- [Streamlit Dashboard](https://student-performance-analyzer-mdxkjyarjfetavak3zp4z6.streamlit.app)
- [FastAPI API](https://student-performance-api-b6sc.onrender.com)
- [API Documentation](https://student-performance-api-b6sc.onrender.com/docs)

*Note: The Streamlit dashboard communicates directly with the FastAPI backend.*

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
- Application logging
- GitHub Actions CI
- Cloud deployment

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

The project currently has 76 automated tests that pass. GitHub Actions automatically runs the test suite on every push and pull request.

## Architecture

```text
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

## Deployment

The project is deployed across two platforms:
- **FastAPI backend**: Deployed on Render.
- **Streamlit dashboard**: Deployed on Streamlit Community Cloud.

**Important Note**: SQLite is used for this project and the deployed Render service uses ephemeral storage, so database data should be treated as demo data and is not guaranteed to persist across service restarts or redeployments.

## Project Highlights

- Modular Python architecture
- REST API with FastAPI
- Streamlit frontend consuming the API
- Automated tests with Pytest
- Centralized application logging
- CI/CD workflow with GitHub Actions
