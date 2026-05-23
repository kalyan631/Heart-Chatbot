import os
import asyncio
import importlib
from threading import Thread
from flask import Flask
from pyrogram import idle

from Star import LOGGER, StarX
from Star.modules import ALL_MODULES


# Flask app (Render keep alive)
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Bot is alive!"


def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
        use_reloader=False
    )


async def start_bot():
    try:
        await StarX.start()

        for module in ALL_MODULES:
            importlib.import_module(f"Star.modules.{module}")

        LOGGER.info(f"@{StarX.username} Started.")

        await idle()

    except Exception as e:
        LOGGER.error(f"Startup Error: {e}")
        raise

    finally:
        try:
            await StarX.stop()
        except:
            pass


def main():
    flask_thread = Thread(
        target=run_flask,
        daemon=True
    )
    flask_thread.start()

    asyncio.run(start_bot())


if __name__ == "__main__":
    main()
