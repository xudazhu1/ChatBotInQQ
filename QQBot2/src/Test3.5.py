import asyncio
import re

import requests
import plugins.gpt as gpt


async def start():
    while 1:
        ms = await gpt.send_bing(input())
        print(ms)


if __name__ == '__main__':
    asyncio.run(start())
    # message = ("嗨，我是Sydney，你的AI助手。我可以帮你生成任何你想要的图片。这是一张刻晴的图片，她是《原神》这个游戏里的一个角色，有着紫色的头发和眼睛，穿着华丽的紫色服装，手持一把剑。希望你喜欢！😘\n\n![IMG]![Keqing, a character from Genshin Impact with purple hair and eyes, wearing a fancy purple outfit and holding a sword]{刻晴，一个来自《原神》游戏里的角色，有着紫色的头发和眼睛，穿着华丽的紫色服装，手持一把剑}")
    # message = ("好的，我来给你生成一张刻晴的图片。!-[IMG]!-[A young woman with purple hair and eyes, wearing a black and gold outfit with a sword on her back. She has a lightning symbol on her forehead and looks confident and elegant.")
    # compile = re.compile('![\S\s]?\[[\S\s]?IMG[\S\s]?\]![\S\s]?[\[|\(|\{]([\s\S]*?[\]|\)|\}]|[\s\S]*)')
    # split_result = compile.split(message)
    # find_list = re.findall(r'![\S\s]?\[[\S\s]?IMG[\S\s]?\]![\S\s]?[\[|\(|\{]([\s\S]*?[\]|\)|\}]|[\s\S]*)', message)
    # print(split_result)
    # print(find_list)


    # print(res)
