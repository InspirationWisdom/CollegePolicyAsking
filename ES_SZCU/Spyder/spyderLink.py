"""
@Description :   
@Author      :   刘诚志-Cjuicy
@Time        :   2024/04/07 12:20:59
"""

import requests
from bs4 import BeautifulSoup

def scrape_webpage(url):
    try:
        # 发送 HTTP 请求获取网页内容
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查是否成功获取页面

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # 提取所有文本内容
        all_text = soup.get_text()
        all_text = remove_whitespace(all_text)
        print(all_text)
        return all_text
    except requests.RequestException as e:
        print(f"Error fetching the webpage: {e}")
        return None

"""
功能：去除字符串中的空格和换行符
"""
def remove_whitespace(text):
    return " ".join(text.split())


# 要爬取的网页 URL
webpage_url = "http://dsjy.szcu.edu.cn/2021/0319/c2008a40349/page.htm"  # 替换为你想要爬取的网页地址
scrape_webpage(webpage_url)