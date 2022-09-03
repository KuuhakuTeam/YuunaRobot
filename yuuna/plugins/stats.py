# Yuuna LastFM Bot
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/YuunaRobot/ >
# PLease read the GNU v3.0 License Agreement in 
# <https://www.github.com/KuuhakuTeam/YuunaRobot/blob/master/LICENSE/>.


from pyrogram import filters
from pyrogram.errors import ChatWriteForbidden
from pyrogram.types import Message

from yuuna import yuuna, db
from yuuna.helpers import is_dev, add_gp, del_gp, find_gp


USERS = db["USERS"]
GROUPS = db["GROUPS"]


@yuuna.on_message(filters.command(["stats", "status"]))
async def status_(_, m: Message):
    user_id = m.from_user.id
    if not is_dev(user_id):
        return
    glist = await GROUPS.estimated_document_count()
    ulist = await USERS.estimated_document_count()
    await m.reply(f"<b>♬ Bot Status</b>\n\n♪ <b>Users</b>: <i>{ulist}</i>\n♪ <b>Groups</b>: <i>{glist}</i>")


@yuuna.on_message(filters.new_chat_members & filters.group)
async def thanks_for(c: yuuna, m: Message):
    if c.me.id in [x.id for x in m.new_chat_members]:
        gid = m.chat.id
        if not await find_gp(gid):
            await add_gp(m)
        try:
            await yuuna.send_message(
                chat_id=gid,
                text=("<b>print('</b><i>Hi guys. Thanks for adding me to the group, report bugs and errors at -> @fnixsup</i><b>')</b>"),
                disable_notification=True,
            )
        except ChatWriteForbidden:
            print(f"\n\n[ ERROR ] Bot cannot send messages in {gid}\n")


@yuuna.on_message(filters.left_chat_member)
async def left_chat_(c: yuuna, m: Message):
    if c.me.id == m.left_chat_member.id:
        if await find_gp(m.chat.id):
            await del_gp(m)
        else:
            return