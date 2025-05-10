from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz

from blog_app import db

bd_timezone = pytz.timezone('Asia/Dhaka')


class Post(db.Model):
    __tablename__ = "blog_posts"

    """
    val: Mapped[type] -> store type : annotations
    mapped_column -> type and other property
    """
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(200), nullable=True)
    body: Mapped[str] = mapped_column(String(500), nullable=False)
    author_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('blog_users.id', ondelete="SET NULL"),
        nullable=True
    )
    create_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(bd_timezone)
    )

    author = relationship('User', back_populates='posts')

    def __repr__(self):
        return f'<Post {self.id} - {self.title}>'


class User(db.Model):
    __tablename__ = 'blog_users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(20), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    create_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(bd_timezone)
    )

    posts = relationship('Post', back_populates='author')

    def __repr__(self):
        return f'<User {self.id} - {self.name}>'
