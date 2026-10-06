"""
streamlit_app.py

Streamlit dashboard for the Student Performance Analyzer.

All data access goes through api_client.py (FastAPI backend).
This module is responsible only for UI: collecting input, displaying data,
and showing errors. No business logic lives here.
"""

import io

import streamlit as st
import pandas as pd

import api_client
from api_client import APIClientError
from logger import app_logger


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _backend_status() -> tuple[bool, str]:
    """Return (is_available, status_label) for the FastAPI backend."""
    try:
        api_client.get_health()
        return True, "✅ Connected"
    except APIClientError:
        return False, "❌ Unavailable"


def _has_data() -> bool:
    """Return True if the database has at least one student."""
    try:
        return api_client.get_student_count() > 0
    except APIClientError:
        return False


def _api_error(message: str, exc: APIClientError) -> None:
    """Display a user-friendly API error and log the details."""
    app_logger.error("Dashboard API error — %s: %s", message, exc)
    st.error(f"{message} ({exc})")


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

def show_dashboard() -> None:
    """High-level overview metrics from the API."""
    st.header("Dashboard Overview")

    if not _has_data():
        st.info(
            "No student data available yet. "
            "Go to **Data Management** to add students or import a CSV."
        )
        return

    try:
        count = api_client.get_student_count()
        summary = api_client.get_performance_summary()
        pass_fail = api_client.get_pass_fail_summary()

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total Students", count)
        col2.metric("Average Marks", f"{summary['average_marks']:.2f}")
        col3.metric("Average Attendance", f"{summary['average_attendance']:.2f}%")
        col4.metric("Average Assignment", f"{summary['average_assignment_score']:.2f}")
        col5.metric("Pass Rate", f"{pass_fail['pass_percentage']:.2f}%")
    except APIClientError as e:
        _api_error("Unable to load dashboard metrics.", e)


# ---------------------------------------------------------------------------
# Students
# ---------------------------------------------------------------------------

def show_students() -> None:
    """Display all students in a table from the API."""
    st.header("Students")

    try:
        records = api_client.get_students()
    except APIClientError as e:
        _api_error("Unable to load student data.", e)
        return

    if not records:
        st.info("No student data available yet.")
        return

    df = pd.DataFrame(records)
    st.dataframe(df, use_container_width=True)


# ---------------------------------------------------------------------------
# Analytics
# ---------------------------------------------------------------------------

