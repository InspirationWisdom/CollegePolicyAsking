import requests
API_URL = 'https://model-app-func-modelscb-a-bfcf-dpnnbuwker.cn-shanghai.fcapp.run/invoke'
def post_request(url, json):
	with requests.Session() as session:
		response = session.post(url,json=json,)
		return response


# payload = {"input":{"messages":[{"content":"谢谢你，我又解决了一个问题","role":"user"}]},"parameters":{"do_sample":True,"max_length":2048}}
# response = post_request(API_URL, json=payload)
# print("response:", response.json())

#返回总结后的文本
def GML_summary(text):
	payload = {"input":{"messages":[{"content":"总结下面文本："+text,"role":"user"}]},"parameters":{"do_sample":True,"max_length":2048}}
	response = post_request(API_URL, json=payload)
	return response.json()

#返回回答问题的文本
def GML_answer(text,question = ''):
	payload = {"input":{"messages":[{"content":"结合问题和文本回答。问题:"+question+"文本:"+text ,"role":"user"}]},"parameters":{"do_sample":True,"max_length":2048}}
	response = post_request(API_URL, json=payload)
	return response.json()

#返回适用于Elasticsearch的搜索的分词结果
def GML_search(text):
	payload = {"input":{"messages":[{"content":"提取问题关键词，只返回关键词："+text,"role":"user"}]},"parameters":{"do_sample":True,"max_length":2048}}
	response = post_request(API_URL, json=payload)
	return response.json()

#返回问题和回答的文本
