#!/usr/bin/python3
"""Unit tests for the HBNBCommand console."""
import io
import os
import unittest
from unittest.mock import patch

import models
from console import HBNBCommand

CLASSES = ("BaseModel", "User", "State", "City", "Amenity", "Place", "Review")


class TestConsole(unittest.TestCase):
    """Test cases for the command interpreter."""

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

    @staticmethod
    def run_command(line):
        """Run ``line`` in a fresh console and return what it printed."""
        with patch("sys.stdout", new=io.StringIO()) as output:
            HBNBCommand().onecmd(line)
        return output.getvalue().strip()

    def create(self, name="User"):
        """Create an instance through the console and return its id."""
        return self.run_command("create {}".format(name))

    def test_quit_and_eof(self):
        """quit and EOF stop the loop."""
        self.assertTrue(HBNBCommand().onecmd("quit"))
        with patch("sys.stdout", new=io.StringIO()):
            self.assertTrue(HBNBCommand().onecmd("EOF"))

    def test_empty_line(self):
        """An empty line prints nothing."""
        self.assertEqual(self.run_command(""), "")

    def test_unknown_command(self):
        """An unknown command is reported."""
        self.assertIn("Unknown syntax", self.run_command("foo"))
        self.assertIn("Unknown syntax", self.run_command("User.foo()"))

    def test_create_errors(self):
        """create validates the class name."""
        self.assertEqual(
            self.run_command("create"), "** class name missing **")
        self.assertEqual(
            self.run_command("create Nope"), "** class doesn't exist **")

    def test_create_every_class(self):
        """create works and persists for every class."""
        for name in CLASSES:
            ident = self.create(name)
            self.assertIn("{}.{}".format(name, ident), models.storage.all())
        self.assertTrue(os.path.isfile("file.json"))

    def test_show(self):
        """show prints the instance or the right error."""
        ident = self.create()
        self.assertIn(ident, self.run_command("show User {}".format(ident)))
        self.assertEqual(self.run_command("show"), "** class name missing **")
        self.assertEqual(
            self.run_command("show Nope 1"), "** class doesn't exist **")
        self.assertEqual(
            self.run_command("show User"), "** instance id missing **")
        self.assertEqual(
            self.run_command("show User 1"), "** no instance found **")

    def test_destroy(self):
        """destroy removes the instance or prints the right error."""
        ident = self.create()
        self.assertEqual(self.run_command("destroy User {}".format(ident)), "")
        self.assertNotIn("User.{}".format(ident), models.storage.all())
        self.assertEqual(
            self.run_command("destroy User {}".format(ident)),
            "** no instance found **")
        self.assertEqual(
            self.run_command("destroy"), "** class name missing **")

    def test_all(self):
        """all lists everything or only one class."""
        self.create("User")
        self.create("State")
        listing = self.run_command("all")
        self.assertIn("[User]", listing)
        self.assertIn("[State]", listing)
        self.assertIn("[User]", self.run_command("all User"))
        self.assertNotIn("[State]", self.run_command("all User"))
        self.assertEqual(
            self.run_command("all Nope"), "** class doesn't exist **")

    def test_count(self):
        """count returns the number of instances of a class."""
        self.create("User")
        self.create("User")
        self.create("State")
        self.assertEqual(self.run_command("count User"), "2")
        self.assertEqual(self.run_command("User.count()"), "2")
        self.assertEqual(self.run_command("count Review"), "0")
        self.assertEqual(
            self.run_command("count"), "** class name missing **")

    def test_update_errors(self):
        """update validates every argument."""
        ident = self.create()
        self.assertEqual(
            self.run_command("update"), "** class name missing **")
        self.assertEqual(
            self.run_command("update User"), "** instance id missing **")
        self.assertEqual(
            self.run_command("update User 1 a b"), "** no instance found **")
        self.assertEqual(
            self.run_command("update User {}".format(ident)),
            "** attribute name missing **")
        self.assertEqual(
            self.run_command("update User {} name".format(ident)),
            "** value missing **")

    def test_update_attribute(self):
        """update sets a quoted attribute value."""
        ident = self.create()
        self.run_command(
            'update User {} first_name "Betty Jane"'.format(ident))
        user = models.storage.all()["User.{}".format(ident)]
        self.assertEqual(user.first_name, "Betty Jane")

    def test_update_casts_numbers(self):
        """update casts known numeric attributes of Place."""
        ident = self.create("Place")
        self.run_command('update Place {} max_guest "4"'.format(ident))
        self.run_command('update Place {} latitude "37.77"'.format(ident))
        place = models.storage.all()["Place.{}".format(ident)]
        self.assertEqual(place.max_guest, 4)
        self.assertEqual(place.latitude, 37.77)

    def test_update_protected_attributes(self):
        """update never changes id or timestamps."""
        ident = self.create()
        self.run_command('update User {} id "hacked"'.format(ident))
        self.assertIn("User.{}".format(ident), models.storage.all())

    def test_dot_syntax(self):
        """The <class>.<command>(<args>) form behaves like the classic one."""
        ident = self.create()
        self.assertEqual(self.run_command("User.all()").count("[User]"), 1)
        self.assertIn(ident, self.run_command('User.show("{}")'.format(ident)))
        self.run_command(
            'User.update("{}", "first_name", "John")'.format(ident))
        user = models.storage.all()["User.{}".format(ident)]
        self.assertEqual(user.first_name, "John")
        self.run_command('User.destroy("{}")'.format(ident))
        self.assertEqual(self.run_command("User.count()"), "0")

    def test_dot_syntax_update_dictionary(self):
        """update accepts a dictionary of attributes."""
        ident = self.create()
        self.run_command(
            'User.update("{}", {{"first_name": "John", "age": 89}})'
            .format(ident))
        user = models.storage.all()["User.{}".format(ident)]
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.age, 89)


if __name__ == "__main__":
    unittest.main()
