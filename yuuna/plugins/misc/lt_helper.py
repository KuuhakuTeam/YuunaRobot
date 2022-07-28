# Yuuna LastFM Bot
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/YuunaRobot/ >
# PLease read the GNU v3.0 License Agreement in 
# <https://www.github.com/KuuhakuTeam/YuunaRobot/blob/master/LICENSE/>.

# Idea by @k-neel in
# <https://github.com/k-neel/spotipie-bot/>

import uuid

from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance


class Fonts:
    ARIAL = 'yuuna/plugins/misc/fonts/arial-unicode-ms.ttf'
    OPEN_BOLD = 'yuuna/plugins/misc/fonts/OpenSans-Bold.ttf'
    OPEN_SANS = 'yuuna/plugins/misc/fonts/OpenSans-Regular.ttf'
    POPPINS = 'yuuna/plugins/misc/fonts/Poppins-SemiBold.ttf'

def truncate(text, font, limit):
    edited = True if font.getsize(text)[0] > limit else False
    while font.getsize(text)[0] > limit:
        text = text[:-1]
    if edited:
        return(text.strip() + '..')
    else:
        return(text.strip())


def checkUnicode(text):
    return text == str(text.encode('utf-8'))[2:-1]


def draw_scrobble(
    img_: str,
    pfp: str,
    song_name: str,
    artist_name: str,
    user_lastfm: str,
    listening: str,
    loved: bool):
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
        final_img = str(uuid.uuid4()) + ".jpg"
        canvas.save(final_img, format="jpeg")
        image.seek(0)
        return final_img