# Yuuna LastFM Bot
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/YuunaRobot/ >
# PLease read the GNU v3.0 License Agreement in 
# <https://www.github.com/KuuhakuTeam/YuunaRobot/blob/master/LICENSE/>.

import time
import asyncio

from typing import Union
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from yuuna import yuuna, version, START_TIME
from yuuna.helpers import get_collection, time_formatter

USERS = get_collection("USERS")

START_PRIVADO = """
𝙷𝚒 𝚠𝚎𝚕𝚌𝚘𝚖𝚎, 𝙸'𝚖 𝚈𝚞𝚞𝚗𝚊 𝚊 𝙻𝚊𝚜𝚝𝙵𝙼 𝚜𝚌𝚛𝚘𝚋𝚋𝚕𝚎𝚛 𝚊𝚖𝚘𝚗𝚐 𝚘𝚝𝚑𝚎𝚛 𝚏𝚞𝚗𝚌𝚝𝚒𝚘𝚗𝚜
"""


@yuuna.on_callback_query(filters.regex(pattern=r"^start_back$"))
@yuuna.on_message(filters.command("start"))
async def start_(c: yuuna, m: Union[Message, CallbackQuery]):
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="Info", callback_data="infos"),
                InlineKeyboardButton(
                    text="Help", url=f"https://t.me/{c.me.username}?start=help_"),
            ],
            [
                InlineKeyboardButton(
                    text="🎶 Add to a group",
                    url=f"https://t.me/{c.me.username}?startgroup=new",
                ),
            ],
        ]
    )
    msg = START_PRIVADO
    gifstart = "https://telegra.ph/file/32663a402ed3beaea526b.jpg"
    if isinstance(m, Message):
        if not m.chat.type == ChatType.PRIVATE:
            return
        await c.send_photo(m.chat.id, gifstart, caption=msg, reply_markup=keyboard)
        user_id = m.from_user.id
        fname = m.from_user.first_name
        uname = m.from_user.username
        user_start = f"#NEW_USER #LOGS\n\n**User:** {fname}\n**ID:** {m.from_user.id} <a href='tg://user?id={user_id}'>**Link**</a>"
        if uname:
            user_start += f"\n**Username:** @{uname}"
        found = await USERS.find_one({"id_": user_id})
        if not found:
            await asyncio.gather(
                USERS.insert_one({"id_": user_id, "user": fname}),
                c.send_log(
                    user_start,
                    disable_notification=False,
                    disable_web_page_preview=True,
                )
            )
    if isinstance(m, CallbackQuery):
        await c.edit_message_caption(
            chat_id=m.message.chat.id,
            message_id=m.message.message_id,
            caption=msg,
            reply_markup=keyboard
        )


@yuuna.on_callback_query(filters.regex(pattern=r"^infos$"))
async def infos(c: yuuna, m: CallbackQuery):
    info_text = f"""
**♬🎷 Bot Info 🎤●♪**

• **Version:** `{version.__yuuna_version__}`
• **Uptime:** `{time_formatter(time.time() - START_TIME)}`
• **Python:** `{version.__python_version__}`
• **Pyrogram:** `{version.__pyro_version__}`
"""
    button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Back", callback_data="start_back"),
                ]
            ]
        )
    await c.edit_message_caption(
        chat_id=m.message.chat.id,
        message_id=m.message.message_id,
        caption=info_text,
        reply_markup=button
    )
