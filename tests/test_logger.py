import logging
from pathlib import Path

from logger import app_logger

def test_logger_configuration_exists():
    """Verify that the dedicated app_logger is exposed with expected name."""
    assert app_logger.name == "student_performance_analyzer"

def test_log_directory_and_file_exist():
    """Verify that the logs directory and app.log file are created."""
    log_dir = Path("logs")
    log_file = log_dir / "app.log"
    
    # Check that they exist
    assert log_dir.exists()
    assert log_dir.is_dir()
    assert log_file.exists()
    assert log_file.is_file()

def test_log_message_can_be_written():
    """Verify that an INFO log message can be written to the log file."""
    test_message = "Test log message for verification"
    
    # Write a message using the dedicated logger
    app_logger.info(test_message)
    
    # Read the log file and verify the message is present
    log_file = Path("logs/app.log")
    content = log_file.read_text(encoding="utf-8")
    
    assert test_message in content
