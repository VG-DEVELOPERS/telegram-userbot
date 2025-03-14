import asyncio
from pyrogram import Client, filters
from pymongo import MongoClient
from pyrogram.types import Message

# Bot Configuration
API_ID = 28231089  
API_HASH = "bb5c1fc4d8b6c163780820e50ccb8a8a"  
BOT_TOKEN = "8163035112:AAGtTrlpo5C-w9IGzkfBQOLBfEtFW5qk"

# MongoDB Connection
MONGO_URI = "mongodb+srv://riyu:riyu@cluster0.kduyo99.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
mongo_client = MongoClient(MONGO_URI)
db = mongo_client["CharacterDB"]
collection = db["Characters"]

# Initialize Bot
app = Client("name_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("savech") & filters.reply)
async def save_character(client, message: Message):
    """Saves a character name and image to MongoDB."""
    if not message.reply_to_message or not message.reply_to_message.photo:
        await message.reply("Please reply to an image with a character name.")
        return

    # Extract Character Name
    if message.reply_to_message.caption:
        lines = message.reply_to_message.caption.split("\n")
        name_line = next((line for line in lines if line.startswith("☘️ Name:")), None)
        if name_line:
            character_name = name_line.replace("☘️ Name:", "").strip()
        else:
            await message.reply("Character name not found in the message.")
            return
    else:
        await message.reply("Reply to an image message with character details.")
        return

    # Save Data in MongoDB
    file_id = message.reply_to_message.photo.file_id
    bot_username = (await client.get_me()).username  # Get bot username

    collection.insert_one({"file_id": file_id, "name": character_name, "bot": bot_username})

    await message.reply(f"✅ Saved: **{character_name}**")

@app.on_message(filters.command("name") & filters.reply)
async def get_character_name(client, message: Message):
    """Retrieves the character name from MongoDB."""
    if not message.reply_to_message or not message.reply_to_message.photo:
        await message.reply("Please reply to an image.")
        return

    # Find Image in MongoDB
    file_id = message.reply_to_message.photo.file_id
    character = collection.find_one({"file_id": file_id})

    if character:
        await message.reply(f"☘️ Name: **{character['name']}**")
    else:
        await message.reply("⚠️ Character not found.")

@app.on_message(filters.command("total"))
async def total_characters(client, message: Message):
    """Displays total saved characters per bot."""
    bot_counts = collection.aggregate([
        {"$group": {"_id": "$bot", "count": {"$sum": 1}}}
    ])

    response_text = ""
    for bot in bot_counts:
        response_text += f"@{bot['_id']} {bot['count']}\n"

    await message.reply(response_text or "No characters saved yet.")

# Run the bot
if __name__ == "__main__":
    app.run()
    
