"""Category Model"""
from models.base_model import BaseModel, db  # type: ignore
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Table


class Category(BaseModel, db.Model):
    """Category Class"""
    __tablename__ = 'categories'
    name = db.Column(db.String(128), unique=True, nullable=False)

    posts = relationship(
        "Post",
        secondary='post_categories',
        back_populates="categories")
