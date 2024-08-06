
import scrapy

#要建立一个Spider， 你必须用scrapy.Spider类创建一个子类，并确定了三个强制的属性 和 一个方法。
# name: 用于区别Spider。 该名字必须是唯一的，你不可以为不同的Spider设定相同的名字。
# allowed_domains: 包含了Spider允许爬取的域名(domain)列表(list)。 当OffsiteMiddleware启用时， 域名不在列表中的URL不会被跟进。
# start_urls: 包含了Spider在启动时进行爬取的url列表。 因此，第一个被获取到的页面将是其中之一。 后续的URL则从初始的URL获取到的数据中提取。
# parse()：parse(self, response) ：解析的方法，每个初始URL完成下载后将被调用，调用的时候传入从每一个URL传回的Response对象来作为唯一参数，主要作用如下：
#---- 负责解析返回的网页数据(response.body)，提取结构化数据(生成item)
#---- 生成需要下一页的URL请求。


from mySpider.items import ItcastItem


class ItcastSpider(scrapy.Spider):
    name = "itcast"
    allowed_domains = ["itcast.cn"]
    start_urls = ["http://www.itcast.cn/channel/teacher.shtml"]

    def parse(self, response):
        # filename = "teacher.html"
        # open(filename, 'wb').write(response.body)
        
        #存放老师信息的集合
        items = []

        #使用xpath获取老师信息的集合
        for each in response.xpath("//div[@class='li_txt']"):
            #将我们得到的数据封装到一个 `ItcastItem` 对象
            item = ItcastItem()
            #extract()方法返回的都是unicode字符串
            name = each.xpath("h3/text()").extract()
            title = each.xpath("h4/text()").extract()
            info = each.xpath("p/text()").extract()

            #xpath返回的是包含一个元素的列表
            item["name"] = name[0]
            item["title"] = title[0]
            item["info"] = info[0]

            items.append(item)

        # 直接返回最后数据
        return items
