
import scrapy
from selenium import webdriver
import time
import mySpider
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from mySpider.items import SZCUItem
import pandas as pd
import os


class SzcuSpider(scrapy.Spider):
    name = "SZCU"
    allowed_domains = ["szcu.edu.cn"]
    start_urls = ["https://www.szcu.edu.cn/_web/search/doSearch.do?locale=zh_CN&request_locale=zh_CN&_p=YXM9NCZ0PTExMSZkPTQzMSZwPTEmbT1TTiY_#"]
    time = time

    # 获取chrome浏览器的驱动，并且设置为无头模式）(初始化)
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=r'C:\Program Files\Google\Chrome\Application\chromedriver')

    #函数结束之后，关闭浏览器
    def __del__(self):
        self.driver.close()  

    def parse(self, response):
        self.driver.get(response.url)
        button = self.driver.find_element_by_xpath('//*[@id="search_head"]/div/div[2]/div[3]/input[1]')
        button.click()
        self.driver.implicitly_wait(10)

        #output 数据是新增的数据，还未保存在知识图谱之中
        #使用pd读取csv文件的第一条记录,获取最新的时间
        if not os.path.exists('output.csv'):
            with open('output.csv', 'w', encoding='utf-8') as f:
                f.write('notice_title,notice_link,notice_creator,notice_time,notice_catalog,notice_source,notice_text\n')
                #获取Notice_csv的最新时间
                df = pd.read_csv('Notice.csv', encoding='utf-8')
                last_time = df['notice_time'].iloc[0]
                last_time = pd.to_datetime(last_time)

                # last_time = pd.to_datetime('2024-01-15 10:39:53')
        else:
            df = pd.read_csv('output.csv', encoding='utf-8')
            last_time = df['notice_time'].iloc[0]
            last_time = pd.to_datetime(last_time)

        #判断是否有temp_output.csv文件，如果有，删除  (该文件为临时文件，保存一天内的临时数据)
        if os.path.exists('temp_output.csv'):
            os.remove('temp_output.csv')
        # print(last_time)
        
        
       
        #---------------------------------------------------------#
        #存放信息集合
        items = []

        #循环遍历，当时间早于最后一条记录的时间时，停止
        while True:
            
            #--------------------------------------------------------#
            #同步操作 scrapy 和 selenium
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.visibility_of_element_located(('xpath', '//*[@class="result_item clearfix"]')))
            #获取更新后的页面源码
            html = self.driver.page_source
            #创建 Scrapy 选择器,获取更新后的页面源码
            response = scrapy.Selector(text=html)
            #--------------------------------------------------------#

            #使用选择器获取界面通知列表
            element_list = response.xpath('//*[@class="result_item clearfix"]')

            #创建新页面 ------
            self.driver.execute_script("window.open('');")
            
            #获取界面需要的信息
            for element in element_list:
                #将我们得到的数据封装到一个 `ItcastItem` 对象
                item = SZCUItem()

                notice_creator = ''
                notice_time = ''
                notice_catalog = ''
                notice_source = ''


                #通知标题
                notice_title = element.xpath('h3/a/text()').extract()
                #通知链接
                notice_link = element.xpath('h3/a/@href').extract()
                #获取所有的span标签
                span_list = element.xpath('span/text()').extract()
                for span in span_list:
                    #通知创建者，且去除不需要的文字
                    if '创建者' in span:
                        notice_creator = span.replace('创建者:','')
                    #通知发布时间,且去除不需要的文字
                    elif '发布时间' in span:
                        notice_time = span.replace('发布时间:','')
                    #通知是否有目录，且去除不需要的文字
                    elif '目录' in span:
                        notice_catalog = span.replace('目录:','')
                    #通知是否有出处，且去除不需要的文字
                    elif '出处' in span:
                        notice_source = span.replace('出处:','')
                    
                #--------------------------------------------------------#
                '''
                这一页面是通知的具体内容，但是由于通知内容是动态加载的，所以需要转到新页面
                '''
                #转到新页面
                self.driver.switch_to.window(self.driver.window_handles[1])
                #点击通知链接，获取通知内容，如果链接失效，跳转到下一个链接
                try :
                    self.driver.get(notice_link[0])
                except :
                    continue
                #同步操作 scrapy 和 selenium
                wait = WebDriverWait(self.driver, 10)
                wait.until(EC.visibility_of_element_located(('xpath', '/html')))  
                 #获取更新后的页面源码
                html = self.driver.page_source

                #创建 Scrapy 选择器
                response = scrapy.Selector(text=html)

                #获取所有的p标签
                notice_text_list = response.xpath('//p//text()')
                notice_texts  = ''
                #获取界面所有的通知内容
                for notice_text in notice_text_list:
                    notice_text = notice_text.extract()
                    #去除空白符
                    notice_text = notice_text
                    #组合通知内容
                    notice_texts = notice_texts + '\n'+ notice_text

                '''
                这个浏览次数形同虚设，所以不需要获取
                '''     
                # #查找span空间中是否有“浏览次数”这个字段，如果有，就获取通知浏览次数
                # notice_view = ''
                # notice_views = response.xpath('//span/text()').extract()
                # for view in notice_views:
                #     if '浏览次数' in view:
                #         notice_view = view.replace('浏览次数：','')
                #         break
                
                '''
                爬取附件链接也失败了
                '''
                #查找span空间中是否有“附件”这个字段，如果有，就获取通知附件文本和链接
                # notice_files = ''
                # notice_file = response.xpath('//p//text()').extract()
                # print(1234567)
                # print(notice_file)
                # for file in notice_file:
                #     print(1234567)
                    
                    # if '附件' in file.extract():
                        # notice_file = file.replace('附件：','')
                        #获取附件链接
                        # notice_file_link = file.xpath('/a/@href').extract()
                        #获取附件文本
                        # notice_file_text = file.xpath('/a/text()').extract()
                        
                        # print(notice_file_link)
                        # print(notice_file_text)

                        #md链接格式组合链接和文本
                        # notice_files = notice_files + "\n" + '[' + notice_file_text + '](' + notice_file_link + ')'
                
                #--------------------------------------------------------#

                
                item["notice_title"] = notice_title[0]
                item["notice_link"] = notice_link[0]
                item["notice_creator"] = notice_creator
                item["notice_time"] = notice_time
                item["notice_catalog"] = notice_catalog                    
                item["notice_source"] = notice_source
                item["notice_text"] = notice_texts
                yield item
                #浏览次数形同虚设，所以不需要获取
                # item["notice_view"] = notice_view

                # item["notice_file"] = notice_files

                #将时间转换为时间格式
                notice_time = pd.to_datetime(notice_time)
                #如果时间早于最后一条记录的时间，停止
                if notice_time <= last_time:
                    break

                items.append(item)
                # yield item
            #--------------------------------------------------------#

            #关闭创建的新页面
            self.driver.close()
            #转到原来的页面
            self.driver.switch_to.window(self.driver.window_handles[0])

            

            #pd保存到指定文件,附加内容
            df = pd.DataFrame(items)
            #保存内容包含标题
            df.to_csv('temp_output.csv', encoding='utf-8', index=False)

            
            
            if notice_time <= last_time:
                break

            #利用文本定位，点击下一页
            self.driver.find_element_by_link_text('下一页').click()

        #将temp_output.csv文件的内容读取出来，保存到output.csv文件中的最前面                                                                          
        temp_output = pd.read_csv('temp_output.csv', encoding='utf-8')
        #获取output.csv文件的内容
        output = pd.read_csv('output.csv', encoding='utf-8')
        #合并两个文件的内容
        output = pd.concat([temp_output, output], ignore_index=True)
        #写回到output.csv文件中
        output.to_csv('output.csv', encoding='utf-8', index=False)
        


        #删除temp_output.csv文件

        # os.remove('temp_output.csv')
            
        # 直接返回最后数据
        return items
        
    
