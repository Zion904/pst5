class User:
    """A base class for all users in the system."""
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name
    @property
    def id(self):
        return self.user_id

    def to_dict(self):
        """Serialize object to a JSON-friendly dict."""
        return {"id": self.user_id, "name": self.name}

    @staticmethod
    def from_dict(cls, d: dict):
        uid = d.get("id", d.get("user_id"))
        return cls(user_id=uid, name=d.get("name", ""))
