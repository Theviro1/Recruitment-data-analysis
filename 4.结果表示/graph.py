import os
import re
import networkx as nx
import matplotlib.pyplot as plt
import gensim
import numpy
import numpy as np

n_keyword = 20  # 保留前多少位关键词项，50个太多了
path = '../结果归档/No2/主题结果/'  # 选择某一个结果归档
files = []
for filename in os.listdir(path):
    file = (filename.rstrip('.txt'), os.path.join(path, filename))
    files.append(file)
topic_vectors = []
topic_nums = []
_topic_vectors = []
for (filename, file_path) in files:
    vector = []
    _vector = []
    # 读取文件内容
    key = ''
    with open(file_path, 'r', encoding='utf-8') as f:
        print(file_path)
        content = f.read()
    # 获取词项
    result_list = content.split('\n')  # 获取全部主题
    # 处理每个主题
    plt.figure(figsize=(10, 10))
    G = nx.Graph()
    nodes = []
    edges = []
    positions = {}
    num = len(result_list)  # 总的主题数目
    topic_nums.append(num)
    width = 0.2  # 节点宽度
    start = -(width * (num-1)/2)  # 起始位置
    idx = 0  # 主题节点的偏移量
    for result in result_list:
        if len(result) == 0:
            break
        # 获取词项
        words = re.findall(r'[\u4e00-\u9fff]+', result)  # 词项列表
        words.remove('主题')
        words.remove('词项分布')
        vector.extend(words)  # 收集主题词项
        words = words[:n_keyword]  # 保留前n位关键词
        # 获取主题
        key = re.match(r'主题：\d', result).group().lstrip('主题：')
        # 构建nx的中心节点
        G.add_node(key)
        positions[key] = (start + idx*width, 0)
        for word in words:
            if word not in nodes:
                nodes.append(word)
            edges.append((key, word))
        idx += 1
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    pos = nx.circular_layout(G, scale=1, center=(0, 0))
    pos.update(positions)
    nx.draw(G, pos, with_labels=True, font_family='SimHei', node_size=700)
    # plt.savefig(path.rstrip('主题结果/') + '/关系图/' + filename + '.png', format='png')
    plt.close()
    # 收集主题
    _vector = vector
    vector = list(set(vector))
    topic_vectors.append(vector)
    _topic_vectors.append(_vector)
print(topic_vectors)
print(_topic_vectors)
# 词袋模型获取TF-IDF
dictionary = gensim.corpora.Dictionary(topic_vectors)
corpus = [dictionary.doc2bow(doc) for doc in topic_vectors]
_bows = []
for corp in corpus:
    bow = [0] * len(dictionary)
    for (index, value) in corp:
        bow[index] = value
    _bows.append(bow)
tf_idf_model = gensim.models.TfidfModel(corpus)
tf_idfs = tf_idf_model[corpus]
# 获取纯数值向量
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
# 获取能力值评分
print(topic_nums)
dictionary = gensim.corpora.Dictionary(_topic_vectors)
corpus = [dictionary.doc2bow(doc) for doc in _topic_vectors]
bows = []
for corp in corpus:
    bow = [0] * len(dictionary)
    for (index, value) in corp:
        bow[index] = value
    bows.append(bow)
# 计算词频
len_bows = len(bows)
len_topic = len(bows[0])
result = []
for i in range(len_topic):
    s = 0
    for j in range(len_bows):
        s += bows[j][i]
    result.append(s)
for i in range(len(result)):
    result[i] /= sum(result)
# 重新计算向量
for bow in _bows:
    for i in range(len(result)):
        bow[i] *= result[i]
for i in range(len_bows):
    print(str(round((np.linalg.norm(_bows[i])*50), 2)) + '    ' + str(sum(_bows[i])/topic_nums[i]))





