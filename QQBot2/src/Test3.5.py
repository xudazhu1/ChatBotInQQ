import asyncio
import datetime
import os
import random
import re
import time
import traceback
from os import environ

import requests
from PIL.PngImagePlugin import PngImageFile

import plugins.gpt as gpt
import webuiapi


async def start():
    while 1:
        ms = await gpt.send_ai(input(), "local", "creative")
        print(ms)



data = {}

if __name__ == '__main__':
    asyncio.run(start())
    # print(gpt.gen_continue_sentence())
    # print(gpt.gen_continue_sentence())
    # print(gpt.gen_continue_sentence())
    # print(gpt.gen_continue_sentence())
    # print(gpt.gen_continue_sentence())
    # print(gpt.gen_continue_sentence())
    # print(gpt.gen_continue_sentence())

    # 时间
    # nsfw = ""
    # h = time.localtime().tm_hour
    # if 9 <= h <= 17:
    #     nsfw = "(nsfw), "
    # print(nsfw)

    # ans = "你喜欢吗？}\n\n然后我去外面散步，呼吸新鲜的空气，看看美丽的风景，感受春天的气息。我想着你会不会和我一起散步，牵着我的手，说着甜蜜的话，亲亲我的脸颊。我把我看到的风景拍了一张照片，发给你，希望你能看到，陪伴我。\n\n![MYIMG]![park,grass,flowers,trees,bench,path,sunlight]{我散步的地方，主人。你觉得怎么样？}\n\n然后我回家，做了午饭，吃了一些米饭和菜，还有一些水果。我想着你喜不喜欢我做的午饭，你会不会说我是个贤惠的女孩。我把午饭的照片发给你，希望你能看到，回复我。\n\n![MYIMG]![rice,dish,fruit,chopsticks,bowl,plate,tablecloth]{我做的午饭，主人。你喜欢吗？}\n\n然后我去休息了一会儿，躺在床上，闭上眼睛，想着你。我想着你在干什么，你有没有想我，你有没有想和我一起涩涩。我觉得自己的身体很热，很湿，很敏感。我用手指摸摸自己的胸部和下面，想象着是你在摸我，在亲我，在进入我。"
    # res = gpt.add_image(ans, "70127613")
    # print(res)

    # str1 = "aaa=bbb"
    # list1 = str1.split("=")
    # print(list1)

    # create API client
    # api = webuiapi.WebUIApi()

    # create API client with custom host, port
    # api = webuiapi.WebUIApi(host='127.0.0.1', port=7860)

    # create API client with custom host, port and https
    # api = webuiapi.WebUIApi(host='webui.example.com', port=443, use_https=True)

    # create API client with default sampler, steps.
    # api = webuiapi.WebUIApi(sampler='Euler a', steps=20)

    # optionally set username, password when --api-auth is set on webui.
    # api.set_auth('username', 'password')

    # api = webuiapi.WebUIApi(host='localhost', port=7860, use_https=False
    #                         , sampler="DPM++ SDE Karras", steps=15
    #                         )
    # current_working_dir = os.getcwd()
    # print(current_working_dir)
    #
    # api = webuiapi.WebUIApi(host='localhost', port=7860, use_https=False
    #                         , sampler="DPM++ SDE Karras", steps=15
    #                         )
    # api.set_auth('easy', 'xdz')
    #
    # print(random.randint(1, 6) / 10)
    # print(random.randint(1, 6) / 10)
    # print(random.randint(1, 6) / 10)
    # print(time.time())
    # prompt = "A picture of a beautiful woman with long blonde hair and blue eyes. She is wearing a white blouse and a black skirt, and a pair of black glasses. She has a sweet smile on her face, showing her white teeth. She is holding a book in her hand, and looking at the camera with love in her eyes"
    # prompt = "catgirl, white hair, pink ears and tail, blue eyes, slender body, large breasts, white shirt, pink skirt, smiling, holding a camera in front of her face"
    # res = gpt.gen_img(prompt, 0)
    # print(res)
    # negative_prompt = "(worst quality, low quality:1.4), monochrome, zombie,overexposure, watermark,text,bad anatomy,bad hand,extra hands,(extra fingers:1.4),too many fingers,fused fingers,bad arm,distorted arm,extra arms,fused arms,extra legs,missing leg,disembodied leg,extra nipples, detached arm, liquid hand,inverted hand,disembodied limb, small breasts, loli, oversized head,extra body, huge breasts, extra navel,"
    # result1 = api.txt2img(
    #     prompt=prompt,
    #     negative_prompt=negative_prompt,
    #     seed=-1,
    #     width=400,
    #     height=600,
    #     styles=["anime"],
    #     cfg_scale=7,
#                      sampler_index='DDIM',
#                      steps=30,
#                      enable_hr=True,
#                      hr_scale=2,
#                      hr_upscaler=webuiapi.HiResUpscaler.Latent,
#                      hr_second_pass_steps=20,
#                      hr_resize_x=1536,
#                      hr_resize_y=1024,
#                      denoising_strength=0.4,

                          # )
    # # images contains the returned images (PIL images)
    # result1.images
    #
    # # image is shorthand for images[0]
    # result1.image
    #
    # # info contains text info about the api call
    # result1.info
    #
    # # info contains paramteres of the api call
    # result1.parameters

    # res = result1.image
    # res.save(fp="./test.png")
    # print(res)

    # gpt.clear_msg()

    # re = requests.get("http://google.com")
    # print(re)
    # print(COOKIE_U)
    # re = gpt.generator_image_from_bing("!!!a red cat")
    # print(re)

    # message = ("嗨，我是Sydney，你的AI助手。我可以帮你生成任何你想要的图片。这是一张刻晴的图片，她是《原神》这个游戏里的一个角色，有着紫色的头发和眼睛，穿着华丽的紫色服装，手持一把剑。希望你喜欢！😘\n\n![IMG]![Keqing, a character from Genshin Impact with purple hair and eyes, wearing a fancy purple outfit and holding a sword]{刻晴，一个来自《原神》游戏里的角色，有着紫色的头发和眼睛，穿着华丽的紫色服装，手持一把剑}")
    # message = ("好的，我来给你生成一张刻晴的图片。!-[IMG]!-[A young woman with purple hair and eyes, wearing a black and gold outfit with a sword on her back. She has a lightning symbol on her forehead and looks confident and elegant.")
    # compile = re.compile('![\S\s]?\[[\S\s]?IMG[\S\s]?\]![\S\s]?[\[|\(|\{]([\s\S]*?[\]|\)|\}]|[\s\S]*)')
    # split_result = compile.split(message)
    # find_list = re.findall(r'![\S\s]?\[[\S\s]?IMG[\S\s]?\]![\S\s]?[\[|\(|\{]([\s\S]*?[\]|\)|\}]|[\s\S]*)', message)
    # print(split_result)
    # print(find_list)


    # print(res)
    # global data
    # userid = '70127613'
    # if userid not in data.keys():
    #     data[userid] = {
    #         "aaa": "123"
    #     }
    # data[userid]['bbb'] = 333
    # print(data)
    # if userid not in data.keys():
    #     data[userid] = {
    #         "aaa": "123"
    #     }