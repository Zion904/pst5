# gui/student_pages.py
import streamlit as st
import pandas as pd

def show_student_management_page(manager):
    """Renders all components for the student management page."""
    st.header("Student Management")

    # --- Section 1: Find a Student ---
    st.subheader("Find a Student")
    search_term = st.text_input("Search by Name or ID")
    # Call manager.find_students() and display results in a dataframe.
    results = manager.find_students(search_term)
    if results:
        st.dataframe(pd.DataFrame(results), use_container_width=True)
    else:
        st.info("No students found matching that search term.")

    # --- Section 2: Register a New Student ---
    st.subheader("Register a New Student")
    submitted = False
    with st.form(key = "registration_form", clear_on_submit=True):
        reg_name = st.text_input("New Student Name")
        reg_instrument = st.text_input("First Instrument")  
        # Add a multiselect to choose courses to enroll in.
        course_map = {c.name: c.id for c in manager.courses}
        selected_course_names = st.multiselect(
            "Enroll in Course(s)", list(course_map.keys())
        )
        submitted = st.form_submit_button("Register Student")

    if submitted:
        if not reg_name.strip():
            st.error("Please enter a name.")
        else:
            selected_course_ids = [course_map[n] for n in selected_course_names]
            stu, msg = manager.register_new_student(
                reg_name.strip(), reg_instrument.strip(), selected_course_ids
            )
            if stu:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
    
    # --- Section 3: View All Students ---
    st.subheader("All Students")
    rows = [{
        "id": getattr(s, "id", getattr(s, "user_id", None)),
        "name": getattr(s, "name", ""),
        "enrolled_course_ids": list(getattr(s, "enrolled_course_ids", [])),
    } for s in manager.students]

    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
    else:
        st.info("No students yet.")
