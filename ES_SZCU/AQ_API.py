from flask import Flask, request, jsonify
from flask_cors import CORS
from Elasticsearch import search as Es_search
import LLM.GML as GML
import speech_recognition as sr
from pydub import AudioSegment
app = Flask(__name__)

# 允许跨域请求
CORS(app, supports_credentials=True)

#编写接口
"""
功能：连接GML功能，完成AI问答
"""
@app.route('/ChatAI', methods=['POST'])
def ChatAI():
    # 获取POST请求中的数据
    file = request.files['file']
    audio = AudioSegment.from_file(file)
    audio_mono = audio.set_channels(1)
    audio_mono.export("./converted_audio_mono.wav", format="wav")
    recognizer = sr.Recognizer()

    with sr.AudioFile("./converted_audio_mono.wav") as source:
        print("正在读取音频文件...")
        audio_data = recognizer.record(source)  # 读取整个音频文件

    text = ""
    try:
        # 使用Google Web Speech API将音频转换为文本
        print("正在将音频转换为文本...")
        text = recognizer.recognize_google(audio_data, language="zh-CN")  # "zh-CN"表示中文
        print("识别结果:", text)
    except sr.RequestError as e:
        print("无法请求结果; {0}".format(e))
    except sr.UnknownValueError:
        print("无法理解音频")

    #进行Elasticsearch搜索
    #对问题进行关键词提取
    #只获取问题前2030个字符
    question = text[:2030]
    question_keywords = GML.GML_question_to_keywords(question)

    #如果extraQuestion中有字符“关键词”，去除
    if "关键词" in question_keywords:
        question_keywords = question_keywords.replace("关键词", "")
        question_keywords = question_keywords.replace("：", "")
    print("关键词：" + question_keywords)

    # 获取搜索结果的总数
    total_num = Es_search.get_total('notices_manual', question_keywords)
    #获取搜索结果
    resp = Es_search.search_text('notices_manual', question_keywords)

    #整合为一个json格式的数据
    result = result_to_json(resp)
    print(result)
    #获取页数相关内容
    page_num = pagenum_to_json(total_num, 0)

    #判断结果是否为空，通过total_num判断
    if page_num['total_num'] == 0:
        print("新数据库搜索结果为空，正在搜索旧数据库")
        return find_in_old_database(text, question, question_keywords)
    else:
        return summary(result, question)


def find_in_old_database(text, question, question_keywords):
    total_num = Es_search.get_total('notices', question_keywords)
    # 获取搜索结果
    resp = Es_search.search_text('notices', question_keywords)

    # 整合为一个json格式的数据
    result = result_to_json(resp)
    print(result)
    # 获取页数相关内容
    page_num = pagenum_to_json(total_num, 0)

    # 判断结果是否为空，通过total_num判断
    if page_num['total_num'] == 0:
        print("搜索结果为空")
        # 如果搜索结果为空，调用GML模型，对问题进行回答
        answer = GML.GML_answer(question)
        # 将三者数据整合为一个json格式的数据，返回
        return answer
    else:
        return summary(result, question)

def summary(result, question):
    print("搜索结果不为空")
    text = ""
    # 如果不为空，获取查询的前三条数据，进行总结
    for i in range(0, len(result)):
        text += result[i]['text'] + "\n"
    release_time = result[0]['time'][:10][0:4]
    if len(text) > 2030:
        text = text[:2030]
        summary = GML.GML_answer(text, question)
        result = "截止于" + release_time + "年，" + summary
        print(result)
        return result
    else:
        # 找到不为空的text，进行总结
        summary = GML.GML_answer(text, question)
        result = "截止于" + release_time + "年，" + summary
        print(result)
        return result

'''
功能：将查询到的结果整合为json格式
'''

def result_to_json(resp):
    result = []
    for hit in resp['hits']['hits']:
        result.append({'title': hit['_source']['notice_title'],
                       'link': hit['_source']['notice_link'],
                       'text': hit['_source']['notice_text'],
                       'time': hit['_source']['notice_time'],
                       'department': hit['_source']['notice_department'],
                       'catalog': hit['_source']['notice_catalog'],
                       'creator': hit['_source']['notice_creator']
                       })
    return result


'''
功能：将查询到的页数整合为json格式
'''
def pagenum_to_json(total, start):
    pagenum = {}
    #计算总页数
    page = total // 10
    if total % 10 != 0:
        page += 1
    #设置当前页数
    pagenum['current'] = start // 10 + 1
    #设置总页数
    pagenum['total'] = page
    #设置总条数
    pagenum['total_num'] = total
    #设置每页条数
    pagenum['per_page'] = 10
    #设置是否有上一页
    if start == 0:
        pagenum['has_prev'] = False
    else:
        pagenum['has_prev'] = True
    #设置是否有下一页
    if start + 10 >= total:
        pagenum['has_next'] = False
    else:
        pagenum['has_next'] = True
    return pagenum


'''
功能：如果查询的结果，text为空，则循环遍历，直到找到不为空的text，或者所有text都为空
'''
def find_text(result):
    for i in range(1, len(result)):
        text = result[i]['text']
        if text != "nan":
            return text
    return "抱歉，没有找到相关内容"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
