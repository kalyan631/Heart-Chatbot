import os
import asyncio
import importlib
from threading import Thread
from flask import Flask
from pyrogram import idle
from Star import LOGGER, StarX
from Star.modules import ALL_MODULES

# 1. Minimal Flask app to bind to a port (needed by Render)
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Bot is alive!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

# 2. Start the Pyrogram bot
async def start_bot():
    try:
        await StarX.start()
    except Exception as ex:
        LOGGER.error(ex)
        quit(1)

    for all_module in ALL_MODULES:
        importlib.import_module("Star.modules." + all_module)

    LOGGER.info(f"@{StarX.username} Started.")
    await idle()

# 3. Start both Flask and Bot
if __name__ == '__main__':
    Thread(target=run_flask).start()           # Run Flask server
    asyncio.get_event_loop().run_until_complete(start_bot())  # Run bot
