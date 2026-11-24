#!/usr/bin/python3
"""Initialize the models package and create the unique storage instance."""
from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()
