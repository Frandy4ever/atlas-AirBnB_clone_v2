#!/usr/bin/python3
""" db_storage tests """
import os
import unittest
import pycodestyle
from models.engine.db_storage import DBStorage
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session


@unittest.skipIf(os.getenv("HBNB_TYPE_STORAGE") != "db", 'DBStorage inactive')
class TestDBStorageClass(unittest.TestCase):
    """Tests DBStorage class init & formatting related operations"""

    def test_doc_string(self):
        """Tests docstrings for module, class, & class methods"""
        self.assertTrue(len(DBStorage.__doc__) > 0)
        self.assertTrue(len(DBStorage.all.__doc__) > 0)
        self.assertTrue(len(DBStorage.new.__doc__) > 0)
        self.assertTrue(len(DBStorage.save.__doc__) > 0)
        self.assertTrue(len(DBStorage.reload.__doc__) > 0)
        self.assertTrue(len(DBStorage.delete.__doc__) > 0)

    def test_pycodestyle(self):
        """Tests pycodestyle formatting standard compliance"""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(
            result.total_errors,
            0,
            "Found code style errors (and warnings)."
        )

    def test_call_with_argument(self):
        """Verifies that TypeError is raised when an argument is supplied"""
        with self.assertRaises(TypeError):
            DBStorage()

    def test_class_attributes_private(self):
        """Tests attributes of correct types & private status"""
        # Suppressing protected access warning for testing purposes
        # noinspection PyProtectedMember
        self.assertEqual(type(DBStorage._DBStorage__engine), Engine)
        # Suppressing protected access warning for testing purposes
        # noinspection PyProtectedMember
        self.assertEqual(type(DBStorage._DBStorage__session), Session)

        with self.assertRaises(AttributeError):
            print(DBStorage.__engine)
            print(DBStorage.__session)

    def test_type(self):
        """Verifies that type returns correct object type"""
        db = DBStorage()
        self.assertTrue(isinstance(db, DBStorage))


if __name__ == "__main__":
    unittest.main()
