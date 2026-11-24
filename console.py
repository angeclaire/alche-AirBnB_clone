#!/usr/bin/python3
"""Defines the HBNBCommand class, the command interpreter."""
import cmd
import json
import re
import shlex

import models


class HBNBCommand(cmd.Cmd):
    """Command interpreter for the AirBnB clone.

    Besides the usual ``<command> <class> [args]`` form, every command
    can be written as ``<class>.<command>(<args>)``.
    """

    prompt = "(hbnb) "

    # Attribute types that ``update`` casts the supplied value to.
    CASTS = {
        "number_rooms": int,
        "number_bathrooms": int,
        "max_guest": int,
        "price_by_night": int,
        "latitude": float,
        "longitude": float,
    }

    # ---------------------------------------------------------------- helpers

    @staticmethod
    def _classes():
        """Return the mapping of class names to storable classes."""
        return models.storage.classes()

    def _get_class(self, name):
        """Return the class called ``name``, or print an error.

        Args:
            name (str or None): Class name typed by the user.

        Returns:
            The class, or None when it is missing or unknown.
        """
        if not name:
            print("** class name missing **")
            return None
        cls = self._classes().get(name)
        if cls is None:
            print("** class doesn't exist **")
        return cls

    def _get_instance_key(self, args):
        """Validate ``<class> <id>`` arguments and return the storage key.

        Prints the matching error message and returns None when the class
        or id is missing, or when no such instance exists.
        """
        if self._get_class(args[0] if args else None) is None:
            return None
        if len(args) < 2:
            print("** instance id missing **")
            return None
        key = "{}.{}".format(args[0], args[1])
        if key not in models.storage.all():
            print("** no instance found **")
            return None
        return key

    @staticmethod
    def _parse(line):
        """Split ``line`` into arguments, honouring double quotes."""
        try:
            return shlex.split(line)
        except ValueError:
            return line.split()

    @classmethod
    def _cast(cls, attribute, value):
        """Convert ``value`` to the type expected by ``attribute``."""
        caster = cls.CASTS.get(attribute)
        if caster is None:
            return value
        try:
            return caster(value)
        except (TypeError, ValueError):
            return value

    # --------------------------------------------------------------- commands

    def do_quit(self, line):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, line):
        """Exit the program on end of file (Ctrl+D)."""
        print()
        return True

    def emptyline(self):
        """Do nothing when an empty line is entered."""

    def do_create(self, line):
        """Create a new instance, save it and print its id.

        Usage: create <class>
        """
        cls = self._get_class(self._parse(line)[0] if line.strip() else None)
        if cls is None:
            return
        instance = cls()
        instance.save()
        print(instance.id)

    def do_show(self, line):
        """Print the string representation of an instance.

        Usage: show <class> <id>
        """
        key = self._get_instance_key(self._parse(line))
        if key is not None:
            print(models.storage.all()[key])

    def do_destroy(self, line):
        """Delete an instance and save the change.

        Usage: destroy <class> <id>
        """
        key = self._get_instance_key(self._parse(line))
        if key is not None:
            del models.storage.all()[key]
            models.storage.save()

    def do_all(self, line):
        """Print every instance, optionally filtered by class.

        Usage: all [<class>]
        """
        args = self._parse(line)
        name = args[0] if args else None
        if name is not None and self._get_class(name) is None:
            return
        print([
            str(obj) for obj in models.storage.all().values()
            if name is None or type(obj).__name__ == name
        ])

    def do_count(self, line):
        """Print the number of instances of a class.

        Usage: count <class>
        """
        args = self._parse(line)
        if self._get_class(args[0] if args else None) is None:
            return
        print(sum(
            1 for obj in models.storage.all().values()
            if type(obj).__name__ == args[0]
        ))

    def do_update(self, line):
        """Update an instance by adding or changing one attribute.

        Usage: update <class> <id> <attribute> "<value>"
               update <class> <id> <dictionary>
        """
        key = self._get_instance_key(self._parse(line))
        if key is None:
            return
        # The dictionary form cannot go through shlex: keep the raw text.
        match = re.search(r"(\{.*\})\s*$", line)
        if match:
            self._update_from_dict(key, match.group(1))
            return
        args = self._parse(line)
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        self._set_attribute(key, args[2], args[3])

    def _update_from_dict(self, key, text):
        """Apply the attributes of the dictionary ``text`` to ``key``."""
        try:
            data = json.loads(text)
        except ValueError:
            try:
                data = json.loads(text.replace("'", '"'))
            except ValueError:
                print("** value missing **")
                return
        for attribute, value in data.items():
            self._set_attribute(key, attribute, value, save=False)
        models.storage.all()[key].save()

    def _set_attribute(self, key, attribute, value, save=True):
        """Set ``attribute`` on the instance stored under ``key``."""
        if attribute in ("id", "created_at", "updated_at"):
            return
        instance = models.storage.all()[key]
        if isinstance(value, str):
            value = self._cast(attribute, value)
        setattr(instance, attribute, value)
        if save:
            instance.save()

    # ------------------------------------------------------- dot syntax hooks

    def default(self, line):
        """Handle ``<class>.<command>(<args>)`` style input."""
        match = re.fullmatch(r"(\w+)\.(\w+)\((.*)\)", line.strip())
        if match is None:
            print("*** Unknown syntax: {}".format(line))
            return
        name, command, raw = match.groups()
        handlers = {
            "all": self.do_all,
            "count": self.do_count,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "update": self.do_update,
            "create": self.do_create,
        }
        handler = handlers.get(command)
        if handler is None:
            print("*** Unknown syntax: {}".format(line))
            return
        handler(self._build_line(name, command, raw))

    @staticmethod
    def _build_line(name, command, raw):
        """Rebuild a classic command line from dot syntax arguments."""
        raw = raw.strip()
        if command == "update" and "{" in raw:
            head, _, tail = raw.partition("{")
            ident = head.strip().rstrip(",").strip().strip("\"'")
            return "{} {} {{{}".format(name, ident, tail)
        lexer = shlex.shlex(raw, posix=True)
        lexer.whitespace = ","
        lexer.whitespace_split = True
        try:
            tokens = [token.strip() for token in lexer]
        except ValueError:
            tokens = [token.strip() for token in raw.split(",")]
        return " ".join([name] + [shlex.quote(token) for token in tokens])


if __name__ == "__main__":
    HBNBCommand().cmdloop()
