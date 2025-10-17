from app.user import User

class StudentUser(User):
    """Represents a student, inheriting from the base User class."""
    def __init__(self, user_id, name, enrolled_course_ids = None):
        # Call the parent class's __init__ method using super().
        super().__init__(user_id, name)
        # Initialize an empty list called 'enrolled_course_ids' to store the IDs of courses.
        self.enrolled_course_ids = list(enrolled_course_ids or [])
    
    def to_dict(self):
        base = super().to_dict()
        base["enrolled_course_ids"] = list(self.enrolled_course_ids)
        return base

    @staticmethod
    def from_dict(data_dict):
        return StudentUser(
            user_id=data_dict.get("user_id", data_dict.get("id")),
            name=data_dict.get("name", ""),
            enrolled_course_ids=data_dict.get("enrolled_course_ids", []),
        )