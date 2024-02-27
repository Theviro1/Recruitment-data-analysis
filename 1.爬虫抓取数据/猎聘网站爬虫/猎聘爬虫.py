#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
FILE_NAME: 猎聘爬虫 ;
DATE: 2023/10/07 ;
"""
import csv
import os
import time

from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By




def getData():
    url = 'https://www.liepin.com/zhaopin/?inputFrom=head_navigation&scene=init&workYearCode=0&ckId=hbb8h8u2n2bin824bu3pj05u7xtxeqgb'
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9527")
    # options.add_argument('--headless')
    # options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    # options.add_argument('--disable-infobars')  # 禁用浏览器正在被自动化程序控制的提示
    # options.add_argument("--disable-gpu")  # 禁用gpu

    driverPath = 'd:\\chromedriver87.exe'
    driver = webdriver.Chrome(options = options, executable_path = driverPath, )
    driver.implicitly_wait(30)
    try:
        driver.maximize_window()
    except:
        pass
    jobTypeList = ['安全工程师', '通信技术工程师',
                   '算法工程师', '导航技术工程师', '嵌入式软件工程师', '电子工程师', '光电技术工程师']
    keywords = [
        '网信安全、算法安全',
        '光纤、卫星、天线通信',
        'DSP算法、图像处理算法、控制算法、优化算法',
        'SLAM、定位、卫星导航',
        'FPGA、仿真测试',
        '电路设计、分析、单片机、电子元器件',
        '光电信息处理、光学系统设计与分析']
    for k in range(0, len(keywords)):
        jobType = jobTypeList[k]
        writeTitile(jobType)
        # jobType = '数据分析工程师'
        keywordList = keywords[k].split('、')
        count = 1
        for keyword in keywordList:
            driver.get(url)
            time.sleep(5)
            # keyword = '大数据'
            driver.find_element(by = By.XPATH, value = '//div[@class="jsx-4146333934 search-input"]/input').send_keys(
                    keyword)
            time.sleep(2)
            driver.find_element(by = By.XPATH, value = '//span[@class="jsx-4146333934 search-btn"]').click()
            for i in range(0, 6):
                time.sleep(5)
                document = etree.HTML(driver.page_source)
            
                divs = document.xpath('//div[@class="job-list-box"]/div')
                for m in range(1, len(divs)+1):
                    print('第 %s 条'%m)
                    district = divs[m-1].xpath('./div/div[1]/div/a/div[1]/div/div[2]//text()')[1]
                    
                    jobName = divs[m-1].xpath('./div/div[1]/div/a/div[1]/div/div[1]//text()')
                    jobName = ''.join(jobName)
                    salary = divs[m-1].xpath('./div/div[1]/div/a/div[1]/span//text()')
                    salary = ''.join(salary).replace('急聘', '')
                    company = divs[m-1].xpath('./div/div[1]/div/div/div/span//text()')
                    company = ''.join(company)
                    requirement = divs[m-1].xpath('./div/div[1]/div/a/div[2]//text()')
                    requirement = '-'.join(requirement)
                    companyTags = divs[m-1].xpath('./div/div[1]/div/div/div/div[2]//text()')
                    companyTags = '-'.join(companyTags)
                    
                    driver.find_element(by = By.XPATH, value = '//div[@class="job-list-box"]/div[%s]/div/div[1]/div/a'%m).click()
                    handles = driver.window_handles
                    driver.switch_to.window(handles[-1])
        
                    time.sleep(3)
                    if '该职位已暂停招聘' not in driver.page_source:
                        detailDocument = etree.HTML(driver.page_source)
                        jobContent = detailDocument.xpath('//dd[@data-selector="job-intro-content"]//text()')[0]
                        splitText = ['任职要求', '岗位要求', '任职资格', ]
                        jobDescribe, jobRequirement = '', ''
                        for text in splitText:
                            if text in jobContent:
                                jobDescribe = jobContent.split(text)[0]
                                jobRequirement = text + jobContent.split(text)[1]
            
                        datas = [count, jobType, jobName, salary, district, requirement, requirement, company, companyTags, district,
                                 companyTags, jobDescribe, jobRequirement]
                        print(datas)
                        saveData(jobType, datas)
                        count += 1

                    driver.close()
                    handles = driver.window_handles
                    driver.switch_to.window(handles[-1])
                    # break
                driver.find_element(by = By.XPATH, value = '//li[@title="Next Page"]').click()
                # break
        break

def writeTitile(jobType):
    with open('d:\\%s.csv'%jobType, 'w', encoding = 'utf-8-sig', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(['序号', '岗位类别', '岗位名称', '薪酬', '地点', '学历要求', '经验要求', '企业名称', '企业规模', '所属地域', '所属行业', '岗位职责',
                         '岗位要求'])

def saveData(jobType, data):
    with open('d:\\%s.csv'%jobType, 'a', encoding = 'utf-8-sig', newline = '') as f:
        writer = csv.writer(f)
        writer.writerow(data)

if __name__ == '__main__':
    
    getData()

