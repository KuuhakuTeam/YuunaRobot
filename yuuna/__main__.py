# Yuuna LastFM Bot
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/YuunaRobot/ >
# PLease read the GNU v3.0 License Agreement in 
# <https://www.github.com/KuuhakuTeam/YuunaRobot/blob/master/LICENSE/>.

import asyncio
import logging

from pyrogram import idle

from logging.handlers import RotatingFileHandler
from pymongo.errors import ConnectionFailure

from . import db_core
from yuuna.bot import yuuna

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s - %(levelname)s] - %(name)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S',
                    handlers=[
                        RotatingFileHandler(
                            "yuuna.log", maxBytes=20480, backupCount=10),
                        logging.StreamHandler()
                    ])

logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("pyrogram.parser.html").setLevel(logging.ERROR)
logging.getLogger("pyrogram.session.session").setLevel(logging.ERROR)


async def db_connect():
    """Check Mongo Client"""
    try:
        logging.info("Connecting to MongoDB.")
        await db_core.server_info()
        logging.info("DB Connected.")
    except (BaseException, ConnectionFailure) as e:
        logging.error("Failed to connect to database, exiting....")
        logging.debug(str(e))
        quit(1)


async def run_yuuna():
    await db_connect()
    await yuuna.start()
    await idle()
    await yuuna.stop()


if __name__ == "__main__" :
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run_yuuna())
    except KeyboardInterrupt:
        pass
    except Exception as err:
        logging.error(err.with_traceback(None))
    finally:
        loop.stop()