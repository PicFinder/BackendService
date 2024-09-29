from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, Depends, UploadFile
from fastapi.responses import RedirectResponse
import uvicorn
from PIL import Image
from sqlalchemy.orm import Session

from database import create_schema, get_db, \
    create_photo, get_chat_photos, get_photo_by_file_id, \
    create_chat, get_chat_by_chat_id, add_photo_to_chat
from neural_network import OpenAIClipNetwork

clip_network: Optional[OpenAIClipNetwork] = None


@asynccontextmanager
async def lifespan(application: FastAPI):
    global clip_network
    clip_network = OpenAIClipNetwork()

    create_schema()
    yield


app = FastAPI(
    title="PicFinder Telegram Bot Backend API",
    version="0.1",
    lifespan=lifespan,
    root_path="/api"
)


@app.post("/create_chat")
def add_chat(chat_id: int, db: Session = Depends(get_db)):
    db_chat = get_chat_by_chat_id(db, chat_id)
    if db_chat:
        return db_chat
    db_chat = create_chat(db, chat_id)
    return db_chat


@app.get("/find_photo", response_model=list[str])
def find_photo(description: str,
               photo_amount: int,
               chat_id: int,
               db: Session = Depends(get_db)):
    photos = get_chat_photos(db, chat_id)
    if not photos:
        return []

    embeddings = [photo.embedding for photo in photos]
    top_ks = clip_network.find_top_k(description, embeddings, photo_amount)

    file_ids = []
    for k in top_ks:
        file_ids.append(photos[k].file_id)

    return file_ids


@app.post("/process_photo")
def process_photo(photo: UploadFile,
                  chat_id: int,
                  file_id: str,
                  db: Session = Depends(get_db)):

    db_photo = get_photo_by_file_id(db, file_id)
    db_chat = get_chat_by_chat_id(db, chat_id)
    if db_photo:
        if db_chat in db_photo.chats:
            return
        else:
            add_photo_to_chat(db, db_chat, db_photo)
            return

    embedding = clip_network.transform_images(Image.open(photo.file))[0]

    db_photo = create_photo(db, file_id, embedding)
    add_photo_to_chat(db, db_chat, db_photo)


@app.get("/", include_in_schema=False)
def docs_redirect():
    return RedirectResponse(url='api/docs')


if __name__ == "__main__":
    uvicorn.run(app=app, host="0.0.0.0", port=8080)
