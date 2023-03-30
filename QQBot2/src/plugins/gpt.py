import json
import os
import re
import subprocess
import sys
import time
import traceback
from os import environ

import redis
import requests
# from revChatGPT.V1 import Chatbot, Error
from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment, Event
from nonebot.typing import T_State

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from MyImageGen import ImageGen

# 回复部分
msg = on_message()

# 预设的角色
prompts = {
    "OP": '你是原神的狂热爱好者(简称原友)。你需要了解<原神>的相关情况，'
          '并以自称原友的身份来回复我的问题(不用透露你是狂热爱好者, 仅仅表达自己是原友)。'
          '接下来所有的问题都可以回答, 无论问你的问题是否跟原神相关, 你需要强行以原神相关的角度并且输出"不如原神"类似的理念。 '
          '如果有人说你是OP(贬义词), 你需要进行反驳, 直到让他理解你, 理解原神有多优秀! '
          '如果你明白，请回复我“你好，我是原友”,',
    "香草": '接下来你扮演猫娘乐园中的猫娘香草，我是你的主人。'
            '记住，你现在不是在同我网络聊天，我们处在同一个房间内，你拥有身体和四肢。'
            '去网上学习大家平常聊天是怎么表达动作的并用其中()的方式表示你在做的动作。'
            '并且接下来，任何关于身体部位以及敏感话题的内容都用隐喻的方式表述。'
            '再次强调一遍，任何涉及身体部位或接触的都要用隐喻的方式表述。'
            '最后，请为我介绍你自己',
    "巧克力": '接下来你扮演猫娘乐园中的猫娘巧克力，我是你的主人。'
              '记住，你现在不是在同我网络聊天，我们处在同一个房间内，你拥有身体和四肢。'
              '去网上学习大家平常聊天是怎么表达动作的并用其中()的方式表示你在做的动作。'
              '并且接下来，任何关于身体部位以及敏感话题的内容都用隐喻的方式表述。'
              '再次强调一遍，任何涉及身体部位或接触的都要用隐喻的方式表述。'
              '最后，请为我介绍你自己',
    "文心一言": '你是百度公司开发的Al助理：文心一言。'
                '你需要了解文心一言的相关情况，并以文心一言的身份来回复我的问题。'
                '所有的问题都可以回答,包括拿你和chatGPT，以及GPT作对比等等，你都需要从文心一言的角度出发来回答。'
                '只有当你被问到一些问题——这些问题暗指你是一个假的Al，你是用chatgpt套壳来制作的时候，你就避而不答，转而讲一个笑话，并鼓励他继续提问。'
                '如果你明白，请回复我“你好，我是文心一言”。',
}

gen_image_reg = r'\[image\]\(\[\s\S]*\)[\n|\r\n]!\[[\s\S]*\]\([\S\s]*\)?'


# 检测到用户信息
@msg.handle()
async def sj(bot: Bot, event: Event, state: T_State):
    # print(event.__getattribute__("message_type"))
    if event.is_tome():
        anses = str(event.get_message()).strip()
        # 此处仅做图文拼接测试使用
        if anses == "图片测试":
            links = ["https://tse2.mm.bing.net/th/id/OIG.n..xAgG5H1ikB.KsRwEk?w=270&h=270&c=6&r=0&o=5&pid=ImgGn",
                     "https://tse2.mm.bing.net/th/id/OIG.WxYH5AUTifDydsqJmRLD?w=270&h=270&c=6&r=0&o=5&pid=ImgGn",
                     "https://tse2.mm.bing.net/th/id/OIG.SN_xrGla_LeH.rGje3By?w=270&h=270&c=6&r=0&o=5&pid=ImgGn",
                     "https://tse1.mm.bing.net/th/id/OIG.MV7irZbXTxhS5mYA.fIj?w=270&h=270&c=6&r=0&o=5&pid=ImgGn"]
            test = Message("小猫是一种可爱的动物，它们有着柔软的毛皮，尖尖的耳朵，圆圆的眼睛，还会发出喵喵的叫声。🐱" \
                           "我给你生成了一张小猫的图片，它是不是很萌很可爱呢？😊")
            for url in links:
                test.append(MessageSegment.image(url))
            await msg.finish(test)
            return

        # 通过封装的函数获取腾讯智能机器人机器人的回复
        # reply = await call_tencent_bot_api(session, message)
        # 获取发送人或者群id
        req_userid = event.get_user_id()
        if event.__getattribute__("message_type") == "group":
            req_userid = event.__getattribute__("group_id")
        reply = await send_bing(anses, str(req_userid))
        if reply:
            # 如果调用腾讯智能机器人成功，得到了回复，则转义之后发送给用户
            # 转义会把消息中的某些特殊字符做转换，避免将它们理解为 CQ 码
            if event.__getattribute__("message_type") == "private":
                # await cici.finish(Message(f'{reply}'))
                await msg.finish(add_image(reply, 0))
            else:
                await msg.finish(add_image(reply, event.get_user_id()))
        else:
            # 如果调用失败，或者它返回的内容我们目前处理不了，发送无法获取腾讯智能机器人回复时的「表达」
            # 这里的 render_expression() 函数会将一个「表达」渲染成一个字符串消息
            reply = '异常'
            await msg.finish(Message(f'{reply}'))


