from pathlib import Path
from logger import app_logger

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from models import Student
import analytics

OUTPUT_DIR = Path("output")


def plot_grade_distribution(students: list[Student]) -> None:
    """Create and save a grade distribution chart."""
    distribution = analytics.calculate_grade_distribution(students)
    grades = list(distribution.keys())
    counts = list(distribution.values())

    plt.figure(figsize=(8, 5))
    sns.barplot(x=grades, y=counts, hue=grades, legend=False, palette="viridis")

    plt.title("Grade Distribution")
    plt.xlabel("Grade")
    plt.ylabel("Number of Students")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUTPUT_DIR / "grade_distribution.png", bbox_inches="tight")
    plt.close()


def plot_score_distribution(students: list[Student]) -> None:
    """Create and save a score distribution chart."""
    distribution = analytics.calculate_score_distribution(students)
    ranges = list(distribution.keys())
    counts = list(distribution.values())

    plt.figure(figsize=(8, 5))
    sns.barplot(x=ranges, y=counts, hue=ranges, legend=False, palette="magma")

    plt.title("Score Distribution")
    plt.xlabel("Score Range")
    plt.ylabel("Number of Students")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUTPUT_DIR / "score_distribution.png", bbox_inches="tight")
    plt.close()


def plot_performance_categories(students: list[Student]) -> None:
    """Create and save a performance categories chart."""
    categories_dict = analytics.calculate_performance_categories(students)
    categories = list(categories_dict.keys())
    counts = list(categories_dict.values())

    plt.figure(figsize=(10, 5))
    sns.barplot(x=categories, y=counts, hue=categories, legend=False, palette="coolwarm")

    plt.title("Student Performance Categories")
    plt.xlabel("Performance Category")
    plt.ylabel("Number of Students")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUTPUT_DIR / "performance_categories.png", bbox_inches="tight")
    plt.close()


def plot_marks_vs_attendance(students: list[Student]) -> None:
    """Create and save a marks vs attendance scatter plot."""
    df = pd.DataFrame({
        "Attendance (%)": [s.attendance for s in students],
        "Marks": [s.marks for s in students],
    })

    plt.figure(figsize=(8, 5))
    sns.regplot(data=df, x="Attendance (%)", y="Marks", scatter_kws={"alpha": 0.6})

    plt.title("Marks vs Attendance")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUTPUT_DIR / "marks_vs_attendance.png", bbox_inches="tight")
    plt.close()


def plot_marks_vs_assignment(students: list[Student]) -> None:
    """Create and save a marks vs assignment score scatter plot."""
    df = pd.DataFrame({
        "Assignment Score": [s.assignment_score for s in students],
        "Marks": [s.marks for s in students],
    })

    plt.figure(figsize=(8, 5))
    sns.regplot(data=df, x="Assignment Score", y="Marks", scatter_kws={"alpha": 0.6})

    plt.title("Marks vs Assignment Score")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUTPUT_DIR / "marks_vs_assignment.png", bbox_inches="tight")
    plt.close()


def generate_all_visualizations(students: list[Student]) -> None:
    """Generate all charts and save them to the output directory."""
    if not students:
        return

    app_logger.info("Generating student performance visualizations")
    try:
        plot_grade_distribution(students)
        plot_score_distribution(students)
        plot_performance_categories(students)
        plot_marks_vs_attendance(students)
        plot_marks_vs_assignment(students)
        app_logger.info("Visualizations generated successfully")
    except Exception:
        app_logger.exception("Failed to generate visualizations")
        raise