def show_analytics() -> None:
    """Display all analytics sections via the API."""
    st.header("Analytics")

    if not _has_data():
        st.info("No student data available yet.")
        return

    # Performance Summary
    try:
        st.subheader("Performance Summary")
        summary = api_client.get_performance_summary()
        col1, col2, col3 = st.columns(3)
        col1.metric("Average Marks", f"{summary['average_marks']:.2f}")
        col2.metric("Median Marks", f"{summary['median_marks']:.2f}")
        col3.metric("Highest Marks", f"{summary['highest_marks']:.2f}")
        col1.metric("Average Attendance", f"{summary['average_attendance']:.2f}%")
        col2.metric("Average Assignment", f"{summary['average_assignment_score']:.2f}")
        col3.metric("Lowest Marks", f"{summary['lowest_marks']:.2f}")
    except APIClientError as e:
        _api_error("Unable to load performance summary.", e)

    # Pass / Fail
    try:
        st.subheader("Pass / Fail Analysis")
        pf = api_client.get_pass_fail_summary()
        pf_df = pd.DataFrame([
            {"Category": "Pass", "Count": pf["pass_count"], "Percentage (%)": pf["pass_percentage"]},
            {"Category": "Fail", "Count": pf["fail_count"], "Percentage (%)": pf["fail_percentage"]},
        ])
        st.dataframe(pf_df, use_container_width=True)
    except APIClientError as e:
        _api_error("Unable to load pass/fail analysis.", e)

    # Grade Distribution
    try:
        st.subheader("Grade Distribution")
        grades = api_client.get_grade_distribution()
        total = sum(grades.values())
        grade_rows = [
            {"Grade": k, "Count": v, "Percentage (%)": round((v / total) * 100, 2) if total else 0}
            for k, v in grades.items()
        ]
        st.dataframe(pd.DataFrame(grade_rows), use_container_width=True)
    except APIClientError as e:
        _api_error("Unable to load grade distribution.", e)

    # Attendance
    try:
        st.subheader("Attendance Analysis")
        att = api_client.get_attendance_summary()
        col1, col2, col3 = st.columns(3)
        col1.metric("Average Attendance", f"{att['average_attendance']:.2f}%")
        col2.metric("Highest Attendance", f"{att['highest_attendance']:.2f}%")
        col3.metric("Lowest Attendance", f"{att['lowest_attendance']:.2f}%")
        st.write(
            f"Students below required attendance: **{att['below_required_attendance_count']}** "
            f"({att['below_required_attendance_percentage']:.2f}%)"
        )
    except APIClientError as e:
        _api_error("Unable to load attendance analysis.", e)

    # Performance Categories
    try:
        st.subheader("Performance Categories")
        cats = api_client.get_performance_categories()
        total = sum(cats.values())
        cat_rows = [
            {"Category": k, "Count": v, "Percentage (%)": round((v / total) * 100, 2) if total else 0}
            for k, v in cats.items()
        ]
        st.dataframe(pd.DataFrame(cat_rows), use_container_width=True)
    except APIClientError as e:
        _api_error("Unable to load performance categories.", e)

    # At-Risk
    try:
        st.subheader("At-Risk Students")
        at_risk = api_client.get_at_risk_students()
        if at_risk:
            st.dataframe(pd.DataFrame({"Name": at_risk}), use_container_width=True)
        else:
            st.success("No students are currently identified as at-risk.")
    except APIClientError as e:
        _api_error("Unable to load at-risk students.", e)

    # High Performers
    try:
        st.subheader("High Performers")
        high = api_client.get_high_performers()
        if high:
            st.dataframe(pd.DataFrame({"Name": high}), use_container_width=True)
        else:
            st.info("No high performers identified based on the current criteria.")
    except APIClientError as e:
        _api_error("Unable to load high performers.", e)

    # Correlations
    try:
        st.subheader("Correlation Analysis")
        label_map = {
            "marks_attendance": "Marks vs Attendance",
            "marks_assignment": "Marks vs Assignment Score",
            "attendance_assignment": "Attendance vs Assignment Score",
        }
        corr = api_client.get_correlations()
        corr_rows = [{"Metric": label_map.get(k, k), "Correlation": v} for k, v in corr.items()]
        st.dataframe(pd.DataFrame(corr_rows), use_container_width=True)

        strongest = api_client.get_strongest_correlation()
        st.write(
            f"**Strongest Correlation:** {label_map.get(strongest['pair'], strongest['pair'])} "
            f"({strongest['value']:.2f})"
        )
    except APIClientError as e:
        if "400" in str(e):
            st.warning("Not enough students to calculate correlations (need at least 2).")
        else:
            _api_error("Unable to load correlation analysis.", e)

    # Insights
    try:
        st.subheader("Performance Insights")
        insights = api_client.get_performance_insights()
        for insight in insights:
            st.write(f"- {insight}")
    except APIClientError as e:
        _api_error("Unable to load performance insights.", e)


# ---------------------------------------------------------------------------
# Visualizations
# ---------------------------------------------------------------------------

def show_visualizations() -> None:
    """Build charts from API analytics data (no direct visualizations.py import)."""
    st.header("Visualizations")

    if not _has_data():
        st.info("No student data available yet.")
        return

    try:
        grades = api_client.get_grade_distribution()
        scores = api_client.get_score_distribution()
        cats = api_client.get_performance_categories()
    except APIClientError as e:
        _api_error("Unable to load visualization data.", e)
        return

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Grade Distribution")
        if grades:
            st.bar_chart(pd.DataFrame.from_dict({"Count": grades}))

    with col2:
        st.subheader("Score Distribution")
        if scores:
            st.bar_chart(pd.DataFrame.from_dict({"Count": scores}))

    st.subheader("Performance Categories")
    if cats:
        st.bar_chart(pd.DataFrame.from_dict({"Count": cats}))

    # Scatter plots require individual student data
    try:
        records = api_client.get_students()
        if records:
            df = pd.DataFrame(records)

            col3, col4 = st.columns(2)
            with col3:
                st.subheader("Marks vs Attendance")
                st.scatter_chart(df, x="attendance", y="marks")
            with col4:
                st.subheader("Marks vs Assignment Score")
                st.scatter_chart(df, x="assignment_score", y="marks")
    except APIClientError as e:
        _api_error("Unable to load scatter chart data.", e)


# ---------------------------------------------------------------------------
# Data Management
# ---------------------------------------------------------------------------

