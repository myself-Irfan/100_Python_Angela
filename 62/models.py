from sqlalchemy import Column, Integer, String, DateTime, func, Time
from database import Base

class Cafe(Base):
    __tablename__ = "cafes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    open_time = Column(Time, nullable=False)
    close_time = Column(Time, nullable=False)
    coffee_rating = Column(String, nullable=False)
    wifi_rating = Column(String, nullable=False)
    power_rating = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)