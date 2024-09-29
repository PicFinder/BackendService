Backend service for the PicFinder Telegram Bot. 

/process_photo - performs embedding calculations and stores them
/find_photo - performs a search through the accessible photos according to photo description and returns Telegram file id's
/add_chat - used to initialize a new chat (i.e. when the bot gets added to a new chat). Required to separate photos between chats while avoiding storing identical files

ML by @zazamrykh
FastAPI wrapper by @azazuent
