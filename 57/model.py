from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime
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
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    create_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(bd_timezone)
    )

    def __repr__(self):
        return f'<Post {self.id} - {self.title}>'