# Yuuna LastFM Bot
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/YuunaRobot/ >
# PLease read the GNU v3.0 License Agreement in 
# <https://www.github.com/KuuhakuTeam/YuunaRobot/blob/master/LICENSE/>.

import asyncio
import os

from .misc import *
from io import BytesIO
from wget import download
from telegraph import upload_file
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, InlineQuery, InlineQueryResultArticle, InputTextMessageContent

from yuuna import yuuna, Config
from yuuna.helpers import input_str, add_gp, find_gp
from yuuna.helpers import get_collection, get_response


API = "http://ws.audioscrobbler.com/2.0"
GROUPS = get_collection("GROUPS")
REG = get_collection("REG")


@yuuna.on_message(filters.command("status", prefixes=""))
@yuuna.on_message(filters.command(["lt", "lastfm"]))
async def now_play(c: yuuna, message: Message):
    if message.chat.type == (ChatType.SUPERGROUP or ChatType.GROUP):
        if not await find_gp(message.chat.id):
            await add_gp(message)
    else:
        pass
    query = input_str(message)
    user_ = message.from_user
    lastdb = await REG.find_one({"id_": user_.id})
    if not (lastdb or query):
        button = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Create LastFM account", url="https://www.last.fm/join"
                    )
                ]
            ]
        )
        reg_ = "__Enter some username or use /set (username) to set yours. If you don't already have a LastFM account, click the button below to register.__"
        await message.reply(reg_, reply_markup=button)
        return
    if query:
        user_lastfm = query
    else:
        user_lastfm = lastdb["last_data"]
    
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
        return await message.reply("__Error. Make sure you entered the correct username__")
    if "error" in view_data:
        return await message.reply(view_data["error"])
    recent_song = view_data["recenttracks"]["track"]
    if len(recent_song) == 0:
        if query:
            return await message.reply(f"__{user_lastfm} don't scrobble any music__")
        else:
            return await message.reply("__You don't scrobble any music__")
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
            scrob =  get_scrob            
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
    if user_.photo:
        photos = message.from_user.photo.big_file_id
        pfp = await yuuna.download_media(photos)
    else:
        pfp = 'yuuna/plugins/misc/pic.jpg'

    # background object
    canvas = Image.new("RGB", (600, 250), (18, 18, 18))
    draw = ImageDraw.Draw(canvas)

    # album art
    try:
        art_ori = Image.open(img_).convert("RGB")
        art = Image.open(img_).convert("RGB")
        enhancer = ImageEnhance.Brightness(art)
        im_ = enhancer.enhance(0.7)
        blur = im_.filter(ImageFilter.GaussianBlur(20))
        blur_ = blur.resize((600, 600))
        canvas.paste(blur_, (0, -250))
        # original art
        art_ori = art_ori.resize((200, 200), Image.ANTIALIAS)
        canvas.paste(art_ori, (25, 25))
    except Exception as ex:
        print(ex)

    # profile pic
    o_pfp = Image.open(pfp).convert("RGB")
    o_pfp = o_pfp.resize((52, 52), Image.ANTIALIAS)
    canvas.paste(o_pfp, (523, 25))

    # set font sizes
    open_sans = ImageFont.truetype(Fonts.OPEN_SANS, 21)

    # open_bold = ImageFont.truetype(Fonts.OPEN_BOLD, 23)
    poppins = ImageFont.truetype(Fonts.POPPINS, 25)
    arial = ImageFont.truetype(Fonts.ARIAL, 25)
    arial23 = ImageFont.truetype(Fonts.ARIAL, 21)

    # assign fonts
    songfont = poppins if checkUnicode(song_name) else arial
    artistfont = open_sans if checkUnicode(artist_name) else arial23

    # draw text on canvas
    white = '#ffffff'
    draw.text((248, 18), truncate(user_lastfm, poppins, 250),
              fill=white, font=poppins)
    draw.text((248, 53), listening,
              fill=white, font=open_sans)
    draw.text((248, 115), truncate(song_name, songfont, 315),
              fill=white, font=songfont)
    draw.text((248, 150), truncate(artist_name, artistfont, 315),
              fill=white, font=artistfont)

    # draw heart
    if loved:
        lov_ = Image.open("yuuna/plugins/misc/heart.png", 'r')
        leve = lov_.resize((25, 25), Image.ANTIALIAS)
        canvas.paste(leve, (248, 190), mask=leve)
        draw.text((278, 187), truncate("loved", artistfont, 315),
                  fill=white, font=artistfont)

    # return canvas
    image = BytesIO()
    canvas.save(image, format="webp")
    image.seek(0)
    artists = artist_name.replace(" ", "+")
    songs = song_name.replace(" ", "+")
    prof = f"https://www.last.fm/user/{user_lastfm}"
    link_ = f"https://www.youtube.com/results?search_query={songs}+{artists}"
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

    os.remove(img_)
    os.remove(pfp)


