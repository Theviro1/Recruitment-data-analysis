import requests
import pandas as pd
import time
import random
from bs4 import BeautifulSoup
from lxml import etree
lst=[] #建立临时列表



#添加自己的cookie信息

cookie='这里添加cookie'

#建立请求头
headers = {
    
'Accept': 'application/json, text/plain, */*',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
'Cache-Control': 'no-cache',
'Connection': 'keep-alive',
'Content-Length': '475',
'Content-Type': 'application/json;charset=UTF-8;',
'Cookie':cookie,
'Host': 'apic.liepin.com',
'Origin': 'https://www.liepin.com',
'Pragma': 'no-cache',
'Referer': 'https://www.liepin.com/',
'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
'sec-ch-ua-mobile': '?0',
'sec-ch-ua-platform': "Windows",
'Sec-Fetch-Dest': 'empty',
'Sec-Fetch-Mode': 'cors',
'Sec-Fetch-Site': 'same-site',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
'X-Client-Type': 'web',
'X-Fscp-Bi-Stat': '{"location": "https://www.liepin.com/zhaopin/?currentPage=1&pageSize=40&city=410&dq=410&pubTime=&key=java&suggestTag=&otherCity=&industry=&sfrom=search_job_pc&skId=jpleldqp9r2of9kqrzqdgpia8z7ki4z8&fkId=jpleldqp9r2of9kqrzqdgpia8z7ki4z8&ckId=jpleldqp9r2of9kqrzqdgpia8z7ki4z8&scene=page&suggestId="}',
'X-Fscp-Fe-Version': '3d319d8',
'X-Fscp-Std-Info': '{"client_id": "40108"}',
'X-Fscp-Trace-Id': 'ca7b891c-9a49-410b-9d4f-cc791659b2b5',
'X-Fscp-Version': '1.1',
'X-Requested-With': 'XMLHttpRequest'
    
            }

url='https://apic.liepin.com/api/com.liepin.searchfront4c.pc-search-job'


count = 1
for key_word in ['C/C++开发',	'Java开发',	'python开发',	'golang开发',	'数据分析',	'数据开发',	'大数据',	'数据结构与算法',	'软件测试',	'深度学习',	'神经网络',	'计算机视觉',	'网络安全',	'信息安全',	'数据安全',	'网信安全',	'算法安全',	'光纤',	'卫星',	'天线通信',	'DSP',	'图像处理',	'控制',	'优化',	'SLAM',	'定位',	'卫星导航',	'FPGA',	'仿真测试',	'电路设计',	'分析',	'单片机',	'电子元器件',	'光电信息处理',	'光学系统']:

    for city in ['410','010','020','050020','050090','060080','060020','070020','170020']:
        for page in range(0,5): #翻页输出800条 5*40
            # print(page)
            time.sleep(random.uniform(3,6))
            #建立请求参数
            data={
                "data":{
                    "mainSearchPcConditionForm":{
                        "city":city,
                        "dq":city,
                        "pubTime":"",
                        "currentPage":page,
                        "pageSize":40,
                        "key":key_word,
                        "workYearCode":"0",
                        "compId":"",
                        "compName":"",
                        "compTag":"",
                        "industry":"",
                        "salary":"",
                        "jobKind":"",
                        "compScale":"",
                        "compKind":"",
                        "compStage":"",
                        "eduLevel":""
                    },
                    "passThroughForm":{
                        "ckId":"2jcwvrp2srrhqdua5y0xv7jc9t7vf58b",
                        "scene":"page",
                        "skId":"jpleldqp9r2of9kqrzqdgpia8z7ki4z8",
                        "fkId":"jpleldqp9r2of9kqrzqdgpia8z7ki4z8",
                        "sfrom":"search_job_pc"
                    }
                }
            }
            try:
                html = requests.post(url=url, headers=headers, json=data,timeout=200)
                
                sj=html.json()['data']['data']['jobCardList']#json解析
                
                
                # ['序号', '岗位类别', '岗位名称', '薪酬', '地点', '学历要求', '经验要求', '企业名称', '企业规模', '所属地域', '所属行业', '岗位职责',                         '岗位要求']
                #循环json
                for i in sj:
                    dic={}
                    dic['jobId']=i.get("job").get("jobId")
                    dic['序号']=count
                    dic['岗位类别']=key_word
                    dic['岗位名称']=i.get("job").get("title")
                    dic['薪酬']=i.get("job").get("salary")
                    dic['地点']=i.get("job").get("dq")
                    dic['学历要求']=i.get("job").get("requireEduLevel")
                    dic['经验要求']=i.get("job").get("requireWorkYears")
                    dic['企业名称']=i.get("comp").get("compName")
                    dic['企业规模']=i.get("comp").get("compScale")
                    dic['所属地域']=i.get("job").get("dq")
                    dic['所属行业']=i.get("comp").get("compIndustry")
                    dic['job_url']=i.get("job").get("link")
    
                    
    
                    lst.append(dic)
                    print(f'正在获取关键字:{key_word},第{page}页数据第{count}条数据获取成功')
                    count += 1
            except Exception as e:  
                print(e)




#插入临时列表
result=pd.DataFrame(lst)
result.drop_duplicates(subset=['job_url'],keep='first',inplace=True)
result.to_excel('猎聘招聘主页数据.xlsx',index=None,encoding='utf-8-sig')  


