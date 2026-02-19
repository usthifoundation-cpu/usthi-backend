from sqlalchemy import Column, Integer, String, LargeBinary, DateTime
from datetime import datetime
from app.database import Base

class Donate(Base):
    __tablename__ = "donation"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)
    utr = Column(String)
    pan = Column(String, nullable=True)
    message = Column(String)
    screenshot = Column(LargeBinary)

    created_at = Column(DateTime, default=datetime.now)
