# FIT1056 – PST5: Music School Management System (MSMS)

A small Streamlit app for managing a music school’s students, daily roster (attendance), and basic finance logs.  
This project completes the PST5 “official skeleton” by implementing the finance trio, logging/backup utilities, and simple search/registration UI.

---

## 1) Tech & Requirements

- Python 3.10+  
- Streamlit

Install:

```bash
pip install streamlit

## 2) project structure
app/
  admin_utils.py        # Logger initialization + one-click JSON backup
  schedule.py           # Core: ScheduleManager (students/courses/attendance/finance)
  student.py            # Student model(s)
  teacher.py            # Teacher/Course models
  user.py               # Base user model + id property
data/
  msms.json             # Primary data file (students, teachers, courses, logs)
  backups/              # Auto-created JSON backups before each session
gui/
  main_dashboard.py     # Streamlit entry and page routing
  student_pages.py      # Student search + registration
  roster_pages.py       # Daily roster (check-in)
  finance_pages.py      # Record payments + view payment history
tests/
  test_schedule_manager.py (optional local sanity checks)
main.py                 # App launcher (init logger -> backup -> launch UI)
msms.log                # Runtime logs

## 3)How to run
streamlit run main.py

## 4) Quick Manual test 
1. Search: In Student Management, type alice or 1 → result table shows Alice Johnson.
2. Register: Add a new student → green success banner → appears in students.
3. Roster: Check in a student for a course → green success banner → attendance updated.
4. Payment: Record a payment (amount > 0) → green success banner → finance_log updated.
5. History: On the Payments page, switch the dropdown to view payment history for different students.
6. Export (optional): Run export_report("finance", "finance.csv") and open the CSV.