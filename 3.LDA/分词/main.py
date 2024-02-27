import jieba
import pandas as pd
import pickle


# 加载文件
jieba.load_userdict("dict_lower.txt")
data = pd.read_csv("../../2.数据清洗/final_data/result.csv")

# 构造停用词
stop_words = []
with open('stopwords.txt', 'r', encoding='utf-8') as file:
    for line in file:
        stop_words.append(line.strip())
stop_words.append([',', '.', '/', '[', ']', '{', '\\', '}', '~', '`', '\'', '"', '=', ' ', '\n'])

# 分词
result_SE_front2back = []
result_SE_test = []
result_DATA_analysis = []
result_DATA_develop = []
result_WEB = []
result_CS_algorithm = []
result_CS_ai = []
result_CE = []
result_EE_embed = []
result_EE_electron = []
result_EE_navigation = []
result_EST_digital = []
result_EST_photoelectric = []
result_IC = []

for index in data.index:
    s1 = str(data.loc[index, '岗位详情'])
    s2 = str(data.loc[index, '岗位名称'])
    s = s1.lower() + s2.lower()
    result_list = [word.lower() for word in jieba.cut(s) if word.strip() not in stop_words
                   and word.strip() != ' ' and word.strip() != '\n' and word.strip() != '\t']
    if str(data.loc[index, '大类岗位']) == '导航':
        result_EE_navigation.append(result_list)
    elif str(data.loc[index, '大类岗位']) == '电气控制':
        result_EE_electron.append(result_list)
    elif str(data.loc[index, '大类岗位']) == '光电':
        result_EST_photoelectric.append(result_list)
    elif str(data.loc[index, '大类岗位']) == '集成电路':
        result_IC.append(result_list)
    elif str(data.loc[index, '大类岗位']) == '前后端':
        result_SE_front2back.append(result_list)
    elif str(data.loc[index, '大类岗位']) == '嵌入式':
        result_EE_embed.append(result_list)
    elif str(data.loc[index, '大类岗位']) == '人工智能':
        result_CS_ai.append(result_list)
    elif str(data.loc[index, '大类岗位']) == '软件测试':
        result_SE_test.append(result_list)
    elif str(data.loc[index, '大类岗位']) == '数据分析':
        result_DATA_analysis.append(result_list)
    elif str(data.loc[index, '大类岗位']) == '数据开发':
        result_DATA_develop.append(result_list)
    elif str(data.loc[index, '大类岗位']) == '数字电子':
        result_EST_digital.append(result_list)
    elif str(data.loc[index, '大类岗位']) == '算法':
        result_CS_algorithm.append(result_list)
    elif str(data.loc[index, '大类岗位']) == '通信技术':
        result_CE.append(result_list)
    elif str(data.loc[index, '大类岗位']) == '网络安全' or str(data.loc[index, '大类岗位']) == '网络运维':
        result_WEB.append(result_list)

# 输出并保存
with open('../导航.pkl', 'wb') as file:
    pickle.dump(result_EE_navigation, file)
with open('../电气控制.pkl', 'wb') as file:
    pickle.dump(result_EE_electron, file)
with open('../光电.pkl', 'wb') as file:
    pickle.dump(result_EST_photoelectric, file)
with open('../集成电路.pkl', 'wb') as file:
    pickle.dump(result_IC, file)
with open('../前后端.pkl', 'wb') as file:
    pickle.dump(result_SE_front2back, file)
with open('../嵌入式.pkl', 'wb') as file:
    pickle.dump(result_EE_embed, file)
with open('../人工智能.pkl', 'wb') as file:
    pickle.dump(result_CS_ai, file)
with open('../软件测试.pkl', 'wb') as file:
    pickle.dump(result_SE_test, file)
with open('../数据分析.pkl', 'wb') as file:
    pickle.dump(result_DATA_analysis, file)
with open('../数据开发.pkl', 'wb') as file:
    pickle.dump(result_DATA_develop, file)
with open('../数字电子.pkl', 'wb') as file:
    pickle.dump(result_EST_digital, file)
with open('../算法.pkl', 'wb') as file:
    pickle.dump(result_CS_algorithm, file)
with open('../通信技术.pkl', 'wb') as file:
    pickle.dump(result_CE, file)
with open('../网络安全.pkl', 'wb') as file:
    pickle.dump(result_WEB, file)
