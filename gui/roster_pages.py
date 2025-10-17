# gui/roster_pages.py
import streamlit as st
import pandas as pd

def show_roster_page(manager):
    """Renders the daily roster and check-in functionality."""
    st.header("Daily Roster")

    # --- View Roster Section (remains the same) ---
    day = st.selectbox("Select a day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
    # ... (code to display the dataframe) ...
    
    # --- Student Check-in Section (now works correctly) ---
    st.subheader("Student Check-in")
    with st.form("check_in_form"):
        # To make this user-friendly, we should populate the dropdowns dynamically.
        # Get lists of student names and course names from the manager.
        student_list = {s.name: s.id for s in manager.students}
        selected_student_name = st.selectbox("Select Student", list(student_list.keys()) or ["<no students>"])
        sid = student_list.get(selected_student_name, None)

        def course_has_lesson_on_day(c, d):
            return any(str(les.get("day", "")).strip().lower() == str(d).strip().lower() 
                        for les in getattr(c, "lessons", []))
        def student_enrolled_in_course(c, student_id):
            return student_id in getattr(c, "enrolled_student_ids", [])
        eligible_courses = [
            c for c in manager.courses
            if sid is not None and student_enrolled_in_course(c, sid) and course_has_lesson_on_day(c, day)
        ]
        course_list = {c.name: c.id for c in eligible_courses}
        selected_course_name = st.selectbox(
            "Select Course",
            list(course_list.keys()) or ["<no eligible course for this day>"]
        )
        submitted = st.form_submit_button("Check-in Student")

        if submitted:           
            if sid is None or not course_list or selected_course_name not in course_list:
                st.error("No eligible course on this day or invalid selection.")
            else:
                course_id = course_list[selected_course_name]
                ok, msg = manager.check_in(sid, course_id, day)   
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)
