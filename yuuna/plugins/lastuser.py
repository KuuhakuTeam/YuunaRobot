# Yuuna LastFM Bot
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/YuunaRobot/ >
# PLease read the GNU v3.0 License Agreement in
# <https://www.github.com/KuuhakuTeam/YuunaRobot/blob/master/LICENSE/>.

from __future__ import nested_scopes

import asyncio

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from yuuna import yuuna, Config
from yuuna.helpers import get_response, input_str, find_user, add_user, update_user, find_username, get_username

API = "http://ws.audioscrobbler.com/2.0"


@yuuna.on_message(filters.command(["set", "reg"]))
async def last_save_user(_, message: Message):
    uid = message.from_user.id
    if not await find_user(uid):
        await add_user(uid)
        await asyncio.sleep(1)
    user = input_str(message)
    if not user:
        return await message.reply("<i>Use /set username.</i>")
    params = {
        "method": "user.getinfo",
        "user": user,
        "api_key": Config.LASTFM_API_KEY,
        "format": "json",
    }
    try:
        resp = await get_response.json(link=API, params=params)
        await asyncio.gather(
                update_user(uid, user),
                message.reply("<i>Your username has been successfully set.</i>")
            )
    except ValueError:
        return await message.reply("<i>This user does not exist in LastFM database</i>")


@yuuna.on_message(filters.command(["profile", "user"]))
async def now_play(c: yuuna, message: Message):
    user_ = message.from_user
    query = input_str(message)
    lastdb = await find_username(user_.id)
    if not (lastdb or query or message.reply_to_message):
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Create LastFM account", url="https://www.last.fm/join"
                    )
                ]
            ]
        )
        reg_ = "<i>Enter some username, reply user or use /set (username) to set yours. If you don't already have a LastFM account, click the button below to register.</i>"
        await message.reply(reg_, reply_markup=button)
        return
    if message.reply_to_message:
        userr_ = message.reply_to_message.from_user.id
        usrdb = await find_username(userr_)
        if not usrdb:
            return await message.reply("<i>This user has not defined username</i>")
        else:
            user_lastfm = await get_username(userr_)
    elif query:
        user_lastfm = query
    else:
        user_lastfm = await get_username(user_.id)
    param_info = {
        "method": "user.getinfo",
        "user": user_lastfm,
        "api_key": Config.LASTFM_API_KEY,
        "format": "json",
    }
    param_recents = {
        "method": "user.getrecenttracks",
        "user": user_lastfm,
        "api_key": Config.LASTFM_API_KEY,
        "limit": 3,
        "format": "json",
    }
    param_loved = {
        "method": "user.getlovedtracks",
        "user": user_lastfm,
        "api_key": Config.LASTFM_API_KEY,
        "limit": 1,
        "format": "json",
    }
    
    try:
        resp_info = await get_response.json(link=API, params=param_info)
        resp_recent = await get_response.json(link=API, params=param_recents)
        resp_loved = await get_response.json(link=API, params=param_loved)
    except ValueError:
        return await message.reply("<i>Error. Make sure you entered correct username</i>")
    
    # == loved tracks count
    try:
        loved = resp_loved["lovedtracks"]["@attr"]["total"]
    except KeyError:
        loved = 0
    
    # == user latest scrobbles
    scr_ = resp_recent["recenttracks"]["track"]
    kek = ""
    for c in scr_:
        kek += f"    ♪ <b>{c['name']}</b> - <i>{c['artist']['#text']}</i>\n"

    # == user data
    data = resp_info["user"]
    usuario = data["name"]
    user_url = data["url"]
    playcount = data["playcount"]
    country = data["country"]
    text_ = f"<b><a href='{user_url}'>{usuario}</a> profile</b>\n"
    if playcount:
        text_ += f"<b>Scrobbles :</b> {playcount}\n"
    if country:
        text_ += f"<b>Country :</b> {country}\n"
    if loved:
        text_ += f"<b>Loved Tracks :</b> {loved}\n"
    if scr_:
        text_ += f"\n<b>Latest scrobbles :</b>\n{kek}"
    await message.reply(text_, disable_web_page_preview=True)
