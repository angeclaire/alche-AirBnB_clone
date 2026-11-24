#!/usr/bin/python3
"""Defines the FileStorage class, a JSON file based storage engine."""
import json
import os


class FileStorage:
    """Serialize instances to a JSON file and deserialize them back.

    Attributes:
        __file_path (str): Path of the JSON file.
        __objects (dict): Every stored object, keyed by ``<class>.<id>``.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Return the dictionary of every stored object."""
        return FileStorage.__objects

    def new(self, obj):
        """Add ``obj`` to the stored objects under ``<class>.<id>``."""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """Serialize the stored objects to the JSON file."""
        data = {
            key: obj.to_dict()
            for key, obj in FileStorage.__objects.items()
        }
        with open(FileStorage.__file_path, "w", encoding="utf-8") as file:
            json.dump(data, file)

    def reload(self):
        """Deserialize the JSON file into the stored objects.

        Does nothing when the file does not exist.
        """
        if not os.path.isfile(FileStorage.__file_path):
            return
        classes = self.classes()
        with open(FileStorage.__file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        for key, value in data.items():
            FileStorage.__objects[key] = classes[value["__class__"]](**value)

    @staticmethod
    def classes():
        """Return a mapping of class names to the models that can be stored.

        Imported lazily to avoid circular imports with ``models``.
        """
        from models.amenity import Amenity
        from models.base_model import BaseModel
        from models.city import City
        from models.place import Place
        from models.review import Review
        from models.state import State
        from models.user import User

        return {
            "Amenity": Amenity,
            "BaseModel": BaseModel,
            "City": City,
            "Place": Place,
            "Review": Review,
            "State": State,
            "User": User,
        }
