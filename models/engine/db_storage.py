#!/usr/bin/python3
"""
DB model
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


classes = {
    "User": User,
    "Post": Post,
    "Comment": Comment,
    "Category": Category,
    "Tag": Tag
}


class DBStorage:
    """
    DB storage class
    """
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        USER = getenv('WordFlow_MYSQL_USER', 'wordflow_dev')
        PWD = getenv('WordFlow_MYSQL_PWD', 'wordflow_dev_pwd')
        HOST = 'localhost'
        DB = getenv('WordFlow_MYSQL_DB', 'WordFlow')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(USER, PWD, HOST, DB))

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        from models.base_model import db  # type: ignore
        """reloads data from the database"""
        db.metadata.create_all(self.__engine)
        sess_factory = db.sessionmaker(
            bind=self.__engine,
            expire_on_commit=False)
        Session = db.scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """ get the object based on the class and its ID, or None"""
        if cls is None or id is None:
            return None
        objects = self.all()
        key = "{}.{}".format(cls.__name__, id)
        if key in objects.keys():
            return objects[key]
        return None

    def count(self, cls=None):
        """the number of objects in storage matching the given class.
        If no class is passed, returns the count of all objects in storage"""
        if cls:
            return len(self.all(cls))
        return len(self.all())
