import json
import re

from bs4 import BeautifulSoup
from Job import Job


class Parser:

    def __init__(self):
        pass

    # 请求某一页的所有招聘信息并处理
    def parse1(self, source):
        root = BeautifulSoup(source, 'html.parser')
        data = json.loads(root.body.pre.get_text())
        jobItems = data['resultbody']['job']['items']
        return jobItems

    # 请求详细的招聘信息并找到描述
    def parse2(self, source):
        root = BeautifulSoup(source, 'html.parser')
        data = root.find('div', class_='bmsg').get_text()
        return data

    # 从描述里筛选出有用的信息
    def filter(self, source):
        # 预处理字符串，去掉所有空白符和后面的职能类别
        source.strip()
        source.replace(" ", "")
        source.replace("\n", "")
        source.replace("\r", "")
        source.replace("\t", "")
        keyword = '职能类别'
        if re.search(keyword, source) is None:
            text = source
        else:
            index = re.search(keyword, source).span()[0]
            text = source[:index]
        # 按关键词截取
        duty_keywords = ['工作职责', '工作信息', '岗位职责', '岗位信息', '职位描述', '工作描述', '岗位描述', '职责描述']
        requirement_keywords = ['岗位要求', '任职资格', '工作要求', '任职要求', '职位要求']
        duty_result_index = -1
        requirement_result_index = -1
        for duty_keyword in duty_keywords:
            if re.search(duty_keyword, text) is None:
                continue
            duty_result_index = re.search(duty_keyword, text).span()[0]
            break
        for requirement_keyword in requirement_keywords:
            if re.search(requirement_keyword, text) is None:
                continue
            requirement_result_index = re.search(requirement_keyword, text).span()[0]

        # 通过索引判断并截取
        if duty_result_index < requirement_result_index:
            duty = text[duty_result_index:requirement_result_index]
            requirement = text[requirement_result_index:]
        elif duty_result_index > requirement_result_index:
            duty = text[duty_result_index:]
            requirement = text[requirement_result_index:duty_result_index]
        else:
            duty = None
            requirement = None

        return duty, requirement

    # 生成Job对象并返回
    def construct(self, type, jobItem, duty, requirement):
        job = Job(jobItem)
        job.set_duty(duty)
        job.set_requirement(requirement)
        job.set_type(type)
        return job
