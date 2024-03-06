#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
from os import getenv
from datetime import datetime
import uuid
import models
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base


TIME = "%Y-%m-%dT%H:%M:%S.%f"
Base = declarative_base()


class BaseModel:
    """Base class for all models"""
    id = Column(String(60), nullable=False, primary_key=True, unique=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instantiation of BaseModel object"""
        self.id = kwargs.get('id', str(uuid4()))
        self.created_at = kwargs.get('created_at', datetime.utcnow())
        self.updated_at = kwargs.get('updated_at', self.created_at)
        if kwargs:
            for key, value in kwargs.items():
                if key in ["created_at", "updated_at"]:
                    setattr(self, key, datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f"))
                elif key != '__class__':
                    setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance"""
        class_name = str(type(self)).rsplit(".", maxsplit=1)[-1]
        return '[{}] ({}) {}'.format(class_name, self.id, self.__dict__)

    def save(self):
        """updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Return a dictionary representation of the object"""
        dictionary = self.__dict__.copy()
        dictionary['__class__'] = self.__class__.__name__
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        dictionary.pop('_sa_instance_state', None)
        return dictionary

    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)
