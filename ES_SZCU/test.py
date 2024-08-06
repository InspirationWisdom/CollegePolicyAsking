import os
import json
import requests
import time
import datetime
import pandas as pd
import Elasticsearch.search as Es_search
import utils
import Spyder.spyderLink as Spyder
import LLM.GML as GML

# d定义一个字符串，含有链接
question_url = "http://news.szcu.edu.cn/2018/0305/c151a27334/page.htm"

#判断是否是链接,且提取对应链接
question_url = utils.get_url(question_url)

#判断文本中是否有链接
if question_url is not None:
    #调用爬虫，对网页进行内容爬取
    text = Spyder.scrape_webpage(question_url)
    #判断有没有爬取到内容
    if text is None:
        print("链接有误，无法爬取内容")
    else:
        #判断文本是否超过2040个字符
        if len(text) > 2040:
            #只截取2040个字符进行总结
            text = text[:2040]
            summary = GML.GML_summary(text)
            #对json格式的summer 的Data的 message,添加链接
            summary['Data']['message']['link'] = question_url
            print(summary)
        else:
            #爬取到内容，连接GML模型，将文字传入模型，进行总结
            summary = GML.GML_summary(text)
            #添加链接
            summary['Data']['message']['link'] = question_url
            print(summary)


else:
    print("没有链接")
