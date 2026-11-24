#!/usr/bin/python3
"""Unit tests for the BaseModel class and its subclasses."""
import os
import unittest
from datetime import datetime

import models
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class TestBaseModel(unittest.TestCase):
    """Test cases for BaseModel."""

    model = BaseModel

    def setUp(self):
        """Start every test from an empty storage."""
        models.storage.all().clear()

    def tearDown(self):
        """Remove the file written by the test."""
        if os.path.exists("file.json"):
            os.remove("file.json")
        models.storage.all().clear()

    def test_attribute_types(self):
        """A new instance has an id and two datetimes."""
        obj = self.model()
        self.assertIsInstance(obj.id, str)
        self.assertIsInstance(obj.created_at, datetime)
        self.assertIsInstance(obj.updated_at, datetime)

    def test_unique_ids(self):
        """Two instances never share an id."""
        self.assertNotEqual(self.model().id, self.model().id)

    def test_new_instance_is_registered(self):
        """A new instance is added to the storage."""
        obj = self.model()
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.assertIs(models.storage.all()[key], obj)

    def test_str(self):
        """__str__ shows class name, id and attributes."""
        obj = self.model()
        text = str(obj)
        self.assertTrue(text.startswith(
            "[{}] ({})".format(type(obj).__name__, obj.id)))
        self.assertIn("'id': '{}'".format(obj.id), text)

    def test_save_updates_timestamp_and_file(self):
        """save refreshes updated_at and writes the JSON file."""
        obj = self.model()
        before = obj.updated_at
        obj.save()
        self.assertGreater(obj.updated_at, before)
        self.assertTrue(os.path.isfile("file.json"))

    def test_to_dict(self):
        """to_dict returns serializable data with the class name."""
        obj = self.model()
        data = obj.to_dict()
        self.assertEqual(data["__class__"], type(obj).__name__)
        self.assertEqual(data["id"], obj.id)
        self.assertEqual(data["created_at"], obj.created_at.isoformat())
        self.assertEqual(data["updated_at"], obj.updated_at.isoformat())

    def test_to_dict_does_not_alter_instance(self):
        """to_dict works on a copy of the instance attributes."""
        obj = self.model()
        obj.to_dict()
        self.assertNotIn("__class__", obj.__dict__)
        self.assertIsInstance(obj.created_at, datetime)

    def test_recreate_from_dict(self):
        """An instance can be rebuilt from its dictionary."""
        obj = self.model()
        obj.name = "Holberton"
        clone = self.model(**obj.to_dict())
        self.assertIsNot(clone, obj)
        self.assertEqual(clone.to_dict(), obj.to_dict())
        self.assertIsInstance(clone.created_at, datetime)

    def test_recreate_does_not_register(self):
        """Rebuilding from a dictionary does not touch the storage."""
        obj = self.model()
        count = len(models.storage.all())
        self.model(**obj.to_dict())
        self.assertEqual(len(models.storage.all()), count)


class TestUser(TestBaseModel):
    """Test cases for User."""

    model = User

    def test_default_attributes(self):
        """User has empty string defaults."""
        obj = User()
        for name in ("email", "password", "first_name", "last_name"):
            self.assertEqual(getattr(obj, name), "")


class TestState(TestBaseModel):
    """Test cases for State."""

    model = State

    def test_default_attributes(self):
        """State has an empty name by default."""
        self.assertEqual(State().name, "")


class TestCity(TestBaseModel):
    """Test cases for City."""

    model = City

    def test_default_attributes(self):
        """City has empty string defaults."""
        obj = City()
        self.assertEqual(obj.state_id, "")
        self.assertEqual(obj.name, "")


class TestAmenity(TestBaseModel):
    """Test cases for Amenity."""

    model = Amenity

    def test_default_attributes(self):
        """Amenity has an empty name by default."""
        self.assertEqual(Amenity().name, "")


class TestPlace(TestBaseModel):
    """Test cases for Place."""

    model = Place

    def test_default_attributes(self):
        """Place has the documented defaults."""
        obj = Place()
        for name in ("city_id", "user_id", "name", "description"):
            self.assertEqual(getattr(obj, name), "")
        for name in ("number_rooms", "number_bathrooms", "max_guest",
                     "price_by_night"):
            self.assertEqual(getattr(obj, name), 0)
        self.assertEqual(obj.latitude, 0.0)
        self.assertEqual(obj.longitude, 0.0)
        self.assertEqual(obj.amenity_ids, [])


class TestReview(TestBaseModel):
    """Test cases for Review."""

    model = Review

    def test_default_attributes(self):
        """Review has empty string defaults."""
        obj = Review()
        for name in ("place_id", "user_id", "text"):
            self.assertEqual(getattr(obj, name), "")


if __name__ == "__main__":
    unittest.main()
