import tempfile
from pathlib import Path

import streamlit as st
import pandas as pd

from logger import app_logger
import database
import analytics
import visualizations
import data_loader
from models import Student


def initialize_app():
    """Initialize the database on dashboard startup."""
    database.initialize_database()


def show_dashboard(students: list[Student]):
    """Show the high-level dashboard metrics."""
    st.header("Dashboard Overview")

    if not students:
        st.info(
            "No student data available yet. "
            "Go to **Data Management** to add students or import a CSV."
        )
        return

    try:
        summary = analytics.calculate_performance_summary(students)
        pass_fail = analytics.calculate_pass_fail_summary(students)

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Total Students", len(students))
        col2.metric("Average Marks", f"{summary['average_marks']:.2f}")
        col3.metric("Average Attendance", f"{summary['average_attendance']:.2f}%")
        col4.metric("Average Assignment", f"{summary['average_assignment_score']:.2f}")
        col5.metric("Pass Rate", f"{pass_fail['pass_percentage']:.2f}%")
    except Exception:
        app_logger.exception("Unable to load performance summary.")
        st.error("Unable to load performance summary.")


def show_students(students: list[Student]):
    """Show all students in a table."""
    st.header("Students")

    if not students:
        st.info("No student data available yet.")
        return

    try:
        records = database.get_all_student_records()
        df = pd.DataFrame(records)
        st.dataframe(df, use_container_width=True)
    except Exception:
        app_logger.exception("Unable to load student data.")
        st.error("Unable to load student data.")


def show_analytics(students: list[Student]):
    """Display comprehensive analytics."""
    st.header("Analytics")

    if not students:
        st.info("No student data available yet.")
        return

    try:
        st.subheader("Performance Summary")
        summary = analytics.calculate_performance_summary(students)
        col1, col2, col3 = st.columns(3)
        col1.metric("Average Marks", f"{summary['average_marks']:.2f}")
        col2.metric("Median Marks", f"{summary['median_marks']:.2f}")
        col3.metric("Highest Marks", f"{summary['highest_marks']:.2f}")
        col1.metric("Average Attendance", f"{summary['average_attendance']:.2f}%")
        col2.metric("Average Assignment", f"{summary['average_assignment_score']:.2f}")
        col3.metric("Lowest Marks", f"{summary['lowest_marks']:.2f}")
    except Exception:
        app_logger.exception("Unable to calculate performance summary.")
        st.error("Unable to calculate this analysis.")
        return

    try:
        st.subheader("Pass / Fail Analysis")
        pf = analytics.calculate_pass_fail_summary(students)
        pf_df = pd.DataFrame([
            {"Category": "Pass", "Count": pf["pass_count"], "Percentage (%)": pf["pass_percentage"]},
            {"Category": "Fail", "Count": pf["fail_count"], "Percentage (%)": pf["fail_percentage"]},
        ])
        st.dataframe(pf_df, use_container_width=True)
    except Exception:
        app_logger.exception("Unable to calculate pass/fail summary.")
        st.error("Unable to calculate pass/fail analysis.")

    try:
        st.subheader("Grade Distribution")
        grades = analytics.calculate_grade_distribution(students)
        grade_rows = [
            {"Grade": k, "Count": v, "Percentage (%)": round((v / len(students)) * 100, 2)}
            for k, v in grades.items()
        ]
        st.dataframe(pd.DataFrame(grade_rows), use_container_width=True)
    except Exception:
        app_logger.exception("Unable to calculate grade distribution.")
        st.error("Unable to calculate grade distribution.")

    try:
        st.subheader("Attendance Analysis")
        att = analytics.calculate_attendance_summary(students)
        col1, col2, col3 = st.columns(3)
        col1.metric("Average Attendance", f"{att['average_attendance']:.2f}%")
        col2.metric("Highest Attendance", f"{att['highest_attendance']:.2f}%")
        col3.metric("Lowest Attendance", f"{att['lowest_attendance']:.2f}%")
        st.write(
            f"Students below required attendance: **{att['below_required_attendance_count']}** "
            f"({att['below_required_attendance_percentage']:.2f}%)"
        )
    except Exception:
        app_logger.exception("Unable to calculate attendance analysis.")
        st.error("Unable to calculate attendance analysis.")

    try:
        st.subheader("Performance Categories")
        cats = analytics.calculate_performance_categories(students)
        cat_rows = [
            {"Category": k, "Count": v, "Percentage (%)": round((v / len(students)) * 100, 2)}
            for k, v in cats.items()
        ]
        st.dataframe(pd.DataFrame(cat_rows), use_container_width=True)
    except Exception:
        app_logger.exception("Unable to calculate performance categories.")
        st.error("Unable to calculate performance categories.")

    try:
        st.subheader("At-Risk Students")
        at_risk_names = analytics.identify_at_risk_students(students)
        if at_risk_names:
            st.dataframe(pd.DataFrame({"Name": at_risk_names}), use_container_width=True)
        else:
            st.success("No students are currently identified as at-risk.")
    except Exception:
        app_logger.exception("Unable to identify at-risk students.")
        st.error("Unable to identify at-risk students.")

    try:
        st.subheader("High Performers")
        high_names = analytics.identify_high_performers(students)
        if high_names:
            st.dataframe(pd.DataFrame({"Name": high_names}), use_container_width=True)
        else:
            st.info("No high performers identified based on the current criteria.")
    except Exception:
        app_logger.exception("Unable to identify high performers.")
        st.error("Unable to identify high performers.")

    try:
        st.subheader("Correlation Analysis")
        corr = analytics.calculate_correlations(students)
        label_map = {
            "marks_attendance": "Marks vs Attendance",
            "marks_assignment": "Marks vs Assignment Score",
            "attendance_assignment": "Attendance vs Assignment Score",
        }
        corr_rows = [{"Metric": label_map.get(k, k), "Correlation": v} for k, v in corr.items()]
        st.dataframe(pd.DataFrame(corr_rows), use_container_width=True)

        strongest_key, strongest_val = analytics.find_strongest_correlation(corr)
        st.write(f"**Strongest Correlation:** {label_map.get(strongest_key, strongest_key)} ({strongest_val:.2f})")
    except ValueError as e:
        st.warning(str(e))
    except Exception:
        app_logger.exception("Unable to calculate correlations.")
        st.error("Unable to calculate correlation analysis.")

    try:
        st.subheader("Performance Insights")
        insights = analytics.generate_performance_insights(students)
        for insight in insights:
            st.write(f"- {insight}")
    except Exception:
        app_logger.exception("Unable to generate performance insights.")
        st.error("Unable to generate performance insights.")


