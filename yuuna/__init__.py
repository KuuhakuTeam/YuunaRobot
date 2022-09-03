# Yuuna LastFM Bot
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/YuunaRobot/ >
# PLease read the GNU v3.0 License Agreement in 
# <https://www.github.com/KuuhakuTeam/YuunaRobot/blob/master/LICENSE/>.

import motor.motor_asyncio

from .config import Config
from .bot import yuuna, START_TIME

db_core = motor.motor_asyncio.AsyncIOMotorClient(Config.DB_URI)
db = db_core["yuuna"]