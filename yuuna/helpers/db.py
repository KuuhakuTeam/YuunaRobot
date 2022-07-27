# Yuuna LastFM Bot
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/YuunaRobot/ >
# PLease read the GNU v3.0 License Agreement in 
# <https://www.github.com/KuuhakuTeam/YuunaRobot/blob/master/LICENSE/>.

__all__ = ["db"]

import asyncio

from motor.core import AgnosticClient, AgnosticCollection, AgnosticDatabase
from motor.motor_asyncio import AsyncIOMotorClient

from yuuna import Config

print("Connecting to Database ...")

DATABASE_URL = Config.DB_URI

_MGCLIENT: AgnosticClient = AsyncIOMotorClient(DATABASE_URL)
_RUN = asyncio.get_event_loop().run_until_complete

if "yuuna" in _RUN(_MGCLIENT.list_database_names()):
    print("Yuuna Database Found :) => Now Logging to it...")
else:
    print("Yuuna Database Not Found :( => Creating New Database...")

_DATABASE: AgnosticDatabase = _MGCLIENT["yuuna"]


def db(name: str) -> AgnosticCollection:
    """Create or Get Collection from your database"""
    return _DATABASE[name]


def _close_db() -> None:
    _MGCLIENT.close()
