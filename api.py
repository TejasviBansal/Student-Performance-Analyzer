from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

import database
import analytics
from models import Student


@asynccontextmanager
async def lifespan(app: FastAPI):
    database.initialize_database()
    yield


app = FastAPI(
    title="Student Performance Analyzer API",
    description="REST API for student performance analysis.",
    version="1.0.0",
    lifespan=lifespan,
)


class StudentCreate(BaseModel):
    name: str = Field(..., min_length=1)
    marks: float = Field(..., ge=0, le=100)
    attendance: float = Field(..., ge=0, le=100)
    assignment_score: float = Field(..., ge=0, le=100)


class StudentResponse(BaseModel):
    id: int
    name: str
    marks: float
    attendance: float
    assignment_score: float


def get_students_or_404() -> list[Student]:
    students = database.get_all_students()
    if not students:
        raise HTTPException(status_code=404, detail="No student data available.")
    return students


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/students", response_model=list[StudentResponse])
def get_students():
    return database.get_all_student_records()


@app.get("/students/count")
def get_student_count():
    return {"count": database.count_students()}


@app.post("/students")
def create_student(student_in: StudentCreate):
    student = Student(
        name=student_in.name,
        marks=student_in.marks,
        attendance=student_in.attendance,
        assignment_score=student_in.assignment_score,
    )
    database.add_student(student)
    return {"message": "Student added successfully"}


@app.post("/students/bulk")
def bulk_create_students(students_in: list[StudentCreate]):
    students = [
        Student(
            name=s.name,
            marks=s.marks,
            attendance=s.attendance,
            assignment_score=s.assignment_score,
        )
        for s in students_in
    ]
    database.add_students(students)
    return {
        "message": "Students added successfully",
        "count": len(students),
    }


@app.delete("/students")
def delete_all_students():
    database.delete_all_students()
    return {"message": "All students deleted successfully"}


@app.get("/analytics/performance")
def get_performance_summary():
    students = get_students_or_404()
    return analytics.calculate_performance_summary(students)


@app.get("/analytics/pass-fail")
def get_pass_fail_summary():
    students = get_students_or_404()
    return analytics.calculate_pass_fail_summary(students)


@app.get("/analytics/grades")
def get_grade_distribution():
    students = get_students_or_404()
    return analytics.calculate_grade_distribution(students)


@app.get("/analytics/attendance")
def get_attendance_summary():
    students = get_students_or_404()
    return analytics.calculate_attendance_summary(students)


@app.get("/analytics/scores")
def get_score_distribution():
    students = get_students_or_404()
    return analytics.calculate_score_distribution(students)


@app.get("/analytics/categories")
def get_performance_categories():
    students = get_students_or_404()
    return analytics.calculate_performance_categories(students)


@app.get("/analytics/at-risk")
def get_at_risk_students():
    students = get_students_or_404()
    return analytics.identify_at_risk_students(students)


@app.get("/analytics/high-performers")
def get_high_performers():
    students = get_students_or_404()
    return analytics.identify_high_performers(students)


@app.get("/analytics/correlations")
def get_correlations():
    students = get_students_or_404()
    try:
        return analytics.calculate_correlations(students)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/analytics/strongest-correlation")
def get_strongest_correlation():
    students = get_students_or_404()
    try:
        corrs = analytics.calculate_correlations(students)
        pair, value = analytics.find_strongest_correlation(corrs)
        return {"pair": pair, "value": value}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/analytics/insights")
def get_performance_insights():
    students = get_students_or_404()
    return {"insights": analytics.generate_performance_insights(students)}
