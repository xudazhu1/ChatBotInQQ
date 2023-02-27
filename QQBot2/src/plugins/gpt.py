from nonebot import on_message
from nonebot.adapters.onebot.v11 import Bot, Message, Event
from nonebot.typing import T_State
from revChatGPT.V1 import Chatbot, Error

# 回复部分
cici = on_message()


# 检测到用户信息
@cici.handle()
async def sj(bot: Bot, event: Event, state: T_State):
    # print(event.__getattribute__("message_type"))
    if event.is_tome():
        anses = str(event.get_message()).strip()
        # 通过封装的函数获取腾讯智能机器人机器人的回复
        # reply = await call_tencent_bot_api(session, message)
        reply = await send(anses)
        if reply:
            # 如果调用腾讯智能机器人成功，得到了回复，则转义之后发送给用户
            # 转义会把消息中的某些特殊字符做转换，避免将它们理解为 CQ 码
            await cici.finish(Message(f'{reply}'))
        else:
            # 如果调用失败，或者它返回的内容我们目前处理不了，发送无法获取腾讯智能机器人回复时的「表达」
            # 这里的 render_expression() 函数会将一个「表达」渲染成一个字符串消息
            reply = '异常'
            await cici.finish(Message(f'{reply}'))


chatbot = Chatbot(config={
    "access_token": 'your chatGPT access_token'
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
