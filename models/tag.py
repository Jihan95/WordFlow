"""Tag Model"""
from models.base_model import BaseModel, db  # type: ignore
from sqlalchemy.orm import relationship


class Tag(BaseModel, db.Model):
    """Tag Class"""
    __tablename__ = 'tags'
    name = db.Column(db.String(128), unique=True, nullable=False)
    posts = relationship("Post", secondary='post_tags', back_populates="tags")
