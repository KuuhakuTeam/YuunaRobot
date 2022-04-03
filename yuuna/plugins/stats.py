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
from yuuna.helpers import get_collection, is_dev

USERS = get_collection("USERS")
GROUPS = get_collection("GROUPS")
REG = get_collection("REG")

@yuuna.on_message(filters.command(["stats", "status"]))
async def status_(_, m: Message):
    user_id = m.from_user.id
    if not is_dev(user_id):
        return
    glist = await GROUPS.estimated_document_count()
    ulist = await USERS.estimated_document_count()
    rlist = await REG.estimated_document_count()
    await m.reply(f"**♬🎷【 Bot Status 】●♪**\n\n**Users**: __{ulist}__\n**Reg Users**: __{rlist}__\n**Groups**: __{glist}__")


@yuuna.on_message(filters.new_chat_members)
async def thanks_for(c: yuuna, m: Message):
    user = (
        f"<a href='tg://user?id={m.from_user.id}'>{m.from_user.first_name}</a>")
    gp_title = m.chat.title
    gp_id = m.chat.id

    text_add = f"#NEW_GROUP #LOGS\n\n**Grupo**: __{gp_title}__\n**ID:** __{gp_id}__\n**User:** __{user}__"
    if m.chat.username:
        text_add += f"**\nUsername:** @{m.chat.username}"
    if c.me.id in [x.id for x in m.new_chat_members]:
        await c.send_message(
            chat_id=m.chat.id,
            text=("""
**print("**__Hi guys. Thanks for adding me to the group, report bugs and errors at -> @fnixsup__**")**
"""
                  ),
            disable_notification=True,
        )
        found = await GROUPS.find_one({"ID_": gp_id})
        if not found:
            await asyncio.gather(
                GROUPS.insert_one({"id_": gp_id, "title": gp_title}),
                c.send_log(
                    text_add,
                    disable_notification=False,
                    disable_web_page_preview=True,
                )
            )
