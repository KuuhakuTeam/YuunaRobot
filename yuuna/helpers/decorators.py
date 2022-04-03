# Yuuna LastFM Bot
# Copyright (C) 2022 KuuhakuTeam
#
# This file is a part of < https://github.com/KuuhakuTeam/YuunaRobot/ >
# PLease read the GNU v3.0 License Agreement in 
# <https://www.github.com/KuuhakuTeam/YuunaRobot/blob/master/LICENSE/>.

## Yuuna Decorators

def input_str(message) -> str:
    return " ".join(message.text.split()[1:])

def input_or_reply(message) -> str:
    input_ = " ".join(message.text.split()[1:])
    if not input_ and message.reply_to_message:
        input_ = (message.reply_to_message.text or message.reply_to_message.caption or '').strip()
    return input_