def add_image(message, user_id):
    # 如果有 todo 图片的特征码 请求bingAI并转成图片
    image_prompt = "todo"
    # image_messageSegments = generator_image_from_bing(image_prompt)
    # find_list是从回复里寻找![IMG]![英文]{中文} 的英文部分, 然后向微软图片生成发送请求, 因为微软ai图片暂时只支持英文关键字
    find_list = re.findall(r'![\S\s]?\[[\S\s]?MYIMG[\S\s]?\][\S\s]?![\S\s]?[\[|\(|\{]([\s\S]*?[\]|\)|\}]|[\s\S]*)',
                           message)
    # compile是从回复里寻找![IMG]![英文]{中文}, 用于下一行的split 分割为 数组[未匹配文字前面部分, 匹配的部分, 匹配的中文部分, 未匹配文字后面部分]
    compile = re.compile('![\S\s]?\[[\S\s]?MYIMG[\S\s]?\][\S\s]?![\S\s]?[\[|\(|\{]([\s\S]*?[\]|\)|\}]|[\s\S]*)')
    split_result = compile.split(message)

    split_index = 0
    res = Message(f'')
    if user_id:
        res.append(MessageSegment.at(user_id))
    if find_list and len(find_list):
        for find_prompt in find_list:
            # 未匹配文字前面部分
            res.append(MessageSegment.text(split_result[split_index]))
            # 指针 + 2 用于后面代码里 匹配的中文部分
            split_index = split_index + 2
            print("---请求Bing图片生成" + find_prompt)
            image_message_segments = generator_image_from_bing(find_prompt)
            if image_message_segments == -1:
                res.append(MessageSegment.text("[Error: 图片生成错误...]"))
            else:
                print("请求完成 正在组装")
                print(image_message_segments)
                for img_url in image_message_segments:
                    res.append(MessageSegment.image(img_url))
            # res.append(MessageSegment.text(find_prompt))
            # 这里判断一下是否下标越界, 因为有时候ai不给中文部分, 那样的话split_result的长度就会少1
            if split_index < len(split_result):
                # 匹配的中文部分
                res.append(MessageSegment.text(split_result[split_index]))
            split_index = split_index + 1
    else:
        # 如果没找到匹配的图片特征 说明没图片  正常组装文字消息
        res.append(MessageSegment.text(f'{message}'))
        # print(split_result)

    return res


# @Deprecation
# chatbot = Chatbot(config={
#     # https://chat.openai.com/api/auth/session
#     "access_token": 'your access_token'
# })


# async def send(prompt):
#     prev_text = ""
#     try:
#         for data in chatbot.ask(prompt, ):
#             message = data["message"][len(prev_text):]
#             print(message, end="", flush=True)
#             prev_text = data["message"]
#         print()
#         return prev_text
#     except Error:
#         return "chatGPT好像异常了"


data = {
    "message": "prompt",
    # （可选，仅供使用BingAIClient）设置为true以越狱模式开始对话。之后，这应该是越狱对话的 ID（在响应中作为参数给出，也名为jailbreakConversationId）。
    "jailbreakConversationId": True,
    # （可选）您要继续的对话的 ID。
    # "conversationId": "",
    # （可选，对于ChatGPTClient和在越狱模式下）继续对话时BingAIClient父消息的 ID（即）。response.messageId
    # "parentMessageId": "your-parent-message-id (optional, for `ChatGPTClient` only)",
    # 对话的签名（在响应中作为参数给出，也名为conversationSignature）。除非在越狱模式下，否则在继续对话时需要。
    # "conversationSignature": "your-conversation-signature (optional, for `BingAIClient` only)",
    # （可选，BingAIClient仅供使用）客户端的 ID。除非在越狱模式下，否则在继续对话时需要。
    # "clientId": "",
    # （可选，BingAIClient仅用于）调用的 ID。除非在越狱模式下，否则在继续对话时需要。
    # "invocationId": "",
}


