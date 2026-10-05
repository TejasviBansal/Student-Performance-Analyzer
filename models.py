from dataclasses import dataclass


@dataclass
class Student:
    """Represents a single student's raw academic data."""

    name: str
    marks: float
    attendance: float
    assignment_score: float