@yuuna.on_inline_query()
async def now_play(c: yuuna, cb: InlineQuery):
    results = []
    user_ = cb.from_user
    lastdb = await REG.find_one({"id_": user_.id})
    if lastdb:
        user_lastfm = lastdb["last_data"]
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
                    title="Error. Make sure you entered the correct username",
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
                    title="Error. Make sure you entered the correct username",
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
        except ValueError:
            results.append(
                InlineQueryResultArticle(
                    title="Error",
                    thumb_url="https://telegra.ph/file/21581612f3170612568dd.jpg",
                )
            )
            return await cb.answer(
                        results=results,
                        cache_time=1
                    )
        get_track = view_data_["track"]
        get_scrob = int(get_track["userplaycount"]) + 1
        if image_:
            img_ = download(image_)
        else:
            img_ = download("https://telegra.ph/file/328131bd27e0cb8969b31.png")
        loved = int(song_["loved"])

        # User Photo
        if user_.photo:
            photos = cb.from_user.photo.big_file_id
            pfp = await yuuna.download_media(photos)
        else:
            pfp = 'yuuna/plugins/misc/pic.jpg'

        # background object
        canvas = Image.new("RGB", (600, 250), (18, 18, 18))
        draw = ImageDraw.Draw(canvas)

        # album art
        try:
            art_ori = Image.open(img_).convert("RGB")
            art = Image.open(img_).convert("RGB")
            enhancer = ImageEnhance.Brightness(art)
            im_ = enhancer.enhance(0.7)
            blur = im_.filter(ImageFilter.GaussianBlur(20))
            blur_ = blur.resize((600, 600))
            canvas.paste(blur_, (0, -250))

            # original art
            art_ori = art_ori.resize((200, 200), Image.ANTIALIAS)
            canvas.paste(art_ori, (25, 25))
        except Exception as ex:
            print(ex)

        # profile pic
        o_pfp = Image.open(pfp).convert("RGB")
        o_pfp = o_pfp.resize((52, 52), Image.ANTIALIAS)
        canvas.paste(o_pfp, (523, 25))

        # set font sizes
        open_sans = ImageFont.truetype(Fonts.OPEN_SANS, 21)

        # open_bold = ImageFont.truetype(Fonts.OPEN_BOLD, 23)
        poppins = ImageFont.truetype(Fonts.POPPINS, 25)
        arial = ImageFont.truetype(Fonts.ARIAL, 25)
        arial23 = ImageFont.truetype(Fonts.ARIAL, 21)

        # assign fonts
        songfont = poppins if checkUnicode(song_name) else arial
        artistfont = open_sans if checkUnicode(artist_name) else arial23

        # draw text on canvas
        white = '#ffffff'
        draw.text((248, 18), truncate(user_lastfm, poppins, 250),
                fill=white, font=poppins)
        draw.text((248, 53), f"is listening for {get_scrob}th time",
                fill=white, font=open_sans)
        draw.text((248, 115), truncate(song_name, songfont, 315),
                fill=white, font=songfont)
        draw.text((248, 150), truncate(artist_name, artistfont, 315),
                fill=white, font=artistfont)

        # draw heart
        if loved:
            lov_ = Image.open("yuuna/plugins/misc/heart.png", 'r')
            leve = lov_.resize((25, 25), Image.ANTIALIAS)
            canvas.paste(leve, (248, 190), mask=leve)
            draw.text((278, 187), truncate("loved", artistfont, 315),
                    fill=white, font=artistfont)

        # return canvas
        image = BytesIO()
        canvas.save(f"image_{user_.id}.jpg", format="jpeg")
        image.seek(0)
        artists = artist_name.replace(" ", "+")
        songs = song_name.replace(" ", "+")
        response = upload_file(f"image_{user_.id}.jpg")
        inquery = f"https://telegra.ph{response[0]}"
        prof = f"https://www.last.fm/user/{user_lastfm}"
        link_ = f"https://www.youtube.com/results?search_query={songs}+{artists}"
        button_ = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔎 Youtube", url=link_
                    ),
                    InlineKeyboardButton(
                        "↗️ Share", switch_inline_query_current_chat=""
                    ),
                ]
            ]
        )
        # send pic
        textx = f"[\u200c]({inquery})[{user_lastfm}]({prof}) is listening."
        results.append(
            InlineQueryResultArticle(
                title=f"{user_lastfm} now playing",
                description=song_name,
                input_message_content=InputTextMessageContent(textx),
                thumb_url=inquery,
                reply_markup=button_
            )
        )
        """
        results.append(
            InlineQueryResultPhoto(
                title="Sucess",
                photo_url=inquery,
                description="Now Playing",
                caption="test",
                reply_markup=button_

            )
        )"""

        await cb.answer(
                    results=results,
                    cache_time=0,
                )
        os.remove(img_)
        os.remove(pfp)

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
