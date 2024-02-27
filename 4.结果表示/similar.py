import os
import re
import gensim
import numpy as np


path = '../结果归档/No2/主题结果/'  # 选择某一个结果归档
files = []
remove_words = ['主题', '词项分布', '团队', '项目', '能力', '深入', '研究', '研发', '沟通', '解决', '实验室', '需求', '规范', '学习', '合作', '文档', '流程', '功能', '技术', '独立', '资源', '原理', '描述', '企业', '规划', '海外', '市场', '销售', '采购', '工具', '运营', '指标', '智慧', '报告', '方向', '专家', '建议', '评估', '逻辑', '岗位', '海量', '经验', '建议', '支持', '推动', '发展', '主流', '应急', '解决方案', '优化', '信息', '协助', '量产', '撰写', '系统', '语言', '方案', '分析', '理解', '论文', '探索', '前沿', '常见', '发表', '目标', '限于', '评分', '风险', '场景', '风控', '生成', '关键', '谈判', '开拓', '旅游', '各类', '竞争力', '重建', '责任心', '订单', '推广', '全球', '部门', '质量', '关系', '业绩', '目标', '创新', '建立', '成本', '资格', '知识', '空间', '解决问题', '建设', '职位', '提升', '过程', '意识', '协调', '国内外', '估计', '理论', '模型', '姿态', '构建']
for filename in os.listdir(path):
    file = (filename.rstrip('.txt'), os.path.join(path, filename))
    files.append(file)
topic_vectors = []
for (filename, file_path) in files:
    vector = []
    # 读取文件内容
    key = ''
    with open(file_path, 'r', encoding='utf-8') as f:
        print(file_path)
        content = f.read()
    # 获取词项
    result_list = content.split('\n')  # 获取全部主题
    for result in result_list:
        if len(result) == 0:
            break
        # 获取词项
        words = re.findall(r'[\u4e00-\u9fff]+|[a-z]+', result)  # 词项列表
        for remove_word in remove_words:
            if remove_word in words:
                words.remove(remove_word)  # 删除所有非专业词项（职业能力）
        vector.extend(words)  # 收集主题词项
    topic_vectors.append(list(set(vector)))
print(topic_vectors)
# 词袋模型获取TF-IDF
dictionary = gensim.corpora.Dictionary(topic_vectors)
corpus = [dictionary.doc2bow(doc) for doc in topic_vectors]
tf_idf_model = gensim.models.TfidfModel(corpus)
tf_idfs = tf_idf_model[corpus]
# 获取词项分布向量
bows = []
for corp in corpus:
    bow = [0] * len(dictionary)
    for (index, value) in corp:
        bow[index] = value
    bows.append(bow)
print(bows)
# 获取纯数值的tf-idf向量
topic_vectors = []
for tf_idf in tf_idfs:
    vector = [0] * len(dictionary)
    for (index, value) in tf_idf:
        vector[index] = value
    topic_vectors.append(vector)
# 获取相似度计算
similarity = []
for vector1 in topic_vectors:
    sim = []
    for vector2 in topic_vectors:
        dot_product = np.dot(vector1, vector2)
        norm1 = np.linalg.norm(vector1)
        norm2 = np.linalg.norm(vector2)
        cos_theta = dot_product/(norm1*norm2)
        sim.append(round(cos_theta*100, 1))
    similarity.append(sim)
for elem in similarity:
    print(elem)
# 获取能力值计算结果，使用范数
for vector in topic_vectors:
    print(round(sum(vector), 2))
