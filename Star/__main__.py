import os
import asyncio
import importlib
from threading import Thread

from flask import Flask
from pyrogram import idle
from pyrogram.errors import FloodWait


print("MAIN FILE STARTED")


# Flask
app = Flask(__name__)


@app.route("/")
def home():
    return "✅ Bot is alive!"


def run_flask():
    port = int(os.environ.get("PORT", 10000))

    print("FLASK STARTING")

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
        use_reloader=False,
    )


async def start_bot():
    print("BOT FUNCTION ENTERED")

    from Star import LOGGER, StarX
    from Star.modules import ALL_MODULES

    print("IMPORT DONE")

    while True:
        try:
            print("LOGIN START")

            await StarX.start()

            print("BOT LOGIN SUCCESS")

            for module in ALL_MODULES:
                print(f"LOADING {module}")
                importlib.import_module(
                    f"Star.modules.{module}"
                )

            print("MODULES LOADED")
            print("BOT ONLINE")

            await idle()

        except FloodWait as e:
            print(f"FloodWait: sleeping {e.value}s")

            await asyncio.sleep(
                int(e.value)
            )

        except Exception as e:
            print("BOT FAILED")
            print(e)
            raise

        finally:
            try:
                await StarX.stop()
            except:
                pass


def main():
    Thread(
        target=run_flask,
        daemon=True
    ).start()

    asyncio.run(start_bot())


if __name__ == "__main__":
    main()
