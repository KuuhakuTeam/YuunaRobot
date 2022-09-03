# Yuuna LastFM Bot
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/YuunaRobot/ >
# PLease read the GNU v3.0 License Agreement in
# <https://www.github.com/KuuhakuTeam/YuunaRobot/blob/master/LICENSE/>.

from typing import Union
from pyrogram.enums import ChatType
from pyrogram import filters
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from yuuna import yuuna


HELP_TEXT = """
<b>Basic commands:<b>

<b>♬</b> /lt - show what you're listening to
<b>♬</b> /set - set your lastfm username 
<b>♬</b> /ping - check if bot is online 
<b>♬</b> /about - bot information and more 
"""


H_COLLAGE = """
<b>Feature removed.</b>
"""


H_COMPAT = """
<b>Check your music compatibility</b>

<i>With compat you can find out which artists both users listen to</i>

<b>♬</b> /compat (reply to a user) or username - checks its compatibility with mentioned user.
<b>♬</b> /compat username1 username2 - checks compatibility between 2 users that you want.
"""


H_SCROB = """
<b>Scrobbles commands<b>

<b>♬</b> /lt or status - shows what you is listening to
<b>♬</b> /set username - set your lastfm username 
<b>♬</b> /user or /user username - verify your or user information
"""


@yuuna.on_callback_query(filters.regex(pattern=r"^help_back$"))
@yuuna.on_message(filters.command("help") | filters.regex("/start help_"))
async def help_(c: yuuna, m: Union[Message, CallbackQuery]):
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Collage", callback_data="help_collage"),
                InlineKeyboardButton(
                    "Compatibility", callback_data="help_compat")
            ],
            [
                InlineKeyboardButton("Scrobble", callback_data="help_scrobble")
            ]
        ]
    )
    if isinstance(m, Message):
        if m.chat.type == ChatType.PRIVATE:
            await m.reply(HELP_TEXT, reply_markup=button)
        else:
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Commands", url=f"https://t.me/{c.me.username}?start=help_")
                    ]
                ]
            )
            await m.reply("Contact me in private", reply_markup=keyboard)
    if isinstance(m, CallbackQuery):
        await m.edit_message_text(text=HELP_TEXT, reply_markup=button)


@yuuna.on_callback_query(filters.regex(pattern=r"help\_(.*)"))
async def help_colla(_, cb: CallbackQuery):
    data, string = cb.data.split("_")
    if string == "collage":
        msg = H_COLLAGE
    if string == "scrobble":
        msg = H_SCROB
    if string == "compat":
        msg = H_COMPAT
    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Back", callback_data="help_back")]]
    )
    await cb.edit_message_text(text=msg, reply_markup=button)


@yuuna.on_message(filters.command("about"))
async def start_(_, m: Message):
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Lazy dev", url="https://t.me/fnixdev"),
                InlineKeyboardButton("Support", url="https://t.me/fnixsup"),
            ],
            [
                InlineKeyboardButton(
                    "Repository", url="https://github.com/KuuhakuTeam/YuunaRobot")
            ]
        ]
    )
    await m.reply_animation("https://telegra.ph/file/4026209b29ecc9da5f1d4.gif", caption="𝚜𝚘𝚖𝚎 𝚘𝚏 𝚖𝚢 𝚏𝚞𝚗𝚌𝚝𝚒𝚘𝚗𝚜 𝚖𝚊𝚢 𝚌𝚘𝚗𝚝𝚊𝚒𝚗 𝚋𝚞𝚐𝚜, 𝚖𝚢 𝚍𝚎𝚟𝚎𝚕𝚘𝚙𝚎𝚛 𝚒𝚜 𝚕𝚊𝚣𝚢 𝚙𝚕𝚜 𝚋𝚎 𝚙𝚊𝚝𝚒𝚎𝚗𝚝", reply_markup=buttons)
