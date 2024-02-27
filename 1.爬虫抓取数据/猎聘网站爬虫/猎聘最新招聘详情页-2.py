import requests
import pandas as pd
import time
import random
from bs4 import BeautifulSoup
from lxml import etree
lst=[] #建立临时列表



#添加自己的cookie信息

cookie='添加cookie'

#建立请求头
headers = {
          'cookie':cookie,
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
          'Accept-Language': 'zh-CN,zh;q=0.9',
          'Cache-Control': 'max-age=0',
          'Connection': 'keep-alive',
          'Sec-Fetch-Dest': 'document',
          'Sec-Fetch-Mode': 'navigate',
          'Sec-Fetch-Site': 'none',
          'Sec-Fetch-User': '?1',
          'Upgrade-Insecure-Requests': '1',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
          'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
          'sec-ch-ua-mobile': '?0',
          'sec-ch-ua-platform': '"Windows"',
      }
        
sj = pd.read_excel('猎聘招聘主页数据.xlsx')            

ls = pd.read_excel('猎聘招聘主页数据.xlsx')['job_url']



for link in ls:
    try:
        response=requests.get(url=link,headers=headers,timeout=200)
        time.sleep(random.uniform(1,3)) #控制速度
        if '该职位已暂停招聘' not in response.text:
                detailDocument = etree.HTML(response.text)
                jobContent = detailDocument.xpath('//dd[@data-selector="job-intro-content"]//text()')[0]
                splitText = ['任职要求', '岗位要求', '任职资格', ]
                jobDescribe, jobRequirement = '', ''
                for text in splitText:
                    if text in jobContent:
                        jobDescribe = jobContent.split(text)[0]
                        jobRequirement = text + jobContent.split(text)[1]
        dic={}
        dic['job_url']=link
        try:
            dic['岗位职责']=jobDescribe
        except:
            dic['岗位职责']=''
        try:
            dic['岗位要求']=jobRequirement
        except:
            dic['岗位要求']=''
        
        lst.append(dic)
        
        print(link,'获取成功')
    except Exception as e:
        print(e)
                    



#插入临时列表
result=pd.DataFrame(lst)
result.drop_duplicates(subset=['job_url'],keep='first',inplace=True)



result2=pd.merge(sj, result, how='left', on='job_url')
result2 = result2.drop(result2[['job_url']], axis=1) 
result2.to_excel('猎聘最终招聘结果数据.xlsx',index=None)
