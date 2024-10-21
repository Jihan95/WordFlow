#!/usr/bin/python3
'''
This module contains the BaseModel class, which defines common attributes 
and methods for other models in the application.
'''

import models  # type: ignore
from uuid import uuid4
from __init__ import app
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base
from api.v1 import db  # type: ignore



class BaseModel:
    '''
    BaseModel class defines common attributes and methods shared across all 
    models. It serves as the base class for other models, providing 
    auto-generated unique IDs, timestamps, and utility methods for saving 
    and deleting records.
    '''
    # Common attributes for all models: id, created_at, and updated_at
    id = db.Column(
        db.String(60),
        primary_key=True,
        nullable=False,
        unique=True
        )
    created_at = db.Column(
        db.DateTime(),
        nullable=False,
        default=datetime.utcnow()
        )
    updated_at = db.Column(
        db.DateTime(),
        nullable=False,
        default=datetime.utcnow()
        )

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of the BaseModel.
        If kwargs are provided, they are used to populate the instance attributes.
        Otherwise, a new UUID is assigned as the id, and current timestamps 
        are set for created_at and updated_at.
        
        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments used to set attributes.
        """
        format = "%Y-%m-%dT%H:%M:%S.%f"
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(
                    kwargs["created_at"],
                    format)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(
                    kwargs["updated_at"],
                    format)
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid4())
        else:
            self.id = str(uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        '''
        Returns a human-readable string representation of the object, including
        its class name and id, along with its attributes.
        
        Returns:
            str: A formatted string representing the instance.
        '''
        obj_dict = self.__dict__.copy()
        obj_dict.pop("_sa_instance_state", None)
        return f"[{self.__class__.__name__}] ({self.id}) {obj_dict}"

    def save(self):
        '''
        Updates the `updated_at` attribute to the current datetime and 
        commits the changes to the storage.
        '''
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        '''
        Converts the instance into a dictionary format, including the class name 
        and ISO-formatted timestamps for serialization purposes.
        
        Returns:
            dict: A dictionary containing the instance's attributes and class name.
        '''
        instance_dict = self.__dict__.copy()
        instance_dict["__class__"] = self.__class__.__name__
        if "created_at" in instance_dict:
            instance_dict["created_at"] = self.created_at.isoformat()
        if "updated_at" in instance_dict:
            instance_dict["updated_at"] = self.updated_at.isoformat()

        if "_sa_instance_state" in instance_dict.keys():
            del instance_dict["_sa_instance_state"]
        return instance_dict

    def delete(self):
        """
        Deletes the current instance from storage.
        """
        models.storage.delete(self)
