import random
import time
from datetime import datetime
import urllib.parse

from Downloader import Downloader
from Parser import Parser
from Manager import Manager


class Executor:
    baseType = {
        '软件开发': ['前端', '后端', 'C/C++开发', 'Java开发', 'python开发', 'golang开发', '软件开发'],
        '数据分析': ['数据分析', '数据开发', '大数据'],
        '算法': ['数据结构与算法', ],
        '测试': ['软件测试', ],
        'AI': ['深度学习', '神经网络', '计算机视觉'],
        '安全': ['网络安全', '信息安全', '数据安全', '网信安全', '算法安全'],
        '通信技术': ['光纤', '卫星', '天线通信'],
        '通信算法': ['DSP', '图像处理', '控制', '优化'],
        '导航技术': ['SLAM', '定位', '卫星导航'],
        '嵌入式软件': ['FPGA', '仿真测试'],
        '电子': ['电路设计', '分析', '单片机', '电子元器件'],
        '光电技术': ['光电信息处理', '光学系统']
    }
    pageNum = 0
    keyword = ''
    timestamp = 0
    manager = Manager()
    parser = Parser()
    downloader = Downloader()

    def __init__(self):
        pass

    # 创建所有需要爬取的url
    def create_url(self):
        # 把每个关键词对应的所有50个url全部放入数据库
        for type in self.baseType:
            for keyword in self.baseType[type]:
                keyword = urllib.parse.quote(keyword, safe='')
                for pageNum in range(2, 51):
                    url = "https://we.51job.com/api/job/search-pc?" \
                          "api_key=51job&" \
                          "timestamp=&" \
                          f"keyword={keyword}&" \
                          "searchType=2&" \
                          "function=&" \
                          "industry=&" \
                          "jobArea=000000&" \
                          "jobArea2=&" \
                          "landmark=&" \
                          "metro=&" \
                          "salary=&" \
                          "workYear=&" \
                          "degree=&" \
                          "companyType=&" \
                          "companySize=&" \
                          "jobType=&" \
                          "issueDate=&" \
                          "sortType=0&" \
                          f"pageNum={pageNum}&" \
                          "requestId=&" \
                          "pageSize=20&" \
                          "source=1&" \
                          "accountId=&" \
                          "pageCode=sou%7Csou%7Csoulb"  # 没有填写timestamp时间戳，填写了关键词和页码
                    self.manager.push_url(url, type)

    # 爬取某一个url
    def scrape_url(self):
        # 取出一个url和他对应的type
        url, type = self.manager.pop_url()
        if url is None:
            return False
        # 查找timestamp属性并添加
        sub = 'timestamp='
        index = url.find(sub)
        timestamp = int(datetime.timestamp(datetime.now()))  # 获取当前时间戳
        url = url[:index + len(sub)] + str(timestamp) + url[index + len(sub):]  # 获取完整url
        print(url)
        # 执行
        try:
            data = self.downloader.download(url)  # 通过下载器获取到接口返回的字符串数据，里面是本页所有招聘信息的json字符串
            jobItems = self.parser.parse1(data)  # 通过解析器获取到返回的json数据数组，每一个元素都是一条招聘信息
            job = None
            for jobItem in jobItems:
                url = jobItem['jobHref']  # 获取到每一条招聘信息内的链接
                data = self.parser.parse2(self.downloader.download(url))  # 通过下载器获取到信息具体要求的字符串数据
                # 解析获取到的数据
                duty, requirement = self.parser.filter(data)  # 通过解析器获取到工作职责和要求的字符串
                if duty is None and requirement is None:  # 解析器没有找到任何一个关键词，这条数据弃用
                    continue
                # 获取对象
                job = self.parser.construct(type, jobItem, duty, requirement)
                self.manager.save(job)

        except Exception:
            pass
        return True