def show_visualizations(students: list[Student]):
    """Display the generated visualization charts."""
    st.header("Visualizations")

    if not students:
        st.info("No student data available yet.")
        return

    try:
        visualizations.generate_all_visualizations(students)

        out_dir = Path("output")
        col1, col2 = st.columns(2)
        with col1:
            st.image(str(out_dir / "grade_distribution.png"), caption="Grade Distribution", use_container_width=True)
            st.image(str(out_dir / "performance_categories.png"), caption="Performance Categories", use_container_width=True)
        with col2:
            st.image(str(out_dir / "score_distribution.png"), caption="Score Distribution", use_container_width=True)
            st.image(str(out_dir / "marks_vs_attendance.png"), caption="Marks vs Attendance", use_container_width=True)

        st.image(str(out_dir / "marks_vs_assignment.png"), caption="Marks vs Assignment Score", use_container_width=True)

    except Exception:
        app_logger.exception("Unable to generate the charts.")
        st.error("Unable to generate the charts.")


def add_student_form():
    """Render the add student form."""
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
                new_student = Student(
                    name=name.strip(),
                    marks=marks,
                    attendance=attendance,
                    assignment_score=assignment_score,
                )
                database.add_student(new_student)
                app_logger.info("Student added via dashboard.")
                st.success(f"Student '{name.strip()}' added successfully!")
                st.rerun()
            except Exception:
                app_logger.exception("Failed to add student from dashboard.")
                st.error("Failed to add student to database.")


def csv_import_section():
    """Render the CSV upload section.

    The file is only imported when the user explicitly clicks 'Import CSV',
    preventing duplicate imports during Streamlit reruns.
    """
    st.subheader("Import CSV")
    with st.form("csv_import_form"):
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        import_clicked = st.form_submit_button("Import CSV")

    if import_clicked:
        if uploaded_file is None:
            st.warning("Please choose a CSV file before clicking Import CSV.")
        else:
            tmp_path = None
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
                    tmp.write(uploaded_file.getvalue())
                    tmp_path = tmp.name

                students_to_add = data_loader.load_students_from_csv(tmp_path)
                database.add_students(students_to_add)
                app_logger.info("CSV imported via dashboard: %d students.", len(students_to_add))
                st.success(f"Successfully imported {len(students_to_add)} valid students.")
                st.rerun()
            except FileNotFoundError as e:
                st.error(str(e))
            except ValueError as e:
                st.warning(str(e))
            except Exception:
                app_logger.exception("Unable to import the selected CSV file.")
                st.error("Unable to import the selected CSV file.")
            finally:
                if tmp_path is not None:
                    Path(tmp_path).unlink(missing_ok=True)


def show_data_management():
    """Show data management forms and controls."""
    st.header("Data Management")

    add_student_form()

    st.divider()

    csv_import_section()

    st.divider()

    st.subheader("Database Record Count")
    try:
        count = database.count_students()
        st.write(f"Total student records: **{count}**")
    except Exception:
        st.error("Unable to retrieve student count.")

    st.divider()

    st.subheader("Delete All Students")
    st.warning("Warning: This action cannot be undone.")
    confirm_delete = st.checkbox(
        "I understand that this will permanently delete all student records."
    )
    if st.button("Delete All Students", disabled=not confirm_delete):
        try:
            database.delete_all_students()
            app_logger.info("All students deleted via dashboard.")
            st.success("All student records have been deleted.")
            st.rerun()
        except Exception:
            app_logger.exception("Failed to delete students via dashboard.")
            st.error("Failed to delete student records.")


def main():
    st.set_page_config(
        page_title="Student Performance Analyzer",
        page_icon="📊",
        layout="wide",
    )

    st.title("📊 Student Performance Analyzer")
    st.write("Analyze student performance, attendance, assignments, and academic risk.")

    app_logger.info("Dashboard started")
    initialize_app()

    try:
        students = database.get_all_students()
    except Exception:
        app_logger.exception("Unable to load student data on dashboard start.")
        st.error("Unable to load student data from the database.")
        students = []

    st.sidebar.title("Navigation")
    selection = st.sidebar.radio(
        "Go to",
        ["Dashboard", "Students", "Analytics", "Visualizations", "Data Management"],
    )

    if st.sidebar.button("🔄 Refresh Data"):
        st.rerun()

    if selection == "Dashboard":
        show_dashboard(students)
    elif selection == "Students":
        show_students(students)
    elif selection == "Analytics":
        show_analytics(students)
    elif selection == "Visualizations":
        show_visualizations(students)
    elif selection == "Data Management":
        show_data_management()


if __name__ == "__main__":
    main()
