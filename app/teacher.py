from app.user import User

class TeacherUser(User):
    """Represents a teacher."""
    # Implement the TeacherUser class, inheriting from User.
    # It should have an additional 'speciality' attribute in its __init__.
    def __init__(self, user_id, name, speciality):
        super().__init__(user_id, name)
        self.speciality = speciality

    def to_dict(self):
        base = super().to_dict()
        base["speciality"] = self.speciality
        return base
    
    @staticmethod
    def from_dict(data_dict):
        return TeacherUser(
            user_id=data_dict.get("user_id", data_dict.get("id")),
            name=data_dict.get("name", ""),
            speciality=data_dict.get("speciality", ""),
        )

class Course:
    """Represents a single course offered by the school, linked to a teacher."""
    def __init__(self, course_id, name, instrument, teacher_id, enrolled_student_ids = None, lessons = None):
        self.id = course_id
        self.name = name
        self.instrument = instrument
        self.teacher_id = teacher_id
        # Initialize two empty lists: 'enrolled_student_ids' and 'lessons'.
        self.enrolled_student_ids = list(enrolled_student_ids or [])
        self.lessons = list(lessons or []) # This will hold lesson dictionaries

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "instrument": self.instrument,
            "teacher_id": self.teacher_id,
            "enrolled_student_ids": list(self.enrolled_student_ids),
            "lessons": list(self.lessons),
        }

    @staticmethod
    def from_dict(data_dict):
        return Course(
            course_id=data_dict.get("id"),
            name=data_dict.get("name", ""),
            instrument=data_dict.get("instrument", ""),
            teacher_id=data_dict.get("teacher_id"),
            enrolled_student_ids=data_dict.get("enrolled_student_ids", []),
            lessons=data_dict.get("lessons", []),
        )