from typing import Type, Optional

from sqlalchemy.orm import Session

from ..models.Chat import Chat
from ..models.Photo import Photo


def create_chat(db: Session, chat_id: int) -> Chat:
    db_chat = Chat(chat_id=chat_id)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)

    return db_chat


def get_chat_by_chat_id(db: Session, chat_id: int) -> Optional[Type[Chat]]:
    return db.query(Chat).filter(Chat.chat_id == chat_id).first()


def get_chat_photos(db: Session, chat_id: int) -> Optional[list[Type[Photo]]]:
    return db.query(Chat).filter(Chat.chat_id == chat_id).first().photos


def add_photo_to_chat(db: Session, db_chat: Chat, db_photo: Photo):
    db_chat.photos.append(db_photo)

    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)

    return db_chat
