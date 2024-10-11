"""Post Model"""
from models.base_model import BaseModel, db  # type: ignore
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Table

# Many-to-many relationship between posts and categories
post_categories = Table(
    'post_categories', db.metadata,
    Column('post_id', db.String(60), ForeignKey('posts.id'), primary_key=True),
    Column(
        'category_id',
        db.String(60),
        ForeignKey('categories.id'),
        primary_key=True),
)

# Many-to-many relationship between posts and tags
post_tags = Table(
    'post_tags', db.metadata,
    Column('post_id', db.String(60), ForeignKey('posts.id'), primary_key=True),
    Column('tag_id', db.String(60), ForeignKey('tags.id'), primary_key=True),
)


class Post(BaseModel, db.Model):
    """Post Class"""
    __tablename__ = "posts"
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'))
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text(512), nullable=False)
    published = db.Column(db.Boolean, default=False)

    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    categories = relationship(
        "Category",
        secondary=post_categories,
        back_populates="posts")
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")
