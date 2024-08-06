#这个文件用于一些常用的数据操作
import re
'''
功能：获取字符串，判断是否有链接，如果有则返回链接，没有则返回None
参数：字符串
'''
def get_url(text):
    url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)
    if len(url) > 0:
        return url[0]
    else:
        return None
