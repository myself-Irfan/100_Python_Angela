from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from app import db


class Book(db.Model):
    """
    val: Mapped[type] -> store type : annotations
    mapped_column -> type and other property
    """
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)

    def __repr__(self):
        return f'<Book {self.title}>'