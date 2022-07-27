# Yuuna LastFM Bot
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/YuunaRobot/ >
# PLease read the GNU v3.0 License Agreement in 
# <https://www.github.com/KuuhakuTeam/YuunaRobot/blob/master/LICENSE/>.

from __future__ import nested_scopes

import requests
import asyncio

from bs4 import BeautifulSoup as bs

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from yuuna import yuuna, Config
from .misc import *
from yuuna.helpers import db, get_response, input_str, find_user, add_user, find_username, get_username

API = "http://ws.audioscrobbler.com/2.0"


@yuuna.on_message(filters.command(["set", "reg"]))
async def last_save_user(_, message: Message):
    uid = message.from_user.id
    if not await find_user(uid):
        await add_user(uid)
        await asyncio.sleep(1)
    query = input_str(message)
    if not query:
        await message.reply("__Use /set username.__")
        return
    await asyncio.gather(
        add_user(uid, query),
        message.reply("__Your username has been successfully set.__")
    )


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
        reg_ = "__Enter some username, reply user or use /set (username) to set yours. If you don't already have a LastFM account, click the button below to register.__"
        await message.reply(reg_, reply_markup=button)
        return
    if message.reply_to_message:
        userr_ = message.reply_to_message.from_user.id
        usrdb = await find_username(userr_)
        if not usrdb:
            return await message.reply("__This user has not defined username__")
        else:
            user_lastfm = await get_username(userr_)
    elif query:
        user_lastfm = query
    else:
        user_lastfm = await get_username(user_.id)
    params = {
        "method": "user.getinfo",
        "user": user_lastfm,
        "api_key": Config.LASTFM_API_KEY,
        "format": "json",
    }
    try:
        view_data = await get_response.json(link=API, params=params)
    except ValueError:
        return await message.reply("__Error. Make sure you entered the correct username__")
    params_ = {
        "method": "user.getrecenttracks",
        "user": user_lastfm,
        "api_key": Config.LASTFM_API_KEY,
        "limit": 3,
        "format": "json",
    }
    try:
        view_scr = await get_response.json(link=API, params=params_)
    except ValueError:
        return await message.reply("__Error. Make sure you entered the correct username__")

    # == scrap site
    url_ = f"https://www.last.fm/user/{user_lastfm}/loved"
    get_url = requests.get(url_).text
    soup = bs(get_url, "html.parser")
    try:
        scrob = soup.select('h1.content-top-header')[0].text.strip()
        scrr = scrob.split()[2].replace("(", "").replace(")", "")
    except IndexError:
        scrr = None
    
    # == user latest scrobbles
    scr_ = view_scr["recenttracks"]["track"]
    kek = ""
    for c in scr_:
        kek += f"    ♪ **{c['name']}** - __{c['artist']['#text']}__\n"

    # == user data
    data = view_data["user"]
    usuario = data["name"]
    user_url = data["url"]
    playcount = data["playcount"]
    country = data["country"]
    userr = f"<a href='{user_url}'>{usuario}</a>"
    text_ = f"**{userr} profile**\n"
    if playcount:
        text_ += f"**Scrobbles :** {playcount}\n"
    if country:
        text_ += f"**Country :** {country}\n"
    if scrr:
        text_ += f"**Loved Tracks :** {scrr}\n"
    if scr_:
        text_ += f"\n**Latest scrobbles :**\n{kek}"
    await message.reply(text_, disable_web_page_preview=True)
