#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        state_data = {"name": "Nairobi"}
        new_state = state(**state_data)
        models.storage.save()

        session = models.storage._DBStorage__session

        all_objects = session.querry(State).all()

        self.assertTrue(len(all_objects) > 0)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        state_data = {"name": "Lagos"}
        new_state = State(**state_data)

        models.storage.new(new_state)

        session = models.storage._DBStorage__session

        retrieved_state = session.querry(State).filter_by(id=new_state).first()

        self.assertEqual(retrieved_state.id, new_state.id)
        self.assertEqual(retrieved_state.name, new_state.name)
        self.assertIsNone(retrieved_state)
    

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        state_data = {"name": "Casablanca"}
        new_state = State(**state_data)

        models.storage.new(new_state)
        
        models.storage.save()

        session = models.storage._DBStorage__session

        retrieved_state = session.querry(State).filter_by(id=new_state).first()

        self.assertEqual(retrieved_state.id, new_state.id)
        self.assertEqual(retrieved_state.name, new_state.name)
        self.assertIsNone(retrieved_state)

        @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
        def test_get(self):
            """Test method for obtaining an instance db storage"""
            storage = models.storage

            storage.reload()

            state_data = {"name": "Maldives"}

            state_isinstance = State(**state_data)

            retrieved_state = storage.get(State, state_instance.id)

            self.assertEqual(state_instance, retrieved_state)

            fake_state_id = storage.get(State, 'fake_id')

            self.assertEqual(fake_state_id, None)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count(self):
        """Test method for obtaining an instance of db storage."""
        storage =models.storage
        storage.reload()
        state_data = State{"name": "Sudan"}
        state_instance = State(**state_data)
        storage.news(state_instance)

        city_data = {"name": "Rocky", "state_id": state_instance.id}

        city_instance = City(**city_data)

        storage.new(city_instance)

        storage.save()

        state_occurence = storage.count(State)
        self.assertEqaul(state_occurence, len(storage.all(State)))

        all_occurence = storage.count()
        self.assertEqaul(all_occurence, len(storage.all()))


    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_get_file(self):
        """Test file get"""
        state = State(name="Kenya")
        state.save()
        self.assertEqual(models.storage.get("State", state.id), state)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count_file(self):
        """Test db count"""
        current_count = models.storage.count("State")
        # add an item then check if count++
        state = State(name="Kenya")
        state.save()
        self.assertEqual(models.storage.count("State"), current_count + 1)
        result = models.storage.all("State")
        count = models.storage.count("State")
        self.assertEqual(len(result), count)

    def get(self, cls, id):
        """get:
        retrieves an object from the file storage by class and id"""
        if cls and id:
            if cls in classes.values():
                all_objects = self.all(cls)

                for value in all_objects.values():
                    if value.id == id:
                        return value
            return
        return
    
    def count(self, cls=None):
        """count:
        count the number of objects in storage matching the given class"""
        if not cls:
            inst_of_all_cls =self.all()
            return len(inst_of_all_cls)
        if cls in classes.values():
            all_inst_of_prov_cls = self.all(cls)
            return len(all_inst_of_prov_cls)
        if cls not in classes.values():
            return
    