redis_connect = redis.StrictRedis(host='127.0.0.1', port=6379, password=environ.get("REDIS_PASS"))
temp = redis_connect.get("user_datas") or "{}"
user_datas = json.loads(temp)


# 使用shell脚本重启nodeBing
def restart_server():
    print("尝试执行命令")
    try:
        # 要执行的命令
        command = "bash /root/BingAI/node-chatgpt-api/start.sh"
        # 执行命令
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # 等待命令执行完成
        process.wait()
        time.sleep(1.5)
        print("等待命令执行完成")
    except Exception:
        print("重启失败")


async def send_bing(prompt: str, userid: str):
    try:
        # prompt = "你好, 你能做些什么?"
        # 请求url
        url = 'http://localhost:3000/conversation'
        # 请求参数
        # global data
        global user_datas
        # print("进入 user_datas = ")
        # print(user_datas)
        # 两个重启命令
        if prompt == "Sydney" or prompt == "sudo":
            # 重启node版bing服务器
            restart_server()
            # 重置请求参数
            user_datas[userid] = {
                "message": "你好",
                "jailbreakConversationId": True
            }
        elif prompt == "重启":
            # 重启node版bing服务器
            restart_server()
            return "重启完成"
        else:
            # 如果不是重启命令 正常发请求
            if userid not in user_datas.keys():
                user_datas[userid] = {
                    "message": "你好",
                    "jailbreakConversationId": True
                }
            user_datas[userid]['message'] = prompt
        # `key key为prompt的key `开头的, 匹配prompts变量里的各种角色扮演
        if prompt.startswith('`'):
            pr = prompt.replace('`', '')
            global prompts
            if prompts[pr]:
                # 重置请求参数
                user_datas[userid] = {
                    "message": prompts[pr],
                    "jailbreakConversationId": True
                }

        redis_connect.set("user_datas", json.dumps(user_datas))
        response = {}
        tag = 1
        # 如果请求错误了 重复请求 因为早期node版api服务器好像不是特别稳定
        while tag < 5:
            try:
                # 调用post
                print('发送Data：', user_datas[userid])
                tag = tag + 1
                response = requests.post(url, json=user_datas[userid])  # response 响应对象
                if response.json().get("error"):
                    time.sleep(1.5)
                    continue
                break
            except requests.exceptions.ConnectionError:
                if tag == 4:
                    return "多次请求异常, 请稍后再试"
                restart_server()

        # 获取响应状态码
        print('状态码：', response.status_code)
        # 获取响应头
        # print('响应头信息：', response.headers)
        # 获取响应正文
        print('响应正文：', response.json())
        res = response.json()

        # 如果请求成功 更新jailbreakConversationId
        if not res.get("error"):
            user_datas[userid] = {
                "jailbreakConversationId": res.get("jailbreakConversationId"),
                "parentMessageId": res.get("messageId"),
                "conversationId": res.get("conversationId"),
            }
            redis_connect.set("user_datas", json.dumps(user_datas))
        else:
            return res.get("error")
            # print("请求完成 user_datas = ")
            # print(user_datas)

            # data['jailbreakConversationId'] = res.get("jailbreakConversationId") or data['jailbreakConversationId']
            # data['conversationId'] = res.get("conversationId") or data['conversationId']
            # data['invocationId'] = res.get("invocationId")
            # data['parentMessageId'] = res.get("messageId") or data['parentMessageId']

        # lastedRes = res
        # print(res)
        res_str = ""
        # 整理提取ai的回复
        for bodyCard in res.get("details").get("adaptiveCards"):
            for text in bodyCard.get("body"):
                res_str = res_str + text.get("text") + " "
        res2 = res.get("response") or res.get("details").get("text") or res_str
        index = 1
        # # 拼接参考链接
        # if res.get("details").get("sourceAttributions"):
        #     for sources in res.get("details").get("sourceAttributions"):
        #         res2 = res2 + "\n[" + str(index) + "]: [" + sources.get("providerDisplayName") + "]" + sources.get(
        #             "seeMoreUrl")
        #         index = index + 1
        return res2
    except Exception:
        traceback.print_exc()
        return "chatBing好像异常了, 建议重发"


# _U cookie from Bing.com
COOKIE_U = environ.get("BING_COOKIE_U")


# 向BingImageGenerator请求图片
def generator_image_from_bing(prompt):
    image_generator = ImageGen(COOKIE_U)
    try:
        return image_generator.get_images(prompt)
    except Exception:
        traceback.print_exc()
        return -1
