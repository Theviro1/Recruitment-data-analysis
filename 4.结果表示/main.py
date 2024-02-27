import pandas
import numpy as np
import os
import locale


locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')
# 读取文件
data = pandas.read_csv('../2.数据清洗/final_data/result.csv')
file_paths = []
for filename in sorted(os.listdir('../3.LDA/聚类结果/'), key=locale.strxfrm):
    file_paths.append(os.path.join('../3.LDA/聚类结果/', filename))

labels = []
for file_path in file_paths:
    load_data = np.load(file_path).tolist()
    labels.append(load_data)

# 索引
idx = [0] * 14
for index in data.index:
    if str(data.loc[index, '大类岗位']) == '导航':
        data.loc[index, '分组'] = labels[0][idx[0]]
        idx[0] += 1
    elif str(data.loc[index, '大类岗位']) == '电气控制':
        data.loc[index, '分组'] = labels[1][idx[1]]
        idx[1] += 1
    elif str(data.loc[index, '大类岗位']) == '光电':
        data.loc[index, '分组'] = labels[2][idx[2]]
        idx[2] += 1
    elif str(data.loc[index, '大类岗位']) == '集成电路':
        data.loc[index, '分组'] = labels[3][idx[3]]
        idx[3] += 1
    elif str(data.loc[index, '大类岗位']) == '前后端':
        data.loc[index, '分组'] = labels[4][idx[4]]
        idx[4] += 1
    elif str(data.loc[index, '大类岗位']) == '嵌入式':
        data.loc[index, '分组'] = labels[5][idx[5]]
        idx[5] += 1
    elif str(data.loc[index, '大类岗位']) == '人工智能':
        data.loc[index, '分组'] = labels[6][idx[6]]
        idx[6] += 1
    elif str(data.loc[index, '大类岗位']) == '软件测试':
        data.loc[index, '分组'] = labels[7][idx[7]]
        idx[7] += 1
    elif str(data.loc[index, '大类岗位']) == '数据分析':
        data.loc[index, '分组'] = labels[8][idx[8]]
        idx[8] += 1
    elif str(data.loc[index, '大类岗位']) == '数据开发':
        data.loc[index, '分组'] = labels[9][idx[9]]
        idx[9] += 1
    elif str(data.loc[index, '大类岗位']) == '数字电子':
        data.loc[index, '分组'] = labels[10][idx[10]]
        idx[10] += 1
    elif str(data.loc[index, '大类岗位']) == '算法':
        data.loc[index, '分组'] = labels[11][idx[11]]
        idx[11] += 1
    elif str(data.loc[index, '大类岗位']) == '通信技术':
        data.loc[index, '分组'] = labels[12][idx[12]]
        idx[12] += 1
    elif str(data.loc[index, '大类岗位']) == '网络安全' or str(data.loc[index, '大类岗位']) == '网络运维':
        data.loc[index, '分组'] = labels[13][idx[13]]
        idx[13] += 1
data.to_csv('result.csv', index=False)
