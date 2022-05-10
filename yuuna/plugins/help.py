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
**Basic commands:**

**♬** /lt - show what you're listening to
**♬** /set - set your lastfm username 
**♬** /ping - check if bot is online 
**♬** /about - bot information and more 
"""


H_COLLAGE = """
**Collage help:**

• **Dimensions:** `3x3, 4x4, 5x5`
• **Period:** `7d, 1m, 3m, 6m, 12m, overall`

**Example:**
**♬** /collage 4x4 6m

__if you don't set any parameters the default value will always be 3x3 7d__
"""


H_COMPAT = """
**Check your music compatibility**

__With compat you can find out which artists both users listen to__

**♬** /compat (reply to a user) or username - checks its compatibility with mentioned user.

**♬** /compat username1 username2 - checks compatibility between 2 users that you want.
"""


H_SCROB = """
**Scrobbles commands**

**♬** /lt or /lt username - shows what you or a user is listening to
**♬** /set username - set your lastfm username 
**♬** /user username - verify a user's information
"""


@yuuna.on_callback_query(filters.regex(pattern=r"^help_back$"))
@yuuna.on_message(filters.command("help") | filters.regex("/start help_"))
async def help_(c: yuuna, m: Union[Message, CallbackQuery]):
    button = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Collage", callback_data="help_collage"),
                InlineKeyboardButton("Compatibility", callback_data="help_compat")
            ],
            [
                InlineKeyboardButton("Scrobble", callback_data="help_scrobble")
            ]
        ]
    )
    if isinstance(m, Message):
        if m.chat.type == ChatType.PRIVATE:
            await m.reply(
                  HELP_TEXT,
                  reply_markup=button
              )
        else:
            msg = "Contact me in private"
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Commands", url=f"https://t.me/{c.me.username}?start=help_")
                    ]
                ]
              )
            await m.reply(
                  msg,
                  reply_markup=keyboard
              )
    elif isinstance(m, CallbackQuery):
        await m.edit_message_text(text=HELP_TEXT, reply_markup=button)


@yuuna.on_callback_query(filters.regex(pattern=r"^help_collage$"))
async def help_colla(_, cb: CallbackQuery):
    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Back", callback_data="help_back")]]
    )
    await cb.edit_message_text(text=H_COLLAGE, reply_markup=button)

@yuuna.on_callback_query(filters.regex(pattern=r"^help_compat$"))
async def help_scro(_, cb: CallbackQuery):
    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Back", callback_data="help_back")]]
    )
    await cb.edit_message_text(text=H_COMPAT, reply_markup=button)

@yuuna.on_callback_query(filters.regex(pattern=r"^help_scrobble$"))
async def help_andro(_, cb: CallbackQuery):
    button = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Back", callback_data="help_back")]]
    )
    await cb.edit_message_text(text=H_SCROB, reply_markup=button)

@yuuna.on_message(filters.command("about"))
async def start_(_, m: Message):
    buttons = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("Lazy dev", url="https://t.me/fnixdev"),
            InlineKeyboardButton("Support", url="https://t.me/fnixsup"),
        ],
        [
            InlineKeyboardButton("Repository", url="https://github.com/KuuhakuTeam/YuunaRobot")
        ]
    ]
    )
    await m.reply_animation("https://telegra.ph/file/4026209b29ecc9da5f1d4.gif", caption="𝚜𝚘𝚖𝚎 𝚘𝚏 𝚖𝚢 𝚏𝚞𝚗𝚌𝚝𝚒𝚘𝚗𝚜 𝚖𝚊𝚢 𝚌𝚘𝚗𝚝𝚊𝚒𝚗 𝚋𝚞𝚐𝚜, 𝚖𝚢 𝚍𝚎𝚟𝚎𝚕𝚘𝚙𝚎𝚛 𝚒𝚜 𝚕𝚊𝚣𝚢 𝚙𝚕𝚜 𝚋𝚎 𝚙𝚊𝚝𝚒𝚎𝚗𝚝", reply_markup=buttons)

