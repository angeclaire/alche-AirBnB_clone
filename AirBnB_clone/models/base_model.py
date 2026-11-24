
#!/usr/bin/python3
"""This module defines the BaseModel class."""

import uuid
from datetime import datetime


class BaseModel:
    """Define common attributes and methods for project models."""

    def __init__(self):
        """Initialize a new instance with a unique ID and timestamps."""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def __str__(self):
        """Return a readable representation of the instance."""
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(
            class_name, self.id, self.__dict__
        )

    def save(self):
        """Update the instance's modification timestamp."""
        self.updated_at = datetime.now()

    def to_dict(self):
        """Return the instance attributes as a serializable dictionary."""
        result = self.__dict__.copy()
        result["__class__"] = self.__class__.__name__
        result["created_at"] = self.created_at.isoformat()
        result["updated_at"] = self.updated_at.isoformat()
        return result

