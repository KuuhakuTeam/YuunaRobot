# Yuuna LastFM Bot
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/YuunaRobot/ >
# PLease read the GNU v3.0 License Agreement in 
# <https://www.github.com/KuuhakuTeam/YuunaRobot/blob/master/LICENSE/>.

# Idea by @k-neel in
# <https://github.com/k-neel/spotipie-bot/>

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
