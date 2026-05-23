import os
import asyncio
import importlib
from threading import Thread
from flask import Flask
from pyrogram import idle

from Star import LOGGER, StarX
from Star.modules import ALL_MODULES


app = Flask(__name__)


@app.route("/")
def home():
    return "✅ Bot is alive!"


def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
        use_reloader=False,
    )


async def start_bot():
    try:
        LOGGER.info("===== BOT STARTING =====")

        await StarX.start()

        LOGGER.info(f"Logged in as @{StarX.username}")

        for module in ALL_MODULES:
            LOGGER.info(f"Loading module: {module}")
            importlib.import_module(f"Star.modules.{module}")

        LOGGER.info("===== BOT ONLINE =====")

        await idle()

    except Exception:
        LOGGER.exception("BOT FAILED")
        raise

    finally:
        try:
            await StarX.stop()
        except:
            pass


def main():
    Thread(target=run_flask, daemon=True).start()
    asyncio.run(start_bot())


if __name__ == "__main__":
    main()
