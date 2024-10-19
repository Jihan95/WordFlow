#!/usr/bin/python3
"""
Database storage model for the WordFlow application. This module defines 
the DBStorage class, which handles interaction with the MySQL database using SQLAlchemy ORM.
"""
from os import getenv
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models.base_model import db, BaseModel  # type: ignore
from models.user import User  # type: ignore
from models.post import Post  # type: ignore
from models.comment import Comment  # type: ignore
from models.category import Category  # type: ignore
from models.tag import Tag  # type: ignore


# Mapping of model names to their corresponding classes
classes = {
    "User": User,
    "Post": Post,
    "Comment": Comment,
    "Category": Category,
    "Tag": Tag
}


class DBStorage:
    """
    DBStorage class provides an abstraction layer for database interactions
    using SQLAlchemy. It supports basic CRUD (Create, Read, Update, Delete)
    operations and handles the session management for database transactions.
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes the DBStorage object by setting up a connection to the 
        MySQL database using environment variables for configuration. 
        If the environment variables are not provided, default values are used.
        """
        USER = getenv('WordFlow_MYSQL_USER', 'wordflow_dev')
        PWD = getenv('WordFlow_MYSQL_PWD', 'wordflow_dev_pwd')
        HOST = 'localhost'
        DB = getenv('WordFlow_MYSQL_DB', 'WordFlow')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(USER, PWD, HOST, DB))

    def all(self, cls=None):
        """
        Queries the current database session for all objects of a given class.
        If no class is provided, it returns all objects across all classes.
        
        Args:
            cls: The class to filter the query by (optional).
            
        Returns:
            dict: A dictionary where keys are in the format <class name>.<id> 
                  and values are the corresponding object instances.
        """
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """
        Adds a new object to the current database session, marking it for 
        insertion into the database during the next commit.
        
        Args:
            obj: The object to be added to the session.
        """
        self.__session.add(obj)

    def save(self):
        """
        Commits all changes in the current database session to the database, 
        ensuring that any pending transactions are persisted.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes the specified object from the current database session.
        The object will be removed during the next commit.
        
        Args:
            obj: The object to be deleted (optional). If None, nothing happens
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        from models.base_model import db  # type: ignore
        """
        Reloads the database by creating all defined tables and establishing 
        a new session. This method is typically called when initializing or 
        resetting the database state.
        """
        db.metadata.create_all(self.__engine)
        sess_factory = db.sessionmaker(
            bind=self.__engine,
            expire_on_commit=False)
        Session = db.scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """
        Closes the current database session by calling the `remove()` method, 
        which safely disposes of the session.
        """
        self.__session.remove()

    def get(self, cls, id):
        """
        Retrieves a specific object based on its class and ID.
        
        Args:
            cls: The class of the object to be retrieved.
            id: The ID of the object to be retrieved.
            
        Returns:
            The object if found, otherwise None.
        """
        if cls is None or id is None:
            return None
        objects = self.all()
        key = "{}.{}".format(cls.__name__, id)
        if key in objects.keys():
            return objects[key]
        return None

    def count(self, cls=None):
        """
        Counts the number of objects in the storage. If a class is provided,
        it returns the count of objects of that specific class. If no class is 
        provided, it returns the count of all objects across all classes.
        
        Args:
            cls: The class to filter by (optional).
            
        Returns:
            int: The count of matching objects in the database.
        """
        if cls:
            return len(self.all(cls))
        return len(self.all())
    
    def get_user_by_email(self, cls, email):
        """
        Retrieves a user based on their email address.
        
        Args:
            cls: The User class.
            email: The email of the user to be retrieved.
        
        Returns:
            The User object if found, otherwise None.
        """
        if cls is None or email is None:
            return None
        if cls == User:
            user = self.__session.query(User).filter_by(email=email).first()
            return user
        return None
