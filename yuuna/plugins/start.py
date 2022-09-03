# Yuuna LastFM Bot
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/YuunaRobot/ >
# PLease read the GNU v3.0 License Agreement in 
# <https://www.github.com/KuuhakuTeam/YuunaRobot/blob/master/LICENSE/>.

import time

from typing import Union
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from yuuna import yuuna, version, START_TIME, db
from yuuna.helpers import time_formatter, add_user, find_user

USERS = db["USERS"]

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
        if not await find_user(m.from_user.id):
            await add_user(m.from_user.id)
    if isinstance(m, CallbackQuery):
        await m.edit_message_caption(
            caption=msg,
            reply_markup=keyboard
        )


@yuuna.on_callback_query(filters.regex(pattern=r"^infos$"))
async def infos(_, cq: CallbackQuery):
    info_text = f"""
<b>♬ Bot Info</b>

♪ <b>Version:</b> <code>{version.__yuuna_version__}</code>
♪ <b>Uptime:</b> <code>{time_formatter(time.time() - START_TIME)}</code>
♪ <b>Python:</b> <code>{version.__python_version__}</code>
♪ <b>Pyrogram:</b> <code>{version.__pyro_version__}</code>
"""
    button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Back", callback_data="start_back"),
                ]
            ]
        )
    await cq.edit_message_caption(
        caption=info_text,
        reply_markup=button
    )
