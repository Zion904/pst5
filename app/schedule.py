import json
import logging
import csv
from app.student import StudentUser
from datetime import datetime
# Corrected Import: TeacherUser and Course now come from the same file.
from app.teacher import TeacherUser, Course

class ScheduleManager:
    """The main controller for all business logic and data handling."""
    def __init__(self, data_path="data/msms.json"):
        self.data_path = data_path
        self.students = []
        self.teachers = []
        self.courses = []
        # Initialize the new attendance_log attribute as an empty list.
        self.attendance_log = []
        self.finance_log = []
        # ... (next_id counters) ...
        self._load_data()


    def _load_data(self):
        """Loads data from the JSON file and populates the object lists."""
        try:
            with open(self.data_path, 'r') as f:
                data = json.load(f)
                # Load students, teachers, and courses as before.
            self.students = []
            for stu_dict in data.get("students", []):
                self.students.append(StudentUser.from_dict(stu_dict))

            # teachers
            self.teachers = []
            for teacher_dict in data.get("teachers", []):
                self.teachers.append(TeacherUser.from_dict(teacher_dict))

            # courses
            self.courses = []
            for course_dict in data.get("courses", []):
                self.courses.append(Course.from_dict(course_dict))

                # Correctly load the attendance log.
                # Use .get() with a default empty list to prevent errors if the key doesn't exist.
            self.attendance_log = data.get("attendance", [])
            self.finance_log = data.get("finance", [])
        except FileNotFoundError:
            print("Data file not found. Starting with a clean state.")
            self.students, self.teachers, self.courses, self.attendance_log = [], [], [], []
    
    
    def _save_data(self):
        """Converts object lists back to dictionaries and saves to JSON."""
        # Create a 'data_to_save' dictionary.
        data_to_save = {
            "students": [s.to_dict() for s in self.students],
            "teachers": [t.to_dict() for t in self.teachers],
            "courses": [c.to_dict() for c in self.courses],
            # Add the attendance_log to the dictionary to be saved.
            # Since it's already a list of dicts, no conversion is needed.
            "attendance": self.attendance_log,
            "finance_log": self.finance_log,
            # ... (next_id counters) ...
        }
        # Write 'data_to_save' to the JSON file.
        with open(self.data_path, 'w') as f:
            json.dump(data_to_save, f, indent=4,ensure_ascii = False) 

    def find_students(self, term):
        """search students by id or name, return a list of dicts"""
        q = str(term or "").strip()
        if not q:
            return []
        
        try:
            target_id = int(q)
        except Exception:
            target_id = None

        results = []
        for s in self.students:
            if (target_id is not None and s.id == target_id) or (q.lower() in s.name.lower()):
                results.append({
                    "id": s.id,
                    "name": s.name,
                    "enrolled_course_ids": getattr(s, "enrolled_course_ids", []),
                })
        return results
        
    

    def record_payment(self, student_id, amount, method):
        """Adds a payment record to the finance log."""
        # Find the student to ensure they exist.
        student = self.find_student_by_id(student_id)
        if not student:
            print("Error:Payment failed. Student not found.")
            return None
        # Create a payment dictionary with student_id, amount, method, and a timestamp.
        payment_record = {
            "student_id": student_id,
            "amount": amount,
            "method": method,
            "timestamp": datetime.now().isoformat()
        }
        # Append the record to self.finance_log and save the data.
        self.finance_log.append(payment_record)
        self._save_data()
        print(f"Payment of {amount} for student {student_id} recorded.")
        logging.info(f"Payment of {amount} recorded for student ID {student_id}.")
        return payment_record


    def get_payment_history(self, student_id):
        """Returns a list of all payments for a given student."""
        # Use a list comprehension to filter self.finance_log
        # and return only the records that match the student_id.
        return [p for p in self.finance_log if p['student_id'] == student_id]

    def export_report(self, kind, out_path):
        """Exports a log to a CSV file."""
        print(f"Exporting {kind} report to {out_path}...")
        # Use an if/elif block to select the correct data list based on 'kind'.
        if kind == "finance":
            data_to_export = self.finance_log
            headers = ["student_id", "amount", "method", "timestamp"]
        elif kind == "attendance":
            data_to_export = self.attendance_log # Assuming this exists from PST2
            headers = ["student_id", "course_id", "timestamp"]
        else:
            print("Error: Unknown report type.")
            return

        # Use Python's 'csv' module to write the data.
        # Open the file, create a csv.DictWriter, write the header, then write all the rows.
        with open(out_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            for row in data_to_export:
                writer.writerow({h: row.get(h, "") for h in headers})
            
        print(f"Done. Report saved to {out_path}.")
        return out_path
    
    def cancel_lesson(self, lesson_id, reason):
        """Cancels a lesson by id (marks it as cancelled in the course's lessons list, then save & log)."""
        try:
            lid = int(lesson_id)
        except (ValueError, TypeError):
            print("Error: invalid lesson id.")
            return False

        for course in self.courses:
            for lesson in course.lessons:
                curr_id = int(lesson.get("lesson_id", lesson.get("id", -1)))  # 兼容 lesson_id / id
                if curr_id == lid:
                    lesson["cancelled"] = True
                    lesson["cancellation_reason"] = reason
                    lesson["cancellation_timestamp"] = datetime.now().isoformat()  # 或者 datetime.now().isoformat()

                    self._save_data()
                    print(f"Lesson ID {lesson_id} cancelled. Reason: {reason}")
                    logging.warning(f"Lesson ID {lesson_id} was cancelled. Reason: {reason}")
                    return True

        print("Error: lesson id not found.")
        return False

    def get_lessons_by_day(self, day):
        """return [(course_obj, lesson_dict), ...], used for print lessons"""
        results = []
        for course in self.courses:
            for lesson in course.lessons:
                if str(lesson.get("day", "")).lower() == str(day).lower():
                    results.append((course, lesson))
        return results
    
    def check_in(self, student_id, course_id, day):
        """Records a student's attendance for a course after validation."""
        # This implementation remains the same, but it will now function correctly.
        student = self.find_student_by_id(student_id)
        course = self.find_course_by_id(course_id)
        
        if not student or not course:
            return False, "Invalid student or course ID."
        try:
            sid = int(getattr(student, "user_id", getattr(student, "id", student_id)))
        except Exception:
            sid = int(student_id)
        try:
            cid = int(getattr(course, "id", course_id))
        except Exception:
            cid = int(course_id)
        
        if cid not in getattr(student, "enrolled_course_ids", []):
            return False, "Student is not enrolled in this course."
        if hasattr(course, "enrolled_student_ids") and \
            sid not in getattr(course, "enrolled_student_ids", []):
            return False, "Student is not enrolled in this course."

        d = str(day).strip().lower()
        has_lesson_today = any(
            str(les.get("day", "")).strip().lower() == d
            for les in getattr(course, "lessons", [])
        )
        if not has_lesson_today:
            return False, f"No lesson for {course.name} on {day}."
        
        self.attendance_log.append({
            "student_id": sid,
            "course_id": cid,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        })
        self._save_data()
        return True, f"Checked in {student.name} for {course.name}!"
    # Also implement find_student_by_id and find_course_by_id helper methods.
    def find_student_by_id(self, student_id):
        """
        Find and return a student object by its ID.
        Args:
        student_id (int): The student's ID.
        """
        for s in self.students:
            if s.user_id == int(student_id):
                return s
        return None
        
    def find_course_by_id(self, course_id):
        """
        Find and return a course object by its ID.
        Args:
        student_id (int): The student's ID. 
        """
        try:
            cid = int(course_id)
        except Exception:
            return None
        for c in self.courses:
            c_id = getattr(c, "id", None)
            if c_id is None and isinstance(c, dict):
                c_id = c.get("id")
            if c_id == cid:
                return c
        return None
        
    def switch_course(self, student_id, from_course_id, to_course_id):
        """
        Switch a student's enrollment from one course to another.
        Args:
        student_id (int): The student's ID.
        from_course_id (int): The current course ID.
        to_course_id (int): The target course ID.
        """
        student = self.find_student_by_id(student_id)
        from_c = self.find_course_by_id(from_course_id)
        to_c = self.find_course_by_id(to_course_id)

        if not student or not from_c or not to_c:
            print("Error: invalid id(s).")
            return False
        
        if from_c.id == to_c.id:
            print("Error: from/to are the same course.")
            return False
        
        if from_c.id not in student.enrolled_course_ids:
            print("Error: student is not currently in the 'from' course.")
            return False
        
        if to_c.id in student.enrolled_course_ids:
            print("Error: student already in the 'to' course.")
            return False
        
        student.enrolled_course_ids.remove(from_c.id)
        student.enrolled_course_ids.append(to_c.id)

        if student.user_id in from_c.enrolled_student_ids:
            from_c.enrolled_student_ids.remove(student.user_id)
        if student.user_id not in to_c.enrolled_student_ids:
            to_c.enrolled_student_ids.append(student.user_id)

        self._save_data()
        print(f"Success: switched {student.name} from {from_c.name} to {to_c.name}.")
        return True

    def create_course(self, name, instrument, teacher_id):
        """create a new course, return the new course object"""
        name = (name or "").strip()
        instrument = (instrument or "").strip()
        try:
            tid = int(teacher_id) if teacher_id is not None else None
        except Exception:
            tid = None

        if not name:
            return None
        new_id = max([c.id for c in self.courses], default=100) + 1
        c = Course(
            course_id = new_id,
            name=name,
            instrument=instrument,
            teacher_id=tid,
            enrolled_student_ids=[],
            lessons=[],
        )

        self.courses.append(c)
        self._save_data()  
        return c
    
    def register_new_student(self, name, instrument = None, course_ids = None):
        """register a new student, return the new student object"""
        name = (name or "").strip()
        if not name:
            return None, "please enter a name."
        new_id = max([s.user_id for s in self.students], default=0) + 1
        stu = StudentUser(user_id=new_id, name=name, enrolled_course_ids=[])
        self.students.append(stu)
        added_names = []
        course_ids = list(course_ids or [])
        for cid in (course_ids or []):
            c = self.find_course_by_id(cid)
            if not c:
                continue
            if new_id not in getattr(c, "enrolled_student_ids", []):
                c.enrolled_student_ids.append(new_id)
            if c.id not in getattr(stu, "enrolled_course_ids", []):
                stu.enrolled_course_ids.append(c.id)
                added_names.append(c.name)
        self._save_data()
        msg = f"Registered {name} (ID {new_id})"
        if added_names:
            msg += f" and enrolled in {', '.join(added_names)}."
        else:
            msg += "."
        return stu, msg
        
        
        