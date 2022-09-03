# Yuuna LastFM Bot
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/YuunaRobot/ >
# PLease read the GNU v3.0 License Agreement in
# <https://www.github.com/KuuhakuTeam/YuunaRobot/blob/master/LICENSE/>.

import asyncio
import os

from .misc import *
from wget import download
from telegraph import upload_file

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultPhoto

from yuuna import yuuna, Config
from yuuna.helpers import add_gp, add_user, find_gp, find_username, get_username, get_response


API = "http://ws.audioscrobbler.com/2.0"


@yuuna.on_message(filters.command("status", prefixes=""))
@yuuna.on_message(filters.command(["lt", "lastfm"]))
async def now_play(c: yuuna, message: Message):
    if message.chat.type == (ChatType.SUPERGROUP or ChatType.GROUP):
        if not await find_gp(message.chat.id):
            await add_gp(message)
    user = message.from_user
    if not await find_username(user.id):
        await add_user(user.id)
        await asyncio.sleep(1)
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Create LastFM account", url="https://www.last.fm/join"
                    )
                ]
            ]
        )
        await message.reply("<i>Use /set (username) to set your lastfm username. If you don't already have a LastFM account, click the button below to register.</i>", reply_markup=button)
        return
    user_lastfm = await get_username(user.id)

    # request on lastfm
    params = {
        "method": "user.getrecenttracks",
        "limit": 1,
        "extended": 1,
        "user": user_lastfm,
        "api_key": Config.LASTFM_API_KEY,
        "limit": 1,
        "format": "json",
    }
    try:
        view_data = await get_response.json(link=API, params=params)
    except ValueError:
        return await message.reply("<i>Error. Make sure you entered correct username</i>")
    recent_song = view_data["recenttracks"]["track"]
    if len(recent_song) == 0:
        return await message.reply("<i>You don't scrobble any music</i>")
    song_ = recent_song[0]
    song_name = song_["name"]
    artist_name = song_["artist"]["name"]
    image_ = song_["image"][3].get("#text")
    params_ = {
        "method": "track.getInfo",
        "track": song_name,
        "artist": artist_name,
        "user": user_lastfm,
        "api_key": Config.LASTFM_API_KEY,
        "format": "json",
    }
    try:
        view_data_ = await get_response.json(link=API, params=params_)
        get_track = view_data_["track"]
        get_scrob = int(get_track["userplaycount"])
        if get_scrob == 0:
            scrob = get_scrob + 1
        else:
            scrob = get_scrob
        listening = f"is listening for {scrob}th time"
    except KeyError:
        listening = "is listening"
    if image_:
        img_ = download(image_, Config.DOWN_PATH)
    else:
        img_ = download(
            "https://telegra.ph/file/328131bd27e0cb8969b31.png", Config.DOWN_PATH)
    loved = int(song_["loved"])

    # User Photo
    if user.photo:
        photos = message.from_user.photo.big_file_id
        pfp = await yuuna.download_media(photos)
    else:
        pfp = 'yuuna/plugins/misc/pic.jpg'

    image = draw_scrobble(img_, pfp, song_name, artist_name,
                          user_lastfm, listening, loved)
    prof = f"https://www.last.fm/user/{user_lastfm}"
    link_ = f'https://www.youtube.com/results?search_query={str(song_name).replace(" ", "+")}+{str(artist_name).replace(" ", "+")}'
    button_ = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "🔎 Youtube", url=link_
                ),
                InlineKeyboardButton(
                    "👤 Profile", url=prof
                ),
                InlineKeyboardButton(
                    "↗️ Share", switch_inline_query=""
                ),
            ]
        ]
    )
    # send pic
    await message.reply_photo(image, reply_markup=button_)
    try:
        os.remove(img_)
        os.remove(pfp)
        os.system("rm *.jpg")
    except FileNotFoundError:
        pass


