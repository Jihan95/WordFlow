"""User Model"""
from models.base_model import BaseModel, db  # type: ignore
from sqlalchemy.orm import relationship
from flask_login import UserMixin


class User(UserMixin, BaseModel, db.Model):
    """User Class"""
    __tablename__ = "users"
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="user")
