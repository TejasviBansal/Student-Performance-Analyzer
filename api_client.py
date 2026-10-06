"""
api_client.py

Thin HTTP client for communicating between Streamlit and the FastAPI backend.

All data access for the Streamlit dashboard goes through this module.
Streamlit should not import database.py, analytics.py, or data_loader.py
for normal operations.
"""

import os

import requests

from logger import app_logger

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
REQUEST_TIMEOUT = 5  # seconds


class APIClientError(Exception):
    """Raised when the API client cannot complete a request."""


def _request(method: str, endpoint: str, **kwargs) -> dict | list:
    """Send an HTTP request and return the parsed JSON response.

    Raises APIClientError on connection failure, timeout, or HTTP error.
    """
    url = f"{API_BASE_URL}{endpoint}"
    kwargs.setdefault("timeout", REQUEST_TIMEOUT)

    try:
        response = requests.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        app_logger.error("API client: connection error reaching %s", url)
        raise APIClientError("Unable to connect to the FastAPI backend. Is the server running?")
    except requests.exceptions.Timeout:
        app_logger.error("API client: request to %s timed out", url)
        raise APIClientError("FastAPI request timed out. Please try again.")
    except requests.exceptions.HTTPError as e:
        status = e.response.status_code
        detail = ""
        try:
            detail = e.response.json().get("detail", "")
        except Exception:
            pass
        app_logger.error("API client: HTTP %d error for %s — %s", status, url, detail)
        raise APIClientError(f"HTTP {status}: {detail}" if detail else f"HTTP error {status}.")
    except requests.exceptions.RequestException as e:
        app_logger.exception("API client: unexpected error for %s", url)
        raise APIClientError(f"Unexpected error: {e}")


# ---------------------------------------------------------------------------
# Health
# ---------------------------------------------------------------------------

def get_health() -> dict:
    """GET /health"""
    return _request("GET", "/health")


# ---------------------------------------------------------------------------
# Students
# ---------------------------------------------------------------------------

def get_students() -> list:
    """GET /students — returns list of student records."""
    return _request("GET", "/students")


def get_student_count() -> int:
    """GET /students/count — returns total student count."""
    data = _request("GET", "/students/count")
    return data["count"]


def create_student(name: str, marks: float, attendance: float, assignment_score: float) -> dict:
    """POST /students — create one student."""
    payload = {
        "name": name,
        "marks": marks,
        "attendance": attendance,
        "assignment_score": assignment_score,
    }
    return _request("POST", "/students", json=payload)


def create_students_bulk(students: list[dict]) -> dict:
    """POST /students/bulk — create multiple students from a list of dicts."""
    return _request("POST", "/students/bulk", json=students)


def delete_all_students() -> dict:
    """DELETE /students — remove all student records."""
    return _request("DELETE", "/students")


# ---------------------------------------------------------------------------
# Analytics
# ---------------------------------------------------------------------------

def get_performance_summary() -> dict:
    """GET /analytics/performance"""
    return _request("GET", "/analytics/performance")


def get_pass_fail_summary() -> dict:
    """GET /analytics/pass-fail"""
    return _request("GET", "/analytics/pass-fail")


def get_grade_distribution() -> dict:
    """GET /analytics/grades"""
    return _request("GET", "/analytics/grades")


def get_attendance_summary() -> dict:
    """GET /analytics/attendance"""
    return _request("GET", "/analytics/attendance")


def get_score_distribution() -> dict:
    """GET /analytics/scores"""
    return _request("GET", "/analytics/scores")


def get_performance_categories() -> dict:
    """GET /analytics/categories"""
    return _request("GET", "/analytics/categories")


def get_at_risk_students() -> list:
    """GET /analytics/at-risk — returns list of at-risk student names."""
    return _request("GET", "/analytics/at-risk")


def get_high_performers() -> list:
    """GET /analytics/high-performers — returns list of high-performer names."""
    return _request("GET", "/analytics/high-performers")


def get_correlations() -> dict:
    """GET /analytics/correlations"""
    return _request("GET", "/analytics/correlations")


def get_strongest_correlation() -> dict:
    """GET /analytics/strongest-correlation — returns {pair, value}."""
    return _request("GET", "/analytics/strongest-correlation")


def get_performance_insights() -> list[str]:
    """GET /analytics/insights — returns list of insight strings."""
    data = _request("GET", "/analytics/insights")
    return data["insights"]
