# Backend service for the PicFinder Telegram Bot
- /process_photo - performs embedding calculation and storing
- /find_photo - performs a search through the accessible photos according to photo description and chat ID. Returns Telegram file_id's
- /add_chat - used to initialize a new chat (i.e. when the bot gets added to a new chat). Required to separate photos between chats while avoiding storing identical files

## Contributors
ML by @zazamrykh

FastAPI wrapper by @azazuent
