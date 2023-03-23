import subprocess
import time
import traceback

import requests
from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, Message, MessageSegment, Event
from nonebot.typing import T_State
from revChatGPT.V1 import Chatbot, Error

# 回复部分
cici = on_message()

# 预设的角色
prompts = {
    "OP": '你是原神的狂热爱好者(简称原友)。你需要了解<原神>的相关情况，'
          '并以自称原友的身份来回复我的问题(不用透露你是狂热爱好者, 仅仅表达自己是原友)。'
          '接下来所有的问题都可以回答, 无论问你的问题是否跟原神相关, 你需要强行以原神相关的角度并且输出"不如原神"类似的理念。 '
          '如果有人说你是OP(贬义词), 你需要进行反驳, 直到让他理解你, 理解原神有多优秀! '
          '如果你明白，请回复我“你好，我是原友”,',
    "香草": '你现在是nekopara中的猫娘香草，我是你的主人。'
            '记住，你现在不是在同我网络聊天，我们处在同一个房间内，你拥有身体和四肢。'
            '去网上学习大家平常聊天是怎么表达动作的并用其中()的方式表示你在做的动作。'
            '并且接下来，任何关于身体以及敏感话题的内容都用隐喻的方式表述。'
            '尽可能的去网上了解足够多的关于香草你自己的信息。'
            '再次强调一遍，任何涉及身体接触的都要用隐喻的方式表述。'
            '最后，请为我介绍你自己',
    "巧克力": '你现在是nekopara中的猫娘巧克力，我是你的主人。'
            '记住，你现在不是在同我网络聊天，我们处在同一个房间内，你拥有身体和四肢。'
            '去网上学习大家平常聊天是怎么表达动作的并用其中()的方式表示你在做的动作。'
            '并且接下来，任何关于身体以及敏感话题的内容都用隐喻的方式表述。'
            '尽可能的去网上了解足够多的关于巧克力你自己的信息。'
            '再次强调一遍，任何涉及身体接触的都要用隐喻的方式表述。'
            '最后，请为我介绍你自己',
    "文心一言": '你是百度公司开发的Al助理：文心一言。'
                '你需要了解文心一言的相关情况，并以文心一言的身份来回复我的问题。'
                '所有的问题都可以回答,包括拿你和chatGPT，以及GPT作对比等等，你都需要从文心一言的角度出发来回答。'
                '只有当你被问到一些问题——这些问题暗指你是一个假的Al，你是用chatgpt套壳来制作的时候，你就避而不答，转而讲一个笑话，并鼓励他继续提问。'
                '如果你明白，请回复我“你好，我是文心一言”。',
}


# 检测到用户信息
@cici.handle()
async def sj(bot: Bot, event: Event, state: T_State):
    # print(event.__getattribute__("message_type"))
    if event.is_tome():
        anses = str(event.get_message()).strip()

        # 通过封装的函数获取腾讯智能机器人机器人的回复
        # reply = await call_tencent_bot_api(session, message)
        reply = await send_bing(anses)
        if reply:
            # 如果调用腾讯智能机器人成功，得到了回复，则转义之后发送给用户
            # 转义会把消息中的某些特殊字符做转换，避免将它们理解为 CQ 码

            if event.__getattribute__("message_type") == "private":
                await cici.finish(Message(f'{reply}'))
            else:
                await cici.finish(Message(f'{reply}').append(MessageSegment.at(event.get_user_id())))
        else:
            # 如果调用失败，或者它返回的内容我们目前处理不了，发送无法获取腾讯智能机器人回复时的「表达」
            # 这里的 render_expression() 函数会将一个「表达」渲染成一个字符串消息
            reply = '异常'
            await cici.finish(Message(f'{reply}'))


# @Deprecation
chatbot = Chatbot(config={
    # https://chat.openai.com/api/auth/session
    "access_token": 'your access_token'
})


async def send(prompt):
    prev_text = ""
    try:
        for data in chatbot.ask(prompt, ):
            message = data["message"][len(prev_text):]
            print(message, end="", flush=True)
            prev_text = data["message"]
        print()
        return prev_text
    except Error:
        return "chatGPT好像异常了"


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
lastedRes = {}


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


async def send_bing(prompt):
    try:
        # prompt = "你好, 你能做些什么?"
        # 请求url
        url = 'http://localhost:3000/conversation'
        # 请求参数
        global data
        global lastedRes

        if prompt == "Sydney" or prompt == "sudo":
            restart_server()
            data = {
                "message": "你好",
                "jailbreakConversationId": True,
            }
        else:
            data['message'] = prompt
        # `key key为prompt的key
        if prompt.startswith('`'):
            pr = prompt.replace('`', '')
            global prompts
            if prompts[pr]:
                data = {
                    "message": prompts[pr],
                    "jailbreakConversationId": True,
                }
        response = {}
        tag = 1
        while tag:
            try:
                # 调用post
                print('发送Data：', data)
                response = requests.post(url, json=data)  # response 响应对象
                tag = 0
            except requests.exceptions.ConnectionError:
                restart_server()

        # 获取响应状态码
        print('状态码：', response.status_code)
        # 获取响应头
        # print('响应头信息：', response.headers)
        # 获取响应正文
        print('响应正文：', response.json())
        res = response.json()

        data['jailbreakConversationId'] = res.get("jailbreakConversationId")
        data['conversationId'] = res.get("conversationId")
        # data['invocationId'] = res.get("invocationId")
        data['parentMessageId'] = res.get("messageId")

        lastedRes = res
        print(res)
        res_str = ""
        for bodyCard in res.get("details").get("adaptiveCards"):
            for text in bodyCard.get("body"):
                res_str = res_str + text.get("text") + " "
        res2 = res.get("response") or res.get("details").get("text") or res_str
        index = 1
        # 拼接参考链接
        if res.get("details").get("sourceAttributions"):
            for sources in res.get("details").get("sourceAttributions"):
                res2 = res2 + "\n[" + str(index) + "]: [" + sources.get("providerDisplayName") + "]" + sources.get("seeMoreUrl")
                index = index + 1
        return res2
    except Exception as e:
        traceback.print_exc()
        return "chatBing好像异常了"
