import requests
import google.generativeai as genai
import os

genai.configure(api_key="Don't you want to know?")
model = genai.GenerativeModel("gemini-1.5-flash")

# def post_request(url, json):
#     with requests.Session() as session:
#         response = session.post(url, json=json, )
#         return response


# payload = {"input":{"messages":[{"content":"谢谢你，我又解决了一个问题","role":"user"}]},"parameters":{"do_sample":True,"max_length":2048}}
# response = post_request(API_URL, json=payload)
# print("response:", response.json())

#返回总结后的文本
def GML_summary(text):
    response = model.generate_content("总结下面文本：" + text)
    return response.text


#返回回答问题的文本
def GML_answer(text, question=''):
    response = model.generate_content("结合问题和文本回答，并将回答控制在100字以内。问题:" + question + "文本:" + text)
    return response.text


#返回适用于Elasticsearch的搜索的分词结果
def GML_question_to_keywords(text):
    response = model.generate_content("提取问题关键词，只返回关键词：" + text)
    return response.text

