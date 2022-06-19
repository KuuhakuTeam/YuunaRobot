# Yuuna LastFM Bot
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/YuunaRobot/ >
# PLease read the GNU v3.0 License Agreement in 
# <https://www.github.com/KuuhakuTeam/YuunaRobot/blob/master/LICENSE/>.

import asyncio

from .db import get_collection
from yuuna import yuuna

GROUPS = get_collection("GROUPS")
USERS = get_collection("USERS")
REG = get_collection("REG")


async def find_user(uid):
    if await USERS.find_one({"user_id": uid}):
        return True


async def add_user(m):
    user_start = f"#Yuuna #NEW_USER #LOGS\n\n**User:** {m.from_user.first_name}\n**ID:** {m.from_user.id} <a href='tg://user?id={m.from_user.id}'>**Link**</a>"
    try:
        await asyncio.gather(
            USERS.insert_one(
                {"user_id": m.from_user.id, "user": m.from_user.first_name}
            ),
            yuuna.send_log(
                user_start, disable_notification=False, disable_web_page_preview=True
            ),
        )
    except Exception as e:
        await yuuna.send_err(e)


# Groups
async def find_gp(gid):
    if await GROUPS.find_one({"chat_id": gid}):
        return True


async def add_gp(m):
    user = f"<a href='tg://user?id={m.from_user.id}'>{m.from_user.first_name}</a>"
    text_add = f"#Yuuna #NEW_GROUP #LOGS\n\n**Grupo**: __{m.chat.title}__\n**ID:** __{m.chat.id}__\n**User:** __{user}__"
    if m.chat.username:
        text_add += f"**\nUsername:** @{m.chat.username}"
    try:
        await GROUPS.insert_one({"chat_id": m.chat.id, "title": m.chat.title}),
        await yuuna.send_log(
            text_add, disable_notification=False, disable_web_page_preview=True
        )
    except Exception as e:
        await yuuna.send_err(e)


async def del_gp(m):
    del_txt = f"#Yuuna #LEFT_GROUP #LOGS\n\n<b>Group</b>: {m.chat.title}\n<b>ID:</b> {m.chat.id}"
    try:
        await GROUPS.delete_one({"chat_id": m.chat.id})
        await yuuna.send_log(
            del_txt, disable_notification=False, disable_web_page_preview=True
        )
    except Exception as e:
        await yuuna.send_err(e)