def add_student_form() -> None:
    """Form to add one student via POST /students."""
    st.subheader("Add Student")
    with st.form("add_student_form"):
        name = st.text_input("Name")
        marks = st.number_input("Marks", min_value=0.0, max_value=100.0, value=0.0)
        attendance = st.number_input("Attendance (%)", min_value=0.0, max_value=100.0, value=0.0)
        assignment_score = st.number_input("Assignment Score", min_value=0.0, max_value=100.0, value=0.0)
        submitted = st.form_submit_button("Add Student")

    if submitted:
        if not name.strip():
            st.error("Name cannot be empty.")
        else:
            try:
                api_client.create_student(
                    name=name.strip(),
                    marks=marks,
                    attendance=attendance,
                    assignment_score=assignment_score,
                )
                app_logger.info("Student added via dashboard.")
                st.success(f"Student '{name.strip()}' added successfully!")
                st.rerun()
            except APIClientError as e:
                _api_error("Failed to add student.", e)


def csv_import_section() -> None:
    """Upload a CSV and send rows to POST /students/bulk.

    Streamlit reads the CSV into a DataFrame and sends each row as JSON.
    data_loader.py is NOT used — validation is handled by FastAPI.
    """
    st.subheader("Import CSV")
    with st.form("csv_import_form"):
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        import_clicked = st.form_submit_button("Import CSV")

    if import_clicked:
        if uploaded_file is None:
            st.warning("Please choose a CSV file before clicking Import CSV.")
        else:
            try:
                df = pd.read_csv(io.BytesIO(uploaded_file.getvalue()))

                required_cols = {"name", "marks", "attendance", "assignment_score"}
                if not required_cols.issubset(df.columns):
                    missing = required_cols - set(df.columns)
                    st.error(f"CSV is missing required columns: {', '.join(missing)}")
                    return

                # Drop rows with nulls in required columns, build list of dicts
                df = df.dropna(subset=list(required_cols))
                records = df[["name", "marks", "attendance", "assignment_score"]].to_dict(orient="records")

                if not records:
                    st.warning("No valid rows found in the uploaded CSV.")
                    return

                result = api_client.create_students_bulk(records)
                count = result.get("count", len(records))
                app_logger.info("CSV imported via dashboard: %d students.", count)
                st.success(f"Successfully imported {count} students.")
                st.rerun()
            except APIClientError as e:
                _api_error("Unable to import the selected CSV file.", e)
            except Exception:
                app_logger.exception("Unexpected error during CSV import.")
                st.error("Unable to import the selected CSV file.")


def show_data_management() -> None:
    """Data management: add student, import CSV, view count, delete all."""
    st.header("Data Management")

    add_student_form()
    st.divider()

    csv_import_section()
    st.divider()

    st.subheader("Database Record Count")
    try:
        count = api_client.get_student_count()
        st.write(f"Total student records: **{count}**")
    except APIClientError as e:
        _api_error("Unable to retrieve student count.", e)

    st.divider()

    st.subheader("Delete All Students")
    st.warning("Warning: This action cannot be undone.")
    confirm_delete = st.checkbox(
        "I understand that this will permanently delete all student records."
    )
    if st.button("Delete All Students", disabled=not confirm_delete):
        try:
            api_client.delete_all_students()
            app_logger.info("All students deleted via dashboard.")
            st.success("All student records have been deleted.")
            st.rerun()
        except APIClientError as e:
            _api_error("Failed to delete student records.", e)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    st.set_page_config(
        page_title="Student Performance Analyzer",
        page_icon="📊",
        layout="wide",
    )

    st.title("📊 Student Performance Analyzer")
    st.write("Analyze student performance, attendance, assignments, and academic risk.")

    app_logger.info("Dashboard started")

    # Sidebar
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio(
        "Go to",
        ["Dashboard", "Students", "Analytics", "Visualizations", "Data Management"],
    )

    # Backend status indicator
    is_available, status_label = _backend_status()
    st.sidebar.write(f"**Backend:** {status_label}")

    if st.sidebar.button("🔄 Refresh Data"):
        st.rerun()

    if not is_available:
        st.error(
            "FastAPI backend is unavailable. "
            "Please start the API server with `uvicorn api:app --reload` and try again."
        )
        return

    # Routing
    if selection == "Dashboard":
        show_dashboard()
    elif selection == "Students":
        show_students()
    elif selection == "Analytics":
        show_analytics()
    elif selection == "Visualizations":
        show_visualizations()
    elif selection == "Data Management":
        show_data_management()


if __name__ == "__main__":
    main()
