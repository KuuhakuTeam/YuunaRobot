# Yuuna LastFM Bot
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/YuunaRobot/ >
# PLease read the GNU v3.0 License Agreement in 
# <https://www.github.com/KuuhakuTeam/YuunaRobot/blob/master/LICENSE/>.

from pyrogram import filters
from pyrogram.types import Message

from yuuna import yuuna


@yuuna.on_message(filters.command(["collage"]))
async def collage_(_, message: Message):
    return await message.reply("<b>Feature removed.</b>")
