#!/usr/bin/python3
"""Unit tests for the FileStorage class."""
import json
import os
import unittest

import models
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User


class TestFileStorage(unittest.TestCase):
    """Test cases for FileStorage."""

    def setUp(self):
        """Start every test from an empty storage and no file."""
        models.storage.all().clear()
        if os.path.exists("file.json"):
            os.remove("file.json")

    def tearDown(self):
        """Clean up the storage and the file."""
        models.storage.all().clear()
        if os.path.exists("file.json"):
            os.remove("file.json")

    def test_storage_is_file_storage(self):
        """The module level storage is a FileStorage."""
        self.assertIsInstance(models.storage, FileStorage)

    def test_all_returns_dict(self):
        """all returns the dictionary of objects."""
        self.assertIsInstance(models.storage.all(), dict)

    def test_new_uses_class_dot_id_key(self):
        """new stores the object under <class>.<id>."""
        obj = User()
        self.assertIn("User.{}".format(obj.id), models.storage.all())

    def test_save_writes_json(self):
        """save writes every object as a dictionary."""
        obj = BaseModel()
        models.storage.save()
        with open("file.json", encoding="utf-8") as file:
            data = json.load(file)
        self.assertEqual(data["BaseModel.{}".format(obj.id)], obj.to_dict())

    def test_reload_restores_objects(self):
        """reload rebuilds instances of the right classes."""
        user = User()
        user.first_name = "Betty"
        user.save()
        models.storage.all().clear()
        models.storage.reload()
        restored = models.storage.all()["User.{}".format(user.id)]
        self.assertIsInstance(restored, User)
        self.assertEqual(restored.first_name, "Betty")
        self.assertEqual(restored.to_dict(), user.to_dict())

    def test_reload_without_file(self):
        """reload does nothing when the file is missing."""
        models.storage.reload()
        self.assertEqual(models.storage.all(), {})


if __name__ == "__main__":
    unittest.main()
