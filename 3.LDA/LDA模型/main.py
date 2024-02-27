import pickle
import gensim
import os
import numpy as np
from sklearn.decomposition import PCA
from sklearn.decomposition import SparsePCA
from sklearn.cluster import KMeans


pass_num = 3  # LDA模型的迭代次数
topic_range = range(1, 10)


# 计算困惑度
def min_perplexity(f_dictionary, f_corpus):
    f_min_perplexity = 10000  # 最小的困惑度
    f_min_num = 0  # 困惑度最小的主题数
    for f_num in topic_range:
        f_lda_model = gensim.models.LdaModel(f_corpus, num_topics=f_num, id2word=f_dictionary, passes=pass_num)
        f_perplexity = f_lda_model.log_perplexity(f_corpus)
        if abs(f_perplexity) < f_min_perplexity:
            f_min_perplexity = abs(f_perplexity)
            f_min_num = f_num
        print(f'主题数量：{f_num} 困惑度：{f_perplexity}')
    print(f_min_num)
    return f_min_num


# 获取保存了结果的文件列表
file_paths = []
for filename in os.listdir('../'):
    if filename.endswith('.pkl'):
        file_paths.append(os.path.join('../', filename))

# 构建词袋模型
for file_path in file_paths:
    with open(file_path, 'rb') as file:
        result = pickle.load(file)
    dictionary = gensim.corpora.Dictionary(result)
    corpus = [dictionary.doc2bow(doc) for doc in result]
    # 比较困惑度
    print(file_path)
    topic_num = min_perplexity(dictionary, corpus)
    # 获取LDA模型
    lda_model = gensim.models.LdaModel(corpus, num_topics=topic_num, id2word=dictionary, passes=pass_num)
    _topics = lda_model.show_topics(num_words=50)  # 获取到主题及其词语分布
    write_string = ''
    for topic_id, topic_words in _topics:
        write_string += f'主题：{topic_id} 词项分布：{topic_words} \n'
        print(f'主题：{topic_id} 词项分布：{topic_words}')
    write_path = '../主题结果/' + file_path.lstrip('../').rstrip('.pkl') + '.txt'
    with open(write_path, 'w', encoding='utf-8') as f:
        f.write(write_string)
    # 处理结果
    topics = lda_model.get_topics()  # 所有主题及其词项分布的二维numpy数组
    topic_vectors = []
    for topic in topics:
        topic_vectors.append(topic.tolist())  # topic_vectors数组是一个普通数组，里面的每一项都是一个主题和它的词项分布
    # 获取TF-IDF模型
    tf_idf_model = gensim.models.TfidfModel(corpus)
    tf_idfs = tf_idf_model[corpus]
    dict_num = len(topics[0])  # 所有主题的语料库中词语是一样的，选择第一个主题计算即可
    vectors = []  # vectors数组是一个普通数组，里面的每一项都是一个文章的tf-idf词项分布
    for tf_idf in tf_idfs:
        result_list = [0] * dict_num
        for (index, num) in tf_idf:
            result_list[index] = num
        vectors.append(result_list)
    # vectors和topic_vectors中的词项顺序是相同的（即对应位置上的单词是一样的，值都是和概率呈正相关的，因此可以放在一起进行降维和聚类）
    # PCA降维
    dims = 64
    pca = PCA(n_components=dims)
    pca.fit(np.array(vectors))
    vectors = pca.transform(vectors)
    topic_vectors = pca.transform(np.array(topic_vectors))
    # kmeans聚类
    kmeans = KMeans(n_clusters=topic_num, init=topic_vectors, n_init=1)
    labels = kmeans.fit_predict(vectors)  # 返回的labels是vectors中每个元素也就是每篇文章的聚类结果numpy数组，形如[1, 2, 0,...]
    # 记录结果
    save_path = '../聚类结果/' + file_path.lstrip('../').rstrip('.pkl') + '.npy'
    np.save(save_path, labels)
