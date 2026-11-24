#!/usr/bin/python3
"""Defines the BaseModel class shared by every AirBnB clone model."""
import uuid
from datetime import datetime

import models


class BaseModel:
    """Base class that defines the common attributes and methods.

    Attributes:
        id (str): Unique identifier generated with uuid4.
        created_at (datetime): Moment the instance was created.
        updated_at (datetime): Moment the instance was last modified.
    """

    TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

    def __init__(self, *args, **kwargs):
        """Initialize a new instance.

        Args:
            *args: Unused.
            **kwargs (dict): Attributes to restore, typically the output
                of ``to_dict``. When empty, a brand new instance is built
                and registered with the storage engine.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == "__class__":
                    continue
                if key in ("created_at", "updated_at"):
                    value = datetime.strptime(value, self.TIME_FORMAT)
                setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def __str__(self):
        """Return the string representation of the instance."""
        return "[{}] ({}) {}".format(
            type(self).__name__, self.id, self.__dict__
        )

    def save(self):
        """Refresh ``updated_at`` and persist the instance."""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Return a dictionary containing all keys/values of the instance.

        The dictionary holds a ``__class__`` key with the class name, and
        the datetime attributes converted to ISO formatted strings.
        """
        data = self.__dict__.copy()
        data["__class__"] = type(self).__name__
        data["created_at"] = self.created_at.isoformat()
        data["updated_at"] = self.updated_at.isoformat()
        return data
