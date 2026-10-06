"""
tests/test_api_client.py

Unit tests for api_client.py.

All tests use unittest.mock — no running FastAPI server is required.
"""

from unittest.mock import patch, MagicMock

import pytest
import requests

import api_client
from api_client import APIClientError


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _mock_response(json_data, status_code=200):
    """Create a mock requests.Response with given JSON and status code."""
    mock = MagicMock()
    mock.json.return_value = json_data
    mock.status_code = status_code
    if status_code >= 400:
        http_error = requests.exceptions.HTTPError(response=mock)
        mock.raise_for_status.side_effect = http_error
    else:
        mock.raise_for_status.return_value = None
    return mock


# ---------------------------------------------------------------------------
# _request helper tests
# ---------------------------------------------------------------------------

class TestRequest:
    def test_successful_get_returns_json(self):
        with patch("requests.request") as mock_req:
            mock_req.return_value = _mock_response({"status": "ok"})
            result = api_client._request("GET", "/health")
        assert result == {"status": "ok"}

    def test_connection_error_raises_api_client_error(self):
        with patch("requests.request") as mock_req:
            mock_req.side_effect = requests.exceptions.ConnectionError()
            with pytest.raises(APIClientError, match="Unable to connect"):
                api_client._request("GET", "/health")

    def test_timeout_raises_api_client_error(self):
        with patch("requests.request") as mock_req:
            mock_req.side_effect = requests.exceptions.Timeout()
            with pytest.raises(APIClientError, match="timed out"):
                api_client._request("GET", "/health")

    def test_http_error_raises_api_client_error(self):
        with patch("requests.request") as mock_req:
            mock_req.return_value = _mock_response({"detail": "Not found"}, status_code=404)
            with pytest.raises(APIClientError, match="404"):
                api_client._request("GET", "/students")

    def test_uses_timeout(self):
        with patch("requests.request") as mock_req:
            mock_req.return_value = _mock_response({})
            api_client._request("GET", "/health")
            _, kwargs = mock_req.call_args
            assert kwargs.get("timeout") == api_client.REQUEST_TIMEOUT


# ---------------------------------------------------------------------------
# Student function tests
# ---------------------------------------------------------------------------

class TestStudentFunctions:
    def test_get_health(self):
        with patch("api_client._request") as mock_req:
            mock_req.return_value = {"status": "ok"}
            result = api_client.get_health()
        assert result == {"status": "ok"}
        mock_req.assert_called_once_with("GET", "/health")

    def test_get_students_returns_list(self):
        students = [{"id": 1, "name": "Alice", "marks": 85.0, "attendance": 90.0, "assignment_score": 80.0}]
        with patch("api_client._request") as mock_req:
            mock_req.return_value = students
            result = api_client.get_students()
        assert result == students

    def test_get_student_count_extracts_count(self):
        with patch("api_client._request") as mock_req:
            mock_req.return_value = {"count": 5}
            result = api_client.get_student_count()
        assert result == 5

    def test_create_student_sends_correct_payload(self):
        with patch("api_client._request") as mock_req:
            mock_req.return_value = {"message": "Student added successfully"}
            result = api_client.create_student("Alice", 85.0, 90.0, 80.0)
        mock_req.assert_called_once_with(
            "POST",
            "/students",
            json={"name": "Alice", "marks": 85.0, "attendance": 90.0, "assignment_score": 80.0},
        )

    def test_create_students_bulk_sends_list(self):
        payload = [{"name": "Bob", "marks": 70.0, "attendance": 80.0, "assignment_score": 75.0}]
        with patch("api_client._request") as mock_req:
            mock_req.return_value = {"message": "Students added", "count": 1}
            api_client.create_students_bulk(payload)
        mock_req.assert_called_once_with("POST", "/students/bulk", json=payload)

    def test_delete_all_students_sends_delete(self):
        with patch("api_client._request") as mock_req:
            mock_req.return_value = {"message": "All students deleted successfully"}
            api_client.delete_all_students()
        mock_req.assert_called_once_with("DELETE", "/students")


# ---------------------------------------------------------------------------
# Analytics function tests
# ---------------------------------------------------------------------------

class TestAnalyticsFunctions:
    def test_get_performance_summary(self):
        expected = {"average_marks": 80.0}
        with patch("api_client._request") as mock_req:
            mock_req.return_value = expected
            result = api_client.get_performance_summary()
        assert result == expected

    def test_get_pass_fail_summary(self):
        expected = {"pass_count": 4, "fail_count": 1}
        with patch("api_client._request") as mock_req:
            mock_req.return_value = expected
            result = api_client.get_pass_fail_summary()
        assert result == expected

    def test_get_at_risk_students_returns_list(self):
        with patch("api_client._request") as mock_req:
            mock_req.return_value = ["Charlie"]
            result = api_client.get_at_risk_students()
        assert result == ["Charlie"]

    def test_get_performance_insights_extracts_list(self):
        with patch("api_client._request") as mock_req:
            mock_req.return_value = {"insights": ["80% passed.", "Good attendance."]}
            result = api_client.get_performance_insights()
        assert result == ["80% passed.", "Good attendance."]

    def test_get_strongest_correlation_returns_dict(self):
        expected = {"pair": "marks_attendance", "value": 0.95}
        with patch("api_client._request") as mock_req:
            mock_req.return_value = expected
            result = api_client.get_strongest_correlation()
        assert result == expected

    def test_api_client_error_propagates(self):
        with patch("api_client._request") as mock_req:
            mock_req.side_effect = APIClientError("Unable to connect")
            with pytest.raises(APIClientError):
                api_client.get_performance_summary()
