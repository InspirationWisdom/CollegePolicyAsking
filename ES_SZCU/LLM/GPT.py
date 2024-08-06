# -*- coding: utf-8 -*-
from openai import OpenAI

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key="sk-A4MhAYEINN3O45ctCi5MG4iAYUf97zJYiveum7Ug6mRW0sCA",
    base_url="https://api.chatanywhere.tech/v1"
    # base_url="https://api.chatanywhere.cn/v1"
)

# 非流式响应
def gpt_35_api(messages: list):
    """为提供的对话消息创建新的回答

    Args:
        messages (list): 完整的对话消息
    """
    completion = client.chat.completions.create(model="gpt-3.5-turbo", messages=messages)
    print(completion.choices[0].message.content)

def gpt_35_api_stream(messages: list):
    """为提供的对话消息创建新的回答 (流式传输)

    Args:
        messages (list): 完整的对话消息
    """
    stream = client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=messages,
        stream=True,
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")

if __name__ == '__main__':

    str1 = '发布者：王洁莹发布时间：2024-01-13浏览次数：10寒假即将来临，不少在苏就读的大学生们，陆续踏上返乡的归途，准备回家过年。那么，苏州参保的大学生寒假期间在老 家发生的医疗费用能否报销？如何就医更加省时省力呢？这份温馨提示请收好。一、返乡大学生可提前办理异地就医，就医地符合规定的费用可以直接划卡结算。1. 异地就医流程第一步：先备案第二步：选择就医地第三步：持卡（码）就医2. 异地就医办理渠道（1）江苏医保云APP/江苏医保云小程序支付宝入口（用于申请省内、跨省异地就医备 案）。（2）国家医保服务平台APP/国家异地就医备案小程序（仅用于申请跨省异地就医备案）。（3）微信公众号（4）园区社保中心APP（工业园区参保人员适用）。（5）医(社)保经办机构柜面。3. 温馨提示大学生回户籍地就医，办理异地就医备案类型选择“异地长期居住人员”，提供居民身份证/社会保障卡、长期居住认定材料（居住证明）材 料。如选择“其他临时外出就医人员”，在备案地发生的符合医疗保险结付规定的医疗费用，按原规定结付比例的80%结付。二、未办理异地备案的，也可以由个人先行垫付，回苏后携带本人医保电子凭证或社会保障卡、身份证（或户籍地材料）、病历记录、费用明确清单和医院收费票据原件等材料到参保地医疗保障经办机构办理零星报销，按规定 享受医保待遇。文章素材来源：“苏州社保”公众号地址：江苏省苏州市吴中区吴中大道1188号（215104）电话：0512-66555732Copyright © 苏州城市学院 苏ICP备2021049900号-1'
    messages = [{'role': 'user','content': '将下面内容，分点表述：' + str1},]
    # 非流式调用
    # gpt_35_api(messages)
    # 流式调用
    #gpt_35_api_stream(messages)