from flask import Flask, request, jsonify
from flask_cors import CORS
import utils
import json

from Elasticsearch import search as Es_search
import Spyder.spyderLink as Spyder
import LLM.GML as GML

app = Flask(__name__)

# 允许跨域请求
CORS(app, supports_credentials=True)

#编写接口
'''
功能：搜索文本，同时返回JSON格式的数据和页数相关内容
'''


@app.route('/search', methods=['GET', 'POST'])
def search():
    # # 获取POST请求中的数据
    # data = request.form['question']
    # 获取params请求中的数据
    question = request.args.get('question')
    #获取起始位置
    # 如果没有传入start参数，则默认为0
    start = request.args.get('start')
    if start is None:
        start = 0
    else:
        start = int(start)

    #调用get_total函数，获取搜索结果的总数
    total = Es_search.get_total('notices', question)
    #调用search_text函数，获取搜索结果
    resp = Es_search.search_text('notices', question, start)

    #将结果的title 和link 以json格式返回
    result = result_to_json(resp)

    #设置变量，存储页数相关内容
    page_num = pagenum_to_json(total, start)

    #response 添加 json格式的数据
    response = jsonify({'result': result}, {'pagenum': page_num})
    return response


"""
功能：连接GML功能，完成AI问答
"""


@app.route('/ChatAI', methods=['GET', 'POST'])
def ChatAI():
    # 获取POST请求中的数据
    question = request.args.get('question')
    question_url = utils.get_url(question)

    '''
    功能：如果提供链接，对提供的链接进行总结
    '''
    #判断文本中是否有链接
    if question_url is not None:
        #如果有链接，则调用爬虫，对网页进行内容爬取
        text = Spyder.scrape_webpage(question_url)
        #判断有没有爬取到内容
        if text is None:
            print("链接有误，无法爬取内容")
            return None
        else:
            #判断文本是否超过2040个字符
            if len(text) > 2030:
                #只截取2030个字符进行总结
                text = text[:2030]
                summary = GML.GML_summary(text)
                #添加是否大于2040个字符的标志
                summary['Data']['message']['link'] = question_url
                summary['Data']['message']['is_over'] = True
                #添加标记，判断是搜索Elasticsearch还是爬取网页
                summary['Data']['message']['is_search'] = False

            else:
                #爬取到内容，连接GML模型，将文字传入模型，进行总结
                summary = GML.GML_summary(text)
                summary['Data']['message']['link'] = question_url
                summary['Data']['message']['is_over'] = False
                #添加标记，判断是搜索Elasticsearch还是爬取网页
                summary['Data']['message']['is_search'] = False
                return summary

    else:
        #如果没有链接，进行Elasticsearch搜索
        #对问题进行关键词提取
        #只获取问题前2030个字符
        question = question[:2030]
        extra_question = GML.GML_search(question)

        #获取提取结果
        extra_question = extra_question['Data']['message']['content']
        #如果extraQuestion中有字符“关键词”，去除
        if "关键词" in extra_question:
            extra_question = extra_question.replace("关键词", "")
            extra_question = extra_question.replace("：", "")
        print(extra_question)

        # 获取搜索结果的总数
        total_num = Es_search.get_total('notices', extra_question)
        #获取搜索结果
        resp = Es_search.search_text('notices', extra_question)

        #整合为一个json格式的数据
        result = result_to_json(resp)
        #获取页数相关内容
        page_num = pagenum_to_json(total_num, 0)

        #判断结果是否为空，通过total_num判断
        if page_num['total_num'] == 0:
            print("搜索结果为空")
            #如果搜索结果为空，调用GML模型，对问题进行回答
            answer = GML.GML_answer(question)
            #将三者数据整合为一个json格式的数据，返回
            return jsonify({'result': result}, {'pagenum': page_num}, {'answer': answer})
        else:
            print("搜索结果不为空")
            #如果不为空，获取查询的第一条数据，进行总结
            text = result[0]['text']
            if len(text) > 2030:
                text = text[:2030]

                summary = GML.GML_answer(text, question)
                #添加标记，判断是搜索Elasticsearch还是爬取网页
                summary['Data']['message']['is_search'] = True
                #添加是第几条数据
                summary['Data']['message']['num'] = 1
                return jsonify({'result': result}, {'pagenum': page_num}, {'summary': summary})
            elif text == "nan":
                #for循环遍历，直到找到不为空的text，或者所有text都为空
                for i in range(1, len(result)):
                    text = result[i]['text']
                    if text != "nan":
                        #找到不为空的text，进行总结
                        summary = GML.GML_answer(text, question)
                        #添加标记，判断是搜索Elasticsearch还是爬取网页
                        summary['Data']['message']['is_search'] = True
                        #添加是第几条数据
                        summary['Data']['message']['num'] = i + 1
                        return jsonify({'result': result}, {'pagenum': page_num}, {'summary': summary})

                #如果所有text都为空，content:抱歉，没有找到相关内容
                summary = {'Data': {'message': {'content': '抱歉，没有找到相关内容'}}}
                #添加标记，判断是搜索Elasticsearch还是爬取网页
                summary['Data']['message']['is_search'] = True
                #添加是第几条数据
                summary['Data']['message']['num'] = 1
                return jsonify({'result': result}, {'pagenum': page_num}, {'summary': summary})
            else:
                #找到不为空的text，进行总结
                summary = GML.GML_answer(text, question)
                #添加标记，判断是搜索Elasticsearch还是爬取网页
                summary['Data']['message']['is_search'] = True
                #添加是第几条数据
                summary['Data']['message']['num'] = 1
                return jsonify({'result': result}, {'pagenum': page_num}, {'summary': summary})

    # 调用GML模型，返回json格式的数据
    return 0


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
    app.run(port=8888)
