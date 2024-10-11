"""Comment Model"""
from models.base_model import BaseModel, db  # type: ignore
from sqlalchemy.orm import relationship


class Comment(BaseModel, db.Model):
    """Comment Class"""
    __tablename__ = 'comments'
    post_id = db.Column(db.String(60), db.ForeignKey('posts.id'))
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'))
    content = db.Column(db.Text(512), nullable=False)

    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")
