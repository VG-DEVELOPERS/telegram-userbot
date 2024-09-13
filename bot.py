import os
from pyrogram import Client, filters
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API ID and API Hash from environment variables
api_id = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
session_name = "userbot_session"

# Initialize the Pyrogram Client
app = Client(session_name, api_id=api_id, api_hash=api_hash)

# Command handler for /start
@app.on_message(filters.command("start", prefixes="/") & filters.me)
def start(client, message):
    message.reply_text("Hello! I am your userbot.")

# Echo handler: repeats any text message sent by you
@app.on_message(filters.text & filters.me)
def echo(client, message):
    message.reply_text(message.text)

# Command handler for /ping
@app.on_message(filters.command("ping", prefixes="/") & filters.me)
def ping(client, message):
    message.reply_text("Pong!")

# Run the bot
app.run()
