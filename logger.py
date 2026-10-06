import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "app.log"

def setup_logger() -> logging.Logger:
    """Configure the standard application logger."""
    LOG_DIR.mkdir(exist_ok=True)
    
    logger = logging.getLogger("student_performance_analyzer")
    logger.setLevel(logging.INFO)
    
    # Prevent duplicate handlers
    if not logger.handlers:
        file_handler = logging.FileHandler(LOG_FILE)
        
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Prevent propagation to root logger to avoid duplicate console output in frameworks
        logger.propagate = False
        
    return logger

app_logger = setup_logger()
