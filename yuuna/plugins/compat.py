# Yuuna LastFM Bot
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/YuunaRobot/ >
# PLease read the GNU v3.0 License Agreement in 
# <https://www.github.com/KuuhakuTeam/YuunaRobot/blob/master/LICENSE/>.

# taken from <https://github.com/UsergeTeam/Userge-Plugins/blob/da006724ebc023d6a7b546b450154e05df89cdbd/plugins/utils/lastfm/__main__.py#L391>

import aiohttp

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from yuuna import yuuna, Config
from yuuna.helpers import input_str, find_username, get_username


API = "http://ws.audioscrobbler.com/2.0"
USER_LAST = "https://last.fm/user/"


@yuuna.on_message(filters.command("compat"))
async def lastfm_compat_(_, message: Message):
    uid = message.from_user.id
    lastdb = await find_username(uid)
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
        reg_ = "<i>It looks like you haven't set your username\nUse /set (username) to set it. If you don't already have a LastFM account, click the button below to register.</i>"
        await message.reply(reg_, reply_markup=button)
        return
    query = input_str(message)
    user_lastfm = await get_username(uid)
    if message.reply_to_message:
        userr_ = message.reply_to_message.from_user.id
        usrdb = await find_username(userr_)
        if usrdb:
            return await message.reply("<i>This user has not defined username</i>")
        else:
            username = await get_username(userr_)
    elif query:
        username = query
    else:
        return await message.reply("<i>I need you to enter username or reply to a message</i>")
    msg = await message.reply("<i>Processing..</i>")
    us1, us2 = user_lastfm, username
    ta = "topartists"
    try:
        ta1 = (await recs(us1, ta, 500))[1][ta]["artist"]
    except KeyError:
        return await msg.edit(f"<i>Could not find {us1} user</i>.")
    try:
        ta2 = (await recs(us2, ta, 500))[1][ta]["artist"]
    except KeyError:
        return await msg.edit(f"<i>Could not find {us2} user.</i>")
    ad1, ad2 = [n["name"] for n in ta1], [n["name"] for n in ta2]
    display = f"<i>[{us1}]({USER_LAST}{us1})</b> and <b>[{us2}]({USER_LAST}{us2})</b>"
    comart = [value for value in ad2 if value in ad1]
    disart = ", ".join({comart[r] for r in range(min(len(comart), 5))})
    compat = min((len(comart) * 100 / 40), 100)
    rep = f"{display} both listen: \n<i>{disart}</i>...\n\nMusic compatibility is <i>{compat}%</b>"
    await msg.edit(rep, disable_web_page_preview=True)


async def resp(params: dict):
    async with aiohttp.ClientSession() as session, \
            session.get(API, params=params) as res:
        return res.status, await res.json()


async def recs(query, typ, lim):
    params = {"method": f"user.get{typ}", "user": query, "limit": lim,
              "api_key": Config.LASTFM_API_KEY, "format": "json"}
    return await resp(params)