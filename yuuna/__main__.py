# Yuuna LastFM Bot
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/YuunaRobot/ >
# PLease read the GNU v3.0 License Agreement in 
# <https://www.github.com/KuuhakuTeam/YuunaRobot/blob/master/LICENSE/>.

from .bot import yuuna
from pyrogram import idle
import asyncio
from yuuna.helpers.db import _close_db

async def main():
    await yuuna.start()
    await idle()
    await yuuna.stop()
    _close_db()

if __name__ == "__main__" :
    asyncio.get_event_loop().run_until_complete(main())