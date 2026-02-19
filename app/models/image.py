from sqlalchemy import Column, Integer, String, LargeBinary
from app.database import Base

class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    content_type = Column(String, nullable=False)
    description = Column(String, nullable=False)
    heading = Column(String, nullable=False)
    image_data = Column(LargeBinary, nullable=False)
