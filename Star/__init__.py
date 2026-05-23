import asyncio

# FIX event loop before importing Abg
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

import logging
import time

from Abg import patch

from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from pyrogram import Client
from pyrogram.enums import ParseMode

import config


logging.basicConfig(
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        logging.FileHandler("log.txt"),
        logging.StreamHandler()
    ],
    level=logging.INFO,
)

logging.getLogger("pyrogram").setLevel(logging.ERROR)

LOGGER = logging.getLogger(__name__)
boot = time.time()

mongo = MongoCli(config.MONGO_URL)
db = mongo.Anonymous

OWNER = config.OWNER_ID


class StarX(Client):
    def __init__(self):
        super().__init__(
            name="StarX",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            lang_code="en",
            in_memory=True,
            parse_mode=ParseMode.DEFAULT,
        )

    async def start(self):
        await super().start()

        me = await self.get_me()

        self.id = me.id
        self.name = f"{me.first_name} {me.last_name or ''}".strip()
        self.username = me.username
        self.mention = me.mention

    async def stop(self):
        await super().stop()


StarX = StarX()
