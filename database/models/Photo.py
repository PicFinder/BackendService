from sqlalchemy import Column, Integer, String, Float, ARRAY, BigInteger
from sqlalchemy.orm import relationship

from ..db_utils import Base


class Photo(Base):
    __tablename__ = "photo"

    id = Column(Integer, primary_key=True)

    file_id = Column(String, unique=True)
    embedding = Column(ARRAY(Float))

    chats = relationship("Chat", secondary="chat_photos", back_populates="photos")
