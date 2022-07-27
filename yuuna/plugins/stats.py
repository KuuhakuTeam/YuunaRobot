# Yuuna LastFM Bot
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/YuunaRobot/ >
# PLease read the GNU v3.0 License Agreement in 
# <https://www.github.com/KuuhakuTeam/YuunaRobot/blob/master/LICENSE/>.


from pyrogram import filters
from pyrogram.errors import ChatWriteForbidden
from pyrogram.types import Message

from yuuna import yuuna
from yuuna.helpers import db, is_dev, add_gp, del_gp, find_gp


USERS = db("USERS")
GROUPS = db("GROUPS")


@yuuna.on_message(filters.command(["stats", "status"]))
async def status_(_, m: Message):
    user_id = m.from_user.id
    if not is_dev(user_id):
        return
    glist = await GROUPS.estimated_document_count()
    ulist = await USERS.estimated_document_count()
    await m.reply(f"**【 Bot Status 】**\n\n**Users**: __{ulist}__\n**Groups**: __{glist}__")


@yuuna.on_message(filters.new_chat_members & filters.group)
async def thanks_for(c: yuuna, m: Message):
    if c.me.id in [x.id for x in m.new_chat_members]:
        if not await find_gp(m.chat.id):
            await add_gp(m)
        try:
            await c.send_message(
                chat_id=m.chat.id,
                text=("**print('**__Hi guys. Thanks for adding me to the group, report bugs and errors at -> @fnixsup__**')**"),
                disable_notification=True,
            )
        except ChatWriteForbidden:
            print("\n[ ERROR ] Bot cannot send messages\n")

@yuuna.on_message(filters.left_chat_member)
async def left_chat_(c: yuuna, m: Message):
    if c.me.id == m.left_chat_member.id:
        if await find_gp(m.chat.id):
            await del_gp(m)
        else:
            return