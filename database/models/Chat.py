from sqlalchemy import Column, Integer, BigInteger, Table, ForeignKey
from sqlalchemy.orm import relationship

from ..db_utils import Base


venue_restriction = Table(
    "chat_photos",
    Base.metadata,
    Column("chat_id", Integer, ForeignKey("chat.id")),
    Column("photo_id", Integer, ForeignKey("photo.id"))
)


class Chat(Base):
    __tablename__ = "chat"

    id = Column(Integer, primary_key=True)

    chat_id = Column(BigInteger, unique=True)

    photos = relationship("Photo", secondary="chat_photos", back_populates="chats")
