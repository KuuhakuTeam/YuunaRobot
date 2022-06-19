# Yuuna LastFM Bot
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/YuunaRobot/ >
# PLease read the GNU v3.0 License Agreement in 
# <https://www.github.com/KuuhakuTeam/YuunaRobot/blob/master/LICENSE/>.

from pyrogram import Client
from . import version, Config

import time
import os

from dotenv import load_dotenv

if os.path.isfile("config.env"):
    load_dotenv("config.env")

START_TIME = time.time()

class YuunaRobot(Client):
    def __init__(self):
        kwargs = {
            'name': "yuuna",
            'app_version': version.__yuuna_version__,
            'api_id': Config.API_ID,
            'api_hash': Config.API_HASH,
            'bot_token': Config.BOT_TOKEN,
            'workers': 24,
            'in_memory': True,
            'plugins': dict(root="yuuna.plugins")
        }
        super().__init__(**kwargs)

    async def start(self):
        await super().start()
        self.me = await self.get_me()
        text_ = f"#Yuuna #Logs\n\n__Yuuna is now working.__\n\n**Version** : `{version.__yuuna_version__}`\n**System** :` {self.system_version}`"
        await self.send_message(chat_id=Config.GP_LOGS, text=text_)
        print("Yuuna is playing now '-'...")

    async def stop(self):
        text_ = f"#Yuuna #Logs\n\n__Yuuna will change batteries.__"
        await self.send_message(chat_id=Config.GP_LOGS, text=text_)
        await super().stop()
        print("Yuuna will change batteries ...")

    async def send_log(self, text: str, *args, **kwargs):
        await self.send_message(
            chat_id=Config.GP_LOGS,
            text=text,
            *args,
            **kwargs,
        )

    async def send_err(self, e: str):
        await self.send_message(
            chat_id=Config.GP_LOGS,
            text="#Yuuna #ERROR #LOGS\n\n{}".format(e)
        )


yuuna = YuunaRobot()
