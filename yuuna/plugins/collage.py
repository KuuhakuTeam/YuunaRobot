# Yuuna LastFM Bot
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/YuunaRobot/ >
# PLease read the GNU v3.0 License Agreement in 
# <https://www.github.com/KuuhakuTeam/YuunaRobot/blob/master/LICENSE/>.

from pyrogram import filters
from pyrogram.errors import WebpageCurlFailed, MediaEmpty
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from yuuna import yuuna
from yuuna.helpers.decorators import input_str
from yuuna.helpers import get_collection, is_dev


API = "http://ws.audioscrobbler.com/2.0"
GROUPS = get_collection("GROUPS")
REG = get_collection("REG")

MODES = [
    "3x3",
    "4x4",
    "5x5",
]


DATE = {
    "7d",
    "1m",
    "3m",
    "6m",
    "12m",
    "overall"
}


@yuuna.on_message(filters.command(["aaa"]))
async def collage_(c: yuuna, message: Message):
    user_id = message.from_user.id
    if not is_dev(user_id):
        return
    query = len(input_str(message).split())
    await message.reply(query)


@yuuna.on_message(filters.command(["collage"]))
async def collage_(c: yuuna, message: Message):
    user_ = message.from_user
    query = int(len(input_str(message).split()))
    args = input_str(message)
    lastdb = await REG.find_one({"id_": user_.id})
    if not lastdb:
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Create LastFM account", url="https://www.last.fm/join"
                    )
                ]
            ]
        )
        
        reg_ = "__It looks like you haven't set your username\nUse /set (username) to set it. If you don't already have a LastFM account, click the button below to register.__"
        await message.reply(reg_, reply_markup=button)
        return
    user_lastfm = lastdb["last_data"]
    if query == 0:
        format_ = "3x3"
        date_ = "7d"
    elif query < 4:
        if " " in args:
            format_, date_ = args.split(" ")
        else:
            format_ = args
            date_ = "7d"
    else:
        return await message.reply("__Invalid format__")
    try:
        if not format_ in MODES:
            return await message.reply("__Invalid format__")
        if not date_ in DATE:
            return await message.reply("__Invalid format__")
        capt = f"__{user_lastfm} - {format_} - {date_}__"
        link = f"https://www.tapmusic.net/collage.php?user={user_lastfm}&type={date_}&size={format_}&caption=true&playcount=true"
        await message.reply_photo(link, caption=capt)
    except WebpageCurlFailed as e:
        print(e)
        return await message.reply("__Failed to process image, try with lower values__")
    except MediaEmpty as e:
        print(e)
        return await message.reply("__Failed to process image, try with lower values__")
