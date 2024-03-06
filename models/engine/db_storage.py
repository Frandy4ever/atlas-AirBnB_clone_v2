#!/usr/bin/python3
"""DBStorage engine"""
import models
from models.city import City
from models.user import User
from models.place import Place
from models.state import State
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

classes = {
    'Amenity': Amenity,
    'City': City,
    'Place': Place,
    'Review': Review,
    'State': State,
    'User': User
}

class DBStorage:
    """Connects to MySQL Database"""
    __engine = None
    __session = None

    def __init__(self):
        """
        Instantiate a DBStorage object
        """
        engine_args = {
            "user": getenv("HBNB_MYSQL_USER"),
            "password": getenv("HBNB_MYSQL_PWD"),
            "host": getenv("HBNB_MYSQL_HOST"),
            "database": getenv("HBNB_MYSQL_DB"),
            "pool_pre_ping": True
        }
        self.__engine = create_engine(
            "mysql+mysqldb://{user}:{password}@{host}/{database}".format(**engine_args)
        )
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def new(self, obj):
        """Add object to current database session"""
        self.__session.add(obj)

    def save(self):
        """Apply all changes to current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from current database session if obj is not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create Database session"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
            sessionmaker(bind=self.__engine, expire_on_commit=False)
        )


    def close(self):
        """Call remove() to close DBStorage session"""
        self.__session.remove()