@yuuna.on_inline_query()
async def now_play(c: yuuna, cb: InlineQuery):
    results = []
    user = cb.from_user
    if await find_username(user.id):
        user_lastfm = await get_username(user.id)
        params = {
            "method": "user.getrecenttracks",
            "limit": 1,
            "extended": 1,
            "user": user_lastfm,
            "api_key": Config.LASTFM_API_KEY,
            "limit": 1,
            "format": "json",
        }
        try:
            view_data = await get_response.json(link=API, params=params)
        except ValueError:
            results.append(
                InlineQueryResultArticle(
                    title="Error. Make sure you entered correct username",
                    thumb_url="https://telegra.ph/file/21581612f3170612568dd.jpg",
                )
            )
            return await cb.answer(
                results=results,
                cache_time=1
            )
        if "error" in view_data:
            results.append(
                InlineQueryResultArticle(
                    title="Error. Make sure you entered correct username",
                    thumb_url="https://telegra.ph/file/21581612f3170612568dd.jpg",
                )
            )
            return await cb.answer(
                results=results,
                cache_time=1
            )
        recent_song = view_data["recenttracks"]["track"]
        if len(recent_song) == 0:
            results.append(
                InlineQueryResultArticle(
                    title="You don't scrobble any music",
                    thumb_url="https://telegra.ph/file/21581612f3170612568dd.jpg",
                )
            )
            return await cb.answer(
                results=results,
                cache_time=1
            )
        song_ = recent_song[0]
        song_name = song_["name"]
        artist_name = song_["artist"]["name"]
        image_ = song_["image"][3]["#text"]
        params_ = {
            "method": "track.getInfo",
            "track": song_name,
            "artist": artist_name,
            "user": user_lastfm,
            "api_key": Config.LASTFM_API_KEY,
            "format": "json",
        }
        try:
            view_data_ = await get_response.json(link=API, params=params_)
            get_track = view_data_["track"]
            get_scrob = int(get_track["userplaycount"])
            if get_scrob == 0:
                scrob = get_scrob + 1
            else:
                scrob = get_scrob
            listening = f"is listening for {scrob}th time"
        except KeyError:
            listening = "is listening"
        if image_:
            img_ = download(image_)
        else:
            img_ = download(
                "https://telegra.ph/file/328131bd27e0cb8969b31.png")
        loved = int(song_["loved"])

        # User Photo
        if user.photo:
            photos = cb.from_user.photo.big_file_id
            pfp = await yuuna.download_media(photos)
        else:
            pfp = 'yuuna/plugins/misc/pic.jpg'

        image = draw_scrobble(img_, pfp, song_name,
                              artist_name, user_lastfm, listening, loved)
        response = upload_file(image)
        inquery = f"https://telegra.ph{response[0]}"
        await asyncio.sleep(0.5)
        prof = f"https://www.last.fm/user/{user_lastfm}"
        link_ = f'https://www.youtube.com/results?search_query={str(song_name).replace(" ", "+")}+{str(artist_name).replace(" ", "+")}'
        button_ = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔎 Youtube", url=link_
                    ),
                    InlineKeyboardButton(
                        "👤 Profile", url=prof
                    ),
                    InlineKeyboardButton(
                        "↗️ Share", switch_inline_query=""
                    ),
                ]
            ]
        )
        # send pic
        results.append(
            InlineQueryResultPhoto(
                title=listening,
                thumb_url=inquery,
                photo_url=inquery,
                description="Now Playing",
                reply_markup=button_
            )
        )
        await cb.answer(
            results=results,
            cache_time=0,
        )
        try:
            os.remove(img_)
            os.remove(pfp)
            os.system("rm *.jpg")
        except FileNotFoundError:
            pass
    else:
        reg_ = "__You haven't set your username, go to PM and set it.__"
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Go PM", url=f"https://t.me/{c.me.username}"
                    )
                ]
            ]
        )
        results.append(
            InlineQueryResultArticle(
                title="Unregistered user",
                input_message_content=InputTextMessageContent(reg_),
                thumb_url="https://telegra.ph/file/21581612f3170612568dd.jpg",
                reply_markup=button
            )
        )
        await cb.answer(
            results=results,
            cache_time=1
        )
