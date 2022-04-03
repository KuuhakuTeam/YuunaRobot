# Yuuna LastFM Bot
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/YuunaRobot/ >
# PLease read the GNU v3.0 License Agreement in 
# <https://www.github.com/KuuhakuTeam/YuunaRobot/blob/master/LICENSE/>.

import asyncio
from pyrogram import filters
from pyrogram.types import Message

from yuuna import yuuna
from yuuna.helpers import get_collection, input_str

REG = get_collection("REG")

@yuuna.on_message(filters.command(["set", "reg"]))
async def last_save_user(c: yuuna, message: Message):
    user_id = message.from_user.id
    fname = message.from_user.first_name
    uname = message.from_user.username
    text = input_str(message)
    if not text:
        await message.reply("__Bruh.. use /set username.__")
        return
    found = await REG.find_one({"id_": user_id})
    user_start = f"#USER_REGISTER #LOGS\n\n**User:** {fname}\n**ID:** {user_id} <a href='tg://user?id={user_id}'>**Link**</a>"
    if uname:
        user_start += f"\n**Username:** @{uname}"
    if found:
        await asyncio.gather(
                REG.update_one({"id_": user_id}, {
                                "$set": {"last_data": text}}, upsert=True),
                message.reply("__Your username has been successfully updated.__")
            )
    else:
        await asyncio.gather(
                REG.update_one({"id_": user_id}, {
                                "$set": {"last_data": text}}, upsert=True),
                c.send_log(
                    user_start,
                    disable_notification=False,
                    disable_web_page_preview=True,
                ),
                message.reply("__Your username has been successfully set.__")
            )


@yuuna.on_message(filters.command(["duser", "deluser"]))
async def last_del_user(c: yuuna, message: Message):
    user_id = message.from_user.id
    found = await REG.find_one({"id_": user_id})
    if found:
        await asyncio.gather(
                REG.delete_one(found),
                message.reply("__Your username has been deleted.__")
            )
    else:
        return await message.reply("__You don't have a registered username__")
